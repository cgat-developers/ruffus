#!/usr/bin/env python
"""

    branching.py

"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys, os
import os.path
from StringIO import StringIO
import re,time
import operator
from collections import defaultdict
import random
import shutil

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *
from ruffus import (pipeline_run, pipeline_printout, suffix, transform, split,
                    merge, dbdict, follows)
from ruffus.combinatorics import *
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus.ruffus_utility import (RUFFUS_HISTORY_FILE,
                                   CHECKSUM_FILE_TIMESTAMPS)

import unittest

JOBS_PER_TASK = 5







#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
tempdir = "temp_filesre_split_and_combine"

#
#   Three starting files
#
original_files = [tempdir  + "/original_%d.fa" % d for d in range(3)]



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
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
       regex(r".*\/original_(\d+).fa"),                               # match original files
       [tempdir + r"/files.split.\1.success",                         # flag file for each original file
        tempdir + r"/files.split.\1.*.fa"],                           # glob pattern
       r"\1")                                                        # index of original file
def split_fasta_file (input_file, outputs, original_index):

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
        open(tempdir + "/files.split.%s.%03d.fa" % (original_index, i), "w")

    open(success_flag,  "w")


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    align_sequences
#
@posttask(lambda: sys.stderr.write("\tSequences aligned\n"))
@transform(split_fasta_file, suffix(".fa"), ".aln")                     # fa -> aln
def align_sequences (input_file, output_filename):
    open(output_filename, "w").write("%s\n" % output_filename)



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    percentage_identity
#
@posttask(lambda: sys.stderr.write("\t%Identity calculated\n"))
@transform(align_sequences,             # find all results from align_sequences
            suffix(".aln"),             # replace suffix with:
            [r".pcid",                  #   .pcid suffix for the result
             r".pcid_success"])         #   .pcid_success to indicate job completed
def percentage_identity (input_file, output_files):
    (output_filename, success_flag_filename) = output_files
    open(output_filename, "w").write("%s\n" % output_filename)
    open(success_flag_filename, "w")



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    combine_results
#
@posttask(lambda: sys.stderr.write("\tResults recombined\n"))
@collate(percentage_identity, regex(r".*files.split\.(\d+)\.\d+.pcid"),
         [tempdir + r"/\1.all.combine_results",
          tempdir + r"/\1.all.combine_results_success"])
def combine_results (input_files, output_files):
    """
    Combine all
    """
    (output_filename, success_flag_filename) = output_files
    out = open(output_filename, "w")
    for inp, flag in input_files:
        out.write(open(inp).read())
    open(success_flag_filename, "w")




class Test_split_regex_and_collate(unittest.TestCase):
    def setUp(self):
        import os
        try:
            shutil.rmtree(tempdir)
        except:
            pass
        os.makedirs(tempdir)
        for f in original_files:
            with open(f, "w") as p: pass

    def cleanup_tmpdir(self):
        os.system('rm -f %s %s' % (os.path.join(tempdir, '*'), RUFFUS_HISTORY_FILE))

    #___________________________________________________________________________
    #
    #   test product() pipeline_printout and pipeline_run
    #___________________________________________________________________________
    def test_collate(self):
        self.cleanup_tmpdir()

        s = StringIO()
        pipeline_printout(s, [combine_results], verbose=5, wrap_width = 10000)
        self.assertIn('Job needs update: Missing files ', s.getvalue())
        #print s.getvalue()

        pipeline_run([combine_results], verbose=0)

    #___________________________________________________________________________
    #
    #   cleanup
    #___________________________________________________________________________
    def tearDown(self):
        shutil.rmtree(tempdir)

#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
#    pipeline_printout(sys.stdout, [combine_results], verbose = 5)
    unittest.main()

