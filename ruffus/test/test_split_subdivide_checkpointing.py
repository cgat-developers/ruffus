#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
from ruffus import pipeline_run, pipeline_printout, Pipeline, formatter, originate, subdivide, split
import time
import sys

"""

    test_split_subdivide_checkpointing.py


"""
import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Each time the pipeline is FORCED to rerun,
#       More files are created for each task


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


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
    output_file_names = []
    for i in range(n_to_produce):
        output_file_name = '{}_{}.subdivided'.format(infile_basename, i)
        open(output_file_name, 'a').close()
        output_file_names.append(output_file_name)


TEST_VERBOSITY = 0


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
                raise Exception("Unexpected file %s" % (tempdir + ne))

    def test_newstyle_ruffus(self):

        test_pipeline = Pipeline("test")
        test_pipeline.originate(task_func=make_start,
                                output=[tempdir + 'start'])
        test_pipeline.split(task_func=split_start,
                            input=make_start, output=tempdir + '*.split')
        test_pipeline.subdivide(task_func=subdivide_start, input=split_start, filter=formatter(
        ), output=tempdir + '{basename[0]}_*.subdivided', extras=[tempdir + '{basename[0]}'])

        expected_files_after_1_runs = ["start", "0.split", "0_0.subdivided"]
        expected_files_after_2_runs = [
            "1.split", "0_1.subdivided", "1_0.subdivided"]
        expected_files_after_3_runs = [
            "2.split", "0_2.subdivided", "1_1.subdivided", "2_0.subdivided"]
        expected_files_after_4_runs = [
            "3.split", "0_3.subdivided", "1_2.subdivided", "2_1.subdivided", "3_0.subdivided"]

        print("     1 Run pipeline normally...")
        test_pipeline.run(multiprocess=10, verbose=TEST_VERBOSITY)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs,
                                                  expected_files_after_2_runs)
        print("     2 Check that running again does nothing. (All up to date).")
        test_pipeline.run(multiprocess=10, verbose=TEST_VERBOSITY)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs,
                                                  expected_files_after_2_runs)
        time.sleep(2)

        print("     3 Running again with forced tasks to generate more files...")
        test_pipeline.run(forcedtorun_tasks=[
                          "test::make_start"], multiprocess=10, verbose=TEST_VERBOSITY)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                  + expected_files_after_2_runs,
                                                  expected_files_after_3_runs)
        print("     4 Check that running again does nothing. (All up to date).")
        test_pipeline.run(multiprocess=10, verbose=TEST_VERBOSITY)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                  + expected_files_after_2_runs,
                                                  expected_files_after_3_runs)
        time.sleep(2)

        print("     5 Running again with forced tasks to generate even more files...")
        test_pipeline.run(forcedtorun_tasks=make_start,
                          multiprocess=10, verbose=TEST_VERBOSITY)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                  + expected_files_after_2_runs
                                                  + expected_files_after_3_runs,
                                                  expected_files_after_4_runs)
        print("     6 Check that running again does nothing. (All up to date).")
        test_pipeline.run(multiprocess=10, verbose=TEST_VERBOSITY)
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                  + expected_files_after_2_runs
                                                  + expected_files_after_3_runs,
                                                  expected_files_after_4_runs)

    def test_ruffus(self):

        expected_files_after_1_runs = ["start", "0.split", "0_0.subdivided"]
        expected_files_after_2_runs = [
            "1.split", "0_1.subdivided", "1_0.subdivided"]
        expected_files_after_3_runs = [
            "2.split", "0_2.subdivided", "1_1.subdivided", "2_0.subdivided"]
        expected_files_after_4_runs = [
            "3.split", "0_3.subdivided", "1_2.subdivided", "2_1.subdivided", "3_0.subdivided"]

        print("     1 Run pipeline normally...")
        pipeline_run(multiprocess=10, verbose=TEST_VERBOSITY, pipeline="main")
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs,
                                                  expected_files_after_2_runs)
        print("     2 Check that running again does nothing. (All up to date).")
        pipeline_run(multiprocess=10, verbose=TEST_VERBOSITY, pipeline="main")
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs,
                                                  expected_files_after_2_runs)

        time.sleep(2)

        print("     3 Running again with forced tasks to generate more files...")
        pipeline_run(forcedtorun_tasks=[
                     make_start], multiprocess=10, verbose=TEST_VERBOSITY, pipeline="main")
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                  + expected_files_after_2_runs,
                                                  expected_files_after_3_runs)
        print("     4 Check that running again does nothing. (All up to date).")
        pipeline_run(multiprocess=10, verbose=TEST_VERBOSITY, pipeline="main")
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                  + expected_files_after_2_runs,
                                                  expected_files_after_3_runs)
        time.sleep(2)

        print("     5 Running again with forced tasks to generate even more files...")
        pipeline_run(forcedtorun_tasks=[
                     make_start], multiprocess=10, verbose=TEST_VERBOSITY, pipeline="main")
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                  + expected_files_after_2_runs
                                                  + expected_files_after_3_runs,
                                                  expected_files_after_4_runs)
        time.sleep(2)
        print("     6 Check that running again does nothing. (All up to date).")
        pipeline_run(multiprocess=10, verbose=TEST_VERBOSITY, pipeline="main")
        self.check_file_exists_or_not_as_expected(expected_files_after_1_runs
                                                  + expected_files_after_2_runs
                                                  + expected_files_after_3_runs,
                                                  expected_files_after_4_runs)


if __name__ == '__main__':
    if len(sys.argv) > 1 and "-v" == sys.argv.pop():
        TEST_VERBOSITY = 7
    unittest.main()
