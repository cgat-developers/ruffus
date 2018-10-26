#!/usr/bin/env python
from __future__ import print_function
import json
from collections import defaultdict
import re
import time
import shutil
import unittest
from ruffus import pipeline_run, pipeline_printout, Pipeline, transform, follows, posttask, merge, \
    mkdir, suffix, originate, regex, inputs, jobs_limit, files
import sys

"""

    branching.py

        test branching dependencies

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


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

try:
    from StringIO import StringIO
except:
    from io import StringIO

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
        with open(f, "w") as oo:
            oo.write(output_text)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


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


@originate([tempdir + d for d in ('a.1', 'b.1', 'c.1')])
@follows(mkdir(tempdir))
@posttask(lambda: do_write(test_file, "Task 1 Done\n"))
def task1(outfile, *extra_params):
    """
    First task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([None, outfile]))
    check_job_io(None, outfile, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([None, outfile]))


#
#    task2
#
@posttask(lambda: do_write(test_file, "Task 2 Done\n"))
@transform(task1, suffix(".1"), ".2")
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
@jobs_limit(1)
@transform(tempdir + "*.1", suffix(".1"), ".4")
@follows(task1)
@posttask(lambda: do_write(test_file, "Task 4 Done\n"))
def task4(infiles, outfiles, *extra_params):
    """
    Fourth task is extra slow
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    time.sleep(0.1)
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
    time.sleep(1)
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


#
#   Use equivalent but new sytle syntax
#
test_pipeline = Pipeline("test")

test_pipeline.originate(task_func=task1,
                        output=[tempdir + d for d in ('a.1', 'b.1', 'c.1')])\
    .follows(mkdir(tempdir))\
    .posttask(lambda: do_write(test_file, "Task 1 Done\n"))

test_pipeline.transform(task_func=task2,
                        input=task1,
                        filter=suffix(".1"),
                        output=".2") \
    .posttask(lambda: do_write(test_file, "Task 2 Done\n"))

test_pipeline.transform(task3, task2, regex('(.*).2'), inputs([r"\1.2", tempdir + "a.1"]), r'\1.3')\
    .posttask(lambda: do_write(test_file, "Task 3 Done\n"))


test_pipeline.transform(task4, tempdir + "*.1", suffix(".1"), ".4")\
    .follows(task1)\
    .posttask(lambda: do_write(test_file, "Task 4 Done\n"))\
    .jobs_limit(1)

test_pipeline.files(task5, None, tempdir + 'a.5')\
    .follows(mkdir(tempdir))\
    .posttask(lambda: do_write(test_file, "Task 5 Done\n"))

test_pipeline.merge(task_func=task6,
                    input=[task3, task4, task5],
                    output=tempdir + "final.6")\
    .follows(task3, task4, task5, ) \
    .posttask(lambda: do_write(test_file, "Task 6 Done\n"))


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
        if before not in job_indices or after not in job_indices:
            continue
        if job_indices[before][-1] >= job_indices[after][0]:
            raise Exception("Precedence violated for job %d [line %d] and job %d [line %d] of [%s]"
                            % (before, job_indices[before][-1],
                               after,  job_indices[after][0],
                               filename))


def check_final_output_correct(after_touch_files=False):
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
        [] -> ["DIR/a.1"]
        [] -> ["DIR/a.1"]
        [] -> ["DIR/a.1"]
        [] -> ["DIR/a.1"]
        [] -> ["DIR/a.1"]
        [] -> ["DIR/a.5"]
        [] -> ["DIR/b.1"]
        [] -> ["DIR/b.1"]
        [] -> ["DIR/c.1"]
        [] -> ["DIR/c.1"]"""

    expected_output = expected_output.replace(
        "        ", "").replace("DIR/", tempdir).split("\n")
    orig_expected_output = expected_output
    if after_touch_files:
        expected_output.pop(-3)
    with open(tempdir + "final.6", "r") as ii:
        final_6_contents = sorted([l.rstrip() for l in ii.readlines()])
    if final_6_contents != expected_output:
        print("Actual:", file=sys.stderr)
        for ll in final_6_contents:
            print(ll, file=sys.stderr)
        print("_" * 80, file=sys.stderr)
        print("Expected:", file=sys.stderr)
        for ll in orig_expected_output:
            print(ll, file=sys.stderr)
        print("_" * 80, file=sys.stderr)
        for i, (l1, l2) in enumerate(zip(final_6_contents, expected_output)):
            if l1 != l2:
                sys.stderr.write(
                    "%d\nActual:\n  >%s<\nExpected:\n  >%s<\n" % (i, l1, l2))
        raise Exception("Final.6 output is not as expected\n")


