#!/usr/bin/env python
from __future__ import print_function
from ruffus import pipeline_run, pipeline_printout, Pipeline, formatter, transform, mkdir, originate
import unittest
import shutil
from ruffus.task import t_stream_logger
from ruffus.ruffus_exceptions import RethrownJobError
import ruffus
import re
import sys
import os

"""

    test_transform_formatter.py

"""
JOBS_PER_TASK = 5

tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0]))

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


try:
    from StringIO import StringIO
except:
    from io import StringIO


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
@mkdir(tempdir)
@originate([os.path.join(tempdir, ff + ".tmp") for ff in "abcd"])
def generate_initial_files(out_name):
    with open(out_name, 'w') as outfile:
        pass


@transform(input=generate_initial_files, filter=formatter(), output="{path[0]}/{basename[0]}.task1.{whatever}",
           extras=['echo {dynamic_message} > {some_file}'])
def transform_with_missing_formatter_args(input_file, output_files, output1):
    print("input = %r, output = %r, extras = %r" %
          (input_file, output_files, output1))


class Test_ruffus(unittest.TestCase):
    # ___________________________________________________________________________
    #
    #   setup and cleanup
    # ___________________________________________________________________________
    def setUp(self):
        import os
        try:
            shutil.rmtree(tempdir)
        except:
            pass
        os.makedirs(tempdir)

    def tearDown(self):
        shutil.rmtree(tempdir)

    # ___________________________________________________________________________
    #
    #   test product() pipeline_printout and pipeline_run
    # ___________________________________________________________________________
    def test_transform_with_missing_formatter_args(self):
        s = StringIO()
        pipeline_printout(s, [transform_with_missing_formatter_args],
                          verbose=4, wrap_width=10000, pipeline="main")
        self.assertIn("Unmatched field {dynamic_message}", s.getvalue())
        pipeline_run([transform_with_missing_formatter_args],
                     verbose=0, pipeline="main")

    def test_transform_with_missing_formatter_args_b(self):
        test_pipeline = Pipeline("test")

        test_pipeline.originate(task_func=generate_initial_files,
                                output=[os.path.join(tempdir, ff + ".tmp") for ff in "abcd"])\
            .mkdir(tempdir)

        test_pipeline.transform(task_func=transform_with_missing_formatter_args,
                                input=generate_initial_files,
                                filter=formatter(),
                                output="{path[0]}/{basename[0]}.task1",
                                extras=['echo {dynamic_message} > {some_file}'])
        s = StringIO()
        test_pipeline.printout(
            s, [transform_with_missing_formatter_args], verbose=4, wrap_width=10000, pipeline="test")
        self.assertIn("Unmatched field {dynamic_message}", s.getvalue())

        # log to stream
        s = StringIO()
        logger = t_stream_logger(s)
        test_pipeline.run([transform_with_missing_formatter_args],
                          verbose=5, pipeline="test", logger=logger)
        self.assertIn("Unmatched field {dynamic_message}", s.getvalue())


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    unittest.main()
