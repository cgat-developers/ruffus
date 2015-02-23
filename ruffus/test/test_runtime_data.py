#!/usr/bin/env python
from __future__ import print_function
"""

    test_tasks.py

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

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__




parser = OptionParser(version="%prog 1.0")
parser.add_option("-t", "--target_tasks", dest="target_tasks",
                  action="append",
                  default = list(),
                  metavar="JOBNAME",
                  type="string",
                  help="Target task(s) of pipeline.")
parser.add_option("-R", "--runtime_files", dest="runtime_files",
                  action="append",
                  default = ["a.3"],
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
parser.add_option("-d", "--debug", dest = "debug",
                  action="count", default=0,
                  help="Cleanup afterwards.")
parser.add_option("--dependency", dest="dependency_file",
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

sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888





# get help string
f =io.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
(options, remaining_args) = parser.parse_args()





#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#
#    task1
#
@originate(['a.1'] + options.runtime_files)
def task1(outfile):
    """
    First task
    """
    output_text  = ""
    output_text += "    -> " + json.dumps(outfile) + "\n"
    with open(outfile, "w") as oo:
        oo.write(output_text)



#
#    task2
#
@transform(task1, suffix(".1"), ".2")
def task2(infile, outfile):
    """
    Second task
    """
    if infile:
        with open(infile) as ii:
            output_text  = ii.read()
    else:
        output_text = ""
    output_text += json.dumps(infile) + " -> " + json.dumps(outfile) + "\n"
    with open(outfile, "w") as oo:
        oo.write(output_text)



#
#    task3
#
@transform(task2, suffix(".2"), ".3")
def task3(infile, outfile):
    """
    Third task
    """
    if infile:
        with open(infile) as ii:
            output_text  = ii.read()
    else:
        output_text = ""
    output_text += json.dumps(infile) + " -> " + json.dumps(outfile) + "\n"
    with open(outfile, "w") as oo:
        oo.write(output_text)



#
#    task4
#
@follows(task3)
@transform(runtime_parameter("a"), suffix(".3"), ".4")
def task4(infile, outfile):
    """
    Fourth task
    """
    if infile:
        with open(infile) as ii:
            output_text  = ii.read()
    else:
        output_text = ""
    output_text += json.dumps(infile) + " -> " + json.dumps(outfile) + "\n"
    with open(outfile, "w") as oo:
        oo.write(output_text)







import unittest, shutil
try:
    from StringIO import StringIO
except:
    from io import StringIO

class Test_ruffus(unittest.TestCase):
    def setUp(self):
        for f in ["a.1", "a.2","a.3","a.4"]:
            if os.path.exists(f):
                os.unlink(f)

    def tearDown(self):
        for f in ["a.1", "a.2","a.3","a.4"]:
            if os.path.exists(f):
                os.unlink(f)
            else:
                raise Exception("%s is missing" % f)


    def test_ruffus (self):
        pipeline_run(verbose = 0, runtime_data = {"a": options.runtime_files})



if __name__ == '__main__':
    unittest.main()

