#!/usr/bin/env python
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
import StringIO
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
                      default=50,
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

import StringIO
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
f =StringIO.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
(options, remaining_args) = parser.parse_args()


tempdir = "temp_filesre_split_and_combine/"

def sleep_a_while ():
    time.sleep(1)

    
if options.verbose:
    verbose_output = sys.stderr
else:
    verbose_output =open("/dev/null", "w")
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    split_fasta_file
#
@posttask(sleep_a_while)
@posttask(lambda: verbose_output.write("Split into %d files\n" % options.jobs_per_task))
@files(tempdir  + "original.fa", tempdir  + "files.split.success")
def split_fasta_file (input_file, success_flag):
    # 
    # remove existing fasta files
    # 
    import glob    
    filenames = sorted(glob.glob(tempdir + "files.split.*.fa"))
    for f in filenames:
        os.unlink(f)
        
        
    import random
    random.seed()
    for i in range(options.jobs_per_task):
        open(tempdir + "files.split.%03d.fa" % i, "w")
        
    open(success_flag,  "w")


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    align_sequences
#
@posttask(sleep_a_while)
@posttask(lambda: verbose_output.write("Sequences aligned\n"))
@follows(split_fasta_file)
@files_re(tempdir  + "files.split.*.fa",       # find all .fa files
            ".fa$", ".aln")                     # fa -> aln
def align_sequences (input_file, output_filename):
    open(output_filename, "w").write("%s\n" % output_filename)



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    percentage_identity
#
@posttask(sleep_a_while)
@posttask(lambda: verbose_output.write("%Identity calculated\n"))
@files_re(align_sequences,                     # find all results from align_sequences
            r"(.*\.)(.+).aln$",                # match file name root and substitute
            r'\g<0>',                          #    the original file
            [r"\1\2.pcid",                     #   .pcid suffix for the result
             r"\1\2.pcid_success"],            #   .pcid_success to indicate job completed
            r"\2")                             #   extra parameter to remember the file index
def percentage_identity (input_file, output_files, split_index):
    (output_filename, success_flag_filename) = output_files
    open(output_filename, "w").write("%s\n" % split_index)
    open(success_flag_filename, "w")

    
    
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    combine_results
#
@posttask(lambda: verbose_output.write("Results recombined\n"))
@posttask(sleep_a_while)
@files_re(percentage_identity, combine(r".*.pcid$"),
                                      [tempdir + "all.combine_results", 
                                       tempdir + "all.combine_results_success"])
def combine_results (input_files, output_files):
    """
    Combine all 
    """
    (output_filename, success_flag_filename) = output_files
    out = open(output_filename, "w")
    for inp, flag in input_files:
        out.write(open(inp).read())
    open(success_flag_filename, "w")



def start_pipeline_afresh ():
    """
    Recreate directory and starting file
    """
    print >>verbose_output, "Start again"
    import os
    os.system("rm -rf %s" % tempdir)
    os.makedirs(tempdir)
    open(tempdir + "original.fa", "w").close()
    sleep_a_while ()

if __name__ == '__main__':
    if options.start_again:
        start_pipeline_afresh()
    if options.just_print:
        pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks,
                            verbose = options.verbose,
                            gnu_make_maximal_rebuild_mode = not options.minimal_rebuild_mode)

    elif options.dependency_file:
        pipeline_printout_graph (     open(options.dependency_file, "w"),
                             options.dependency_graph_format,
                             options.target_tasks,
                             options.forced_tasks,
                             draw_vertically = not options.draw_horizontally,
                             gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                             no_key_legend  = options.no_key_legend_in_graph)
    elif options.debug:
        start_pipeline_afresh()
        pipeline_run(options.target_tasks, options.forced_tasks, multiprocess = options.jobs,
                            logger = stderr_logger if options.verbose else black_hole_logger,
                            gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                            verbose = options.verbose)
        os.system("rm -rf %s" % tempdir)
        print "OK"
    else:
        pipeline_run(options.target_tasks, options.forced_tasks, multiprocess = options.jobs,
                            logger = stderr_logger if options.verbose else black_hole_logger,
                             gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                            verbose = options.verbose)

