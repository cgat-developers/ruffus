#!/usr/bin/env python
from __future__ import print_function
"""
    test_follows_mkdir.py
"""


import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"
import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]

import ruffus
from ruffus import follows, pipeline_run, Pipeline, mkdir




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
directories = [os.path.abspath(tempdir +'a'), tempdir + 'b']
@follows(mkdir(tempdir), mkdir(directories), mkdir(tempdir +'c'), mkdir(tempdir +'d', tempdir +'e'), mkdir(tempdir +'e'))
def task_which_makes_directories ():
    pass


import unittest

class Test_task_mkdir(unittest.TestCase):

    def setUp (self):
        """
        """
        pass

    def tearDown (self):
        """
        delete directories
        """
        for d in 'abcde':
            fullpath = os.path.join(os.path.dirname(__file__), tempdir, d)
            os.rmdir(fullpath)
        os.rmdir(tempdir)


    def test_mkdir (self):
        pipeline_run(multiprocess = 10, verbose = 0, pipeline= "main")

        for d in 'abcde':
            fullpath = os.path.join(os.path.dirname(__file__), tempdir, d)
            self.assertTrue(os.path.exists(fullpath))

    def test_newstyle_mkdir (self):
        test_pipeline = Pipeline("test")
        test_pipeline.follows(task_which_makes_directories, mkdir(directories), mkdir(tempdir + 'c'), mkdir(tempdir + 'd', tempdir + 'e'), mkdir(tempdir + 'e'))
        test_pipeline.run(multiprocess = 10, verbose = 0)

        for d in 'abcde':
            fullpath = os.path.join(os.path.dirname(__file__), tempdir, d)
            self.assertTrue(os.path.exists(fullpath))




if __name__ == '__main__':
    unittest.main()

