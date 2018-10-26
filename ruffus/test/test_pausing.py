#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
import json
from collections import defaultdict
import re
from ruffus import *
import sys

"""

    test_pausing.py

        test time.sleep keeping input files and output file times correct

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


# use simplejson in place of json for python < 2.6
# try:
#    import json
# except ImportError:
#    import simplejson
#    json = simplejson

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


def check_job_io(infiles, outfiles, extra_params):
    """
    cat input files content to output files
        after writing out job parameters
    """
    # dump parameters
    params = (infiles, outfiles) + extra_params

    if isinstance(infiles, str):
        infiles = [infiles]
    elif infiles is None:
        infiles = []
    if isinstance(outfiles, str):
        outfiles = [outfiles]
    output_text = list()
    for f in infiles:
        with open(f) as ii:
            output_text.append(ii.read())
    output_text = "".join(sorted(output_text))
    output_text += json.dumps(infiles) + " -> " + json.dumps(outfiles) + "\n"
    for f in outfiles:
        with open(f, "w") as ff:
            ff.write(output_text)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#   1   ->  2   ->  3   ->
#       ->  4           ->
#                   5   ->    6
#

def do_write(file_name, what):
    with open(file_name, "a") as oo:
        oo.write(what)


test_file = tempdir + "task.done"
#
#    task1
#


@files(None, [tempdir + d for d in ('a.1', 'b.1', 'c.1')])
@follows(mkdir(tempdir))
@posttask(lambda: do_write(test_file, "Task 1 Done\n"))
def task1(infiles, outfiles, *extra_params):
    """
    First task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    check_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))


#
#    task2
#
@posttask(lambda: do_write(test_file, "Task 2 Done\n"))
@follows(task1)
@transform(tempdir + "*.1", suffix(".1"), ".2")
def task2(infiles, outfiles, *extra_params):
    """
    Second task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    check_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))


#
#    task3
#
@transform(task2, regex('(.*).2'), inputs([r"\1.2", tempdir + "a.1"]), r'\1.3')
@posttask(lambda: do_write(test_file, "Task 3 Done\n"))
def task3(infiles, outfiles, *extra_params):
    """
    Third task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    check_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))


#
#    task4
#
@transform(tempdir + "*.1", suffix(".1"), ".4")
@follows(task1)
@posttask(lambda: do_write(test_file, "Task 4 Done\n"))
def task4(infiles, outfiles, *extra_params):
    """
    Fourth task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    check_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))

#
#    task5
#


@files(None, tempdir + 'a.5')
@follows(mkdir(tempdir))
@posttask(lambda: do_write(test_file, "Task 5 Done\n"))
def task5(infiles, outfiles, *extra_params):
    """
    Fifth task is extra slow
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    check_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))

#
#    task6
#
# @files([[[tempdir + d for d in 'a.3', 'b.3', 'c.3', 'a.4', 'b.4', 'c.4', 'a.5'], tempdir + 'final.6']])


@merge([task3, task4, task5], tempdir + "final.6")
@follows(task3, task4, task5, )
@posttask(lambda: do_write(test_file, "Task 6 Done\n"))
def task6(infiles, outfiles, *extra_params):
    """
    final task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    check_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))


def check_job_order_correct(filename):
    """
       1   ->  2   ->  3   ->
           ->  4           ->
                       5   ->    6
    """

    precedence_rules = [[1, 2],
                        [2, 3],
                        [1, 4],
                        [5, 6],
                        [3, 6],
                        [4, 6]]

    index_re = re.compile(r'.*\.([0-9])["\]\n]*$')
    job_indices = defaultdict(list)
    with open(filename) as ii:
        for linenum, l in enumerate(ii):
            m = index_re.search(l)
            if not m:
                raise "Non-matching line in [%s]" % filename
            job_indices[int(m.group(1))].append(linenum)

    for job_index in job_indices:
        job_indices[job_index].sort()

    for before, after in precedence_rules:
        if job_indices[before][-1] >= job_indices[after][0]:
            raise "Precedence violated for job %d [line %d] and job %d [line %d] of [%s]"


def check_final_output_correct():
    """
    check if the final output in final.6 is as expected
    """
    expected_output = \
        """        ["DIR/a.1"] -> ["DIR/a.2"]
        ["DIR/a.1"] -> ["DIR/a.4"]
        ["DIR/a.2", "DIR/a.1"] -> ["DIR/a.3"]
        ["DIR/a.3", "DIR/b.3", "DIR/c.3", "DIR/a.4", "DIR/b.4", "DIR/c.4", "DIR/a.5"] -> ["DIR/final.6"]
        ["DIR/b.1"] -> ["DIR/b.2"]
        ["DIR/b.1"] -> ["DIR/b.4"]
        ["DIR/b.2", "DIR/a.1"] -> ["DIR/b.3"]
        ["DIR/c.1"] -> ["DIR/c.2"]
        ["DIR/c.1"] -> ["DIR/c.4"]
        ["DIR/c.2", "DIR/a.1"] -> ["DIR/c.3"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.5"]"""
    expected_output = expected_output.replace(
        "        ", "").replace("DIR/", tempdir).split("\n")
    with open(tempdir + "final.6", "r") as ii:
        final_6_contents = sorted([l.rstrip() for l in ii.readlines()])
    if final_6_contents != expected_output:
        for i, (l1, l2) in enumerate(zip(final_6_contents, expected_output)):
            if l1 != l2:
                sys.stderr.write("%d\n  >%s<\n  >%s<\n" % (i, l1, l2))
        raise Exception("Final.6 output is not as expected\n")


try:
    from StringIO import StringIO
except:
    from io import StringIO


class Test_ruffus(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_ruffus(self):
        pipeline_run(multiprocess=50, verbose=0, pipeline="main")
        check_final_output_correct()
        check_job_order_correct(tempdir + "jobs.start")
        check_job_order_correct(tempdir + "jobs.finish")

    def test_newstyle_ruffus(self):
        test_pipeline = Pipeline("test")

        test_pipeline.files(task1,
                            None,
                            [tempdir + d for d in ('a.1', 'b.1', 'c.1')])\
            .follows(mkdir(tempdir))\
            .posttask(lambda: do_write(test_file, "Task 1 Done\n"))

        test_pipeline.transform(task2, tempdir + "*.1", suffix(".1"), ".2")\
            .posttask(lambda: do_write(test_file, "Task 2 Done\n"))\
            .follows(task1)

        test_pipeline.transform(task3, task2, regex('(.*).2'), inputs([r"\1.2", tempdir + "a.1"]), r'\1.3')\
            .posttask(lambda: do_write(test_file, "Task 3 Done\n"))

        test_pipeline.transform(task_func=task4,
                                input=tempdir + "*.1",
                                filter=suffix(".1"),
                                output=".4")\
            .follows(task1)\
            .posttask(lambda: do_write(test_file, "Task 4 Done\n"))

        test_pipeline.files(task5, None, tempdir + 'a.5')\
            .follows(mkdir(tempdir))\
            .posttask(lambda: do_write(test_file, "Task 5 Done\n"))

        test_pipeline.merge(task_func=task6,
                            input=[task3, task4, task5],
                            output=tempdir + "final.6")\
            .follows(task3, task4, task5, )\
            .posttask(lambda: do_write(test_file, "Task 6 Done\n"))

        test_pipeline.run(multiprocess=50, verbose=0)
        check_final_output_correct()
        check_job_order_correct(tempdir + "jobs.start")
        check_job_order_correct(tempdir + "jobs.finish")


if __name__ == '__main__':
    unittest.main()
