#!/usr/bin/env python
from __future__ import print_function
import re
import shutil
import unittest
from ruffus.ruffus_utility import RUFFUS_HISTORY_FILE
from ruffus import pipeline_run, pipeline_printout, Pipeline, formatter, output_from
import sys

"""

    test_combinatorics.py

        test product, combine, permute, combine_with_replacement

"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0]))
# sub-1s resolution in system?
one_second_per_job = None


# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


try:
    from StringIO import StringIO
except:
    from io import StringIO


def touch(outfile):
    with open(outfile, "w"):
        pass


# ___________________________________________________________________________
#
#   generate_initial_files1
# ___________________________________________________________________________
def generate_initial_files1(outfile):
    touch(outfile)

# ___________________________________________________________________________
#
#   generate_initial_files2
# ___________________________________________________________________________


def generate_initial_files2(outfile):
    touch(outfile)

# ___________________________________________________________________________
#
#   generate_initial_files3
# ___________________________________________________________________________


def generate_initial_files3(outfile):
    touch(outfile)

# ___________________________________________________________________________
#
#   check_product_task
# ___________________________________________________________________________


def check_product_task(infiles, outfile,
                       prefices,
                       subpath,
                       subdir):
    with open(outfile, "w") as p:
        p.write(prefices + ",")


# ___________________________________________________________________________
#
#   check_product_merged_task
# ___________________________________________________________________________
def check_product_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())

# ___________________________________________________________________________
#
#   check_product_misspelt_capture_error_task
# ___________________________________________________________________________


def check_product_misspelt_capture_error_task(infiles, outfile):
    """
    FILE_PART mispelt as FILE_PART
    """
    touch(outfile)


# ___________________________________________________________________________
#
#   check_product_out_of_range_formatter_ref_error_task
# ___________________________________________________________________________
def check_product_out_of_range_formatter_ref_error_task(infiles, outfile, ignored_filter):
    """
    {path[2][0]} when len(path) == 1
    """
    touch(outfile)

# ___________________________________________________________________________
#
#   check_product_formatter_ref_index_error_task
# ___________________________________________________________________________


def check_product_formatter_ref_index_error_task(infiles, outfile, ignored_filter):
    """
    {path[0][0][1000} when len of the path string len(path[0][0]) < 1000
    """
    touch(outfile)

# ___________________________________________________________________________
#
#   check_combinations2_task
# ___________________________________________________________________________


def check_combinations2_task(infiles, outfile,
                             prefices,
                             subpath,
                             subdir):
    """
        Test combinations with k-tuple = 2
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


def check_combinations2_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())

# ___________________________________________________________________________
#
#   check_combinations3_task
# ___________________________________________________________________________


def check_combinations3_task(infiles, outfile,
                             prefices,
                             subpath,
                             subdir):
    """
        Test combinations with k-tuple = 3
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


def check_combinations3_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())


# ___________________________________________________________________________
#
#   check_permutations2_task
# ___________________________________________________________________________
def check_permutations2_task(infiles, outfile,
                             prefices,
                             subpath,
                             subdir):
    """
        Test permutations with k-tuple = 2
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


def check_permutations2_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())


# ___________________________________________________________________________
#
#   check_permutations3_task
# ___________________________________________________________________________
def check_permutations3_task(infiles, outfile,
                             prefices,
                             subpath,
                             subdir):
    """
        Test permutations with k-tuple = 3
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


def check_permutations3_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())


# ___________________________________________________________________________
#
#   check_combinations_with_replacement2_task
# ___________________________________________________________________________
def check_combinations_with_replacement2_task(infiles, outfile,
                                              prefices,
                                              subpath,
                                              subdir):
    """
        Test combinations_with_replacement with k-tuple = 2
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


def check_combinations_with_replacement2_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())


