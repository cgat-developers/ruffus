#!/usr/bin/env python
from __future__ import print_function
import unittest
from ruffus import transform, Pipeline, pipeline_run, regex, inputs
import ruffus
import sys

"""

    test_inputs_with_multiple_args_raising_exception.py

        inputs with multiple arguments should raise an exception

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

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
try:
    @transform(None, regex(tempdir + "b"), inputs(tempdir + "a", tempdir + "b"), "task_1.output")
    def task_1(i, o):
        for f in o:
            open(f, 'w')
except ruffus.ruffus_exceptions.error_task_transform_inputs_multiple_args:
    print("\tExpected exception thrown 1")
except ruffus.ruffus_exceptions.error_inputs_multiple_args:
    print("\tExpected exception thrown 2")


def task_2(i, o):
    for f in o:
        open(f, 'w')


class Test_task_mkdir(unittest.TestCase):

    def setUp(self):
        """
        """
        pass

    def tearDown(self):
        """
        """
        pass

    def test_no_re_match(self):
        try:
            pipeline_run(multiprocess=10, verbose=0, pipeline="main")
        except:
            return
        raise Exception(
            "Inputs(...) with multiple arguments should have thrown an exception")

    def test_newstyle_no_re_match(self):
        try:
            test_pipeline = Pipeline("test")
            test_pipeline.transform(task_func=task_2,
                                    input=None,
                                    filter=regex(tempdir + "b"),
                                    replace_inputs=inputs(
                                        tempdir + "a", tempdir + "b"),
                                    output="task_1.output")
            test_pipeline.run(multiprocess=10, verbose=0)
        except ruffus.ruffus_exceptions.error_task_transform_inputs_multiple_args:
            print("\tExpected exception thrown 1")
            return
        except ruffus.ruffus_exceptions.error_inputs_multiple_args:
            print("\tExpected exception thrown 2")
            return
        raise Exception(
            "Inputs(...) with multiple arguments should have thrown an exception")


if __name__ == '__main__':
    unittest.main()
