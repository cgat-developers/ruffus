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


from __future__ import with_statement
import os,sys,copy, multiprocessing
#from collections import namedtuple
import collections

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
import time
from multiprocessing.managers import SyncManager
from contextlib import contextmanager


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
    def warning (self, message):
        pass


class t_stderr_logger:
    """
    Everything to stderr
    """
    def __init__ (self):
        self.unique_prefix = ""
    def add_unique_prefix (self):
        import random
        random.seed()
        self.unique_prefix= str(random.randint(0,1000)) + " "
    def info (self, message):
        sys.stderr.write(self.unique_prefix + message + "\n")
    def warning (self, message):
        sys.stderr.write("\n\n" + self.unique_prefix + "WARNING:\n    " + message + "\n\n")
    def debug (self, message):
        sys.stderr.write(self.unique_prefix + message + "\n")

class t_stream_logger:
    """
    Everything to stderr
    """
    def __init__ (self, stream):
        self.stream = stream
    def info (self, message):
        self.stream.write(message + "\n")
    def warning (self, message):
        sys.stream.write("\n\nWARNING:\n    " + message + "\n\n")
    def debug (self, message):
        self.stream.write(message + "\n")

black_hole_logger = t_black_hole_logger()
stderr_logger     = t_stderr_logger()

class t_verbose_logger:
    def __init__ (self, verbose, logger, runtime_data):
        self.verbose = verbose
        self.logger = logger
        self.runtime_data = runtime_data

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


#
# synchronisation data
#
#SyncManager()
#syncmanager.start()

#
# do nothing semaphore
#
@contextmanager
def do_nothing_semaphore():
    yield












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

class jobs_limit(task_decorator):
    pass


#
#   Advanced
#
class collate(task_decorator):
    pass

class active_if(task_decorator):
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

#_________________________________________________________________________________________

#   add_inputs

#_________________________________________________________________________________________
class add_inputs(object):
    def __init__ (self, *args):
        self.args = args

#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#       job descriptors

#           given parameters, returns string describing job
#           main use in error logging

#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888
def generic_job_descriptor (param, runtime_data):
    if param in ([], None):
        return "Job"
    else:
        return "Job = %s" % ignore_unknown_encoder(param)

def io_files_job_descriptor (param, runtime_data):
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


def mkdir_job_descriptor (param, runtime_data):
    # input, output and parameters
    return "Make directories %s" % (shorten_filenames_encoder(param[0]))


#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#       job wrappers
#           registers files/directories for cleanup

#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#_________________________________________________________________________________________

#   generic job wrapper

#_________________________________________________________________________________________
def job_wrapper_generic(param, user_defined_work_func, register_cleanup, touch_files_only):
    """
    run func
    """
    assert(user_defined_work_func)
    return user_defined_work_func(*param)

#_________________________________________________________________________________________

#   job wrapper for all that deal with i/o files

#_________________________________________________________________________________________
def job_wrapper_io_files(param, user_defined_work_func, register_cleanup, touch_files_only):
    """
    run func on any i/o if not up to date
    """
    assert(user_defined_work_func)

    i,o = param[0:2]

    if not touch_files_only:
        ret_val = user_defined_work_func(*param)
    else:
        for f in get_strings_in_nested_sequence(o):
            if not os.path.exists(f):
                open(f, 'w')
            else:
                os.utime(f, None)



    #
    # register strings in output file for cleanup
    #
    for f in get_strings_in_nested_sequence(o):
        register_cleanup(f, "file")


#_________________________________________________________________________________________

#   job wrapper for mkdir

#_________________________________________________________________________________________
def job_wrapper_mkdir(param, user_defined_work_func, register_cleanup, touch_files_only):
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
        except:
            #
            #   ignore exception if exception == OSError / "File exists"
            #
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            if exceptionType == OSError and "File exists" in str(exceptionValue):
                continue
            raise

        #   changed for compatibility with python 3.x
        #except OSError, e:
        #    if "File exists" not in e:
        #        raise


JOB_ERROR           = 0
JOB_SIGNALLED_BREAK = 1
JOB_UP_TO_DATE      = 2
JOB_COMPLETED       = 3

#_________________________________________________________________________________________

#   t_job_result
#       Previously a collections.namedtuple (introduced in python 2.6)
#       Now using implementation from running
#           t_job_result = namedtuple('t_job_result', 'task_name state job_name return_value exception', verbose =1)
#           for compatibility with python 2.5

