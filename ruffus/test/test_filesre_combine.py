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
def do_write(file_name, what):
    with open(file_name, "a") as oo:
        oo.write(what)
test_file = tempdir + "task.done"


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    task1
#
@follows(mkdir(tempdir, tempdir + "test"))
@posttask(lambda: do_write(test_file, "Task 1 Done\n"))
def prepare_files ():
    for grouping in species_list.keys():
        for species_name in species_list[grouping]:
            filename = tempdir + "%s.%s.animal" % (species_name, grouping)
            with open(filename, "w") as oo:
                oo.write(species_name + "\n")


#
#    task2
#
@files_re(tempdir + '*.animal', r'(.*/)(.*)\.(.*)\.animal', combine(r'\1\2.\3.animal'), r'\1\3.results')
@follows(prepare_files)
@posttask(lambda: do_write(test_file, "Task 2 Done\n"))
def summarise_by_grouping(infiles, outfile):
    """
    Summarise by each species group, e.g. mammals, reptiles, fish
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfile]))
    with open(outfile, "w") as oo:
        for i in infiles:
            with open(i) as ii:
                oo.write(ii.read())
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfile]))







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
        with open(tempdir + grouping + ".results") as ii:
            assert(ii.read() ==
                    "".join(s + "\n" for s in sorted(species_list[grouping])))





import unittest, shutil
class Test_ruffus(unittest.TestCase):

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass
    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_ruffus (self):
        ""
        pipeline_run(multiprocess = 10, verbose = 0)
        check_species_correct()


if __name__ == '__main__':
    unittest.main()

