#!/usr/bin/env python
"""

    branching.py
    
        test branching dependencies

"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys, os
import os.path
import StringIO
import re

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__




parser = OptionParser(version="%prog 1.0")
parser.add_option("-D", "--debug", dest="debug",
                    action="store_true", default=False,
                    help="Make sure output is correct and clean up.")
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

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888





# get help string
f =StringIO.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
(options, remaining_args) = parser.parse_args()

species_list = defaultdict(list)
species_list["mammals"].append("cow"       )
species_list["mammals"].append("horse"     )
species_list["mammals"].append("sheep"     )
species_list["reptiles"].append("snake"     )
species_list["reptiles"].append("lizard"    )
species_list["reptiles"].append("crocodile" )
species_list["fish"   ].append("pufferfish")


tempdir = "temp_filesre_combine/"


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    task1
#
@follows(mkdir(tempdir, tempdir + "test"))
@posttask(lambda: open(tempdir + "task.done", "a").write("Task 1 Done\n"))
def prepare_files ():
    for grouping in species_list.keys():
        for species_name in species_list[grouping]:
            filename = tempdir + "%s.%s.animal" % (species_name, grouping)
            open(filename, "w").write(species_name + "\n")


#
#    task2
#
@files_re(tempdir + '*.animal', r'(.*/)(.*)\.(.*)\.animal', combine(r'\1\2.\3.animal'), r'\1\3.results')
@follows(prepare_files)
@posttask(lambda: open(tempdir + "task.done", "a").write("Task 2 Done\n"))
def summarise_by_grouping(infiles, outfile):
    """
    Summarise by each species group, e.g. mammals, reptiles, fish
    """
    open(tempdir + "jobs.start",  "a").write('job = %s\n' % json.dumps([infiles, outfile]))
    o = open(outfile, "w")
    for i in infiles:
        o.write(open(i).read())
    open(tempdir + "jobs.finish",  "a").write('job = %s\n' % json.dumps([infiles, outfile]))







def check_species_correct():
    """
    #cow.mammals.animal
    #horse.mammals.animal
    #sheep.mammals.animal
    #    -> mammals.results
    #
    #snake.reptiles.animal
    #lizard.reptiles.animal
    #crocodile.reptiles.animal
    #    -> reptiles.results
    #
    #pufferfish.fish.animal
    #    -> fish.results
    """
    for grouping in species_list:
        assert(open(tempdir + grouping + ".results").read() ==
                "".join(s + "\n" for s in sorted(species_list[grouping])))





#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    if options.just_print:
        pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks,
                            long_winded=True,
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
        import os
        os.system("rm -rf %s" % tempdir)
        pipeline_run(options.target_tasks, options.forced_tasks, multiprocess = options.jobs,
                            logger = stderr_logger if options.verbose else black_hole_logger,
                            gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                            verbose = options.verbose > 1)


        check_species_correct()
        #os.system("rm -rf %s" % tempdir)
        print "OK"
    else:
        pipeline_run(options.target_tasks, options.forced_tasks, multiprocess = options.jobs,
                            logger = stderr_logger if options.verbose else black_hole_logger,
                             gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                            verbose = options.verbose > 1)


