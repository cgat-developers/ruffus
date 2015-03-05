#!/usr/bin/env python
from __future__ import print_function
"""

    test_inputs_with_multiple_args_raising_exception.py

        inputs with multiple arguments should raise an exception

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

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import unittest

import json
## use simplejson in place of json for python < 2.6
#try:
#    import json
#except ImportError:
#    import simplejson
#    json = simplejson




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
try:
    @transform(None, regex("b"), inputs("a", "b"), "task_1.output")
    def task_1 (i, o):
        for f in o:
            open(f, 'w')
except ruffus.ruffus_exceptions.error_task_transform_inputs_multiple_args:
    print("\tExpected exception thrown 1")
except ruffus.ruffus_exceptions.error_inputs_multiple_args:
    print("\tExpected exception thrown 2")

def task_2 (i, o):
    for f in o:
        open(f, 'w')


class Test_task_mkdir(unittest.TestCase):

    def setUp (self):
        """
        """
        pass

    def tearDown (self):
        """
        """
        pass


    def test_no_re_match (self):
        try:
            pipeline_run(multiprocess = 10, verbose = 0)
        except:
            return
        raise Exception("Inputs(...) with multiple arguments should have thrown an exception")

    def test_newstyle_no_re_match (self):
        try:
            test_pipeline = Pipeline("test")
            test_pipeline.transform(task_func = task_2,
                                    input = None,
                                    filter = regex("b"),
                                    replace_inputs = inputs("a", "b"),
                                    output = "task_1.output")
            test_pipeline.run(multiprocess = 10, verbose = 0)
        except ruffus.ruffus_exceptions.error_task_transform_inputs_multiple_args:
            print("\tExpected exception thrown 1")
            return
        except ruffus.ruffus_exceptions.error_inputs_multiple_args:
            print("\tExpected exception thrown 2")
            return
        raise Exception("Inputs(...) with multiple arguments should have thrown an exception")




if __name__ == '__main__':
        unittest.main()

