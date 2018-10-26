#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
import re
import sys
"""

    test_regex_error_messages.py

        test product, combine, permute, combine_with_replacement

        Includes code from python.unittest with the following copyright notice:


        Copyright (c) 1999-2003 Steve Purcell
        Copyright (c) 2003-2010 Python Software Foundation
        This module is free software, and you may redistribute it and/or modify
        it under the same terms as Python itself, so long as this copyright message
        and disclaimer are retained in their original form.

        IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
        SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
        THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
        DAMAGE.

        THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
        LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
        PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
        AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
        SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

"""
import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"
# sub-1s resolution in system?
one_second_per_job = None
parallelism = 2


# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ruffus_name = os.path.basename(parent_dir)
ruffus = __import__(ruffus_name)
for attr in "pipeline_run", "pipeline_printout", "suffix", "transform", "split", "merge", "dbdict", "follows", "originate", "Pipeline", "regex":
    globals()[attr] = getattr(ruffus, attr)
RUFFUS_HISTORY_FILE = ruffus.ruffus_utility.RUFFUS_HISTORY_FILE
fatal_error_input_file_does_not_match = ruffus.ruffus_exceptions.fatal_error_input_file_does_not_match
RethrownJobError = ruffus.ruffus_exceptions.RethrownJobError


try:
    from StringIO import StringIO
except:
    from io import StringIO


# ___________________________________________________________________________
#
#   generate_initial_files1
# ___________________________________________________________________________
@originate([tempdir + prefix + "_name.tmp1" for prefix in "abcdefghi"])
def generate_initial_files1(out_name):
    with open(out_name, 'w') as outfile:
        pass

# ___________________________________________________________________________
#
#   check_regex_task
# ___________________________________________________________________________


@transform(
    generate_initial_files1,
    regex("(.*)/(?P<PREFIX>[abcd])(_name)(.tmp1)"),
    r"\1/\g<PREFIX>\3.tmp2",  # output file
    r"\2",                  # extra: prefix = \2
    r"\g<PREFIX>",          # extra: prefix = \2
    r"\4")                  # extra: extension
def check_regex_task(infiles, outfile,
                     prefix1,
                     prefix2,
                     extension):
    with open(outfile, "w") as p:
        pass

    if prefix1 != prefix2:
        raise Exception("Expecting %s == %s" % (prefix1, prefix2))


# ___________________________________________________________________________
#
#   check_regex_unmatched_task
# ___________________________________________________________________________
@transform(
    generate_initial_files1,
    regex("(.*)/(?P<PREFIX>[abcd])(_name)(.xxx)"),
    r"\1/\g<PREFIXA>\3.tmp2",  # output file
    r"\2",                  # extra: prefix = \2
    r"\g<PREFIX>",          # extra: prefix = \2
    r"\4")                  # extra: extension
def check_regex_unmatched_task(infiles, outfile,
                               prefix1,
                               prefix2,
                               extension):
    raise Exception("Should blow up first")


# ___________________________________________________________________________
#
#   check_suffix_task
# ___________________________________________________________________________
@transform(
    generate_initial_files1,
    suffix(".tmp1"),
    r".tmp2",           # output file
    r"\1")              # extra: basename
def check_suffix_task(infile, outfile,
                      basename):
    with open(outfile, "w") as f:
        pass


# ___________________________________________________________________________
#
#   check_suffix_unmatched_task
# ___________________________________________________________________________
@transform(
    generate_initial_files1,
    suffix(".tmp1"),
    r".tmp2",           # output file
    r"\2")              # extra: unknown
def check_suffix_unmatched_task(infiles, outfile, unknown):
    raise Exception("Should blow up first")


# ___________________________________________________________________________
#
#   check_suffix_unmatched_task
# ___________________________________________________________________________
@transform(
    generate_initial_files1,
    suffix(".tmp2"),
    r".tmp2")           # output file
def check_suffix_unmatched_task2(infiles, outfile):
    raise Exception("Should blow up first")


# ___________________________________________________________________________
#
#   check_product_misspelt_capture_error_task
# ___________________________________________________________________________
@transform(
    generate_initial_files1,
    regex("(.*)/(?P<PREFIX>[abcd])(_name)(.tmp)"),
    r"\1/\g<PREFIXA>\3.tmp2",  # output file
    r"\2",                  # extra: prefix = \2
    r"\g<PREFIX>",          # extra: prefix = \2
    r"\4")                  # extra: extension
def check_regex_misspelt_capture_error_task(infiles, outfile,
                                            prefix1,
                                            prefix2,
                                            extension):
    raise Exception("Should blow up first")


