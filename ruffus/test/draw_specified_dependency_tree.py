#!/usr/bin/env python
from __future__ import print_function
from adjacent_pairs_iterate import adjacent_pairs_iterate
from ruffus import *
from collections import defaultdict
import sys
import operator
import re
"""

    draw_specified_dependency_tree.py

"""


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys
import os
import os.path
try:
    import StringIO as io
except:
    import io as io

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0]
else:
    module_name = __name__


parser = OptionParser(version="%prog 1.0")
parser.add_option("-d", "--dot_file", dest="dot_file",
                  metavar="FILE",
                  default=os.path.join(exe_path, "test_data/dag.dependency"),
                  type="string",
                  help="name and path of tree file in DOT format")
parser.add_option("-u", "--uptodate_job_names", dest="uptodate_job_names",
                  action="append",
                  metavar="JOBNAME",
                  default=list(),
                  type="string",
                  help="nodes to terminate on.")
parser.add_option("-t", "--target_job_names", dest="target_job_names",
                  action="append",
                  default=list(),
                  metavar="JOBNAME",
                  type="string",
                  help="nodes to start on.")
parser.add_option("-f", "--forced_job_names", dest="forced_job_names",
                  action="append",
                  default=list(),
                  metavar="JOBNAME",
                  type="string",
                  help="nodes to start on.")
parser.add_option("-v", "--verbose", dest="verbose",
                  action="count", default=0,
                  help="Print more verbose messages for each additional verbose level.")
parser.add_option("-z", "--horizontal_graph", dest="horizontal_graph",
                  action="store_true", default=False,
                  help="Draw dependency graph horizontally")
parser.add_option("--skip_upstream", dest="skip_upstream",
                  action="store_true", default=False,
                  help="Only draw from targets")
parser.add_option("--skip_up_to_date", dest="skip_up_to_date",
                  action="store_true", default=False,
                  help="Only draw tasks which need to be rerun")

parameters = [
    "uptodate_job_names"
]

mandatory_parameters = ["dot_file"]


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


sys.path.append(os.path.abspath(os.path.join(exe_path, "..", "..")))

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# _________________________________________________________________________________________

#   make_tree_from_dotfile

# _________________________________________________________________________________________


def make_tree_from_dotfile(stream):

    attributes = re.compile("\[.+\]")

    #
    #   remember node
    #

    for linenum, line in enumerate(stream):
        line = line.strip()
        if "digraph" in line:
            continue
        if not len(line) or line[0] in '#{}/':
            continue
        line = line.strip(';')
        line = attributes.sub("", line)
        if "=" in line:
            continue
        nodes = [x.strip() for x in line.split('->')]
        for name1, name2 in adjacent_pairs_iterate(nodes):
            if not node._is_node(name1):
                node(name1)
            if not node._is_node(name2):
                node(name2)
            node._lookup_node_from_name(name2).add_child(
                node._lookup_node_from_name(name1))

            #
            # task hack
            node._lookup_node_from_name(name2)._action = 1
            node._lookup_node_from_name(name1)._action = 1


def die_error(Msg):
    """
    Standard way of dying after a fatal error
    """
    print_error(Msg)
    sys.exit()


def print_error(Msg):
    """
    Standard way of printing error
    """
    sys.stderr.write("\nError:\n" + wrap_text(Msg, "\t", "") + "\n")


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


if __name__ == '__main__':

    # get help string
    f = io.StringIO()
    parser.print_help(f)
    helpstr = f.getvalue()
    (options, remaining_args) = parser.parse_args()
    # mandatory options
    for parameter in mandatory_parameters:
        if options.__dict__[parameter] is None:
            die_error("Please specify a file in --%s.\n\n" %
                      parameter + helpstr)

    make_tree_from_dotfile(open(options.dot_file))

    #
    #   set up_to_date jobs
    #
    uptodate_jobs = task_names_to_tasks(
        "Up to date", options.uptodate_job_names)
    for n in uptodate_jobs:
        n._signal = True

    graph_printout_in_dot_format(sys.stdout,
                                 options.target_job_names,
                                 options.forced_job_names,
                                 not options.horizontal_graph,
                                 options.skip_upstream,
                                 options.skip_up_to_date)
