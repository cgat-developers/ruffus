#!/usr/bin/env python
from __future__ import print_function
import unittest
import json
from ruffus import follows, posttask, files, suffix, mkdir, Pipeline, touch_file, originate, pipeline_run
import sys

"""

    test_follows_mkdir.py

        test make directory dependencies

        use :
            -j N / --jobs N       to speify multitasking
            -v                    to see the jobs in action
            -n / --just_print     to see what jobs would run

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

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


def touch(filename):
    with open(filename, "w"):
        pass


if sys.hexversion >= 0x03000000:
    unicode = str

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
directories = [os.path.abspath(unicode(tempdir + "a")), unicode(tempdir + "b")]


@follows(mkdir(directories), mkdir(unicode(tempdir + "c")), mkdir(unicode(tempdir + "d"), unicode(tempdir + "e")), mkdir(unicode(tempdir + "e")))
@posttask(touch_file(unicode(tempdir + "f")))
def task_which_makes_directories():
    pass


@originate([tempdir + "g", tempdir + "h"])
def task_which_makes_files(o):
    touch(o)


class Test_task_mkdir(unittest.TestCase):

    def setUp(self):
        """
        """
        os.makedirs(tempdir)
        pass

    def tearDown(self):
        """
        delete directories
        """
        for d in 'abcde':
            fullpath = os.path.join(os.path.dirname(__file__), tempdir, d)
            os.rmdir(fullpath)
        for d in 'fgh':
            fullpath = os.path.join(os.path.dirname(__file__), tempdir, d)
            os.unlink(fullpath)

        os.rmdir(tempdir)

    def test_mkdir(self):
        pipeline_run(multiprocess=10, verbose=0, pipeline="main")

        for d in 'abcdefgh':
            fullpath = os.path.join(os.path.dirname(__file__), tempdir, d)
            self.assertTrue(os.path.exists(fullpath))

    def test_newstyle_mkdir(self):
        test_pipeline = Pipeline("test")

        test_pipeline.follows(task_which_makes_directories,
                              mkdir(directories),
                              mkdir(unicode(tempdir + "c")),
                              mkdir(unicode(tempdir + "d"),
                                    unicode(tempdir + "e")),
                              mkdir(unicode(tempdir + "e")))\
            .posttask(touch_file(unicode(tempdir + "f")))

        test_pipeline.originate(task_which_makes_files, [
                                tempdir + "g", tempdir + "h"])
        test_pipeline.run(multiprocess=10, verbose=0)

        for d in 'abcdefgh':
            fullpath = os.path.join(os.path.dirname(__file__), tempdir, d)
            self.assertTrue(os.path.exists(fullpath))


if __name__ == '__main__':
    unittest.main()
