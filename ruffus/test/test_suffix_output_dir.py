#!/usr/bin/env python
from __future__ import print_function
import json
import shutil
import unittest
from ruffus import transform, subdivide, merge, suffix, mkdir, pipeline_run, Pipeline, originate
import ruffus
import sys

"""

    test_suffix_output_dir.py

"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0]))
data_dir = tempdir + "/data"
work_dir = tempdir + "/work"

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
    """
    Helper function: Writes input output file names and input contents to outfile
    """
    # None = []
    if outfiles is None:
        outfiles = []
    # str = [str]
    if not isinstance(outfiles, list):
        outfiles = [outfiles]

    for outfile in outfiles:
        with open(outfile, "w") as oo:
            # save file name strings before we turn infiles into a list
            fn_str = "%s -> %s" % (infiles, outfile)

            # None = []
            if infiles is None:
                infiles = []
            # str = [str]
            if not isinstance(infiles, list):
                infiles = [infiles]

            # write header
            # if len(infiles):
            #    for infile in infiles:
            #        with open(infile) as ii:
            #            for line in ii:
            #                line = line.rstrip()
            #                if line[-1:] == ":":
            #                    oo.write(outfile + ":" + line + "\n")
            # else:
            #    oo.write(outfile + ":\n")

            max_white_space = -2
            # write content of infiles indented
            for infile in infiles:
                with open(infile) as ii:
                    for line in ii:
                        line = line.rstrip()
                        if line[-1:] != ":":
                            oo.write(line + "\n")
                        max_white_space = max(
                            [max_white_space, len(line) - len(line.lstrip())])

            # add extra spaces before filenames
            oo.write(" " * (max_white_space + 2) + fn_str + "\n")


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
#    task1
#
@mkdir(data_dir, work_dir)
@originate([os.path.join(data_dir, "%s.1" % aa) for aa in "abcd"])
def task1(outfile):
    """
    originate
    """
    # N.B. originate works with an extra parameter
    helper(None, outfile)


#
#    task2
#
@mkdir(task1,
       suffix(".1"),
       ".dir",
       output_dir=work_dir)
@transform(task1, suffix(".1"), [".1", ".bak"], "extra.tst", 4, r"orig_dir=\1", output_dir=work_dir)
def task2(infile, outfile, extra_str, extra_num, extra_dir):
    """
    transform switch directory
    """
    if (extra_str, extra_num) != ("extra.tst", 4) or \
       extra_dir[:len("orig_dir=" + work_dir)] != "orig_dir=" + work_dir:
        raise Exception("transform with output_dir has changed extras: %s, %s %s"
                        % (extra_str, extra_num, extra_dir))
    helper(infile, outfile)


#
#    task3
#
@subdivide(task2, suffix(".1"), r"\1.*.2", [r"\1.a.2", r"\1.b.2"], output_dir=data_dir)
def task3(infile, ignore_outfiles, outfiles):
    """
    subdivide
    """
    helper(infile, outfiles)


#
#    task4
#
@transform(task3, suffix(".2"), ".3", output_dir=work_dir)
def task4(infile, outfile):
    """
    transform
    """
    helper(infile, outfile)

#
#    task4
#


@merge(task4, os.path.join(data_dir, "summary.5"))
def task5(infiles, outfile):
    """
    merge
    """
    helper(infiles, outfile)


expected_active_text = \
    """None -> {tempdir}/data/a.1
  {tempdir}/data/a.1 -> {tempdir}/work/a.1
None -> {tempdir}/data/a.1
  ['{tempdir}/data/a.1'] -> {tempdir}/work/a.bak
    ['{tempdir}/work/a.1', '{tempdir}/work/a.bak'] -> {tempdir}/data/a.a.2
      {tempdir}/data/a.a.2 -> {tempdir}/work/a.a.3
None -> {tempdir}/data/a.1
  {tempdir}/data/a.1 -> {tempdir}/work/a.1
None -> {tempdir}/data/a.1
  ['{tempdir}/data/a.1'] -> {tempdir}/work/a.bak
    ['{tempdir}/work/a.1', '{tempdir}/work/a.bak'] -> {tempdir}/data/a.b.2
      {tempdir}/data/a.b.2 -> {tempdir}/work/a.b.3
None -> {tempdir}/data/b.1
  {tempdir}/data/b.1 -> {tempdir}/work/b.1
None -> {tempdir}/data/b.1
  ['{tempdir}/data/b.1'] -> {tempdir}/work/b.bak
    ['{tempdir}/work/b.1', '{tempdir}/work/b.bak'] -> {tempdir}/data/b.a.2
      {tempdir}/data/b.a.2 -> {tempdir}/work/b.a.3
