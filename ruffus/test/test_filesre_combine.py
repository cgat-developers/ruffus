#!/usr/bin/env python
from __future__ import print_function
"""

    branching.py

        test branching dependencies

"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import sys, os
import os.path
# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *
import ruffus.cmdline as cmdline


parser = cmdline.get_argparse(description='Tests legacy @files_re with combine()', version="%prog 1.0")

parser.add_argument("-D", "--debug",
                    action="store_true",
                    help="Make sure output is correct and clean up.")
options = parser.parse_args()

#  standard python logger which can be synchronised across concurrent Ruffus tasks
logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)







#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

try:
    import StringIO as io
except:
    import io as io
import re
import operator
from collections import defaultdict

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888





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


    if options.debug:
        import os
        os.system("rm -rf %s" % tempdir)
        options=cmdline.handle_verbose (options)
        pipeline_run(target_tasks = options.target_tasks, forcedtorun_tasks  = options.forced_tasks, multiprocess = options.jobs, verbose = options.verbose)
        check_species_correct()
        #os.system("rm -rf %s" % tempdir)
        print("OK")
    else:
        cmdline.run (options)

