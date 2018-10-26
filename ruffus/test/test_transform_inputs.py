#!/usr/bin/env python
from __future__ import print_function
import unittest
import shutil
from ruffus import follows, mkdir, transform, regex, merge, Pipeline, pipeline_run
import ruffus
import sys

"""

    test_transform_with_no_re_matches.py

        test messages with no regular expression matches

"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


def touch(outfile):
    with open(outfile, "w"):
        pass


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
@follows(mkdir(tempdir))
@ruffus.files([[None, tempdir + "a.1"], [None, tempdir + "b.1"]])
def task1(i, o):
    touch(o)


@follows(mkdir(tempdir))
@ruffus.files([[None, tempdir + "c.1"], [None, tempdir + "d.1"]])
def task2(i, o):
    touch(o)


@transform(task1, regex(r"(.+)"), ruffus.inputs(((r"\1"), task2, "test_transform_inputs.*y")), r"\1.output")
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
                o_file.write(f + ":" + ff.read() + ";")


class Test_task(unittest.TestCase):

    def tearDown(self):
        """
        """
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_task(self):
        pipeline_run([task4], multiprocess=10, verbose=0, pipeline="main")

        correct_output = "{tempdir}a.1.output:test_transform_inputs.py,{tempdir}a.1,{tempdir}c.1,{tempdir}d.1;{tempdir}b.1.output:test_transform_inputs.py,{tempdir}b.1,{tempdir}c.1,{tempdir}d.1;".format(
            tempdir=tempdir)
        with open(tempdir + "final.output") as ff:
            real_output = ff.read()
        self.assertEqual(correct_output, real_output)

    def test_newstyle_task(self):
        test_pipeline = Pipeline("test")

        test_pipeline.files(task1, [[None, tempdir + "a.1"], [None, tempdir + "b.1"]])\
            .follows(mkdir(tempdir))

        test_pipeline.files(task2, [[None, tempdir + "c.1"], [None, tempdir + "d.1"]])\
            .follows(mkdir(tempdir))

        test_pipeline.transform(task_func=task3,
                                input=task1,
                                filter=regex(r"(.+)"),
                                replace_inputs=ruffus.inputs(
                                    ((r"\1"), task2, "test_transform_inputs.*y")),
                                output=r"\1.output")
        test_pipeline.merge(task4, (task3), tempdir + "final.output")

        test_pipeline.run([task4], multiprocess=10, verbose=0)

        correct_output = "{tempdir}a.1.output:test_transform_inputs.py,{tempdir}a.1,{tempdir}c.1,{tempdir}d.1;{tempdir}b.1.output:test_transform_inputs.py,{tempdir}b.1,{tempdir}c.1,{tempdir}d.1;".format(
            tempdir=tempdir)
        with open(tempdir + "final.output") as ff:
            real_output = ff.read()
        self.assertEqual(correct_output, real_output)


if __name__ == '__main__':
    unittest.main()
