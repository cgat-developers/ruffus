#!/usr/bin/env python
"""

    branching.py
    
        test branching dependencies

"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys, os
import os.path
import StringIO
import re

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__




parser = OptionParser(version="%prog 1.0")
parser.add_option("-D", "--debug", dest="debug",
                    action="store_true", default=False,
                    help="Make sure output is correct and clean up.")
parser.add_option("-t", "--target_tasks", dest="target_tasks",
                  action="append",
                  default = list(),
                  metavar="JOBNAME", 
                  type="string",
                  help="Target task(s) of pipeline.")
parser.add_option("-f", "--forced_tasks", dest="forced_tasks",
                  action="append",
                  default = list(),
                  metavar="JOBNAME", 
                  type="string",
                  help="Pipeline task(s) which will be included even if they are up to date.")
parser.add_option("-j", "--jobs", dest="jobs",
                  default=1,
                  metavar="jobs", 
                  type="int",
                  help="Specifies  the number of jobs (commands) to run simultaneously.")
parser.add_option("-v", "--verbose", dest = "verbose",
                  action="store_true", default=False,
                  help="Do not echo to shell but only print to log.")
parser.add_option("-d", "--dependency", dest="dependency_file",
                  #default="simple.svg",
                  metavar="FILE", 
                  type="string",
                  help="Print a dependency graph of the pipeline that would be executed "
                        "to FILE, but do not execute it.")
parser.add_option("-F", "--dependency_graph_format", dest="dependency_graph_format",
                  metavar="FORMAT", 
                  type="string",
                  default = 'svg',
                  help="format of dependency graph file. Can be 'ps' (PostScript), "+
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

parameters = [  
                ]







#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import StringIO
import re
import operator
import sys,os
from collections import defaultdict
import random

sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import time
def test_job_io(infiles, outfiles, extra_params):
    """
    cat input files content to output files
        after writing out job parameters
    """
    # dump parameters
    params = (infiles, outfiles) + extra_params
    
    if isinstance(infiles, str):
        infiles = [infiles]
    elif infiles == None:
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
    time.sleep(random.random() * 0.25)

    

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888





# get help string
f =StringIO.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
(options, remaining_args) = parser.parse_args()





#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#   1   ->  2   ->  3   ->    
#       ->  4           ->
#                   5   ->    6
# 

tempdir = "temp_branching_dir/"
#
#    task1
#
@files(None, [tempdir + d for d in 'a.1', 'b.1', 'c.1'])
@follows(mkdir(tempdir))
@posttask(lambda: open(tempdir + "task.done", "a").write("Task 1 Done\n"))
def task1(infiles, outfiles, *extra_params):
    """
    First task
    """
    open(tempdir + "jobs.start",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    open(tempdir + "jobs.finish",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))



#
#    task2
#
@files_re(tempdir + '*.1', '(.*).1', r'\1.1', r'\1.2')
@follows(task1)
@posttask(lambda: open(tempdir + "task.done", "a").write("Task 2 Done\n"))
def task2(infiles, outfiles, *extra_params):
    """
    Second task
    """
    open(tempdir + "jobs.start",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    open(tempdir + "jobs.finish",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))



#
#    task3
#
@files_re(tempdir + '*.1', '(.*).1', r'\1.2', r'\1.3')
@follows(task2)
@posttask(lambda: open(tempdir + "task.done", "a").write("Task 3 Done\n"))
def task3(infiles, outfiles, *extra_params):
    """
    Third task
    """
    open(tempdir + "jobs.start",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    open(tempdir + "jobs.finish",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))



#
#    task4
#
@files_re(tempdir + '*.1', '(.*).1', r'\1.1', r'\1.4')
@follows(task1)
@posttask(lambda: open(tempdir + "task.done", "a").write("Task 4 Done\n"))
def task4(infiles, outfiles, *extra_params):
    """
    Fourth task
    """
    open(tempdir + "jobs.start",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    open(tempdir + "jobs.finish",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))

#
#    task5
#
@files(None, tempdir + 'a.5')
@follows(mkdir(tempdir))
@posttask(lambda: open(tempdir + "task.done", "a").write("Task 5 Done\n"))
def task5(infiles, outfiles, *extra_params):
    """
    Fifth task is extra slow
    """
    open(tempdir + "jobs.start",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    time.sleep(random.random() * 3)
    open(tempdir + "jobs.finish",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))
    
#
#    task6
#
@files([[[tempdir + d for d in 'a.3', 'b.3', 'c.3', 'a.4', 'b.4', 'c.4', 'a.5'], tempdir + 'final.6']])
@follows(task3, task4, task5, )
@posttask(lambda: open(tempdir + "task.done", "a").write("Task 6 Done\n"))
def task6(infiles, outfiles, *extra_params):
    """
    final task
    """
    open(tempdir + "jobs.start",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    open(tempdir + "jobs.finish",  "a").write('job = %s\n' % json.dumps([infiles, outfiles]))
    
    
    
    
    
def check_job_order_correct(filename):
    """
       1   ->  2   ->  3   ->    
           ->  4           ->
                       5   ->    6
    """
    
    precedence_rules = [[1, 2],
                        [2, 3],
                        [1, 4],
                        [5, 6],
                        [3, 6],
                        [4, 6]]
    
    index_re = re.compile(r'.*\.([0-9])["\]\n]*$')
    job_indices = defaultdict(list)
    for linenum, l in enumerate(open(filename)):
        m = index_re.search(l)
        if not m:
            raise "Non-matching line in [%s]" % filename
        job_indices[int(m.group(1))].append(linenum)
        
    for job_index in job_indices:
        job_indices[job_index].sort()
        
    for before, after in precedence_rules:
        if job_indices[before][-1] >= job_indices[after][0]:
            raise ("Precedence violated for job %d [line %d] and job %d [line %d] of [%s]"
                                % ( before, job_indices[before][-1],
                                    after,  job_indices[after][0],
                                    filename))
        
    
    
def check_final_output_correct():
    """
    check if the final output in final.6 is as expected
    """
    expected_output = \
"""        ["DIR/a.1"] -> ["DIR/a.2"]
        ["DIR/a.1"] -> ["DIR/a.4"]
        ["DIR/a.2"] -> ["DIR/a.3"]
        ["DIR/a.3", "DIR/b.3", "DIR/c.3", "DIR/a.4", "DIR/b.4", "DIR/c.4", "DIR/a.5"] -> ["DIR/final.6"]
        ["DIR/b.1"] -> ["DIR/b.2"]
        ["DIR/b.1"] -> ["DIR/b.4"]
        ["DIR/b.2"] -> ["DIR/b.3"]
        ["DIR/c.1"] -> ["DIR/c.2"]
        ["DIR/c.1"] -> ["DIR/c.4"]
        ["DIR/c.2"] -> ["DIR/c.3"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.5"]"""
    expected_output = expected_output.replace("        ", "").replace("DIR/", tempdir).split("\n")
    final_6_contents = sorted([l.rstrip() for l in open(tempdir + "final.6", "r").readlines()])
    if final_6_contents != expected_output:
        for i, (l1, l2) in enumerate(zip(final_6_contents, expected_output)):
            if l1 != l2:
                sys.stderr.write("%d\n  >%s<\n  >%s<\n" % (i, l1, l2))
        raise Exception ("Final.6 output is not as expected\n")
    
        
# 
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    if options.just_print:
        pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks, 
                            long_winded=True, 
                            gnu_make_maximal_rebuild_mode = not options.minimal_rebuild_mode)
    
    elif options.dependency_file:
        pipeline_printout_graph (     open(options.dependency_file, "w"),
                             options.dependency_graph_format,
                             options.target_tasks, 
                             options.forced_tasks,
                             draw_vertically = not options.draw_horizontally,
                             gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                             no_key_legend  = options.no_key_legend_in_graph)
    elif options.debug:    
        import os
        os.system("rm -rf %s" % tempdir)
        pipeline_run(options.target_tasks, options.forced_tasks, multiprocess = options.jobs, 
                            gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode)
        
        check_final_output_correct()
        check_job_order_correct(tempdir + "jobs.start")
        check_job_order_correct(tempdir + "jobs.finish")
        os.system("rm -rf %s" % tempdir)
        print "Done"
    else:
        pipeline_run(options.target_tasks, options.forced_tasks, multiprocess = options.jobs, 
                            gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode)

