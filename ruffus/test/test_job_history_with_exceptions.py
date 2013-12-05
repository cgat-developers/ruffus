#!/usr/bin/env python
"""

    test_job_history_with_exceptions.py

        Make sure that when an exception is thrown only the current and following tasks fail

"""


import unittest
import os
import sys
import shutil
from StringIO import StringIO
import time
import re

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *
from ruffus import (pipeline_run, pipeline_printout, suffix, transform, split,
                    merge, dbdict, follows)
#from ruffus.combinatorics import *
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus.ruffus_utility import (RUFFUS_HISTORY_FILE,
                                   CHECKSUM_FILE_TIMESTAMPS)

workdir = 'tmp_test_job_history_with_exceptions'
#sub-1s resolution in system?
one_second_per_job = True
throw_exception = False
#___________________________________________________________________________
#
#   generate_initial_files1
#___________________________________________________________________________
@originate([workdir +  "/" + prefix + "_name.tmp1" for prefix in "abcd"])
def generate_initial_files1(on):
    with open(on, 'w') as outfile:
        pass

#___________________________________________________________________________
#
#   generate_initial_files2
#___________________________________________________________________________
@originate([workdir +  "/e_name.tmp1", workdir +  "/f_name.tmp1"])
def generate_initial_files2(on):
    with open(on, 'w') as outfile:
        pass

#___________________________________________________________________________
#
#   generate_initial_files3
#___________________________________________________________________________
@originate([workdir +  "/g_name.tmp1", workdir +  "/h_name.tmp1"])
def generate_initial_files3(on):
    with open(on, 'w') as outfile:
        pass

#___________________________________________________________________________
#
#   generate_initial_files1
#___________________________________________________________________________
@originate(workdir +  "/i_name.tmp1")
def generate_initial_files4(on):
    with open(on, 'w') as outfile:
        pass

#___________________________________________________________________________
#
#   test_task2
#___________________________________________________________________________
@collate([generate_initial_files1, generate_initial_files2, generate_initial_files3,
            generate_initial_files4],
         formatter(),
         "{path[0]}/all.tmp2")
#@transform([generate_initial_files1, generate_initial_files2, generate_initial_files3,
#            generate_initial_files4],
#            formatter( ),
#            "{path[0]}/{basename[0]}.tmp2")
def test_task2( infiles, outfile):
    with open(outfile, "w") as p:
        pass

#___________________________________________________________________________
#
#   test_task3
#___________________________________________________________________________
@transform(test_task2, suffix(".tmp2"), ".tmp3")
def test_task3( infile, outfile):
    global throw_exception
    throw_exception = not throw_exception
    if throw_exception:
        #print >>sys.stderr, "Throw exception for ", infile, outfile
        raise Exception("oops")
    else:
        #print >>sys.stderr, "No throw exception for ", infile, outfile
        pass
    with open(outfile, "w") as p: pass

#___________________________________________________________________________
#
#   test_task4
#___________________________________________________________________________
@transform(test_task3, suffix(".tmp3"), ".tmp4")
def test_task4( infile, outfile):
    with open(outfile, "w") as p: pass




def cleanup_tmpdir():
    os.system('rm -f %s %s' % (os.path.join(workdir, '*'), RUFFUS_HISTORY_FILE))


class Test_job_history_with_exceptions(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(workdir)
        except OSError:
            pass

    #___________________________________________________________________________
    #
    #   test product() pipeline_printout and pipeline_run
    #___________________________________________________________________________
    def test_job_history_with_exceptions(self):
        cleanup_tmpdir()
        s = StringIO()
        pipeline_printout(s, [test_task4], verbose=5, wrap_width = 10000)
        #print s.getvalue()

    def test_job_history_with_exceptions_run(self):
        """Run"""
        for i in range(1):
            # output is up to date, but function body changed (e.g., source different)
            cleanup_tmpdir()
            try:
                pipeline_run([test_task4], verbose = 0,
                             #multithread = 2,
                             one_second_per_job = one_second_per_job)
            except:
                pass
            s = StringIO()
            pipeline_printout(s, [test_task4], verbose=5, wrap_width = 10000)
            #
            # task 2 should be up to date because exception was throw in task 3
            #
            pipeline_printout_str = s.getvalue()
            correct_order = not re.search('Tasks which will be run:.*\n(.*\n)*Task = test_task2', pipeline_printout_str)
            if not correct_order:
                print pipeline_printout_str
            self.assertTrue(correct_order)
            sys.stderr.write(".")
        print



    #___________________________________________________________________________
    #
    #   cleanup
    #___________________________________________________________________________
    def tearDown(self):
        pass
        shutil.rmtree(workdir)



#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    #pipeline_printout(sys.stdout, [test_product_task], verbose = 5)
    unittest.main()
