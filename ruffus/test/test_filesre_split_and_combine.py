#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
import random
from ruffus.combinatorics import *
from ruffus.ruffus_utility import CHECKSUM_FILE_TIMESTAMPS
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus import pipeline_run, pipeline_printout, Pipeline, follows, merge, posttask, \
    split, collate, mkdir, regex, files, files_re, combine
import sys

"""

    branching.py

        test branching dependencies

        use :
            --debug               to test automatically
            --start_again         the first time you run the file
            --jobs_per_task N     to simulate tasks with N numbers of files per task

            -j N / --jobs N       to speify multitasking
            -v                    to see the jobs in action
            -n / --just_print     to see what jobs would run

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

#   constants


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

JOBS_PER_TASK = 50
verbose_output = sys.stderr


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

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    split_fasta_file
#
@posttask(lambda: verbose_output.write("    Split into %d files\n" % JOBS_PER_TASK))
@files(tempdir + "original.fa", tempdir + "files.split.success")
def split_fasta_file(input_file, success_flag):
    #
    # remove existing fasta files
    #
    import glob
    filenames = sorted(glob.glob(tempdir + "files.split.*.fa"))
    for f in filenames:
        os.unlink(f)

    random.seed()
    for i in range(JOBS_PER_TASK):
        with open(tempdir + "files.split.%03d.fa" % i, "w") as oo:
            pass

    with open(success_flag,  "w") as oo:
        pass


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    align_sequences
#
@posttask(lambda: verbose_output.write("    Sequences aligned\n"))
@follows(split_fasta_file)
@files_re(tempdir + "files.split.*.fa",       # find all .fa files
          ".fa$", ".aln")                     # fa -> aln
def align_sequences(input_file, output_filename):
    with open(output_filename, "w") as oo:
        oo.write("%s\n" % output_filename)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    percentage_identity
#
@posttask(lambda: verbose_output.write("    %Identity calculated\n"))
@files_re(align_sequences,                     # find all results from align_sequences
          # match file name root and substitute
          r"(.*\.)(.+).aln$",
          r'\g<0>',  # the original file
          [r"\1\2.pcid",  # .pcid suffix for the result
           r"\1\2.pcid_success"],  # .pcid_success to indicate job completed
          r"\2")  # extra parameter to remember the file index
def percentage_identity(input_file, output_files, split_index):
    (output_filename, success_flag_filename) = output_files
    with open(output_filename, "w") as oo:
        oo.write("%s\n" % split_index)
    with open(success_flag_filename, "w") as oo:
        pass


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    combine_results
#
@posttask(lambda: verbose_output.write("    Results recombined\n"))
@files_re(percentage_identity, combine(r".*.pcid$"),
          [tempdir + "all.combine_results",
           tempdir + "all.combine_results_success"])
def combine_results(input_files, output_files):
    """
    Combine all
    """
    (output_filename, success_flag_filename) = output_files
    out = open(output_filename, "w")
    for inp, flag in input_files:
        with open(inp) as ii:
            out.write(ii.read())
    out.close()
    with open(success_flag_filename, "w") as oo:
        pass


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
        with open(tempdir + "original.fa", "w") as oo:
            pass

    def test_ruffus(self):
        pipeline_run(multiprocess=100, verbose=0, pipeline="main")


if __name__ == '__main__':
    unittest.main()
