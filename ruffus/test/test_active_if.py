#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
import json
from ruffus import transform, follows, originate, pipeline_run, Pipeline, \
    suffix, regex, mkdir, active_if, collate, merge
import sys

"""

    test_active_if.py

"""


import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


def helper(infiles, outfiles):
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
                    output_text += line
                    preamble_len = max(preamble_len, len(
                        line) - len(line.lstrip()))

    preamble = " " * (preamble_len + 4) if len(output_text) else ""

    for outfile in outfiles:
        file_output_text = preamble + \
            json.dumps(infile) + " -> " + json.dumps(outfile) + "\n"
        with open(outfile, "w") as oo:
            oo.write(output_text + file_output_text)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
pipeline_active_if = True
#
#    task1
#


@follows(mkdir("test_active_if"))
@originate(['test_active_if/a.1', 'test_active_if/b.1'], "an extra_parameter")
def task1(outfile, extra):
    """
    First task
    """
    # N.B. originate works with an extra parameter
    helper(None, outfile)


#
#    task2
#
@transform(task1, suffix(".1"), ".2")
def task2(infile, outfile):
    """
    Second task
    """
    helper(infile, outfile)


#
#    task3
#
@active_if(lambda: pipeline_active_if)
@transform(task1, suffix(".1"), ".3")
def task3(infile, outfile):
    """
    Third task
    """
    helper(infile, outfile)


#
#    task4
#
@collate([task2, task3], regex(r"(.+)\.[23]"), r"\1.4")
def task4(infiles, outfile):
    """
    Fourth task
    """
    helper(infiles, outfile)

#
#    task4
#


@merge(task4, "test_active_if/summary.5")
def task5(infiles, outfile):
    """
    Fifth task
    """
    helper(infiles, outfile)


expected_active_text = """null -> "test_active_if/a.1"
    "test_active_if/a.1" -> "test_active_if/a.2"
null -> "test_active_if/a.1"
    "test_active_if/a.1" -> "test_active_if/a.3"
        "test_active_if/a.3" -> "test_active_if/a.4"
null -> "test_active_if/b.1"
    "test_active_if/b.1" -> "test_active_if/b.2"
null -> "test_active_if/b.1"
    "test_active_if/b.1" -> "test_active_if/b.3"
        "test_active_if/b.3" -> "test_active_if/b.4"
            "test_active_if/b.4" -> "test_active_if/summary.5"
"""

expected_inactive_text = """null -> "test_active_if/a.1"
    "test_active_if/a.1" -> "test_active_if/a.2"
        "test_active_if/a.2" -> "test_active_if/a.4"
null -> "test_active_if/b.1"
    "test_active_if/b.1" -> "test_active_if/b.2"
        "test_active_if/b.2" -> "test_active_if/b.4"
            "test_active_if/b.4" -> "test_active_if/summary.5"
"""


# alternative syntax
test_pipeline = Pipeline("test")
test_pipeline.originate(task1, ['test_active_if/a.1', 'test_active_if/b.1'], "an extra_parameter")\
    .follows(mkdir("test_active_if"))
test_pipeline.transform(task2, task1, suffix(".1"), ".2")
test_pipeline.transform(task3, task1, suffix(
    ".1"), ".3").active_if(lambda: pipeline_active_if)
test_pipeline.collate(task4, [task2, task3], regex(r"(.+)\.[23]"), r"\1.4")
test_pipeline.merge(task5, task4, "test_active_if/summary.5")


class Test_ruffus(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass
        os.makedirs(tempdir)

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
            pass
        except:
            pass

    def test_active_if_true(self):
        global pipeline_active_if
        pipeline_active_if = True
        pipeline_run(multiprocess=50, verbose=0, pipeline="main")

        with open("test_active_if/summary.5") as ii:
            active_text = ii.read()
        if active_text != expected_active_text:
            raise Exception("Error:\n\tExpected\n%s\nInstead\n%s\n" %
                            (active_text, expected_active_text))

    def test_active_if_false(self):
        global pipeline_active_if
        pipeline_active_if = False
        pipeline_run(multiprocess=50, verbose=0, pipeline="main")
        with open("test_active_if/summary.5") as ii:
            inactive_text = ii.read()
        if inactive_text != expected_inactive_text:
            raise Exception("Error:\n\tExpected\n%s\nInstead\n%s\n" %
                            (inactive_text, expected_inactive_text))
            shutil.rmtree("test_active_if")

    def test_newstyle_active_if_true(self):
        global pipeline_active_if
        pipeline_active_if = True
        test_pipeline.run(multiprocess=50, verbose=0)

        with open("test_active_if/summary.5") as ii:
            active_text = ii.read()
        if active_text != expected_active_text:
            raise Exception("Error:\n\tExpected\n%s\nInstead\n%s\n" %
                            (active_text, expected_active_text))

    def test_newstyle_active_if_false(self):
        global pipeline_active_if
        pipeline_active_if = False
        test_pipeline.run(multiprocess=50, verbose=0)
        with open("test_active_if/summary.5") as ii:
            inactive_text = ii.read()
        if inactive_text != expected_inactive_text:
            raise Exception("Error:\n\tExpected\n%s\nInstead\n%s\n" %
                            (inactive_text, expected_inactive_text))
            shutil.rmtree("test_active_if")


if __name__ == '__main__':
    unittest.main()
