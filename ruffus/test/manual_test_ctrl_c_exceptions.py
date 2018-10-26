#! /usr/bin/env python

from __future__ import print_function
from ruffus.ruffus_utility import RUFFUS_HISTORY_FILE, CHECKSUM_FILE_TIMESTAMPS, get_default_history_file_name
from ruffus.drmaa_wrapper import run_job
from ruffus.ruffus_exceptions import RethrownJobError
import ruffus

import unittest
import os
import sys
import shutil
try:
    from StringIO import StringIO
except:
    from io import StringIO
import time
import re
import subprocess

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path, "..", "..")))

# from ruffus.combinatorics import *


workdir = 'tmp_test_job_history_with_exceptions'
# sub-1s resolution in system?
one_second_per_job = None
throw_exception = False

@ruffus.mkdir(workdir)
@ruffus.originate([workdir + "/" + prefix + "_name.tmp1" for prefix in "abcdefghijk"])
def generate_initial_files1(on):
    with open(on, 'w') as outfile:
        pass


@ruffus.transform(generate_initial_files1,
           ruffus.suffix(".tmp1"), ".tmp2")
def test_task2(infile, outfile):
    print("%s start to run " % infile)
    run_job("./five_second.py", run_locally=True)
    print("%s wake up " % infile)
    with open(outfile, "w") as p:
        pass


@ruffus.transform(test_task2, ruffus.suffix(".tmp2"), ".tmp3")
def test_task3(infile, outfile):
    print("%s start to run " % infile)
    # subprocess.check_call("./five_second.py")
    run_job("./five_second.py", run_locally=True)
    print("%s wake up " % infile)
    with open(outfile, "w") as p:
        pass


def cleanup_tmpdir():
    os.system('rm -f %s %s' %
              (os.path.join(workdir, '*'), RUFFUS_HISTORY_FILE))


def do_main():
    print("Press Ctrl-C Now!!", file=sys.stdout)
    sys.stdout.flush()
    time.sleep(2)
    print("Start....", file=sys.stdout)
    sys.stdout.flush()
    ruffus.pipeline_run(verbose=11,
                        multiprocess=5, pipeline="main")
    print("too late!!", file=sys.stdout)
    sys.stdout.flush()
    cleanup_tmpdir()


do_main()
