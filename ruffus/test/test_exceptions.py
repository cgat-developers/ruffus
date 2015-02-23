#!/usr/bin/env python
from __future__ import print_function
"""

    test_exceptions.py

        use :
            --debug               to test automatically
            -j N / --jobs N       to specify multitasking
            -v                    to see the jobs in action
            -n / --just_print     to see what jobs would run

"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
import sys, os

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))



from ruffus import *
import ruffus


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

@parallel([['A', 1], ['B',3], ['C',3], ['D',4], ['E',4], ['F',4]])
def parallel_task(name, param1):
    sys.stderr.write("    Parallel task %s: \n" % name)
    #raise task.JobSignalledBreak("Oops! I did it again!")
    raise Exception("new")


import unittest, shutil
try:
    from StringIO import StringIO
except:
    from io import StringIO

class Test_ruffus(unittest.TestCase):
    def test_ruffus (self):
        try:
            pipeline_run(multiprocess = 50, verbose = 0)
        except ruffus.ruffus_exceptions.RethrownJobError:
            return
        raise Exception("Missing exception")



if __name__ == '__main__':
    unittest.main()


