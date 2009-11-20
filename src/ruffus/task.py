#!/usr/bin/env python
################################################################################
#
# 
#   task.py
#
#   Copyright (c) 10/9/2009 Leo Goodstadt
#   
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.
#################################################################################
"""

********************************************
:mod:`ruffus.task` -- Overview
********************************************

.. moduleauthor:: Leo Goodstadt <ruffus@llew.org.uk>


============================
Decorator syntax:
============================

    Pipelined tasks are created by "decorating" a function with the following syntax::
    
        def func_a():
            pass
            
        @follows(func_a)
        def func_b ():
            pass
                
    
    Each task is a single function which is applied one or more times to a list of parameters
    (typically input files to produce a list of output files).
    
    Each of these is a separate, independent job (sharing the same code) which can be
    run in parallel.
        

============================
Running the pipeline
============================
    To run the pipeline::
    
            pipeline_run(target_tasks, forcedtorun_tasks = [], multiprocess = 1, 
                            logger = stderr_logger,
                            gnu_make_maximal_rebuild_mode  = True,
                            cleanup_log = "../cleanup.log")

            pipeline_cleanup(cleanup_log = "../cleanup.log")
        
        

           
    

"""


import os,sys,copy, multiprocessing
from collections import namedtuple

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
import logging
import re
from collections import defaultdict
from multiprocessing import Pool
import traceback
import types
from itertools import imap 
import textwrap


if __name__ == '__main__':
    import sys
    sys.path.insert(0,".")

from graph import *
from print_dependencies import *
from ruffus_exceptions import  *
from ruffus_utility import *
from file_name_parameters import  *


# 
# use simplejson in place of json for python < 2.6
# 
try:
    import json
except ImportError:
    import simplejson
    json = simplejson
dumps = json.dumps

import Queue
Queue = Queue.Queue


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
#   light weight logging objects
# 
#     
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class t_black_hole_logger:
    """
    Does nothing!
    """
    def info (self, message):
        pass
    def debug (self, message):
        pass


class t_stderr_logger:
    """
    Everything to stderr
    """
    def info (self, message):
        sys.stderr.write(message + "\n")
    def debug (self, message):
        sys.stderr.write(message + "\n")

class t_stream_logger:
    """
    Everything to stderr
    """
    def __init__ (self, stream):
        self.stream = stream
    def info (self, message):
        self.stream.write(message + "\n")
    def debug (self, message):
        self.stream.write(message + "\n")

black_hole_logger = t_black_hole_logger()
stderr_logger     = t_stderr_logger()

class t_verbose_logger:
    def __init__ (self, verbose, logger):
        self.verbose = verbose
        self.logger = logger

#_________________________________________________________________________________________
#
#   logging helper function
#
#________________________________________________________________________________________ 
def log_at_level (logger, message_level, verbose_level, msg):
    """
    writes to log if message_level > verbose level 
    """
    if message_level <= verbose_level:
        logger.info(msg)

        


    
    
    
    
    
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#   queue management objects

#       inserted into queue like job parameters to control multi-processing queue

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

# fake parameters to signal in queue
class all_tasks_complete:
    pass

class waiting_for_more_tasks_to_complete:
    pass

    
        
    
    
    
    
    
    
        
        
        

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   task_decorator

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class task_decorator(object):
    """
        Adds task to the "pipeline_task" attribute of this function but
        otherwise leaves function untouched
    """
    def __init__(self, *decoratorArgs):
        """
            saves decorator arguments
        """
        self.args = decoratorArgs

    def __call__(self, func):
        """
            calls func in task with the same name as the class
        """
        # add task as attribute of this function
        if not hasattr(func, "pipeline_task"):
            func.pipeline_task = _task.create_task(func)


        # call the method called  
        #   "task.task_decorator" 
        #   where "task_decorator" is the name of this class
        decorator_function_name = "task_" + self.__class__.__name__
        task_decorator_function = getattr(func.pipeline_task, decorator_function_name)
        task_decorator_function(self.args)

        #
        #   don't change the function so we can call it unaltered
        # 
        return func


#
#   Basic decorators 
#
class follows(task_decorator):
    pass
    
class files(task_decorator):
    pass
    

    
    
#
#   Core
#
class split(task_decorator):
    pass

class transform(task_decorator):
    pass
    
class merge(task_decorator):
    pass
    
class posttask(task_decorator):
    pass

    
    
#
#   Advanced
#
class collate(task_decorator):
    pass
    
#
#   Esoteric
#     
class check_if_uptodate(task_decorator):
    pass
    
class parallel(task_decorator):
    pass
    
     
#
#   Obsolete
#     
class files_re(task_decorator):
    pass

        
        
        

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   indicator objects

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#_________________________________________________________________________________________

#   mkdir

#_________________________________________________________________________________________
class mkdir(object):
    def __init__ (self, *args):
        self.args = args

#_________________________________________________________________________________________

#   touch_file

#_________________________________________________________________________________________
class touch_file(object):
    def __init__ (self, *args):
        self.args = args
        


#_________________________________________________________________________________________

#   inputs

#_________________________________________________________________________________________
class inputs(object):
    def __init__ (self, *args):
        self.args = args

#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#       job descriptors

#           given parameters, returns string describing job
#           main use in error logging

#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888
def generic_job_descriptor (param):
    if param in ([], None):
        return "Job"
    else:
        return "Job = %s" % ignore_unknown_encoder(param)

def io_files_job_descriptor (param):
    # input, output
    if len(param) >= 2:
        extra_param = "" if len(param) == 2 else ", " + shorten_filenames_encoder(param[2:])[1:-1]
        return ("Job = [%s -> %s%s]" % (shorten_filenames_encoder(param[0]),
                                        shorten_filenames_encoder(param[1]),
                                        extra_param))
    elif len(param) == 0:
            return "JOb = [ ?? -> ?? ]"
    else:
        return ("Job = [%s -> ??]" % (shorten_filenames_encoder(param[0])))    
    
    
def split_job_descriptor_factory (output_files):
    def io_files_job_descriptor (param):
        # input, output
        extra_param = "" if len(param) == 2 else ", " + shorten_filenames_encoder(param[2:])[1:-1]
        return ("Job = [%s -> %s%s]" % (shorten_filenames_encoder(param[0]),
                                        shorten_filenames_encoder(output_files),
                                        extra_param))
    return io_files_job_descriptor

def mkdir_job_descriptor (param):
    # input, output and parameters
    return "Make directories %s" % (shorten_filenames_encoder(param[0]))


#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#       job wrappers
#           registers files/directories for cleanup    

#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#_________________________________________________________________________________________

#   generic job wrapper

#_________________________________________________________________________________________
def job_wrapper_generic(param, user_defined_work_func, register_cleanup):
    """
    run func
    """
    assert(user_defined_work_func)
    return user_defined_work_func(*param)

#_________________________________________________________________________________________

#   job wrapper for all that deal with i/o files

#_________________________________________________________________________________________
def job_wrapper_io_files(param, user_defined_work_func, register_cleanup):
    """
    run func on any i/o if not up to date
    """
    assert(user_defined_work_func)

    ret_val = user_defined_work_func(*param)
    #if ret_val == False:
    #    return False

    i,o = param[0:2]

    #
    # register output file for cleanup
    #
    if o == None:
        return
    elif isinstance(o, str):
        register_cleanup(o, "file")
    else:
        for f in o:
            register_cleanup(f, "file")


#_________________________________________________________________________________________

#   job wrapper for mkdir

