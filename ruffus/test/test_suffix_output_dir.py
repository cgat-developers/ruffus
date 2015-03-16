#!/usr/bin/env python
from __future__ import print_function
"""

    test_suffix_output_dir.py

"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0]))
data_dir  = tempdir + "/data"
work_dir  = tempdir + "/work"
import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]

import ruffus
from ruffus import transform, subdivide, merge, suffix, mkdir, pipeline_run, Pipeline, originate


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import unittest
import shutil
import json



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

def helper (infiles, outfiles):
    if not isinstance(infiles, (tuple, list)):
        infiles = [infiles]
    if not isinstance(outfiles, list):
        outfiles = [outfiles]

    output_text = ""
    preamble_len = 0
    for infile in infiles:
        if infile:
            with open(infile) as ii:
                for line in ii:
                    output_text  += line
                    preamble_len = max(preamble_len, len(line) - len(line.lstrip()))

    preamble = " " * (preamble_len + 4) if len(output_text) else ""

    for outfile in outfiles:
        file_output_text = preamble + json.dumps(infiles) + " -> " + json.dumps(outfiles) + "\n"
        with open(outfile, "w") as oo:
            oo.write(output_text + file_output_text)



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
#    task1
#
@mkdir(data_dir, work_dir)
@originate([os.path.join(data_dir, "%s.1" % aa) for aa in "abcd"])
def task1(outfile):
    """
    First task
    """
    # N.B. originate works with an extra parameter
    helper (None, outfile)



#
#    task2
#
@mkdir( task1,
        suffix(".1"),
        ".dir",
        output_dir = work_dir)
@transform(task1, suffix(".1"), ".1", "extra.tst", 4, r"orig_dir=\1", output_dir = work_dir)
def task2(infile, outfile, extra_str, extra_num, extra_dir):
    """
    Second task
    """
    if (extra_str, extra_num) != ("extra.tst", 4) and \
       extra_dir[:len("orig_dir=" + data_dir)] != "orig_dir=" + data_dir:
        raise Exception("transform with output_dir has changed extras")
    helper (infile, outfile)


#
#    task3
#
@subdivide(task2, suffix(".1"), r"\1.*.2", [r"\1.a.2", r"\1.b.2"])
def task3(infile, ignore_outfiles, outfiles):
    """
    Third task
    """
    helper (infile, outfiles)



#
#    task4
#
@transform(task3, suffix(".2"), ".3", output_dir = work_dir)
def task4(infile, outfile):
    """
    Fourth task
    """
    helper (infile, outfile)

#
#    task4
#
@merge(task4, os.path.join(data_dir, "summary.5"))
def task5(infiles, outfile):
    """
    Fifth task
    """
    helper (infiles, outfile)


expected_active_text = """[null] -> ["{tempdir}/data/a.1"]
    ["{tempdir}/data/a.1"] -> ["{tempdir}/work/a.1"]
        ["{tempdir}/work/a.1"] -> ["{tempdir}/work/a.a.2", "{tempdir}/work/a.b.2"]
            ["{tempdir}/work/a.a.2"] -> ["{tempdir}/work/a.a.3"]
[null] -> ["{tempdir}/data/a.1"]
    ["{tempdir}/data/a.1"] -> ["{tempdir}/work/a.1"]
        ["{tempdir}/work/a.1"] -> ["{tempdir}/work/a.a.2", "{tempdir}/work/a.b.2"]
            ["{tempdir}/work/a.b.2"] -> ["{tempdir}/work/a.b.3"]
[null] -> ["{tempdir}/data/b.1"]
    ["{tempdir}/data/b.1"] -> ["{tempdir}/work/b.1"]
        ["{tempdir}/work/b.1"] -> ["{tempdir}/work/b.a.2", "{tempdir}/work/b.b.2"]
            ["{tempdir}/work/b.a.2"] -> ["{tempdir}/work/b.a.3"]
[null] -> ["{tempdir}/data/b.1"]
    ["{tempdir}/data/b.1"] -> ["{tempdir}/work/b.1"]
        ["{tempdir}/work/b.1"] -> ["{tempdir}/work/b.a.2", "{tempdir}/work/b.b.2"]
            ["{tempdir}/work/b.b.2"] -> ["{tempdir}/work/b.b.3"]
