#!/usr/bin/env python
from __future__ import print_function
"""

    test_simpler.py

"""


import os
tempdir = os.path.splitext(__file__)[0] + "/"


import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
import ruffus
from ruffus import *

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import unittest
import re
import sys
import os
import json

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

def write_input_output_filenames_to_output(infiles, outfile):
    """
    Helper function: Writes input output file names and input contents to outfile
    """
    with open(outfile, "w") as oo:
        # save file name strings before we turn infiles into a list
        fn_str = "%s -> %s\n" % (infiles, outfile)

        # None = []
        if infiles is None:
            infiles = []
        # str = [str]
        if not isinstance(infiles, list):
            infiles = [infiles]

        max_white_space = -2
        # write content of infiles indented
        for infile in infiles:
            with open(infile) as ii:
                for line in ii:
                    oo.write(line)
                    max_white_space = max([max_white_space, len(line) - len(line.lstrip())])
        # add extra spaces before filenames
        oo.write(" " * (max_white_space + 2) + fn_str)




#
#    task1
#
@originate(tempdir + 'a.1')
def task1(outfile):
    write_input_output_filenames_to_output(None, outfile)



#
#    task2
#
@transform(task1, suffix(".1"), ".2")
def task2(infile, outfile):
    write_input_output_filenames_to_output(infile, outfile)



#
#    task3
#
@transform(task2, suffix(".2"), ".3")
def task3(infile, outfile):
    """
    Third task
    """
    write_input_output_filenames_to_output(infile, outfile)



#
#    task4
#
@transform(task3, suffix(".3"), ".4")
def task4(infile, outfile):
    """
    Fourth task
    """
    write_input_output_filenames_to_output(infile, outfile)





class Test_ruffus(unittest.TestCase):
    def setUp(self):
        self.tearDown()
        try:
            os.makedirs(tempdir)
        except:
            pass




    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_simpler (self):
        pipeline_run(multiprocess = 50, verbose = 0, pipeline= "main")

    def test_newstyle_simpler (self):
        test_pipeline = Pipeline("test")
        test_pipeline.originate(task1, tempdir + 'a.1')
        test_pipeline.transform(task2, task1, suffix(".1"), ".2")
        test_pipeline.transform(task3, task2, suffix(".2"), ".3")
        test_pipeline.transform(task4, task3, suffix(".3"), ".4")
        test_pipeline.run(multiprocess = 50, verbose = 0)




if __name__ == '__main__':
    unittest.main()

