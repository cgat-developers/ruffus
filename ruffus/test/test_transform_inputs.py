#!/usr/bin/env python
"""

    test_transform_with_no_re_matches.py
    
        test messages with no regular expression matches
        
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


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
tempdir = "tempdir/"
@follows(mkdir(tempdir))
@files([[None, tempdir+ "a.1"], [None, tempdir+ "b.1"]])
def task1(i, o): 
    open(o,  "w")


@follows(mkdir(tempdir))
@files([[None, tempdir+ "c.1"], [None, tempdir+ "d.1"]])
def task2(i, o): 
    open(o,  "w")

    
@transform(task1, regex(r"(.*)"), inputs(((r"\1"), task2, "test_transform_inputs.*")), r"\1.output")
def task3(i, o):
    names = ",".join(sorted(i))
    for f in o:
        open(o,  "w").write(names)
    
@merge((task3), tempdir + "final.output")
def task4(i, o):
    o_file = open(o, "w")
    for f in sorted(i):
        o_file.write(f +":" +open(f).read() + ";")

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
        pipeline_run([task4], options.forced_tasks, multiprocess = options.jobs,
                            verbose = options.verbose)
        
        correct_output = "tempdir/a.1.output:tempdir/a.1,tempdir/c.1,tempdir/d.1,test_transform_inputs.py;tempdir/b.1.output:tempdir/b.1,tempdir/c.1,tempdir/d.1,test_transform_inputs.py;"
        real_output = open(tempdir + "final.output").read()
        self.assert_(correct_output == real_output)
        

if __name__ == '__main__':
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
    else:
        sys.argv= sys.argv[0:1]
        unittest.main()        

