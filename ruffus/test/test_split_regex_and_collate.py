#!/usr/bin/env python
from __future__ import print_function
import unittest
import shutil
from ruffus.combinatorics import *
from ruffus.ruffus_utility import RUFFUS_HISTORY_FILE, CHECKSUM_FILE_TIMESTAMPS
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus import pipeline_run, pipeline_printout, Pipeline, suffix, regex, formatter, originate, follows, merge, mkdir, posttask, subdivide, transform, collate, split
import ruffus
import re
import sys
import os

"""

    test_split_regex_and_collate.py

"""
JOBS_PER_TASK = 5

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

#   options


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

try:
    from StringIO import StringIO
except:
    from io import StringIO


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
#   Three starting files
#
original_files = [tempdir + "/original_%d.fa" % d for d in range(3)]


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
@mkdir(tempdir)
@originate(original_files)
def generate_initial_files(out_name):
    with open(out_name, 'w') as outfile:
        pass


#
#    split_fasta_file
#

@posttask(lambda: sys.stderr.write("\tSplit into %d files each\n" % JOBS_PER_TASK))
@subdivide(generate_initial_files,
           # match original files
           regex(r".*\/original_(\d+).fa"),
           [tempdir + r"/files.split.\1.success",                         # flag file for each original file
            tempdir + r"/files.split.\1.*.fa"],                           # glob pattern
           r"\1")                                                        # index of original file
def split_fasta_file(input_file, outputs, original_index):

    #
    # remove previous fasta files
    #
    success_flag = outputs[0]
    output_file_names = outputs[1:]
    for f in output_file_names:
        os.unlink(f)

    #
    # create as many files as we are simulating in JOBS_PER_TASK
    #
    for i in range(JOBS_PER_TASK):
        with open(tempdir + "/files.split.%s.%03d.fa" % (original_index, i), "w") as oo:
            pass

    with open(success_flag,  "w") as oo:
        pass


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    align_sequences
#
@posttask(lambda: sys.stderr.write("\tSequences aligned\n"))
# fa -> aln
@transform(split_fasta_file, suffix(".fa"), ".aln")
def align_sequences(input_file, output_filename):
    with open(output_filename, "w") as oo:
        oo.write("%s\n" % output_filename)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    percentage_identity
#
@posttask(lambda: sys.stderr.write("\t%Identity calculated\n"))
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
@posttask(lambda: sys.stderr.write("\tResults recombined\n"))
@collate(percentage_identity, regex(r".*files.split\.(\d+)\.\d+.pcid"),
         [tempdir + r"/\1.all.combine_results",
          tempdir + r"/\1.all.combine_results_success"])
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
        import os
        try:
            shutil.rmtree(tempdir)
        except:
            pass
        os.makedirs(tempdir)
        for f in original_files:
            with open(f, "w") as p:
                pass

    def cleanup_tmpdir(self):
        os.system('rm -f %s %s' %
                  (os.path.join(tempdir, '*'), RUFFUS_HISTORY_FILE))

    # ___________________________________________________________________________
    #
    #   test product() pipeline_printout and pipeline_run
    # ___________________________________________________________________________
    def test_collate(self):
        self.cleanup_tmpdir()

        s = StringIO()
        pipeline_printout(s, [combine_results], verbose=5,
                          wrap_width=10000, pipeline="main")
        self.assertTrue(re.search(
            'Job needs update:.*Missing files.*', s.getvalue(), re.DOTALL) is not None)
        # print s.getvalue()

        pipeline_run([combine_results], verbose=0, pipeline="main")

    def test_newstyle_collate(self):
        """
        As above but create pipeline on the fly using object orientated syntax rather than decorators
        """

        #
        # Create pipeline on the fly, joining up tasks
        #
        test_pipeline = Pipeline("test")

        test_pipeline.originate(task_func=generate_initial_files,
                                output=original_files)\
            .mkdir(tempdir, tempdir+"/test")

        test_pipeline.subdivide(task_func=split_fasta_file,
                                input=generate_initial_files,
                                # match original files
                                filter=regex(r".*\/original_(\d+).fa"),
                                output=[tempdir + r"/files.split.\1.success",  # flag file for each original file
                                        tempdir + r"/files.split.\1.*.fa"],   # glob pattern
                                extras=[r"\1"])\
            .posttask(lambda: sys.stderr.write("\tSplit into %d files each\n" % JOBS_PER_TASK))

        test_pipeline.transform(task_func=align_sequences,
                                input=split_fasta_file,
                                filter=suffix(".fa"),
                                output=".aln")  \
            .posttask(lambda: sys.stderr.write("\tSequences aligned\n"))

        test_pipeline.transform(task_func=percentage_identity,
                                input=align_sequences,             # find all results from align_sequences
                                # replace suffix with:
                                filter=suffix(".aln"),
                                output=[r".pcid",  # .pcid suffix for the result
                                        r".pcid_success"]  # .pcid_success to indicate job completed
                                )\
            .posttask(lambda: sys.stderr.write("\t%Identity calculated\n"))

        test_pipeline.collate(task_func=combine_results,
                              input=percentage_identity,
                              filter=regex(r".*files.split\.(\d+)\.\d+.pcid"),
                              output=[tempdir + r"/\1.all.combine_results",
                                      tempdir + r"/\1.all.combine_results_success"])\
            .posttask(lambda: sys.stderr.write("\tResults recombined\n"))

        #
        # Cleanup, printout and run
        #
        self.cleanup_tmpdir()
        s = StringIO()
        test_pipeline.printout(s, [combine_results],
                               verbose=5, wrap_width=10000)
        self.assertTrue(re.search(
            'Job needs update:.*Missing files.*', s.getvalue(), re.DOTALL) is not None)
        test_pipeline.run(verbose=0)

    # ___________________________________________________________________________
    #
    #   cleanup
    # ___________________________________________________________________________
    def tearDown(self):
        shutil.rmtree(tempdir)


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    unittest.main()
