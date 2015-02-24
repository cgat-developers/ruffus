#!/usr/bin/env python
from __future__ import print_function
"""

    test_split_subdivide_checkpointing.py


"""








#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import sys
import os
import os.path
import re
import operator
from collections import defaultdict
import random
import json

try:
    import StringIO as io
except:
    import io as io
import re

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__


from ruffus import pipeline_run, pipeline_printout
from ruffus import originate
from ruffus import split
from ruffus import transform
from ruffus import subdivide
from ruffus import formatter


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Each time the pipeline is FORCED to rerun,
#       More files are created for each task


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


tempdir = "./testing_dir/"


@originate([tempdir + 'start'])
def make_start(outfile):
    """
    -> start
    """
    open(outfile, 'w').close()


@split(make_start, tempdir + '*.split')
def split_start(infiles, outfiles):
    """
    -> XXX.split
        where XXX = 0 .. N,
              N   = previous N + 1
    """

    # split always runs exactly one job (unlike @subdivide)
    # So it implicitly combines all its inputs before running and generating multiple output
    # @originate generates multiple output so the input for @split is a list...
    infile = infiles[0]

    # clean up previous
    for f in outfiles:
        os.unlink(f)


    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #   Create more files than the previous invocation
    #
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    n_to_produce = len(outfiles) + 1
    for i in range(n_to_produce):
        f = '{}{}.split'.format(tempdir, i)
        open(f, 'a').close()



@subdivide(split_start, formatter(), tempdir + '{basename[0]}_*.subdivided', tempdir + '{basename[0]}')
def subdivide_start(infile, outfiles, infile_basename):
    # cleanup existing
    for f in outfiles:
        os.unlink(f)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #   Create more files than the previous invocation
    #
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    n_to_produce = len(outfiles) + 1
    for i in range(    n_to_produce):
        open('{}_{}.subdivided'.format(infile_basename, i), 'a').close()


import unittest, shutil
try:
    from StringIO import StringIO
except:
    from io import StringIO


class Test_ruffus(unittest.TestCase):

    def tearDown(self):
        # only tear down if not throw exception so we can debug?
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass
        os.makedirs(tempdir)

    def check_file_exists_or_not_as_expected(self, expected_files, not_expected_files):
        """
        Check if files exist / not exist
        """
        for ee in expected_files:
            if not os.path.exists(tempdir + ee):
                raise Exception("Expected file %s" % (tempdir + ee))
        for ne in not_expected_files:
            if os.path.exists(tempdir + ne):
                raise Exception("Unexpected file %s" % (tempdir + ne ))



    def test_ruffus (self):

        expected_files_after_1_runs = ["start", "0.split", "0_0.subdivided"]
        expected_files_after_2_runs = ["1.split", "0_1.subdivided", "1_0.subdivided"]
        expected_files_after_3_runs = ["2.split", "0_2.subdivided", "1_1.subdivided", "2_0.subdivided"]
        expected_files_after_4_runs = ["3.split", "0_3.subdivided", "1_2.subdivided", "2_1.subdivided", "3_0.subdivided"]

        print("     Run pipeline normally...")
        pipeline_run(multiprocess = 10, verbose=0)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs,
                                                 expected_files_after_2_runs)

        print("     Check that running again does nothing. (All up to date).")
        pipeline_run(multiprocess = 10, verbose=0)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs,
                                                 expected_files_after_2_runs)

        print("     Running again with forced tasks to generate more files...")
        pipeline_run(forcedtorun_tasks = [make_start], multiprocess = 10, verbose=0)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                 + expected_files_after_2_runs,
                                                 expected_files_after_3_runs)

        print("     Check that running again does nothing. (All up to date).")
        pipeline_run(multiprocess = 10, verbose=0)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                 + expected_files_after_2_runs,
                                                 expected_files_after_3_runs)


        print("     Running again with forced tasks to generate even more files...")
        pipeline_run(forcedtorun_tasks = [make_start], multiprocess = 10, verbose=0)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                 + expected_files_after_2_runs
                                                 + expected_files_after_3_runs,
                                                 expected_files_after_4_runs)
        print("     Check that running again does nothing. (All up to date).")
        pipeline_run(multiprocess = 10, verbose=0)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                 + expected_files_after_2_runs
                                                 + expected_files_after_3_runs,
                                                 expected_files_after_4_runs)


if __name__ == '__main__':
    unittest.main()


