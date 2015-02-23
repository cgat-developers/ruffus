#!/usr/bin/env python
from __future__ import print_function
"""

    test_inputs_with_multiple_args_raising_exception.py

        inputs with multiple arguments should raise an exception

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
try:
    @transform(None, regex("b"), inputs("a", "b"), "task_1.output")
    def task_1 (i, o):
        for f in o:
            open(f, 'w')
except ruffus.ruffus_exceptions.error_task_transform_inputs_multiple_args:
    print("\tExpected exception thrown")
    sys.exit(0)
except ruffus.ruffus_exceptions.error_inputs_multiple_args:
    print("\tExpected exception thrown")


import unittest

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


if __name__ == '__main__':
        unittest.main()

