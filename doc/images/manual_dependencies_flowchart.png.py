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

import time
def task_helper(infile, outfile):
    """
    cat input file content to output file
        after writing out job parameters
    """
    if infile:
        output_text = "".join(sorted(open(infile).readlines()))
    else:
        output_text = "None"
    output_text += json.dumps(infile) + " -> " + json.dumps(outfile) + "\n"
    open(outfile, "w").write(output_text)



#
#    task1
#
@files(None, 'a.1')
def task1(infile, outfile):
    """
    First task
    """
    task_helper(infile, outfile)



#
#    task2
#
@transform(task1, regex(r'.1'), '.2')
def task2(infile, outfile):
    """
    Second task
    """
    task_helper(infile, outfile)



#
#    task3
#
@transform(task2, regex(r'.2'), '.3')
def task3(infile, outfile):
    """
    Third task
    """
    task_helper(infile, outfile)



#
#    task4
#
@transform(task3, regex(r'.3'), '.4')
def task4(infile, outfile):
    """
    Fourth task
    """
    task_helper(infile, outfile)

for f in range(4):
    fn = "a.%d" % (f + 1)
    if os.path.exists(fn):
        os.unlink(fn)
pipeline_printout_graph ("manual_dependencies_flowchart1.png", "png", [task4], dpi = 72, size = (2,2))
pipeline_run([task4])
pipeline_printout_graph ("manual_dependencies_flowchart2.png", "png", [task4], dpi = 72, size = (2,2))
open("a.1", "w")
open("a.3", "w")
pipeline_printout_graph ("manual_dependencies_flowchart3.png", "png", [task4], dpi = 72, size = (2,2))
pipeline_printout_graph ("manual_dependencies_flowchart4.png", "png", [task4], [task1], dpi = 72, size = (2,2))
for f in range(4):
    fn = "a.%d" % (f + 1)
    if os.path.exists(fn):
        os.unlink(fn)

