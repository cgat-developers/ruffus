#!/usr/bin/env python
from __future__ import print_function
"""

    test_verbosity.py

"""
temp_dir = "test_verbosity/"

import unittest

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
ruffus = list(map(__import__, [ruffus_name]))[0]


import shutil
try:
    from StringIO import StringIO
except:
    from io import StringIO
import re

ruffus = __import__ (ruffus_name)
for attr in "pipeline_run", "pipeline_printout", "suffix", "transform", "split", "merge", "dbdict", "follows", "mkdir", "originate", "Pipeline":
    globals()[attr] = getattr (ruffus, attr)
RethrownJobError =  ruffus.ruffus_exceptions.RethrownJobError
RUFFUS_HISTORY_FILE      = ruffus.ruffus_utility.RUFFUS_HISTORY_FILE
CHECKSUM_FILE_TIMESTAMPS = ruffus.ruffus_utility.CHECKSUM_FILE_TIMESTAMPS




#---------------------------------------------------------------
#   create initial files
#
@mkdir(temp_dir + 'data/scratch/lg/what/one/two/three/')
@originate([   [temp_dir + 'data/scratch/lg/what/one/two/three/job1.a.start', temp_dir + 'job1.b.start'],
               [temp_dir + 'data/scratch/lg/what/one/two/three/job2.a.start', temp_dir + 'job2.b.start'],
               [temp_dir + 'data/scratch/lg/what/one/two/three/job3.a.start', temp_dir + 'job3.b.start']    ])
def create_initial_file_pairs(output_files):
    # create both files as necessary
    for output_file in output_files:
        with open(output_file, "w") as oo: pass

#---------------------------------------------------------------
#   first task
@transform(create_initial_file_pairs, suffix(".start"), ".output.1")
def first_task(input_files, output_file):
    with open(output_file, "w"): pass


#---------------------------------------------------------------
#   second task
@transform(first_task, suffix(".output.1"), ".output.2")
def second_task(input_files, output_file):
    with open(output_file, "w"): pass

test_pipeline = Pipeline("test")
test_pipeline.originate(output = [    [temp_dir + 'data/scratch/lg/what/one/two/three/job1.a.start',  temp_dir + 'job1.b.start'],
                                       [temp_dir + 'data/scratch/lg/what/one/two/three/job2.a.start', temp_dir + 'job2.b.start'],
                                       [temp_dir + 'data/scratch/lg/what/one/two/three/job3.a.start', temp_dir + 'job3.b.start']    ],
                                       task_func = create_initial_file_pairs)
test_pipeline.transform(task_func = first_task, input = create_initial_file_pairs, filter = suffix(".start"), output = ".output.1")
test_pipeline.transform(input = first_task, filter = suffix(".output.1"), output = ".output.2", task_func= second_task)


decorator_syntax = 0
oop_syntax = 1

class Test_verbosity(unittest.TestCase):
    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path1
    #___________________________________________________________________________
    def test_printout_abbreviated_path1(self):
        """Input file exists, output doesn't exist"""
        for syntax in decorator_syntax, oop_syntax:
            s = StringIO()
            if syntax == oop_syntax:
                test_pipeline.printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 1)
            else:
                pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 1, wrap_width = 500)
            ret = s.getvalue()
            print (ret)
            self.assertTrue(re.search('Job needs update:.*Missing files.*'
                          '\[\.\.\./job2\.a\.start, test_verbosity/job2\.b\.start, \.\.\./job2.a.output.1\]', ret, re.DOTALL) is not None)


    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path2
    #___________________________________________________________________________
    def test_printout_abbreviated_path2(self):
        """Input file exists, output doesn't exist"""
        for syntax in decorator_syntax, oop_syntax:
            s = StringIO()
            if syntax == oop_syntax:
                test_pipeline.printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 2, wrap_width = 500)
            else:
                pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 2, wrap_width = 500)
            ret = s.getvalue()
            self.assertTrue('[.../three/job1.a.start, test_verbosity/job1.b.start, .../three/job1.a.output.1]' in ret)


    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path3
    #___________________________________________________________________________
    def test_printout_abbreviated_path3(self):
        """Input file exists, output doesn't exist"""
        for syntax in decorator_syntax, oop_syntax:
            s = StringIO()
            if syntax == oop_syntax:
                test_pipeline.printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 3, wrap_width = 500)
            else:
                pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 3, wrap_width = 500)
            ret = s.getvalue()
            self.assertTrue('[.../two/three/job1.a.start, test_verbosity/job1.b.start, .../two/three/job1.a.output.1]' in s.getvalue())

    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path9
    #___________________________________________________________________________
    def test_printout_abbreviated_path9(self):
        """Input file exists, output doesn't exist"""
        for syntax in decorator_syntax, oop_syntax:
            s = StringIO()
            if syntax == oop_syntax:
                test_pipeline.printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 9, wrap_width = 500)
            else:
                pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 9, wrap_width = 500)
            ret = s.getvalue()
            self.assertTrue('[%sdata/scratch/lg/what/one/two/three/job2.a.start, test_verbosity/job2.b.start,' % temp_dir in ret)


    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path0
    #___________________________________________________________________________
    def test_printout_abbreviated_path0(self):
        """Input file exists, output doesn't exist"""
        for syntax in decorator_syntax, oop_syntax:
            s = StringIO()
            if syntax == oop_syntax:
                test_pipeline.printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 0, wrap_width = 500)
            else:
                pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = 0, wrap_width = 500)
            ret = s.getvalue()
            path_str = os.path.abspath('%sdata/scratch/lg/what/one/two/three/job2.a.start'  % temp_dir)
            path_str = '[[%s' % path_str
            self.assertTrue(path_str in ret)
        self.assertTrue(temp_dir + 'job2.b.start]' in ret)



    #___________________________________________________________________________
    #
    #   test_printout_abbreviated_path_minus_60
    #___________________________________________________________________________
    def test_printout_abbreviated_path_minus_60(self):
        """Input file exists, output doesn't exist"""
        for syntax in decorator_syntax, oop_syntax:
            s = StringIO()
            if syntax == oop_syntax:
                test_pipeline.printout(s, [second_task], verbose = 5, verbose_abbreviated_path = -60, wrap_width = 500)
            else:
                pipeline_printout(s, [second_task], verbose = 5, verbose_abbreviated_path = -60, wrap_width = 500)
            ret = s.getvalue()
            self.assertTrue('[<???> ne/two/three/job2.a.start, test_verbosity/job2.b.start]' in ret)


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    unittest.main()

