#!/usr/bin/env python
"""

    test_regex_error_messages.py

        test product, combine, permute, combine_with_replacement

"""


import unittest
import os
import sys
import shutil
from StringIO import StringIO
import time

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *
from ruffus import (pipeline_run, pipeline_printout, suffix, transform, split,
                    merge, dbdict, follows)
from ruffus.ruffus_exceptions import *
from ruffus.ruffus_utility import (RUFFUS_HISTORY_FILE)

workdir = 'tmp_test_regex_error_messages'
#sub-1s resolution in system?
one_second_per_job = None
parallelism = 1
#___________________________________________________________________________
#
#   generate_initial_files1
#___________________________________________________________________________
@originate([workdir +  "/" + prefix + "_name.tmp1" for prefix in "abcd"])
def generate_initial_files1(out_name):
    with open(out_name, 'w') as outfile:
        pass

#___________________________________________________________________________
#
#   test_regex_task
#___________________________________________________________________________
@transform(
        generate_initial_files1,
        regex("(.*)/(?P<PREFIX>[abcd])(_name)(.tmp1)"),
        r"\1/\g<PREFIX>\3.tmp2",# output file
        r"\2",                  # extra: prefix = \2
        r"\g<PREFIX>",          # extra: prefix = \2
        r"\4")                  # extra: extension
def test_regex_task(infiles, outfile,
                    prefix1,
                    prefix2,
                    extension):
    with open(outfile, "w") as p:
        pass

    if prefix1 != prefix2:
        raise Exception("Expecting %s == %s" % (prefix1, prefix2))


#___________________________________________________________________________
#
#   test_regex_unmatched_task
#___________________________________________________________________________
@transform(
        generate_initial_files1,
        regex("(.*)/(?P<PREFIX>[abcd])(_name)(.xxx)"),
        r"\1/\g<PREFIXA>\3.tmp2",# output file
        r"\2",                  # extra: prefix = \2
        r"\g<PREFIX>",          # extra: prefix = \2
        r"\4")                  # extra: extension
def test_regex_unmatched_task(infiles, outfile,
                    prefix1,
                    prefix2,
                    extension):
    raise Exception("Should blow up first")


#___________________________________________________________________________
#
#   test_suffix_task
#___________________________________________________________________________
@transform(
        generate_initial_files1,
        suffix(".tmp1"),
        r".tmp2",           # output file
        r"\1")              # extra: basename
def test_suffix_task(infile, outfile,
                    basename):
    with open (outfile, "w") as f: pass


#___________________________________________________________________________
#
#   test_suffix_unmatched_task
#___________________________________________________________________________
@transform(
        generate_initial_files1,
        suffix(".tmp1"),
        r".tmp2",           # output file
        r"\2")              # extra: unknown
def test_suffix_unmatched_task(infiles, outfile, unknown):
    raise Exception("Should blow up first")


#___________________________________________________________________________
#
#   test_suffix_unmatched_task
#___________________________________________________________________________
@transform(
        generate_initial_files1,
        suffix(".tmp2"),
        r".tmp2")           # output file
def test_suffix_unmatched_task2(infiles, outfile):
    raise Exception("Should blow up first")



#___________________________________________________________________________
#
#   test_product_misspelt_capture_error_task
#___________________________________________________________________________
@transform(
        generate_initial_files1,
        regex("(.*)/(?P<PREFIX>[abcd])(_name)(.tmp)"),
        r"\1/\g<PREFIXA>\3.tmp2",# output file
        r"\2",                  # extra: prefix = \2
        r"\g<PREFIX>",          # extra: prefix = \2
        r"\4")                  # extra: extension
def test_regex_misspelt_capture_error_task(infiles, outfile,
                    prefix1,
                    prefix2,
                    extension):
    raise Exception("Should blow up first")


#___________________________________________________________________________
#
#   test_regex_misspelt_capture2_error_task
#___________________________________________________________________________
@transform(
        generate_initial_files1,
        regex("(.*)/(?P<PREFIX>[abcd])(_name)(.tmp)"),
        r"\1/\g<PREFIX>\3.tmp2",# output file
        r"\2",                  # extra: prefix = \2
        r"\g<PREFIXA>",          # extra: prefix = \2
        r"\4")                  # extra: extension
def test_regex_misspelt_capture2_error_task(infiles, outfile,
                    prefix1,
                    prefix2,
                    extension):
    raise Exception("Should blow up first")


#___________________________________________________________________________
#
#   test_regex_out_of_range_regex_reference_error_task
#___________________________________________________________________________
@transform(
        generate_initial_files1,
        regex("(.*)/(?P<PREFIX>[abcd])(_name)(.tmp)"),
        r"\1/\g<PREFIX>\5.tmp2",# output file
        r"\2",                  # extra: prefix = \2
        r"\g<PREFIX>",          # extra: prefix = \2
        r"\4")                  # extra: extension
def test_regex_out_of_range_regex_reference_error_task(infiles, outfile,
                    prefix1,
                    prefix2,
                    extension):
    raise Exception("Should blow up first")





def cleanup_tmpdir():
    os.system('rm -f %s %s' % (os.path.join(workdir, '*'), RUFFUS_HISTORY_FILE))