#_________________________________________________________________________________________
class t_job_result(tuple):
        't_job_result(task_name, state, job_name, return_value, exception)'

        __slots__ = ()

        fields = ('task_name', 'state', 'job_name', 'return_value', 'exception')

        def __new__(cls, task_name, state, job_name, return_value, exception):
            return tuple.__new__(cls, (task_name, state, job_name, return_value, exception))

        @classmethod
        def make(cls, iterable, new=tuple.__new__, len=len):
            'Make a new t_job_result object from a sequence or iterable'
            result = new(cls, iterable)
            if len(result) != 5:
                raise TypeError('Expected 5 arguments, got %d' % len(result))
            return result

        def __repr__(self):
            return 't_job_result(task_name=%r, state=%r, job_name=%r, return_value=%r, exception=%r)' % self

        def asdict(t):
            'Return a new dict which maps field names to their values'
            return {'task_name': t[0], 'state': t[1], 'job_name': t[2], 'return_value': t[3], 'exception': t[4]}

        def replace(self, **kwds):
            'Return a new t_job_result object replacing specified fields with new values'
            result = self.make(map(kwds.pop, ('task_name', 'state', 'job_name', 'return_value', 'exception'), self))
            if kwds:
                raise ValueError('Got unexpected field names: %r' % kwds.keys())
            return result

        def __getnewargs__(self):
            return tuple(self)

        task_name   = property(itemgetter(0))
        state       = property(itemgetter(1))
        job_name    = property(itemgetter(2))
        return_value= property(itemgetter(3))
        exception   = property(itemgetter(4))



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

    (param, task_name, job_name, job_wrapper, user_defined_work_func,
            job_limit_semaphore, one_second_per_job, touch_files_only) = process_parameters

    if job_limit_semaphore == None:
        job_limit_semaphore = do_nothing_semaphore()

    try:
        with job_limit_semaphore:
            return_value =  job_wrapper(param, user_defined_work_func, register_cleanup, touch_files_only)

            #
            #   ensure one second between jobs
            #
            #if one_second_per_job:
            #    time.sleep(1.01)
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

        if exceptionType == JobSignalledBreak:
            job_state = JOB_SIGNALLED_BREAK
        else:
            job_state = JOB_ERROR
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
                    "task_active_if",
                    ]
    action_unspecified        =  0
    action_task               =  1
    action_task_files_re      =  2
    action_task_split         =  3
    action_task_merge         =  4
    action_task_transform     =  5
    action_task_collate       =  6
    action_task_files_func    =  7
    action_task_files         =  8
    action_mkdir              =  9
    action_parallel           = 10
    action_active_if          = 11

    add_to_inputs             =  False
    replace_inputs            =  True


    multiple_jobs_outputs    = 0
    single_job_single_output = 1
    job_single_matches_parent= 2

    job_limit_semaphores = {}
    

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
        # convert description into one line
        if func.__doc__:
            t._description           = re.sub("\n\s+", " ", func.__doc__).strip()
        else:
            t._description = ""

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



        self.param_generator_func       = None
        self.needs_update_func          = None
        self.job_wrapper                = job_wrapper_generic

        #                               
        self.job_descriptor             = generic_job_descriptor

        # jobs which produce a single output.
        # special handling for task.get_output_files for dependency chaining
        self._single_job_single_output  = self.multiple_jobs_outputs
        self.single_multi_io            = self.many_to_many

        # function which is decorated and does the actual work
        self.user_defined_work_func = None

        # functions which will be called when task completes
        self.posttask_functions         = []

        # give makedir automatically made parent tasks unique names
        self.cnt_task_mkdir             = 0

        # whether only task function itself knows what output it will produce
        # i.e. output is a glob or something similar
        self.indeterminate_output       = 0

        # cache output file names here
        self.output_filenames           = None

        self.semaphore_name             = module_name + "." + func_name

        # do not test for whether task is active
        self.active_if_checks           = None

        # extra flag for outputfiles
        self.is_active                  = True



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
        self._action_type_desc = _task.action_names[new_action_type]


    #_________________________________________________________________________________________

    #   printout

    #_________________________________________________________________________________________
    def printout (self, runtime_data, force_rerun, verbose=1, indent = 4):
        """
        Print out all jobs for this task

                verbose = 1 : print task name
                          2 : print task description if exists
                          3 : print job names for jobs to be run
                          4 : print job names for up-to- date jobs
        """

        def get_job_names (param, indent_str):
            job_names = (indent_str + self.job_descriptor(param, runtime_data)).split("-> ")
            if len(job_names) > 1:
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
        #   If has an @active_if decorator, check if the task needs to be run
        #       @active_if parameters may be call back functions or booleans
        #
        if (self.active_if_checks != None and
            any( not arg() if isinstance(arg, collections.Callable) else not arg
                     for arg in self.active_if_checks)):
                if verbose <= 3:
                    return messages
                messages.append(indent_str + "Task is inactive")
                return messages
                

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
            cnt_jobs = 0
            for param, descriptive_param in self.param_generator_func(runtime_data):
                cnt_jobs += 1
                job_name = self.job_descriptor(descriptive_param, runtime_data)
                job_name = job_name.replace("->", indent_str + " " * 7 +  "\n->")

                #
                #   needs update func = None: always needs update
                #
                if not self.needs_update_func:
                    messages.extend(get_job_names (descriptive_param, indent_str))
                    messages.append(indent_str + "  Jobs needs update: No function to check if up-to-date or not")
                    continue

                needs_update, msg = self.needs_update_func (*param)
                if needs_update:
                    messages.extend(get_job_names (descriptive_param, indent_str))
                    per_job_messages = [(indent_str + s) for s in ("  Job needs update: %s" % msg).split("\n")]
                    messages.extend(per_job_messages)
                else:
                    if verbose > 4:
                        messages.extend(get_job_names (descriptive_param, indent_str))
                        messages.append(indent_str + "  Job up-to-date")
            if cnt_jobs == 0:
                messages.append(indent_str + "!!! No jobs for this task. "
                                             "Are you sure there is not a error in your "
                                             "code / regular expression?")
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
            if verbose_logger:
                logger       = verbose_logger.logger
                verbose      = verbose_logger.verbose
                runtime_data = verbose_logger.runtime_data
            else:
                logger       = None
                verbose      = 0
                runtime_data = {}
            short_task_name = self._name.replace('__main__.', '')
            log_at_level (logger, 4, verbose,
                            "  Task = " + short_task_name)

            #
            #   If job is inactive, always consider it up-to-date
            #     
            if (self.active_if_checks != None and
                any( not arg() if isinstance(arg, collections.Callable) else not arg
                         for arg in self.active_if_checks)):
                log_at_level (logger, 4, verbose,
                                "    Inactive task: treat as Up to date")
                #print 'signaling that the inactive task is up to date'
                return True
            
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
                for param, descriptive_param in self.param_generator_func(runtime_data):
                    needs_update, msg = self.needs_update_func (*param)
                    if needs_update:
                        if verbose >= 4:
                            job_name = self.job_descriptor(descriptive_param, runtime_data)
                            log_at_level (logger, 4, verbose,
                                            "    Needing update:\n      %s" % job_name)
                        return False

                #
                #   Percolate warnings from parameter factories
                #
                if (verbose >= 1 and "ruffus_WARNING" in runtime_data and
                    self.param_generator_func in runtime_data["ruffus_WARNING"]):
                    for msg in runtime_data["ruffus_WARNING"][self.param_generator_func]:
                        logger.warning("    'In Task def %s(...):' %s " % (short_task_name, msg))


                log_at_level (logger, 4, verbose, "    All jobs up to date")




                return True

        #
        # removed for compatibility with python 3.x
        #
        # rethrow exception after adding task name
        #except error_task, inst:
        #    inst.specify_task(self, "Exceptions in dependency checking")
        #    raise

        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()

            #
            # rethrow exception after adding task name
            #
            if exceptionType == error_task:
                exceptionValue.specify
                inst.specify_task(self, "Exceptions in dependency checking")
                raise

            exception_stack  = traceback.format_exc(exceptionTraceback)
            exception_name   = exceptionType.__module__ + '.' + exceptionType.__name__
            exception_value  = str(exceptionValue)
            if len(exception_value):
                exception_value = "(%s)" % exception_value
            errt = RethrownJobError([(self._name,
                                     "",
                                     exception_name,
                                     exception_value,
                                     exception_stack)])
            errt.specify_task(self, "Exceptions generating parameters")
            raise errt



    #_____________________________________________________________________________________

    #   get_output_files
    #
    #
    #_____________________________________________________________________________________
    def get_output_files (self, do_not_expand_single_job_tasks, runtime_data):
        """
        Cache output files

            If flattened is True, returns file as a list of strings,
                flattening any nested structures and discarding non string names
            Normally returns a list with one item for each job or a just a list of file names.
            For "single_job_single_output" i.e. @merge and @files with single jobs,
                returns the output of a single job (i.e. can be a string)
        """

        #
        #   N.B. active_if_checks is called once per task 
        #        in make_job_parameter_generator() for consistency
        #
        #   self.is_active can be set using self.active_if_checks in that function,
        #       and therefore can be changed BETWEEN invocations of pipeline_run
        #
        #   self.is_active is not used anywhere else
        #
        if (not self.is_active):
            #print >>sys.stderr, "    Removing all outputs from " + self._name.replace('__main__.', '')
            return []
        
        #
        #   This looks like the wrong place to flatten
        #
        flattened = False
        if self.output_filenames == None:

            self.output_filenames = []

            # skip tasks which don't have parameters
            if self.param_generator_func != None:

                cnt_jobs = 0
                for param, descriptive_param in self.param_generator_func(runtime_data):
                    cnt_jobs += 1
                    # skip tasks which don't have output parameters
                    if len(param) >= 2:
                        self.output_filenames.append(param[1])


                if self._single_job_single_output == self.single_job_single_output:
                    if cnt_jobs > 1:
                        raise error_task_get_output(self,
                               "Task which is supposed to produce a single output "
                               "somehow has more than one job.")

                #
                #   The output of @split should be treated as multiple jobs
                #
                #       The output of @split is always a list of lists:
                #         1) There is a list of @split jobs
                #            A) For advanced (regex) @split
                #               this is a many -> many more operation
                #               So len(list) == many (i.e. the number of jobs
                #            B) For normal @split
                #               this is a  1   -> many operation
                #               So len(list)  = 1
                #
                #         2) The output of each @split job is a list
                #            The items in this list of lists are each a job in subsequent tasks
                #
                #
                #         So we need to concatenate these separate lists into a single list of output
                #
                #         For example:
                #         @split(["a.1", "b.1"], regex(r"(.)\.1"), r"\1.*.2")
                #         def example(input, output):
                #             # JOB 1
                #             #   a.1 -> a.i.2
                #             #       -> a.j.2
                #
                #             # JOB 2
                #             #   b.1 -> b.i.2
                #             #       -> b.j.2
                #
                #         output_filenames = [ [a.i.2, a.j.2], [b.i.2, b.j.2] ]
                #
                #         we want [ a.i.2, a.j.2, b.i.2, b.j.2 ]
                #
                #         This also works for simple @split
                #
                #         @split("a.1", r"a.*.2")
                #         def example(input, output):
                #             # only job
                #             #   a.1 -> a.i.2
                #             #       -> a.j.2
                #
                #         output_filenames = [ [a.i.2, a.j.2] ]
                #
                #         we want [ a.i.2, a.j.2 ]
                #
                if len(self.output_filenames) and self.indeterminate_output:
                    self.output_filenames = reduce(lambda x,y: x + y, self.output_filenames)


        if flattened:
            # if single file name, return that
            # accepts unicode
            if (do_not_expand_single_job_tasks and
                len(self.output_filenames) and
                isinstance(self.output_filenames[0], basestring)):
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
        function_or_func_names, globs, runtime_data_names = get_nested_tasks_or_globs(input_params)

        #
        # replace function / function names with tasks
        #
        tasks = self.task_follows(function_or_func_names)
        functions_to_tasks = dict(zip(function_or_func_names, tasks))
        input_params = replace_func_names_with_tasks(input_params, functions_to_tasks)

        return t_params_tasks_globs_run_time_data(input_params, tasks, globs, runtime_data_names)





    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

    #       task handlers

    #         sets
    #               1) action_type
    #               2) param_generator_func
    #               3) needs_update_func
    #               4) job wrapper


    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

    #_________________________________________________________________________________________

    #   task_split_ex

    #_________________________________________________________________________________________
    def task_split_ex (self, orig_args):
        """
        Splits a single set of input files into multiple output file names,
            where the number of output files may not be known beforehand.
        """
        #
        #   check enough arguments
        #
        if (len(orig_args) < 3 or
            (isinstance(orig_args[2], inputs) and len(orig_args) < 4) or
            (isinstance(orig_args[2], add_inputs) and len(orig_args) < 4)
            ):
            raise error_task_split(self, "Too few arguments for @split")



        self.set_action_type (_task.action_task_split)

        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])

        #   allows split to take a single file or task
        input_files_task_globs.single_file_to_list()


        # regular expression match
        matching_regex = compile_regex(self, orig_args[1], error_task_split, "@split")

        #
        #   inputs can also be defined by pattern match
        #
        replace_inputs = _task.add_to_inputs
        if isinstance(orig_args[2], inputs):
            if len(orig_args[2].args) != 1:
                raise error_task_transform_inputs_multiple_args(self,
                                    "inputs(...) expects only a single argument. "
                                    "This can be, for example, a file name, "
                                    "a regular expression pattern, or any "
                                    "nested structure. If the intention was to "
                                    "specify a tuple as the input parameter, "
                                    "please wrap the elements of the tuple "
                                    "in brackets in the decorator\n\n@transform(..., inputs(...), ...)\n")
            extra_inputs = self.handle_tasks_globs_in_inputs(orig_args[2].args[0])
            output_pattern = orig_args[3]
            replace_inputs = _task.replace_inputs
            extra_params = orig_args[4:]
        elif isinstance(orig_args[2], add_inputs):
            extra_inputs = self.handle_tasks_globs_in_inputs(orig_args[2].args)
            output_pattern = orig_args[3]
            extra_params = orig_args[4:]
        else:
            extra_inputs = None
            output_pattern = orig_args[2]
            extra_params = orig_args[3:]



        #
        #   replace output globs with files
        #
        output_files_task_globs = self.handle_tasks_globs_in_inputs(output_pattern)
        if len(output_files_task_globs.tasks):
            raise error_task_split(self, "@split cannot output to another task. "
                                            "Do not include tasks in output parameters.")



        self.param_generator_func = split_ex_param_factory (   input_files_task_globs,
                                                                False, # flatten input
                                                                matching_regex,
                                                                extra_inputs,
                                                                replace_inputs,
                                                                output_files_task_globs,
                                                                *extra_params)
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor # (orig_args[2], output_runtime_data_names)

        # output is a glob
        self.indeterminate_output = 2
        self.single_multi_io       = self.many_to_many

    #_________________________________________________________________________________________

    #   task_split

    #_________________________________________________________________________________________
    def task_split (self, orig_args):
        """
        Splits a single set of input files into multiple output file names,
            where the number of output files may not be known beforehand.
        """
        if isinstance(orig_args[1], regex):
            self.task_split_ex(orig_args)
            return

        #check enough arguments
        if len(orig_args) < 2:
            raise error_task_split(self, "Too few arguments for @split")

        self.set_action_type (_task.action_task_split)

        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])

        #
        #   replace output globs with files
        #
        output_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[1])
        if len(output_files_task_globs.tasks):
            raise error_task_split(self, "@split cannot output to another task. "
                                            "Do not include tasks in output parameters.")

        extra_params = orig_args[2:]
        self.param_generator_func = split_param_factory (input_files_task_globs, output_files_task_globs, *extra_params)


        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor# (orig_args[1], output_runtime_data_names)

        # output is a glob
        self.indeterminate_output = 1
        self.single_multi_io       = self.one_to_many

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
            (isinstance(orig_args[2], inputs) and len(orig_args) < 4) or
            (isinstance(orig_args[2], add_inputs) and len(orig_args) < 4)
            ):
            raise error_task_transform(self, "Too few arguments for @transform")



        self.set_action_type (_task.action_task_transform)

        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])


        # regular expression match
        if isinstance(orig_args[1], regex):
            matching_regex = compile_regex(self, orig_args[1], error_task_transform, "@transform")
            regex_or_suffix = True

        # simulate end of string (suffix) match
        elif isinstance(orig_args[1], suffix):
            matching_regex = compile_suffix(self, orig_args[1], error_task_transform, "@transform")
            regex_or_suffix = False

        else:
            raise error_task_transform(self, "@transform expects suffix() or "
                                                            "regex() as the second argument")



        #
        #   inputs can also be defined by pattern match
        #
        replace_inputs = _task.add_to_inputs
        if isinstance(orig_args[2], inputs):
            if len(orig_args[2].args) != 1:
                raise error_task_transform_inputs_multiple_args(self,
                                    "inputs(...) expects only a single argument. "
                                    "This can be, for example, a file name, "
                                    "a regular expression pattern, or any "
                                    "nested structure. If the intention was to "
                                    "specify a tuple as the input parameter, "
                                    "please wrap the elements of the tuple "
                                    "in brackets in the decorator\n\n@transform(..., inputs(...), ...)\n")
            extra_inputs = self.handle_tasks_globs_in_inputs(orig_args[2].args[0])
            output_pattern_extras = orig_args[3:]
            replace_inputs = _task.replace_inputs
        elif isinstance(orig_args[2], add_inputs):
            extra_inputs = self.handle_tasks_globs_in_inputs(orig_args[2].args)
            output_pattern_extras = orig_args[3:]
        else:
            extra_inputs = None
            output_pattern_extras = orig_args[2:]

        #
        #   allows transform to take a single file or task
        if input_files_task_globs.single_file_to_list():
            self._single_job_single_output = self.single_job_single_output

        #
        #   whether transform generates a list of jobs or not will depend on the parent task
        #
        elif isinstance(input_files_task_globs.params, _task):
            self._single_job_single_output = input_files_task_globs.params

        self.param_generator_func = transform_param_factory (   input_files_task_globs,
                                                                False, # flatten input
                                                                matching_regex,
                                                                regex_or_suffix,
                                                                extra_inputs,
                                                                replace_inputs,
                                                                *output_pattern_extras)
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        self.single_multi_io       = self.many_to_many

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
        input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])


        # regular expression match
        if isinstance(orig_args[1], regex):
            matching_regex = compile_regex(self, orig_args[1], error_task_collate, "@collate")
        else:
            raise error_task_collate(self, "@collate expects regex() as the second argument")

        #
        #   inputs also defined by pattern match
        #
        replace_inputs = _task.add_to_inputs
        if isinstance(orig_args[2], inputs):
            if len(orig_args[2].args) != 1:
                raise error_task_collate_inputs_multiple_args(self,
                                    "inputs(...) expects only a single argument. "
                                    "This can be, for example, a file name, "
                                    "a regular expression pattern, or any "
                                    "nested structure. If the intention was to "
                                    "specify a tuple as the input parameter, "
                                    "please wrap the elements of the tuple "
                                    "in brackets in the decorator\n\n@collate(..., inputs(...), ...)\n")
            extra_inputs = self.handle_tasks_globs_in_inputs(orig_args[2].args[0])
            output_pattern_extras = orig_args[3:]
            replace_inputs = _task.replace_inputs
        elif isinstance(orig_args[2], add_inputs):
            extra_inputs = self.handle_tasks_globs_in_inputs(orig_args[2].args)
            output_pattern_extras = orig_args[3:]
        else:
            extra_inputs = None
            output_pattern_extras = orig_args[2:]

        extra_params = orig_args[2:]
        self.single_multi_io           = self.many_to_many

        self.param_generator_func = collate_param_factory (input_files_task_globs,
                                                            False, # flatten input
                                                            matching_regex,
                                                            extra_inputs,
                                                            replace_inputs,
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
        input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])

        extra_params = orig_args[1:]
        self.param_generator_func = merge_param_factory (input_files_task_globs,
                                                           *extra_params)


