#!/usr/bin/env python
from __future__ import print_function
import unittest
import shutil
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


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ruffus_name = os.path.basename(parent_dir)
ruffus = __import__(ruffus_name)

for attr in "follows", "transform", "merge", "add_inputs", "inputs", "mkdir", "regex", "pipeline_run", "Pipeline":
    globals()[attr] = getattr(ruffus, attr)


print("\tRuffus Version = ", ruffus.__version__)


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


# @transform(input = task1, filter = regex(r"(.+)"), add_inputs = (task2, "test_transform_inputs.*y"), output = r"\1.output")
@transform(input=task1, filter=regex(r"(.+)"), add_inputs=add_inputs(task2, "test_transform_inputs.*y"), output=r"\1.output")
# @transform(input = task1, filter = regex(r"(.+)"), replace_inputs = [task2, "test_transform_inputs.*y"], output = r"\1.output")
# @transform(input = task1, filter = regex(r"(.+)"), replace_inputs = inputs([task2, "test_transform_inputs.*y"]), output = r"\1.output")
def task3_add_inputs(i, o):
    names = ",".join(sorted(i))
    with open(o, "w") as oo:
        oo.write(names)


@merge((task3_add_inputs), tempdir + "final.output")
def task4(i, o):
    with open(o, "w") as o_file:
        for f in sorted(i):
            with open(f) as ii:
                o_file.write(f + ":" + ii.read() + ";")


class Test_task(unittest.TestCase):

    def tearDown(self):
        """
        """
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_task(self):
        pipeline_run(multiprocess=10, verbose=0, pipeline="main")

        correct_output = "{tempdir}a.1.output:{tempdir}a.1,{tempdir}c.1,{tempdir}d.1,test_transform_inputs.py;{tempdir}b.1.output:{tempdir}b.1,{tempdir}c.1,{tempdir}d.1,test_transform_inputs.py;".format(
            tempdir=tempdir)
        with open(tempdir + "final.output") as real_output:
            real_output_str = real_output.read()
        self.assertEqual(correct_output, real_output_str)

    def test_newstyle_task(self):
        test_pipeline = Pipeline("test")

        test_pipeline.files(task1, [[None, tempdir + "a.1"], [None, tempdir + "b.1"]])\
            .follows(mkdir(tempdir))
        test_pipeline.files(task2, [[None, tempdir + "c.1"], [None, tempdir + "d.1"]])\
            .follows(mkdir(tempdir))
        test_pipeline.transform(task_func=task3_add_inputs,
                                input=task1,
                                filter=regex(r"(.+)"),
                                add_inputs=add_inputs(
                                    task2, "test_transform_inputs.*y"),
                                output=r"\1.output")
        test_pipeline.merge(task_func=task4,
                            input=task3_add_inputs,
                            output=tempdir + "final.output")
        test_pipeline.run(multiprocess=10, verbose=0)

        correct_output = "{tempdir}a.1.output:{tempdir}a.1,{tempdir}c.1,{tempdir}d.1,test_transform_inputs.py;{tempdir}b.1.output:{tempdir}b.1,{tempdir}c.1,{tempdir}d.1,test_transform_inputs.py;".format(
            tempdir=tempdir)
        with open(tempdir + "final.output") as real_output:
            real_output_str = real_output.read()
        self.assertEqual(correct_output, real_output_str)


if __name__ == '__main__':
    unittest.main()
