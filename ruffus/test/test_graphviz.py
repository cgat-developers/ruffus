#!/usr/bin/env python
from __future__ import print_function
from ruffus.ruffus_exceptions import JobSignalledBreak
from ruffus import transform, graphviz, check_if_uptodate, follows, Pipeline, \
    pipeline_run, pipeline_printout, pipeline_printout_graph
import sys

"""
    test_graphviz.py

"""
import unittest

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

try:
    from StringIO import StringIO
except:
    from io import StringIO, BytesIO


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Pipeline


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#
# up to date tasks
#
@check_if_uptodate(lambda: (False, ""))
def Up_to_date_task1(infile, outfile):
    pass


@graphviz(URL='"http://cnn.com"', fillcolor='"#FFCCCC"',
          color='"#FF0000"', pencolor='"#FF0000"', fontcolor='"#4B6000"',
          label_suffix="???", label_prefix="What is this?<BR/> ",
          label="<What <FONT COLOR=\"red\">is</FONT>this>",
          shape="component", height=1.5, peripheries=5,
          style="dashed")
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


class Test_graphviz(unittest.TestCase):
    # ___________________________________________________________________________
    #
    #   test product() pipeline_printout diagnostic error messsages
    #
    #       require verbose >= 3 or an empty jobs list
    # ___________________________________________________________________________
    def test_graphviz_dot(self):
        """Make sure annotations from graphviz appear in dot
        """

        if sys.hexversion >= 0x03000000:
            # everything is unicode in python3
            s = BytesIO()
        else:
            s = StringIO()

        pipeline_printout_graph(
            s,
            # use flowchart file name extension to decide flowchart format
            #   e.g. svg, jpg etc.
            "dot",
            [Final_target, Up_to_date_final_target], pipeline="main")
        self.assertTrue('[URL="http://cnn.com", color="#FF0000", fillcolor="#FFCCCC", fontcolor="#4B6000", height=1.5, label=<What is this?<BR/> What <FONT COLOR="red">is</FONT>this???>, pencolor="#FF0000", peripheries=5, shape=component, style=dashed]' in s.getvalue().decode())

    def test_newstyle_graphviz_dot(self):
        test_pipeline = Pipeline("test")
        test_pipeline.check_if_uptodate(Up_to_date_task1, lambda: (False, ""))
        test_pipeline.follows(Up_to_date_task2, Up_to_date_task1)\
            .check_if_uptodate(lambda: (False, ""))\
            .graphviz(URL='"http://cnn.com"', fillcolor='"#FFCCCC"',
                      color='"#FF0000"', pencolor='"#FF0000"', fontcolor='"#4B6000"',
                      label_suffix="???", label_prefix="What is this?<BR/> ",
                      label="<What <FONT COLOR=\"red\">is</FONT>this>",
                      shape="component", height=1.5, peripheries=5,
                      style="dashed")
        test_pipeline.follows(Up_to_date_task3, Up_to_date_task2)\
            .check_if_uptodate(lambda: (False, ""))
        test_pipeline.follows(Up_to_date_final_target, Up_to_date_task3)\
            .check_if_uptodate(lambda: (False, ""))
        test_pipeline.follows(Explicitly_specified_task, Up_to_date_task1)\
            .check_if_uptodate(lambda: (False, ""))
        test_pipeline.follows(Task_to_run1, Explicitly_specified_task)
        test_pipeline.follows(Task_to_run2, Task_to_run1)
        test_pipeline.follows(Task_to_run3, Task_to_run2)
        test_pipeline.follows(Up_to_date_task_forced_to_rerun, Task_to_run2)\
            .check_if_uptodate(lambda: (False, ""))
        test_pipeline.follows(
            Final_target, Up_to_date_task_forced_to_rerun, Task_to_run3)
        test_pipeline.follows(Downstream_task1_ignored, Final_target)
        test_pipeline.follows(Downstream_task2_ignored, Final_target)

        if sys.hexversion >= 0x03000000:
            # everything is unicode in python3
            s = BytesIO()
        else:
            s = StringIO()

        test_pipeline.printout_graph(
            s,
            # use flowchart file name extension to decide flowchart format
            #   e.g. svg, jpg etc.
            "dot",
            [Final_target, Up_to_date_final_target])
        self.assertTrue('[URL="http://cnn.com", color="#FF0000", fillcolor="#FFCCCC", fontcolor="#4B6000", height=1.5, label=<What is this?<BR/> What <FONT COLOR="red">is</FONT>this???>, pencolor="#FF0000", peripheries=5, shape=component, style=dashed]' in s.getvalue().decode())


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    unittest.main()
