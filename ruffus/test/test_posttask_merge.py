#!/usr/bin/env python
from __future__ import print_function
"""

    test_files_post_merge.py

        bug where @files follows merge and extra parenthesis inserted

        use :
            --debug               to test automatically
            --start_again         the first time you run the file
            --jobs_per_task N     to simulate tasks with N numbers of files per task

            -j N / --jobs N       to speify multitasking
            -v                    to see the jobs in action
            -n / --just_print     to see what jobs would run

"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys, os
import os.path
try:
    import StringIO as io
except:
    import io as io

import re,time

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__



import ruffus
parser = OptionParser(version="%%prog v1.0, ruffus v%s" % ruffus.ruffus_version.__version)
parser.add_option("-D", "--debug", dest="debug",
                    action="store_true", default=False,
                    help="Make sure output is correct and clean up.")
parser.add_option("-s", "--start_again", dest="start_again",
                    action="store_true", default=False,
                    help="Make a new 'original.fa' file to simulate having to restart "
                            "pipeline from scratch.")
parser.add_option("--jobs_per_task", dest="jobs_per_task",
                      default=3,
                      metavar="N",
                      type="int",
                      help="Simulates tasks with N numbers of files per task.")


parser.add_option("-t", "--target_tasks", dest="target_tasks",
                  action="append",
                  default = list(),
                  metavar="JOBNAME",
                  type="string",
                  help="Target task(s) of pipeline.")
parser.add_option("-f", "--forced_tasks", dest="forced_tasks",
                  action="append",
                  default = list(),
                  metavar="JOBNAME",
                  type="string",
                  help="Pipeline task(s) which will be included even if they are up to date.")
parser.add_option("-j", "--jobs", dest="jobs",
                  default=1,
                  metavar="jobs",
                  type="int",
                  help="Specifies  the number of jobs (commands) to run simultaneously.")
parser.add_option("-v", "--verbose", dest = "verbose",
                  action="count", default=0,
                  help="Print more verbose messages for each additional verbose level.")
parser.add_option("-d", "--dependency", dest="dependency_file",
                  #default="simple.svg",
                  metavar="FILE",
                  type="string",
                  help="Print a dependency graph of the pipeline that would be executed "
                        "to FILE, but do not execute it.")
parser.add_option("-F", "--dependency_graph_format", dest="dependency_graph_format",
                  metavar="FORMAT",
                  type="string",
                  default = 'svg',
                  help="format of dependency graph file. Can be 'ps' (PostScript), "+
                  "'svg' 'svgz' (Structured Vector Graphics), " +
                  "'png' 'gif' (bitmap  graphics) etc ")
parser.add_option("-n", "--just_print", dest="just_print",
                    action="store_true", default=False,
                    help="Print a description of the jobs that would be executed, "
                        "but do not execute them.")
parser.add_option("-M", "--minimal_rebuild_mode", dest="minimal_rebuild_mode",
                    action="store_true", default=False,
                    help="Rebuild a minimum of tasks necessary for the target. "
                    "Ignore upstream out of date tasks if intervening tasks are fine.")
parser.add_option("-K", "--no_key_legend_in_graph", dest="no_key_legend_in_graph",
                    action="store_true", default=False,
                    help="Do not print out legend and key for dependency graph.")
parser.add_option("-H", "--draw_graph_horizontally", dest="draw_horizontally",
                    action="store_true", default=False,
                    help="Draw horizontal dependency graph.")

parameters = [
                ]







#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


import re
import operator
import sys,os
from collections import defaultdict
import random

sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888





# get help string
f =io.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
(options, remaining_args) = parser.parse_args()


tempdir = "temp_filesre_split_and_combine/"
test_file = tempdir  + "test_output"


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    split_fasta_file
#

def do_write(file_name, what):
    with open(file_name, "a") as oo:
        oo.write(what)
test_file = tempdir + "task.done"



@posttask(lambda: do_write(test_file, "Split into %d files\n" % options.jobs_per_task))
@split(tempdir  + "original.fa", [tempdir  + "files.split.success", tempdir + "files.split.*.fa"])
def split_fasta_file (input_file, outputs):

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
    for i in range(options.jobs_per_task):
        with open(tempdir + "files.split.%03d.fa" % i, "w") as oo:
            pass

    with open(success_flag,  "w") as oo:
        pass


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    align_sequences
#
@posttask(lambda: do_write(test_file, "Sequences aligned\n"))
@transform(split_fasta_file, suffix(".fa"), ".aln")                     # fa -> aln
def align_sequences (input_file, output_filename):
    with open(output_filename, "w") as oo:
        oo.write("%s\n" % output_filename)



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    percentage_identity
#
@posttask(lambda: do_write(test_file, "%Identity calculated\n"))
@transform(align_sequences,             # find all results from align_sequences
            suffix(".aln"),             # replace suffix with:
            [r".pcid",                  #   .pcid suffix for the result
             r".pcid_success"])         #   .pcid_success to indicate job completed
def percentage_identity (input_file, output_files):
    (output_filename, success_flag_filename) = output_files
    with open(output_filename, "w") as oo:
        oo.write("%s\n" % output_filename)
    with open(success_flag_filename, "w") as oo:
        pass



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    combine_results
#
@posttask(lambda: do_write(test_file, "Results recombined\n"))
@merge(percentage_identity, tempdir + "all.combine_results")
def combine_results (input_files, output_files):
    """
    Combine all
    """
    (output_filename) = output_files
    with open(output_filename, "w") as oo:
        for inp, flag in input_files:
            with open(inp) as ii:
                oo.write(ii.read())



@files(combine_results, os.path.join(tempdir, "check_all_is.well"))
def post_merge_check (input_filename, output_filename):
    """
    check that merge sends just one file, not a list to me
    """
    with open(output_filename, "w") as oo:
        with open(input_filename) as ii:
            oo.write(ii.read())

@files(post_merge_check, os.path.join(tempdir, "check_all_is.weller"))
def post_post_merge_check (input_filename, output_filename):
    """
    check that @files forwards a single file on when given a single file
    """
    with open(output_filename, "w") as oo:
        with open(input_filename) as ii:
            oo.write(ii.read())



import unittest, shutil
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
        self.expected_text = """Split into 3 files