class Test_ruffus(unittest.TestCase):

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass
        os.makedirs(tempdir)

    def test_ruffus(self):
        print("\n\n     Run pipeline normally...")
        pipeline_run(multiprocess=10, verbose=0, pipeline="main")
        check_final_output_correct()
        check_job_order_correct(tempdir + "jobs.start")
        check_job_order_correct(tempdir + "jobs.finish")
        print("     OK")

        print("\n\n     Touch task2 only:")
        os.unlink(os.path.join(tempdir, "jobs.start"))
        os.unlink(os.path.join(tempdir, "jobs.finish"))
        print("       First delete b.1 for task2...")
        os.unlink(os.path.join(tempdir, "b.1"))
        print("       Then run with touch_file_only...")
        pipeline_run([task2], multiprocess=10,
                     touch_files_only=True, verbose=0, pipeline="main")

        # check touching has made task2 up to date
        s = StringIO()
        pipeline_printout(s, [task2], verbose=4,
                          wrap_width=10000, pipeline="main")
        output_str = s.getvalue()
        #print (">>>\n", output_str, "<<<\n", file=sys.stderr)
        if "b.1" in output_str:
            raise Exception("Expected b.1 created by touching...")
        if "b.2" in output_str:
            raise Exception("Expected b.2 created by touching...")
        print("     Touching has made task2 up to date...\n")

        print("     Then run normally again...")
        pipeline_run(multiprocess=10, verbose=0, pipeline="main")
        check_final_output_correct(True)
        check_job_order_correct(tempdir + "jobs.start")
        check_job_order_correct(tempdir + "jobs.finish")

    def test_ruffus_new_syntax(self):
        print("\n\n     Run pipeline normally...")
        test_pipeline.run(multiprocess=10, verbose=0)
        check_final_output_correct()
        check_job_order_correct(tempdir + "jobs.start")
        check_job_order_correct(tempdir + "jobs.finish")
        print("     OK")

        print("\n\n     Touch task2 only:")
        os.unlink(os.path.join(tempdir, "jobs.start"))
        os.unlink(os.path.join(tempdir, "jobs.finish"))
        print("       First delete b.1 for task2...")
        os.unlink(os.path.join(tempdir, "b.1"))
        print("       Then run with touch_file_only...")
        test_pipeline.run([task2], multiprocess=10,
                          touch_files_only=True, verbose=0)

        # check touching has made task2 up to date
        s = StringIO()
        test_pipeline.printout(s, [task2], verbose=4, wrap_width=10000)
        output_str = s.getvalue()
        #print (">>>\n", output_str, "<<<\n", file=sys.stderr)
        if "b.1" in output_str:
            raise Exception("Expected b.1 created by touching...")
        if "b.2" in output_str:
            raise Exception("Expected b.2 created by touching...")
        print("     Touching has made task2 up to date...\n")

        print("     Then run normally again...")
        test_pipeline.run(multiprocess=10, verbose=0)
        check_final_output_correct(True)
        check_job_order_correct(tempdir + "jobs.start")
        check_job_order_correct(tempdir + "jobs.finish")


if __name__ == '__main__':
    unittest.main()
