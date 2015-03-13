#!/usr/bin/env python
from __future__ import print_function
"""

    test_job_history_with_exceptions.py

        Make sure that when an exception is thrown only the current and following tasks fail

"""


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
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *
from ruffus import (pipeline_run, pipeline_printout, suffix, transform, split,
                    merge, dbdict, follows)
#from ruffus.combinatorics import *
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus.drmaa_wrapper import run_job
from ruffus.ruffus_utility import (RUFFUS_HISTORY_FILE,
                                   CHECKSUM_FILE_TIMESTAMPS,
                                    get_default_history_file_name)

workdir = 'tmp_test_job_history_with_exceptions'
#sub-1s resolution in system?
one_second_per_job = None
throw_exception = False
#___________________________________________________________________________
#
#   generate_initial_files1
#___________________________________________________________________________
@mkdir(workdir)
@originate([workdir +  "/" + prefix + "_name.tmp1" for prefix in "abcdefghijk"])
def generate_initial_files1(on):
    with open(on, 'w') as outfile:
        pass


#___________________________________________________________________________
#
#   test_task2
#___________________________________________________________________________
@transform(generate_initial_files1,
         suffix(".tmp1"), ".tmp2")
def test_task2( infile, outfile):
    print ("%s start to run " % infile)
    run_job("./five_second.py", run_locally = True)
    print ("%s wake up " % infile)
    with open(outfile, "w") as p:
        pass

#___________________________________________________________________________
#
#   test_task3
#___________________________________________________________________________
@transform(test_task2, suffix(".tmp2"), ".tmp3")
def test_task3( infile, outfile):
    print ("%s start to run " % infile)
    #subprocess.check_call("./five_second.py")
    run_job("./five_second.py", run_locally = True)
    print ("%s wake up " % infile)
    with open(outfile, "w") as p:
        pass


def cleanup_tmpdir():
    os.system('rm -f %s %s' % (os.path.join(workdir, '*'), RUFFUS_HISTORY_FILE))


def do_main ():
    print("Press Ctrl-C Now!!", file=sys.stdout)
    sys.stdout.flush()
    time.sleep(2)
    print("Start....", file=sys.stdout)
    sys.stdout.flush()
    pipeline_run(verbose = 11,
                 multiprocess = 5, pipeline= "main")
    print("too late!!", file=sys.stdout)
    sys.stdout.flush()
    cleanup_tmpdir()

do_main()
