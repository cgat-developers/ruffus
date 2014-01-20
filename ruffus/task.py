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

Initial implementation of @active_if by Jacob Biesinger

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
from multiprocessing.pool import ThreadPool
import traceback
import types
from itertools import imap
import textwrap
import time
from multiprocessing.managers import SyncManager
from contextlib import contextmanager
import cPickle as pickle
import dbdict


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
    def info (self, message, *args, **kwargs):
        pass
    def debug (self, message, *args, **kwargs):
        pass
    def warning (self, message, *args, **kwargs):
        pass
    def error (self, message, *args, **kwargs):
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
    def error (self, message):
        sys.stderr.write("\n\n" + self.unique_prefix + "ERROR:\n    " + message + "\n\n")
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
    def error (self, message):
        sys.stream.write("\n\nERROR:\n    " + message + "\n\n")
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

class subdivide(task_decorator):
    pass

class originate(task_decorator):
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
class mkdir(task_decorator):
    #def __init__ (self, *args):
    #    self.args = args
    pass

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

#           given parameters, returns strings describing job
#           First returned parameter is string in strong form
#           Second returned parameter is a list of strings for input, output and extra parameters
#               intended to be reformatted with indentation
#           main use in error logging

#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888
def generic_job_descriptor (param, runtime_data):
    if param in ([], None):
        m = "Job"
    else:
        m = "Job  = %s" % ignore_unknown_encoder(param)

    return m, [m]

def io_files_job_descriptor (param, runtime_data):
    extra_param = ", " + shorten_filenames_encoder(param[2:])[1:-1] if len(param) > 2 else ""
    out_param   =        shorten_filenames_encoder(param[1])        if len(param) > 1 else "??"
    in_param    =        shorten_filenames_encoder(param[0])        if len(param) > 0 else "??"

    return ("Job  = [%s -> %s%s]" % (in_param, out_param, extra_param),
            ["Job  = [%s" % in_param, "-> " + out_param + extra_param + "]"])


def io_files_one_to_many_job_descriptor (param, runtime_data):

    extra_param = ", " + shorten_filenames_encoder(param[2:])[1:-1] if len(param) > 2 else ""
    out_param   =        shorten_filenames_encoder(param[1])        if len(param) > 1 else "??"
    in_param    =        shorten_filenames_encoder(param[0])        if len(param) > 0 else "??"

    # start with input parameter
    ret_params = ["Job  = [%s" % in_param]

    # add output parameter to list,
    #   processing one by one if multiple output parameters
    if len(param) > 1:
        if isinstance(param[1], (list, tuple)):
            ret_params.extend("-> " + shorten_filenames_encoder(p) for p in param[1])
        else:
            ret_params.append("-> " + out_param)

    # add extra
    if len(param) > 2 :
        ret_params.append(" , " + shorten_filenames_encoder(param[2:])[1:-1])

    # add closing bracket
    ret_params[-1] +="]"

    return ("Job  = [%s -> %s%s]" % (in_param, out_param, extra_param), ret_params)


def mkdir_job_descriptor (param, runtime_data):
    # input, output and parameters
    if len(param) == 1:
        m = "Make directories %s" % (shorten_filenames_encoder(param[0]))
    elif len(param) == 2:
        m = "Make directories %s" % (shorten_filenames_encoder(param[1]))
    else:
        return [], []
    return m, [m]


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
def job_wrapper_io_files(param, user_defined_work_func, register_cleanup, touch_files_only, output_files_only = False):
    """
    run func on any i/o if not up to date
    """
    assert(user_defined_work_func)

    i,o = param[0:2]

    if touch_files_only == 0:
        # @originate only uses output files
        if output_files_only:
            ret_val = user_defined_work_func(*(param[1:]))
        # all other decorators
        else:
            ret_val = user_defined_work_func(*param)
    elif touch_files_only == 1:
        #job_history = dbdict.open(RUFFUS_HISTORY_FILE, picklevalues=True)

        #
        #   touch files only
        #
        for f in get_strings_in_nested_sequence(o):
            #
            #   race condition still possible...
            #
            with file(f, 'a'):
                os.utime(f, None)
            #if not os.path.exists(f):
            #    open(f, 'w')
            #    mtime = os.path.getmtime(f)
            #else:
            #    os.utime(f, None)
            #    mtime = os.path.getmtime(f)


            #chksum = JobHistoryChecksum(f, mtime, param[2:], user_defined_work_func.pipeline_task)
            #job_history[f] = chksum  # update file times and job details in history



    #
    # register strings in output file for cleanup
    #
    for f in get_strings_in_nested_sequence(o):
        register_cleanup(f, "file")


#_________________________________________________________________________________________

#   job wrapper for all that only deals with output files