None -> {tempdir}/data/b.1
  {tempdir}/data/b.1 -> {tempdir}/work/b.1
None -> {tempdir}/data/b.1
  ['{tempdir}/data/b.1'] -> {tempdir}/work/b.bak
    ['{tempdir}/work/b.1', '{tempdir}/work/b.bak'] -> {tempdir}/data/b.b.2
      {tempdir}/data/b.b.2 -> {tempdir}/work/b.b.3
None -> {tempdir}/data/c.1
  {tempdir}/data/c.1 -> {tempdir}/work/c.1
None -> {tempdir}/data/c.1
  ['{tempdir}/data/c.1'] -> {tempdir}/work/c.bak
    ['{tempdir}/work/c.1', '{tempdir}/work/c.bak'] -> {tempdir}/data/c.a.2
      {tempdir}/data/c.a.2 -> {tempdir}/work/c.a.3
None -> {tempdir}/data/c.1
  {tempdir}/data/c.1 -> {tempdir}/work/c.1
None -> {tempdir}/data/c.1
  ['{tempdir}/data/c.1'] -> {tempdir}/work/c.bak
    ['{tempdir}/work/c.1', '{tempdir}/work/c.bak'] -> {tempdir}/data/c.b.2
      {tempdir}/data/c.b.2 -> {tempdir}/work/c.b.3
None -> {tempdir}/data/d.1
  {tempdir}/data/d.1 -> {tempdir}/work/d.1
None -> {tempdir}/data/d.1
  ['{tempdir}/data/d.1'] -> {tempdir}/work/d.bak
    ['{tempdir}/work/d.1', '{tempdir}/work/d.bak'] -> {tempdir}/data/d.a.2
      {tempdir}/data/d.a.2 -> {tempdir}/work/d.a.3
None -> {tempdir}/data/d.1
  {tempdir}/data/d.1 -> {tempdir}/work/d.1
None -> {tempdir}/data/d.1
  ['{tempdir}/data/d.1'] -> {tempdir}/work/d.bak
    ['{tempdir}/work/d.1', '{tempdir}/work/d.bak'] -> {tempdir}/data/d.b.2
      {tempdir}/data/d.b.2 -> {tempdir}/work/d.b.3
        ['{tempdir}/work/a.a.3', '{tempdir}/work/a.b.3', '{tempdir}/work/b.a.3', '{tempdir}/work/b.b.3', '{tempdir}/work/c.a.3', '{tempdir}/work/c.b.3', '{tempdir}/work/d.a.3', '{tempdir}/work/d.b.3'] -> {tempdir}/data/summary.5
""".format(tempdir=tempdir)


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

    def test_ruffus(self):
        pipeline_run(multiprocess=50, verbose=0, pipeline="main")

        with open(os.path.join(data_dir, "summary.5")) as ii:
            active_text = ii.read()
        if active_text != expected_active_text:
            raise Exception("Error:\n\tExpected\n%s\nInstead\n%s\n" %
                            (expected_active_text, active_text))

    def test_newstyle_ruffus(self):
        # alternative syntax
        test_pipeline = Pipeline("test")

        test_pipeline.mkdir(data_dir, work_dir)
        test_pipeline.originate(task_func=task1,
                                output=[os.path.join(data_dir, "%s.1" % aa) for aa in "abcd"])

        test_pipeline.mkdir(filter=suffix(".1"),
                            output=".dir",
                            output_dir=work_dir)

        test_pipeline.transform(task_func=task2,
                                input=task1,
                                filter=suffix(".1"),
                                output=[".1", ".bak"],
                                extras=["extra.tst", 4, r"orig_dir=\1"],
                                output_dir=work_dir)

        test_pipeline.subdivide(task3, task2, suffix(
            ".1"), r"\1.*.2", [r"\1.a.2", r"\1.b.2"], output_dir=data_dir)
        test_pipeline.transform(task4, task3, suffix(
            ".2"), ".3", output_dir=work_dir)
        test_pipeline.merge(task5, task4, os.path.join(data_dir, "summary.5"))
        test_pipeline.run(multiprocess=50, verbose=0)

        with open(os.path.join(data_dir, "summary.5")) as ii:
            active_text = ii.read()
        if active_text != expected_active_text:
            raise Exception("Error:\n\tExpected\n%s\nInstead\n%s\n" %
                            (expected_active_text, active_text))


if __name__ == '__main__':
    unittest.main()
