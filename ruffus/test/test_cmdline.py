#!/usr/bin/env python
from __future__ import print_function
"""

    test_cmdline.py



"""


import unittest
import os, re
import sys
import shutil
try:
    from StringIO import StringIO
except:
    from io import StringIO
import time

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))

from ruffus.cmdline import handle_verbose
import ruffus.cmdline as cmdline

# mock for command line options
class t_options(object):
    def __str__(self):
        return self.__dict__
    def __repr__(self):
        return str(self.__dict__)

class _AssertRaisesContext_v27(object):
    """A context manager used to implement TestCase.assertRaises* methods."""

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
        self.exception = exc_value # store for later retrieval
        if self.expected_regexp is None:
            return True

        expected_regexp = self.expected_regexp
        if isinstance(expected_regexp, basestring):
            expected_regexp = re.compile(expected_regexp)
        if not expected_regexp.search(str(exc_value)):
            raise self.failureException('"%s" does not match "%s"' %
                     (expected_regexp.pattern, str(exc_value)))
        return True

class Test_cmdline(unittest.TestCase):
    def setUp(self):
        #if sys.hexversion < 0x03000000:
        #    self.assertRaisesRegex = self.assertRaisesRegexp


    #___________________________________________________________________________
    #
    #   test_something()
    #___________________________________________________________________________
    #def test_something(self):
    #    s = StringIO()
    #    cleanup_tmpdir()
    #    pipeline_printout(s, [test_regex_task], verbose=5, wrap_width = 10000)
    #    self.assertTrue(re.search('Missing files\n\s+\[tmp_test_regex_error_messages/a_name.tmp1, tmp_test_regex_error_messages/a_name.tmp2', s.getvalue()))
    #    self.assertIn("Warning: File match failure: File 'tmp_test_regex_error_messages/a_name.tmp1' does not match regex", s.getvalue())
    #    self.assertRaisesRegex(fatal_error_input_file_does_not_match,
    #                            "File '.*?' does not match regex\('.*?'\) and pattern '.*?':\n.*unknown group name",
    #                            pipeline_printout,
    #                            s, [test_regex_misspelt_capture_error_task],
    #                            verbose = 3)


    #___________________________________________________________________________
    #
    #   cleanup
    #___________________________________________________________________________
    #def tearDown(self):
    #    pass
    #    shutil.rmtree(workdir)
    #
    #

    #_____________________________________________________________________________________
    #
    #   test_verbose
    #_____________________________________________________________________________________
    def test_verbose (self):
        """
        --verbose on its own increases the verbosity by one
        --verbose NNN (re)sets the verbosity to NNN whatever the previous state
        """

        # options.verbose defined by user to be None
        options = t_options()
        setattr(options, "verbose", None)
        handle_verbose(options)
        self.assertTrue(options.verbose==None)
        self.assertTrue(options.verbose_abbreviated_path == None)

        # options.verbose defined by user to be 0
        options = t_options()
        setattr(options, "verbose", 0)
        handle_verbose(options)
        self.assertTrue(options.verbose==0)
        self.assertTrue(options.verbose_abbreviated_path == None)

        # options.verbose defined by user to be "6"
        options = t_options()
        setattr(options, "verbose", "6")
        handle_verbose(options)
        self.assertTrue(options.verbose==6)
        self.assertTrue(options.verbose_abbreviated_path==None)

        # options.verbose defined by user to be 6
        options = t_options()
        setattr(options, "verbose", 6)
        handle_verbose(options)
        self.assertTrue(options.verbose==6)
        self.assertTrue(options.verbose_abbreviated_path==None)


        # options.verbose defined by user to "+"
        options = t_options()
        setattr(options, "verbose", "+")
        handle_verbose(options)
        self.assertTrue(options.verbose==1)
        self.assertTrue(options.verbose_abbreviated_path==None)

        # --verbose not set
        options = t_options()
        setattr(options, "verbose", [])
        handle_verbose(options)
        self.assertTrue(options.verbose==0)
        self.assertTrue(options.verbose_abbreviated_path==None)

        # --verbose
        options = t_options()
        setattr(options, "verbose", ["+"])
        handle_verbose(options)
        self.assertTrue(options.verbose==1)
        self.assertTrue(options.verbose_abbreviated_path==None)

        # --verbose --verbose 5 --verbose
        options = t_options()
        setattr(options, "verbose", ["+", "5", "+"])
        handle_verbose(options)
        self.assertTrue(options.verbose==6)
        self.assertTrue(options.verbose_abbreviated_path==None)


        # --verbose --verbose 5 --verbose --verbose 4
        # last value overrides the 5
        options = t_options()
        setattr(options, "verbose", ["+", "5", "+", "4"])
        handle_verbose(options)
        self.assertTrue(options.verbose==4)
        self.assertTrue(options.verbose_abbreviated_path==None)


    #_____________________________________________________________________________________
    #
    #   test_verbose_abbreviated_path
    #_____________________________________________________________________________________
    def test_verbose_abbreviated_path (self):
        """
        --verbose NNN:MMM sets the verbose_abbreviated_path to MMM
        """

        #
        # do not override users' verbose_abbreviated_path
        #
        options = t_options()
        # take verbose_abbreviated_path
        setattr(options, "verbose", ["+", "5", "+", "4:3"])
        handle_verbose(options)
        self.assertTrue(options.verbose==4)
        self.assertTrue(options.verbose_abbreviated_path==3)
        # do not override users' verbose_abbreviated_path
        setattr(options, "verbose", ["+", "5", "+", "7:5"])
        handle_verbose(options)
        self.assertTrue(options.verbose==7)
        self.assertTrue(options.verbose_abbreviated_path==3)


        options = t_options()
        # take verbose_abbreviated_path
        setattr(options, "verbose", ["+", "5:3", "+", "7:5", "+"])
        handle_verbose(options)
        self.assertTrue(options.verbose==8)
        self.assertTrue(options.verbose_abbreviated_path==5)

    #_____________________________________________________________________________________
    #
    #   test_argparse
    #_____________________________________________________________________________________
    def test_argparse(self):
        """
        Same as above but setting up options using ruffus.cmdline.get_argparse
            --verbose on its own increases the verbosity by one
            --verbose NNN (re)sets the verbosity to NNN whatever the previous state
            --verbose NNN:MMM sets the verbose_abbreviated_path to MMM
        """

        parser = cmdline.get_argparse(description='WHAT DOES THIS PIPELINE DO?')

        import sys

        sys.argv = ["test", "--verbose", "--verbose=2"]
        options = parser.parse_args()
        handle_verbose(options)
        self.assertTrue(options.verbose==2)
        self.assertTrue(options.verbose_abbreviated_path==None)

        sys.argv = ["test", "--verbose", "--verbose=3", "--verbose"]
        options = parser.parse_args()
        handle_verbose(options)
        self.assertTrue(options.verbose==4)
        self.assertTrue(options.verbose_abbreviated_path==None)

        sys.argv = ["test", "--verbose", "--verbose=5:3", "--verbose"]
        options = parser.parse_args()
        handle_verbose(options)
        self.assertTrue(options.verbose==6)
        self.assertTrue(options.verbose_abbreviated_path==3)

        sys.argv = ["test", "--verbose", "--verbose=5:3", "--verbose", "--verbose=7", "--verbose"]
        options = parser.parse_args()
        handle_verbose(options)
        self.assertTrue(options.verbose==8)
        self.assertTrue(options.verbose_abbreviated_path==3)

        sys.argv = ["test", "--verbose", "--verbose=5:3", "--verbose", "--verbose=7:5", "--verbose"]
        options = parser.parse_args()
        handle_verbose(options)
        self.assertTrue(options.verbose==8)
        self.assertTrue(options.verbose_abbreviated_path==5)


    #_____________________________________________________________________________________
    #
    #   test_optparse
    #_____________________________________________________________________________________
    def test_optparse(self):
        """
        Same as above but setting up options using ruffus.cmdline.get_opt-parse
            --verbose on its own increases the verbosity by one
            --verbose NNN (re)sets the verbosity to NNN whatever the previous state
            --verbose NNN:MMM sets the verbose_abbreviated_path to MMM
        """
        parser = cmdline.get_optparse(usage='WHAT DOES THIS PIPELINE DO?')

        sys.argv = ["test", "--verbose", "--verbose=2"]
        (options, remaining_args) = parser.parse_args()
        handle_verbose(options)
        self.assertTrue(options.verbose==2)
        self.assertTrue(options.verbose_abbreviated_path==None)

        sys.argv = ["test", "--verbose", "--verbose=3", "--verbose"]
        (options, remaining_args) = parser.parse_args()
        handle_verbose(options)
        self.assertTrue(options.verbose==4)
        self.assertTrue(options.verbose_abbreviated_path==None)

        sys.argv = ["test", "--verbose", "--verbose=5:3", "--verbose"]
        (options, remaining_args) = parser.parse_args()
        handle_verbose(options)
        self.assertTrue(options.verbose==6)
        self.assertTrue(options.verbose_abbreviated_path==3)

        sys.argv = ["test", "--verbose", "--verbose=5:3", "--verbose", "--verbose=7", "--verbose"]
        (options, remaining_args) = parser.parse_args()
        handle_verbose(options)
        self.assertTrue(options.verbose==8)
        self.assertTrue(options.verbose_abbreviated_path==3)

        sys.argv = ["test", "--verbose", "--verbose=5:3", "--verbose", "--verbose=7:5", "--verbose"]
        (options, remaining_args) = parser.parse_args()
        handle_verbose(options)
        self.assertTrue(options.verbose==8)
        self.assertTrue(options.verbose_abbreviated_path==5)



#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    #pipeline_printout(sys.stdout, [test_product_task], verbose = 3)
    unittest.main()