#_________________________________________________________________________________________
def job_wrapper_output_files(param, user_defined_work_func, register_cleanup, touch_files_only):
    """
    run func on any output file if not up to date
    """
    job_wrapper_io_files(param, user_defined_work_func, register_cleanup, touch_files_only, output_files_only = True)


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
    if len(param) == 1:
        dirs = param[0]

    # if there are two parameters, they are i/o, and the directories to be created are the output
    elif len(param) == 2:
        dirs = param[1]
    else:
        raise Exception("Wrong number of arguments in mkdir check %s" % (param,))

    # get all file names in flat list
    dirs = get_strings_in_nested_sequence (dirs)

    for d in dirs:
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
        't_job_result(task_name, state, job_name, return_value, exception, params)'

        __slots__ = ()

        fields = ('task_name', 'state', 'job_name', 'return_value', 'exception', 'params')

        def __new__(cls, task_name, state, job_name, return_value, exception, params):
            return tuple.__new__(cls, (task_name, state, job_name, return_value, exception, params))

        @classmethod
        def make(cls, iterable, new=tuple.__new__, len=len):
            'Make a new t_job_result object from a sequence or iterable'
            result = new(cls, iterable)
            if len(result) != 6:
                raise TypeError('Expected 6 arguments, got %d' % len(result))
            return result

        def __repr__(self):
            return 't_job_result(task_name=%r, state=%r, job_name=%r, return_value=%r, exception=%r, params=%r)' % self

        def asdict(t):
            'Return a new dict which maps field names to their values'
            return {'task_name': t[0], 'state': t[1], 'job_name': t[2], 'return_value': t[3], 'exception': t[4], 'params':t[5]}

        def replace(self, **kwds):
            'Return a new t_job_result object replacing specified fields with new values'
            result = self.make(map(kwds.pop, ('task_name', 'state', 'job_name', 'return_value', 'exception', 'params'), self))
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
        params      = property(itemgetter(5))



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
            job_limit_semaphore, touch_files_only) = process_parameters

    ##job_history = dbdict.open(RUFFUS_HISTORY_FILE, picklevalues=True)
    ##outfile = param[1] if len(param) > 1 else None   # mkdir has no output
    ##if not isinstance(outfile, list):
    ##    outfile = [outfile]
    ##for o in outfile:
    ##    job_history.pop(o, None)  # remove outfile from history if it exists

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
            return t_job_result(task_name, JOB_COMPLETED, job_name, return_value, None, param)
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
                             exception_stack], param)



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
                    "task_product",
                    "task_permutations",
                    "task_combinations",
                    "task_combinations_with_replacement",
                    "task_subdivide",
                    "task_originate",
                    ]
    action_unspecified                          =  0
    action_task                                 =  1
    action_task_files_re                        =  2
    action_task_split                           =  3
    action_task_merge                           =  4
    action_task_transform                       =  5
    action_task_collate                         =  6
    action_task_files_func                      =  7
    action_task_files                           =  8
    action_mkdir                                =  9
    action_parallel                             = 10
    action_active_if                            = 11
    action_task_product                         = 12
    action_task_permutations                    = 13
    action_task_combinations                    = 14
    action_task_combinations_with_replacement   = 15
    action_task_subdivide                       = 16
    action_task_originate                       = 17



    multiple_jobs_outputs    = 0
    single_job_single_output = 1
    job_single_matches_parent= 2

    job_limit_semaphores = {}

    checksum_level = CHECKSUM_FILE_TIMESTAMPS


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
        module_name = str(func.__module__)
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
        return _task.action_names[self._action_type]

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

    #   get_job_name

    #_________________________________________________________________________________________
    def get_job_name(self, descriptive_param, runtime_data):
        """
        Use job descriptor to return short name for job, including any parameters

            runtime_data is not (yet) used but may be used to add context in future
        """
        return self.job_descriptor(descriptive_param, runtime_data)[0]


    #_________________________________________________________________________________________

    #   get_task_name

    #_________________________________________________________________________________________
    def get_task_name(self, in_func_format = False):
        """
        Returns name of task function, removing __main__ namespace if necessary

        if in_func_format is true, will return def task_func(...):

        """

        task_name = self._name.replace("__main__.", "")
        if self._action_type != _task.action_mkdir and in_func_format:
            return "def %s(...):" % task_name
        else:
            return task_name



    #_________________________________________________________________________________________

    #   update_active_state

    #_________________________________________________________________________________________
    def update_active_state (self):
        #
        #   If has an @active_if decorator, check if the task needs to be run
        #       @active_if parameters may be call back functions or booleans
        #
        if (self.active_if_checks != None and
            any( not arg() if isinstance(arg, collections.Callable) else not arg
                     for arg in self.active_if_checks)):
                # flip is active to false.
                #   ( get_output_files() will return empty if inactive )
                #   Remember each iteration of pipeline_printout pipeline_run will have
                #   another bite at changing this value
                self.is_active = False
        else:
            # flip is active to True so that downstream dependencies will be correct
            #   ( get_output_files() will return empty if inactive )
            #   Remember each iteration of pipeline_printout pipeline_run will have
            #   another bite at changing this value
            self.is_active = True



    #_________________________________________________________________________________________

    #   printout

    #_________________________________________________________________________________________
    def printout (self, runtime_data, force_rerun, job_history, verbose=1, indent = 4):
        """
        Print out all jobs for this task

                verbose = 1 : print task name
                          2 : print task description if exists
                          3 : print job names for jobs to be run
                          4 : print job names for up-to- date jobs
        """

        def get_job_names (param, indent_str):
            job_names = self.job_descriptor(param, runtime_data)[1]
            if len(job_names) > 1:
                job_names = ([indent_str + job_names[0]]  +
                             [indent_str + "      " + jn for jn in job_names[1:]])
            else:
                job_names = ([indent_str + job_names[0]])
            return job_names



        if not verbose:
            return []

        indent_str = ' ' * indent

        messages = []

        messages.append("Task = " + self.get_task_name() + ("    >>Forced to rerun<<" if force_rerun else ""))
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
        if not self.is_active:
            if verbose <= 3:
                return messages
            messages.append(indent_str + "Task is inactive")
            # add spacer line
            messages.append("")
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

            if self.needs_update_func == needs_update_check_modify_time:
                needs_update, msg = self.needs_update_func (task=self, job_history = job_history)
            else:
                needs_update, msg = self.needs_update_func ()

            if needs_update:
                messages.append(indent_str + "Task needs update: %s" % msg)
            else:
                messages.append(indent_str + "Task up-to-date")

        else:
            runtime_data["MATCH_FAILURE"] = []
            #
            #   return messages description per job
            #
            cnt_jobs = 0
            for param, descriptive_param in self.param_generator_func(runtime_data):
                cnt_jobs += 1

                #
                #   needs update func = None: always needs update
                #
                if not self.needs_update_func:
                    messages.extend(get_job_names (descriptive_param, indent_str))
                    messages.append(indent_str + "  Jobs needs update: No function to check if up-to-date or not")
                    continue

                if self.needs_update_func == needs_update_check_modify_time:
                    needs_update, msg = self.needs_update_func (*param, task=self, job_history = job_history)
                else:
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
            if verbose >= 3 or (verbose and cnt_jobs == 0):
                if runtime_data and "MATCH_FAILURE" in runtime_data:
                    for s in runtime_data["MATCH_FAILURE"]:
                        messages.append(indent_str + "Warning: File match failure: " + s)
            runtime_data["MATCH_FAILURE"] = []
        messages.append("")
        return messages




    #_____________________________________________________________________________________

    #   signal
    #
    #       returns whether up to date
    #
    #_____________________________________________________________________________________
    def signal (self, verbose_logger_job_history):
        """
        If up to date: signal = true
        If true, depth first search will not pass through this node
        """
        if not verbose_logger_job_history:
            raise Exception("verbose_logger_job_history is None")

        verbose_logger = verbose_logger_job_history[0]
        job_history = verbose_logger_job_history[1]

        try:
            logger       = verbose_logger.logger
            verbose      = verbose_logger.verbose
            runtime_data = verbose_logger.runtime_data
            log_at_level (logger, 4, verbose,
                            "  Task = " + self.get_task_name())

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
                    if self.needs_update_func == needs_update_check_modify_time:
                        needs_update, msg = self.needs_update_func (task=self, job_history = job_history)
                    else:
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
                    if self.needs_update_func == needs_update_check_modify_time:
                        needs_update, msg = self.needs_update_func (*param, task=self, job_history = job_history)
                    else:
                        needs_update, msg = self.needs_update_func (*param)
                    if needs_update:
                        if verbose >= 4:
                            job_name = self.get_job_name(descriptive_param, runtime_data)
                            log_at_level (logger, 4, verbose,
                                            "    Needing update:\n      %s" % job_name)
                        return False

                #
                #   Percolate warnings from parameter factories
                #
                if (verbose >= 1 and "ruffus_WARNING" in runtime_data and
                    self.param_generator_func in runtime_data["ruffus_WARNING"]):
                    for msg in runtime_data["ruffus_WARNING"][self.param_generator_func]:
                        logger.warning("    'In Task %s' %s " % (self.get_task_name(True), msg))


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
                        # make sure each @split or @subdivide or @originate returns a list of jobs
                        #   i.e. each @split or @subdivide or @originate is always a ->many operation
                        #       even if len(many) can be 1 (or zero)
                        if self.indeterminate_output and not non_str_sequence(param[1]):
                            self.output_filenames.append([param[1]])
                        else:
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
        if not self.is_active:
            logger.info("Inactive Task = " + self.get_task_name())
            self.output_filenames = None
            return

        for f in self.posttask_functions:
            f()
        if jobs_uptodate:
            logger.info("Uptodate Task = " + self.get_task_name())
        else:
            logger.info("Completed Task = " + self.get_task_name())


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

    #   do_task_subdivide

    #_________________________________________________________________________________________
    def do_task_subdivide (self, orig_args, decorator_name, error_type):
        """
            @subdivide and @split are synonyms
            Common code here
        """

        if len(orig_args) < 3:
            raise error_type(self, "Too few arguments for %s" % decorator_name)




        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])

        #   allows split to take a single file or task
        input_files_task_globs.single_file_to_list()

        # how to transform input to output file name
        file_names_transform = self.choose_file_names_transform (orig_args[1], error_type, decorator_name)

        orig_args = orig_args[2:]

        #   inputs can also be defined by pattern match
        extra_inputs, replace_inputs, output_pattern, extra_params = self.get_extra_inputs_outputs_extra (orig_args, error_type, decorator_name)

        #
        #   output globs will be replaced with files. But there should not be tasks here!
        #
        output_files_task_globs = self.handle_tasks_globs_in_inputs(output_pattern)
        if len(output_files_task_globs.tasks):
            raise error_type(self, ("%s cannot output to another task. "
                                          "Do not include tasks in output parameters.") % decorator_name)



        self.param_generator_func = subdivide_param_factory (   input_files_task_globs,
                                                                False, # flatten input
                                                                file_names_transform,
                                                                extra_inputs,
                                                                replace_inputs,
                                                                output_files_task_globs,
                                                                *extra_params)
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        #self.job_descriptor       = io_files_job_descriptor # (orig_args[0], output_runtime_data_names)
        self.job_descriptor       = io_files_one_to_many_job_descriptor

        # output is a glob
        self.indeterminate_output = 2
        self.single_multi_io       = self.many_to_many

    #_________________________________________________________________________________________

    #   task_split

    #_________________________________________________________________________________________
    def do_task_simple_split (self, orig_args, decorator_name, error_type):

        #check enough arguments
        if len(orig_args) < 2:
            raise error_type(self, "Too few arguments for %s" % decorator_name)

        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])

        #
        #   replace output globs with files
        #
        output_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[1])
        if len(output_files_task_globs.tasks):
            raise error_type(self, ("%s cannot output to another task. "
                                    "Do not include tasks in output parameters.") % decorator_name)

        extra_params = orig_args[2:]
        self.param_generator_func = split_param_factory (input_files_task_globs, output_files_task_globs, *extra_params)


        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        #self.job_descriptor       = io_files_job_descriptor# (orig_args[1], output_runtime_data_names)
        self.job_descriptor       = io_files_one_to_many_job_descriptor

        # output is a glob
        self.indeterminate_output = 1
        self.single_multi_io       = self.one_to_many



    #_________________________________________________________________________________________

    #   task_split

    #_________________________________________________________________________________________
    def task_split (self, orig_args):
        """
        Splits a single set of input files into multiple output file names,
            where the number of output files may not be known beforehand.
        """
        decorator_name  = "@split"
        error_type      = error_task_split
        self.set_action_type (_task.action_task_split)

        #
        #   This is actually @subdivide
        #
        if isinstance(orig_args[1], regex):
            self.do_task_subdivide(orig_args, decorator_name, error_type)

        #
        #   This is actually @split
        #
        else:
            self.do_task_simple_split(orig_args, decorator_name, error_type)



    #_________________________________________________________________________________________

    #   task_originate

    #_________________________________________________________________________________________
    def task_originate (self, orig_args):
        """
        Splits out multiple output file names,
            where the number of output files may or may not be known beforehand.
            This is a synonym for @split(None,...)
        """
        decorator_name  = "@originate"
        error_type      = error_task_originate
        self.set_action_type (_task.action_task_originate)

        if len(orig_args) < 1:
            raise error_type(self, "%s takes a single argument" % decorator_name)

        output_params = orig_args[0]

        # make sure output_params is a list.
        # Each of these will be called as an output
        if not non_str_sequence (output_params):
            output_params = [output_params]

        #
        #   output globs will be replaced with files. But there should not be tasks here!
        #
        list_output_files_task_globs = [self.handle_tasks_globs_in_inputs(oo) for oo in output_params]
        for oftg in list_output_files_task_globs:
            if len(oftg.tasks):
                raise error_type(self, ("%s cannot output to another task. "
                                              "Do not include tasks in output parameters.") % decorator_name)

        self.param_generator_func = originate_param_factory (list_output_files_task_globs, orig_args[1:])
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_output_files
        self.job_descriptor       = io_files_one_to_many_job_descriptor

        # output is not a glob
        self.indeterminate_output = 0
        self.single_multi_io       = self.many_to_many







    #_________________________________________________________________________________________

    #   task_subdivide

    #_________________________________________________________________________________________
    def task_subdivide (self, orig_args):
        """
        Splits a single set of input files into multiple output file names,
            where the number of output files may not be known beforehand.
        """
        decorator_name  = "@subdivide"
        error_type      = error_task_subdivide
        self.set_action_type (_task.action_task_subdivide)
        self.do_task_subdivide(orig_args, decorator_name, error_type)

    #_________________________________________________________________________________________

    #   get_extra_inputs

    #_________________________________________________________________________________________
    def get_extra_inputs_outputs_extra (self, orig_args, error_type, decorator_name):
        """
        shared code for subdivide, transform, product etc for parsing orig_args into
            add_inputs/inputs, output, extra
        """

        #
        #   inputs can also be defined by pattern match
        #
        if isinstance(orig_args[0], inputs):
            if len(orig_args) < 2:
                raise error_type(self, "Too few arguments for %s" % decorator_name)
            if len(orig_args[0].args) != 1:
                raise error_task_transform_inputs_multiple_args(self,
                                    "inputs(...) expects only a single argument. "
                                    "This can be, for example, a file name, "
                                    "a regular expression pattern, or any "
                                    "nested structure. If the intention was to "
                                    "specify a tuple as the input parameter, "
                                    "please wrap the elements of the tuple "
                                    "in brackets in the decorator\n\n"
                                    "%s(..., inputs(...), ...)\n" % (decorator_name))
            replace_inputs = t_extra_inputs.REPLACE_INPUTS
            extra_inputs = self.handle_tasks_globs_in_inputs(orig_args[0].args[0])
            output_pattern = orig_args[1]
            extra_params = orig_args[2:]
        elif isinstance(orig_args[0], add_inputs):
            if len(orig_args) < 2:
                raise error_type(self, "Too few arguments for %s" % decorator_name)
            replace_inputs = t_extra_inputs.ADD_TO_INPUTS
            extra_inputs = self.handle_tasks_globs_in_inputs(orig_args[0].args)
            output_pattern = orig_args[1]
            extra_params = orig_args[2:]
        else:
            replace_inputs = t_extra_inputs.KEEP_INPUTS
            extra_inputs = None
            output_pattern = orig_args[0]
            extra_params = orig_args[1:]

        return extra_inputs, replace_inputs, output_pattern, extra_params

    #_________________________________________________________________________________________

    #   choose_file_names_transform

    #_________________________________________________________________________________________
    def choose_file_names_transform (self, file_name_transform_tag, error_type, decorator_name, valid_tags = (regex, suffix, formatter)):
        """
        shared code for subdivide, transform, product etc for choosing method for transform input file to output files
        """
        valid_tag_names = [];
        # regular expression match
        if (regex in valid_tags):
            valid_tag_names.append("regex()")
            if isinstance(file_name_transform_tag, regex):
                return t_regex_file_names_transform(self, file_name_transform_tag, error_type, decorator_name)

        # simulate end of string (suffix) match
        if (suffix in valid_tags):
            valid_tag_names.append("suffix()")
            if isinstance(file_name_transform_tag, suffix):
                return t_suffix_file_names_transform(self, file_name_transform_tag, error_type, decorator_name)

        # new style string.format()
        if (formatter in valid_tags):
            valid_tag_names.append("formatter()")
            if isinstance(file_name_transform_tag, formatter):
                return t_formatter_file_names_transform(self, file_name_transform_tag, error_type, decorator_name)

        raise error_type(self, "%s expects one of %s as the second argument" % (decorator_name, ", ".join(valid_tag_names)))


    #_________________________________________________________________________________________

    #   task_product

    #_________________________________________________________________________________________
    def task_product(self, orig_args):
        """
        all versus all
        """
        decorator_name  = "@product"
        error_type      = error_task_product
        if len(orig_args) < 3:
            raise error_type(self, "Too few arguments for %s" % decorator_name)

        #
        #   get all pairs of tasks / globs and formatter()
        #
        list_input_files_task_globs = []
        list_formatter = []
        while len(orig_args) >= 3:
            if isinstance(orig_args[1], formatter):
                list_input_files_task_globs .append(orig_args[0])
                list_formatter              .append(orig_args[1])
                orig_args = orig_args[2:]
            else:
                break

        if not len(list_formatter):
            raise error_task_product(self, "@product expects formatter() as the second argument")


        self.set_action_type (_task.action_task_product)

        #
        # replace function / function names with tasks
        #
        list_input_files_task_globs = [self.handle_tasks_globs_in_inputs(ii) for ii in list_input_files_task_globs]


        # list of new style string.format()
        file_names_transform = t_nested_formatter_file_names_transform(self, list_formatter, error_task_product, decorator_name)


        #
        #   inputs can also be defined by pattern match
        #
        extra_inputs, replace_inputs, output_pattern, extra_params = self.get_extra_inputs_outputs_extra (orig_args, error_type, decorator_name)

        self.param_generator_func = product_param_factory ( list_input_files_task_globs,
                                                            False, # flatten input
                                                            file_names_transform,
                                                            extra_inputs,
                                                            replace_inputs,
                                                            output_pattern,
                                                            *extra_params)
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        self.single_multi_io      = self.many_to_many


    #_________________________________________________________________________________________

    #   task_combinatorics

    #_________________________________________________________________________________________
    def task_combinatorics (self, orig_args, combinatorics_type, decorator_name, error_type):
        """
            Common code for task_permutations, task_combinations_with_replacement, task_combinations
        """

        if len(orig_args) < 4:
            raise error_type(self, "Too few arguments for %s" % decorator_name)


        if not isinstance(orig_args[1], formatter):
            raise error_task_product(self, "%s expects formatter() as the second argument" % decorator_name)

        #
        # replace function / function names with tasks
        #
        input_files_task_globs  = self.handle_tasks_globs_in_inputs(orig_args[0])

        k_tuple = orig_args[2]

        # how to transform input to output file name: len(k-tuples) of (identical) formatters
        file_names_transform = t_nested_formatter_file_names_transform(self, [orig_args[1]] * k_tuple, error_type, decorator_name)


        self.set_action_type (_task.action_task_permutations)

        if not isinstance(orig_args[2], int):
            raise error_task_product(self, "%s expects an integer number as the third argument specifying the number of elements in each tuple." % decorator_name)


        orig_args = orig_args[3:]


        #
        #   inputs can also be defined by pattern match
        #
        extra_inputs, replace_inputs, output_pattern, extra_params = self.get_extra_inputs_outputs_extra (orig_args, error_type, decorator_name)

        self.param_generator_func = combinatorics_param_factory (   input_files_task_globs,
                                                                    False, # flatten input
                                                                    combinatorics_type,
                                                                    k_tuple,
                                                                    file_names_transform,
                                                                    extra_inputs,
                                                                    replace_inputs,
                                                                    output_pattern,
                                                                    *extra_params)
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        self.single_multi_io      = self.many_to_many

    #_________________________________________________________________________________________

    #   task_permutations

    #_________________________________________________________________________________________
    def task_permutations(self, orig_args):
        """
            k-permutations of n

            k-length tuples, all possible orderings, no self vs self
        """
        decorator_name      = "@permutations"
        error_type          = error_task_permutations
        combinatorics_type  = t_combinatorics_type.COMBINATORICS_PERMUTATIONS
        self.task_combinatorics (orig_args, combinatorics_type, decorator_name, error_type)


    #_________________________________________________________________________________________

    #   task_combinations

    #_________________________________________________________________________________________
    def task_combinations(self, orig_args):
        """
            k-length tuples
                Single (sorted) ordering, i.e. AB is the same as BA,
                No repeats. No AA, BB

            E.g.
                combinations("ABCD", 3) = ['ABC', 'ABD', 'ACD', 'BCD']
                combinations("ABCD", 2) = ['AB', 'AC', 'AD', 'BC', 'BD', 'CD']
        """
        decorator_name      = "@combinations"
        error_type          = error_task_combinations
        combinatorics_type  = t_combinatorics_type.COMBINATORICS_COMBINATIONS
        self.task_combinatorics (orig_args, combinatorics_type, decorator_name, error_type)


    #_________________________________________________________________________________________

    #   task_combinations_with_replacement

    #_________________________________________________________________________________________
    def task_combinations_with_replacement(self, orig_args):
        """
            k-length tuples
                Single (sorted) ordering, i.e. AB is the same as BA,
                Repeats. AA, BB, AAC etc.

            E.g.
                combinations_with_replacement("ABCD", 3) = ['AAA', 'AAB', 'AAC', 'AAD',
                                                            'ABB', 'ABC', 'ABD',
                                                            'ACC', 'ACD',
                                                            'ADD',
                                                            'BBB', 'BBC', 'BBD',
                                                            'BCC', 'BCD',
                                                            'BDD',
                                                            'CCC', 'CCD',
                                                            'CDD',
                                                            'DDD']
                combinations_with_replacement("ABCD", 2) = ['AA', 'AB', 'AC', 'AD',
                                                            'BB', 'BC', 'BD',
                                                            'CC', 'CD',
                                                            'DD']

        """
        decorator_name      = "@combinations_with_replacement"
        error_type          = error_task_combinations_with_replacement
        combinatorics_type  = t_combinatorics_type.COMBINATORICS_COMBINATIONS_WITH_REPLACEMENT
        self.task_combinatorics (orig_args, combinatorics_type, decorator_name, error_type)




    #_________________________________________________________________________________________

    #   task_transform

    #_________________________________________________________________________________________
    def task_transform (self, orig_args):
        """
        Merges multiple input files into a single output.
        """
        decorator_name  = "@transform"
        error_type      = error_task_transform
        if len(orig_args) < 3:
            raise error_type(self, "Too few arguments for %s" % decorator_name)


        self.set_action_type (_task.action_task_transform)

        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])


        #_________________________________________________________________________________
        #
        #       single_job_single_output is bad policy. Can we remove it?
        #       What does this actually mean in Ruffus semantics?
        #
        #
        #   allows transform to take a single file or task
        if input_files_task_globs.single_file_to_list():
            self._single_job_single_output = self.single_job_single_output

        #
        #   whether transform generates a list of jobs or not will depend on the parent task
        #
        elif isinstance(input_files_task_globs.params, _task):
            self._single_job_single_output = input_files_task_globs.params

        #_________________________________________________________________________________

        # how to transform input to output file name
        file_names_transform = self.choose_file_names_transform (orig_args[1], error_task_transform, decorator_name)

        orig_args = orig_args[2:]


        #
        #   inputs can also be defined by pattern match
        #
        extra_inputs, replace_inputs, output_pattern, extra_params = self.get_extra_inputs_outputs_extra (orig_args, error_type, decorator_name)

        self.param_generator_func = transform_param_factory (   input_files_task_globs,
                                                                False, # flatten input
                                                                file_names_transform,
                                                                extra_inputs,
                                                                replace_inputs,
                                                                output_pattern,
                                                                *extra_params)
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        self.single_multi_io      = self.many_to_many

    #_________________________________________________________________________________________

    #   task_collate

    #_________________________________________________________________________________________
    def task_collate (self, orig_args):
        """
        Merges multiple input files into a single output.
        """
        decorator_name = "@collate"
        error_type      = error_task_collate
        if len(orig_args) < 3:
            raise error_type(self, "Too few arguments for %s" % decorator_name)

        self.set_action_type (_task.action_task_collate)

        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])


        # how to transform input to output file name
        file_names_transform = self.choose_file_names_transform (orig_args[1], error_task_collate, decorator_name, (regex, formatter))

        orig_args = orig_args[2:]

        #
        #   inputs also defined by pattern match
        #
        extra_inputs, replace_inputs, output_pattern, extra_params = self.get_extra_inputs_outputs_extra (orig_args, error_type, decorator_name)

        self.single_multi_io           = self.many_to_many

        self.param_generator_func = collate_param_factory ( input_files_task_globs,
                                                            False, # flatten input
                                                            file_names_transform,
                                                            extra_inputs,
                                                            replace_inputs,
                                                            output_pattern,
                                                            *extra_params)
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

        file_names_transform = t_regex_file_names_transform(self, regex(orig_args[1]), error_task_files_re, "@files_re")


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
                                                                file_names_transform,
                                                                extra_input_files_task_globs,
                                                                t_extra_inputs.REPLACE_INPUTS,
                                                                *output_and_extras)
        else:

            self.single_multi_io           = self.many_to_many
            self.param_generator_func = transform_param_factory (input_files_task_globs,
                                                                    False,              # flatten
                                                                    file_names_transform,
                                                                    extra_input_files_task_globs,
                                                                    t_extra_inputs.REPLACE_INPUTS,
                                                                    *output_and_extras)


        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor



    #_________________________________________________________________________________________

    #   task_mkdir

    #       only called within task_follows

    #_________________________________________________________________________________________
    def task_mkdir (self, orig_args):
        self.cnt_task_mkdir += 1
        # give unique name to this instance of mkdir
        unique_name = r"(mkdir %d) before " % self.cnt_task_mkdir + self._name
        new_node = _task(self._module_name, unique_name)
        self.add_child(new_node)
        new_node.do_task_mkdir(orig_args)
        new_node.display_name = new_node._description


    def do_task_mkdir (self, orig_args):
        """
        list of directory names or a single argument which is aa list of directory names
        Creates directory if missing
        """
        decorator_name = "mkdir"
        error_type      = error_task_mkdir

        #   jump through hoops
        self.set_action_type (_task.action_mkdir)
        self.needs_update_func    = self.needs_update_func or needs_update_check_directory_missing
        self._description         = "Make directories %s" % (shorten_filenames_encoder(orig_args))
        self.job_wrapper          = job_wrapper_mkdir
        self.job_descriptor       = mkdir_job_descriptor

        # doesn't have a real function
        #  use job_wrapper just so it is not None
        self.user_defined_work_func = self.job_wrapper


        #
        # @transform like behaviour with regex / suffix or formatter
        #
        if len(orig_args) > 1 and isinstance(orig_args[1], (formatter, suffix, regex)):
            self.single_multi_io      = self.many_to_many

            if len(orig_args) < 3:
                raise error_type(self, "Too few arguments for %s" % decorator_name)

            #
            # replace function / function names with tasks
            #
            input_files_task_globs = self.handle_tasks_globs_in_inputs(orig_args[0])


            # how to transform input to output file name
            file_names_transform = self.choose_file_names_transform (orig_args[1], error_task_transform, decorator_name)

            orig_args = orig_args[2:]

            #
            #   inputs can also be defined by pattern match
            #
            extra_inputs, replace_inputs, output_pattern, extra_params = self.get_extra_inputs_outputs_extra (orig_args, error_type, decorator_name)

            if len(extra_params):
                raise error_type(self, "Too many arguments for %s" % decorator_name)


            self.param_generator_func = transform_param_factory (   input_files_task_globs,
                                                                    False, # flatten input
                                                                    file_names_transform,
                                                                    extra_inputs,
                                                                    replace_inputs,
                                                                    output_pattern,
                                                                    *extra_params)

        #
        # simple behaviour: just make directories in list of strings
        #
        # the mkdir decorator accepts one string, multiple strings or a list of strings
        else:
            self.single_multi_io        = self.one_to_one

            #
            #
            #
            # if a single argument collection of parameters, keep that as is
            if len(orig_args) == 0:
                mkdir_params = []
            elif len(orig_args) > 1:
                mkdir_params = orig_args
            # len(orig_args) == 1: unpack orig_args[0]
            elif non_str_sequence (orig_args[0]):
                mkdir_params = orig_args[0]
            # single string or other non collection types
            else:
                mkdir_params = orig_args

            #   all directories created in one job to reduce race conditions
            #    so we are converting [a,b,c] into [   [(a, b,c)]   ]
            #    where orig_args = (a,b,c)
            #   i.e. one job whose solitory argument is a tuple/list of directory names
            self.param_generator_func = args_param_factory([[sorted(mkdir_params)]])








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
                new_node.do_task_mkdir(arg.args)
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
            dependent_display_task_name = n._inward[0].get_task_name()
            if n._module_name in sys.modules:
                module = sys.modules[n._module_name]
                if hasattr(module, n._func_name):
                    n.user_defined_work_func = getattr(module, n._func_name)
                else:
                    raise error_decorator_args(("Module '%s' has no function '%s' in " +
                                                "\n@task_follows('%s')\ndef %s...") %
                                        (n._module_name, n._func_name, n.get_task_name(), dependent_display_task_name))
            else:
                raise error_decorator_args("Module '%s' not found in " +
                                        "\n@task_follows('%s')\ndef %s..." %
                                (n._module_name, n.get_task_name(), dependent_display_task_name))


        #
        # some jobs single state status mirrors parent's state
        #   and parent task not known until know
        #
        if isinstance(n._single_job_single_output, _task):
            n._single_job_single_output = n._single_job_single_output._single_job_single_output

