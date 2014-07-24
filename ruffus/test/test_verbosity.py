#!/usr/bin/env python
from __future__ import print_function
"""

    test_verbosity.py

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

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *
from ruffus import (pipeline_run, pipeline_printout, suffix, transform, split,
                    merge, dbdict, follows)
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus.ruffus_utility import (RUFFUS_HISTORY_FILE,
                                   CHECKSUM_FILE_TIMESTAMPS)



parser = cmdline.get_argparse(description='WHAT DOES THIS PIPELINE DO?')
options = parser.parse_args()
logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)


#---------------------------------------------------------------
#   create initial files
#
@originate([   ['/data/scratch/lg/what/one/two/three/job1.a.start', 'job1.b.start'],
               ['/data/scratch/lg/what/one/two/three/job2.a.start', 'job2.b.start'],
               ['/data/scratch/lg/what/one/two/three/job3.a.start', 'job3.b.start']    ])
def create_initial_file_pairs(output_files):
    # create both files as necessary
    for output_file in output_files:
        with open(output_file, "w") as oo: pass

#---------------------------------------------------------------
#   first task
@transform(create_initial_file_pairs, suffix(".start"), ".output.1")
def first_task(input_files, output_file):
    with open(output_file, "w"): pass


#---------------------------------------------------------------
#   second task
@transform(first_task, suffix(".output.1"), ".output.2")
def second_task(input_files, output_file):
    with open(output_file, "w"): pass

class Test_verbosity(unittest.TestCase):
    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path1
    #___________________________________________________________________________
    def test_printout_abbreviated_path1(self):
        """Input file exists, output doesn't exist"""
        s = StringIO()
        pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 1)
        self.assertTrue(re.search('Job needs update: Missing files\n\s+'
                      '\[\.\.\./job2\.a\.start, job2\.b\.start, \.\.\./job2.a.output.1\]', s.getvalue()))

    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path2
    #___________________________________________________________________________
    def test_printout_abbreviated_path2(self):
        """Input file exists, output doesn't exist"""
        s = StringIO()
        pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 2)
        self.assertTrue('[.../three/job1.a.start, job1.b.start, .../three/job1.a.output.1]' in s.getvalue())


    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path2
    #___________________________________________________________________________
    def test_printout_abbreviated_path3(self):
        """Input file exists, output doesn't exist"""
        s = StringIO()
        pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 3)
        self.assertTrue('[.../two/three/job1.a.start, job1.b.start, .../two/three/job1.a.output.1]' in s.getvalue())

    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path9
    #___________________________________________________________________________
    def test_printout_abbreviated_path9(self):
        """Input file exists, output doesn't exist"""
        s = StringIO()
        pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 9)
        ret = s.getvalue()
        self.assertTrue('[/data/scratch/lg/what/one/two/three/job2.a.start, job2.b.start,' in ret)


    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path0
    #___________________________________________________________________________
    def test_printout_abbreviated_path0(self):
        """Input file exists, output doesn't exist"""
        s = StringIO()
        pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 0)
        ret = s.getvalue()
        self.assertTrue('[[/data/scratch/lg/what/one/two/three/job2.a.start,' in ret)
        self.assertTrue('/home/lg/src/oss/ruffus/ruffus/test/job2.b.start]' in ret)


    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path_minus_60
    #___________________________________________________________________________
    def test_printout_abbreviated_path_minus_60(self):
        """Input file exists, output doesn't exist"""
        s = StringIO()
        pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = -60)
        ret = s.getvalue()
        self.assertTrue('[<???> ratch/lg/what/one/two/three/job2.a.start, job2.b.start]' in ret)

#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    unittest.main()