Sequences aligned
%Identity calculated
Results recombined
"""


    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_ruffus (self):
        pipeline_run(multiprocess = 50, verbose = 0)
        with open(test_file) as ii:
            post_task_text =  ii.read()
        self.assertEqual(post_task_text, self.expected_text)



    def test_newstyle_ruffus (self):

        test_pipeline = Pipeline("test")


        test_pipeline.split(    task_func   = split_fasta_file,
                                input       = tempdir  + "original.fa", 
                                output      = [tempdir  + "files.split.success", 
                                               tempdir + "files.split.*.fa"])\
            .posttask(lambda: do_write(test_file, "Split into %d files\n" % options.jobs_per_task))


        test_pipeline.transform(task_func   = align_sequences,
                                input       = split_fasta_file, 
                                filter      = suffix(".fa"), 
                                output      = ".aln"                     # fa -> aln
                                )\
            .posttask(lambda: do_write(test_file, "Sequences aligned\n"))


        test_pipeline.transform(task_func   = percentage_identity,
                                input       = align_sequences,             # find all results from align_sequences
                                filter      = suffix(".aln"),             # replace suffix with:
                                output      = [r".pcid",                  #   .pcid suffix for the result
                                               r".pcid_success"]          #   .pcid_success to indicate job completed
                                )\
            .posttask(lambda: do_write(test_file, "%Identity calculated\n"))


        test_pipeline.merge(task_func   = combine_results, 
                            input       = percentage_identity, 
                            output      = tempdir + "all.combine_results")\
            .posttask(lambda: do_write(test_file, "Results recombined\n"))

        test_pipeline.files(post_merge_check, combine_results, os.path.join(tempdir, "check_all_is.well"))

        test_pipeline.files(post_post_merge_check, post_merge_check, os.path.join(tempdir, "check_all_is.weller"))

        test_pipeline.run(multiprocess = 50, verbose = 0)
        with open(test_file) as ii:
            post_task_text =  ii.read()
        self.assertEqual(post_task_text, self.expected_text)



if __name__ == '__main__':
    unittest.main()

