#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
from ruffus import posttask, split, merge, transform, pipeline_printout, pipeline_run, Pipeline, suffix

"""

    test_split_and_combine.py

        test branching dependencies

"""


import sys
import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"
verbose_output = sys.stderr


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


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    split_fasta_file
#
@posttask(lambda: verbose_output.write("    Split into %d files\n" % 10))
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
    for i in range(10):
        with open(tempdir + "files.split.%03d.fa" % i, "w") as oo:
            pass

    with open(success_flag,  "w") as oo:
        pass


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    align_sequences
#
@posttask(lambda: verbose_output.write("    Sequences aligned\n"))
# fa -> aln
@transform(split_fasta_file, suffix(".fa"), ".aln")
def align_sequences(input_file, output_filename):
    with open(output_filename, "w") as oo:
        oo.write("%s\n" % output_filename)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    percentage_identity
#
@posttask(lambda: verbose_output.write("    %Identity calculated\n"))
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
@posttask(lambda: verbose_output.write("    Results recombined\n"))
@merge(percentage_identity, [tempdir + "all.combine_results",
                             tempdir + "all.combine_results_success"])
def combine_results(input_files, output_files):
    """
    Combine all
    """
    (output_filename, success_flag_filename) = output_files
    with open(output_filename, "w") as out:
        for inp, flag in input_files:
            with open(inp) as ii:
                out.write(ii.read())
    with open(success_flag_filename, "w") as oo:
        pass


class Test_ruffus(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass
        os.makedirs(tempdir)
        open(tempdir + "original.fa", "w").close()

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
            pass
        except:
            pass

    def test_ruffus(self):
        pipeline_run(multiprocess=50, verbose=0, pipeline="main")
        if not os.path.exists(tempdir + "all.combine_results"):
            raise Exception("Missing %s" % (tempdir + "all.combine_results"))

    def test_newstyle_ruffus(self):

        test_pipeline = Pipeline("test")

        test_pipeline.split(task_func=split_fasta_file,
                            input=tempdir + "original.fa",
                            output=[tempdir + "files.split.success",
                                    tempdir + "files.split.*.fa"])\
            .posttask(lambda: verbose_output.write("    Split into %d files\n" % 10))

        test_pipeline.transform(task_func=align_sequences,
                                input=split_fasta_file,
                                filter=suffix(".fa"),
                                output=".aln"                     # fa -> aln
                                )\
            .posttask(lambda: verbose_output.write("    Sequences aligned\n"))

        test_pipeline.transform(task_func=percentage_identity,
                                input=align_sequences,      # find all results from align_sequences
                                # replace suffix with:
                                filter=suffix(".aln"),
                                output=[r".pcid",  # .pcid suffix for the result
                                        r".pcid_success"]  # .pcid_success to indicate job completed
                                )\
            .posttask(lambda: verbose_output.write("    %Identity calculated\n"))

        test_pipeline.merge(task_func=combine_results,
                            input=percentage_identity,
                            output=[tempdir + "all.combine_results",
                                    tempdir + "all.combine_results_success"])\
            .posttask(lambda: verbose_output.write("    Results recombined\n"))

        test_pipeline.run(multiprocess=50, verbose=0)
        if not os.path.exists(tempdir + "all.combine_results"):
            raise Exception("Missing %s" % (tempdir + "all.combine_results"))


if __name__ == '__main__':
    unittest.main()
