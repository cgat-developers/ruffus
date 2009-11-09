#!/usr/bin/env python
"""

    test_exceptions.py
    
        use :
            --debug               to test automatically
            -j N / --jobs N       to specify multitasking
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
                  help="Do not echo to shell but only print to log.")
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
import time

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

@parallel([['A', 1], ['B',3], ['C',3], ['D',4], ['E',4], ['F',4]])
def parallel_task(name, param1):
    time.sleep(2)
    if options.verbose:
        sys.stderr.write("    Parallel task %s: \n\n" % name)
    raise task.JobSignalledBreak("Oops! I did it again!")





if __name__ == '__main__':
    try:
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
            pipeline_run(options.target_tasks, options.forced_tasks, multiprocess = options.jobs,
                                logger = stderr_logger if options.verbose else black_hole_logger,
                                gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                                verbose = options.verbose)
            print "Done"
        else:
            pipeline_run(options.target_tasks, options.forced_tasks, multiprocess = options.jobs,
                                logger = stderr_logger if options.verbose else black_hole_logger,
                                 gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                                verbose = options.verbose)

    except Exception, e:
        if (e.args[0][2] == "ruffus.ruffus_exceptions.JobSignalledBreak" and
            'Oops! I did it again!' in e.args[0][3]):
            print "\nOK\n"
            sys.exit()
        raise

    print "\nFailed\n"
    sys.exit(1)