#        self._single_job_single_output = self.multiple_jobs_outputs
        self._single_job_single_output = self.single_job_single_output
        self.single_multi_io           = self.many_to_one

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
        if len(orig_args) == 1 and isinstance(orig_args[0], collections.Callable):
        #if len(orig_args) == 1 and type(orig_args[0]) == types.FunctionType:
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
        if len(orig_args) == 1 and isinstance(orig_args[0], collections.Callable):
            #if len(orig_args) == 1 and type(orig_args[0]) == types.FunctionType:

            self.set_action_type (_task.action_task_files_func)
            self.param_generator_func = files_custom_generator_param_factory(orig_args[0])

            # assume
            self.single_multi_io           = self.many_to_many

        #   Use parameters in supplied list
        else:
            self.set_action_type (_task.action_task_files)

            if len(orig_args) > 1:

                # single jobs
                # This is true even if the previous task has multiple output
                # These will all be joined together at the hip (like @merge)
                # If you want different behavior, use @transform
                params = copy.copy([orig_args])
                self._single_job_single_output = self.single_job_single_output
                self.single_multi_io           = self.one_to_one


            else:

                # multiple jobs with input/output parameters etc.
                params = copy.copy(orig_args[0])
                self._single_job_single_output = self.multiple_jobs_outputs
                self.single_multi_io           = self.many_to_many

            check_files_io_parameters (self, params, error_task_files)

            #
            # get list of function/function names and globs for all job params
            #

            #
            # replace function / function names with tasks
            #
            input_patterns = [j[0] for j in params]
            input_files_task_globs = self.handle_tasks_globs_in_inputs(input_patterns)


            #
            #   extra params
            #
            output_extra_params = [tuple(j[1:]) for j in params]

            self.param_generator_func = files_param_factory (input_files_task_globs,
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
        input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])

        matching_regex = compile_regex(self, regex(orig_args[1]), error_task_files_re, "@files_re")

        # if the input file term is missing, just use the original
        if len(orig_args) == 3:
            extra_input_files_task_globs = None
            output_and_extras = [orig_args[2]]
        else:
            extra_input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[2])
            output_and_extras = orig_args[3:]


        if combining_all_jobs:
            self.single_multi_io           = self.many_to_many
            self.param_generator_func = collate_param_factory (input_files_task_globs,
                                                                False,                  # flatten
                                                                matching_regex,
                                                                extra_input_files_task_globs,
                                                                _task.replace_inputs,
                                                                *output_and_extras)
        else:

            self.single_multi_io           = self.many_to_many
            self.param_generator_func = transform_param_factory (input_files_task_globs,
                                                                    False,              # flatten
                                                                    matching_regex,
                                                                    #regex_or_suffix
                                                                    True,               # substitute all parameters
                                                                    extra_input_files_task_globs,
                                                                    _task.replace_inputs,
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
        # accepts unicode
        if not isinstance(orig_args[0], basestring):
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
        self.single_multi_io           = self.one_to_one






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
            #   specified by string: unicode or otherwise
            #
            if isinstance(arg, basestring):
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
                unique_name = r"(mkdir %d) before " % self.cnt_task_mkdir + self._name
                new_node = _task(self._module_name, unique_name)
                self.add_child(new_node)
                new_node.task_mkdir(arg.args)
                new_node.display_name = new_node._description
                new_tasks.append(new_node)




            #
            #   Is this a function?
            #       Turn this function into a task
            #           (add task as attribute of this function)
            #       Add self as dependent
            else:
                #if type(arg) != types.FunctionType:
                if not isinstance(arg, collections.Callable):

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
        if len(args) != 1 or not isinstance(args[0], collections.Callable):
        #if len(args) != 1 or type(args[0]) != types.FunctionType:
            raise error_decorator_args("Expecting a single function in  " +
                                                "@task_check_if_uptodate %s:\n[%s]" %
                                                (self._name, str(args)))
        self.needs_update_func        = args[0]



    #_________________________________________________________________________________________

    #   task_posttask

    #_________________________________________________________________________________________
    def task_posttask(self, args):
        """
        Saved decorator arguments should be:
                one or more functions which will be called if the task completes
        """
        for arg in args:
            if isinstance(arg, touch_file):
                self.posttask_functions.append(touch_file_factory (arg.args, register_cleanup))
            elif isinstance(arg, collections.Callable):
            #elif type(arg) == types.FunctionType:
                self.posttask_functions.append(arg)
            else:
                raise PostTaskArgumentError("Expecting simple functions or touch_file in  " +
                                                "@posttask(...)\n Task = %s" %
                                                (self._name))

    #_________________________________________________________________________________________

    #   task_jobs_limit

    #_________________________________________________________________________________________
    def task_jobs_limit(self, args):
        """
        Limit the number of concurrent jobs
        """
        maximum_jobs, name = (args + (None,))[0:2]
        try:
            maximum_jobs_num = int(maximum_jobs)
            assert(maximum_jobs_num >= 1)
        except:
            limit_name = ", " + name if name else ""
            raise JobsLimitArgumentError(('In @jobs_limit(%s%s), the limit '
                                          'must be an integer number greater than or '
                                          'equal to 1') %
                                         (maximum_jobs_num, limit_name))
        if name != None:
            self.semaphore_name = name
        if self.semaphore_name in self.job_limit_semaphores:
            curr_maximum_jobs = self.job_limit_semaphores[self.semaphore_name]
            if curr_maximum_jobs != maximum_jobs_num:
                raise JobsLimitArgumentError(('@jobs_limit(%d, "%s") cannot ' +
                                            're-defined with a different limit of %d') %
                                             (self.semaphore_name, curr_maximum_jobs,
                                                maximum_jobs_num))
        else:
            #
            #   save semaphore and limit
            #
            self.job_limit_semaphores[self.semaphore_name] = maximum_jobs_num


    #_________________________________________________________________________________________

    #   task_active_if

    #_________________________________________________________________________________________
    def task_active_if (self, active_if_checks):
        """
        If any of active_checks is False or returns False, then the task is
        marked as "inactive" and its outputs removed.
        """
        #print 'job is active:', active_checks, [
        #                arg() if isinstance(arg, collections.Callable) else arg
        #                for arg in active_checks]
        self.active_if_checks = active_if_checks


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
    #       accepts unicode
    #
    if isinstance(task_names, basestring) or isinstance(task_names, collections.Callable):
    #if isinstance(task_names, basestring) or type(task_names) == types.FunctionType:
        task_names = [task_names]

    task_nodes = []
    for task_name in task_names:

        # Is this already a function, don't do mapping if already is task
        if isinstance(task_name, collections.Callable):
        #if type(task_name) == types.FunctionType:
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
                raise error_node_not_task("%s task '%s' is not a pipelined task in Ruffus. Have you mis-spelt the function name?" % (
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
                             no_key_legend                  = False,
                             minimal_key_legend             = True,
                             user_colour_scheme             = None,
                             pipeline_name                  = "Pipeline:",
                             size                           = (11,8),
                             dpi                            = 120,
                             runtime_data                   =  None):
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
    #   run time data
    #
    if runtime_data == None:
        runtime_data = {}
    if not isinstance(runtime_data, dict):
        raise Exception("pipeline_run parameter runtime_data should be a dictionary of "
                        "values passes to jobs at run time.")

    #
    #   target jobs
    #
    target_tasks        = task_names_to_tasks ("Target", target_tasks)
    forcedtorun_tasks   = task_names_to_tasks ("Forced to run", forcedtorun_tasks)

    # open file if (unicode?) string
    if isinstance(stream, basestring):
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
                      no_key_legend,
                      minimal_key_legend,
                      user_colour_scheme,
                      pipeline_name,
                      size,
                      dpi,
                      extra_data_for_signal = t_verbose_logger(0, None, runtime_data))




#_________________________________________________________________________________________

#   pipeline_printout

#_________________________________________________________________________________________
def pipeline_printout(output_stream, target_tasks, forcedtorun_tasks = [], verbose=1, indent = 4,
                                    gnu_make_maximal_rebuild_mode  = True, wrap_width = 100,
                                    runtime_data= None):
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
    :param verbose: level 0 : nothing
                    level 1 : logs task names and warnings
                    level 2 : logs task description if exists
                    level 3 : logs job names for jobs to be run
                    level 4 : logs list of up-to-date tasks and job names for jobs to be run
                    level 5 : logs job names for all jobs whether up-to-date or not
                    level 10: logs messages useful only for debugging ruffus pipeline code
    :param indent: How much indentation for pretty format.
    :param gnu_make_maximal_rebuild_mode: Defaults to re-running *all* out-of-date tasks. Runs minimal
                                          set to build targets if set to ``True``. Use with caution.
    :param wrap_width: The maximum length of each line
    :param runtime_data: Experimental feature for passing data to tasks at run time
    """
    if verbose == 0:
        return

    if not hasattr(output_stream, "write"):
        raise Exception("The first parameter to pipeline_printout needs to be an output file, e.g. sys.stdout")

    if runtime_data == None:
        runtime_data = {}
    if not isinstance(runtime_data, dict):
        raise Exception("pipeline_run parameter runtime_data should be a dictionary of "
                        "values passes to jobs at run time.")

    link_task_names_to_functions ()

    #
    #   target jobs
    #
    target_tasks = task_names_to_tasks ("Target", target_tasks)
    forcedtorun_tasks = task_names_to_tasks ("Forced to run", forcedtorun_tasks)

    logging_strm = t_verbose_logger(verbose, t_stream_logger(output_stream), runtime_data)


    (topological_sorted,
    self_terminated_nodes,
    dag_violating_edges,
    dag_violating_nodes) = topologically_sorted_nodes(target_tasks, forcedtorun_tasks,
                                                        gnu_make_maximal_rebuild_mode,
                                                        extra_data_for_signal = t_verbose_logger(0, None, runtime_data))


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
                                                     gnu_make_maximal_rebuild_mode,
                                                     extra_data_for_signal = t_verbose_logger(0, None, runtime_data))
        if len(all_tasks) > len(topological_sorted):
            output_stream.write("\n" + "_" * 40 + "\nTasks which are up-to-date:\n\n")
            pipelined_tasks_to_run = set(topological_sorted)

            for t in all_tasks:
                if t in pipelined_tasks_to_run:
                    continue
                messages = t.printout(runtime_data, t in forcedtorun_tasks, verbose, indent)
                for m in messages:
                    output_stream.write(textwrap.fill(m, subsequent_indent = wrap_indent, width = wrap_width) + "\n")

    output_stream.write("\n" + "_" * 40 + "\nTasks which will be run:\n\n")
    for t in topological_sorted:
        messages = t.printout(runtime_data, t in forcedtorun_tasks, verbose, indent)
        for m in messages:
            output_stream.write(textwrap.fill(m, subsequent_indent = wrap_indent, width = wrap_width) + "\n")

    if verbose:
        output_stream.write("_" * 40 + "\n")

#_________________________________________________________________________________________

#   get_semaphore

#_________________________________________________________________________________________
def get_semaphore (t, job_limit_semaphores, syncmanager):
    """
    return semaphore to limit the number of concurrent jobs
    """
    #
    #   Is this task limited in the number of jobs?
    #
    if t.semaphore_name not in t.job_limit_semaphores:
        return None


    #
    #   create semaphore if not yet created
    #
    if t.semaphore_name not in job_limit_semaphores:
        maximum_jobs_num = t.job_limit_semaphores[t.semaphore_name]
        job_limit_semaphores[t.semaphore_name] = syncmanager.BoundedSemaphore(maximum_jobs_num)
    return job_limit_semaphores[t.semaphore_name]

#_________________________________________________________________________________________
#
#   Parameter generator for all jobs / tasks
#
#________________________________________________________________________________________
def make_job_parameter_generator (incomplete_tasks, task_parents, logger, forcedtorun_tasks,
                                    count_remaining_jobs, runtime_data, verbose,
                                    syncmanager,
                                    one_second_per_job, touch_files_only):

    inprogress_tasks = set()
    job_limit_semaphores = dict()

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
                    log_at_level (logger, 3, verbose, "Task enters queue = " + task_name + (": Forced to rerun" if force_rerun else ""))
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
                    if (t.active_if_checks != None):
                        t.is_active = all(arg() if isinstance(arg, collections.Callable) else arg
                                            for arg in t.active_if_checks)
                    if not t.is_active:
                        parameters = []



                    #
                    #   If no parameters: just call task function (empty list)
                    #
                    elif t.param_generator_func == None:
                        parameters = ([[], []],)
                    else:
                        parameters = t.param_generator_func(runtime_data)

                    #
                    #   iterate through parameters
                    #
                    cnt_jobs_created = 0
                    for param, descriptive_param in parameters:

                        #
                        #   save output even if uptodate
                        #
                        if len(param) >= 2:
                            t.output_filenames.append(param[1])

                        job_name = t.job_descriptor(descriptive_param, runtime_data)

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

                        # pause for one second before first job of each tasks
                        if one_second_per_job and cnt_jobs_created == 0:
                            log_at_level (logger, 10, verbose, "   1 second PAUSE in job_parameter_generator\n\n\n")
                            time.sleep(1.01)


                        count_remaining_jobs[t] += 1
                        cnt_jobs_created += 1
                        cnt_jobs_created_for_all_tasks += 1
                        yield (param,
                                t._name,
                                job_name,
                                t.job_wrapper,
                                t.user_defined_work_func,
                                get_semaphore (t, job_limit_semaphores, syncmanager),
                                one_second_per_job,
                                touch_files_only)

                    # if no job came from this task, this task is complete
                    #   we need to retire it here instead of normal completion at end of job tasks
                    #   precisely because it created no jobs
                    if cnt_jobs_created == 0:
                        incomplete_tasks.remove(t)
                        t.completed (logger, True)

                        #
                        #   Add extra warning if no regular expressions match:
                        #   This is a common class of frustrating errors
                        #
                        if (verbose >= 1 and "ruffus_WARNING" in runtime_data and
                            t.param_generator_func in runtime_data["ruffus_WARNING"]):
                            for msg in runtime_data["ruffus_WARNING"][t.param_generator_func]:
                                logger.warning("    'In Task def %s(...):' %s " % (task_name, msg))


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
def feed_job_params_to_process_pool_factory (parameter_q, logger, verbose):
    """
    Process pool gets its parameters from this generator
    Use factory function to save parameter_queue
    """
    def feed_job_params_to_process_pool ():
        log_at_level (logger, 10, verbose, "   Send param to Pooled Process START")
        while 1:
            log_at_level (logger, 10, verbose, "   Get next parameter size = %d" %
                                                        parameter_q.qsize())
            if not parameter_q.qsize():
                time.sleep(0.1)
            param = parameter_q.get()
            log_at_level (logger, 10, verbose, "   Get next parameter done")

            # all tasks done
            if isinstance(param, all_tasks_complete):
                break

            log_at_level (logger, 10, verbose, "   Send param to Pooled Process=>" + str(param[0]))
            yield param

        log_at_level (logger, 10, verbose, "   Send param to Pooled Process END")

    # return generator
    return feed_job_params_to_process_pool

#_________________________________________________________________________________________
#
#   fill_queue_with_job_parameters
#
#________________________________________________________________________________________
def fill_queue_with_job_parameters (job_parameters, parameter_q, POOL_SIZE, logger, verbose):
    """
    Ensures queue is filled with number of parameters > jobs / slots (POOL_SIZE)
    """
    log_at_level (logger, 10, verbose, "    fill_queue_with_job_parameters START")
    for param in job_parameters:

        # stop if no more jobs available
        if isinstance(param, waiting_for_more_tasks_to_complete):
            log_at_level (logger, 10, verbose, "    fill_queue_with_job_parameters WAITING for task to complete")
            break

        if not isinstance(param, all_tasks_complete):
            log_at_level (logger, 10, verbose, "    fill_queue_with_job_parameters=>" + str(param[0]))

        # put into queue
        parameter_q.put(param)

        # queue size needs to be at least 2 so that the parameter queue never consists of a single
        #   waiting_for_task_to_complete entry which will cause
        #   a loop and everything to hang!
        if parameter_q.qsize() > POOL_SIZE + 1:
            break
    log_at_level (logger, 10, verbose, "    fill_queue_with_job_parameters END")


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
                 gnu_make_maximal_rebuild_mode  = True, verbose = 1,
                 runtime_data = None, one_second_per_job = True, touch_files_only = False):
    """
    Run pipelines.

    :param target_tasks: targets task functions which will be run if they are out-of-date
    :param forcedtorun_tasks: task functions which will be run whether or not they are out-of-date
    :param multiprocess: The number of concurrent jobs
    :param logger: Where progress will be logged. Defaults to stderr output.
    :type logger: `logging <http://docs.python.org/library/logging.html>`_ objects
    :param gnu_make_maximal_rebuild_mode: Defaults to re-running *all* out-of-date tasks. Runs minimal
                                          set to build targets if set to ``True``. Use with caution.
    :param verbose: level 0 : nothing
                    level 1 : logs task names and warnings
                    level 2 : logs task description if exists
                    level 3 : logs job names for jobs to be run
                    level 4 : logs list of up-to-date tasks and job names for jobs to be run
                    level 5 : logs job names for all jobs whether up-to-date or not
                    level 10: logs messages useful only for debugging ruffus pipeline code
    :param runtime_data: Experimental feature for passing data to tasks at run time
    :param one_second_per_job: Defaults to (true) forcing jobs to take a minimum of 1 second to complete
    :param touch_file_only: Create or update input/output files only to simulate running the pipeline. Do not run jobs

    """
    syncmanager = multiprocessing.Manager()

    if runtime_data == None:
        runtime_data = {}
    if not isinstance(runtime_data, dict):
        raise Exception("pipeline_run parameter runtime_data should be a dictionary of "
                        "values passes to jobs at run time.")

    if verbose == 0:
        logger = black_hole_logger
    elif verbose >= 11:
        if hasattr(logger, "add_unique_prefix"):
            logger.add_unique_prefix()

    if touch_files_only and verbose >= 1:
        logger.info("Touch output files instead of remaking them.")

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
                                                        extra_data_for_signal = t_verbose_logger(verbose, logger, runtime_data))

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
                                                        count_remaining_jobs,
                                                        runtime_data, verbose,
                                                        syncmanager,
                                                        one_second_per_job,
                                                        touch_files_only)
    job_parameters = parameter_generator()
    fill_queue_with_job_parameters(job_parameters, parameter_q, multiprocess, logger, verbose)

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



    feed_job_params_to_process_pool = feed_job_params_to_process_pool_factory (parameter_q, logger, verbose)

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
            fill_queue_with_job_parameters(job_parameters, parameter_q, multiprocess, logger, verbose)




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




