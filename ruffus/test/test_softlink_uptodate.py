#!/usr/bin/env python
from __future__ import print_function
import unittest
from ruffus import originate, transform, Pipeline, pipeline_run, suffix
import sys

"""
    test_softlink_uptodate.py
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

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
#   First task
#
@originate(["a.1", "b.1"])
def start_task(output_file_name):
    with open(output_file_name,  "w") as f:
        pass

#
#   Forwards file names, is always as up to date as its input files...
#


@transform(start_task, suffix(".1"), ".1")
def same_file_name_task(input_file_name, output_file_name):
    pass

#
#   Links file names, is always as up to date if links are not missing
#


@transform(start_task, suffix(".1"), ".linked.1")
def linked_file_name_task(input_file_name, output_file_name):
    try:
        os.symlink(input_file_name, output_file_name)
    except:
        print(input_file_name, output_file_name)
        raise


#
#   Final task linking everything
#
@transform([linked_file_name_task, same_file_name_task], suffix(".1"), ".3")
def final_task(input_file_name, output_file_name):
    with open(output_file_name,  "w") as f:
        pass

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Run pipeline


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


try:
    from StringIO import StringIO
except:
    from io import StringIO


class Test_ruffus(unittest.TestCase):
    def setUp(self):
        for f in ["a.1", "b.1", "a.linked.1", "b.linked.1", "a.3", "b.3", "a.linked.3", "b.linked.3"]:
            try:
                if os.path.exists(f):
                    os.unlink(f)
            except:
                print("    !!!!OOPs. Can't unlink %s" % f, file=sys.stderr)
                pass

    def tearDown(self):
        for f in ["a.1", "b.1", "a.linked.1", "b.linked.1", "a.3", "b.3", "a.linked.3", "b.linked.3"]:
            if os.path.lexists(f):
                os.unlink(f)
            else:
                raise Exception("Expected %s missing" % f)

    def test_ruffus(self):
        pipeline_run(log_exceptions=True, verbose=0, pipeline="main")

    def test_newstyle_ruffus(self):
        test_pipeline = Pipeline("test")
        test_pipeline.originate(start_task, ["a.1", "b.1"])
        test_pipeline.transform(same_file_name_task,
                                start_task, suffix(".1"), ".1")
        test_pipeline.transform(linked_file_name_task,
                                start_task, suffix(".1"), ".linked.1")
        test_pipeline.transform(
            final_task, [linked_file_name_task, same_file_name_task], suffix(".1"), ".3")
        test_pipeline.run(log_exceptions=True, verbose=0)


if __name__ == '__main__':
    unittest.main()
