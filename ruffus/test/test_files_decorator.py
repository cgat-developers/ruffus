#!/usr/bin/env python
"""

    test_files_decorator.py

        test @files which take single files forwards arguments as single files rather
        than as lists

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
print "\tRuffus Version = ", ruffus.__version__
parser = OptionParser(version="%%prog v1.0, ruffus v%s" % ruffus.ruffus_version.__version)
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

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

def test_job_io(infiles, outfiles, extra_params):
    """
    cat input files content to output files
        after writing out job parameters
    """
    # dump parameters
    params = (infiles, outfiles) + extra_params

    if isinstance(infiles, str):
        infile_names = [infiles]
    elif infiles == None:
        infile_names = []
    else:
        infile_names = infiles
        
    if isinstance(outfiles, str):
        outfile_names = [outfiles]
    else:
        outfile_names = outfiles


    output_text = list()
    for f in infile_names:
        output_text.append(open(f).read())
    output_text = "".join(sorted(output_text))
    output_text += json.dumps(infiles) + " -> " + json.dumps(outfiles) + "\n"
    for f in outfile_names:
        open(f, "w").write(output_text)

        
        
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
tempdir = "tempdir/"
@follows(mkdir(tempdir))
#
#    task1
#
@files(None, tempdir + 'a.1')
def task1(infiles, outfiles, *extra_params):
    """
    First task
    """
    test_job_io(infiles, outfiles, extra_params)



#
#    task2
#
@transform(task1, regex(r".*"), tempdir + 'b.1')
def task2(infiles, outfiles, *extra_params):
    """
    Second task
    """
    test_job_io(infiles, outfiles, extra_params)
    assert(infiles == tempdir + "a.1")



#
#    task3
#
@files(task2, tempdir + 'c.1')
def task3(infiles, outfiles, *extra_params):
    """
    Second task
    """
    test_job_io(infiles, outfiles, extra_params)
    assert(infiles == tempdir + "b.1")

import unittest

class Test_task(unittest.TestCase):

    def tearDown (self):
        """
        """
        import glob
        for f in glob.glob(tempdir + "*"):
            os.unlink(f)
        os.rmdir(tempdir)


    def test_task (self):
        pipeline_run([task3], options.forced_tasks, multiprocess = options.jobs,
                            verbose = options.verbose)


if __name__ == '__main__':
    if options.just_print:
        pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks,
                            verbose = options.verbose)

    elif options.dependency_file:
        pipeline_printout_graph (     open(options.dependency_file, "w"),
                             options.dependency_graph_format,
                             options.target_tasks,
                             options.forced_tasks,
                             draw_vertically = not options.draw_horizontally,
                             no_key_legend  = options.no_key_legend_in_graph)
    else:
        sys.argv= sys.argv[0:1]
        unittest.main()        
    
