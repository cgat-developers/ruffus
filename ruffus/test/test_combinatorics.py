#!/usr/bin/env python
from __future__ import print_function
import re
import shutil
import unittest
from ruffus.combinatorics import *
from ruffus.ruffus_utility import RUFFUS_HISTORY_FILE, CHECKSUM_FILE_TIMESTAMPS
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus import pipeline_run, pipeline_printout, Pipeline, formatter, originate, follows, merge
import ruffus
import sys

"""

    test_combinatorics.py

        test product, combine, permute, combine_with_replacement

"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0]))

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


try:
    from StringIO import StringIO
except:
    from io import StringIO


# sub-1s resolution in system?
one_second_per_job = None


def touch(filename):
    with open(filename, "w"):
        pass


# ___________________________________________________________________________
#
#   generate_initial_files1
# ___________________________________________________________________________
@originate(output=[tempdir + "/" + prefix + "_name.tmp1" for prefix in "abcd"])
def generate_initial_files1(out_name):
    with open(out_name, 'w') as outfile:
        pass

# ___________________________________________________________________________
#
#   generate_initial_files1
# ___________________________________________________________________________


@originate([tempdir + "/e_name.tmp1", tempdir + "/f_name.tmp1"])
def generate_initial_files2(out_name):
    with open(out_name, 'w') as outfile:
        pass

# ___________________________________________________________________________
#
#   generate_initial_files1
# ___________________________________________________________________________


@originate([tempdir + "/g_name.tmp1", tempdir + "/h_name.tmp1"])
def generate_initial_files3(out_name):
    with open(out_name, 'w') as outfile:
        pass

# ___________________________________________________________________________
#
#   check_product_task
# ___________________________________________________________________________


@follows(generate_initial_files1)
@product(
    [tempdir + "/" + prefix + "_name.tmp1" for prefix in "abcd"],
    formatter(".*/(?P<FILE_PART>.+).tmp1$"),
    generate_initial_files2,
    formatter(),
    "{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.{basename[2][0]}.tmp2",
    input3=generate_initial_files3,
    filter3=formatter(r"tmp1$"),
    extras=["{basename[0][0][0]}{basename[1][0][0]}{basename[2][0][0]}",       # extra: prefices only (abcd etc)
            # extra: path for 2nd input, 1st file
            "{subpath[0][0][0]}",
            "{subdir[0][0][0]}"])
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
@merge(check_product_task, tempdir + "/merged.results")
def check_product_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())

# ___________________________________________________________________________
#
#   check_product_misspelt_capture_error_task
# ___________________________________________________________________________


@product(
    generate_initial_files1,
    formatter(".*/(?P<FILE_PART>.+).tmp1$"),
    "{path[0][0]}/{FILEPART[0][0]}.tmp2")
def check_product_misspelt_capture_error_task(infiles, outfile):
    """
    FILE_PART mispelt as FILE_PART
    """
    with open(outfile, "w") as p:
        pass


# ___________________________________________________________________________
#
#   check_product_out_of_range_formatter_ref_error_task
# ___________________________________________________________________________
@product(
    generate_initial_files1,
    formatter(".*/(?P<FILE_PART>.+).tmp1$"),
    "{path[2][0]}/{basename[0][0]}.tmp2",
    "{FILE_PART[0][0]}")
def check_product_out_of_range_formatter_ref_error_task(infiles, outfile, ignored_filter):
    """
    {path[2][0]} when len(path) == 1
    """
    with open(outfile, "w") as p:
        pass

# ___________________________________________________________________________
#
#   check_product_formatter_ref_index_error_task
# ___________________________________________________________________________


@product(
    generate_initial_files1,
    formatter(".*/(?P<FILE_PART>.+).tmp1$"),
    "{path[0][0][1000]}/{basename[0][0]}.tmp2",
    "{FILE_PART[0][0]}")
def check_product_formatter_ref_index_error_task(infiles, outfile, ignored_filter):
    """
    {path[0][0][1000} when len of the path string len(path[0][0]) < 1000
    """
    with open(outfile, "w") as p:
        pass

# ___________________________________________________________________________
#
#   check_combinations2_task
# ___________________________________________________________________________


@combinations(
    generate_initial_files1,
    formatter(".*/(?P<FILE_PART>.+).tmp1$"),
    2,
    "{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.tmp2",
    "{basename[0][0][0]}{basename[1][0][0]}",       # extra: prefices
    "{subpath[0][0][0]}",      # extra: path for 2nd input, 1st file
    "{subdir[0][0][0]}")
def check_combinations2_task(infiles, outfile,
                             prefices,
                             subpath,
                             subdir):
    """
        Test combinations with k-tuple = 2
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


@merge(check_combinations2_task, tempdir + "/merged.results")
def check_combinations2_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())

# ___________________________________________________________________________
#
#   check_combinations3_task
# ___________________________________________________________________________