# ___________________________________________________________________________
#
#   check_combinations_with_replacement3_task
# ___________________________________________________________________________
def check_combinations_with_replacement3_task(infiles, outfile,
                                              prefices,
                                              subpath,
                                              subdir):
    """
        Test combinations_with_replacement with k-tuple = 3
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


def check_combinations_with_replacement3_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())


def cleanup_tmpdir():
    os.system('rm -f %s %s' %
              (os.path.join(tempdir, '*'), RUFFUS_HISTORY_FILE))


test_pipeline1 = Pipeline("test1")
test_pipeline2 = Pipeline("test2")
gen_task1 = test_pipeline1.originate(task_func=generate_initial_files1,
                                     name="WOWWWEEE",
                                     output=[tempdir + "/" + prefix + "_name.tmp1" for prefix in "abcd"])
test_pipeline1.originate(task_func=generate_initial_files2,
                         output=[tempdir + "/e_name.tmp1", tempdir + "/f_name.tmp1"])
test_pipeline1.originate(task_func=generate_initial_files3,
                         output=[tempdir + "/g_name.tmp1", tempdir + "/h_name.tmp1"])
test_pipeline1.product(task_func=check_product_task,
                       input=[tempdir + "/" + prefix +
                              "_name.tmp1" for prefix in "abcd"],
                       filter=formatter(".*/(?P<FILE_PART>.+).tmp1$"),
                       input2=generate_initial_files2,
                       filter2=formatter(),
                       input3=generate_initial_files3,
                       filter3=formatter(r"tmp1$"),
                       output="{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.{basename[2][0]}.tmp2",
                       extras=["{basename[0][0][0]}{basename[1][0][0]}{basename[2][0][0]}",       # extra: prefices only (abcd etc)
                               # extra: path for 2nd input, 1st file
                               "{subpath[0][0][0]}",
                               "{subdir[0][0][0]}"]).follows("WOWWWEEE").follows(gen_task1).follows(generate_initial_files1).follows("generate_initial_files1")
test_pipeline1.merge(task_func=check_product_merged_task,
                     input=check_product_task,
                     output=tempdir + "/merged.results")
test_pipeline1.product(task_func=check_product_misspelt_capture_error_task,
                       input=gen_task1,
                       filter=formatter(".*/(?P<FILE_PART>.+).tmp1$"),
                       output="{path[0][0]}/{FILEPART[0][0]}.tmp2")
test_pipeline1.product(task_func=check_product_out_of_range_formatter_ref_error_task,
                       input=generate_initial_files1,  #
                       filter=formatter(".*/(?P<FILE_PART>.+).tmp1$"),
                       output="{path[2][0]}/{basename[0][0]}.tmp2",
                       extras=["{FILE_PART[0][0]}"])
test_pipeline1.product(task_func=check_product_formatter_ref_index_error_task,
                       input=output_from("generate_initial_files1"),
                       filter=formatter(".*/(?P<FILE_PART>.+).tmp1$"),
                       output="{path[0][0][1000]}/{basename[0][0]}.tmp2",
                       extras=["{FILE_PART[0][0]}"])
test_pipeline1.combinations(task_func=check_combinations2_task,
                            input=generate_initial_files1,      # gen_task1
                            filter=formatter(".*/(?P<FILE_PART>.+).tmp1$"),
                            tuple_size=2,
                            output="{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.tmp2",
                            extras=["{basename[0][0][0]}{basename[1][0][0]}",       # extra: prefices
                                    # extra: path for 2nd input, 1st file
                                    "{subpath[0][0][0]}",
                                    "{subdir[0][0][0]}"])
test_pipeline1.merge(task_func=check_combinations2_merged_task,
                     input=check_combinations2_task,
                     output=tempdir + "/merged.results")
test_pipeline1.combinations(task_func=check_combinations3_task,
                            input=output_from("WOWWWEEE"),
                            filter=formatter(".*/(?P<FILE_PART>.+).tmp1$"),
                            tuple_size=3,
                            output="{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.{basename[2][0]}.tmp2",
                            extras=["{basename[0][0][0]}{basename[1][0][0]}{basename[2][0][0]}",       # extra: prefices
                                    # extra: path for 2nd input, 1st file
                                    "{subpath[0][0][0]}",
                                    "{subdir[0][0][0]}"])

test_pipeline1.merge(check_combinations3_merged_task,
                     check_combinations3_task, tempdir + "/merged.results")
test_pipeline1.permutations(task_func=check_permutations2_task,
                            input=output_from("WOWWWEEE"),
                            filter=formatter(".*/(?P<FILE_PART>.+).tmp1$"),
                            tuple_size=2,
                            output="{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.tmp2",
                            extras=["{basename[0][0][0]}{basename[1][0][0]}",       # extra: prefices
                                    # extra: path for 2nd input, 1st file
                                    "{subpath[0][0][0]}",
                                    "{subdir[0][0][0]}"])

test_pipeline2.merge(check_permutations2_merged_task,
                     check_permutations2_task, tempdir + "/merged.results")


test_pipeline2.permutations(task_func=check_permutations3_task,
                            input=output_from("WOWWWEEE"),
                            filter=formatter(".*/(?P<FILE_PART>.+).tmp1$"),
                            tuple_size=3,
                            output="{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.{basename[2][0]}.tmp2",
                            extras=["{basename[0][0][0]}{basename[1][0][0]}{basename[2][0][0]}",       # extra: prefices
                                    # extra: path for 2nd input, 1st file
                                    "{subpath[0][0][0]}",
                                    "{subdir[0][0][0]}"])
test_pipeline2.merge(check_permutations3_merged_task,
                     check_permutations3_task, tempdir + "/merged.results")
test_pipeline2.combinations_with_replacement(check_combinations_with_replacement2_task,
                                             input=output_from("WOWWWEEE"),
                                             filter=formatter(
                                                 ".*/(?P<FILE_PART>.+).tmp1$"),
                                             tuple_size=2,
                                             output="{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.tmp2",
                                             extras=["{basename[0][0][0]}{basename[1][0][0]}",       # extra: prefices
                                                     # extra: path for 2nd input, 1st file
                                                     "{subpath[0][0][0]}",
                                                     "{subdir[0][0][0]}"])
test_pipeline2.merge(check_combinations_with_replacement2_merged_task,
                     check_combinations_with_replacement2_task, tempdir + "/merged.results")
test_pipeline2.combinations_with_replacement(task_func=check_combinations_with_replacement3_task,
                                             input=output_from("WOWWWEEE"),
                                             filter=formatter(
                                                 ".*/(?P<FILE_PART>.+).tmp1$"),
                                             tuple_size=3,
                                             output="{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.{basename[2][0]}.tmp2",
                                             extras=["{basename[0][0][0]}{basename[1][0][0]}{basename[2][0][0]}",       # extra: prefices
                                                     # extra: path for 2nd input, 1st file
                                                     "{subpath[0][0][0]}",
                                                     "{subdir[0][0][0]}"])
test_pipeline2.merge(check_combinations_with_replacement3_merged_task,
                     check_combinations_with_replacement3_task, tempdir + "/merged.results")


class TestCombinatorics(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(tempdir)
        except OSError:
            pass

    # ___________________________________________________________________________
    #
    #   test product() pipeline_printout and pipeline_run
    # ___________________________________________________________________________
    def test_product_printout(self):
        """Input file exists, output doesn't exist"""
        cleanup_tmpdir()
        s = StringIO()
        test_pipeline2.printout(
            s, [check_product_merged_task], verbose=5, wrap_width=10000)
        self.assertTrue(re.search('Job needs update:.*Missing files.*'
                                  '\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/e_name.tmp1, '
                                  '.*{tempdir}/h_name.tmp1, '
                                  '.*{tempdir}/a_name.e_name.h_name.tmp2\]'.format(tempdir=tempdir), s.getvalue(), re.DOTALL))

    def test_product_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        test_pipeline2.run([check_product_merged_task], verbose=0,
                           multiprocess=100, one_second_per_job=one_second_per_job)
        with open(tempdir + "/merged.results") as oo:
            self.assertEqual(oo.read(),
                             "aeg,aeh,afg,afh,beg,beh,bfg,bfh,ceg,ceh,cfg,cfh,deg,deh,dfg,dfh,")

    # ___________________________________________________________________________
    #
    #   test product() pipeline_printout diagnostic error messsages
    #
    #       require verbose >= 3 or an empty jobs list
    # ___________________________________________________________________________
    def test_product_misspelt_capture_error(self):
        """Misspelt named capture group
            Requires verbose >= 3 or an empty jobs list
        """
        cleanup_tmpdir()

        s = StringIO()
        test_pipeline2.printout(
            s, [check_product_misspelt_capture_error_task], verbose=3, wrap_width=10000)
        self.assertIn("Warning: Input substitution failed:", s.getvalue())
        self.assertIn("Unmatched field {FILEPART}", s.getvalue())

    def test_product_out_of_range_formatter_ref_error(self):
        """
        {path[2][0]} when len(path) == 1
            Requires verbose >= 3 or an empty jobs list
        """
        cleanup_tmpdir()

        s = StringIO()
        test_pipeline2.printout(
            s, [check_product_out_of_range_formatter_ref_error_task], verbose=3, wrap_width=10000)
        self.assertIn("Warning: Input substitution failed:", s.getvalue())
        self.assertIn("Unmatched field {2}", s.getvalue())

    def test_product_formatter_ref_index_error(self):
        """
        {path[0][0][1000} when len of the path string len(path[0][0]) < 1000
            Requires verbose >= 3 or an empty jobs list
        """
        cleanup_tmpdir()

        s = StringIO()
        test_pipeline2.printout(
            s, [check_product_formatter_ref_index_error_task], verbose=3, wrap_width=10000)
        self.assertIn("Warning: Input substitution failed:", s.getvalue())
        self.assertIn(
            "Unmatched field {string index out of range}", s.getvalue())
        # print s.getvalue()

    # ___________________________________________________________________________
    #
    #   test combinations() pipeline_printout and pipeline_run
    # ___________________________________________________________________________

    def test_combinations2_printout(self):
        """Input file exists, output doesn't exist"""
        cleanup_tmpdir()

        s = StringIO()
        test_pipeline1.printout(
            s, [check_combinations2_merged_task], verbose=5, wrap_width=10000)
        self.assertTrue(re.search('Job needs update:.*Missing files.*'
                                  '\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/b_name.tmp1, '
                                  '.*{tempdir}/a_name.b_name.tmp2\]'.format(tempdir=tempdir), s.getvalue(), re.DOTALL))

    def test_combinations2_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        test_pipeline2.run([check_combinations2_merged_task], verbose=0,
                           multiprocess=100, one_second_per_job=one_second_per_job)
        with open(tempdir + "/merged.results") as oo:
            self.assertEqual(oo.read(),
                             'ab,ac,ad,bc,bd,cd,')

    # ___________________________________________________________________________
    #
    #   test combinations() pipeline_printout and pipeline_run
    # ___________________________________________________________________________
    def test_combinations3_printout(self):
        """Input file exists, output doesn't exist"""
        cleanup_tmpdir()

        s = StringIO()
        test_pipeline2.printout(
            s, [check_combinations3_merged_task], verbose=5, wrap_width=10000)
        self.assertTrue(re.search(
            '\[.*{tempdir}/a_name.tmp1, '
            '.*{tempdir}/b_name.tmp1, '
            '.*{tempdir}/c_name.tmp1, '
            '.*{tempdir}/a_name.b_name.c_name.tmp2\]'.format(tempdir=tempdir), s.getvalue()))

    def test_combinations3_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        test_pipeline2.run([check_combinations3_merged_task], verbose=0,
                           multiprocess=100, one_second_per_job=one_second_per_job)
        with open(tempdir + "/merged.results") as oo:
            self.assertEqual(oo.read(),
                             "abc,abd,acd,bcd,")

    # ___________________________________________________________________________
    #
    #   test permutations() pipeline_printout and pipeline_run
    # ___________________________________________________________________________

    def test_permutations2_printout(self):
        """Input file exists, output doesn't exist"""
        cleanup_tmpdir()

        s = StringIO()
        test_pipeline2.printout(
            s, [check_permutations2_merged_task], verbose=5, wrap_width=10000)
        self.assertTrue(re.search('\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/b_name.tmp1, '
                                  '.*{tempdir}/a_name.b_name.tmp2\]'.format(tempdir=tempdir), s.getvalue()))

    def test_permutations2_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        test_pipeline2.run([check_permutations2_merged_task], verbose=0,
                           multiprocess=100, one_second_per_job=one_second_per_job)
        with open(tempdir + "/merged.results") as oo:
            self.assertEqual(oo.read(),
                             "ab,ac,ad,ba,bc,bd,ca,cb,cd,da,db,dc,")

    # ___________________________________________________________________________
    #
    #   test permutations() pipeline_printout and pipeline_run
    # ___________________________________________________________________________
    def test_permutations3_printout(self):
        """Input file exists, output doesn't exist"""
        cleanup_tmpdir()

        s = StringIO()
        test_pipeline2.printout(
            s, [check_permutations3_merged_task], verbose=5, wrap_width=10000)
        self.assertTrue(re.search('\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/b_name.tmp1, '
                                  '.*{tempdir}/c_name.tmp1, '
                                  '.*{tempdir}/a_name.b_name.c_name.tmp2\]'.format(tempdir=tempdir), s.getvalue()))

    def test_permutations3_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        test_pipeline2.run([check_permutations3_merged_task], verbose=0,
                           multiprocess=100, one_second_per_job=one_second_per_job)
        with open(tempdir + "/merged.results") as oo:
            self.assertEqual(oo.read(),
                             'abc,abd,acb,acd,adb,adc,bac,bad,bca,bcd,bda,bdc,cab,cad,cba,cbd,cda,cdb,dab,dac,dba,dbc,dca,dcb,')

    # ___________________________________________________________________________
    #
    #   test combinations_with_replacement() pipeline_printout and pipeline_run
    # ___________________________________________________________________________

    def test_combinations_with_replacement2_printout(self):
        """Input file exists, output doesn't exist"""
        cleanup_tmpdir()

        s = StringIO()
        test_pipeline2.printout(
            s, [check_combinations_with_replacement2_merged_task], verbose=5, wrap_width=10000)
        self.assertTrue(re.search('\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/b_name.tmp1, '
                                  '.*{tempdir}/a_name.b_name.tmp2\]'.format(tempdir=tempdir), s.getvalue()))

    def test_combinations_with_replacement2_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        test_pipeline2.run([check_combinations_with_replacement2_merged_task],
                           verbose=0, multiprocess=100, one_second_per_job=one_second_per_job)
        with open(tempdir + "/merged.results") as oo:
            self.assertEqual(oo.read(),
                             "aa,ab,ac,ad,bb,bc,bd,cc,cd,dd,")

    # ___________________________________________________________________________
    #
    #   test combinations_with_replacement() pipeline_printout and pipeline_run
    # ___________________________________________________________________________
    def test_combinations_with_replacement3_printout(self):
        """Input file exists, output doesn't exist"""
        cleanup_tmpdir()

        s = StringIO()
        test_pipeline2.printout(
            s, [check_combinations_with_replacement3_merged_task], verbose=5, wrap_width=10000)
        self.assertTrue(re.search('\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/b_name.tmp1, '
                                  '.*{tempdir}/c_name.tmp1, '
                                  '.*{tempdir}/a_name.b_name.c_name.tmp2\]'.format(tempdir=tempdir), s.getvalue()))

    def test_combinations_with_replacement3_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        test_pipeline2.run([check_combinations_with_replacement3_merged_task],
                           verbose=0, multiprocess=100, one_second_per_job=one_second_per_job)
        with open(tempdir + "/merged.results") as oo:
            self.assertEqual(oo.read(),
                             'aaa,aab,aac,aad,abb,abc,abd,acc,acd,add,bbb,bbc,bbd,bcc,bcd,bdd,ccc,ccd,cdd,ddd,')

    # ___________________________________________________________________________
    #
    #   cleanup
    # ___________________________________________________________________________

    def tearDown(self):
        shutil.rmtree(tempdir)


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    #pipeline_printout(sys.stdout, [check_product_task], verbose = 5)
    unittest.main()
