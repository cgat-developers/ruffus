#!/usr/bin/env python
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

parser = cmdline.get_argparse(   description='Test exceptions?')
options = parser.parse_args()

#  optional logger which can be passed to ruffus tasks
logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

@parallel([['A', 1], ['B',3], ['C',3], ['D',4], ['E',4], ['F',4]])
def parallel_task(name, param1):
    if options.verbose:
        sys.stderr.write("    Parallel task %s: \n\n" % name)
    #raise task.JobSignalledBreak("Oops! I did it again!")
    raise Exception("new")

try:
    cmdline.run (options, logger = logger, log_exceptions = True)
except:
    pass


