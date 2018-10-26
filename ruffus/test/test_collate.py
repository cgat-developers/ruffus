#!/usr/bin/env python
from __future__ import print_function
import json
from collections import defaultdict
import shutil
import unittest
from ruffus import pipeline_run, Pipeline, follows, posttask, split, collate, mkdir, regex
import sys

"""

    test_collate.py

        test branching dependencies

"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

try:
    from StringIO import StringIO
except:
    from io import StringIO

# use simplejson in place of json for python < 2.6
# try:
#    import json
# except ImportError:
#    import simplejson
#    json = simplejson

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


species_list = defaultdict(list)
species_list["mammals"].append("cow")
species_list["mammals"].append("horse")
species_list["mammals"].append("sheep")
species_list["reptiles"].append("snake")
species_list["reptiles"].append("lizard")
species_list["reptiles"].append("crocodile")
species_list["fish"].append("pufferfish")


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#    task1
#

def do_write(file_name, what):
    with open(file_name, "a") as oo:
        oo.write(what)


test_file = tempdir + "task.done"


@follows(mkdir(tempdir, tempdir + "test"))
@posttask(lambda: do_write(tempdir + "task.done", "Task 1 Done\n"))
@split(None, tempdir + '*.animal')
def prepare_files(no_inputs, outputs):
    # cleanup previous
    for f in outputs:
        os.unlink(f)

    for grouping in species_list:
        for species_name in species_list[grouping]:
            filename = tempdir + "%s.%s.animal" % (species_name, grouping)
            with open(filename, "w") as oo:
                oo.write(species_name + "\n")


#
#    task2
#
@collate(prepare_files, regex(r'(.*/).*\.(.*)\.animal'), r'\1\2.results')
@posttask(lambda: do_write(tempdir + "task.done", "Task 2 Done\n"))
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
        with open(tempdir + grouping + ".results") as oo:
            assert(oo.read() == "".join(
                s + "\n" for s in sorted(species_list[grouping])))


class Test_ruffus(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_ruffus(self):
        pipeline_run(multiprocess=10, verbose=0, pipeline="main")
        check_species_correct()

    def test_newstyle_ruffus(self):
        test_pipeline = Pipeline("test")
        test_pipeline.split(task_func=prepare_files,
                            input=None,
                            output=tempdir + '*.animal')\
            .follows(mkdir(tempdir, tempdir + "test"))\
            .posttask(lambda: do_write(tempdir + "task.done", "Task 1 Done\n"))

        test_pipeline.collate(task_func=summarise_by_grouping,
                              input=prepare_files,
                              filter=regex(r'(.*/).*\.(.*)\.animal'),
                              output=r'\1\2.results')\
            .posttask(lambda: do_write(tempdir + "task.done", "Task 2 Done\n"))

        test_pipeline.run(multiprocess=10, verbose=0)
        check_species_correct()


if __name__ == '__main__':
    unittest.main()