#_________________________________________________________________________________________
def job_wrapper_mkdir(param, user_defined_work_func, register_cleanup):
    """
    make directories if not exists
    """
    #
    #   Just in case, swallow file exist errors because some other makedirs might be subpath 
    #       of this directory
    #   Should not be necessary because of "sorted" in task_mkdir
    #   
    #
    for d in param[0]:
        try:
            os.makedirs(d)
            register_cleanup(d, "makedirs")
        except OSError, e:
            if "File exists" not in e:
                raise


JOB_ERROR           = 0
JOB_SIGNALLED_BREAK = 1
JOB_UP_TO_DATE      = 2
JOB_COMPLETED       = 3
t_job_result = namedtuple('t_job_result', 'task_name state job_name return_value exception')

        
#_________________________________________________________________________________________

#   multiprocess_callback 
# 
#_________________________________________________________________________________________
def run_pooled_job_without_exceptions (process_parameters):
    """
    handles running jobs in parallel
    Make sure exceptions are caught here: 
        Otherwise, these will kill the thread/process
        return any exceptions which will be rethrown at the other end:
        See RethrownJobError /  run_all_jobs_in_task
    """
    
    (param, task_name, job_name, job_wrapper, user_defined_work_func) = process_parameters
    
    try:

        # if user return false, halt job
        return_value =  job_wrapper(param, user_defined_work_func, register_cleanup)
        return t_job_result(task_name, JOB_COMPLETED, job_name, return_value, None)
    except:
        #   Wrap up one or more exceptions rethrown across process boundaries
        #   
        #       See multiprocessor.Server.handle_request/serve_client for an analogous function
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        exception_stack  = traceback.format_exc(exceptionTraceback)
        exception_name   = exceptionType.__module__ + '.' + exceptionType.__name__
        exception_value  = str(exceptionValue)
        if len(exception_value):
            exception_value = "(%s)" % exception_value
        return t_job_result(task_name, JOB_ERROR, job_name, None,
                            [task_name,
                             job_name, 
                             exception_name, 
                             exception_value, 
                             exception_stack])
        
        
        
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Helper function

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#_________________________________________________________________________________________

#   register_cleanup

#       to do

