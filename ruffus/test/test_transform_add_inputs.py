#!/usr/bin/env python
from __future__ import print_function
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



import ruffus
print("\tRuffus Version = ", ruffus.__version__)
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
f =io.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
#(options, remaining_args) = parser.parse_args()

def touch (filename):
    with open(filename, "w"):
        pass


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
tempdir = "tempdir/"
@follows(mkdir(tempdir))
@files([[None, tempdir+ "a.1"], [None, tempdir+ "b.1"]])
def task1(i, o):
    touch(o)


@follows(mkdir(tempdir))
@files([[None, tempdir+ "c.1"], [None, tempdir+ "d.1"]])
def task2(i, o):
    touch(o)


@transform(input = task1, filter = regex(r"(.*)"), add_inputs = add_inputs(task2, "test_transform_inputs.*y"), output = r"\1.output")
def task3_add_inputs(i, o):
    names = ",".join(sorted(i))
    with open(o, "w") as oo:
        oo.write(names)

@merge((task3_add_inputs), tempdir + "final.output")
def task4(i, o):
    with open(o, "w") as o_file:
        for f in sorted(i):
            with open(f) as ii:
                o_file.write(f +":" + ii.read() + ";")

















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
        pipeline_run(multiprocess = 10, verbose = 0)

        correct_output = "tempdir/a.1.output:tempdir/a.1,tempdir/c.1,tempdir/d.1,test_transform_inputs.py;tempdir/b.1.output:tempdir/b.1,tempdir/c.1,tempdir/d.1,test_transform_inputs.py;"
        with open(tempdir + "final.output") as real_output:
            real_output_str = real_output.read()
        self.assertEqual(correct_output, real_output_str)


if __name__ == '__main__':
    unittest.main()

