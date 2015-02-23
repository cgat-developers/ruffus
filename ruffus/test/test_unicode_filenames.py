#!/usr/bin/env python
from __future__ import print_function
"""

    test_follows_mkdir.py

        test make directory dependencies

        use :
            -j N / --jobs N       to speify multitasking
            -v                    to see the jobs in action
            -n / --just_print     to see what jobs would run

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






def touch (filename):
    with open(filename, "w"):
        pass

if sys.hexversion >= 0x03000000:
    unicode = str

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
directories = [os.path.abspath(unicode("a")), unicode("b")]
@follows(mkdir(directories), mkdir(unicode("c")), mkdir(unicode("d"), unicode("e")), mkdir(unicode("e")))
@posttask(touch_file(unicode("f")))
def task_which_makes_directories ():
    pass

@files(None, ["g", "h"])
def task_which_makes_files (i, o):
    for f in o:
        touch(f)

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
            fullpath = os.path.join(exe_path, d)
            os.rmdir(fullpath)
        for d in 'fgh':
            fullpath = os.path.join(exe_path, d)
            os.unlink(fullpath)


    def test_mkdir (self):
        pipeline_run(multiprocess = 10, verbose = 0)

        for d in 'abcdefgh':
            fullpath = os.path.join(exe_path, d)
            self.assertTrue(os.path.exists(fullpath))


if __name__ == '__main__':
    unittest.main()



