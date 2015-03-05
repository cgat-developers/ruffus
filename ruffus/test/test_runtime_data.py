#!/usr/bin/env python
from __future__ import print_function
"""

    test_tasks.py

"""

runtime_files = ["a.3"]

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
import shutil

import json
# use simplejson in place of json for python < 2.6
#try:
#    import json
#except ImportError:
#    import simplejson
#    json = simplejson




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#
#    task1
#
@originate(['a.1'] + runtime_files)
def task1(outfile):
    """
    First task
    """
    output_text  = ""
    output_text += "    -> " + json.dumps(outfile) + "\n"
    with open(outfile, "w") as oo:
        oo.write(output_text)



#
#    task2
#
@transform(task1, suffix(".1"), ".2")
def task2(infile, outfile):
    """
    Second task
    """
    if infile:
        with open(infile) as ii:
            output_text  = ii.read()
    else:
        output_text = ""
    output_text += json.dumps(infile) + " -> " + json.dumps(outfile) + "\n"
    with open(outfile, "w") as oo:
        oo.write(output_text)



#
#    task3
#
@transform(task2, suffix(".2"), ".3")
def task3(infile, outfile):
    """
    Third task
    """
    if infile:
        with open(infile) as ii:
            output_text  = ii.read()
    else:
        output_text = ""
    output_text += json.dumps(infile) + " -> " + json.dumps(outfile) + "\n"
    with open(outfile, "w") as oo:
        oo.write(output_text)



#
#    task4
#
@follows(task3)
@transform(runtime_parameter("a"), suffix(".3"), ".4")
def task4(infile, outfile):
    """
    Fourth task
    """
    if infile:
        with open(infile) as ii:
            output_text  = ii.read()
    else:
        output_text = ""
    output_text += json.dumps(infile) + " -> " + json.dumps(outfile) + "\n"
    with open(outfile, "w") as oo:
        oo.write(output_text)








class Test_ruffus(unittest.TestCase):
    def setUp(self):
        for f in ["a.1", "a.2","a.3","a.4"]:
            if os.path.exists(f):
                os.unlink(f)

    def tearDown(self):
        for f in ["a.1", "a.2","a.3","a.4"]:
            if os.path.exists(f):
                os.unlink(f)
            else:
                raise Exception("%s is missing" % f)


    def test_ruffus (self):
        pipeline_run(verbose = 0, runtime_data = {"a": runtime_files})


    def test_newstyle_ruffus (self):


        test_pipeline = Pipeline("test")
        test_pipeline.originate(task_func = task1,
                                output = ['a.1'] + runtime_files)
        test_pipeline.transform(task2, task1, suffix(".1"), ".2")
        test_pipeline.transform(task_func = task3,
                                   input = task2,
                                   filter = suffix(".2"),
                                   output = ".3")
        test_pipeline.transform(task_func = task4,
                                input = runtime_parameter("a"),
                                filter = suffix(".3"),
                                output = ".4").follows(task3)
        test_pipeline.run(verbose = 0, runtime_data = {"a": runtime_files})



if __name__ == '__main__':
    unittest.main()

