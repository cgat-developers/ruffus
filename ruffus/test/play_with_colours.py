#!/usr/bin/env python
from __future__ import print_function
from collections import defaultdict
from ruffus.ruffus_exceptions import JobSignalledBreak
from ruffus import *
from optparse import OptionParser
"""

    play_with_colours.py
    [--log_file PATH]
    [--verbose]

"""

################################################################################
#
#   test
#
#
#   Copyright (c) 7/13/2010 Leo Goodstadt
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.
#################################################################################

import sys
import os

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path, "..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0]
else:
    module_name = __name__


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


try:
    import StringIO as io
except:
    import io as io

parser = OptionParser(version="%play_with_colours 1.0",
                      usage="\n\n    play_with_colours "
                      "--flowchart FILE [options] "
                      "[--colour_scheme_index INT ] "
                      "[--key_legend_in_graph]")

#
#   pipeline
#
parser.add_option("--flowchart", dest="flowchart",
                  metavar="FILE",
                  type="string",
                  help="Don't actually run any commands; just print the pipeline "
                  "as a flowchart.")
parser.add_option("--colour_scheme_index", dest="colour_scheme_index",
                  metavar="INTEGER",
                  type="int",
                  help="Index of colour scheme for flow chart.")
parser.add_option("--key_legend_in_graph", dest="key_legend_in_graph",
                  action="store_true", default=False,
                  help="Print out legend and key for dependency graph.")

(options, remaining_args) = parser.parse_args()
if not options.flowchart:
    raise Exception("Missing mandatory parameter: --flowchart.\n")


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Pipeline


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#
# up to date tasks
#
@check_if_uptodate(lambda: (False, ""))
def Up_to_date_task1(infile, outfile):
    pass


@check_if_uptodate(lambda: (False, ""))
@follows(Up_to_date_task1)
def Up_to_date_task2(infile, outfile):
    pass


@check_if_uptodate(lambda: (False, ""))
@follows(Up_to_date_task2)
def Up_to_date_task3(infile, outfile):
    pass


@check_if_uptodate(lambda: (False, ""))
@follows(Up_to_date_task3)
def Up_to_date_final_target(infile, outfile):
    pass


#
# Explicitly specified
#
@check_if_uptodate(lambda: (False, ""))
@follows(Up_to_date_task1)
def Explicitly_specified_task(infile, outfile):
    pass


#
# Tasks to run
#
@follows(Explicitly_specified_task)
def Task_to_run1(infile, outfile):
    pass


@follows(Task_to_run1)
def Task_to_run2(infile, outfile):
    pass


@follows(Task_to_run2)
def Task_to_run3(infile, outfile):
    pass


@check_if_uptodate(lambda: (False, ""))
@follows(Task_to_run2)
def Up_to_date_task_forced_to_rerun(infile, outfile):
    pass


#
# Final target
#
@follows(Up_to_date_task_forced_to_rerun, Task_to_run3)
def Final_target(infile, outfile):
    pass

#
# Ignored downstream
#


@follows(Final_target)
def Downstream_task1_ignored(infile, outfile):
    pass


@follows(Final_target)
def Downstream_task2_ignored(infile, outfile):
    pass


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#   Main logic
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
custom_flow_chart_colour_scheme = defaultdict(dict)

#
#   Base chart on this overall colour scheme index
#
custom_flow_chart_colour_scheme["colour_scheme_index"] = options.colour_scheme_index

