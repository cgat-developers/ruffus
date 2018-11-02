#! /usr/bin/env python

from __future__ import print_function
import ruffus
import ruffus.drmaa_wrapper
import os
import sys
import time


try:
    import drmaa
    HAVE_DRMAA = True
    DRMAA_SESSION = drmaa.Session()
    DRMAA_SESSION.initialize()

except ImportError:
    HAVE_DRMAA = False


logger, logger_mutex = ruffus.cmdline.setup_logging("me", "test.log", 1)

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path, "..", "..")))

workdir = 'tmp_test_job_history_with_exceptions'
# sub-1s resolution in system?
one_second_per_job = None
throw_exception = False


def run_job(infile, outfile, **kwargs):
    if not kwargs.get("run_locally", False):
        kwargs["drmaa_session"] = DRMAA_SESSION

    print("%s start to run " % infile)
    stdout, stderr = ruffus.drmaa_wrapper.run_job(
        cmd_str="sleep 100 && hostname > {}".format(os.path.abspath(outfile)),
        verbose=1,
        local_echo=False,
        logger=logger,
        **kwargs)
    print("%s completed" % infile)


@ruffus.mkdir(workdir)
@ruffus.originate([workdir + "/" + prefix + "_name.tmp1" for prefix in "abcdefghijk"])
def generate_initial_files1(on):
    with open(on, 'w') as outfile:
        pass


@ruffus.transform(generate_initial_files1,
                  ruffus.suffix(".tmp1"), ".tmp2")
def test_task2(infile, outfile):
    run_job(infile, outfile)


@ruffus.transform(test_task2, ruffus.suffix(".tmp2"), ".tmp3")
def test_task3(infile, outfile):
    run_job(infile, outfile)


def cleanup_tmpdir():
    os.system('rm -f %s %s' %
              (os.path.join(workdir, '*'), ruffus.RUFFUS_HISTORY_FILE))


def do_main():
    print("Press Ctrl-C Now!!", file=sys.stdout)
    sys.stdout.flush()
    time.sleep(2)
    print("Start....", file=sys.stdout)
    sys.stdout.flush()
    ruffus.pipeline_run(verbose=5,
                        pool_manager="gevent",
                        multiprocess=5,
                        pipeline="main")
    print("too late!!", file=sys.stdout)
    sys.stdout.flush()
    cleanup_tmpdir()


do_main()
