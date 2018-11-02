#!/usr/bin/env python
from __future__ import print_function
import unittest
from ruffus import task
from ruffus import ruffus_exceptions

"""
    test_task_misc.py
"""

import os
import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Test_needs_update_check_directory_missing(unittest.TestCase):

    def setUp(self):
        """
        Create temp directory and temp file
        """
        import tempfile

        # test_file =tempfile.NamedTemporaryFile(delete=False)
        # self.tempfile = test_file.name
        # test_file.close()
        fh, self.tempfile = tempfile.mkstemp(suffix='.dot')
        os.fdopen(fh, "w").close()
        self.directory = tempfile.mkdtemp(prefix='testing_tmp')

    def tearDown(self):
        """
        delete files
        """
        os.unlink(self.tempfile)
        os.removedirs(self.directory)

    def test_up_to_date(self):
        #
        #   lists of files
        #

        self.assertTrue(
            not task.needs_update_check_directory_missing([self.directory])[0])
        self.assertTrue(task.needs_update_check_directory_missing(
            ["missing directory"])[0])
        self.assertRaises(ruffus_exceptions.error_not_a_directory,
                          task.needs_update_check_directory_missing, [self.tempfile])


if __name__ == '__main__':
    unittest.main()
