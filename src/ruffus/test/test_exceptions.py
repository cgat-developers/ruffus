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
    raise task.JobSignalledBreak("Oops! I did it again!")

# 
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    try:
        pipeline_run([parallel_task], multiprocess = 2)
    except Exception, e:
        print e
        if (e.args[0][2] == "ruffus.ruffus_exceptions.JobSignalledBreak" and
            'Oops! I did it again!' in e.args[0][3]):
            print "\nCorrect\n"
            sys.exit()
    print "\nFailed\n"
    sys.exit(1)
    