class Test_regex_error_messages(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(workdir)
        except OSError:
            pass


    #___________________________________________________________________________
    #
    #   test regex() pipeline_printout and pipeline_run
    #___________________________________________________________________________
    def test_regex_printout(self):
        cleanup_tmpdir()

        s = StringIO()
        pipeline_printout(s, [test_regex_task], verbose=5, wrap_width = 10000)
        self.assertIn("Missing files [tmp_test_regex_error_messages/a_name.tmp1, tmp_test_regex_error_messages/a_name.tmp2", s.getvalue())

    def test_regex_run(self):
        """Run transform(...,regex()...)"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([test_regex_task], verbose=0, multiprocess = parallelism, one_second_per_job = one_second_per_job)


    #___________________________________________________________________________
    #
    #   test regex() pipeline_printout and pipeline_run
    #___________________________________________________________________________
    def test_regex_unmatched_printout(self):
        cleanup_tmpdir()
        s = StringIO()
        pipeline_printout(s, [test_regex_unmatched_task], verbose=5, wrap_width = 10000)
        self.assertIn("Warning: File match failure: File 'tmp_test_regex_error_messages/a_name.tmp1' does not match regex", s.getvalue())

    def test_regex_unmatched_run(self):
        """Run transform(...,regex()...)"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([test_regex_unmatched_task], verbose=0, multiprocess = parallelism, one_second_per_job = one_second_per_job)


    #___________________________________________________________________________
    #
    #   test suffix() pipeline_printout and pipeline_run
    #___________________________________________________________________________
    def test_suffix_printout(self):
        cleanup_tmpdir()

        s = StringIO()
        pipeline_printout(s, [test_suffix_task], verbose=5, wrap_width = 10000)
        self.assertIn("Missing files [tmp_test_regex_error_messages/a_name.tmp1, tmp_test_regex_error_messages/a_name.tmp2", s.getvalue())

    def test_suffix_run(self):
        """Run transform(...,suffix()...)"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([test_suffix_task], verbose=0, multiprocess = parallelism, one_second_per_job = one_second_per_job)


    #___________________________________________________________________________
    #
    #   test suffix() pipeline_printout and pipeline_run
    #___________________________________________________________________________
    def test_suffix_unmatched(self):
        cleanup_tmpdir()
        s = StringIO()
        self.assertRaisesRegexp(fatal_error_input_file_does_not_match,
                                "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*invalid group reference",
                                pipeline_printout,
                                s, [test_suffix_unmatched_task],
                                verbose = 3)
        self.assertRaisesRegexp(RethrownJobError,
                                "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*invalid group reference",
                                pipeline_run,
                                [test_suffix_unmatched_task], verbose = 0)


    #___________________________________________________________________________
    #
    #   test suffix() pipeline_printout and pipeline_run
    #___________________________________________________________________________
    def test_suffix_unmatched_printout2(self):
        cleanup_tmpdir()
        s = StringIO()
        pipeline_printout(s, [test_suffix_unmatched_task2], verbose=5, wrap_width = 10000)
        self.assertIn("Warning: File match failure: File 'tmp_test_regex_error_messages/a_name.tmp1' does not match suffix", s.getvalue())

    def test_suffix_unmatched_run2(self):
        """Run transform(...,suffix()...)"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([test_suffix_unmatched_task2], verbose=0, multiprocess = parallelism, one_second_per_job = one_second_per_job)



    #___________________________________________________________________________
    #
    #   test regex() errors: func pipeline_printout
    #___________________________________________________________________________
    def test_regex_misspelt_capture_error(self):
        cleanup_tmpdir()
        s = StringIO()
        self.assertRaisesRegexp(fatal_error_input_file_does_not_match,
                                "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*unknown group name",
                                pipeline_printout,
                                s, [test_regex_misspelt_capture_error_task],
                                verbose = 3)
        self.assertRaisesRegexp(RethrownJobError,
                                "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*unknown group name",
                                pipeline_run,
                                [test_regex_misspelt_capture_error_task], verbose = 0)

    #___________________________________________________________________________
    #
    #   test regex() errors: func pipeline_printout
    #___________________________________________________________________________
    def test_regex_misspelt_capture2_error(self):
        cleanup_tmpdir()
        s = StringIO()
        self.assertRaisesRegexp(fatal_error_input_file_does_not_match,
                                "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*unknown group name",
                                pipeline_printout,
                                s, [test_regex_misspelt_capture2_error_task],
                                verbose = 3)
        self.assertRaisesRegexp(RethrownJobError,
                                "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*unknown group name",
                                pipeline_run,
                                [test_regex_misspelt_capture2_error_task], verbose = 0)


    #___________________________________________________________________________
    #
    #   test regex() errors: func pipeline_printout
    #___________________________________________________________________________
    def test_regex_out_of_range_regex_reference_error_printout(self):
        cleanup_tmpdir()
        s = StringIO()
        self.assertRaisesRegexp(fatal_error_input_file_does_not_match,
                                "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*invalid group reference",
                                pipeline_printout,
                                s, [test_regex_out_of_range_regex_reference_error_task],
                                verbose = 3)
        self.assertRaisesRegexp(RethrownJobError,
                                "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*invalid group reference",
                                pipeline_run,
                                [test_regex_out_of_range_regex_reference_error_task], verbose = 0)


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
    #pipeline_printout(sys.stdout, [test_product_task], verbose = 3)
    unittest.main()
