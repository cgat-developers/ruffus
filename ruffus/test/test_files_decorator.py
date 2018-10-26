#!/usr/bin/env python
from __future__ import print_function
import unittest
import json
from ruffus import transform, follows, pipeline_run, Pipeline, regex, mkdir, files
import sys

"""

    test_files_decorator.py

        test @files which take single files forwards arguments as single files rather
        than as lists

"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# from ruffus.file_name_parameters import


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

# use simplejson in place of json for python < 2.6
# try:
# except ImportError:
#    import simplejson
#    json = simplejson

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

def check_job_io(infiles, outfiles, extra_params):
    """
    cat input files content to output files
        after writing out job parameters
    """
    # dump parameters
    params = (infiles, outfiles) + extra_params

    if isinstance(infiles, str):
        infile_names = [infiles]
    elif infiles is None:
        infile_names = []
    else:
        infile_names = infiles

    if isinstance(outfiles, str):
        outfile_names = [outfiles]
    else:
        outfile_names = outfiles

    output_text = list()
    for f in infile_names:
        with open(f) as ii:
            output_text.append(ii.read())
    output_text = "".join(sorted(output_text))
    output_text += json.dumps(infiles) + " -> " + json.dumps(outfiles) + "\n"
    for f in outfile_names:
        with open(f, "w") as oo:
            oo.write(output_text)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

@follows(mkdir(tempdir))
#
#    task1
#
@files(None, tempdir + 'a.1')
def task1(infiles, outfiles, *extra_params):
    """
    First task
    """
    check_job_io(infiles, outfiles, extra_params)


#
#    task2
#
@transform(task1, regex(r".+"), tempdir + 'b.1')
def task2(infiles, outfiles, *extra_params):
    """
    Second task
    """
    check_job_io(infiles, outfiles, extra_params)
    assert(infiles == tempdir + "a.1")


#
#    task3
#
@files(task2, tempdir + 'c.1')
def task3(infiles, outfiles, *extra_params):
    """
    Second task
    """
    check_job_io(infiles, outfiles, extra_params)
    assert(infiles == tempdir + "b.1")

#
#    task4
#


@follows(task3)
@files([[None, tempdir + 'd.1'], [None, tempdir + 'e.1']])
def task4(infiles, outfiles, *extra_params):
    """
    Second task
    """
    check_job_io(infiles, outfiles, extra_params)

#
#    task5
#


@files(task4, tempdir + "f.1")
def task5(infiles, outfiles, *extra_params):
    """
    Second task
    """
    check_job_io(infiles, outfiles, extra_params)
    assert(infiles == [tempdir + "d.1", tempdir + "e.1"])


class Test_task(unittest.TestCase):

    def tearDown(self):
        """
        """
        import glob
        for f in glob.glob(tempdir + "*"):
            os.unlink(f)
        os.rmdir(tempdir)

    def test_task(self):
        pipeline_run(multiprocess=10, verbose=0, pipeline="main")

    def test_newstyle_task(self):
        """
        Same as above but construct a new pipeline on the fly without decorators
        """
        test_pipeline = Pipeline("test")
        test_pipeline.files(task1, None, tempdir + 'a.1')\
            .follows(mkdir(tempdir))
        test_pipeline.transform(task_func=task2,
                                input=task1,
                                filter=regex(r".+"),
                                output=tempdir + 'b.1')
        test_pipeline.files(task3, task2, tempdir + 'c.1')
        test_pipeline.files(task4, [[None, tempdir + 'd.1'], [None, tempdir + 'e.1']])\
            .follows(task3)
        test_pipeline.files(task5, task4, tempdir + "f.1")
        test_pipeline.run(multiprocess=10, verbose=0)


if __name__ == '__main__':
    unittest.main()
