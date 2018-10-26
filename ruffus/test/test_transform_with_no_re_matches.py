#!/usr/bin/env python
from __future__ import print_function
import unittest
import ruffus
from ruffus import transform, regex, pipeline_run, Pipeline, originate, mkdir
import sys

"""

    test_transform_with_no_re_matches.py

        test messages with no regular expression matches

"""


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]

print("    Ruffus Version = ", ruffus.__version__)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
@mkdir(tempdir)
@originate(tempdir + "a")
def task_1(o):
    open(o, 'w').close()


@transform(task_1, regex("b"), "task_2.output")
def task_2(i, o):
    for f in o:
        with open(f, 'w') as oo:
            pass


class t_save_to_str_logger:
    """
    Everything to stderr
    """

    def __init__(self):
        self.info_str = ""
        self.warning_str = ""
        self.debug_str = ""

    def info(self, message):
        self.info_str += message

    def warning(self, message):
        self.warning_str += message

    def debug(self, message):
        self.debug_str += message


class Test_task_mkdir(unittest.TestCase):

    def setUp(self):
        """
        """
        pass

    def tearDown(self):
        """
        """
        for d in ['a']:
            fullpath = os.path.join(os.path.dirname(__file__), tempdir + d)
            os.unlink(fullpath)
        os.rmdir(tempdir)

    def test_no_re_match(self):

        save_to_str_logger = t_save_to_str_logger()
        pipeline_run(multiprocess=10, logger=save_to_str_logger,
                     verbose=1, pipeline="main")

        print(save_to_str_logger.warning_str)
        self.assertTrue(
            "no file names matched" in save_to_str_logger.warning_str)
        print("\n    Warning printed out correctly", file=sys.stderr)

    def test_newstyle_no_re_match(self):

        test_pipeline = Pipeline("test")
        test_pipeline.originate(task_1, tempdir + "a").mkdir(tempdir)
        test_pipeline.transform(task_2, task_1, regex("b"), "task_2.output")

        save_to_str_logger = t_save_to_str_logger()
        test_pipeline.run(
            multiprocess=10, logger=save_to_str_logger, verbose=1)
        print(save_to_str_logger.warning_str)
        self.assertTrue(
            "no file names matched" in save_to_str_logger.warning_str)
        print("\n    Warning printed out correctly", file=sys.stderr)


if __name__ == '__main__':
    unittest.main()
