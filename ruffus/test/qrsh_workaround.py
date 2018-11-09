#!/usr/bin/env python
from __future__ import print_function
import time
from subprocess import Popen, PIPE
from ruffus import *
import os
import sys
# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path, "..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0]
else:
    module_name = __name__
parameters = [
    ['A',  1, 2],  # 1st job
    ['B',  2, 4],  # 2nd job
    ['C',  3, 6],  # 3rd job
    ['C',  4, 6],  # 4rd job
    ['C',  5, 6],  # 5rd job
    ['C',  6, 6],  # 6rd job
    ['C',  7, 6],  # 7rd job
    ['C',  8, 6],  # 8rd job
    ['C',  9, 6],  # 9rd job
    ['C', 10, 6],  # 10rd job
]


@parallel(parameters)
@follows(mkdir("qrsh_workaround"))
@posttask(lambda: os.system("rm -rf qrsh_workaround"))
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
    p = Popen(cmds, stdin=PIPE)
    p.stdin.close()
    sts = os.waitpid(p.pid, 0)


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    pipeline_run([parallel_task], multiprocess=5)
