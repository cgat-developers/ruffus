#!/usr/bin/env python
from __future__ import print_function
"""
    test_follows_mkdir.py
"""


import os
import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ruffus_name = os.path.basename(parent_dir)
ruffus = __import__ (ruffus_name)

try:
    attrlist = ruffus.__all__
except AttributeError:
    attrlist = dir (ruffus)
for attr in attrlist:
    if attr[0:2] != "__":
        globals()[attr] = getattr (ruffus, attr)





#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
directories = [os.path.abspath('a'), 'b']
@follows(mkdir(directories), mkdir('c'), mkdir('d', 'e'), mkdir('e'))
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
            fullpath = os.path.join(os.path.dirname(__file__), d)
            os.rmdir(fullpath)


    def test_mkdir (self):
        pipeline_run(multiprocess = 10, verbose = 0)

        for d in 'abcde':
            fullpath = os.path.join(os.path.dirname(__file__), d)
            self.assertTrue(os.path.exists(fullpath))

    def test_newstyle_mkdir (self):
        test_pipeline = Pipeline("test")
        test_pipeline.follows(task_which_makes_directories, mkdir(directories), mkdir('c'), mkdir('d', 'e'), mkdir('e'))
        test_pipeline.run(multiprocess = 10, verbose = 0)

        for d in 'abcde':
            fullpath = os.path.join(os.path.dirname(__file__), d)
            self.assertTrue(os.path.exists(fullpath))




if __name__ == '__main__':
    unittest.main()

