#!/usr/bin/env python
from __future__ import print_function
"""

    test_exceptions.py

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
import ruffus
from ruffus import pipeline_run, pipeline_printout, Pipeline, parallel




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

@parallel([['A', 1], ['B',3], ['C',3], ['D',4], ['E',4], ['F',4]])
def parallel_task(name, param1):
    sys.stderr.write("    Parallel task %s: \n" % name)
    #raise task.JobSignalledBreak("Oops! I did it again!")
    print ("    Raising exception", file = sys.stderr)
    raise Exception("new")


import unittest, shutil
try:
    from StringIO import StringIO
except:
    from io import StringIO

class Test_ruffus(unittest.TestCase):
    def test_ruffus (self):
        try:
            pipeline_run(multiprocess = 50, verbose = 0, pipeline= "main")
        except ruffus.ruffus_exceptions.RethrownJobError:
            return
        raise Exception("Missing exception")

    def test_newstyle_ruffus (self):
        test_pipeline = Pipeline("test")
        test_pipeline.parallel(parallel_task, [['A', 1], ['B',3], ['C',3], ['D',4], ['E',4], ['F',4]])
        try:
            test_pipeline.run(multiprocess = 50, verbose = 0)
        except ruffus.ruffus_exceptions.RethrownJobError:
            return
        raise Exception("Missing exception")




if __name__ == '__main__':
    unittest.main()