# ___________________________________________________________________________
#
#   check_regex_misspelt_capture2_error_task
# ___________________________________________________________________________
@transform(
    generate_initial_files1,
    regex("(.*)/(?P<PREFIX>[abcd])(_name)(.tmp)"),
    r"\1/\g<PREFIX>\3.tmp2",  # output file
    r"\2",                  # extra: prefix = \2
    r"\g<PREFIXA>",          # extra: prefix = \2
    r"\4")                  # extra: extension
def check_regex_misspelt_capture2_error_task(infiles, outfile,
                                             prefix1,
                                             prefix2,
                                             extension):
    raise Exception("Should blow up first")


# ___________________________________________________________________________
#
#   check_regex_out_of_range_regex_reference_error_task
# ___________________________________________________________________________
@transform(
    generate_initial_files1,
    regex("(.*)/(?P<PREFIX>[abcd])(_name)(.tmp)"),
    r"\1/\g<PREFIX>\5.tmp2",  # output file
    r"\2",                  # extra: prefix = \2
    r"\g<PREFIX>",          # extra: prefix = \2
    r"\4")                  # extra: extension
def check_regex_out_of_range_regex_reference_error_task(infiles, outfile,
                                                        prefix1,
                                                        prefix2,
                                                        extension):
    raise Exception("Should blow up first")


def cleanup_tmpdir():
    os.system('rm -f %s %s' %
              (os.path.join(tempdir, '*'), RUFFUS_HISTORY_FILE))


class _AssertRaisesContext_27(object):
    """A context manager used to implement TestCase.assertRaises* methods.
    Taken from python unittest2.7
    """

    def __init__(self, expected, test_case, expected_regexp=None):
        self.expected = expected
        self.failureException = test_case.failureException
        self.expected_regexp = expected_regexp

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            try:
                exc_name = self.expected.__name__
            except AttributeError:
                exc_name = str(self.expected)
            raise self.failureException(
                "{0} not raised".format(exc_name))
        if not issubclass(exc_type, self.expected):
            # let unexpected exceptions pass through
            return False
        self.exception = exc_value  # store for later retrieval
        if self.expected_regexp is None:
            return True

        expected_regexp = self.expected_regexp
        if isinstance(expected_regexp, basestring):
            expected_regexp = re.compile(expected_regexp)
        if not expected_regexp.search(str(exc_value)):
            raise self.failureException('"%s" does not match "%s"' %
                                        (expected_regexp.pattern, str(exc_value)))
        return True


