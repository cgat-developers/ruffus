#!/usr/bin/env python
from __future__ import print_function
"""

    test_softlink_uptodate.py

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

#parser = cmdline.get_argparse(   description='Test soft link up to date?', version = "%(prog)s v.2.23")
#options = parser.parse_args()

#  optional logger which can be passed to ruffus tasks
#logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


import multiprocessing.managers



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
#   First task
#
def start_task(output_file_name, executed_tasks_proxy, mutex_proxy):
    with open(output_file_name,  "w") as f:
        pass
    with mutex_proxy:
        executed_tasks_proxy["start_task"] = 1

#
#   Forwards file names, is always as up to date as its input files...
#
def same_file_name_task(input_file_name, output_file_name, executed_tasks_proxy, mutex_proxy):
    with mutex_proxy:
        executed_tasks_proxy["same_file_name_task"] = executed_tasks_proxy.get("same_file_name_task", 0) + 1

#
#   Links file names, is always as up to date if links are not missing
#
def linked_file_name_task(input_file_name, output_file_name, executed_tasks_proxy, mutex_proxy):
    os.symlink(input_file_name, output_file_name)
    with mutex_proxy:
        executed_tasks_proxy["linked_file_name_task"] = executed_tasks_proxy.get("linked_file_name_task", 0) + 1


#
#   Final task linking everything
#
def final_task (input_file_name, output_file_name, executed_tasks_proxy, mutex_proxy):
    with open(output_file_name,  "w") as f:
        pass
    with mutex_proxy:
        executed_tasks_proxy["final_task"] = executed_tasks_proxy.get("final_task", 0) + 1

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Run pipeline


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


import unittest, shutil
try:
    from StringIO import StringIO
except:
    from io import StringIO

class Test_ruffus(unittest.TestCase):
    def setUp(self):

        # list of executed tasks
        manager = multiprocessing.managers.SyncManager()
        manager.start()
        global mutex_proxy
        global executed_tasks_proxy
        mutex_proxy = manager.Lock()
        executed_tasks_proxy = manager.dict()

        pipeline = Pipeline.pipelines["main"]
        pipeline.originate(task_func = start_task,
                            output = ["a.1", "b.1"],
                            extras = [executed_tasks_proxy, mutex_proxy])
        pipeline.transform(task_func = same_file_name_task,
                            input = start_task,
                            filter = suffix(".1"),
                            output = ".1",
                            extras = [executed_tasks_proxy, mutex_proxy])
        pipeline.transform( task_func = linked_file_name_task,
                            input = start_task,
                            filter = suffix(".1"),
                            output = ".linked.1",
                            extras = [executed_tasks_proxy, mutex_proxy])
        pipeline.transform(task_func = final_task,
                            input = [linked_file_name_task, same_file_name_task],
                            filter = suffix(".1"),
                            output = ".3",
                            extras = [executed_tasks_proxy, mutex_proxy])

        for f in ["a.1", "b.1", "a.linked.1", "b.linked.1", "a.3", "b.3", "a.linked.3", "b.linked.3"]:
            try:
                os.unlink(f)
            except:
                pass

    def tearDown(self):
        for f in ["a.1", "b.1", "a.linked.1", "b.linked.1", "a.3", "b.3", "a.linked.3", "b.linked.3"]:
            if os.path.lexists(f):
                os.unlink(f)
            else:
                raise Exception("Expected %s missing" % f)

    def test_ruffus (self):
        #
        #   Run task 1 only
        #
        #print("  Run start_task only", file=sys.stderr)
        pipeline_run(log_exceptions = True, verbose = 0)


        #
        #   Run task 3 only
        #
        #print("  Run final_task: linked_file_name_task should run as well", file=sys.stderr)
        pipeline_run(log_exceptions = True, verbose = 0)


        #
        #   Run task 3 again:
        #
        #       All jobs should be up to date
        #
        #print("Run final_task again: All jobs should be up to date", file=sys.stderr)
        pipeline_run(log_exceptions = True, verbose = 0)

        #
        #   Make sure right number of jobs / tasks ran
        #
        for task_name, jobs_count in ({'start_task': 1, 'final_task': 4, 'linked_file_name_task': 2}).items():
            if task_name not in executed_tasks_proxy:
                raise Exception("Error: %s did not run!!" % task_name)
            if executed_tasks_proxy[task_name] != jobs_count:
                raise Exception("Error: %s did not have %d jobs!!" % (task_name, jobs_count))
        if "same_file_name_task" in executed_tasks_proxy:
            raise Exception("Error: %s should not have run!!" % "same_file_name_task")



if __name__ == '__main__':
    unittest.main()