@combinations(
    generate_initial_files1,
    formatter(".*/(?P<FILE_PART>.+).tmp1$"),
    3,
    "{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.{basename[2][0]}.tmp2",
    # extra: prefices
    "{basename[0][0][0]}{basename[1][0][0]}{basename[2][0][0]}",
    "{subpath[0][0][0]}",      # extra: path for 2nd input, 1st file
    "{subdir[0][0][0]}")
def check_combinations3_task(infiles, outfile,
                             prefices,
                             subpath,
                             subdir):
    """
        Test combinations with k-tuple = 3
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


@merge(check_combinations3_task, tempdir + "/merged.results")
def check_combinations3_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())


# ___________________________________________________________________________
#
#   check_permutations2_task
# ___________________________________________________________________________
@permutations(
    generate_initial_files1,
    formatter(".*/(?P<FILE_PART>.+).tmp1$"),
    2,
    "{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.tmp2",
    "{basename[0][0][0]}{basename[1][0][0]}",       # extra: prefices
    "{subpath[0][0][0]}",      # extra: path for 2nd input, 1st file
    "{subdir[0][0][0]}")
def check_permutations2_task(infiles, outfile,
                             prefices,
                             subpath,
                             subdir):
    """
        Test permutations with k-tuple = 2
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


@merge(check_permutations2_task, tempdir + "/merged.results")
def check_permutations2_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())


# ___________________________________________________________________________
#
#   check_permutations3_task
# ___________________________________________________________________________
@permutations(
    generate_initial_files1,
    formatter(".*/(?P<FILE_PART>.+).tmp1$"),
    3,
    "{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.{basename[2][0]}.tmp2",
    # extra: prefices
    "{basename[0][0][0]}{basename[1][0][0]}{basename[2][0][0]}",
    "{subpath[0][0][0]}",      # extra: path for 2nd input, 1st file
    "{subdir[0][0][0]}")
def check_permutations3_task(infiles, outfile,
                             prefices,
                             subpath,
                             subdir):
    """
        Test permutations with k-tuple = 3
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


@merge(check_permutations3_task, tempdir + "/merged.results")
def check_permutations3_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())


# ___________________________________________________________________________
#
#   check_combinations_with_replacement2_task
# ___________________________________________________________________________
@combinations_with_replacement(
    input=generate_initial_files1,
    filter=formatter(".*/(?P<FILE_PART>.+).tmp1$"),
    tuple_size=2,
    output="{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.tmp2",
    extras=["{basename[0][0][0]}{basename[1][0][0]}",       # extra: prefices
            "{subpath[0][0][0]}",      # extra: path for 2nd input, 1st file
            "{subdir[0][0][0]}"])
def check_combinations_with_replacement2_task(infiles, outfile,
                                              prefices,
                                              subpath,
                                              subdir):
    """
        Test combinations_with_replacement with k-tuple = 2
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


@merge(check_combinations_with_replacement2_task, tempdir + "/merged.results")
def check_combinations_with_replacement2_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())


# ___________________________________________________________________________
#
#   check_combinations_with_replacement3_task
# ___________________________________________________________________________
@combinations_with_replacement(
    generate_initial_files1,
    formatter(".*/(?P<FILE_PART>.+).tmp1$"),
    3,
    "{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.{basename[2][0]}.tmp2",
    # extra: prefices
    "{basename[0][0][0]}{basename[1][0][0]}{basename[2][0][0]}",
    "{subpath[0][0][0]}",      # extra: path for 2nd input, 1st file
    "{subdir[0][0][0]}")
def check_combinations_with_replacement3_task(infiles, outfile,
                                              prefices,
                                              subpath,
                                              subdir):
    """
        Test combinations_with_replacement with k-tuple = 3
    """
    with open(outfile, "w") as outf:
        outf.write(prefices + ",")


@merge(check_combinations_with_replacement3_task, tempdir + "/merged.results")
def check_combinations_with_replacement3_merged_task(infiles, outfile):
    with open(outfile, "w") as p:
        for infile in sorted(infiles):
            with open(infile) as ii:
                p.write(ii.read())


