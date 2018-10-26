#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
from ruffus import posttask, parallel, check_if_uptodate, follows, touch_file, pipeline_printout, pipeline_run
import sys

"""
Test check_if_uptodate

    Bug: @parallel sets @check_if_uptodate to None.
    Submitted by Jafar Taghiyar (jafar<dot>taghiyar<at>gmail.com)
    https://github.com/bunbun/ruffus/issues/53

"""
import os
tempdir = os.path.abspath(os.path.abspath(os.path.splitext(__file__)[0]))
exe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

try:
    from StringIO import StringIO
except:
    from io import StringIO


def sentinel_file_exists(output_file):
    if not os.path.exists(output_file):
        return True, "Missing file %s" % output_file
    else:
        return False, "File %s exists" % output_file


@posttask(touch_file(os.path.join(tempdir, "task1_completed.flag")))
@parallel([[os.path.join(tempdir, "task1_completed.flag")]])
@check_if_uptodate(sentinel_file_exists)
def task1(x):
    pass


@follows(task1)
@posttask(touch_file(os.path.join(tempdir, "task2_completed.flag")))
@parallel([[os.path.join(tempdir, "task2_completed.flag")]])
@check_if_uptodate(sentinel_file_exists)
def task2(x):
    pass


class Test_ruffus(unittest.TestCase):

    def do_assertNotRegexpMatches(self, test_str, re_str):
        import re
        if re.search(re_str, test_str) is not None:
            raise AssertionError(
                "Regexp matched: %r found in %r" % (re_str, test_str))

    def do_assertRegexpMatches(self, test_str, re_str):
        import re
        if re.search(re_str, test_str) is None:
            # AssertionError:
            raise AssertionError(
                "Regexp didn't match: %r not found in %r" % (re_str, test_str))

    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass
        os.makedirs(tempdir)

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_ruffus(self):
        # run first
        pipeline_run(verbose=0)
        # should now be out of date
        s = StringIO()
        pipeline_printout(s, verbose=5)

        ret = s.getvalue()
        try:
            self.do_assertRegexpMatches(
                ret, r"Tasks which are up-to-date:(\n\s*)*Task = 'test_check_if_uptodate.task1'(\n\s*)*Task = 'test_check_if_uptodate.task2'")
        except:
            print("\n\tOops: Both tasks should be up to date!!\n\n")
            raise
        try:
            self.do_assertNotRegexpMatches(
                ret, r"Jobs needs update:\s*No function to check if up-to-date")
        except:
            print("\n\tOops: @check_if_uptodate is not being picked up!!\n\n")
            raise


if __name__ == '__main__':
    unittest.main()
