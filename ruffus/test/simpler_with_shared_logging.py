#!/usr/bin/env python
from __future__ import print_function
import time
import logging
from ruffus.proxy_logger import *
from ruffus import *
from collections import defaultdict
import operator
import re
"""

    simpler_with_shared_logging.py

"""


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys
import os
import os.path
try:
    import StringIO as io
except:
    import io as io

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path, "..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0]
else:
    module_name = __name__


parser = OptionParser(version="%prog 1.0")
parser.add_option("-t", "--target_tasks", dest="target_tasks",
                  action="append",
                  default=list(),
                  metavar="JOBNAME",
                  type="string",
                  help="Target task(s) of pipeline.")
parser.add_option("-f", "--forced_tasks", dest="forced_tasks",
                  action="append",
                  default=list(),
                  metavar="JOBNAME",
                  type="string",
                  help="Pipeline task(s) which will be included even if they are up to date.")
parser.add_option("-j", "--jobs", dest="jobs",
                  default=1,
                  metavar="jobs",
                  type="int",
                  help="Specifies  the number of jobs (commands) to run simultaneously.")
parser.add_option("-v", "--verbose", dest="verbose",
                  action="count", default=0,
                  help="Print more verbose messages for each additional verbose level.")
parser.add_option("-d", "--dependency", dest="dependency_file",
                  # default="simple.svg",
                  metavar="FILE",
                  type="string",
                  help="Print a dependency graph of the pipeline that would be executed "
                        "to FILE, but do not execute it.")
parser.add_option("-F", "--dependency_graph_format", dest="dependency_graph_format",
                  metavar="FORMAT",
                  type="string",
                  default='svg',
                  help="format of dependency graph file. Can be 'ps' (PostScript), " +
                  "'svg' 'svgz' (Structured Vector Graphics), " +
                  "'png' 'gif' (bitmap  graphics) etc ")
parser.add_option("-n", "--just_print", dest="just_print",
                  action="store_true", default=False,
                  help="Print a description of the jobs that would be executed, "
                        "but do not execute them.")
parser.add_option("-M", "--minimal_rebuild_mode", dest="minimal_rebuild_mode",
                  action="store_true", default=False,
                  help="Rebuild a minimum of tasks necessary for the target. "
                  "Ignore upstream out of date tasks if intervening tasks are fine.")
parser.add_option("-K", "--no_key_legend_in_graph", dest="no_key_legend_in_graph",
                  action="store_true", default=False,
                  help="Do not print out legend and key for dependency graph.")
parser.add_option("-H", "--draw_graph_horizontally", dest="draw_horizontally",
                  action="store_true", default=False,
                  help="Draw horizontal dependency graph.")

parser.add_option("-L", "--log_file_name", dest="log_file_name",
                  default="/tmp/simple.log",
                  metavar="FILE",
                  type="string",
                  help="log file.")
parameters = [
]


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


sys.path.append(os.path.abspath(os.path.join(exe_path, "..", "..")))

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Shared logging


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

def create_custom_file_func(params):
    """
    creates function which can be used as input to @files_func
    """
    def cust_func():
        for job_param in params:
            yield job_param
    return cust_func


def is_job_uptodate(infiles, outfiles, *extra_params):
    """
    assumes first two parameters are files, checks if they are up to date
    """
    return task.needs_update_check_modify_time(infiles, outfiles, *extra_params)


def test_post_task_function():
    print("Hooray")


def test_job_io(infiles, outfiles, extra_params):
    """
    cat input files content to output files
        after writing out job parameters
    """

    # dump parameters
    params = (infiles, outfiles)  # + extra_params[0:-3]

    logger_proxy, logging_mutex = extra_params
    with logging_mutex:
        logger_proxy.debug("job = %s, process name = %s" %
                           (json.dumps(params),
                            multiprocessing.current_process().name))

    sys.stdout.write('    job = %s\n' % json.dumps(params))

    if isinstance(infiles, str):
        infiles = [infiles]
    elif infiles is None:
        infiles = []
    if isinstance(outfiles, str):
        outfiles = [outfiles]
    output_text = list()
    for f in infiles:
        output_text.append(open(f).read())
    output_text = "".join(sorted(output_text))
    output_text += json.dumps(infiles) + " -> " + json.dumps(outfiles) + "\n"
    for f in outfiles:
        open(f, "w").write(output_text)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


if __name__ == '__main__':

    # get help string
    f = io.StringIO()
    parser.print_help(f)
    helpstr = f.getvalue()

    #
    #   Get options
    #
    (options, remaining_args) = parser.parse_args()

    args = {}
    args["file_name"] = options.log_file_name
    args["level"] = logging.DEBUG
    args["rotating"] = True
    args["maxBytes"] = 20000
    args["backupCount"] = 10
    args["formatter"] = "%(asctime)s - %(name)s - %(levelname)6s - %(message)s"

    (logger_proxy,
     logging_mutex) = make_shared_logger_and_proxy(setup_std_shared_logger,
                                                   "my_logger", args)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#
#    task1
#
@files(None, os.path.abspath('a.1'), logger_proxy, logging_mutex)
def task1(infiles, outfiles, *extra_params):
    """
    First task
    """
    test_job_io(infiles, outfiles, extra_params)


#
#    task2
#
@files_re('*.1', '(.*).1', r'\1.1', r'\1.2', logger_proxy, logging_mutex)
@follows(task1)
def task2(infiles, outfiles, *extra_params):
    """
    Second task
    """
    test_job_io(infiles, outfiles, extra_params)


#
#    task3
#
@files_re('*.1', '(.*).1', r'\1.2', r'\1.3', logger_proxy, logging_mutex)
@follows(task2)
def task3(infiles, outfiles, *extra_params):
    """
    Third task
    """
    test_job_io(infiles, outfiles, extra_params)


#
#    task4
#
@files_re('*.1', '(.*).1', r'\1.3', r'\1.4', logger_proxy, logging_mutex)
@follows(task3)
def task4(infiles, outfiles, *extra_params):
    """
    Fourth task
    """
    test_job_io(infiles, outfiles, extra_params)


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    try:
        if options.just_print:
            pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks,
                              verbose=options.verbose,
                              gnu_make_maximal_rebuild_mode=not options.minimal_rebuild_mode,
                              pipeline="main")

        elif options.dependency_file:
            pipeline_printout_graph(open(options.dependency_file, "w"),
                                    options.dependency_graph_format,
                                    options.target_tasks,
                                    options.forced_tasks,
                                    draw_vertically=not options.draw_horizontally,
                                    gnu_make_maximal_rebuild_mode=not options.minimal_rebuild_mode,
                                    no_key_legend=options.no_key_legend_in_graph,
                                    pipeline="main")
        else:
            pipeline_run(options.target_tasks, options.forced_tasks, multiprocess=options.jobs,
                         gnu_make_maximal_rebuild_mode=not options.minimal_rebuild_mode,
                         verbose=options.verbose,
                         logger=logger_proxy,
                         pipeline="main")
    except Exception as e:
        print(e.args)
