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



#
#    up_to_date_task1
#
@files(None, 'a.1')
def up_to_date_task1(infile, outfile):
    open(outfile, "w")



#
#    up_to_date_task2
#
@transform(up_to_date_task1, suffix('.1'), '.2')
def up_to_date_task2(infile, outfile):
    open(outfile, "w")

#
#    task3
#
@transform(up_to_date_task2, suffix('.2'), '.3')
def task3(infile, outfile):
    open(outfile, "w")

#
#    up_to_date_task4
#
@files(None, 'a.4')
def up_to_date_task4(infile, outfile):
    open(outfile, "w")

#
#    task5
#
@transform(up_to_date_task4, suffix('.4'), '.5')
def task5(infile, outfile):
    open(outfile, "w")

#
#    task6
#
@follows(task3)
@transform([task5], suffix('.5'), '.6')
def task6(infile, outfile):
    open(outfile, "w")

#
#    task7
#
@transform(task6, suffix('.6'), '.7')
def final_task(infile, outfile):
    open(outfile, "w")



for f in range(7):
    fn = "a.%d" % (f + 1)
    if os.path.exists(fn):
        os.unlink(fn)
import time
open("a.3", "w")
open("a.7", "w")
open("a.5", "w")
time.sleep(1)
open("a.1", "w")
time.sleep(1)
open("a.2", "w")
time.sleep(1)
open("a.4", "w")
time.sleep(1)
open("a.6", "w")
time.sleep(1)
pipeline_printout_graph ("manual_dependencies_flowchart_intro.png", "png", [final_task], dpi = 72, size = (2,2))
#pipeline_printout (sys.stdout, [final_task], verbose = 5)
for f in range(7):
    fn = "a.%d" % (f + 1)
    if os.path.exists(fn):
        os.unlink(fn)

