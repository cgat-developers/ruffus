#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
from ruffus import *
import sys

"""

    test_files_post_merge.py

        bug where @files follows merge and extra parenthesis inserted

"""
import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"
test_file = tempdir + "test_output"
jobs_per_task = 50


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

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    split_fasta_file
#

def do_write(file_name, what):
    with open(file_name, "a") as oo:
        oo.write(what)


test_file = tempdir + "task.done"


@posttask(lambda: do_write(test_file, "Split into %d files\n" % jobs_per_task))
@split(tempdir + "original.fa", [tempdir + "files.split.success", tempdir + "files.split.*.fa"])
def split_fasta_file(input_file, outputs):

    #
    # remove previous fasta files
    #
    success_flag = outputs[0]
    output_file_names = outputs[1:]
    for f in output_file_names:
        os.unlink(f)

    #
    # create as many files as we are simulating in jobs_per_task
    #
    for i in range(jobs_per_task):
        with open(tempdir + "files.split.%03d.fa" % i, "w") as oo:
            pass

    with open(success_flag,  "w") as oo:
        pass


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    align_sequences
#
@posttask(lambda: do_write(test_file, "Sequences aligned\n"))
# fa -> aln
@transform(split_fasta_file, suffix(".fa"), ".aln")
def align_sequences(input_file, output_filename):
    with open(output_filename, "w") as oo:
        oo.write("%s\n" % output_filename)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    percentage_identity
#
@posttask(lambda: do_write(test_file, "%Identity calculated\n"))
@transform(align_sequences,             # find all results from align_sequences
           suffix(".aln"),             # replace suffix with:
           [r".pcid",  # .pcid suffix for the result
            r".pcid_success"])  # .pcid_success to indicate job completed
def percentage_identity(input_file, output_files):
    (output_filename, success_flag_filename) = output_files
    with open(output_filename, "w") as oo:
        oo.write("%s\n" % output_filename)
    with open(success_flag_filename, "w") as oo:
        pass


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    combine_results
#
@posttask(lambda: do_write(test_file, "Results recombined\n"))
@merge(percentage_identity, tempdir + "all.combine_results")
def combine_results(input_files, output_files):
    """
    Combine all
    """
    (output_filename) = output_files
    with open(output_filename, "w") as oo:
        for inp, flag in input_files:
            with open(inp) as ii:
                oo.write(ii.read())


@files(combine_results, os.path.join(tempdir, "check_all_is.well"))
def post_merge_check(input_filename, output_filename):
    """
    check that merge sends just one file, not a list to me
    """
    with open(output_filename, "w") as oo:
        with open(input_filename) as ii:
            oo.write(ii.read())


@files(post_merge_check, os.path.join(tempdir, "check_all_is.weller"))
def post_post_merge_check(input_filename, output_filename):
    """
    check that @files forwards a single file on when given a single file
    """
    with open(output_filename, "w") as oo:
        with open(input_filename) as ii:
            oo.write(ii.read())


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
        os.makedirs(tempdir)
        open(tempdir + "original.fa", "w").close()
        self.expected_text = """Split into %d files
Sequences aligned
%%Identity calculated
Results recombined
""" % jobs_per_task

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_ruffus(self):
        pipeline_run(multiprocess=50, verbose=0, pipeline="main")
        with open(test_file) as ii:
            post_task_text = ii.read()
        self.assertEqual(post_task_text, self.expected_text)

    def test_newstyle_ruffus(self):

        test_pipeline = Pipeline("test")

        test_pipeline.split(task_func=split_fasta_file,
                            input=tempdir + "original.fa",
                            output=[tempdir + "files.split.success",
                                    tempdir + "files.split.*.fa"])\
            .posttask(lambda: do_write(test_file, "Split into %d files\n" % jobs_per_task))

        test_pipeline.transform(task_func=align_sequences,
                                input=split_fasta_file,
                                filter=suffix(".fa"),
                                output=".aln"                     # fa -> aln
                                )\
            .posttask(lambda: do_write(test_file, "Sequences aligned\n"))

        test_pipeline.transform(task_func=percentage_identity,
                                input=align_sequences,             # find all results from align_sequences
                                # replace suffix with:
                                filter=suffix(".aln"),
                                output=[r".pcid",  # .pcid suffix for the result
                                        r".pcid_success"]  # .pcid_success to indicate job completed
                                )\
            .posttask(lambda: do_write(test_file, "%Identity calculated\n"))

        test_pipeline.merge(task_func=combine_results,
                            input=percentage_identity,
                            output=tempdir + "all.combine_results")\
            .posttask(lambda: do_write(test_file, "Results recombined\n"))

        test_pipeline.files(post_merge_check, combine_results,
                            os.path.join(tempdir, "check_all_is.well"))

        test_pipeline.files(post_post_merge_check, post_merge_check, os.path.join(
            tempdir, "check_all_is.weller"))

        test_pipeline.run(multiprocess=50, verbose=0)
        with open(test_file) as ii:
            post_task_text = ii.read()
        self.assertEqual(post_task_text, self.expected_text)


if __name__ == '__main__':
    unittest.main()
