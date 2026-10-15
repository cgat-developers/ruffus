"""History keys must identify files independently of the launch directory."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import warnings

from ruffus import Pipeline, dbdict, suffix
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus.ruffus_utility import open_job_history, get_history_file_path


class TestHistoryPaths(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        self.directory = TemporaryDirectory()
        self.root = Path(self.directory.name).resolve()

    def tearDown(self):
        os.chdir(self.cwd)
        self.directory.cleanup()

    def test_changed_working_directory_and_moved_project(self):
        for level in (1, 2, 3):
            with self.subTest(level=level):
                project = self.root / str(level)
                project.mkdir()
                (project / 'metadata').mkdir()
                (project / 'launch').mkdir()
                calls = []

                def write_output(outfile):
                    calls.append(outfile)
                    Path(outfile).write_text('complete')

                pipeline = Pipeline(self.id() + str(level))
                pipeline.originate(write_output, str(project / 'output'))
                options = dict(verbose=0, multiprocess=1, checksum_level=level,
                               history_file=str(project / 'metadata/history.sqlite'))
                os.chdir(project)
                pipeline.run(**options)
                os.chdir(project / 'launch')
                pipeline.run(**options)
                self.assertEqual(len(calls), 1)
                history = open_job_history(options['history_file'])
                self.assertEqual(list(history), ['../output'])
                self.assertEqual(history['../output'].outfile, '../output')
                history.close()

                os.chdir(self.root)
                moved = self.root / ('moved' + str(level))
                project.rename(moved)
                relocated = Pipeline(self.id() + 'moved' + str(level))
                relocated.originate(write_output, str(moved / 'output'))
                options['history_file'] = str(moved / 'metadata/history.sqlite')
                relocated.run(**options)
                self.assertEqual(len(calls), 1)
                # Missing outputs must still cause execution.
                (moved / 'output').unlink()
                relocated.run(**options)
                self.assertEqual(len(calls), 2)

    def test_legacy_history_is_preserved_but_not_trusted(self):
        filename = str(self.root / 'history.sqlite')
        legacy = dbdict.open(filename, picklevalues=True)
        legacy['output'] = 'old checkpoint'
        legacy.close()
        with self.assertWarnsRegex(UserWarning, 'working-directory-relative'):
            history = open_job_history(filename)
        self.assertEqual(list(history), [])
        row = history.con.execute('SELECT key, value FROM ruffus_legacy_history').fetchone()
        self.assertEqual(row[0], 'output')
        self.assertEqual(history.pickle_loads(row[1]), 'old checkpoint')
        history['new-output'] = 'new checkpoint'
        history.close()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            history = open_job_history(filename)
        self.assertEqual(caught, [])
        self.assertEqual(history['new-output'], 'new checkpoint')
        history.close()

    def test_dependencies_and_failed_job_cleanup(self):
        (self.root / 'metadata').mkdir()
        (self.root / 'launch').mkdir()
        filename = str(self.root / 'metadata/history.sqlite')
        calls = []
        fail = []

        def source(outfile):
            calls.append('source')
            if fail:
                raise RuntimeError('failed job must lose its checkpoint')
            Path(outfile).write_text('input')

        def transform(infile, outfile):
            calls.append('transform')
            Path(outfile).write_text(Path(infile).read_text())

        pipeline = Pipeline(self.id())
        pipeline.originate(source, str(self.root / 'input.txt'))
        pipeline.transform(transform, source, suffix('.txt'), '.out')
        options = dict(verbose=0, multiprocess=1, checksum_level=1,
                       history_file=filename)
        os.chdir(self.root)
        pipeline.run(**options)
        os.chdir(self.root / 'launch')
        pipeline.run(**options)
        self.assertEqual(calls, ['source', 'transform'])
        fail.append(True)
        with self.assertRaises(RethrownJobError):
            pipeline.run(forcedtorun_tasks=[source], **options)
        history = open_job_history(filename)
        self.assertNotIn('../input.txt', history)
        self.assertIn('../input.out', history)
        history.close()

    def test_memory_history_keeps_its_original_base(self):
        os.chdir(self.root)
        history = open_job_history(':memory:')
        output = self.root / 'output'
        self.assertEqual(get_history_file_path(str(output), history), 'output')
        os.chdir(self.cwd)
        self.assertEqual(get_history_file_path(str(output), history), 'output')
        history.close()


if __name__ == '__main__':
    unittest.main()