#_________________________________________________________________________________________
def register_cleanup (file_name, operation):
    pass

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   _task

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class _task (node):
    """
    pipeline task
    """

    action_names = ["unspecified",
                    "task",
                    "task_files_re",
                    "task_split",
                    "task_merge",
                    "task_transform",
                    "task_collate",
                    "task_files_func",
                    "task_files",
                    "task_mkdir",
                    "task_parallel",
                    ]
    action_unspecified      = 0
    action_task             = 1
    action_task_files_re    = 2
    action_task_split       = 3
    action_task_merge       = 4
    action_task_transform   = 5
    action_task_collate     = 6
    action_task_files_func  = 7
    action_task_files       = 8
    action_mkdir            = 9
    action_parallel         = 10
    
    multiple_jobs_outputs    = 0
    single_job_single_output = 1
    job_single_matches_parent= 2

    #_________________________________________________________________________________________

    #   create_task / __init__

    #_________________________________________________________________________________________
    @staticmethod
    def create_task(func):
        """
        Create task if the name as not been previously specified
        Note that the task function may not have been created yet.
        This allows us to create tasks and dependencies out of order
        """
        func_name   = func.__name__
        module_name = func.__module__
        task_name   = module_name + "." + func_name
    
        # Link to existing dependency if task name has previously been specified
        if node.is_node(task_name):
            t = node.lookup_node_from_name(task_name)
            if t.user_defined_work_func != None:
                raise error_duplicate_task_name("Same task name %s specified multiple times in the same module" % task_name)
        #   otherwise create new
        else:
            t = _task(module_name, func_name)

        t.set_action_type (_task.action_task)
        t.user_defined_work_func = func
        assert(t._name == task_name)
        t._description           = func.__doc__ or ""
        t._description = t._description.strip()

        return t

    #_________________________________________________________________________________________

    #   get_action_name

    #_________________________________________________________________________________________
    def get_action_name (self):
        return _task.action_mkdir[self._action_type]

    #_________________________________________________________________________________________

    #   __init__

    #_________________________________________________________________________________________
    def __init__ (self, module_name, func_name):
        """
        Does nothing because this might just be a dependency.
        If it does not get initialised by a real task 
            (a task is depending on an unknown function/task), 
            throw an exception when running the pipeline

        """
        self._module_name = module_name
        self._func_name   = func_name
        
        node.__init__ (self, module_name + "." + func_name)
        self._action_type  = _task.action_unspecified
        
        
        
        self.param_generator_func   = None
        self.needs_update_func      = None
        self.job_wrapper            = job_wrapper_generic
        
        # 
        self.job_descriptor         = generic_job_descriptor
        
        # jobs which produce a single output. 
        # special handling for task.get_output_files for dependency chaining
        self._single_job_single_output = self.multiple_jobs_outputs

        # function which is decorated and does the actual work
        self.user_defined_work_func = None
        
        # functions which will be called when task completes
        self.posttask_functions    = []
                
        # give makedir automatically made parent tasks unique names
        self.cnt_task_mkdir         = 0
        
        # whether only task function itself knows what output it will produce
        # i.e. output is a glob or something similar
        self.indeterminate_output   = False
        
        # cache output file names here
        self.output_filenames = None

    #_________________________________________________________________________________________

    #   init_for_pipeline

    #_________________________________________________________________________________________
    def init_for_pipeline (self):
        """
        Initialize variables for pipeline run / printout

        **********
          BEWARE
        **********

        Because state is stored, ruffus is *not* reentrant.

        **********
          BEWARE
        **********
        """

        # cache output file names here
        self.output_filenames = None
        
        
    #_________________________________________________________________________________________

    #   set_action_type

    #_________________________________________________________________________________________
    def set_action_type (self, new_action_type):
        """
        Save how this task 
            1) tests whether it is up-to-date and 
            2) handles input/output files

        Checks that the task has not been defined with conflicting actions    
            
        """
        if self._action_type not in (_task.action_unspecified, _task.action_task):
            old_action = _task.action_names[self._action_type]
            new_action = _task.action_names[new_action_type]
            actions = " and ".join(list(set((old_action, new_action))))
            task_name = "def %s(...)" % self._name.replace("__main__.", "")
            raise error_decorator_args(("    %s\n      has duplicate task specifications: (%s)\n") % 
                                        (task_name, actions))
        self._action_type = new_action_type
        #
        #   DEBUGG
        # 
        self._action_type_desc = _task.action_names[new_action_type]


    #_________________________________________________________________________________________

    #   printout

    #_________________________________________________________________________________________
    def printout (self, force_rerun, verbose=1, indent = 4):
        """
        Print out all jobs for this task
        
                verbose = 1 : print task name
                          2 : print task description if exists
                          3 : print job names for jobs to be run
                          4 : print job names for up-to- date jobs
        """
        
        def get_job_names (param, indent_str):
            job_names = (indent_str + self.job_descriptor(param)).split("-> ")
            if job_names[1]:
                job_names[1] = indent_str + "      ->" + job_names[1]
            return job_names

            #   
            #   needs update func = None: always needs update
            #
            if not self.needs_update_func:
                messages.append(indent_str + job_name + "")
            
            
        
        if not verbose:
            return []
            
        indent_str = ' ' * indent
        
        messages = []
        
        task_name = self._name.replace("__main__.", "")
        messages.append("Task = " + task_name + ("    >>Forced to rerun<<" if force_rerun else ""))
        if verbose ==1:
            return messages
            
        if verbose >= 2 and len(self._description):
            messages.append(indent_str + '"' + self._description + '"')

        #
        #   single job state
        # 
        if verbose > 5:
            if self._single_job_single_output == self.single_job_single_output:
                messages.append("    Single job single output")
            elif self._single_job_single_output == self.multiple_jobs_outputs:
                messages.append("    Multiple jobs Multiple outputs")
            else:
                messages.append("    Single jobs status depends on %s" % self._single_job_single_output._name)


        if verbose <= 2 :
            return messages

        # increase indent for jobs up to date status
        indent_str += " " * 3
        
        #
        #   No parameters: just call task function 
        #
        if self.param_generator_func == None:
            if verbose <= 3:
                return messages
                
            #   
            #   needs update func = None: always needs update
            #
            if not self.needs_update_func:
                messages.append(indent_str + "Task needs update: No function to check if up-to-date or not")
                return messages
                
            needs_update, msg = self.needs_update_func ()
            if needs_update:
                messages.append(indent_str + "Task needs update: %s" % msg)
            else:
                messages.append(indent_str + "Task up-to-date")

        else:
            #
            #   return messages description per job
            # 
            for param in self.param_generator_func():
                job_name = self.job_descriptor(param)
                job_name = job_name.replace("->", indent_str + " " * 7 +  "\n->")
                    
                #   
                #   needs update func = None: always needs update
                #
                if not self.needs_update_func:
                    messages.extend(get_job_names (param, indent_str))
                    messages.append(indent_str + "  Jobs needs update: No function to check if up-to-date or not")
                    continue

                needs_update, msg = self.needs_update_func (*param)
                if needs_update:
                    messages.extend(get_job_names (param, indent_str))
                    messages.append(indent_str + "  Job needs update: %s" % msg)
                else:
                    if verbose > 4:
                        messages.extend(get_job_names (param, indent_str))
                        messages.append(indent_str + "  Job up-to-date")
        messages.append("")
        return messages

    


    #_____________________________________________________________________________________

    #   signal
    # 
    #       returns whether up to date
    # 
    #_____________________________________________________________________________________
    def signal (self, verbose_logger):
        """
        If up to date: signal = true
        If true, depth first search will not pass through this node
        """
        try:
            logger  = verbose_logger.logger  if verbose_logger else None
            verbose = verbose_logger.verbose if verbose_logger else 0
            short_task_name = self._name.replace('__main__.', '')
            log_at_level (logger, 4, verbose, 
                            "  Task = " + short_task_name)

            #
            #   Always needs update if no way to check if up to date
            #
            if self.needs_update_func == None:
                log_at_level (logger, 4, verbose, 
                                "    No update function: treat as out of date")
                return False
                
            #
            #   if no parameters, just return the results of needs update
            # 
            if self.param_generator_func == None:
                if self.needs_update_func:
                    needs_update, msg = self.needs_update_func ()
                    log_at_level (logger, 4, verbose, 
                                    "    Needs update = %s" % needs_update)
                    return not needs_update
                else:
                    return True
            else:
                #
                #   return not up to date if ANY jobs needs update
                # 
                for param in self.param_generator_func():
                    needs_update, msg = self.needs_update_func (*param)
                    if needs_update:
                        if verbose >= 4:
                            job_name = self.job_descriptor(param)
                            log_at_level (logger, 4, verbose, 
                                            "    Job needing update = %s" % job_name)
                        return False
                log_at_level (logger, 4, verbose, 
                                "    All jobs up to date")
                return True
                
        # rethrow exception after adding task name
        except error_task, inst:
            inst.specify_task(self, "Exceptions in dependency checking")
            raise


        
        
    #_____________________________________________________________________________________

    #   get_output_files
    # 
    # 
    #_____________________________________________________________________________________
    def get_output_files (self, do_not_expand_single_job_tasks = False):
        """
        Cache output files
        
            If flattened is True, returns file as a list of strints, 
                flattening any nested structures and discarding non string names
            Normally returns a list with one item for each job or a just a list of file names.
            For "single_job_single_output" i.e. @merge and @files with single jobs,
                returns the output of a single job (i.e. can be a string)
        """
        #
        #   This looks like the wrong place to flatten 
        #
        flattened = False
        if self.output_filenames == None:
            
            self.output_filenames = []

            # skip tasks which don't have parameters
            if self.param_generator_func != None:

                cnt_jobs = 0
                for param in self.param_generator_func():
    
                    cnt_jobs += 1
                    # skip tasks which don't have output parameters
                    if len(param) >= 2:
                        self.output_filenames.append(param[1])

                if self._single_job_single_output == self.single_job_single_output:
                    if cnt_jobs > 1:
                        raise error_task_get_output(this, 
                               "Task which is supposed to produce a single output "
                               "somehow has more than one job.")

                # the output of split should be treated as multiple jobs
                if self.indeterminate_output:
                    self.output_filenames = self.output_filenames[0]
    
        if flattened:
            # if single file name, return that
            if (do_not_expand_single_job_tasks and 
                len(self.output_filenames) and 
                isinstance(self.output_filenames[0], str)):
                return self.output_filenames
            # if it is flattened, might as well sort it
            return sorted(get_strings_in_nested_sequence(self.output_filenames))
                
        else:
            # special handling for jobs which have a single task, 
            if (do_not_expand_single_job_tasks and 
                self._single_job_single_output and
                len(self.output_filenames) ):
                return self.output_filenames[0]

            # 
            # sort by jobs so it is just a weeny little bit less deterministic
            #
            return sorted(self.output_filenames)

        

    #_____________________________________________________________________________________

    #   completed
    # 
    # 
    #_____________________________________________________________________________________
    def completed (self, logger, jobs_uptodate = False):
        """
        called even when all jobs are up to date
        """
        for f in self.posttask_functions:
            f()
        short_task_name = self._name.replace('__main__.', '')
        if jobs_uptodate:
            logger.info("Uptodate Task = " + short_task_name)
        else:
            logger.info("Completed Task = " + short_task_name)
            

        #
        #   indeterminate output. Check actual output again if someother tasks job function depend on it
        #       used for @split
        #
        if self.indeterminate_output:
            self.output_filenames = None
            
            
            
            
            
    #_________________________________________________________________________________________

    #   handle_tasks_globs_in_inputs

    #_________________________________________________________________________________________
    def handle_tasks_globs_in_inputs(self, input_params):
        """
        Helper function for tasks which 
            1) Notes globs and tasks
            2) Replaces tasks names and functions with actual tasks
            3) Adds task dependencies automatically via task_follows
        """
        # 
        # get list of function/function names and globs
        # 
        function_or_func_names, globs = get_nested_tasks_or_globs(input_params)

        # 
        # replace function / function names with tasks
        # 
        tasks = self.task_follows(function_or_func_names)
        functions_to_tasks = dict(zip(function_or_func_names, tasks))
        input_params = replace_func_names_with_tasks(input_params, functions_to_tasks)
        
        return tasks, globs, input_params
            
            
            
            
            
    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

    #       task handlers
    
    #         sets 
    #               1) action_type
    #               2) param_generator_func
    #               3) needs_update_func
    #               4) job wrapper


    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        
    #_________________________________________________________________________________________

    #   task_split

    #_________________________________________________________________________________________
    def task_split (self, orig_args):
        """
        Splits a single set of input files into multiple output file names, 
            where the number of output files may not be known beforehand.
        """
        #check enough arguments
        if len(orig_args) < 2:
            raise error_task_split(self, "Too few arguments for @split")

        self.set_action_type (_task.action_task_split)

        # 
        # replace function / function names with tasks
        # 
        tasks, globs, input_params = self.handle_tasks_globs_in_inputs(orig_args[0])
        output_tasks, output_globs, output_params = self.handle_tasks_globs_in_inputs(orig_args[1])
        if len(output_tasks):
            raise error_task_split(self, "@split cannot output to another task. "
                                            "Do not include tasks in output parameters.")
        
        extra_params = orig_args[1:]
        self.param_generator_func = split_param_factory (tasks, globs, input_params, output_globs, *extra_params)


        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = split_job_descriptor_factory (orig_args[1])

        # output is a glob
        self.indeterminate_output = True

    #_________________________________________________________________________________________

    #   task_transform

    #_________________________________________________________________________________________
    def task_transform (self, orig_args):
        """
        Merges multiple input files into a single output.
        """
        #
        #   check enough arguments
        #
        if (len(orig_args) < 3 or         
            (isinstance(orig_args[2], inputs) and len(orig_args) < 4)):
            raise error_task_transform(self, "Too few arguments for @transform")



        self.set_action_type (_task.action_task_transform)

        # 
        # replace function / function names with tasks
        # 
        tasks, globs, input_param = self.handle_tasks_globs_in_inputs(orig_args[0])

        
        # regular expression match
        if isinstance(orig_args[1], regex):
            matching_regex = compile_regex(self, orig_args[1], error_task_transform, "@transform")
            regex_substitute_extra_parameters = True
            
        # simulate end of string (suffix) match
        elif isinstance(orig_args[1], suffix):
            matching_regex = compile_suffix(self, orig_args[1], error_task_transform, "@transform")
            regex_substitute_extra_parameters = False

        else:
            raise error_task_transform(self, "@transform expects suffix() or "
                                                            "regex() as the second argument")
            
        
        #
        #   inputs also defined by pattern match
        #         
        if isinstance(orig_args[2], inputs):
            input_pattern = orig_args[2].args[0]
            output_pattern_extras = orig_args[3:]
        else:
            input_pattern = None
            output_pattern_extras = orig_args[2:]
            
        #
        #   allows transform to take a single file or task
        #             
        if isinstance(input_param, str):
            self._single_job_single_output = self.single_job_single_output
            input_param = [input_param]
            
        #
        #   whether transform generates a list of jobs or not will depend on the parent task
        # 
        elif isinstance(input_param, _task):
            self._single_job_single_output = input_param

        self.param_generator_func = transform_param_factory (   tasks, globs, input_param,
                                                                False, # flatten input
                                                                matching_regex, 
                                                                regex_substitute_extra_parameters,
                                                                input_pattern,
                                                                *output_pattern_extras)
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor

    #_________________________________________________________________________________________

    #   task_collate

    #_________________________________________________________________________________________
    def task_collate (self, orig_args):
        """
        Merges multiple input files into a single output.
        """
        #
        #   check enough arguments
        #
        if len(orig_args) < 3:
            raise error_task_collate(self, "Too few arguments for @collate")

        self.set_action_type (_task.action_task_collate)

        # 
        # replace function / function names with tasks
        # 
        tasks, globs, input_param = self.handle_tasks_globs_in_inputs(orig_args[0])

        
        # regular expression match
        if isinstance(orig_args[1], regex):
            matching_regex = compile_regex(self, orig_args[1], error_task_collate, "@collate")
        else:
            raise error_task_collate(self, "@collate expects regex() as the second argument")

        #
        #   inputs also defined by pattern match
        #         
        if isinstance(orig_args[2], inputs):
            input_pattern = orig_args[2].args[0]
            output_pattern_extras = orig_args[3:]
        else:
            input_pattern = None
            output_pattern_extras = orig_args[2:]

        extra_params = orig_args[2:]

        self.param_generator_func = collate_param_factory (tasks, globs, input_param, 
                                                            False, # flatten input
                                                            matching_regex, 
                                                            input_pattern,
                                                            *output_pattern_extras)
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        
        

    #_________________________________________________________________________________________

    #   task_merge

    #_________________________________________________________________________________________
    def task_merge (self, orig_args):
        """
        Merges multiple input files into a single output.
        """
        #
        #   check enough arguments
        #
        if len(orig_args) < 2:
            raise error_task_merge(self, "Too few arguments for @merge")

        self.set_action_type (_task.action_task_merge)

        # 
        # replace function / function names with tasks
        # 
        tasks, globs, input_param = self.handle_tasks_globs_in_inputs(orig_args[0])

        extra_params = orig_args[1:]
        self.param_generator_func = merge_param_factory (tasks, globs, input_param,
                                                           *extra_params)


        self._single_job_single_output = self.multiple_jobs_outputs
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor

    #_________________________________________________________________________________________

    #   task_parallel

    #_________________________________________________________________________________________
    def task_parallel (self, orig_args):
        """
        calls user function in parallel
            with either each of a list of parameters
            or using parameters generated by a custom function
        """
        self.set_action_type (_task.action_parallel)

        #   unmodified from __init__
        # 
        # self.needs_update_func      = None
        # self.job_wrapper          = job_wrapper_generic
        # self.job_descriptor       = io_files_job_descriptor

        if len(orig_args) == 0:
            raise error_task_parallel(self, "Too few arguments for @parallel")

        #   Use parameters generated by a custom function
        if len(orig_args) == 1 and type(orig_args[0]) == types.FunctionType:
            self.param_generator_func = orig_args[0]

        # list of  params 
        else:
            if len(orig_args) > 1:
                # single jobs
                params = copy.copy([orig_args])
                self._single_job_single_output = self.single_job_single_output
            else:
                # multiple jobs with input/output parameters etc.
                params = copy.copy(orig_args[0])
                check_parallel_parameters (self, params, error_task_parallel)

            self.param_generator_func = args_param_factory (params)



    #_________________________________________________________________________________________

    #   task_files

    #_________________________________________________________________________________________
    def task_files (self, orig_args):
        """
        calls user function in parallel
            with either each of a list of parameters
            or using parameters generated by a custom function
            
            In the parameter list,
                The first two items of each set of parameters must 
                be input/output files or lists of files or Null
        """
        
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor

        if len(orig_args) == 0:
            raise error_task_files(self, "Too few arguments for @files")

        #   Use parameters generated by a custom function
        if len(orig_args) == 1 and type(orig_args[0]) == types.FunctionType:
            self.set_action_type (_task.action_task_files_func)
            self.param_generator_func = orig_args[0]

        #   Use parameters in supplied list
        else:
            self.set_action_type (_task.action_task_files)

            if len(orig_args) > 1:

                # single jobs
                params = copy.copy([orig_args])
                self._single_job_single_output = self.single_job_single_output
            else:

                # multiple jobs with input/output parameters etc.
                params = copy.copy(orig_args[0])
                self._single_job_single_output = self.multiple_jobs_outputs

            check_files_io_parameters (self, params, error_task_files)
            
            # 
            # get list of function/function names and globs for all job params
            # 
            function_or_func_names, globs = set(), set()
            input_params = []
            for j in params:
                func1job, glob1job = get_nested_tasks_or_globs(j[0])
                function_or_func_names |= func1job
                globs                  |= glob1job
                input_params.append(j[0])

            # 
            # replace function / function names with tasks
            # 
            tasks = self.task_follows(function_or_func_names)
            functions_to_tasks = dict(zip(function_or_func_names, tasks))
            input_params = [replace_func_names_with_tasks(i, functions_to_tasks) 
                                                            for i in input_params]

            #
            #   extra params 
            #
            output_extra_params = [tuple(j[1:]) for j in params]
                
            self.param_generator_func = files_param_factory (tasks, globs, input_params,
                                                             False, # flatten input
                                                             True,  # do_not_expand_single_job_tasks
                                                             output_extra_params)
                                                             
            

    #_________________________________________________________________________________________

    #   task_files_re

    #_________________________________________________________________________________________
    def task_files_re (self, old_args):
        """
        calls user function in parallel
            with input_files, output_files, parameters
            These needed to be generated on the fly by 
                getting all file names in the supplied list/glob pattern
            There are two variations:

            1)    inputfiles = all files in glob which match the regular expression
                  outputfile = generated from the replacement string

            2)    inputfiles = all files in glob which match the regular expression and
                                          generated from the "from" replacement string
                  outputfiles = all files in glob which match the regular expression and
                                          generated from the "to" replacement string
        """
        #
        #   check enough arguments
        #
        if len(old_args) < 3:
            raise error_task_files_re(self, "Too few arguments for @files_re")
            
        self.set_action_type (_task.action_task_files_re)

        # check if parameters wrapped in combine
        combining_all_jobs, orig_args = is_file_re_combining(old_args)

        # 
        # replace function / function names with tasks
        # 
        tasks, globs, input_param = self.handle_tasks_globs_in_inputs(orig_args[0])

        matching_regex = compile_regex(self, regex(orig_args[1]), error_task_files_re, "@files_re")

        # if the input file term is missing, just use the original
        if len(orig_args) == 3:
            input_pattern = None
            output_and_extras = [orig_args[2]]
        else:
            input_pattern = orig_args[2]
            output_and_extras = orig_args[3:]


        if combining_all_jobs:
            self.param_generator_func = collate_param_factory (tasks, globs, input_param, 
                                                                False,                  # flatten
                                                                matching_regex,
                                                                input_pattern, 
                                                                *output_and_extras)
        else:

            self.param_generator_func = transform_param_factory (tasks, globs, input_param, 
                                                                    False,              # flatten
                                                                    matching_regex, 
                                                                    True,               # substitute all parameters
                                                                    input_pattern, 
                                                                    *output_and_extras)
            
            
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor

    

    #_________________________________________________________________________________________

    #   task_mkdir
    
    #       only called within task_follows
    
    #_________________________________________________________________________________________
    def task_mkdir (self, orig_args):
        """
        list of directory names or a single argument which is aa list of directory names
        Creates directory if missing
        """
        #   jump through hoops 
        self.set_action_type (_task.action_mkdir)
        
        # the mkdir decorator accepts one string, multiple strings or a list of strings
        # convert everything into the multiple strings format
        if not isinstance(orig_args[0], str):
            orig_args = orig_args[0]
        #   all directories created in one job to reduce race conditions
        #    so we are converting [a,b,c] into [   [(a, b,c)]   ]
        #    where orig_args = (a,b,c)
        #   i.e. one job whose solitory argument is a tuple/list of directory names
        param_func                = args_param_factory([[sorted(orig_args)]])
        
        #print >>sys.stderr, dumps(list(param_func()), indent = 4) # DEBUG
        
        self.param_generator_func = param_func
        self._description         = "Make directories %s" % (shorten_filenames_encoder(orig_args))
        self.needs_update_func    = self.needs_update_func or needs_update_check_directory_missing
        self.job_wrapper          = job_wrapper_mkdir
        self.job_descriptor       = mkdir_job_descriptor

        # doesn't have a real function
        #  use job_wrapper just so it is not None
        self.user_defined_work_func = self.job_wrapper
        
        

        
        
        
    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

    #   Other task handlers



    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        
        
        
        
    
                
    #_________________________________________________________________________________________

    #   task_follows

    #_________________________________________________________________________________________
    def task_follows (self, args):
        """
        Saved decorator arguments should be:
                (string/task,...)
        """
        new_tasks = []
        for arg in args:
            #
            #   specified by string 
            #
            if isinstance(arg, str):
                # string looks up to defined task, use that
                if node.is_node(arg):
                    arg = node.lookup_node_from_name(arg)
                # string looks up to defined task in main module, use that
                elif node.is_node("__main__." + arg):
                    arg = node.lookup_node_from_name("__main__." + arg)

                # 
                # string does not look up to defined task: defer
                #
                else:    
                    #   no module: use same module as current task
                    names = arg.rsplit(".", 2)
                    if len(names) == 1:
                        arg = _task(self._module_name, arg)
                    else:
                        arg = _task(*names)

                # 
                #   add dependency
                #       duplicate dependencies are ignore automatically
                #
                self.add_child(arg)
                new_tasks.append(arg)
                
        
            #
            #   for mkdir, automatically generate task with unique name 
            #
            elif isinstance(arg, mkdir):
                self.cnt_task_mkdir += 1
                # give unique name to this instance of mkdir
                unique_name = self._name + "_mkdir_%d" % self.cnt_task_mkdir
                new_node = _task(self._module_name, unique_name)
                self.add_child(new_node)
                new_node.task_mkdir(arg.args)
                new_tasks.append(new_node)

                
                
                
            # 
            #   Is this a function?
            #       Turn this function into a task
            #           (add task as attribute of this function)
            #       Add self as dependent
            else:
                if type(arg) != types.FunctionType:
                    raise error_decorator_args("Dependencies must be functions or function names in " +
                                                "@task_follows %s:\n[%s]" %
                                                (self._name, str(arg)))
                    
                # add task as attribute of this function
                if not hasattr(arg, "pipeline_task"):
                    arg.pipeline_task = _task.create_task(arg)
                self.add_child(arg.pipeline_task)
                new_tasks.append(arg.pipeline_task)

        return new_tasks
            
            
            
    #_________________________________________________________________________________________

    #   task_check_if_uptodate

    #_________________________________________________________________________________________
    def task_check_if_uptodate (self, args):
        """
        Saved decorator arguments should be:
                a function which takes the appropriate number of arguments for each job
        """
        if len(args) != 1 or type(args[0]) != types.FunctionType:
            raise error_decorator_args("Expecting a single function in  " +
                                                "@task_check_if_uptodate %s:\n[%s]" %
                                                (self._name, str(args)))
        self.needs_update_func        = args[0]
        


    #_________________________________________________________________________________________

    #   task_check_if_uptodate

    #_________________________________________________________________________________________
    def task_posttask(self, args):
        """
        Saved decorator arguments should be:
                one or more functions which will be called if the task completes
        """
        for arg in args:
            if isinstance(arg, touch_file):
                self.posttask_functions.append(touch_file_factory (arg.args, register_cleanup))
            elif type(arg) == types.FunctionType:
                self.posttask_functions.append(arg)
            else:
                raise PostTaskArgumentError("Expecting simple functions or touch_file in  " +
                                                "@posttask(...)\n Task = %s" %
                                                (self._name))

        
        