#_________________________________________________________________________________________

#   update_checksum_level_on_tasks

#_________________________________________________________________________________________
def update_checksum_level_on_tasks (checksum_level):
    """Reset the checksum level for all tasks"""
    for n in node._all_nodes:
        n.checksum_level = checksum_level


#_________________________________________________________________________________________

#   update_active_states_for_all_tasks

#_________________________________________________________________________________________
def update_active_states_for_all_tasks ():
    """

    @active_if decorated tasks can change their active state every time
      pipeline_run / pipeline_printout / pipeline_printout_graph is called

    update_active_states_for_all_tasks ()

    """
    for n in node._all_nodes:
        n.update_active_state()

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
                raise error_function_is_not_a_task(("Function def %s(...): is not a pipelined task in ruffus." %
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
                             runtime_data                   = None,
                             checksum_level                 = CHECKSUM_HISTORY_TIMESTAMPS,
                             history_file                   = None):
                             # Remember to add further extra parameters here to "extra_pipeline_printout_graph_options" inside cmdline.py
                             # This will forward extra parameters from the command line to pipeline_printout_graph
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
    :param checksum_level: Several options for checking up-to-dateness are available: Default is level 1.
                    level 0 : Use only file timestamps
                    level 1 : above, plus timestamp of successful job completion
                    level 2 : above, plus a checksum of the pipeline function body
                    level 3 : above, plus a checksum of the pipeline function default arguments and the additional arguments passed in by task decorators
    """


    link_task_names_to_functions ()
    update_checksum_level_on_tasks (checksum_level)

    #
    # @active_if decorated tasks can change their active state every time
    #   pipeline_run / pipeline_printout / pipeline_printout_graph is called
    #
    update_active_states_for_all_tasks ()

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

    #
    #   If we aren't using checksums, and history file hasn't been specified,
    #       we might be a bit surprised to find Ruffus writing to a sqlite db anyway.
    #       Let us just use a in memory db which will be thrown away
    #   Of course, if history_file is specified, we presume you know what you are doing
    #
    if checksum_level == CHECKSUM_FILE_TIMESTAMPS and history_file == None:
        history_file = ':memory:'

    #
    # load previous job history if it exists, otherwise create an empty history
    #
    job_history = open_job_history (history_file)


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
                      extra_data_for_signal = [t_verbose_logger(0, None, runtime_data), job_history])



#_________________________________________________________________________________________

#   pipeline_printout

#_________________________________________________________________________________________
def pipeline_printout(  output_stream,
                        target_tasks,
                        forcedtorun_tasks               = [],
                        verbose                         = 1,
                        indent                          = 4,
                        gnu_make_maximal_rebuild_mode   = True,
                        wrap_width                      = 100,
                        runtime_data                    = None,
                        checksum_level                  = CHECKSUM_HISTORY_TIMESTAMPS,
                        history_file                    = None):
                      # Remember to add further extra parameters here to "extra_pipeline_printout_options" inside cmdline.py
                      # This will forward extra parameters from the command line to pipeline_printout
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
    :param checksum_level: Several options for checking up-to-dateness are available: Default is level 1.
                    level 0 : Use only file timestamps
                    level 1 : above, plus timestamp of successful job completion
                    level 2 : above, plus a checksum of the pipeline function body
                    level 3 : above, plus a checksum of the pipeline function default arguments and the additional arguments passed in by task decorators
    """
    if verbose == 0:
        return

    if not hasattr(output_stream, "write"):
        raise Exception("The first parameter to pipeline_printout needs to be an output file, e.g. sys.stdout and not %s" % str(output_stream))

    if runtime_data == None:
        runtime_data = {}
    if not isinstance(runtime_data, dict):
        raise Exception("pipeline_run parameter runtime_data should be a dictionary of "
                        "values passes to jobs at run time.")

    link_task_names_to_functions ()
    update_checksum_level_on_tasks(checksum_level)

    #
    # @active_if decorated tasks can change their active state every time
    #   pipeline_run / pipeline_printout / pipeline_printout_graph is called
    #
    update_active_states_for_all_tasks ()

    #
    #   target jobs
    #
    target_tasks = task_names_to_tasks ("Target", target_tasks)
    forcedtorun_tasks = task_names_to_tasks ("Forced to run", forcedtorun_tasks)

    logging_strm = t_verbose_logger(verbose, t_stream_logger(output_stream), runtime_data)

    #
    #   If we aren't using checksums, and history file hasn't been specified,
    #       we might be a bit surprised to find Ruffus writing to a sqlite db anyway.
    #       Let us just use a in memory db which will be thrown away
    #   Of course, if history_file is specified, we presume you know what you are doing
    #
    if checksum_level == CHECKSUM_FILE_TIMESTAMPS and history_file == None:
        history_file = ':memory:'

    #
    # load previous job history if it exists, otherwise create an empty history
    #
    job_history = open_job_history (history_file)

    (topological_sorted,
    self_terminated_nodes,
    dag_violating_edges,
    dag_violating_nodes) = topologically_sorted_nodes(target_tasks, forcedtorun_tasks,
                                                        gnu_make_maximal_rebuild_mode,
                                                        extra_data_for_signal = [t_verbose_logger(0, None, runtime_data), job_history])


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
                                                     extra_data_for_signal = [t_verbose_logger(0, None, runtime_data), job_history])

        if len(all_tasks) > len(topological_sorted):
            output_stream.write("\n" + "_" * 40 + "\nTasks which are up-to-date:\n\n")
            pipelined_tasks_to_run = set(topological_sorted)

            for t in all_tasks:
                if t in pipelined_tasks_to_run:
                    continue
                messages = t.printout(runtime_data, t in forcedtorun_tasks, job_history, verbose, indent)
                for m in messages:
                    output_stream.write(textwrap.fill(m, subsequent_indent = wrap_indent, width = wrap_width) + "\n")

    output_stream.write("\n" + "_" * 40 + "\nTasks which will be run:\n\n")
    for t in topological_sorted:
        messages = t.printout(runtime_data, t in forcedtorun_tasks, job_history, verbose, indent)
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
                                    task_with_completed_job_q, runtime_data, verbose,
                                    syncmanager,
                                    touch_files_only, job_history):

    inprogress_tasks = set()
    job_limit_semaphores = dict()

    def parameter_generator():
        count_remaining_jobs = defaultdict(int)
        log_at_level (logger, 10, verbose, "   job_parameter_generator BEGIN")
        while len(incomplete_tasks):
            cnt_jobs_created_for_all_tasks = 0
            cnt_tasks_processed = 0

            #
            #   get rid of all completed tasks first
            #       Completion is signalled from pipeline_run
            #
            while True:
                try:
                    item = task_with_completed_job_q.get_nowait()
                    job_completed_task, job_completed_task_name, job_completed_name = item


                    if not job_completed_task in incomplete_tasks:
                        raise Exception("Last job %s for %s. Missing from incomplete tasks in make_job_parameter_generator" % (job_completed_name, job_completed_task_name))
                    count_remaining_jobs[job_completed_task] = count_remaining_jobs[job_completed_task] - 1
                    #
                    #   This is bad: something has gone very wrong
                    #
                    if count_remaining_jobs[t] < 0:
                        raise Exception("job %s for %s causes job count < 0." % (job_completed_name, job_completed_task_name))

                    #
                    #   This Task completed
                    #
                    if count_remaining_jobs[job_completed_task] == 0:
                        log_at_level (logger, 10, verbose, "   Last job for %s. Retired from incomplete tasks in pipeline_run " % job_completed_task._name)
                        incomplete_tasks.remove(job_completed_task)
                        job_completed_task.completed (logger)
                except Queue.Empty:
                    break

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
                    # Only log active task
                    #
                    if t.is_active:
                        log_at_level (logger, 3, verbose, "Task enters queue = " + t.get_task_name() + (": Forced to rerun" if force_rerun else ""))
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
                    #if (t.active_if_checks != None):
                    #    t.is_active = all(arg() if isinstance(arg, collections.Callable) else arg
                    #                        for arg in t.active_if_checks)
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

                        job_name = t.get_job_name(descriptive_param, runtime_data)

                        #
                        #    don't run if up to date unless force to run
                        #
                        if force_rerun:
                            log_at_level (logger, 3, verbose, "    force task %s to rerun " % job_name)
                        else:
                            if not t.needs_update_func:
                                log_at_level (logger, 3, verbose, "    %s no function to check if up-to-date " % job_name)
                            else:
                                # extra clunky hack to also pass task info--
                                # makes sure that there haven't been code or arg changes
                                if t.needs_update_func == needs_update_check_modify_time:
                                    needs_update, msg = t.needs_update_func (*param, task=t, job_history = job_history)
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
                        # @originate tasks do not need to pause, because they depend on nothing!
                        if cnt_jobs_created == 0 and touch_files_only < 2:
                            if "ONE_SECOND_PER_JOB" in runtime_data and runtime_data["ONE_SECOND_PER_JOB"] and t._action_type != _task.action_task_originate:
                                log_at_level (logger, 10, verbose, "   1 second PAUSE in job_parameter_generator\n\n\n")
                                time.sleep(1.01)
                            else:
                                time.sleep(0.1)


                        count_remaining_jobs[t] += 1
                        cnt_jobs_created += 1
                        cnt_jobs_created_for_all_tasks += 1
                        yield (param,
                                t._name,
                                job_name,
                                t.job_wrapper,
                                t.user_defined_work_func,
                                get_semaphore (t, job_limit_semaphores, syncmanager),
                                touch_files_only)

                    # if no job came from this task, this task is complete
                    #   we need to retire it here instead of normal completion at end of job tasks
                    #   precisely because it created no jobs
                    if cnt_jobs_created == 0:
                        incomplete_tasks.remove(t)
                        t.completed (logger, True)
                        log_at_level (logger, 10, verbose, "   No jobs created for %s. Retired in parameter_generator " % t._name)

                        #
                        #   Add extra warning if no regular expressions match:
                        #   This is a common class of frustrating errors
                        #
                        if (verbose >= 1 and "ruffus_WARNING" in runtime_data and
                            t.param_generator_func in runtime_data["ruffus_WARNING"]):
                            for msg in runtime_data["ruffus_WARNING"][t.param_generator_func]:
                                logger.warning("    'In Task def %s(...):' %s " % (t.get_task_name(), msg))


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
def pipeline_run(target_tasks                     = [],
                 forcedtorun_tasks                = [],
                 multiprocess                     = 1,
                 logger                           = stderr_logger,
                 gnu_make_maximal_rebuild_mode    = True,
                 verbose                          = 1,
                 runtime_data                     = None,
                 one_second_per_job               = None,
                 touch_files_only                 = False,
                 exceptions_terminate_immediately = False,
                 log_exceptions                   = False,
                 checksum_level                    = CHECKSUM_HISTORY_TIMESTAMPS,
                 multithread                      = 0,
                 history_file                     = None):
                 # Remember to add further extra parameters here to "extra_pipeline_run_options" inside cmdline.py
                 # This will forward extra parameters from the command line to pipeline_run
    """
    Run pipelines.

    :param target_tasks: targets task functions which will be run if they are out-of-date
    :param forcedtorun_tasks: task functions which will be run whether or not they are out-of-date
    :param multiprocess: The number of concurrent jobs running on different processes.
    :param multithread: The number of concurrent jobs running as different threads. If > 1, ruffus will use multithreading *instead of* multiprocessing (and ignore the multiprocess parameter). Using multi threading is particularly useful to manage high performance clusters which otherwise are prone to "processor storms" when large number of cores finish jobs at the same time. (Thanks Andreas Heger)
    :param logger: Where progress will be logged. Defaults to stderr output.
    :type logger: `logging <http://docs.python.org/library/logging.html>`_ objects
    :param verbose: level 0 : nothing
                    level 1 : logs task names and warnings
                    level 2 : logs task description if exists
                    level 3 : logs job names for jobs to be run
                    level 4 : logs list of up-to-date tasks and job names for jobs to be run
                    level 5 : logs job names for all jobs whether up-to-date or not
                    level 10: logs messages useful only for debugging ruffus pipeline code
    :param touch_files_only: Create or update input/output files only to simulate running the pipeline. Do not run jobs. If set to CHECKSUM_REGENERATE, will regenerate the checksum history file to reflect the existing i/o files on disk.
    :param exceptions_terminate_immediately: Exceptions cause immediate termination
                        rather than waiting for N jobs to finish where N = multiprocess
    :param log_exceptions: Print exceptions to the logger as soon as they occur.
    :param checksum_level: Several options for checking up-to-dateness are available: Default is level 1.
                           level 0 : Use only file timestamps
                           level 1 : above, plus timestamp of successful job completion
                           level 2 : above, plus a checksum of the pipeline function body
                           level 3 : above, plus a checksum of the pipeline function default arguments and the additional arguments passed in by task decorators
    :param history_file: The database file which stores checksums and file timestamps for input/output files.
    :param one_second_per_job: To work around poor file timepstamp resolution for some file systems. Defaults to True if checksum_level is 0 forcing Tasks to take a minimum of 1 second to complete.
    :param runtime_data: Experimental feature for passing data to tasks at run time
    :param gnu_make_maximal_rebuild_mode: Defaults to re-running *all* out-of-date tasks. Runs minimal
                                          set to build targets if set to ``True``. Use with caution.
    """
    if touch_files_only == False:
        touch_files_only = 0
    elif touch_files_only == True:
        touch_files_only = 1
    else:
        touch_files_only = 2
        # we are not running anything so do it as quickly as possible
        one_second_per_job = False

    syncmanager = multiprocessing.Manager()

    if runtime_data == None:
        runtime_data = {}
    if not isinstance(runtime_data, dict):
        raise Exception("pipeline_run parameter runtime_data should be a dictionary of "
                        "values passes to jobs at run time.")


    #
    #   whether using multiprocessing or multithreading
    #
    if multithread:
        pool = ThreadPool(multithread)
        parallelism = multithread
    elif multiprocess > 1:
        pool = Pool(multiprocess)
        parallelism = multiprocess
    else:
        parallelism = 1
        pool = None

    #
    #   Supplement mtime with system clock if using CHECKSUM_HISTORY_TIMESTAMPS
    #       we don't need to default to adding 1 second delays between jobs
    #
    if one_second_per_job == None:
         if checksum_level == CHECKSUM_FILE_TIMESTAMPS:
            log_at_level (logger, 5, verbose, "   Checksums rely on FILE TIMESTAMPS only and we don't know if the system file time resolution: Pause 1 second...")
            runtime_data["ONE_SECOND_PER_JOB"] = True
         else:
            log_at_level (logger, 5, verbose, "   Checksum use calculated time as well: No 1 second pause...")
            runtime_data["ONE_SECOND_PER_JOB"] = False
    else:
        log_at_level (logger, 5, verbose, "   One second per job specified to be %s" % one_second_per_job)
        runtime_data["ONE_SECOND_PER_JOB"] = one_second_per_job


    if verbose == 0:
        logger = black_hole_logger
    elif verbose >= 11:
        if hasattr(logger, "add_unique_prefix"):
            logger.add_unique_prefix()

    if touch_files_only and verbose >= 1:
        logger.info("Touch output files instead of remaking them.")

    link_task_names_to_functions ()
    update_checksum_level_on_tasks (checksum_level)

    #
    #   If we aren't using checksums, and history file hasn't been specified,
    #       we might be a bit surprised to find Ruffus writing to a sqlite db anyway.
    #       Let us just use a in-memory db which will be thrown away
    #   Of course, if history_file is specified, we presume you know what you are doing
    #
    if checksum_level == CHECKSUM_FILE_TIMESTAMPS and history_file == None:
        history_file = ':memory:'

    job_history = open_job_history (history_file)




    #
    # @active_if decorated tasks can change their active state every time
    #   pipeline_run / pipeline_printout / pipeline_printout_graph is called
    #
    update_active_states_for_all_tasks ()


    #
    #   target jobs
    #
    target_tasks = task_names_to_tasks ("Target", target_tasks)
    forcedtorun_tasks = task_names_to_tasks ("Forced to run", forcedtorun_tasks)


    #
    #   To update the checksum file, we force all tasks to rerun but then don't actually call the task function...
    #
    #   So starting with target_tasks and forcedtorun_tasks, we harvest all upstream dependencies willy, nilly
    #           and assign the results to forcedtorun_tasks
    #
    if touch_files_only == 2:
        (forcedtorun_tasks, ignore_param1, ignore_param2,
         ignore_param3) = topologically_sorted_nodes(target_tasks + forcedtorun_tasks, True,
                                                     gnu_make_maximal_rebuild_mode,
                                                     extra_data_for_signal = [t_verbose_logger(0, None, runtime_data), job_history])



    (topological_sorted,
    self_terminated_nodes,
    dag_violating_edges,
    dag_violating_nodes) = topologically_sorted_nodes(  target_tasks, forcedtorun_tasks,
                                                        gnu_make_maximal_rebuild_mode,
                                                        extra_data_for_signal = [t_verbose_logger(verbose, logger, runtime_data), job_history])

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
    parameter_q = Queue.Queue()
    task_with_completed_job_q = Queue.Queue()
    parameter_generator = make_job_parameter_generator (incomplete_tasks, task_parents,
                                                        logger, forcedtorun_tasks,
                                                        task_with_completed_job_q,
                                                        runtime_data, verbose,
                                                        syncmanager,
                                                        touch_files_only, job_history)
    job_parameters = parameter_generator()
    fill_queue_with_job_parameters(job_parameters, parameter_q, parallelism, logger, verbose)

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
    #   pool = Pool(parallelism) if multiprocess > 1 else None
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




    if pool:
        pool_func = pool.imap_unordered
    else:
        pool_func = imap



    feed_job_params_to_process_pool = feed_job_params_to_process_pool_factory (parameter_q, logger, verbose)

    #
    #   for each result from job
    #
    job_errors = RethrownJobError()
    tasks_with_errors = set()


    #
    #   job_result.job_name / job_result.return_value
    #       Reserved for returning result from job...
    #       How?
    #
    for job_result in pool_func(run_pooled_job_without_exceptions, feed_job_params_to_process_pool()):
        t = node.lookup_node_from_name(job_result.task_name)

        # remove failed jobs from history-- their output is bogus now!
        if job_result.state in (JOB_ERROR, JOB_SIGNALLED_BREAK):

            if len(job_result.params) > 1:  # some jobs have no outputs
                output_file_name = job_result.params[1]
                if not isinstance(output_file_name, list): # some have multiple outputs from one job
                    output_file_name = [output_file_name]
                #
                # N.B. output parameters are not necessary all strings
                #
                for o_f_n in get_strings_in_nested_sequence(output_file_name):
                    #
                    # use paths relative to working directory
                    #
                    o_f_n = os.path.relpath(o_f_n)
                    job_history.pop(o_f_n, None)  # remove outfile from history if it exists

        # only save poolsize number of errors
        if job_result.state == JOB_ERROR:
            log_at_level (logger, 6, verbose, "   Exception caught for %s" % job_result.job_name)
            job_errors.append(job_result.exception)
            tasks_with_errors.add(t)

            #
            # print to logger immediately
            #
            if log_exceptions:
                log_at_level (logger, 6, verbose, "   Log Exception")
                logger.error(job_errors.get_nth_exception_str())

            #
            # break if too many errors
            #
            if len(job_errors) >= parallelism or exceptions_terminate_immediately:
                log_at_level (logger, 6, verbose, "   Break loop %s %s %s " % (exceptions_terminate_immediately, len(job_errors), parallelism) )
                parameter_q.put(all_tasks_complete())
                break


        # break immediately if the user says stop
        elif job_result.state == JOB_SIGNALLED_BREAK:
            job_errors.append(job_result.exception)
            job_errors.specify_task(t, "Exceptions running jobs")
            break

        else:
            if job_result.state == JOB_UP_TO_DATE:
                if verbose > 1:
                    logger.info("    %s unnecessary: already up to date" % job_result.job_name)
            else:
                if verbose:
                    logger.info("    %s completed" % job_result.job_name)
                # save this task name and the job (input and output files)
                # alternatively, we could just save the output file and its
                # completion time, or on the other end of the spectrum,
                # we could save a checksum of the function that generated
                # this file, something akin to:
                # chksum = md5.md5(marshal.dumps(t.user_defined_work_func.func_code.co_code))
                # we could even checksum the arguments to the function that
                # generated this file:
                # chksum2 = md5.md5(marshal.dumps(t.user_defined_work_func.func_defaults) +
                #                   marshal.dumps(t.args))

                if len(job_result.params) > 1:  # some jobs have no outputs
                    output_file_name = job_result.params[1]
                    if not isinstance(output_file_name, list): # some have multiple outputs from one job
                        output_file_name = [output_file_name]
                    #
                    # N.B. output parameters are not necessary all strings
                    #       and not all files have been successfully created,
                    #       even though the task apparently completed properly!
                    #
                    for o_f_n in get_strings_in_nested_sequence(output_file_name):
                        #
                        # use paths relative to working directory
                        #
                        o_f_n = os.path.relpath(o_f_n)
                        try:
                            log_at_level (logger, 6, verbose, "   Job History for : " + o_f_n)
                            mtime = os.path.getmtime(o_f_n)
                            #
                            #   use probably higher resolution time.time() over mtime
                            #       which might have 1 or 2s resolutions, unless there is
                            #       clock skew and the filesystem time > system time
                            #       (e.g. for networks)
                            #
                            epoch_seconds = time.time()
                            # Aargh. go back to insert one second between jobs
                            if epoch_seconds < mtime:
                                if one_second_per_job == None and not runtime_data["ONE_SECOND_PER_JOB"]:
                                    log_at_level (logger, 6, verbose, "   Switch to one second per job")
                                    runtime_data["ONE_SECOND_PER_JOB"] = True
                            elif  epoch_seconds - mtime < 1.1:
                                mtime = epoch_seconds
                            chksum = JobHistoryChecksum(o_f_n, mtime, job_result.params[2:], t)
                            job_history[o_f_n] = chksum
                        except:
                            pass

                ##for output_file_name in t.output_filenames:
                ##    # could use current time instead...
                ##    if not isinstance(output_file_name, list):
                ##        output_file_name = [output_file_name]
                ##    for o_f_n in output_file_name:
                ##        mtime = os.path.getmtime(o_f_n)
                ##        chksum = JobHistoryChecksum(o_f_n, mtime, job_result.params[2:], t)
                ##        job_history[o_f_n] = chksum


        #
        #   signal completed task after checksumming
        #
        task_with_completed_job_q.put((t, job_result.task_name, job_result.job_name))


        # make sure queue is still full after each job is retired
        # do this after undating which jobs are incomplete
        if len(job_errors):
            #parameter_q.clear()
            #if len(job_errors) == 1 and not parameter_q._closed:
            parameter_q.put(all_tasks_complete())
        else:
            fill_queue_with_job_parameters(job_parameters, parameter_q, parallelism, logger, verbose)


    syncmanager.shutdown()


    if pool:
        pool.close()
        pool.terminate()


    if len(job_errors):
        raise job_errors



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