class Test_regex_error_messages(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(tempdir)
        except OSError:
            pass
        if sys.hexversion < 0x03000000:
            self.assertRaisesRegex = self.assertRaisesRegexp27

        if sys.hexversion < 0x02070000:
            self.assertIn = self.my_assertIn

    def my_assertIn(self, test_string, full_string):
        self.assertTrue(test_string in full_string)

    #

    def assertRaisesRegexp27(self, expected_exception, expected_regexp,
                             callable_obj=None, *args, **kwargs):
        """Asserts that the message in a raised exception matches a regexp.

        Args:
            expected_exception: Exception class expected to be raised.
            expected_regexp: Regexp (re pattern object or string) expected
                    to be found in error message.
            callable_obj: Function to be called.
            args: Extra args.
            kwargs: Extra kwargs.
        """
        context = _AssertRaisesContext_27(
            expected_exception, self, expected_regexp)
        if callable_obj is None:
            return context
        with context:
            callable_obj(*args, **kwargs)

    # ___________________________________________________________________________
    #
    #   test regex() pipeline_printout and pipeline_run
    # ___________________________________________________________________________

    def test_regex_printout(self):
        cleanup_tmpdir()

        s = StringIO()
        pipeline_printout(s, [check_regex_task], verbose=5,
                          wrap_width=10000, pipeline="main")
        self.assertTrue(re.search(
            'Missing files.*\[{tempdir}a_name.tmp1, {tempdir}a_name.tmp2'.format(tempdir=tempdir), s.getvalue(), re.DOTALL))

    def test_regex_run(self):
        """Run transform(...,regex()...)"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_regex_task], verbose=0, multiprocess=parallelism,
                     one_second_per_job=one_second_per_job, pipeline="main")

    # ___________________________________________________________________________
    #
    #   test regex() pipeline_printout and pipeline_run
    # ___________________________________________________________________________

    def test_regex_unmatched_printout(self):
        cleanup_tmpdir()
        s = StringIO()
        pipeline_printout(s, [check_regex_unmatched_task],
                          verbose=5, wrap_width=10000, pipeline="main")
        self.assertIn("Warning: Input substitution failed:", s.getvalue())
        self.assertIn("File '{tempdir}a_name.tmp1' does not match regex".format(
            tempdir=tempdir), s.getvalue())

    def test_regex_unmatched_run(self):
        """Run transform(...,regex()...)"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_regex_unmatched_task], verbose=0, multiprocess=parallelism,
                     one_second_per_job=one_second_per_job, pipeline="main")

    # ___________________________________________________________________________
    #
    #   test suffix() pipeline_printout and pipeline_run
    # ___________________________________________________________________________

    def test_suffix_printout(self):
        cleanup_tmpdir()

        s = StringIO()
        pipeline_printout(s, [check_suffix_task], verbose=5,
                          wrap_width=10000, pipeline="main")
        self.assertTrue(re.search(
            'Missing files.*\[{tempdir}a_name.tmp1, {tempdir}a_name.tmp2'.format(tempdir=tempdir), s.getvalue(), re.DOTALL))

    def test_suffix_run(self):
        """Run transform(...,suffix()...)"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_suffix_task], verbose=0, multiprocess=parallelism,
                     one_second_per_job=one_second_per_job, pipeline="main")

    # ___________________________________________________________________________
    #
    #   test suffix() pipeline_printout and pipeline_run
    # ___________________________________________________________________________

    def test_suffix_unmatched(self):
        cleanup_tmpdir()
        s = StringIO()
        self.assertRaisesRegex(fatal_error_input_file_does_not_match,
                               "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*invalid group reference",
                               pipeline_printout,
                               s, [check_suffix_unmatched_task],
                               verbose=3)
        self.assertRaisesRegex(RethrownJobError,
                               "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*invalid group reference",
                               pipeline_run,
                               [check_suffix_unmatched_task], verbose=0, multiprocess=parallelism)

    # ___________________________________________________________________________
    #
    #   test suffix() pipeline_printout and pipeline_run
    # ___________________________________________________________________________

    def test_suffix_unmatched_printout2(self):
        cleanup_tmpdir()
        s = StringIO()
        pipeline_printout(s, [check_suffix_unmatched_task2],
                          verbose=5, wrap_width=10000, pipeline="main")
        self.assertIn("Warning: Input substitution failed:", s.getvalue())
        self.assertIn("File '{tempdir}a_name.tmp1' does not match suffix".format(
            tempdir=tempdir), s.getvalue())

    def test_suffix_unmatched_run2(self):
        """Run transform(...,suffix()...)"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_suffix_unmatched_task2], verbose=0, multiprocess=parallelism,
                     one_second_per_job=one_second_per_job, pipeline="main")

    # ___________________________________________________________________________
    #
    #   test regex() errors: func pipeline_printout
    # ___________________________________________________________________________

    def test_regex_misspelt_capture_error(self):
        cleanup_tmpdir()
        s = StringIO()
        self.assertRaisesRegex(fatal_error_input_file_does_not_match,
                               "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*unknown group name",
                               pipeline_printout,
                               s, [check_regex_misspelt_capture_error_task],
                               verbose=3)
        self.assertRaisesRegex(RethrownJobError,
                               "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*unknown group name",
                               pipeline_run,
                               [check_regex_misspelt_capture_error_task], verbose=0)

    # ___________________________________________________________________________
    #
    #   test regex() errors: func pipeline_printout
    # ___________________________________________________________________________
    def test_regex_misspelt_capture2_error(self):
        cleanup_tmpdir()
        s = StringIO()
        self.assertRaisesRegex(fatal_error_input_file_does_not_match,
                               "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*unknown group name",
                               pipeline_printout,
                               s, [check_regex_misspelt_capture2_error_task],
                               verbose=3)
        self.assertRaisesRegex(RethrownJobError,
                               "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*unknown group name",
                               pipeline_run,
                               [check_regex_misspelt_capture2_error_task], verbose=0, multiprocess=parallelism)

    # ___________________________________________________________________________
    #
    #   test regex() errors: func pipeline_printout
    # ___________________________________________________________________________

    def test_regex_out_of_range_regex_reference_error_printout(self):
        cleanup_tmpdir()
        s = StringIO()
        self.assertRaisesRegex(fatal_error_input_file_does_not_match,
                               "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*invalid group reference",
                               pipeline_printout,
                               s, [check_regex_out_of_range_regex_reference_error_task],
                               verbose=3)
        self.assertRaisesRegex(RethrownJobError,
                               "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*invalid group reference",
                               pipeline_run,
                               [check_regex_out_of_range_regex_reference_error_task], verbose=0, multiprocess=parallelism)

    # ___________________________________________________________________________
    #
    #   cleanup
    # ___________________________________________________________________________

    def tearDown(self):
        pass
        shutil.rmtree(tempdir)


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    # pipeline_printout(sys.stdout, [check_product_task], verbose = 3, pipeline= "main")
    parallelism = 1
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_regex_error_messages)
    unittest.TextTestRunner(verbosity=1).run(suite)
    parallelism = 2
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_regex_error_messages)
    unittest.TextTestRunner(verbosity=1).run(suite)
    # unittest.main()