#
#   Overriding colours
#
if options.colour_scheme_index is None:
    custom_flow_chart_colour_scheme["Vicious cycle"]["linecolor"] = '"#FF3232"'
    custom_flow_chart_colour_scheme["Pipeline"]["fontcolor"] = '"#FF3232"'
    custom_flow_chart_colour_scheme["Key"]["fontcolor"] = "black"
    custom_flow_chart_colour_scheme["Key"]["fillcolor"] = '"#F6F4F4"'
    custom_flow_chart_colour_scheme["Task to run"]["linecolor"] = '"#0044A0"'
    custom_flow_chart_colour_scheme["Up-to-date"]["linecolor"] = "gray"
    custom_flow_chart_colour_scheme["Final target"]["fillcolor"] = '"#EFA03B"'
    custom_flow_chart_colour_scheme["Final target"]["fontcolor"] = "black"
    custom_flow_chart_colour_scheme["Final target"]["color"] = "black"
    custom_flow_chart_colour_scheme["Final target"]["dashed"] = 0
    custom_flow_chart_colour_scheme["Vicious cycle"]["fillcolor"] = '"#FF3232"'
    custom_flow_chart_colour_scheme["Vicious cycle"]["fontcolor"] = 'white'
    custom_flow_chart_colour_scheme["Vicious cycle"]["color"] = "white"
    custom_flow_chart_colour_scheme["Vicious cycle"]["dashed"] = 0
    custom_flow_chart_colour_scheme["Up-to-date task"]["fillcolor"] = '"#B8CC6E"'
    custom_flow_chart_colour_scheme["Up-to-date task"]["fontcolor"] = '"#006000"'
    custom_flow_chart_colour_scheme["Up-to-date task"]["color"] = '"#006000"'
    custom_flow_chart_colour_scheme["Up-to-date task"]["dashed"] = 0
    custom_flow_chart_colour_scheme["Down stream"]["fillcolor"] = "white"
    custom_flow_chart_colour_scheme["Down stream"]["fontcolor"] = "gray"
    custom_flow_chart_colour_scheme["Down stream"]["color"] = "gray"
    custom_flow_chart_colour_scheme["Down stream"]["dashed"] = 0
    custom_flow_chart_colour_scheme["Explicitly specified task"]["fillcolor"] = "transparent"
    custom_flow_chart_colour_scheme["Explicitly specified task"]["fontcolor"] = "black"
    custom_flow_chart_colour_scheme["Explicitly specified task"]["color"] = "black"
    custom_flow_chart_colour_scheme["Explicitly specified task"]["dashed"] = 0
    custom_flow_chart_colour_scheme["Task to run"]["fillcolor"] = '"#EBF3FF"'
    custom_flow_chart_colour_scheme["Task to run"]["fontcolor"] = '"#0044A0"'
    custom_flow_chart_colour_scheme["Task to run"]["color"] = '"#0044A0"'
    custom_flow_chart_colour_scheme["Task to run"]["dashed"] = 0
    custom_flow_chart_colour_scheme["Up-to-date task forced to rerun"]["fillcolor"] = 'transparent'
    custom_flow_chart_colour_scheme["Up-to-date task forced to rerun"]["fontcolor"] = '"#0044A0"'
    custom_flow_chart_colour_scheme["Up-to-date task forced to rerun"]["color"] = '"#0044A0"'
    custom_flow_chart_colour_scheme["Up-to-date task forced to rerun"]["dashed"] = 1
    custom_flow_chart_colour_scheme["Up-to-date Final target"]["fillcolor"] = '"#EFA03B"'
    custom_flow_chart_colour_scheme["Up-to-date Final target"]["fontcolor"] = '"#006000"'
    custom_flow_chart_colour_scheme["Up-to-date Final target"]["color"] = '"#006000"'
    custom_flow_chart_colour_scheme["Up-to-date Final target"]["dashed"] = 0

if __name__ == '__main__':
    pipeline_printout_graph(

        open(options.flowchart, "w"),
        # use flowchart file name extension to decide flowchart format
        #   e.g. svg, jpg etc.
        os.path.splitext(options.flowchart)[1][1:],

        # final targets
        [Final_target, Up_to_date_final_target],

        # Explicitly specified tasks
        [Explicitly_specified_task],

        # Do we want key legend
        no_key_legend=not options.key_legend_in_graph,

        # Print all the task types whether used or not
        minimal_key_legend=False,

        user_colour_scheme=custom_flow_chart_colour_scheme,
        pipeline_name="Colour schemes",
        pipeline="main")
