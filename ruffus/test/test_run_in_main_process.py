"""Mixed local/process execution, including nested multiprocessing."""

import json
import multiprocessing
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import threading
import time
import unittest
from uuid import uuid4

from ruffus import Pipeline, originate, pipeline_run, run_in_main_process, suffix
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus.ruffus_utility import open_job_history, get_history_file_path


def record_process(outfile):
    Path(outfile).write_text(json.dumps({
        'pid': os.getpid(), 'daemon': multiprocessing.current_process().daemon,
    }))


def copy_file(infile, outfile):
    Path(outfile).write_text(Path(infile).read_text())


def failing_worker(outfile):
    raise RuntimeError('worker failed')


def exclusive_job(outfile, lockfile):
    with open(lockfile, 'x'):
        try:
            time.sleep(0.05)
            record_process(outfile)
        finally:
            os.unlink(lockfile)


class TestRunInMainProcess(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.pipeline = Pipeline(uuid4().hex)
        self.options = dict(multiprocess=2, verbose=0,
                            history_file=str(self.root / 'history.sqlite'))

    def test_nested_process_and_ordinary_worker_overlap(self):
        calls = []
        caller_thread = threading.get_ident()
        worker_output = self.root / 'worker.txt'
        child_output = self.root / 'child.txt'

        def local(outfile):
            self.assertEqual(threading.get_ident(), caller_thread)
            self.assertEqual(os.getpid(), parent_pid)
            self.assertFalse(multiprocessing.current_process().daemon)
            calls.append('local')
            # The independent worker must be able to finish while this task runs.
            deadline = time.monotonic() + 20
            while not worker_output.exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue(worker_output.exists())
            child = multiprocessing.get_context('spawn').Process(
                target=record_process, args=(str(child_output),))
            child.start()
            try:
                child.join(20)
                self.assertEqual(child.exitcode, 0)
            finally:
                if child.is_alive():
                    child.terminate()
                    child.join()
            Path(outfile).write_text('local')

        parent_pid = os.getpid()
        self.pipeline.originate(local, str(self.root / 'local.txt')).run_in_main_process().jobs_limit(1)
        # A concurrency limit of one alone must still use a pool worker.
        self.pipeline.originate(record_process, str(worker_output)).jobs_limit(1)
        self.pipeline.transform(copy_file, local, suffix('.txt'), '.copy')
        self.pipeline.run(**self.options)
        self.pipeline.run(**self.options)
        self.assertEqual(calls, ['local'])
        self.assertEqual((self.root / 'local.copy').read_text(), 'local')
        worker = json.loads(worker_output.read_text())
        self.assertNotEqual(worker['pid'], parent_pid)
        self.assertTrue(worker['daemon'])
        self.assertNotEqual(json.loads(child_output.read_text())['pid'], parent_pid)

    def test_decorator_multiple_jobs_and_clone(self):
        calls = []

        def local(outfile):
            calls.append(threading.get_ident())
            Path(outfile).write_text('done')

        local.__name__ = 'local_' + uuid4().hex
        originate([str(self.root / ('output%d' % i)) for i in range(5)])(local)
        run_in_main_process()(local)
        pipeline_run(target_tasks=[local], **self.options)
        self.assertEqual(calls, [threading.get_ident()] * 5)
        self.pipeline.originate(record_process, str(self.root / 'cloned')).run_in_main_process()
        cloned = self.pipeline.clone(uuid4().hex)
        cloned.run(**self.options)
        self.assertEqual(json.loads((self.root / 'cloned').read_text())['pid'], os.getpid())

    def test_local_failure_invalidates_history_and_stops_dependents(self):
        fail = []
        output = self.root / 'local.txt'

        def local(outfile):
            Path(outfile).write_text('output')
            if fail:
                raise RuntimeError('local task failed')

        self.pipeline.originate(local, str(output)).run_in_main_process()
        self.pipeline.transform(copy_file, local, suffix('.txt'), '.copy')
        self.pipeline.run(**self.options)
        (self.root / 'local.copy').unlink()
        fail.append(True)
        with self.assertRaisesRegex(RethrownJobError, 'local task failed'):
            self.pipeline.run(forcedtorun_tasks=[local], **self.options)
        self.assertFalse((self.root / 'local.copy').exists())
        history = open_job_history(self.options['history_file'])
        self.assertNotIn(get_history_file_path(str(output), history), history)
        history.close()

    def test_worker_failure_stops_local_dependents(self):
        calls = []

        def local(infile, outfile):
            calls.append('unexpected')

        self.pipeline.originate(failing_worker, str(self.root / 'input.txt'))
        self.pipeline.transform(local, failing_worker, suffix('.txt'), '.out').run_in_main_process()
        with self.assertRaisesRegex(RethrownJobError, 'worker failed'):
            self.pipeline.run(**self.options)
        self.assertEqual(calls, [])

    def test_named_job_limit_shared_with_workers(self):
        limit = uuid4().hex
        lockfile = str(self.root / 'exclusive.lock')
        for name in ('local', 'worker'):
            task = self.pipeline.originate(
                exclusive_job, [str(self.root / (name + str(i))) for i in range(4)],
                extras=[lockfile], name=name).jobs_limit(1, limit)
            if name == 'local':
                task.run_in_main_process()
        self.pipeline.run(**self.options)
        for i in range(4):
            self.assertEqual(json.loads((self.root / ('local' + str(i))).read_text())['pid'], os.getpid())
            self.assertNotEqual(json.loads((self.root / ('worker' + str(i))).read_text())['pid'], os.getpid())

    def test_thread_and_serial_modes(self):
        for mode in ('thread', 'serial'):
            with self.subTest(mode=mode):
                pipeline = Pipeline(uuid4().hex)
                calls = []

                def local(outfile):
                    calls.append(threading.get_ident())
                    record_process(outfile)

                pipeline.originate(local, str(self.root / mode)).run_in_main_process()
                options = dict(self.options, multiprocess=1)
                if mode == 'thread':
                    options['multithread'] = 2
                pipeline.run(**options)
                self.assertEqual(calls, [threading.get_ident()])

    def test_gevent_rejected_before_pool_creation(self):
        self.pipeline.originate(record_process, str(self.root / 'output')).run_in_main_process()
        with self.assertRaisesRegex(ValueError, 'pool_manager'):
            self.pipeline.run(pool_manager='gevent', **self.options)


if __name__ == '__main__':
    unittest.main()