#   DEBUGG
class task_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, defaultdict):
            return dict(obj)
        if isinstance(obj, _task):
            return obj._name #, _task.action_names[obj.action_task], obj._description]
        return json.JSONEncoder.default(self, obj)


            
            
            


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#_________________________________________________________________________________________

#   link_task_names_to_functions

#_________________________________________________________________________________________
def link_task_names_to_functions ():
    """
    Make sure all tasks in dependency list are linked to real functions
        Call this before running anything else
    """
    
    for n in node._all_nodes:
        if n.user_defined_work_func == None:
            display_task_name = n._name.replace("__main__.", "")
            dependent_display_task_name = n._inward[0]._name.replace("__main__.", "")
            if n._module_name in sys.modules:
                module = sys.modules[n._module_name]
                if hasattr(module, n._func_name):
                    n.user_defined_work_func = getattr(module, n._func_name)
                else:
                    raise error_decorator_args(("Module '%s' has no function '%s' in " +
                                                "\n@task_follows('%s')\ndef %s...") %
                                        (n._module_name, n._func_name, display_task_name, dependent_display_task_name))
            else:        
                raise error_decorator_args("Module '%s' not found in " +
                                        "\n@task_follows('%s')\ndef %s..." %
                                (n._module_name, display_task_name, dependent_display_task_name))
    
        
        # 
        # some jobs single state status mirrors parent's state
        #   and parent task not known until know
        # 
        if isinstance(n._single_job_single_output, _task):
            n._single_job_single_output = n._single_job_single_output._single_job_single_output

