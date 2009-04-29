#!/usr/bin/python
import os, sys
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *
from time import sleep
    
@parallel([['A', 1], ['B',3], ['C',3], ['D',4], ['E',4], ['F',4]])
def parallel_task(name, param1):
    sleep(2)
    sys.stderr.write("    Parallel task %s: \n\n" % name)
    raise task.JobSignalledBreak("oops")

pipeline_run([parallel_task], multiprocess = 2)