[null] -> ["{tempdir}/data/c.1"]
    ["{tempdir}/data/c.1"] -> ["{tempdir}/work/c.1"]
        ["{tempdir}/work/c.1"] -> ["{tempdir}/work/c.a.2", "{tempdir}/work/c.b.2"]
            ["{tempdir}/work/c.a.2"] -> ["{tempdir}/work/c.a.3"]
[null] -> ["{tempdir}/data/c.1"]
    ["{tempdir}/data/c.1"] -> ["{tempdir}/work/c.1"]
        ["{tempdir}/work/c.1"] -> ["{tempdir}/work/c.a.2", "{tempdir}/work/c.b.2"]
            ["{tempdir}/work/c.b.2"] -> ["{tempdir}/work/c.b.3"]
[null] -> ["{tempdir}/data/d.1"]
    ["{tempdir}/data/d.1"] -> ["{tempdir}/work/d.1"]
        ["{tempdir}/work/d.1"] -> ["{tempdir}/work/d.a.2", "{tempdir}/work/d.b.2"]
            ["{tempdir}/work/d.a.2"] -> ["{tempdir}/work/d.a.3"]
[null] -> ["{tempdir}/data/d.1"]
    ["{tempdir}/data/d.1"] -> ["{tempdir}/work/d.1"]
        ["{tempdir}/work/d.1"] -> ["{tempdir}/work/d.a.2", "{tempdir}/work/d.b.2"]
            ["{tempdir}/work/d.b.2"] -> ["{tempdir}/work/d.b.3"]
                ["{tempdir}/work/a.a.3", "{tempdir}/work/a.b.3", "{tempdir}/work/b.a.3", "{tempdir}/work/b.b.3", "{tempdir}/work/c.a.3", "{tempdir}/work/c.b.3", "{tempdir}/work/d.a.3", "{tempdir}/work/d.b.3"] -> ["{tempdir}/data/summary.5"]
""".format(tempdir = tempdir)






class Test_ruffus(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass
        for dd in tempdir, work_dir, data_dir:
            try:
                os.makedirs(dd)
            except:
                pass



    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
        except:
            sys.stderr.write("Can't remove %s" % tempdir)
            pass

    def test_ruffus (self):
        pipeline_run(multiprocess = 50, verbose = 0, pipeline= "main")

        with open(os.path.join(data_dir, "summary.5")) as ii:
            active_text = ii.read()
        if active_text != expected_active_text:
            raise Exception("Error:\n\tExpected\n%s\nInstead\n%s\n"  % (expected_active_text, active_text))

    def test_newstyle_ruffus (self):
        # alternative syntax
        test_pipeline = Pipeline("test")


        test_pipeline.mkdir(data_dir, work_dir)
        test_pipeline.originate(task_func   = task1,
                                output      = [os.path.join(data_dir, "%s.1" % aa) for aa in "abcd"])

        test_pipeline.mkdir(filter      = suffix(".1"),
                            output      = ".dir",
                            output_dir = work_dir)

        test_pipeline.transform(task_func   = task2,
                                input       = task1,
                                filter      = suffix(".1"),
                                output      = ".1",
                                extras      = ["extra.tst", 4, r"orig_dir=\1"],
                                output_dir  = work_dir)

        test_pipeline.subdivide(task3, task2, suffix(".1"), r"\1.*.2", [r"\1.a.2", r"\1.b.2"])
        test_pipeline.transform(task4, task3, suffix(".2"), ".3", output_dir = work_dir)
        test_pipeline.merge(task5, task4, os.path.join(data_dir, "summary.5"))
        test_pipeline.run(multiprocess = 50, verbose = 0)

        with open(os.path.join(data_dir, "summary.5")) as ii:
            active_text = ii.read()
        if active_text != expected_active_text:
            raise Exception("Error:\n\tExpected\n%s\nInstead\n%s\n"  % (expected_active_text, active_text))



if __name__ == '__main__':
    unittest.main()