#_________________________________________________________________________________________

#   task_names_to_tasks

#_________________________________________________________________________________________
def task_names_to_tasks (task_description, task_names):
    """
    Given a list of task names, look up the corresponding tasks
    Will just pass through if the task_name is already a task
    """
    
    #
    #   In case we are given a single item instead of a list
    #
    if isinstance(task_names, str) or type(task_names) == types.FunctionType:
        task_names = [task_names]

    task_nodes = []
    for task_name in task_names:

        # Is this already a function, don't do mapping if already is task
        if type(task_name) == types.FunctionType:
            if hasattr(task_name, "pipeline_task"):
                task_nodes.append(task_name.pipeline_task)
                continue
            else:
                # blow up for unwrapped function
                raise error_function_is_not_a_task(("Function %s is not a pipelined task in ruffus." % 
                                                    task_name.__name__) + 
                                                    " To include this, this function needs to have a ruffus "+
                                                    "decoration like '@parallel', '@files', or named as a dependent "+
                                                    "of some other Ruffus task function via '@follows'.")
            
        # assumes is some kind of string
        if not node.is_node(task_name):
            if  node.is_node("__main__." + task_name):
                task_nodes.append(node.lookup_node_from_name("__main__." + task_name))
            else:
                raise error_node_not_task("%s task %s not a pipelined task " % (
                                                        task_description, task_name))
        else:
            task_nodes.append(node.lookup_node_from_name(task_name))
    return task_nodes


