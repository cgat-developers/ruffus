#!/usr/bin/env python
from __future__ import print_function
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





tempdir = "temp_filesre_split_and_combine/"



verbose_output = sys.stderr
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    split_fasta_file
#
@posttask(lambda: verbose_output.write("    Split into %d files\n" % 10))
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
    for i in range(10):
        with open(tempdir + "files.split.%03d.fa" % i, "w") as oo:
            pass

    with open(success_flag,  "w") as oo:
        pass


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    align_sequences
#
@posttask(lambda: verbose_output.write("    Sequences aligned\n"))
@transform(split_fasta_file, suffix(".fa"), ".aln")                     # fa -> aln
def align_sequences (input_file, output_filename):
    with open(output_filename, "w") as oo:
        oo.write("%s\n" % output_filename)



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    percentage_identity
#
@posttask(lambda: verbose_output.write("    %Identity calculated\n"))
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
@posttask(lambda: verbose_output.write("    Results recombined\n"))
@merge(percentage_identity, [tempdir + "all.combine_results",
                             tempdir + "all.combine_results_success"])
def combine_results (input_files, output_files):
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

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
            pass
        except:
            pass

    def test_ruffus (self):
        pipeline_run(multiprocess = 50, verbose = 0)
        if not os.path.exists(tempdir + "all.combine_results"):
            raise Exception("Missing %s" % (tempdir + "all.combine_results"))



if __name__ == '__main__':
    unittest.main()

