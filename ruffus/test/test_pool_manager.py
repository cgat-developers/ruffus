import contextlib
import random
import unittest
import ruffus
import ruffus.drmaa_wrapper
import os
import shutil
import glob
import tempfile

try:
    import gevent
    HAVE_GEVENT = True
except ImportError:
    HAVE_GEVENT = False

try:
    import drmaa
    HAVE_DRMAA = True
    DRMAA_SESSION = drmaa.Session()
    DRMAA_SESSION.initialize()

except ImportError:
    HAVE_DRMAA = False


ROOT = os.path.abspath(os.path.dirname(__file__))
TESTS_TEMPDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))

# number of cores used for testing parallelism
NUM_CORES = 4


@contextlib.contextmanager
def temp_cd(target):
    curdir = os.path.curdir
    os.chdir(target)
    yield
    os.chdir(curdir)


def save_pid(outfile):
    with open(outfile + ".pid", "w") as outf:
        outf.write("{}".format(os.getpid()))


def create_files(outfile):
    with open(outfile, "w") as outf:
        outf.write("\n".join(map(
            str,
            random.sample(range(0, 1000), 100))) + "\n")
    save_pid(outfile)


def compute_mean(infile, outfile):
    """compute mean"""
    with open(infile, "r") as inf:
        n = [float(x.strip()) for x in inf.readlines()]

    with open(outfile, "w") as outf:
        outf.write("{}\n".format(sum(n) / len(n)))
    save_pid(outfile)


def run_job(infile, outfile, **kwargs):
    if not kwargs.get("run_locally", False):
        kwargs["drmaa_session"] = DRMAA_SESSION

    stdout, stderr = ruffus.drmaa_wrapper.run_job(
        cmd_str="hostname > {}".format(os.path.abspath(outfile)),
        verbose=1,
        local_echo=False,
        **kwargs)


def run_local_job1(*args):
    return run_job(*args, run_locally=True)


def run_local_job2(*args):
    return run_job(*args, run_locally=True)


def run_remote_job1(*args):
    return run_job(*args, run_locally=False)


def run_remote_job2(*args):
    return run_job(*args, run_locally=False)


def combine_means(infiles, outfile):
    with open(outfile, "w") as outf:
        for infile in infiles:
            with open(infile) as inf:
                outf.write(inf.read())
    save_pid(outfile)


class BaseTest(unittest.TestCase):

    expected_output_files = ["sample_{:02}.mean".format(x) for x in range(10)] +\
                            ["sample_{:02}.txt".format(x) for x in range(10)]

    def setUp(self):
        try:
            os.makedirs(TESTS_TEMPDIR)
        except OSError:
            pass
        self.work_dir = tempfile.mkdtemp(suffix="",
                                         prefix="ruffus_tmp_{}_".format(
                                             self.id()),
                                         dir=TESTS_TEMPDIR)

    def tearDown(self):
        # shutil.rmtree(self.work_dir)
        pass

    def check_files(self, present=[], absent=[]):
        for fn in present:
            path = os.path.join(self.work_dir, fn)
            self.assertTrue(os.path.exists(path),
                            "file {} does not exist".format(path))
        for fn in absent:
            path = os.path.join(self.work_dir, fn)
            self.assertFalse(os.path.exists(path),
                             "file {} does exist but not expected".format(path))

    def build_pipeline(self, pipeline_name, **kwargs):
        # fudge: clear all previous pipelines
        ruffus.Pipeline.clear_all()
        pipeline = ruffus.Pipeline(pipeline_name)

        task_create_files = pipeline.originate(
            task_func=create_files,
            output=["sample_{:02}.txt".format(x) for x in range(10)])

        task_compute_mean = pipeline.transform(
            task_func=compute_mean,
            input=task_create_files,
            filter=ruffus.suffix(".txt"),
            output=".mean")

        task_combine_means = pipeline.merge(
            task_func=combine_means,
            input=task_compute_mean,
            output="means.txt")

        task_run_local_job1 = pipeline.transform(
            task_func=run_local_job1,
            input=task_create_files,
            filter=ruffus.suffix(".txt"),
            output=".local1")

        # test jobs_limit with local running
        task_run_local_job2 = pipeline.transform(
            task_func=run_local_job2,
            input=task_create_files,
            filter=ruffus.suffix(".txt"),
            output=".local2").jobs_limit(NUM_CORES // 2)

        # multiprocessing and DRMAA do not work at the moment likely
        # cause is the shared session object.
        if not HAVE_DRMAA or (kwargs.get("multiprocess", 1) > 1):
            return

        task_run_remote_job1 = pipeline.transform(
            task_func=run_remote_job1,
            input=task_create_files,
            filter=ruffus.suffix(".txt"),
            output=".remote1")

        # test jobs_limit with remote running
        task_run_remote_job2 = pipeline.transform(
            task_func=run_remote_job2,
            input=task_create_files,
            filter=ruffus.suffix(".txt"),
            output=".remote2").jobs_limit(NUM_CORES // 2)

    def run_pipeline(self, **kwargs):
        pipeline = self.build_pipeline(self.id(), **kwargs)
        with temp_cd(self.work_dir):
            ruffus.pipeline_run(pipeline=pipeline, verbose=5, **kwargs)
        self.check_files(self.expected_output_files)

    def read_pids(self):
        pids = []
        for fn in glob.glob(os.path.join(self.work_dir, "*.pid")):
            with open(fn) as inf:
                pids.append(int(inf.readline().strip()))
        return pids


class TestExecutionEngines(BaseTest):

    def test_pipeline_runs_with_multiprocessing(self):
        self.run_pipeline(multiprocess=NUM_CORES)
        pids = self.read_pids()
        self.assertEqual(len(set(pids)), NUM_CORES)

    def test_pipeline_runs_with_multithreading(self):
        self.run_pipeline(multithread=NUM_CORES)
        pids = self.read_pids()
        self.assertEqual(len(set(pids)), 1)
        self.assertEqual(pids[0], os.getpid())

    @unittest.skipIf(not HAVE_GEVENT, "no gevent installed")
    def test_pipeline_runs_with_gevent_manager(self):
        self.run_pipeline(multithread=NUM_CORES, pool_manager="gevent")
        pids = self.read_pids()
        self.assertEqual(len(set(pids)), 1)
        self.assertEqual(pids[0], os.getpid())

    def test_pipeline_fails_with_unknown_manager(self):
        self.assertRaises(ValueError,
                          self.run_pipeline,
                          multithread=NUM_CORES,
                          pool_manager="mystical_manager")


if __name__ == "__main__":
    unittest.main()
