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

import json
# use simplejson in place of json for python < 2.6
#try:
#    import json
#except ImportError:
#    import simplejson
#    json = simplejson

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
            fullpath = os.path.join(os.path.dirname(__file__), d)
            os.rmdir(fullpath)
        for d in 'fgh':
            fullpath = os.path.join(os.path.dirname(__file__), d)
            os.unlink(fullpath)


    def test_mkdir (self):
        pipeline_run(multiprocess = 10, verbose = 0)

        for d in 'abcdefgh':
            fullpath = os.path.join(os.path.dirname(__file__), d)
            self.assertTrue(os.path.exists(fullpath))


    def test_newstyle_mkdir (self):
        test_pipeline = Pipeline("test")

        test_pipeline.follows(task_which_makes_directories,
                         mkdir(directories),
                         mkdir(unicode("c")),
                         mkdir(unicode("d"),
                               unicode("e")),
                         mkdir(unicode("e")))\
            .posttask(touch_file(unicode("f")))

        test_pipeline.files(task_which_makes_files, None, ["g", "h"])
        test_pipeline.run(multiprocess = 10, verbose = 0)

        for d in 'abcdefgh':
            fullpath = os.path.join(os.path.dirname(__file__), d)
            self.assertTrue(os.path.exists(fullpath))





if __name__ == '__main__':
    unittest.main()



