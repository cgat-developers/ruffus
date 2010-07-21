#!/usr/bin/env python
import sys, os

# add self to search path for testing
if __name__ == '__main__':
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__

# Use import path from <<../python_modules>>
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"../..")))

from ruffus import *
import json


def Explicitly_specified_task(infile, outfile):
    pass


@follows(Explicitly_specified_task)
def Task_to_run(infile, outfile):
    pass

@follows(Task_to_run)
def Up_to_date_task_forced_to_rerun(infile, outfile):
    pass


@follows(Up_to_date_task_forced_to_rerun)
def Final_target(infile, outfile):
    pass

@follows(Final_target)
def Downstream_task1_ignored(infile, outfile):
    pass

@follows(Final_target)
def Downstream_task2_ignored(infile, outfile):
    pass

pipeline_printout_graph ("pretty_flowchart.png", "png", [Final_target], [Explicitly_specified_task], dpi = 72, size = (2,2), draw_vertically = False, no_key_legend = True)

