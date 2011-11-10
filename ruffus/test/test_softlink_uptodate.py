#!/usr/bin/env python
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

parser = cmdline.get_argparse(   description='Test soft link up to date?')
options = parser.parse_args()

#  optional logger which can be passed to ruffus tasks
logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


import multiprocessing.managers


# list of executed tasks
manager = multiprocessing.managers.SyncManager()
manager.start()
executed_tasks_proxy = manager.dict()
mutex_proxy = manager.Lock()
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
#   First task
#
@split(None, ["a.1", "b.1"], executed_tasks_proxy, mutex_proxy)
def start_task(input_file_names, output_file_names, executed_tasks_proxy, mutex_proxy):
    for output_file_name in output_file_names:
        with open(output_file_name,  "w") as f:
            pass
    with mutex_proxy:
        executed_tasks_proxy["start_task"] = 1

#
#   Forwards file names, is always as up to date as its input files...
#
@transform(start_task, suffix(".1"), ".1", executed_tasks_proxy, mutex_proxy)
def same_file_name_task(input_file_name, output_file_name, executed_tasks_proxy, mutex_proxy):
    with mutex_proxy:
        executed_tasks_proxy["same_file_name_task"] = executed_tasks_proxy.get("same_file_name_task", 0) + 1

#
#   Links file names, is always as up to date if links are not missing
#
@transform(start_task, suffix(".1"), ".linked.1", executed_tasks_proxy, mutex_proxy)
def linked_file_name_task(input_file_name, output_file_name, executed_tasks_proxy, mutex_proxy):
    os.symlink(input_file_name, output_file_name)
    with mutex_proxy:
        executed_tasks_proxy["linked_file_name_task"] = executed_tasks_proxy.get("linked_file_name_task", 0) + 1


#
#   Final task linking everything
#
@transform([linked_file_name_task, same_file_name_task], suffix(".1"), ".3", executed_tasks_proxy, mutex_proxy)
def final_task (input_file_name, output_file_name, executed_tasks_proxy, mutex_proxy):
    with open(output_file_name,  "w") as f:
        pass
    with mutex_proxy:
        executed_tasks_proxy["final_task"] = executed_tasks_proxy.get("final_task", 0) + 1

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Run pipeline


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
#   Run task 1 only
#
logger.debug("Run start_task only")
options.target_tasks = ["start_task"]
cmdline.run (options, logger = logger, log_exceptions = True)
logger.debug("")


#
#   Run task 3 only
#
logger.debug("Run final_task: linked_file_name_task should run as well")
options.target_tasks = []
cmdline.run (options, logger = logger, log_exceptions = True)
logger.debug("")


#
#   Run task 3 again:
#
#       All jobs should be up to date
#
logger.debug("Run final_task again: All jobs should be up to date")
cmdline.run (options, logger = logger, log_exceptions = True)
logger.debug("")


#
#   cleanup
#
for f in ["a.1", "b.1", "a.linked.1", "b.linked.1", "a.3", "b.3", "a.linked.3", "b.linked.3"]:
    if os.path.lexists(f):
        os.unlink(f)




#
#   Make sure right number of jobs / tasks ran
#
for task_name, jobs_count in ({'start_task': 1, 'final_task': 4, 'linked_file_name_task': 2}).iteritems():
    if task_name not in executed_tasks_proxy:
        raise Exception("Error: %s did not run!!" % task_name)
    if executed_tasks_proxy[task_name] != jobs_count:
        raise Exception("Error: %s did not have %d jobs!!" % (task_name, jobs_count))
if "same_file_name_task" in executed_tasks_proxy:
    raise Exception("Error: %s should not have run!!" % "same_file_name_task")

print "Succeeded"