#_________________________________________________________________________________________

#   pipeline_printout_in_dot_format

#_________________________________________________________________________________________
def pipeline_printout_graph (stream, 
                             output_format,
                             target_tasks, 
                             forcedtorun_tasks              = [], 
                             draw_vertically                = True, 
                             ignore_upstream_of_target      = False,
                             skip_uptodate_tasks            = False,
                             gnu_make_maximal_rebuild_mode  = True,
                             test_all_task_for_update       = True,
                             no_key_legend                  = False):
    """
    print out pipeline dependencies in various formats

    :param stream: where to print to
    :type stream: file-like object with ``write()`` function
    :param output_format: ["dot", "jpg", "svg", "ps", "png"]. All but the first depends on the `dot <http://www.graphviz.org>`_ program. 
    :param target_tasks: targets task functions which will be run if they are out-of-date.
    :param forcedtorun_tasks: task functions which will be run whether or not they are out-of-date.
    :param draw_vertically: Top to bottom instead of left to right.
    :param ignore_upstream_of_target: Don't draw upstream tasks of targets. 
    :param skip_uptodate_tasks: Don't draw up-to-date tasks if possible. 
    :param gnu_make_maximal_rebuild_mode: Defaults to re-running *all* out-of-date tasks. Runs minimal
                                          set to build targets if set to ``True``. Use with caution.
    :param test_all_task_for_update: Ask all task functions if they are up-to-date.
    :param no_key_legend: Don't draw key/legend for graph. 
    
    """
    

    link_task_names_to_functions ()
    
    #
    #   target jobs
    #     
    target_tasks        = task_names_to_tasks ("Target", target_tasks)
    forcedtorun_tasks   = task_names_to_tasks ("Forced to run", forcedtorun_tasks)
    
    # open file if string    
    if isinstance(stream, str):
        stream = open(stream, "w")
    
    graph_printout (  stream, 
                      output_format,
                      target_tasks, 
                      forcedtorun_tasks,
                      draw_vertically,
                      ignore_upstream_of_target,
                      skip_uptodate_tasks,
                      gnu_make_maximal_rebuild_mode,
                      test_all_task_for_update,
                      no_key_legend)

    

    
#_________________________________________________________________________________________

#   pipeline_printout

#_________________________________________________________________________________________
def pipeline_printout(output_stream, target_tasks, forcedtorun_tasks = [], verbose=0, indent = 4,
                                    gnu_make_maximal_rebuild_mode  = True, wrap_width = 100):
    """
    Printouts the parts of the pipeline which will be run

    Because the parameters of some jobs depend on the results of previous tasks, this function
    produces only the current snap-shot of task jobs. In particular, tasks which generate 
    variable number of inputs into following tasks will not produce the full range of jobs. 
    
    ::
    
        verbose = 0 : nothing
        verbose = 1 : print task name
        verbose = 2 : print task description if exists
        verbose = 3 : print job names for jobs to be run
        verbose = 4 : print list of up-to-date tasks and job names for jobs to be run
        verbose = 5 : print job names for all jobs whether up-to-date or not

    :param output_stream: where to print to
    :type output_stream: file-like object with ``write()`` function
    :param target_tasks: targets task functions which will be run if they are out-of-date
    :param forcedtorun_tasks: task functions which will be run whether or not they are out-of-date
    :param verbose: More verbose output
    :param indent: How much indentation for pretty format. 
    :param gnu_make_maximal_rebuild_mode: Defaults to re-running *all* out-of-date tasks. Runs minimal
                                          set to build targets if set to ``True``. Use with caution.
    :param test_all_task_for_update: Ask all task functions if they are up-to-date 
    """

    link_task_names_to_functions ()

    #
    #   target jobs
    #     
    target_tasks = task_names_to_tasks ("Target", target_tasks)
    forcedtorun_tasks = task_names_to_tasks ("Forced to run", forcedtorun_tasks)
    
    logging_strm = t_verbose_logger(verbose, t_stream_logger(output_stream))
    

    (topological_sorted,
    self_terminated_nodes,
    dag_violating_edges,
    dag_violating_nodes) = topologically_sorted_nodes(target_tasks, forcedtorun_tasks, 
                                                        gnu_make_maximal_rebuild_mode)
        

    #
    #   raise error if DAG violating nodes 
    #
    if len(dag_violating_nodes):
        dag_violating_tasks = ", ".join(t._name for t in dag_violating_nodes)

        e = error_circular_dependencies("Circular dependencies found in the "
                                        "pipeline involving one or more of (%s)" %
                                            (dag_violating_tasks))
        raise e

    wrap_indent = " " * (indent + 11)
        
    # 
    #   Get updated nodes as all_nodes - nodes_to_run
    # 
    if verbose >= 4:
        (all_tasks, ignore_param1, ignore_param2, 
         ignore_param3) = topologically_sorted_nodes(target_tasks, True, 
                                                            gnu_make_maximal_rebuild_mode)
        if len(all_tasks) > len(topological_sorted):
            output_stream.write("\n" + "_" * 40 + "\nTasks which are up-to-date:\n\n")
            pipelined_tasks_to_run = set(topological_sorted)

            for t in all_tasks:
                if t in pipelined_tasks_to_run:
                    continue
                messages = t.printout(t in forcedtorun_tasks, verbose, indent)
                for m in messages:
                    output_stream.write(textwrap.fill(m, subsequent_indent = wrap_indent, width = wrap_width) + "\n")

    output_stream.write("\n" + "_" * 40 + "\nTasks which will be run:\n\n")
    for t in topological_sorted:
        messages = t.printout(t in forcedtorun_tasks, verbose, indent)
        for m in messages:
            output_stream.write(textwrap.fill(m, subsequent_indent = wrap_indent, width = wrap_width) + "\n")

    if verbose:
        output_stream.write("_" * 40 + "\n")
        
