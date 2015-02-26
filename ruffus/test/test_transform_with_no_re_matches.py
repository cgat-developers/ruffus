#!/usr/bin/env python
from __future__ import print_function
"""

    test_transform_with_no_re_matches.py

        test messages with no regular expression matches

"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys, os
import os.path
try:
    import StringIO as io
except:
    import io as io

import re,time

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__



import ruffus
print("\tRuffus Version = ", ruffus.__version__)





#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import re
import operator
import sys,os
from collections import defaultdict
import random

sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888







#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
@files(None, "a")
def task_1 (i, o):
    for f in o:
        with open(f, 'w') as oo:
            pass

@transform(task_1, regex("b"), "task_2.output")
def task_2 (i, o):
    for f in o:
        with open(f, 'w') as oo:
            pass

import unittest


class t_save_to_str_logger:
    """
    Everything to stderr
    """
    def __init__ (self):
        self.info_str = ""
        self.warning_str = ""
        self.debug_str = ""
    def info (self, message):
        self.info_str += message
    def warning (self, message):
        self.warning_str += message
    def debug (self, message):
        self.debug_str += message

class Test_task_mkdir(unittest.TestCase):

    def setUp (self):
        """
        """
        pass

    def tearDown (self):
        """
        """
        for d in ['a']:
            fullpath = os.path.join(exe_path, d)
            os.unlink(fullpath)


    def test_no_re_match (self):

        save_to_str_logger = t_save_to_str_logger()
        pipeline_run(multiprocess = 10, logger = save_to_str_logger, verbose = 1)

        self.assertTrue("no files names matched" in save_to_str_logger.warning_str)
        print("\n    Warning printed out correctly", file=sys.stderr)

    def test_newstyle_no_re_match (self):

        test_pipeline = Pipeline("test")
        test_pipeline.files(task_1, None, "a")
        test_pipeline.transform(task_2, task_1, regex("b"), "task_2.output")


        save_to_str_logger = t_save_to_str_logger()
        test_pipeline.run(multiprocess = 10, logger = save_to_str_logger, verbose = 1)
        self.assertTrue("no files names matched" in save_to_str_logger.warning_str)
        print("\n    Warning printed out correctly", file=sys.stderr)


if __name__ == '__main__':
    unittest.main()

