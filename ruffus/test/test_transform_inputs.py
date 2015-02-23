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



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
tempdir = "tempdir/"
@follows(mkdir(tempdir))
@files([[None, tempdir+ "a.1"], [None, tempdir+ "b.1"]])
def task1(i, o):
    touch(o)


@follows(mkdir(tempdir))
@files([[None, tempdir+ "c.1"], [None, tempdir+ "d.1"]])
def task2(i, o):
    touch(o)


@transform(task1, regex(r"(.*)"), inputs(((r"\1"), task2, "test_transform_inputs.*y")), r"\1.output")
def task3(i, o):
    names = ",".join(sorted(i))
    for f in o:
        with open(o,  "w") as ff:
            ff.write(names)

@merge((task3), tempdir + "final.output")
def task4(i, o):
    with open(o, "w") as o_file:
        for f in sorted(i):
            with open(f) as ff:
                o_file.write(f +":" + ff.read() + ";")

import unittest

class Test_task(unittest.TestCase):

    def tearDown (self):
        """
        """
        import glob
        for f in glob.glob(tempdir + "*"):
            os.unlink(f)
        os.rmdir(tempdir)


    def test_task (self):
        pipeline_run([task4], multiprocess = 10, verbose = 0)

        correct_output = "tempdir/a.1.output:tempdir/a.1,tempdir/c.1,tempdir/d.1,test_transform_inputs.py;tempdir/b.1.output:tempdir/b.1,tempdir/c.1,tempdir/d.1,test_transform_inputs.py;"
        with open(tempdir + "final.output") as ff:
            real_output = ff.read()
        self.assertEqual(correct_output, real_output)


if __name__ == '__main__':
        unittest.main()

