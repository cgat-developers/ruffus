#!/usr/bin/env python
from ruffus import *
from subprocess import Popen, PIPE
parameters = [
                 ['A',  1, 2], # 1st job
                 ['B',  2, 4], # 2nd job
                 ['C',  3, 6], # 3rd job
                 ['C',  4, 6], # 4rd job
                 ['C',  5, 6], # 5rd job
                 ['C',  6, 6], # 6rd job
                 ['C',  7, 6], # 7rd job
                 ['C',  8, 6], # 8rd job
                 ['C',  9, 6], # 9rd job
                 ['C', 10, 6], # 10rd job
             ]
import time,os

@parallel(parameters)
def parallel_task(name, param1, param2):
    sys.stderr.write("    Parallel task %s: " % name)
    sys.stderr.write("%d + %d = %d\n" % (param1, param2, param1 + param2))
    cmds = ["qrsh", 
                "-now", "n", 
                "-cwd", 
                "-p", "-20", 
                "-N", "job%d" % (param1), 
                "-q", "short_jobs.q", 
                "ls qrsh_workaround  > qrsh_workaround/output.%d" % param1]
    p = Popen(cmds, stdin = PIPE)
    p.stdin.close()
    sts = os.waitpid(p.pid, 0)

# 
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    try:
        pipeline_run([parallel_task], multiprocess = 5)
    except Exception, e:
        print e.args