def cleanup_tmpdir():
    os.system('rm -f %s %s' %
              (os.path.join(tempdir, '*'), RUFFUS_HISTORY_FILE))


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
        pipeline_printout(s, [check_product_merged_task],
                          verbose=5, wrap_width=10000, pipeline="main")
        self.assertTrue(re.search('Job needs update:.*Missing files.*'
                                  '\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/e_name.tmp1, '
                                  '.*{tempdir}/h_name.tmp1, '
                                  '.*{tempdir}/a_name.e_name.h_name.tmp2\]'.format(tempdir=tempdir), s.getvalue(), re.DOTALL))

    def test_product_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_product_merged_task], verbose=0, multiprocess=100,
                     one_second_per_job=one_second_per_job, pipeline="main")
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
        pipeline_printout(s, [check_product_misspelt_capture_error_task],
                          verbose=3, wrap_width=10000, pipeline="main")
        self.assertIn("Warning: Input substitution failed:", s.getvalue())
        self.assertIn("Unmatched field {FILEPART}", s.getvalue())

    def test_product_out_of_range_formatter_ref_error(self):
        """
        {path[2][0]} when len(path) == 1
            Requires verbose >= 3 or an empty jobs list
        """
        cleanup_tmpdir()

        s = StringIO()
        pipeline_printout(s, [check_product_out_of_range_formatter_ref_error_task],
                          verbose=3, wrap_width=10000, pipeline="main")
        self.assertIn("Warning: Input substitution failed:", s.getvalue())
        self.assertIn("Unmatched field {2}", s.getvalue())

    def test_product_formatter_ref_index_error(self):
        """
        {path[0][0][1000} when len of the path string len(path[0][0]) < 1000
            Requires verbose >= 3 or an empty jobs list
        """
        cleanup_tmpdir()

        s = StringIO()
        pipeline_printout(s, [check_product_formatter_ref_index_error_task],
                          verbose=3, wrap_width=10000, pipeline="main")
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
        pipeline_printout(s, [check_combinations2_merged_task],
                          verbose=5, wrap_width=10000, pipeline="main")
        self.assertTrue(re.search('Job needs update:.*Missing files.*'
                                  '\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/b_name.tmp1, '
                                  '.*{tempdir}/a_name.b_name.tmp2\]'.format(tempdir=tempdir), s.getvalue(), re.DOTALL))

    def test_combinations2_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_combinations2_merged_task], verbose=0, multiprocess=100,
                     one_second_per_job=one_second_per_job, pipeline="main")
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
        pipeline_printout(s, [check_combinations3_merged_task],
                          verbose=5, wrap_width=10000, pipeline="main")
        self.assertTrue(re.search(
            '\[.*{tempdir}/a_name.tmp1, '
            '.*{tempdir}/b_name.tmp1, '
            '.*{tempdir}/c_name.tmp1, '
            '.*{tempdir}/a_name.b_name.c_name.tmp2\]'.format(tempdir=tempdir), s.getvalue()))

    def test_combinations3_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_combinations3_merged_task], verbose=0, multiprocess=100,
                     one_second_per_job=one_second_per_job, pipeline="main")
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
        pipeline_printout(s, [check_permutations2_merged_task],
                          verbose=5, wrap_width=10000, pipeline="main")
        self.assertTrue(re.search('\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/b_name.tmp1, '
                                  '.*{tempdir}/a_name.b_name.tmp2\]'.format(tempdir=tempdir), s.getvalue()))

    def test_permutations2_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_permutations2_merged_task], verbose=0, multiprocess=100,
                     one_second_per_job=one_second_per_job, pipeline="main")
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
        pipeline_printout(s, [check_permutations3_merged_task],
                          verbose=5, wrap_width=10000, pipeline="main")
        self.assertTrue(re.search('\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/b_name.tmp1, '
                                  '.*{tempdir}/c_name.tmp1, '
                                  '.*{tempdir}/a_name.b_name.c_name.tmp2\]'.format(tempdir=tempdir), s.getvalue()))

    def test_permutations3_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_permutations3_merged_task], verbose=0, multiprocess=100,
                     one_second_per_job=one_second_per_job, pipeline="main")
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
        pipeline_printout(s, [check_combinations_with_replacement2_merged_task],
                          verbose=5, wrap_width=10000, pipeline="main")
        self.assertTrue(re.search('\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/b_name.tmp1, '
                                  '.*{tempdir}/a_name.b_name.tmp2\]'.format(tempdir=tempdir), s.getvalue()))

    def test_combinations_with_replacement2_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_combinations_with_replacement2_merged_task], verbose=0,
                     multiprocess=100, one_second_per_job=one_second_per_job, pipeline="main")
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
        pipeline_printout(s, [check_combinations_with_replacement3_merged_task],
                          verbose=5, wrap_width=10000, pipeline="main")
        self.assertTrue(re.search('\[.*{tempdir}/a_name.tmp1, '
                                  '.*{tempdir}/b_name.tmp1, '
                                  '.*{tempdir}/c_name.tmp1, '
                                  '.*{tempdir}/a_name.b_name.c_name.tmp2\]'.format(tempdir=tempdir), s.getvalue()))

    def test_combinations_with_replacement3_run(self):
        """Run product"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_combinations_with_replacement3_merged_task], verbose=0,
                     multiprocess=100, one_second_per_job=one_second_per_job, pipeline="main")
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
    #pipeline_printout(sys.stdout, [check_product_task], verbose = 5, pipeline= "main")
    unittest.main()