#_________________________________________________________________________________________
#
#   Parameter generator for all jobs / tasks
#
#________________________________________________________________________________________ 
def make_job_parameter_generator (incomplete_tasks, task_parents, logger, forcedtorun_tasks, 
                                                        count_remaining_jobs, verbose):

    inprogress_tasks = set()

    def parameter_generator():
        log_at_level (logger, 10, verbose, "   job_parameter_generator BEGIN")
        while len(incomplete_tasks):
            cnt_jobs_created_for_all_tasks = 0
            cnt_tasks_processed = 0
            for t in list(incomplete_tasks):              
                #
                #   wrap in execption handler so that we know which task exception
                #       came from 
                #
                try:
                    log_at_level (logger, 10, verbose, "   job_parameter_generator consider task = %s" % t._name)
    
                    # ignore tasks in progress
                    if t in inprogress_tasks:
                        continue
                    log_at_level (logger, 10, verbose, "   job_parameter_generator task %s not in progress" % t._name)
                    
                    # ignore tasks with incomplete dependencies
                    incomplete_parent = False
                    for parent in task_parents[t]:                  
                        if parent in incomplete_tasks:         
                            incomplete_parent = True
                            break
                    if incomplete_parent:
                        continue
                        
                    log_at_level (logger, 10, verbose, "   job_parameter_generator start task %s (parents completed)" % t._name)
                    force_rerun = t in forcedtorun_tasks
                    # 
                    # log task
                    # 
                    task_name = t._name.replace("__main__.", "")
                    log_at_level (logger, 3, verbose, "Start Task = " + task_name + (": Forced to rerun" if force_rerun else ""))
                    log_at_level (logger, 3, verbose, t._description)
                    inprogress_tasks.add(t)
                    cnt_tasks_processed += 1
                    

                    #
                    #   Use output parameters actually generated by running task
                    #
                    t.output_filenames = []


                    #
                    #   If no parameters: just call task function (empty list)
                    #
                    if t.param_generator_func == None:
                        parameters = ([],)
                    else:
                        parameters = t.param_generator_func()
                        
                    # 
                    #   iterate through parameters
                    #                         
                    cnt_jobs_created = 0
                    for param in parameters:
                        
                        #
                        #   save output even if uptodate 
                        #
                        if len(param) >= 2:
                            t.output_filenames.append(param[1])

                        job_name = t.job_descriptor(param)

                        # 
                        #    don't run if up to date
                        #
                        if force_rerun:
                            log_at_level (logger, 3, verbose, "    force task %s to rerun " % job_name)
                        else:
                            if not t.needs_update_func:
                                log_at_level (logger, 3, verbose, "    %s no function to check if up-to-date " % job_name)
                            else:
                                needs_update, msg = t.needs_update_func (*param)
                                if not needs_update:
                                    log_at_level (logger, 2, verbose, "    %s unnecessary: already up to date " % job_name)
                                    continue
                                else:
                                    log_at_level (logger, 3, verbose, "    %s %s " % (job_name, msg))

                        #
                        #   Clunky hack to make sure input files exists right before 
                        #        job is called for better error messages
                        #
                        if t.needs_update_func == needs_update_check_modify_time:
                            check_input_files_exist (*param)
                            
                        count_remaining_jobs[t] += 1
                        cnt_jobs_created += 1
                        cnt_jobs_created_for_all_tasks += 1
                        yield (param, 
                                t._name,
                                job_name,   
                                t.job_wrapper, 
                                t.user_defined_work_func)

                    # if no job came from this task, this task is complete
                    #   we need to retire it here instead of normal completion at end of job tasks
                    #   precisely because it created no jobs
                    if cnt_jobs_created == 0:
                        incomplete_tasks.remove(t)
                        t.completed (logger, True)
                        
                # 
                #   GeneratorExit is thrown when this generator does not complete.
                #       I.e. there is a break in the pipeline_run loop.
                #       This happens where there are exceptions signalled from within a job
                # 
                #   This is not really an exception, more a way to exit the generator loop
                #       asynchrononously so that cleanups can happen (e.g. the "with" statement
                #       or finally.)
                # 
                #   We could write except Exception: below which will catch everything but
                #       KeyboardInterrupt and StopIteration and GeneratorExit in python 2.6
                # 
                #   However, in python 2.5, GeneratorExit inherits from Exception. So
                #       we explicitly catch and rethrow GeneratorExit.
                except GeneratorExit:
                    raise
                except:
                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                    exception_stack  = traceback.format_exc(exceptionTraceback)
                    exception_name   = exceptionType.__module__ + '.' + exceptionType.__name__
                    exception_value  = str(exceptionValue)
                    if len(exception_value):
                        exception_value = "(%s)" % exception_value
                    errt = RethrownJobError([(t._name,
                                             "", 
                                             exception_name, 
                                             exception_value, 
                                             exception_stack)])
                    errt.specify_task(t, "Exceptions generating parameters")
                    raise errt



            # extra tests incase final tasks do not result in jobs
            if len(incomplete_tasks) and (not cnt_tasks_processed or cnt_jobs_created_for_all_tasks):
                log_at_level (logger, 10, verbose, "    incomplete tasks = " + 
                                       ",".join([t._name for t in incomplete_tasks] ))
                yield waiting_for_more_tasks_to_complete()

        yield all_tasks_complete()
        # This function is done
        log_at_level (logger, 10, verbose, "   job_parameter_generator END")

    return parameter_generator

 

#_________________________________________________________________________________________
#
#   feed_job_params_to_process_pool
#
#
#________________________________________________________________________________________ 
def feed_job_params_to_process_pool_factory (parameter_q):
    """
    Process pool gets its parameters from this generator
    Use factory function to save parameter_queue
    """
    def feed_job_params_to_process_pool ():
        #print >>sys.stderr, "   Send param to Pooled Process START" # DEBUG PIPELINE
        while 1:
            #print >>sys.stderr, "   Get next parameter size = %d" % parameter_q.qsize()               # DEBUG PIPELINE
            param = parameter_q.get()
            #print >>sys.stderr, "   Get next parameter done"           # DEBUG PIPELINE

            # all tasks done
            if isinstance(param, all_tasks_complete):
                break

            #print >>sys.stderr, "   Send param to Pooled Process=>", param[0] # DEBUG PIPELINE
            yield param

        #print >>sys.stderr, "   Send param to Pooled Process END" # DEBUG PIPELINE
        
    # return generator
    return feed_job_params_to_process_pool

#_________________________________________________________________________________________
#
#   fill_queue_with_job_parameters
#
#________________________________________________________________________________________ 
def fill_queue_with_job_parameters (job_parameters, parameter_q, POOL_SIZE):
    """
    Ensures queue is filled with number of parameters > jobs / slots (POOL_SIZE)
    """
    #print >>sys.stderr, "   fill_queue_with_job_parameters START" # DEBUG PIPELINE
    for param in job_parameters:

        # stop if no more jobs available
        if isinstance(param, waiting_for_more_tasks_to_complete):
            #print >>sys.stderr, "   fill_queue_with_job_parameters wait for task to complete" # DEBUG PIPELINE
            break
            
        #if not isinstance(param, all_tasks_complete):                           # DEBUG PIPELINE
            #print >>sys.stderr, "   fill_queue_with_job_parameters=>", param[0] # DEBUG PIPELINE

        # put into queue
        parameter_q.put(param)
        
        # queue size needs to be at least 2 so that the parameter queue never consists of a single
        #   waiting_for_task_to_complete entry which will cause
        #   a loop and everything to hang!
        if parameter_q.qsize() > POOL_SIZE + 1:
            break
    #print >>sys.stderr, "   fill_queue_with_job_parameters END" # DEBUG PIPELINE


#   
#   How the job queue works:
# 
#   Main loop
#       iterates pool.map using feed_job_params_to_process_pool() 
#       (calls parameter_q.get() until all_tasks_complete)
# 
#           if errors but want to finish tasks already in pipeine:
#               parameter_q.put(all_tasks_complete())
#               keep going
#        else:
#            
#            loops through jobs until no more jobs in non-dependent tasks
#               separate loop in generator so that list of incomplete_tasks does not 
#               get updated half way through
#               causing race conditions
#
#               parameter_q.put(param)
#               until waiting_for_more_tasks_to_complete
#               until queue is full (check *after*)
#

#_________________________________________________________________________________________

#   pipeline_run

#_________________________________________________________________________________________
def pipeline_run(target_tasks = [], forcedtorun_tasks = [], multiprocess = 1, logger = stderr_logger, 
                                    gnu_make_maximal_rebuild_mode  = True, verbose = 1):
    """
    Run pipelines.

    :param target_tasks: targets task functions which will be run if they are out-of-date
    :param forcedtorun_tasks: task functions which will be run whether or not they are out-of-date
    :param multiprocess: The number of concurrent jobs
    :param logger: Where progress will be logged. Defaults to stderr output. 
    :type logger: `logging <http://docs.python.org/library/logging.html>`_ objects
    :param gnu_make_maximal_rebuild_mode: Defaults to re-running *all* out-of-date tasks. Runs minimal
                                          set to build targets if set to ``True``. Use with caution. 
    :param verbose: level 0: nothing
                    level 1: logs completed jobs/tasks; 
                    level 2: logs up to date jobs in incomplete tasks
                    level 3: logs reason for running job;
                    level 4: Shows the tasks Ruffus check for up-to-date/completion to decide which part of the pipeline to execute
                    level 10: logs messages useful only for debug ruffus pipeline code


    """
    if verbose == 0:
        logger = black_hole_logger

    link_task_names_to_functions ()
    #
    #   target jobs
    #     
    target_tasks = task_names_to_tasks ("Target", target_tasks)
    forcedtorun_tasks = task_names_to_tasks ("Forced to run", forcedtorun_tasks)
    
    (topological_sorted,
    self_terminated_nodes,
    dag_violating_edges,
    dag_violating_nodes) = topologically_sorted_nodes(  target_tasks, forcedtorun_tasks, 
                                                        gnu_make_maximal_rebuild_mode,
                                                        extra_data_for_signal = t_verbose_logger(verbose, logger))

    if len(dag_violating_nodes):
        dag_violating_tasks = ", ".join(t._name for t in dag_violating_nodes)

        e = error_circular_dependencies("Circular dependencies found in the "
                                        "pipeline involving one or more of (%s)" %
                                            (dag_violating_tasks))
        raise e



    # 
    # get dependencies. Only include tasks which will be run
    # 
    incomplete_tasks = set(topological_sorted)
    task_parents = defaultdict(set)
    for t in incomplete_tasks:
        task_parents[t] = set()
        for parent in t._outward:
            if parent in incomplete_tasks:
                task_parents[t].add(parent)
    #print json.dumps(task_parents.items(), indent=4, cls=task_encoder)
    
    
    # prepare tasks for pipeline run
    #    **********
    #      BEWARE
    #    **********
    #    
    #    Because state is stored, ruffus is *not* reentrant.
    #    
    #    **********
    #      BEWARE
    #    **********
    for t in topological_sorted:
        t.init_for_pipeline()
    

    # 
    # prime queue with initial set of job parameters    
    # 
    parameter_q = Queue()

    count_remaining_jobs = defaultdict(int)
    parameter_generator = make_job_parameter_generator (incomplete_tasks, task_parents, 
                                                        logger, forcedtorun_tasks, 
                                                        count_remaining_jobs, verbose)
    job_parameters = parameter_generator()
    fill_queue_with_job_parameters(job_parameters, parameter_q, multiprocess)

    # 
    #   N.B. 
    #   Handling keyboard shortcuts may require 
    #       See http://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool
    # 
    #   When waiting for a condition in threading.Condition.wait(), KeyboardInterrupt is never sent
    #       unless a timeout is specified
    # 
    #   
    # 
    #   #                                                              
    #   #   whether using multiprocessing                              
    #   #                                                              
    #   pool = Pool(multiprocess) if multiprocess > 1 else None        
    #   if pool:                                                       
    #       pool_func = pool.imap_unordered                            
    #       job_iterator_timeout = []
    #   else:                                                          
    #       pool_func = imap                                           
    #       job_iterator_timeout = [999999999999]
    # 
    # 
    #   ....
    # 
    # 
    #   it = pool_func(run_pooled_job_without_exceptions, feed_job_params_to_process_pool())
    #   while 1:
    #      try:
    #          job_result = it.next(*job_iterator_timeout)
    # 
    #          ...
    #           
    #      except StopIteration:
    #          break



    #
    #   whether using multiprocessing
    #   
    pool = Pool(multiprocess) if multiprocess > 1 else None
    if pool:
        pool_func = pool.imap_unordered
    else:
        pool_func = imap

    
    
    feed_job_params_to_process_pool = feed_job_params_to_process_pool_factory (parameter_q)

    # 
    #   for each result from job
    # 
    job_errors = list()
    tasks_with_errors = set()

    #   
    #   job_result.job_name / job_result.return_value
    #       Reserved for returning result from job... 
    #       How?
    # 
    
    for job_result in pool_func(run_pooled_job_without_exceptions, feed_job_params_to_process_pool()):
        
        t = node.lookup_node_from_name(job_result.task_name)
        count_remaining_jobs[t] = count_remaining_jobs[t] - 1
        
        last_job_in_task = False
        if count_remaining_jobs[t] == 0:
            incomplete_tasks.remove(t)
            last_job_in_task = True
            
        elif count_remaining_jobs[t] < 0:
            raise Exception("Task [%s] job count < 0" % t._name)
            
        # only save poolsize number of errors            
        if job_result.state == JOB_ERROR:
            job_errors.append(job_result.exception)
            tasks_with_errors.add(t)
            if len(job_errors) >= multiprocess:
                break
                
        # break immediately if the user says stop
        elif job_result.state == JOB_SIGNALLED_BREAK:
            job_errors.append(job_result.exception)
            tasks_with_errors.add(t)
            break

        else:
            if job_result.state == JOB_UP_TO_DATE:
                if verbose > 1:
                    logger.info("    %s unnecessary: already up to date" % job_result.job_name)
            elif verbose:
                logger.info("    %s completed" % job_result.job_name)
            
        #
        # Current Task completed
        #             
        if last_job_in_task:

            t.completed (logger)

            
        # make sure queue is still full after each job is retired
        # do this after undating which jobs are incomplete
        if len(job_errors):
            #parameter_q.clear()
            #if len(job_errors) == 1 and not parameter_q._closed:
            parameter_q.put(all_tasks_complete())
        else:
            fill_queue_with_job_parameters(job_parameters, parameter_q, multiprocess)

        
        

    if len(job_errors):
        errt = RethrownJobError(job_errors)
        for t in tasks_with_errors:
            errt.specify_task(t, "Exceptions running jobs")
        raise errt



        
#   use high resolution timestamps where available            
#       default in python 2.5 and greater
#   N.B. File modify times / stat values have 1 second precision for many file systems
#       and may not be accurate to boot, especially over the network.
os.stat_float_times(True)


if __name__ == '__main__':
    import unittest
    
    


    #
    #   debug parameter ignored if called as a module
    #     
    if sys.argv.count("--debug"):
        sys.argv.remove("--debug")
    unittest.main()




