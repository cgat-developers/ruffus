#!/usr/bin/env python
from __future__ import print_function
import sys
#import signal
if sys.hexversion < 0x03000000:
    from future_builtins import zip, map
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
if sys.hexversion >= 0x03000000:
    # everything is unicode in python3
    from functools import reduce


import textwrap
import time
from multiprocessing.managers import SyncManager
from collections import namedtuple
from contextlib import contextmanager
try:
    import cPickle as pickle
except:
    import pickle as pickle
from . import dbdict


if __name__ == '__main__':
    import sys
    sys.path.insert(0,".")

from .graph import *
from .print_dependencies import *
from .ruffus_exceptions import  *
from .ruffus_utility import *
from .file_name_parameters import  *

if sys.hexversion >= 0x03000000:
    # everything is unicode in python3
    path_str_type = str
else:
    path_str_type = basestring


#
# use simplejson in place of json for python < 2.6
#
try:
    import json
except ImportError:
    import simplejson
    json = simplejson
dumps = json.dumps

if sys.hexversion >= 0x03000000:
    import queue as queue
else:
    import Queue as queue

class Ruffus_Keyboard_Interrupt_Exception (Exception):
    pass

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
    def __init__ (self, verbose, verbose_abbreviated_path, logger, runtime_data):
        self.verbose = verbose
        self.logger = logger
        self.runtime_data = runtime_data
        self.verbose_abbreviated_path = verbose_abbreviated_path

#_________________________________________________________________________________________
#
#   logging helper function
#
#________________________________________________________________________________________
def log_at_level (logger, message_level, verbose_level, msg):
    """
    writes to log if message_level > verbose level
    Returns anything written in case we might want to drop down and output at a lower log level
    """
    if message_level <= verbose_level:
        logger.info(msg)
        return True
    return False









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



# EXTRA pipeline_run DEBUGGING
EXTRA_PIPELINERUN_DEBUGGING = False








#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   task_decorator

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class task_decorator(object):
    """
        Forwards to functions within Task
    """
    def __init__(self, *decoratorArgs, **decoratorNamedArgs):
        """
            saves decorator arguments
        """
        self.args = decoratorArgs
        self.named_args = decoratorNamedArgs

    def __call__(self, task_func):
        """
            calls func in task with the same name as the class
        """
        #
        #   We are being paranoid here. In practice @decorators always precede the OO interface
        #

        # add task to main pipeline
        task_name = str(task_func.__module__) + "." + task_func.__name__
        if task_name not in main_pipeline:
            task = main_pipeline._create_task(task_func)

        # task_name already there as the identifying task_name.
        # If the func also matches everything is fine
        elif task_name in main_pipeline.task_names and main_pipeline[task_name][0].user_defined_work_func == task_func:
            task = main_pipeline[task_name][0]

        # If the task name is already taken but with a different function, this will blow up
        # But if the function is being reused and with a previously different task name then OK
        else:
            task = main_pipeline._create_task(task_func)


        # call the method called
        #   task.decorator_xxxx
        #   where xxxx = transform subdivide etc
        task_decorator_function = getattr(task, "_decorator_" + self.__class__.__name__)
        task_decorator_function(*self.args, **self.named_args)
        task.created_via_decorator = True


        #
        #   don't change the function so we can call it unaltered
        #
        return task_func


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
    """
    Splits a each set of input files into multiple output file names,
        where the number of output files may not be known beforehand.
    """
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

class graphviz(task_decorator):
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




#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#       job descriptors

#           given parameters, returns strings describing job
#           First returned parameter is string in strong form
#           Second returned parameter is a list of strings for input, output and extra parameters
#               intended to be reformatted with indentation
#           main use in error logging

#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888
def generic_job_descriptor (param, verbose_abbreviated_path, runtime_data):
    if param in ([], None):
        m = "Job"
    else:
        m = "Job  = %s" % ignore_unknown_encoder(param)

    return m, [m]

def io_files_job_descriptor (param, verbose_abbreviated_path, runtime_data):
    extra_param = ", " + shorten_filenames_encoder(param[2:], verbose_abbreviated_path)[1:-1] if len(param) > 2 else ""
    out_param   =        shorten_filenames_encoder(param[1], verbose_abbreviated_path)        if len(param) > 1 else "??"
    in_param    =        shorten_filenames_encoder(param[0], verbose_abbreviated_path)        if len(param) > 0 else "??"

    return ("Job  = [%s -> %s%s]" % (in_param, out_param, extra_param),
            ["Job  = [%s" % in_param, "-> " + out_param + extra_param + "]"])


def io_files_one_to_many_job_descriptor (param, verbose_abbreviated_path, runtime_data):

    extra_param = ", " + shorten_filenames_encoder(param[2:], verbose_abbreviated_path)[1:-1] if len(param) > 2 else ""
    out_param   =        shorten_filenames_encoder(param[1], verbose_abbreviated_path)        if len(param) > 1 else "??"
    in_param    =        shorten_filenames_encoder(param[0], verbose_abbreviated_path)        if len(param) > 0 else "??"

    # start with input parameter
    ret_params = ["Job  = [%s" % in_param]

    # add output parameter to list,
    #   processing one by one if multiple output parameters
    if len(param) > 1:
        if isinstance(param[1], (list, tuple)):
            ret_params.extend("-> " + shorten_filenames_encoder(p, verbose_abbreviated_path) for p in param[1])
        else:
            ret_params.append("-> " + out_param)

    # add extra
    if len(param) > 2 :
        ret_params.append(" , " + shorten_filenames_encoder(param[2:], verbose_abbreviated_path)[1:-1])

    # add closing bracket
    ret_params[-1] +="]"

    return ("Job  = [%s -> %s%s]" % (in_param, out_param, extra_param), ret_params)


def mkdir_job_descriptor (param, verbose_abbreviated_path, runtime_data):
    # input, output and parameters
    if len(param) == 1:
        m = "Make directories %s" % (shorten_filenames_encoder(param[0], verbose_abbreviated_path))
    elif len(param) == 2:
        m = "Make directories %s" % (shorten_filenames_encoder(param[1], verbose_abbreviated_path))
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
            try:
                ret_val = user_defined_work_func(*param)
                # EXTRA pipeline_run DEBUGGING
                if EXTRA_PIPELINERUN_DEBUGGING:
                    sys.stderr.write("w" * 36 + "[[ task() done ]]" + "w" * 27 + "\n")
            except KeyboardInterrupt as e:
                # Reraise KeyboardInterrupt as a normal Exception
                # EXTRA pipeline_run DEBUGGING
                if EXTRA_PIPELINERUN_DEBUGGING:
                    sys.stderr.write("E" * 36 + "[[ KeyboardInterrupt from task() ]]" + "E" * 9 + "\n")
                raise Ruffus_Keyboard_Interrupt_Exception("KeyboardInterrupt")
            except:
                #sys.stderr.write("?? %s ??" % (tuple(param),))
                raise
    elif touch_files_only == 1:
        #job_history = dbdict.open(RUFFUS_HISTORY_FILE, picklevalues=True)

        #
        #   Do not touch any output files which are the same as any in the input
        #       i.e. which are just being passed through
        #
        # list of input files
        real_input_file_names = set()
        for f in get_strings_in_nested_sequence(i):
            real_input_file_names.add(os.path.realpath(f))

        #
        #   touch files only
        #
        for f in get_strings_in_nested_sequence(o):

            if os.path.realpath(f) in real_input_file_names:
                continue

            #
            #   race condition still possible...
            #
            with open(f, 'a') as ff:
                os.utime(f, None)
            #if not os.path.exists(f):
            #    open(f, 'w')
            #    mtime = os.path.getmtime(f)
            #else:
            #    os.utime(f, None)
            #    mtime = os.path.getmtime(f)


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
    Make missing directories including any intermediate directories on the specified path(s)
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
    elif len(param) >= 2:
        dirs = param[1]
    else:
        raise Exception("No arguments in mkdir check %s" % (param,))

    # get all file names in flat list
    dirs = get_strings_in_nested_sequence (dirs)

    for d in dirs:
        try:
            os.makedirs(d)  # Please email the authors if an uncaught exception is raised here
            register_cleanup(d, "makedirs")
        except:
            #
            #   ignore exception if
            #       exception == OSError        + "File exists" or              // Linux
            #       exception == WindowsError   + "file already exists"        // Windows
            #   Are other exceptions raised by other OS?
            #
            #
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            # exceptionType == OSError and
            if "File exists" in str(exceptionValue):
                continue
            # exceptionType == WindowsError and
            elif "file already exists" in str(exceptionValue):
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
t_job_result        = namedtuple('t_job_result', 'task_name node_index state job_name return_value exception params', verbose =0)
t_deferred_pipeline = namedtuple('t_deferred_pipeline',     'task pipeline_name', verbose =0)
t_deferred_task     = namedtuple('t_deferred_task', 'task module_name task_name', verbose =0)



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
    #signal.signal(signal.SIGINT, signal.SIG_IGN)
    (param, task_name, node_index, job_name, job_wrapper, user_defined_work_func,
            job_limit_semaphore, death_event, touch_files_only) = process_parameters

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
            # EXTRA pipeline_run DEBUGGING
            if EXTRA_PIPELINERUN_DEBUGGING:
                sys.stderr.write(">" * 36 + "[[ job_wrapper ]]" + ">" * 27 + "\n")
            return_value =  job_wrapper(param, user_defined_work_func, register_cleanup, touch_files_only)

            #
            #   ensure one second between jobs
            #
            #if one_second_per_job:
            #    time.sleep(1.01)
            # EXTRA pipeline_run DEBUGGING
            if EXTRA_PIPELINERUN_DEBUGGING:
                sys.stderr.write("<" * 36 + "[[ job_wrapper done ]]" + "<" * 22 + "\n")
            return t_job_result(task_name, node_index, JOB_COMPLETED, job_name, return_value, None, param)
    except KeyboardInterrupt as e:
        # Reraise KeyboardInterrupt as a normal Exception. Should never be necessary here
        # EXTRA pipeline_run DEBUGGING
        if EXTRA_PIPELINERUN_DEBUGGING:
            sys.stderr.write("E" * 36 + "[[ KeyboardInterrupt ]]" + "E" * 21 + "\n")
        death_event.set()
        raise Ruffus_Keyboard_Interrupt_Exception("KeyboardInterrupt")
    except:
        # EXTRA pipeline_run DEBUGGING
        if EXTRA_PIPELINERUN_DEBUGGING:
            sys.stderr.write("E" * 36 + "[[ Other Interrupt ]]" + "E" * 23 + "\n")
        #   Wrap up one or more exceptions rethrown across process boundaries
        #
        #       See multiprocessor.Server.handle_request/serve_client for an analogous function
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        exception_stack  = traceback.format_exc()
        exception_name   = exceptionType.__module__ + '.' + exceptionType.__name__
        exception_value  = str(exceptionValue)
        if len(exception_value):
            exception_value = "(%s)" % exception_value

        if exceptionType == Ruffus_Keyboard_Interrupt_Exception:
            death_event.set()
            job_state = JOB_SIGNALLED_BREAK
        elif exceptionType == JobSignalledBreak:
            job_state = JOB_SIGNALLED_BREAK
        else:
            job_state = JOB_ERROR
        return t_job_result(task_name, node_index, job_state, job_name, None,
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

#   Pipeline


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
pipelines = dict()

class Pipeline(dict):
    def __init__(self, name, *arg, **kw):
        """
        Each Ruffus Pipeline object has to have a unique name.
        "main" is reserved for "main_pipeline", the default pipeline for all Ruffus decorators.
        """
        # initialise dict
        super(Pipeline, self).__init__(*arg, **kw)

        # set of tasks
        self.tasks = set()
        self.deferred_tasks = []
        self.deferred_pipelines = []
        self.task_names = set()

        # add self to list of all pipelines
        self.name = name
        if name in pipelines:
            raise Exception("Error:\nDuplicate pipeline. A pipeline named '%s' already exists.\n" % name)
        pipelines[name] = self

    #_____________________________________________________________________________________

    #   _create_task

    #_____________________________________________________________________________________
    def _create_task(self, func, task_name = None):
        """
        Create task with a function
        """
        task = Task(func, task_name, self)


        return task


    def _complete_task_setup (self):
        """
        Finishes initialising all tasks
        Make sure all tasks in dependency list are linked to real functions
        """

        self._resolve_deferred_dependencies()
        #print("_" * 80, file = sys.stderr)
        for task in self.tasks:
            #print("%s.setup_task_func()" % task._name, file = sys.stderr)
            task.setup_task_func()
            #
            #   some jobs single state status mirrors parent's state
            #       and parent task not known until dependencies resolved
            #   Is this legacy code?
            #       Breaks @merge otherwise
            #
            if isinstance(task._is_single_job_single_output, Task):
                task._is_single_job_single_output = task._is_single_job_single_output._is_single_job_single_output


        #print("_" * 80, file = sys.stderr)


    #_____________________________________________________________________________________

    #   _resolve_deferred_dependencies

    #_____________________________________________________________________________________
    def _resolve_deferred_dependencies (self):
        """
        Make sure all tasks in dependency list are linked to real tasks
            Call this before running anything else
        """

        #
        #   Resolve deferred task dependencies
        #
        for task, module_name, task_name in self.deferred_tasks:
            # returns a list of tasks if task_name is a pipeline name
            new_tasks = lookup_tasks_from_user_specified_names(task_description = "Forwarded declared", task_names = [task_name], default_pipeline_name = self.name, default_module_name = module_name)
            if not new_tasks:
                raise error_decorator_args("The dependencies for %s must be functions or "
                                           "function names or task names or Tasks or "
                                           "Pipelines. Have you misspelt '%s'?"
                                           % (task._name, task_name))
            for new_task in new_tasks:
                task._add_child(new_task)

        #
        #   Resolve deferred pipeline dependencies
        #
        for task, pipeline_name in self.deferred_pipelines:
            if pipeline_name not in pipelines:
                raise error_not_a_pipeline("%s does not name a pipeline." % pipeline_name)
            for new_task in pipelines[pipeline_name].get_tail_tasks():
                task._add_child(new_task)

    #_____________________________________________________________________________________

    #   get_head_tasks

    #_____________________________________________________________________________________
    def get_head_tasks(self):
        self._complete_task_setup()
        pass

    #_____________________________________________________________________________________

    #   get_head_tasks

    #_____________________________________________________________________________________
    def get_tail_tasks(self):
        self._complete_task_setup()
        pass

    #_____________________________________________________________________________________

    #   clone

    #_____________________________________________________________________________________
    def clone(self, name):
        self._complete_task_setup()
        pass

    #_____________________________________________________________________________________

    #   mkdir

    #_____________________________________________________________________________________
    def mkdir(self, name, *unnamed_args, **named_args):
        """
        Makes directories each incoming input to a corresponding output
        This is a One to One operation
        """
        # func is a placeholder...
        task = self._create_task(func = job_wrapper_mkdir, task_name = name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.mkdir"
        task_description = "%s(name = %r, %%s)" % (self.specification_name, name)
        task._prepare_mkdir (unnamed_args, named_args, task_description)


    #_____________________________________________________________________________________

    #   transform

    #_____________________________________________________________________________________
    def transform(self, name, task_func, *unnamed_args, **named_args):
        """
        Transforms each incoming input to a corresponding output
        This is a One to One operation
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.transform"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_transform (unnamed_args, named_args, task_description)


    #_____________________________________________________________________________________

    #   originate

    #_____________________________________________________________________________________
    def originate(self, name, task_func, unnamed_args, **named_args):
        """
        Originates a new set of output files, one output per call to the task function
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.originate"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_originate (unnamed_args, named_args, task_description)


    #_____________________________________________________________________________________

    #   split

    #_____________________________________________________________________________________
    def split(self, name, task_func, unnamed_args, **named_args):
        """
        Splits a single set of input files into multiple output file names,
            where the number of output files may not be known beforehand.
        This is a One to Many operation
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.split"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_split (unnamed_args, named_args, task_description)


    #_____________________________________________________________________________________

    #   subdivide

    #_____________________________________________________________________________________
    def subdivide(self, name, task_func, unnamed_args, **named_args):
        """
        Subdivides a each set of input files into multiple output file names,
            where the number of output files may not be known beforehand.
        This is a Many to Even More operation
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.subdivide"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_subdivide (unnamed_args, named_args, task_description)

    #_____________________________________________________________________________________

    #   merge

    #_____________________________________________________________________________________
    def merge(self, name, task_func, unnamed_args, **named_args):
        """
        Merges multiple input files into a single output.
        This is a Many to One operation
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.merge"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_merge (unnamed_args, named_args, task_description)
    #_____________________________________________________________________________________

    #   collate

    #_____________________________________________________________________________________
    def collate(self, name, task_func, unnamed_args, **named_args):
        """
        Collates each set of multiple matching input files into an output.
        This is a Many to Fewer operation
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.collate"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_collate (unnamed_args, named_args, task_description)
    #_____________________________________________________________________________________

    #   product

    #_____________________________________________________________________________________
    def product(self, name, task_func, unnamed_args, **named_args):
        """
        All-vs-all Product between items from each set of inputs
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.product"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_product (unnamed_args, named_args, task_description)
    #_____________________________________________________________________________________

    #   permutations

    #_____________________________________________________________________________________
    def permutations(self, name, task_func, unnamed_args, **named_args):
        """
        Permutations between items from a set of inputs
        * k-length tuples
        * all possible orderings
        * no self vs self
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.permutations"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_combinatorics (unnamed_args, named_args, task_description, error_task_permutations)

    #_____________________________________________________________________________________

    #   combinations

    #_____________________________________________________________________________________
    def combinations(self, name, task_func, unnamed_args, **named_args):
        """
        Combinations of items from a set of inputs
        * k-length tuples
        * Single (sorted) ordering, i.e. AB is the same as BA,
        * No repeats. No AA, BB
        For Example:
            combinations("ABCD", 3) = ['ABC', 'ABD', 'ACD', 'BCD']
            combinations("ABCD", 2) = ['AB', 'AC', 'AD', 'BC', 'BD', 'CD']
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.combinations"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_combinatorics (unnamed_args, named_args, task_description, error_task_combinations)

    #_____________________________________________________________________________________

    #   combinations_with_replacement

    #_____________________________________________________________________________________
    def combinations_with_replacement(self, name, task_func, unnamed_args, **named_args):
        """
        Combinations with replacement of items from a set of inputs
        * k-length tuples
        * Single (sorted) ordering, i.e. AB is the same as BA,
        * Repeats. AA, BB, AAC etc.
        For Example:
            combinations_with_replacement("ABCD", 2) = ['AA', 'AB', 'AC', 'AD',
                                                        'BB', 'BC', 'BD',
                                                        'CC', 'CD',
                                                        'DD']
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
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.combinations_with_replacement"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_combinatorics (unnamed_args, named_args, task_description, error_task_combinations_with_replacement)

    #_____________________________________________________________________________________

    #   files

    #_____________________________________________________________________________________
    def files(self, name, task_func, unnamed_args, **named_args):
        """
        calls user function in parallel
            with either each of a list of parameters
            or using parameters generated by a custom function

            In the parameter list,
                The first two items of each set of parameters must
                be input/output files or lists of files or Null
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.files"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_files (unnamed_args, named_args, task_description)
    #_____________________________________________________________________________________

    #   parallel

    #_____________________________________________________________________________________
    def parallel(self, name, task_func, unnamed_args, **named_args):
        """
        calls user function in parallel
            with either each of a list of parameters
            or using parameters generated by a custom function
        """
        task = self._create_task(task_func, name)
        task.created_via_decorator = False
        task.specification_name  = "pipeline.parallel"
        task_description = "%s(name = %r, task_func = %s, %%s)" % (self.specification_name,
                                                                   name, task_func.__name__)
        task._prepare_parallel (unnamed_args, named_args, task_description)


#
#   Global default shared pipeline (used for decorators)
#
main_pipeline = Pipeline(name = "main")




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#_________________________________________________________________________________________

#   lookup_unique_task_from_func

#_________________________________________________________________________________________
def lookup_unique_task_from_func (task_func, default_pipeline_name = "main"):
    """
    Go through all pipelines and match task_func to find a unique task
    Throw exception if ambiguous
    """

    def lookup_unique_task_from_func_in_pipeline (task_func, pipeline):
        if task_func in pipeline:
            if len(pipeline[task_func]) == 1:
                # Found task!
                return pipeline[task_func][0]

            # Found too many tasks! Ambiguous...
            task_names = ", ".join(task.task_name for task in pipeline[task_func])
            raise error_ambiguous_task("Function def %s(...): is used by multiple tasks (%s). Which one do you mean?."
                                                   % (task_func.__name__, task_names))
        return None

    #
    #   Iterate through all pipelines starting with the specified pipeline
    #
    task = lookup_unique_task_from_func_in_pipeline (task_func, pipelines[default_pipeline_name])
    if task:
        return task

    #
    #   Sees if function uniquely identifies a single task across other pipelines
    #
    found_tasks = []
    found_pipelines = []
    for pipeline in pipelines.values():
        task = lookup_unique_task_from_func_in_pipeline (task_func, pipeline)
        if task:
            found_tasks.append(task)
            found_pipelines.append(pipeline)

    if len(found_tasks) == 1:
        return found_tasks[0]

    if len(found_tasks) > 1:
        raise error_ambiguous_task("Task Name %s is ambiguous and specifies different tasks across multiple pipelines (%s)."
                                               % (task_func.__name__, ",".join(found_pipelines)))

    return None


#_________________________________________________________________________________________

#   lookup_tasks_from_name

#_________________________________________________________________________________________
def lookup_tasks_from_name (task_name, default_pipeline_name, default_module_name = "__main__"):
    """

        Tries:
            (1) Named pipeline in the format pipeline::task_name
            (2) tasks matching task_name in default_pipeline_name
            (3) pipeline names matching task_name
            (4) if task_name uniquely identifies a task in all other pipelines...
    """

    def lookup_task_in_pipeline_from_name(task_name, pipeline_name, default_module_name):
        """
        Look in specified pipeline to see if contains task
        If lookup returns None, means ambiguous: do nothing
        Only ever returns a list of one
        """
        multiple_tasks = []
        if pipeline_name not in pipelines:
            raise error_not_a_pipeline("%s does not name a pipeline." % pipeline_name)

        #
        #   Does the unqualified name uniquely identify?
        #
        pipeline = pipelines[pipeline_name]
        if task_name in pipeline:
            if len(pipeline[task_name]) == 1:
                return pipeline[task_name]
            else:
                multiple_tasks = pipeline[task_name]

        #
        #   Even if the unqualified name does not uniquely identify, maybe the qualified name does
        #
        full_qualified_name = default_module_name + "." + task_name
        if full_qualified_name in pipeline:
            if len(pipeline[full_qualified_name]) == 1:
                return pipeline[full_qualified_name]
            else:
                multiple_tasks = pipeline[task_name]

        #
        #   If either the qualified or unqualified name is ambiguous, throw...
        #
        if multiple_tasks:
            raise error_ambiguous_task("%s is ambiguous and specifies different tasks (%s)."
                                        % (task_name, ",".join(task._name for task in multiple_tasks)))

        #
        #   Nothing matched
        #
        return []



    # Lookup the task from the function or task name
    pipeline_name, task_name = re.match("(?:(.+):)?(.*)", task_name).groups()

    # Only try specified pipeline if there is one.
    #   Will blow up if task_name is ambiguous
    if pipeline_name:
        return lookup_task_in_pipeline_from_name(task_name, pipeline_name, default_module_name)

    # Try default pipeline first
    #   Will blow up if task_name is ambiguous
    #   Note that tasks only ever has 0 or 1 items
    tasks = lookup_task_in_pipeline_from_name(task_name, default_pipeline_name, default_module_name)
    if tasks:
        return tasks

    # task_name names a pipeline? Run the whole thing
    if task_name in pipelines:
        return pipelines[task_name].get_tail_tasks()

    #
    #   Otherwise all other pipelines and complain if ambiguous
    #
    found_tasks = []
    found_pipelines = []
    for pipeline_name in pipelines:

        tasks = lookup_task_in_pipeline_from_name(task_name, pipeline_name, default_module_name)
        if tasks:
            found_tasks.append(tasks)
            found_pipelines.append(pipeline_name)

    if len(found_tasks) == 1:
        return found_tasks[0]

    if len(found_tasks) > 1:
        raise error_ambiguous_task("Task Name %s is ambiguous and specifies different tasks across multiple pipelines (%s)."
                                               % (task_name, ",".join(found_pipelines)))

    return []



#_________________________________________________________________________________________

#   lookup_tasks_from_user_specified_names
#
#_________________________________________________________________________________________
def lookup_tasks_from_user_specified_names (task_description, task_names, default_pipeline_name = "main", default_module_name = "__main__"):
    """
    Given a list of task names, look up the corresponding tasks
    Will just pass through if the task_name is already a task
    """

    #
    #   In case we are given a single item instead of a list
    #
    if not isinstance(task_names, (list, tuple)):
        task_names = [task_names]

    task_list = []

    for task_name in task_names:

        # "task_name" is a Task or pipeline, add those
        if isinstance(task_name, Task):
            task_list.append(task_name)
            continue

        elif isinstance(task_name, Pipeline):
            task_list.extend(task_name.get_tail_tasks())
            continue

        if isinstance(task_name, collections.Callable):
            # blows up if ambiguous
            task = lookup_unique_task_from_func(task_name)
            # blow up for unwrapped function
            if not task:
                raise error_function_is_not_a_task(("Function def %s(...): is not a Ruffus task." %
                                                    task_func.__name__) +
                                                    " The function needs to have a ruffus decoration "
                                                    "like '@transform', or be a member of a ruffus.Pipeline().")

            task_list.append(task)
            continue


        # some kind of string: task or func or pipeline name?
        if isinstance(task_name, path_str_type):

            # Will throw Exception if ambiguous
            tasks = lookup_tasks_from_name(task_name, default_pipeline_name, default_module_name)
            # not found
            if not tasks:
                raise error_node_not_task("%s task '%s' is not a pipelined task in Ruffus. Have you mis-spelt the function or task name?" % (
                                                            task_description, task_name))

            task_list.extend(tasks)
            continue

        else:
            raise TypeError("Expecting a string or function, or a Ruffus Task or Pipeline object")
    return task_list







#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Task

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class Task (node):
    """

    * Represents each stage of a pipeline.
    * Associated with a single python function.
    * Identified uniquely within the pipeline by its name.

    """

    _action_names = ["unspecified",
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
                    "task_graphviz",
                    ]
    _action_unspecified                          =  0
    _action_task                                 =  1
    _action_task_files_re                        =  2
    _action_task_split                           =  3
    _action_task_merge                           =  4
    _action_task_transform                       =  5
    _action_task_collate                         =  6
    _action_task_files_func                      =  7
    _action_task_files                           =  8
    _action_mkdir                                =  9
    _action_task_parallel                        = 10
    _action_active_if                            = 11
    _action_task_product                         = 12
    _action_task_permutations                    = 13
    _action_task_combinations                    = 14
    _action_task_combinations_with_replacement   = 15
    _action_task_subdivide                       = 16
    _action_task_originate                       = 17
    _action_task_graphviz                        = 18



    _multiple_jobs_outputs    = 0
    _single_job_single_output = 1
    _job_single_matches_parent= 2

    _job_limit_semaphores = {}



    #_________________________________________________________________________________________

    #   _get_action_name

    #_________________________________________________________________________________________
    def _get_action_name (self):
        return Task._action_names[self._action_type]

    #_________________________________________________________________________________________

    #   __init__

    #_________________________________________________________________________________________
    def __init__ (self, func, task_name = None, pipeline = None):
        """
        * Creates a Task object with a specified python function and task name
        * The type of the Task (whether it is a transform or merge or collate etc. operation)
            is specified subsequently. This is because Ruffus decorators do not have to
            be specified in order, and we don't know ahead of time.
        """
        if not pipeline:
            pipeline = main_pipeline
        self.pipeline = pipeline
        self.func_module_name = str(func.__module__)
        self.func_name   = func.__name__
        # convert description into one line
        self.func_description = re.sub("\n\s+", " ", func.__doc__).strip() if func.__doc__ else ""

        if not task_name:
            task_name = self.func_module_name + "." + self.func_name

        node.__init__ (self, task_name)
        self._action_type  = Task._action_task
        self._action_type_desc = Task._action_names[self._action_type]

        #   Each task has its own checksum level
        #   At the moment this is really so multiple pipelines in the same script can have
        #       different checksum levels
        #   Though set by pipeline_xxxx functions, have initial valid value so unit tests work :-|
        self.checksum_level             = CHECKSUM_FILE_TIMESTAMPS
        self.param_generator_func       = None
        self.needs_update_func          = None
        self.job_wrapper                = job_wrapper_generic

        #
        self.job_descriptor             = generic_job_descriptor

        # jobs which produce a single output.
        # special handling for task.get_output_files for dependency chaining
        self._is_single_job_single_output  = self._multiple_jobs_outputs
        self.single_multi_io            = self._many_to_many

        # function which is decorated and does the actual work
        self.user_defined_work_func = func


        # functions which will be called when task completes
        self.posttask_functions         = []

        # give makedir automatically made parent tasks unique names
        self.cnt_task_mkdir             = 0

        # whether only task function itself knows what output it will produce
        # i.e. output is a glob or something similar
        self.indeterminate_output       = 0

        # cache output file names here
        self.output_filenames           = None

        # semaphore name must be unique
        self.semaphore_name             = pipeline.name + ":" + task_name

        # do not test for whether task is active
        self.active_if_checks           = None

        # extra flag for outputfiles
        self.is_active                  = True

        # Created via decorator or OO interface
        #   so that display_name looks more natural
        self.created_via_decorator      = False

        # Finish setting up task
        self.setup_task_func            = self._do_nothing_setup

        # Finish setting up task
        self.parsed_args                = {}
        self.error_type                 = None

        # @split or pipeline.split etc.
        self.specification_name         = ""

        # add to pipeline's lookup
        # this code is here rather than the pipeline so that current unittests do not
        #   need to bother about pipeline
        if task_name in self.pipeline.task_names:
            raise error_duplicate_task_name("Same task name %s specified multiple times in the same pipeline (%s)" % (task_name, self.pipeline.name))

        self.pipeline.tasks.add(self)

        # task_name is always a unique lookup and overrides everything else
        self.pipeline[task_name] = [self]
        self.pipeline.task_names.add(task_name)

        #
        #   Allow pipeline to lookup task by
        #       1) Func
        #       2) task name
        #       3) func name
        #
        #   Ambiguous func names returns an empty list []
        #

        for lookup in (func, self.func_name, self.func_module_name + "." + self.func_name):
            # don't add to lookup if this conflicts with a task_name which is always unique and overriding
            if lookup not in self.pipeline.task_names:
                if lookup in self.pipeline:
                    self.pipeline[lookup].append(self)
                else:
                    self.pipeline[lookup] = [self]

    #_________________________________________________________________________________________

    #   _init_for_pipeline

    #_________________________________________________________________________________________
    def _init_for_pipeline (self):
        """
        Initialize variables for pipeline run / printout

        **********
          BEWARE
        **********

        Because state is stored, ruffus is *not* reentrant.

        TODO: Need to create runtime DAG to mirror task DAG which holds output_filenames to be reentrant

        **********
          BEWARE
        **********
        """

        # cache output file names here
        self.output_filenames = None


    #_________________________________________________________________________________________

    #   _set_action_type

    #_________________________________________________________________________________________
    def _set_action_type (self, new_action_type):
        """
        Save how this task
            1) tests whether it is up-to-date and
            2) handles input/output files

        Checks that the task has not been defined with conflicting actions

        """
        if self._action_type not in (Task._action_unspecified, Task._action_task):
            old_action = Task._action_names[self._action_type]
            new_action = Task._action_names[new_action_type]
            actions = " and ".join(list(set((old_action, new_action))))
            task_name = "def %s(...)" % self._name.replace("__main__.", "")
            raise error_decorator_args(("    %s\n      has duplicate task specifications: (%s)\n") %
                                        (task_name, actions))
        self._action_type = new_action_type
        self._action_type_desc = Task._action_names[new_action_type]


    #_________________________________________________________________________________________

    #   _decorator_follows
    #       Deferred tasks will need to be resolved later
    #       Because deferred tasks can belong to other pipelines

    #_________________________________________________________________________________________
    def _decorator_follows (self, *unnamed_args, **named_args):
        """
        unnamed_args can be string or function or Task
        For strings, if lookup fails, will defer.
        """
        new_tasks = []
        for arg in unnamed_args:
            #
            #   Task
            #
            if isinstance(arg, Task):
                new_tasks.append(arg)

            #
            #   Pipeline: defer
            #
            elif isinstance(arg, Pipeline):
                pipeline.deferred_pipelines.append(t_deferred_pipeline(self, arg))

            #
            #   specified by string: unicode or otherwise
            #
            elif isinstance(arg, path_str_type):
                tasks = lookup_tasks_from_name(arg, default_pipeline_name = self.pipeline.name, default_module_name = self.func_module_name)
                new_tasks.extend(tasks)

                #
                #   task not yet defined: Add to Defer list
                #
                if not tasks:
                    #   If no module: use same module as current task
                    self.pipeline.deferred_tasks.append(t_deferred_task(self, self.func_module_name, arg))


            #
            #   for mkdir, automatically generate task with unique name
            #
            elif isinstance(arg, mkdir):

                specification_name = "@follows(..., mkdir(),...)"
                task_description = "@follows(..., mkdir(%%s))\n%s\n" % self._get_decorator_func_name()
                self._prepare_preceding_mkdir (arg.args, {}, specification_name, task_description)

            #
            #   Is this a function?
            #       Turn this function into a task
            #           (add task as attribute of this function)
            #       Add self as dependent
            elif isinstance(arg, collections.Callable):
                task = lookup_unique_task_from_func (arg, default_pipeline_name = self.pipeline.name)

                # add new task to pipeline if necessary
                if not task:
                    task = main_pipline._create_task(arg)
                new_tasks.append(task)

            else:
                raise error_decorator_args("@follows(%r)\n%s\n should take functions or "
                                           "function names or task names or Tasks or "
                                           "Pipelines"
                                           % (arg, self._get_decorator_func_name()))


        #
        #   add dependency
        #       duplicate dependencies are ignore automatically
        #
        for task in new_tasks:
            self._add_child(task)

        return new_tasks


    #_________________________________________________________________________________________

    #   _get_job_name

    #_________________________________________________________________________________________
    def _get_job_name(self, descriptive_param, verbose_abbreviated_path, runtime_data):
        """
        Use job descriptor to return short name for job, including any parameters

            runtime_data is not (yet) used but may be used to add context in future
        """
        return self.job_descriptor(descriptive_param, verbose_abbreviated_path, runtime_data)[0]


    #_________________________________________________________________________________________

    #   _get_display_name

    #_________________________________________________________________________________________
    def _get_display_name(self, in_func_format = False):
        """
        Returns name of task function, removing __main__ namespace if necessary

        if in_func_format is true, will return def task_func(...):

        in_func_format = True for
            1) throwing exceptions
            2) Forwarding errors from param factories such as no regex matches etc.

        """

        func_name = (self.func_module_name + "." + self.func_name) if self.func_module_name != "__main__" else self.func_name
        if self._action_type != Task._action_mkdir and in_func_format:
            return "def %s(...):" % func_name

        else:
            # TODO: return task_name
            return func_name

    #_________________________________________________________________________________________

    #   _get_decorator_func_name

    #_________________________________________________________________________________________
    def _get_decorator_func_name(self):
        """
        Returns name of task function, removing __main__ namespace if necessary

        """

        func_name = (self.func_module_name + "." + self.func_name) if self.func_module_name != "__main__" else self.func_name
        return "def %s(...):\n    ..." % func_name

    #_________________________________________________________________________________________

    #   _update_active_state

    #_________________________________________________________________________________________
    def _update_active_state (self):
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

    #   _printout

    #       This code will look so much better once we have job level dependencies
    #           pipeline_run has dependencies percolating up/down. Don't want to
    #           recreate all the logic here

    #_________________________________________________________________________________________
    def _printout (self, runtime_data, force_rerun, job_history, task_is_out_of_date, verbose=1, verbose_abbreviated_path = 2, indent = 4):
        """
        Print out all jobs for this task

            verbose =
                    level 1 : logs Out-of-date Task names
                    level 2 : logs All Tasks (including any task function docstrings)
                    level 3 : logs Out-of-date Jobs in Out-of-date Tasks, no explanation
                    level 4 : logs Out-of-date Jobs in Out-of-date Tasks, saying why they are out of date (include only list of up-to-date tasks)
                    level 5 : All Jobs in Out-of-date Tasks (include only list of up-to-date tasks)
                    level 6 : All jobs in All Tasks whether out of date or not

        """

        def _get_job_names (param, indent_str):
            job_names = self.job_descriptor(param, verbose_abbreviated_path, runtime_data)[1]
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

        # LOGGER: level 1 : logs Out-of-date Tasks (names and warnings)
        messages.append("Task = " + self._get_display_name() + ("    >>Forced to rerun<<" if force_rerun else ""))
        if verbose ==1:
            return messages

        # LOGGER: level 2 : logs All Tasks (including any task function docstrings)
        if verbose >= 2 and len(self.func_description):
            messages.append(indent_str + '"' + self.func_description + '"')

        #
        #   single job state
        #
        if verbose >= 10:
            if self._is_single_job_single_output == self._single_job_single_output:
                messages.append("    Single job single output")
            elif self._is_single_job_single_output == self._multiple_jobs_outputs:
                messages.append("    Multiple jobs Multiple outputs")
            else:
                messages.append("    Single jobs status depends on %s" % self._is_single_job_single_output._name)


        # LOGGER: No job if less than 2
        if verbose <= 2 :
            return messages

        # increase indent for jobs up to date status
        indent_str += " " * 3

        #
        #   If has an @active_if decorator, check if the task needs to be run
        #       @active_if parameters may be call back functions or booleans
        #
        if not self.is_active:
            # LOGGER
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
            # LOGGER
            if verbose <= 3:
                return messages

            #
            #   needs update func = None: always needs update
            #
            if not self.needs_update_func:
                messages.append(indent_str + "Task needs update: No function to check if up-to-date or not")
                return messages

            if self.needs_update_func == needs_update_check_modify_time:
                needs_update, msg = self.needs_update_func (task=self, job_history = job_history, verbose_abbreviated_path = verbose_abbreviated_path)
            else:
                needs_update, msg = self.needs_update_func ()

            if needs_update:
                messages.append(indent_str + "Task needs update: %s" % msg)
            #
            #   Get rid of up-to-date messages:
            #       Superfluous for parts of the pipeline which are up-to-date and
            #       Misleading for parts of the pipeline which require updating:
            #           tasks might have to run based on dependencies anyway
            #
            #else:
            #    if task_is_out_of_date:
            #        messages.append(indent_str + "Task appears up-to-date but will rerun after its dependencies")
            #    else:
            #        messages.append(indent_str + "Task up-to-date")

        else:
            runtime_data["MATCH_FAILURE"] = []
            #
            #   return messages description per job if verbose > 5 else whether up to date or not
            #
            cnt_jobs = 0
            for param, descriptive_param in self.param_generator_func(runtime_data):
                cnt_jobs += 1

                #
                #   needs update func = None: always needs update
                #
                if not self.needs_update_func:
                    if verbose >= 5:
                        messages.extend(_get_job_names (descriptive_param, indent_str))
                        messages.append(indent_str + "  Jobs needs update: No function to check if up-to-date or not")
                    continue

                if self.needs_update_func == needs_update_check_modify_time:
                    needs_update, msg = self.needs_update_func (*param, task=self, job_history = job_history, verbose_abbreviated_path = verbose_abbreviated_path)
                else:
                    needs_update, msg = self.needs_update_func (*param)

                if needs_update:
                    messages.extend(_get_job_names (descriptive_param, indent_str))
                    if verbose >= 4:
                        per_job_messages = [(indent_str + s) for s in ("  Job needs update: %s" % msg).split("\n")]
                        messages.extend(per_job_messages)
                    else:
                        messages.append(indent_str + "  Job needs update")


                # up to date: log anyway if verbose
                else:
                    # LOGGER
                    if (task_is_out_of_date and verbose >= 5) or verbose >= 6:
                        messages.extend(_get_job_names (descriptive_param, indent_str))
                        #
                        #   Get rid of up-to-date messages:
                        #       Superfluous for parts of the pipeline which are up-to-date and
                        #       Misleading for parts of the pipeline which require updating:
                        #           tasks might have to run based on dependencies anyway
                        #
                        #if not task_is_out_of_date:
                        #    messages.append(indent_str + "  Job up-to-date")


            if cnt_jobs == 0:
                messages.append(indent_str + "!!! No jobs for this task. "
                                             "Are you sure there is not a error in your "
                                             "code / regular expression?")
            # LOGGER
            if verbose >= 4 or (verbose and cnt_jobs == 0):
                if runtime_data and "MATCH_FAILURE" in runtime_data:
                    for s in runtime_data["MATCH_FAILURE"]:
                        messages.append(indent_str + "Job Warning: File match failure: " + s)
            runtime_data["MATCH_FAILURE"] = []
        messages.append("")
        return messages




    #_____________________________________________________________________________________

    #   _stop_dfs
    #
    #       returns whether up to date
    #
    #_____________________________________________________________________________________
    def _stop_dfs (self, verbose_logger_job_history):
        """
        If up to date: _stop_dfs = true
        If true, depth first search will not pass through this node
        """
        if not verbose_logger_job_history:
            raise Exception("verbose_logger_job_history is None")

        verbose_logger      = verbose_logger_job_history[0]
        job_history         = verbose_logger_job_history[1]

        try:
            logger              = verbose_logger.logger
            verbose             = verbose_logger.verbose
            runtime_data        = verbose_logger.runtime_data
            verbose_abbreviated_path = verbose_logger.verbose_abbreviated_path

            log_at_level (logger, 10, verbose,
                            "  Task = " + self._get_display_name())

            #
            #   If job is inactive, always consider it up-to-date
            #
            if (self.active_if_checks != None and
                any( not arg() if isinstance(arg, collections.Callable) else not arg
                         for arg in self.active_if_checks)):
                log_at_level (logger, 10, verbose,
                                "    Inactive task: treat as Up to date")
                #print 'signaling that the inactive task is up to date'
                return True

            #
            #   Always needs update if no way to check if up to date
            #
            if self.needs_update_func == None:
                log_at_level (logger, 10, verbose,
                                "    No update function: treat as out of date")
                return False

            #
            #   if no parameters, just return the results of needs update
            #
            if self.param_generator_func == None:
                if self.needs_update_func:
                    if self.needs_update_func == needs_update_check_modify_time:
                        needs_update, msg = self.needs_update_func (task=self, job_history = job_history, verbose_abbreviated_path = verbose_abbreviated_path)
                    else:
                        needs_update, msg = self.needs_update_func ()
                    log_at_level (logger, 10, verbose,
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
                        needs_update, msg = self.needs_update_func (*param, task=self, job_history = job_history, verbose_abbreviated_path = verbose_abbreviated_path)
                    else:
                        needs_update, msg = self.needs_update_func (*param)
                    if needs_update:
                        log_at_level (logger, 10, verbose, "    Needing update:\n      %s" % self._get_job_name(descriptive_param, verbose_abbreviated_path, runtime_data))
                        return False

                #
                #   Percolate warnings from parameter factories
                #
                if (verbose >= 1 and "ruffus_WARNING" in runtime_data and
                    self.param_generator_func in runtime_data["ruffus_WARNING"]):
                    for msg in runtime_data["ruffus_WARNING"][self.param_generator_func]:
                        logger.warning("    'In Task %s' %s " % (self._get_display_name(True), msg))

                log_at_level (logger, 10, verbose, "    All jobs up to date")




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

            exception_stack  = traceback.format_exc()
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

    #   _get_output_files
    #
    #
    #_____________________________________________________________________________________
    def _get_output_files (self, do_not_expand_single_job_tasks, runtime_data):
        """
        Cache output files

            If flattened is True, returns file as a list of strings,
                flattening any nested structures and discarding non string names
            Normally returns a list with one item for each job or a just a list of file names.
            For "_single_job_single_output" i.e. @merge and @files with single jobs,
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


                if self._is_single_job_single_output == self._single_job_single_output:
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
                isinstance(self.output_filenames[0], path_str_type)):
                return self.output_filenames
            # if it is flattened, might as well sort it
            return sorted(get_strings_in_nested_sequence(self.output_filenames))

        else:
            # special handling for jobs which have a single task,
            if (do_not_expand_single_job_tasks and
                self._is_single_job_single_output and
                len(self.output_filenames) ):
                return self.output_filenames[0]

            #
            # sort by jobs so it is just a weeny little bit less deterministic
            #
            return sorted(self.output_filenames, key = lambda x: str(x))



    #_____________________________________________________________________________________

    #   _completed
    #
    #       All logging logic moved to caller site
    #_____________________________________________________________________________________
    def _completed (self):
        """
        called even when all jobs are up to date
        """
        if not self.is_active:
            self.output_filenames = None
            return

        for f in self.posttask_functions:
            f()

        #
        #   indeterminate output. Check actual output again if someother tasks job function depend on it
        #       used for @split
        #
        if self.indeterminate_output:
            self.output_filenames = None









    #_________________________________________________________________________________________

    #   _handle_tasks_globs_in_inputs

    #_________________________________________________________________________________________
    def _handle_tasks_globs_in_inputs(self, input_params):
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
        tasks = self._decorator_follows(*function_or_func_names)
        functions_to_tasks = dict(zip(function_or_func_names, tasks))
        input_params = replace_func_names_with_tasks(input_params, functions_to_tasks)

        return t_params_tasks_globs_run_time_data(input_params, tasks, globs, runtime_data_names)



    #_________________________________________________________________________________________

    #   _choose_file_names_transform

    #_________________________________________________________________________________________
    def _choose_file_names_transform (self, file_name_transform_tag, valid_tags = (regex, suffix, formatter)):
        """
        shared code for subdivide, transform, product etc for choosing method for transform input file to output files
        """
        valid_tag_names = [];
        # regular expression match
        if (regex in valid_tags):
            valid_tag_names.append("regex()")
            if isinstance(file_name_transform_tag, regex):
                return t_regex_file_names_transform(self, file_name_transform_tag, self.error_type, self.specification_name)

        # simulate end of string (suffix) match
        if (suffix in valid_tags):
            valid_tag_names.append("suffix()")
            if isinstance(file_name_transform_tag, suffix):
                return t_suffix_file_names_transform(self, file_name_transform_tag, self.error_type, self.specification_name)

        # new style string.format()
        if (formatter in valid_tags):
            valid_tag_names.append("formatter()")
            if isinstance(file_name_transform_tag, formatter):
                return t_formatter_file_names_transform(self, file_name_transform_tag, self.error_type, self.specification_name)

        raise self.error_type(self, "%s expects one of %s as the second argument" % (self.specification_name, ", ".join(valid_tag_names)))




    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

    #       task handlers

    #         sets
    #               1) action_type
    #               2) param_generator_func
    #               3) needs_update_func
    #               4) job wrapper


    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

    def _do_nothing_setup (self):
        """
        Task is already set up: do nothing
        """
        pass

    #=====================================================================================

    #   _decorator_originate

    #=====================================================================================
    def _decorator_originate (self, *unnamed_args, **named_args):
        """
        @originate
        """
        self.specification_name   = "@originate"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_originate (unnamed_args, named_args, task_description)



    #_____________________________________________________________________________________

    #   _prepare_originate

    #_____________________________________________________________________________________
    def _prepare_originate (self, unnamed_args, named_args, task_description):
        """
        Common function for pipeline.originate and @originate
        """
        self.error_type           = error_task_originate
        self._set_action_type (Task._action_task_originate)
        self.setup_task_func      = self._originate_setup
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_output_files
        self.job_descriptor       = io_files_one_to_many_job_descriptor
        self.single_multi_io      = self._many_to_many
        # output is not a glob
        self.indeterminate_output = 0

        #
        #   Parse named and unnamed arguments
        #
        self.parsed_args = parse_task_arguments (unnamed_args, named_args,
                                                 ["output", "extras"], task_description)

    #_________________________________________________________________________________________

    #   _originate_setup

    #_________________________________________________________________________________________
    def _originate_setup (self):
        """
        Finish setting up originate
        """
        #
        # If self.parsed_args["output"] is a single item (e.g. file name),
        # that will be treated as a list
        # Each item in the list of these will be called as an output in a separate function call
        #
        output_params = self.parsed_args["output"]
        if not non_str_sequence (output_params):
            output_params = [output_params]


        #
        #   output globs will be replaced with files. But there should not be tasks here!
        #
        list_output_files_task_globs = [self._handle_tasks_globs_in_inputs(oo) for oo in output_params]
        for oftg in list_output_files_task_globs:
            if len(oftg.tasks):
                raise self.error_type(self, ("%s cannot output to another task. "
                                              "Do not include tasks in output parameters.") % self.specification_name)

        self.param_generator_func = originate_param_factory (   list_output_files_task_globs,
                                                                *self.parsed_args["extras"])

    #=====================================================================================

    #   _decorator_transform

    #=====================================================================================
    def _decorator_transform (self, *unnamed_args, **named_args):
        """
        @originate
        """
        self.specification_name  = "@transform"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_transform (unnamed_args, named_args, task_description)


    #_____________________________________________________________________________________

    #   _prepare_transform

    #_____________________________________________________________________________________
    def _prepare_transform (self, unnamed_args, named_args, task_description):
        """
        Common function for pipeline.transform and @transform
        """
        self.error_type           = error_task_transform
        self._set_action_type (Task._action_task_transform)
        self.setup_task_func      = self._transform_setup
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        self.single_multi_io      = self._many_to_many

        #
        #   Parse named and unnamed arguments
        #
        self.parsed_args = parse_task_arguments (unnamed_args, named_args,
                                                 ["input", "filter", "modify_inputs", "output", "extras"], task_description)

    #_____________________________________________________________________________________

    #   _transform_setup

    #_____________________________________________________________________________________
    def _transform_setup (self):
        """
        Finish setting up transform
        """

        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self._handle_tasks_globs_in_inputs(self.parsed_args["input"])

        #_________________________________________________________________________________
        #
        #       _single_job_single_output is bad policy. Can we remove it?
        #       What does this actually mean in Ruffus semantics?
        #
        #
        #   allows transform to take a single file or task
        if input_files_task_globs.single_file_to_list():
            self._is_single_job_single_output = self._single_job_single_output

        #
        #   whether transform generates a list of jobs or not will depend on the parent task
        #
        elif isinstance(input_files_task_globs.params, Task):
            self._is_single_job_single_output = input_files_task_globs.params

        #_________________________________________________________________________________

        # how to transform input to output file name
        file_names_transform = self._choose_file_names_transform (self.parsed_args["filter"])

        modify_inputs = self.parsed_args["modify_inputs"]
        if modify_inputs != None:
            modify_inputs = self._handle_tasks_globs_in_inputs(modify_inputs)



        self.param_generator_func = transform_param_factory (   input_files_task_globs,
                                                                False, # flatten input
                                                                file_names_transform,
                                                                modify_inputs,
                                                                self.parsed_args["modify_inputs_mode"],
                                                                self.parsed_args["output"],
                                                                *self.parsed_args["extras"])



    #=====================================================================================

    #   _decorator_subdivide

    #=====================================================================================
    def _decorator_subdivide (self, *unnamed_args, **named_args):
        """
        @subdivide
        """
        self.specification_name  = "@subdivide"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_subdivide (unnamed_args, named_args, task_description)


    #_____________________________________________________________________________________

    #   _prepare_subdivide

    #_____________________________________________________________________________________
    def _prepare_subdivide (self, unnamed_args, named_args, task_description):
        """
            Common code for @subdivide and pipeline.subdivide
            @split can also end up here
        """
        self.error_type           = error_task_subdivide
        self._set_action_type (Task._action_task_subdivide)
        self.setup_task_func      = self._subdivide_setup
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_one_to_many_job_descriptor
        self.single_multi_io      = self._many_to_many
        # output is a glob
        self.indeterminate_output = 2

        #
        #   Parse named and unnamed arguments
        #
        self.parsed_args = parse_task_arguments (unnamed_args, named_args,
                                                 ["input", "filter", "modify_inputs", "output", "extras"], task_description)


    #_________________________________________________________________________________________

    #   _subdivide_setup

    #_________________________________________________________________________________________
    def _subdivide_setup (self):
        """
        Finish setting up subdivide
        """

        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self._handle_tasks_globs_in_inputs(self.parsed_args["input"])

        #   allows split to take a single file or task
        input_files_task_globs.single_file_to_list()

        # how to transform input to output file name
        file_names_transform = self._choose_file_names_transform (self.parsed_args["filter"])

        modify_inputs = self.parsed_args["modify_inputs"]
        if modify_inputs != None:
            modify_inputs = self._handle_tasks_globs_in_inputs(modify_inputs)

        #
        #   output globs will be replaced with files. But there should not be tasks here!
        #
        output_files_task_globs = self._handle_tasks_globs_in_inputs(self.parsed_args["output"])
        if len(output_files_task_globs.tasks):
            raise self.error_type(self, ("%s cannot output to another task. "
                                          "Do not include tasks in output parameters.") % self.specification_name)

        self.param_generator_func = subdivide_param_factory (   input_files_task_globs,
                                                                False, # flatten input
                                                                file_names_transform,
                                                                modify_inputs,
                                                                self.parsed_args["modify_inputs_mode"],
                                                                output_files_task_globs,
                                                                *self.parsed_args["extras"])

    #=====================================================================================

    #   _decorator_split

    #=====================================================================================
    def _decorator_split (self, *unnamed_args, **named_args):
        """
        @split
        """
        self.specification_name  = "@split"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())

        #
        #   This is actually @subdivide
        #
        if isinstance(unnamed_args[1], regex):
            self._prepare_subdivide (unnamed_args, named_args, task_description)

        #
        #   This is actually @split
        #
        else:
            self._prepare_split(unnamed_args, named_args, task_description)

    #_________________________________________________________________________________________

    #   _prepare_split

    #_________________________________________________________________________________________
    def _prepare_split (self, unnamed_args, named_args, task_description):
        """
        Common code for @split and pipeline.split
        """
        self.error_type      = error_task_split
        self._set_action_type (Task._action_task_split)
        self.setup_task_func      = self._split_setup
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_one_to_many_job_descriptor
        self.single_multi_io      = self._one_to_many
        # output is a glob
        self.indeterminate_output = 1

        #
        #   Parse named and unnamed arguments
        #
        self.parsed_args = parse_task_arguments (unnamed_args, named_args,
                                                 ["input", "output", "extras"], task_description)



    #_________________________________________________________________________________________

    #   _split_setup

    #_________________________________________________________________________________________
    def _split_setup (self):
        """
        Finish setting up split
        """

        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self._handle_tasks_globs_in_inputs(self.parsed_args["input"])

        #
        #   output globs will be replaced with files. But there should not be tasks here!
        #
        output_files_task_globs = self._handle_tasks_globs_in_inputs(self.parsed_args["output"])
        if len(output_files_task_globs.tasks):
            raise self.error_type(self, ("%s cannot output to another task. "
                                          "Do not include tasks in output parameters.") % self.specification_name)

        self.param_generator_func = split_param_factory (   input_files_task_globs,
                                                                output_files_task_globs,
                                                                *self.parsed_args["extras"])




    #=====================================================================================

    #   _decorator_merge

    #=====================================================================================
    def _decorator_merge (self, *unnamed_args, **named_args):
        """
        @merge
        """
        self.specification_name  = "@merge"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_merge (unnamed_args, named_args, task_description)

    #_____________________________________________________________________________________

    #   _prepare_merge

    #_____________________________________________________________________________________
    def _prepare_merge (self, unnamed_args, named_args, task_description):
        """
        Common code for @merge and pipeline.merge
        """
        self.error_type           = error_task_merge
        self._set_action_type (Task._action_task_merge)
        self.setup_task_func      = self._merge_setup
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        self.single_multi_io      = self._many_to_one
        self._is_single_job_single_output = self._single_job_single_output

        #
        #   Parse named and unnamed arguments
        #
        self.parsed_args = parse_task_arguments (unnamed_args, named_args, ["input", "output", "extras"], task_description)


    #_________________________________________________________________________________________

    #   _merge_setup

    #_________________________________________________________________________________________
    def _merge_setup (self):
        """
        Finish setting up merge
        """
        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self._handle_tasks_globs_in_inputs(self.parsed_args["input"])

        self.param_generator_func = merge_param_factory (   input_files_task_globs,
                                                            self.parsed_args["output"],
                                                            *self.parsed_args["extras"])



    #=====================================================================================

    #   _decorator_collate

    #=====================================================================================
    def _decorator_collate (self, *unnamed_args, **named_args):
        """
        @collate
        """
        self.specification_name  = "@collate"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_collate (unnamed_args, named_args, task_description)

    #_____________________________________________________________________________________

    #   _prepare_collate

    #_____________________________________________________________________________________
    def _prepare_collate (self, unnamed_args, named_args, task_description):
        """
        Common code for @collate and pipeline.collate
        """
        self.error_type           = error_task_collate
        self._set_action_type (Task._action_task_collate)
        self.setup_task_func      = self._collate_setup
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        self.single_multi_io      = self._many_to_many

        #
        #   Parse named and unnamed arguments
        #
        self.parsed_args = parse_task_arguments (unnamed_args, named_args,
                                                 ["input", "filter", "modify_inputs", "output", "extras"], task_description)

    #_________________________________________________________________________________________

    #   _collate_setup

    #_________________________________________________________________________________________
    def _collate_setup (self):
        """
        Finish setting up collate
        """

        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self._handle_tasks_globs_in_inputs(self.parsed_args["input"])

        # how to transform input to output file name
        file_names_transform = self._choose_file_names_transform (self.parsed_args["filter"], (regex, formatter))

        modify_inputs = self.parsed_args["modify_inputs"]
        if modify_inputs != None:
            modify_inputs = self._handle_tasks_globs_in_inputs(modify_inputs)


        self.param_generator_func = collate_param_factory (     input_files_task_globs,
                                                                False, # flatten input
                                                                file_names_transform,
                                                                modify_inputs,
                                                                self.parsed_args["modify_inputs_mode"],
                                                                self.parsed_args["output"],
                                                                *self.parsed_args["extras"])


    #=====================================================================================

    #   _decorator_mkdir

    #=====================================================================================
    def _decorator_mkdir (self, *unnamed_args, **named_args):
        """
        @mkdir
        """
        specification_name = "@mkdir"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_preceding_mkdir ( unnamed_args, named_args, specification_name, task_description)

    #_____________________________________________________________________________________

    #   mkdir

    #_____________________________________________________________________________________
    def mkdir (self, unnamed_args, **named_args):
        """
        Make missing directories including any intermediate directories before the this task
        """
        specification_name = "Task(%s).mkdir" % self._name
        task_description = "%s(%%s)\n" % (self.specification_name)
        self._prepare_preceding_mkdir (unnamed_args, named_args, specification_name, task_description)


    #_____________________________________________________________________________________

    #   _prepare_dependent_mkdir

    #_____________________________________________________________________________________
    def _prepare_preceding_mkdir (self, unnamed_args, named_args, specification_name, task_description):
        """
        Add mkdir Task to run before self
            Common to
                Task.mkdir
                @mkdir
                @follows(..., mkdir())
        """
        #
        #   Create a new Task with a unique name to this instance of mkdir
        #
        self.cnt_task_mkdir += 1
        cnt_task_mkdir_str = (" #%d" % self.cnt_task_mkdir) if self.cnt_task_mkdir > 1 else ""
        task_name = r"mkdir%s before %s " % (cnt_task_mkdir_str, self._name)
        new_task = self.pipeline._create_task(func = job_wrapper_mkdir, task_name = task_name)
        self._add_child(new_task)


        #
        #   Prepare new node
        #
        new_task.specification_name = specification_name
        new_task._prepare_mkdir (unnamed_args, named_args, task_description)

        #print ("Create child\nname=%s\nspec=%s\ndescription=%s" % (new_task._name, specification_name, task_description), file = sys.stderr)

        #
        #   Hack:
        #       If the task name is too ugly,
        #       we can override it for flowchart printing using the display_name
        #
        #new_node.display_name = ??? new_node.func_description


    #_____________________________________________________________________________________

    #   _prepare_mkdir

    #_____________________________________________________________________________________
    def _prepare_mkdir (self, unnamed_args, named_args, task_description):

        self.error_type         = error_task_mkdir
        self._set_action_type (Task._action_mkdir)
        self.needs_update_func  = self.needs_update_func or needs_update_check_directory_missing
        self.job_wrapper        = job_wrapper_mkdir
        self.job_descriptor     = mkdir_job_descriptor


        # doesn't have a real function
        #  use job_wrapper just so it is not None
        self.user_defined_work_func = self.job_wrapper


        #
        # @transform like behaviour with regex / suffix or formatter
        #
        if (len(unnamed_args) > 1 and isinstance(unnamed_args[1], (formatter, suffix, regex))) or "filter" in named_args:
            self.single_multi_io      = self._many_to_many
            self.setup_task_func      = self._transform_setup

            #
            #   Parse named and unnamed arguments
            #
            self.parsed_args = parse_task_arguments (unnamed_args, named_args, ["input", "filter", "modify_inputs", "output", "extras"], task_description)


        #
        # simple behaviour: just make directories in list of strings
        #
        # the mkdir decorator accepts one string, multiple strings or a list of strings
        else:

            #
            # override funct description normally parsed from func.__doc__
            #   "Make missing directories including any intermediate directories on the specified path(s)"
            #
            self.func_description     = "Make missing directories %s" % (shorten_filenames_encoder(unnamed_args, 0))


            self.single_multi_io        = self._one_to_one
            self.setup_task_func        = self._do_nothing_setup

            #
            #
            #
            # if a single argument collection of parameters, keep that as is
            if len(unnamed_args) == 0:
                self.parsed_args["output"]  = []
            elif len(unnamed_args) > 1:
                self.parsed_args["output"]  = unnamed_args
            # len(unnamed_args) == 1: unpack unnamed_args[0]
            elif non_str_sequence (unnamed_args[0]):
                self.parsed_args["output"]  = unnamed_args[0]
            # single string or other non collection types
            else:
                self.parsed_args["output"]  = unnamed_args


            #   all directories created in one job to reduce race conditions
            #    so we are converting [a,b,c] into [   [(a, b,c)]   ]
            #    where unnamed_args = (a,b,c)
            #   i.e. one job whose solitory argument is a tuple/list of directory names
            self.param_generator_func = args_param_factory([[sorted(self.parsed_args["output"])]])


            #print ("mkdir %s" % (self.func_description), file = sys.stderr)


    #=====================================================================================

    #   _decorator_product

    #=====================================================================================
    def _decorator_product (self, *unnamed_args, **named_args):
        """
        @product
        """
        self.specification_name  = "@product"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_product (unnamed_args, named_args, task_description)

    #_____________________________________________________________________________________

    #   _prepare_product

    #_____________________________________________________________________________________
    def _prepare_product (self, unnamed_args, named_args, task_description):
        """
        Common code for @product and pipeline.product
        """
        self.error_type           = error_task_product
        self._set_action_type (Task._action_task_product)
        self.setup_task_func      = self._product_setup
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        self.single_multi_io      = self._many_to_many


        #
        #   Parse named and unnamed arguments
        #
        self.parsed_args = parse_task_arguments (unnamed_args, named_args,
                                                 ["input", "filter", "inputN", "modify_inputs", "output", "extras"], task_description)


    #_________________________________________________________________________________________

    #   _product_setup

    #_________________________________________________________________________________________
    def _product_setup (self):
        """
        Finish setting up product
        """
        #
        # replace function / function names with tasks
        #
        list_input_files_task_globs = [self._handle_tasks_globs_in_inputs(ii) for ii in self.parsed_args["input"]]

        # how to transform input to output file name
        file_names_transform = t_nested_formatter_file_names_transform(self, self.parsed_args["filter"], self.error_type, self.specification_name)

        modify_inputs = self.parsed_args["modify_inputs"]
        if modify_inputs != None:
            modify_inputs = self._handle_tasks_globs_in_inputs(modify_inputs)

        self.param_generator_func = product_param_factory (     list_input_files_task_globs,
                                                                False, # flatten input
                                                                file_names_transform,
                                                                modify_inputs,
                                                                self.parsed_args["modify_inputs_mode"],
                                                                self.parsed_args["output"],
                                                                *self.parsed_args["extras"])


    #=====================================================================================

    #   _decorator_permutations
    #   _decorator_combinations
    #   _decorator_combinations_with_replacement

    #=====================================================================================
    def _decorator_permutations(self, *unnamed_args, **named_args):
        """
        @permutations
        """
        self.specification_name = "@permutations"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_combinatorics (unnamed_args, named_args, task_description, error_task_permutations)

    def _decorator_combinations(self, *unnamed_args, **named_args):
        """
        @combinations
        """
        self.specification_name  = "@combinations"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_combinatorics (unnamed_args, named_args, task_description, error_task_combinations)

    def _decorator_combinations_with_replacement(self, *unnamed_args, **named_args):
        """
        @combinations_with_replacement
        """
        self.specification_name  = "@combinations_with_replacement"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_combinatorics (unnamed_args, named_args, task_description, error_task_combinations_with_replacement)

    #_____________________________________________________________________________________

    #   _prepare_combinatorics

    #_____________________________________________________________________________________
    def _prepare_combinatorics (self, unnamed_args, named_args, task_description, error_type):
        """
        Common code for
            @permutations and pipeline.permutations
            @combinations and pipeline.combinations
            @combinations_with_replacement and pipeline.combinations_with_replacement
        """
        self.error_type           = error_type
        self.setup_task_func      = self._combinatorics_setup
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        self.single_multi_io      = self._many_to_many


        #
        #   Parse named and unnamed arguments
        #
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self.parsed_args = parse_task_arguments (unnamed_args, named_args,
                                                 ["input", "filter", "tuple_size", "modify_inputs", "output", "extras"], task_description)


    #_________________________________________________________________________________________

    #   _combinatorics_setup

    #_________________________________________________________________________________________
    def _combinatorics_setup (self):
        """
            Finish setting up combinatorics
        """
        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self._handle_tasks_globs_in_inputs(self.parsed_args["input"])

        # how to transform input to output file name: len(k-tuples) of (identical) formatters
        file_names_transform = t_nested_formatter_file_names_transform(self, [self.parsed_args["filter"]] * self.parsed_args["tuple_size"], self.error_type, self.specification_name)

        modify_inputs = self.parsed_args["modify_inputs"]
        if modify_inputs != None:
            modify_inputs = self._handle_tasks_globs_in_inputs(modify_inputs)

        # we are not going to specify what type of combinatorics this is twice:
        #       just look up from our error type
        error_type_to_combinatorics_type = {
            error_task_combinations_with_replacement  : t_combinatorics_type.COMBINATORICS_COMBINATIONS_WITH_REPLACEMENT,
            error_task_combinations                   : t_combinatorics_type.COMBINATORICS_COMBINATIONS,
            error_task_permutations                   : t_combinatorics_type.COMBINATORICS_PERMUTATIONS
        }

        self.param_generator_func = combinatorics_param_factory (   input_files_task_globs,
                                                                    False, # flatten input
                                                                    error_type_to_combinatorics_type[self.error_type],
                                                                    self.parsed_args["tuple_size"],
                                                                    file_names_transform,
                                                                    modify_inputs,
                                                                    self.parsed_args["modify_inputs_mode"],
                                                                    self.parsed_args["output"],
                                                                    *self.parsed_args["extras"])



    #=====================================================================================

    #   _decorator_files

    #=====================================================================================
    def _decorator_files (self, *unnamed_args, **named_args):
        """
        @files
        """
        self.specification_name  = "@files"
        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self._prepare_files (unnamed_args, named_args, task_description)

    #_____________________________________________________________________________________

    #   _prepare_files

    #_____________________________________________________________________________________
    def _prepare_files (self, unnamed_args, named_args, task_description):
        """
        Common code for @files and pipeline.files
        """
        self.error_type             = error_task_files
        self.setup_task_func        = self._do_nothing_setup
        self.needs_update_func      = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper            = job_wrapper_io_files
        self.job_descriptor         = io_files_job_descriptor

        if len(unnamed_args) == 0:
            raise error_task_files(self, "Too few arguments for @files")

        #   Use parameters generated by a custom function
        if len(unnamed_args) == 1 and isinstance(unnamed_args[0], collections.Callable):

            self._set_action_type (Task._action_task_files_func)
            self.param_generator_func = files_custom_generator_param_factory(unnamed_args[0])

            # assume
            self.single_multi_io           = self._many_to_many

        #   Use parameters in supplied list
        else:
            self._set_action_type (Task._action_task_files)

            if len(unnamed_args) > 1:

                # single jobs
                # This is true even if the previous task has multiple output
                # These will all be joined together at the hip (like @merge)
                # If you want different behavior, use @transform
                params = copy.copy([unnamed_args])
                self._is_single_job_single_output = self._single_job_single_output
                self.single_multi_io           = self._one_to_one


            else:

                # multiple jobs with input/output parameters etc.
                params = copy.copy(unnamed_args[0])
                self._is_single_job_single_output = self._multiple_jobs_outputs
                self.single_multi_io           = self._many_to_many

            check_files_io_parameters (self, params, error_task_files)

            self.parsed_args["input"]   =[pp[0]         for pp in params]
            self.parsed_args["output"]  =[tuple(pp[1:]) for pp in params]
            self.setup_task_func = self._files_setup


    #_________________________________________________________________________________________

    #   _files_setup

    #_________________________________________________________________________________________
    def _files_setup (self):
        """
            Finish setting up @files
        """
        #
        # replace function / function names with tasks
        #
        input_files_task_globs = self._handle_tasks_globs_in_inputs(self.parsed_args["input"])


        self.param_generator_func = files_param_factory (input_files_task_globs,
                                                         False, # flatten input
                                                         True,  # do_not_expand_single_job_tasks
                                                         self.parsed_args["output"])

    #=====================================================================================

    #   _decorator_parallel

    #=====================================================================================
    def _decorator_parallel (self, *unnamed_args, **named_args):
        """
        @parallel
        """
        self.specification_name  = "@parallel"
        self._prepare_parallel (unnamed_args, named_args)

    #_____________________________________________________________________________________

    #   _prepare_parallel

    #_____________________________________________________________________________________
    def _prepare_parallel (self, unnamed_args, named_args):
        """
        Common code for @parallel and pipeline.parallel
        """
        self.error_type           = error_task_parallel
        self._set_action_type (Task._action_task_parallel)
        self.setup_task_func      = self._do_nothing_setup
        self.needs_update_func    = None
        self.job_wrapper          = job_wrapper_generic
        self.job_descriptor       = io_files_job_descriptor


        if len(unnamed_args) == 0:
            raise error_task_parallel(self, "Too few arguments for @parallel")

        #   Use parameters generated by a custom function
        if len(unnamed_args) == 1 and isinstance(unnamed_args[0], collections.Callable):
            self.param_generator_func = args_param_factory(unnamed_args[0]())

        # list of  params
        else:
            if len(unnamed_args) > 1:
                # single jobs
                params = copy.copy([unnamed_args])
                self._is_single_job_single_output = self._single_job_single_output
            else:
                # multiple jobs with input/output parameters etc.
                params = copy.copy(unnamed_args[0])
                check_parallel_parameters (self, params, error_task_parallel)

            self.param_generator_func = args_param_factory (params)




    #=====================================================================================

    #   _decorator_files_re

    #=====================================================================================
    def _decorator_files_re (self, *unnamed_args, **named_args):
        """
        @files_re

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
        self.specification_name  = "@files_re"
        self.error_type           = error_task_files_re
        self._set_action_type (Task._action_task_files_re)
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor
        self.single_multi_io      = self._many_to_many


        if len(unnamed_args) < 3:
            raise self.error_type(self, "Too few arguments for @files_re")

        #888888888888888888888888888888888888888888888888888888888888888888888888888888888

        #   !! HERE BE DRAGONS !!

        #       Legacy, deprecated parameter handling depending on positions
        #           and not even on type

        # check if parameters wrapped in combine
        combining_all_jobs, unnamed_args = is_file_re_combining(unnamed_args)

        # second parameter is always regex()
        unnamed_args[1] = regex(unnamed_args[1])

        # third parameter is inputs() if there is a four and fifth parameter...
        # That means if you want "extra" parameters, you always need inputs()
        if len(unnamed_args) > 3:
            unnamed_args[2] = inputs(unnamed_args[2])

        #888888888888888888888888888888888888888888888888888888888888888888888888888888888

        task_description = "%s(%%s)\n%s\n" % (self.specification_name, self._get_decorator_func_name())
        self.parsed_args = parse_task_arguments (unnamed_args, named_args, ["input", "filter", "modify_inputs", "output", "extras"], task_description)

        if combining_all_jobs:
            self.setup_task_func      = self._collate_setup
        else:
            self.setup_task_func      = self._transform_setup














    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

    #   Other task handlers



    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888







    #=====================================================================================

    #   check_if_uptodate

    #=====================================================================================
    def check_if_uptodate (self, func):
        """
        func returns true if input / output files are up to date
        func takes as many arguments as the task function
        """
        if not isinstance(func, collections.Callable):
            raise error_decorator_args("Task(%s).check_if_uptodate expects a single function or Callable object"
                                       % (self._name))
        self.needs_update_func        = func


    #_____________________________________________________________________________________

    #   _decorator_check_if_uptodate

    #_____________________________________________________________________________________
    def _decorator_check_if_uptodate (self, *args):
        """
        @check_if_uptodate
        """
        if len(args) != 1 or not isinstance(args[0], collections.Callable):
            raise error_decorator_args("Expecting a single function or Callable object in  " +
                                                "@check_if_uptodate %s:\n[%s]" %
                                                (self._name, str(args)))
        self.needs_update_func      = args[0]


    #=====================================================================================

    #   posttask

    #=====================================================================================
    def posttask(self, *funcs):
        """
        Takes one or more functions which will be called if the task completes
        """
        specification_name = "Task(%s).posttask" % self._name
        self._set_posttask(specification_name, *funcs)

    #_________________________________________________________________________________________

    #   _decorator_posttask

    #_________________________________________________________________________________________
    def _decorator_posttask(self, *funcs):
        """
        @posttask
        """
        specification_name = "@posttask"
        self._set_posttask(specification_name, *funcs)

    #_________________________________________________________________________________________

    #   _set_posttask

    #_________________________________________________________________________________________
    def _set_posttask(self, specification_name, *funcs):
        """
        Takes one or more functions which will be called if the task completes
        """
        for arg in funcs:
            if isinstance(arg, touch_file):
                self.posttask_functions.append(touch_file_factory (arg.args, register_cleanup))
            elif isinstance(arg, collections.Callable):
                self.posttask_functions.append(arg)
            else:
                raise PostTaskArgumentError("Expecting simple functions or touch_file() in  " +
                                                "%s(...)\n" % (specification_name))



    #=====================================================================================

    #   jobs_limit

    #=====================================================================================
    def jobs_limit(self, maximum_jobs_in_parallel, limit_name = None):
        """
        Limit the number of concurrent jobs
        """
        specification_name = "Task(%s).jobs_limit" % self._name
        self._set_jobs_limit(specification_name, maximum_jobs_in_parallel, limit_name)

    #_________________________________________________________________________________________

    #   _decorator_jobs_limit

    #_________________________________________________________________________________________
    def _decorator_jobs_limit(self, maximum_jobs_in_parallel, limit_name = None):
        """
        @jobs_limit
        """
        specification_name = "@jobs_limit"
        self._set_jobs_limit(specification_name, maximum_jobs_in_parallel, limit_name)

    #_________________________________________________________________________________________

    #   _set_jobs_limit

    #_________________________________________________________________________________________
    def _set_jobs_limit(self, specification_name, maximum_jobs_in_parallel, limit_name = None):
        try:
            maximum_jobs_in_parallel = int(maximum_jobs_in_parallel)
            assert(maximum_jobs_in_parallel >= 1)
        except:
            limit_name = ", " + limit_name if limit_name else ""
            raise JobsLimitArgumentError(('In %s(%r%s), the limit '
                                          'must be an integer number greater than or '
                                          'equal to 1') %
                                         (specification_name, maximum_jobs_in_parallel, limit_name))

        # set semaphore name to other than the "pipeline.name:task name"
        if limit_name != None:
            self.semaphore_name = limit_name
        if self.semaphore_name in self._job_limit_semaphores:
            prev_maximum_jobs = self._job_limit_semaphores[self.semaphore_name]
            if prev_maximum_jobs != maximum_jobs_in_parallel:
                raise JobsLimitArgumentError(('%s(%d, %r) The job limit %r cannot ' +
                                            're-defined from the previous limit of %d') %
                                             (   specification_name,
                                                 maximum_jobs_in_parallel,
                                                 self.semaphore_name,
                                                 self.semaphore_name,
                                                 prev_maximum_jobs))
        else:
            #
            #   save semaphore and limit
            #
            self._job_limit_semaphores[self.semaphore_name] = maximum_jobs_in_parallel

    #=====================================================================================

    #   active_if

    #=====================================================================================
    def active_if (self, *active_if_checks):
        """
        If any of active_checks is False or returns False, then the task is
        marked as "inactive" and its outputs removed.
        """
        #print 'job is active:', active_checks, [
        #                arg() if isinstance(arg, collections.Callable) else arg
        #                for arg in active_checks]
        if self.active_if_checks == None:
            self.active_if_checks = []
        self.active_if_checks.extend(active_if_checks)
        #print(self.active_if_checks)

    #_____________________________________________________________________________________

    #   _decorator_active_if

    #_____________________________________________________________________________________
    def _decorator_active_if (self, *active_if_checks):
        """
        @active_if
        """
        self.active_if(*active_if_checks)


    #=====================================================================================

    #   _decorator_graphviz

    #=====================================================================================
    def graphviz(self, *unnamed_args, **named_args):
        self.graphviz_attributes=named_args
        if len(unnamed_args):
            raise TypeError("Task(%s).graphviz only understands named arguments" % self._name)

    #_____________________________________________________________________________________

    #   _decorator_graphviz

    #_____________________________________________________________________________________
    def _decorator_graphviz(self, *unnamed_args, **named_args):
        self.graphviz_attributes=named_args
        if len(unnamed_args):
            raise TypeError("@graphviz only understands named arguments")


class task_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, defaultdict):
            return dict(obj)
        if isinstance(obj, Task):
            return obj._name #, Task._action_names[obj._action_task], obj.func_description]
        return json.JSONEncoder.default(self, obj)







#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888



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
        n._update_active_state()


#_________________________________________________________________________________________

#   lookup_pipeline

#_________________________________________________________________________________________
def lookup_pipeline (pipeline):
    """
    If pipeline is
        None                : main_pipeline
        string              : lookup name in pipelines
    """

    # Pipeline object pass through unchanged
    if isinstance(pipeline, Pipeline):
        return pipeline

    # default to main_pipeline if None
    if not pipeline:
        return main_pipeline

    # strings: lookup from name
    if isinstance(pipeline, str) and pipeline in pipelines:
        return pipelines[pipeline]

    raise error_not_a_pipeline("%s does not name a pipeline." % pipeline)


#_________________________________________________________________________________________

#   pipeline_printout_in_dot_format

#_________________________________________________________________________________________
def pipeline_printout_graph (stream,
                             output_format                  = None,
                             target_tasks                   = [],
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
                             checksum_level                 = None,
                             history_file                   = None,
                             pipeline                       = None):
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
    :param minimal_key_legend: Only add entries to the legend for task types which appear
    :param user_colour_scheme: Dictionary specifying colour scheme for flowchart
    :param pipeline_name: Pipeline Title
    :param size: tuple of x and y dimensions
    :param dpi: print resolution
    :param runtime_data: Experimental feature for passing data to tasks at run time
    :param history_file: The database file which stores checksums and file timestamps for input/output files.
    :param checksum_level: Several options for checking up-to-dateness are available: Default is level 1.
                    level 0 : Use only file timestamps
                    level 1 : above, plus timestamp of successful job completion
                    level 2 : above, plus a checksum of the pipeline function body
                    level 3 : above, plus a checksum of the pipeline function default arguments and the additional arguments passed in by task decorators
    """

    # EXTRA pipeline_run DEBUGGING
    global EXTRA_PIPELINERUN_DEBUGGING
    EXTRA_PIPELINERUN_DEBUGGING = False

    if checksum_level is None:
        checksum_level = get_default_checksum_level()


    #
    #   pipeline must be a Pipeline or a string naming a pipeline
    #
    pipeline = lookup_pipeline (pipeline)
    #
    #   Make sure all tasks in dependency list are linked to real functions
    #
    pipeline._complete_task_setup()

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

    #
    #   target jobs
    #
    if target_tasks == None:
        target_tasks = []
    if forcedtorun_tasks == None:
        forcedtorun_tasks = []
    target_tasks        = lookup_tasks_from_user_specified_names ("Target", target_tasks, pipeline.name)
    if not target_tasks:
        target_tasks = list(pipeline.tasks)
    forcedtorun_tasks   = lookup_tasks_from_user_specified_names ("Forced to run", forcedtorun_tasks, pipeline.name)


    (topological_sorted, ignore_param1, ignore_param2,
         ignore_param3) = topologically_sorted_nodes(target_tasks, forcedtorun_tasks,
                                                        gnu_make_maximal_rebuild_mode,
                                                        extra_data_for_signal = [t_verbose_logger(0, 0, None, runtime_data), job_history])
    if not len(target_tasks):
        target_tasks = topological_sorted[-1:]



    # open file if (unicode?) string
    if isinstance(stream, path_str_type):
        stream = open(stream, "w")

    # derive format automatically from name
    if output_format == None:
        output_format = os.path.splitext(stream.name)[1].lstrip(".")



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
                      extra_data_for_signal = [t_verbose_logger(0, 0, None, runtime_data), job_history])


#_________________________________________________________________________________________

#   get_completed_task_strings

#_________________________________________________________________________________________
def get_completed_task_strings (incomplete_tasks, all_tasks, forcedtorun_tasks, verbose, verbose_abbreviated_path, indent, runtime_data, job_history):
    """
    Printout list of completed tasks
    """
    completed_task_strings = []
    if len(all_tasks) > len(incomplete_tasks):
        completed_task_strings.append("")
        completed_task_strings.append("_" * 40)
        completed_task_strings.append("Tasks which are up-to-date:")
        completed_task_strings.append("")
        completed_task_strings.append("")
        set_of_incomplete_tasks = set(incomplete_tasks)

        for t in all_tasks:
            # Only print Up to date tasks
            if t in set_of_incomplete_tasks:
                continue
            # LOGGER
            completed_task_strings.extend(t._printout(runtime_data, t in forcedtorun_tasks, job_history, False, verbose, verbose_abbreviated_path, indent))

        completed_task_strings.append("_" * 40)
        completed_task_strings.append("")
        completed_task_strings.append("")

    return completed_task_strings

#_________________________________________________________________________________________

#   pipeline_printout

#_________________________________________________________________________________________
def pipeline_printout(  output_stream                   = None,
                        target_tasks                    = [],
                        forcedtorun_tasks               = [],
                        # verbose defaults to 4 if None
                        verbose                         = None,
                        indent                          = 4,
                        gnu_make_maximal_rebuild_mode   = True,
                        wrap_width                      = 100,
                        runtime_data                    = None,
                        checksum_level                  = None,
                        history_file                    = None,
                        verbose_abbreviated_path        = None,
                        pipeline                        = None):
                      # Remember to add further extra parameters here to "extra_pipeline_printout_options" inside cmdline.py
                      # This will forward extra parameters from the command line to pipeline_printout
    """
    Printouts the parts of the pipeline which will be run

    Because the parameters of some jobs depend on the results of previous tasks, this function
    produces only the current snap-shot of task jobs. In particular, tasks which generate
    variable number of inputs into following tasks will not produce the full range of jobs.

    ::
        verbose = 0 : Nothing
        verbose = 1 : Out-of-date Task names
        verbose = 2 : All Tasks (including any task function docstrings)
        verbose = 3 : Out-of-date Jobs in Out-of-date Tasks, no explanation
        verbose = 4 : Out-of-date Jobs in Out-of-date Tasks, with explanations and warnings
        verbose = 5 : All Jobs in Out-of-date Tasks,  (include only list of up-to-date tasks)
        verbose = 6 : All jobs in All Tasks whether out of date or not

    :param output_stream: where to print to
    :type output_stream: file-like object with ``write()`` function
    :param target_tasks: targets task functions which will be run if they are out-of-date
    :param forcedtorun_tasks: task functions which will be run whether or not they are out-of-date
    :param verbose: level 0 : nothing
                    level 1 : Out-of-date Task names
                    level 2 : All Tasks (including any task function docstrings)
                    level 3 : Out-of-date Jobs in Out-of-date Tasks, no explanation
                    level 4 : Out-of-date Jobs in Out-of-date Tasks, with explanations and warnings
                    level 5 : All Jobs in Out-of-date Tasks,  (include only list of up-to-date tasks)
                    level 6 : All jobs in All Tasks whether out of date or not
                    level 10: logs messages useful only for debugging ruffus pipeline code
    :param indent: How much indentation for pretty format.
    :param gnu_make_maximal_rebuild_mode: Defaults to re-running *all* out-of-date tasks. Runs minimal
                                          set to build targets if set to ``True``. Use with caution.
    :param wrap_width: The maximum length of each line
    :param runtime_data: Experimental feature for passing data to tasks at run time
    :param checksum_level: Several options for checking up-to-dateness are available: Default is level 1.
                    level 0 : Use only file timestamps
                    level 1 : As above, plus timestamp of successful job completion
                    level 2 : As above, plus a checksum of the pipeline function body
                    level 3 : As above, plus a checksum of the pipeline function default arguments and the additional arguments passed in by task decorators
    :param history_file: The database file which stores checksums and file timestamps for input/output files.
    :param verbose_abbreviated_path: whether input and output paths are abbreviated.
                    level 0: The full (expanded, abspath) input or output path
                    level > 1: The number of subdirectories to include. Abbreviated paths are prefixed with ``[,,,]/``
                    level < 0: level < 0: Input / Output parameters are truncated to ``MMM`` letters where ``verbose_abbreviated_path ==-MMM``. Subdirectories are first removed to see if this allows the paths to fit in the specified limit. Otherwise abbreviated paths are prefixed by ``<???>``
    """
    # do nothing!
    if verbose == 0:
        return

    #
    # default values
    #
    if verbose_abbreviated_path == None:
        verbose_abbreviated_path = 2
    if verbose == None:
        verbose = 4

    # EXTRA pipeline_run DEBUGGING
    global EXTRA_PIPELINERUN_DEBUGGING
    EXTRA_PIPELINERUN_DEBUGGING = False

    if output_stream == None:
        output_stream = sys.stdout


    if not hasattr(output_stream, "write"):
        raise Exception("The first parameter to pipeline_printout needs to be an output file, e.g. sys.stdout and not %s" % str(output_stream))

    if runtime_data == None:
        runtime_data = {}
    if not isinstance(runtime_data, dict):
        raise Exception("pipeline_run parameter runtime_data should be a dictionary of "
                        "values passes to jobs at run time.")

    if checksum_level is None:
        checksum_level = get_default_checksum_level()

    #
    #   pipeline must be a Pipeline or a string naming a pipeline
    #
    pipeline = lookup_pipeline (pipeline)
    #
    #   Make sure all tasks in dependency list are linked to real functions
    #
    pipeline._complete_task_setup()

    update_checksum_level_on_tasks(checksum_level)

    #
    # @active_if decorated tasks can change their active state every time
    #   pipeline_run / pipeline_printout / pipeline_printout_graph is called
    #
    update_active_states_for_all_tasks ()

    #
    #   target jobs
    #
    target_tasks = lookup_tasks_from_user_specified_names ("Target", target_tasks, pipeline.name)
    if not target_tasks:
        target_tasks = list(pipeline.tasks)
    forcedtorun_tasks = lookup_tasks_from_user_specified_names ("Forced to run", forcedtorun_tasks, pipeline.name)

    logging_strm = t_verbose_logger(verbose, verbose_abbreviated_path, t_stream_logger(output_stream), runtime_data)

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

    (incomplete_tasks,
    self_terminated_nodes,
    dag_violating_edges,
    dag_violating_nodes) = topologically_sorted_nodes(target_tasks, forcedtorun_tasks,
                                                        gnu_make_maximal_rebuild_mode,
                                                        extra_data_for_signal = [t_verbose_logger(0, 0, None, runtime_data), job_history])


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
    #   LOGGER level 6 : All jobs in All Tasks whether out of date or not
    if verbose == 2 or verbose >= 5:
        (all_tasks, ignore_param1, ignore_param2,
         ignore_param3) = topologically_sorted_nodes(target_tasks, True,
                                                     gnu_make_maximal_rebuild_mode,
                                                     extra_data_for_signal = [t_verbose_logger(0, 0, None, runtime_data), job_history])
        for m in get_completed_task_strings (incomplete_tasks, all_tasks, forcedtorun_tasks, verbose, verbose_abbreviated_path, indent, runtime_data, job_history):
            output_stream.write(textwrap.fill(m, subsequent_indent = wrap_indent, width = wrap_width) + "\n")

    output_stream.write("\n" + "_" * 40 + "\nTasks which will be run:\n\n")
    for t in incomplete_tasks:
        # LOGGER
        messages = t._printout(runtime_data, t in forcedtorun_tasks, job_history, True, verbose, verbose_abbreviated_path, indent)
        for m in messages:
            output_stream.write(textwrap.fill(m, subsequent_indent = wrap_indent, width = wrap_width) + "\n")

    if verbose:
        # LOGGER
        output_stream.write("_" * 40 + "\n")


#_________________________________________________________________________________________

#   get_semaphore

#_________________________________________________________________________________________
def get_semaphore (t, _job_limit_semaphores, syncmanager):
    """
    return semaphore to limit the number of concurrent jobs
    """
    #
    #   Is this task limited in the number of jobs?
    #
    if t.semaphore_name not in t._job_limit_semaphores:
        return None


    #
    #   create semaphore if not yet created
    #
    if t.semaphore_name not in _job_limit_semaphores:
        maximum_jobs_num = t._job_limit_semaphores[t.semaphore_name]
        _job_limit_semaphores[t.semaphore_name] = syncmanager.BoundedSemaphore(maximum_jobs_num)
    return _job_limit_semaphores[t.semaphore_name]

#_________________________________________________________________________________________
#
#   Parameter generator for all jobs / tasks
#
#________________________________________________________________________________________
def make_job_parameter_generator (incomplete_tasks, task_parents, logger, forcedtorun_tasks,
                                    task_with_completed_job_q, runtime_data, verbose,
                                    verbose_abbreviated_path,
                                    syncmanager,
                                    death_event,
                                    touch_files_only, job_history):

    inprogress_tasks = set()
    _job_limit_semaphores = dict()

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
                    job_completed_task, job_completed_task_name, job_completed_node_index, job_completed_name = item


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
                        job_completed_task._completed ()
                        # LOGGER: Out-of-date Tasks
                        log_at_level (logger, 1, verbose, "Completed Task = " + job_completed_task._get_display_name())

                except queue.Empty:
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
                        # LOGGER: Out-of-date Tasks
                        log_at_level (logger, 1, verbose, "Task enters queue = " + t._get_display_name() + (": Forced to rerun" if force_rerun else ""))
                        # LOGGER: logs All Tasks (including any task function docstrings)
                        # indent string
                        if len(t.func_description):
                            log_at_level (logger, 2, verbose, "    " + t.func_description)
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

                        job_name = t._get_job_name(descriptive_param, verbose_abbreviated_path, runtime_data)

                        #
                        #    don't run if up to date unless force to run
                        #
                        if force_rerun:
                            # LOGGER: Out-of-date Jobs in Out-of-date Tasks
                            log_at_level (logger, 3, verbose, "    force task %s to rerun " % job_name)
                        else:
                            if not t.needs_update_func:
                                # LOGGER: Out-of-date Jobs in Out-of-date Tasks
                                log_at_level (logger, 3, verbose, "    %s no function to check if up-to-date " % job_name)
                            else:
                                # extra clunky hack to also pass task info--
                                # makes sure that there haven't been code or arg changes
                                if t.needs_update_func == needs_update_check_modify_time:
                                    needs_update, msg = t.needs_update_func (*param, task=t, job_history = job_history, verbose_abbreviated_path = verbose_abbreviated_path)
                                else:
                                    needs_update, msg = t.needs_update_func (*param)

                                if not needs_update:
                                    # LOGGER: All Jobs in Out-of-date Tasks
                                    log_at_level (logger, 5, verbose, "    %s unnecessary: already up to date " % job_name)
                                    continue
                                else:
                                    # LOGGER: Out-of-date Jobs in Out-of-date Tasks: Why out of date
                                    if not log_at_level (logger, 4, verbose, "    %s %s " % (job_name, msg)):

                                        # LOGGER: Out-of-date Jobs in Out-of-date Tasks: No explanation
                                        log_at_level (logger, 3, verbose, "    %s" % (job_name))

                        #
                        #   Clunky hack to make sure input files exists right before
                        #        job is called for better error messages
                        #
                        if t.needs_update_func == needs_update_check_modify_time:
                            check_input_files_exist (*param)

                        # pause for one second before first job of each tasks
                        # @originate tasks do not need to pause, because they depend on nothing!
                        if cnt_jobs_created == 0 and touch_files_only < 2:
                            if "ONE_SECOND_PER_JOB" in runtime_data and runtime_data["ONE_SECOND_PER_JOB"] and t._action_type != Task._action_task_originate:
                                log_at_level (logger, 10, verbose, "   1 second PAUSE in job_parameter_generator\n\n\n")
                                time.sleep(1.01)
                            else:
                                time.sleep(0.1)


                        count_remaining_jobs[t] += 1
                        cnt_jobs_created += 1
                        cnt_jobs_created_for_all_tasks += 1
                        yield (param,
                                t._name,
                                t._node_index,
                                job_name,
                                t.job_wrapper,
                                t.user_defined_work_func,
                                get_semaphore (t, _job_limit_semaphores, syncmanager),
                                death_event,
                                touch_files_only)

                    # if no job came from this task, this task is complete
                    #   we need to retire it here instead of normal completion at end of job tasks
                    #   precisely because it created no jobs
                    if cnt_jobs_created == 0:
                        incomplete_tasks.remove(t)
                        t._completed ()
                        if not t.is_active:
                            log_at_level (logger, 2, verbose, "Inactive Task = " + t._get_display_name())
                        else:
                            log_at_level (logger, 2, verbose, "Uptodate Task = " + t._get_display_name())
                        # LOGGER: logs All Tasks (including any task function docstrings)
                        log_at_level (logger, 10, verbose, "   No jobs created for %s. Retired in parameter_generator " % t._name)

                        #
                        #   Add extra warning if no regular expressions match:
                        #   This is a common class of frustrating errors
                        #
                        if (verbose >= 1 and "ruffus_WARNING" in runtime_data and
                            t.param_generator_func in runtime_data["ruffus_WARNING"]):
                            for msg in runtime_data["ruffus_WARNING"][t.param_generator_func]:
                                logger.warning("    'In Task def %s(...):' %s " % (t._get_display_name(), msg))


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
                    exception_stack  = traceback.format_exc()
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
def feed_job_params_to_process_pool_factory (parameter_q, death_event, logger, verbose):
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

            if death_event.is_set():
                death_event.clear()
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




#_________________________________________________________________________________________

#   pipeline_get_task_names

#_________________________________________________________________________________________
def pipeline_get_task_names (pipeline = None):
    """
    Get all task names in a pipeline
    Not that does not check if pipeline is wired up properly
    """

    # EXTRA pipeline_run DEBUGGING
    global EXTRA_PIPELINERUN_DEBUGGING
    EXTRA_PIPELINERUN_DEBUGGING = False

    #
    #   pipeline must be a Pipeline or a string naming a pipeline
    #
    pipeline = lookup_pipeline (pipeline)

    #
    #   Make sure all tasks in dependency list are linked to real functions
    #
    pipeline._complete_task_setup()



    #
    #   Return task names for all nodes willy nilly
    #


    return [n._get_display_name() for n in node._all_nodes]


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
                 #verbose defaults to 1 if None
                 verbose                          = None,
                 runtime_data                     = None,
                 one_second_per_job               = None,
                 touch_files_only                 = False,
                 exceptions_terminate_immediately = False,
                 log_exceptions                   = False,
                 checksum_level                   = None,
                 multithread                      = 0,
                 history_file                     = None,
                 # defaults to 2 if None
                 verbose_abbreviated_path         = None,
                 pipeline                         = None):
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
                    level 1 : Out-of-date Task names
                    level 2 : All Tasks (including any task function docstrings)
                    level 3 : Out-of-date Jobs in Out-of-date Tasks, no explanation
                    level 4 : Out-of-date Jobs in Out-of-date Tasks, with explanations and warnings
                    level 5 : All Jobs in Out-of-date Tasks,  (include only list of up-to-date tasks)
                    level 6 : All jobs in All Tasks whether out of date or not
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
    :param one_second_per_job: To work around poor file timepstamp resolution for some file systems. Defaults to True if checksum_level is 0 forcing Tasks to take a minimum of 1 second to complete.
    :param runtime_data: Experimental feature for passing data to tasks at run time
    :param gnu_make_maximal_rebuild_mode: Defaults to re-running *all* out-of-date tasks. Runs minimal
                                          set to build targets if set to ``True``. Use with caution.
    :param history_file: The database file which stores checksums and file timestamps for input/output files.
    :param verbose_abbreviated_path: whether input and output paths are abbreviated.
                          level 0: The full (expanded, abspath) input or output path
                          level > 1: The number of subdirectories to include. Abbreviated paths are prefixed with ``[,,,]/``
                          level < 0: level < 0: Input / Output parameters are truncated to ``MMM`` letters where ``verbose_abbreviated_path ==-MMM``. Subdirectories are first removed to see if this allows the paths to fit in the specified limit. Otherwise abbreviated paths are prefixed by ``<???>``
    """

    #
    # default values
    #
    if touch_files_only == False:
        touch_files_only = 0
    elif touch_files_only == True:
        touch_files_only = 1
    else:
        touch_files_only = 2
        # we are not running anything so do it as quickly as possible
        one_second_per_job = False
    if verbose == None:
        verbose = 1
    if verbose_abbreviated_path == None:
        verbose_abbreviated_path = 2

    # EXTRA pipeline_run DEBUGGING
    global EXTRA_PIPELINERUN_DEBUGGING
    if verbose >= 10:
        EXTRA_PIPELINERUN_DEBUGGING = True
    else:
        EXTRA_PIPELINERUN_DEBUGGING = False


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

    if checksum_level is None:
        checksum_level = get_default_checksum_level()

    #
    #   Supplement mtime with system clock if using CHECKSUM_HISTORY_TIMESTAMPS
    #       we don't need to default to adding 1 second delays between jobs
    #
    if one_second_per_job == None:
         if checksum_level == CHECKSUM_FILE_TIMESTAMPS:
            log_at_level (logger, 10, verbose, "   Checksums rely on FILE TIMESTAMPS only and we don't know if the system file time resolution: Pause 1 second...")
            runtime_data["ONE_SECOND_PER_JOB"] = True
         else:
            log_at_level (logger, 10, verbose, "   Checksum use calculated time as well: No 1 second pause...")
            runtime_data["ONE_SECOND_PER_JOB"] = False
    else:
        log_at_level (logger, 10, verbose, "   One second per job specified to be %s" % one_second_per_job)
        runtime_data["ONE_SECOND_PER_JOB"] = one_second_per_job


    if verbose == 0:
        logger = black_hole_logger
    elif verbose >= 11:
        #   debugging aid: See t_stderr_logger
        #   Each invocation of add_unique_prefix adds a unique prefix to all subsequent output
        #       So that individual runs of pipeline run are tagged
        if hasattr(logger, "add_unique_prefix"):
            logger.add_unique_prefix()


    if touch_files_only and verbose >= 1:
        logger.info("Touch output files instead of remaking them.")

    #
    #   pipeline must be a Pipeline or a string naming a pipeline
    #
    pipeline = lookup_pipeline (pipeline)
    #
    #   Make sure all tasks in dependency list are linked to real functions
    #
    pipeline._complete_task_setup()

    #link_task_names_to_functions ()
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
    target_tasks = lookup_tasks_from_user_specified_names ("Target", target_tasks, pipeline.name)
    if not target_tasks:
        target_tasks = list(pipeline.tasks)
    forcedtorun_tasks = lookup_tasks_from_user_specified_names ("Forced to run", forcedtorun_tasks, pipeline.name)


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
                                                     extra_data_for_signal = [t_verbose_logger(0, 0, None, runtime_data), job_history])



    #
    #   If verbose >=10, for debugging:
    #       Prints which tasks trigger the pipeline rerun...
    #       i.e. start from the farthest task, prints out all the up to date tasks, and the first out of date task
    #
    (incomplete_tasks,
    self_terminated_nodes,
    dag_violating_edges,
    dag_violating_nodes) = topologically_sorted_nodes(  target_tasks, forcedtorun_tasks,
                                                        gnu_make_maximal_rebuild_mode,
                                                        extra_data_for_signal = [t_verbose_logger(verbose, verbose_abbreviated_path, logger, runtime_data), job_history])

    if len(dag_violating_nodes):
        dag_violating_tasks = ", ".join(t._name for t in dag_violating_nodes)

        e = error_circular_dependencies("Circular dependencies found in the "
                                        "pipeline involving one or more of (%s)" %
                                            (dag_violating_tasks))
        raise e



    #
    # get dependencies. Only include tasks which will be run
    #
    set_of_incomplete_tasks = set(incomplete_tasks)
    task_parents = defaultdict(set)
    for t in set_of_incomplete_tasks:
        task_parents[t] = set()
        for parent in t._outward:
            if parent in set_of_incomplete_tasks:
                task_parents[t].add(parent)


    #
    #   Print Complete tasks
    #
    #   LOGGER level 5 : All jobs in All Tasks whether out of date or not
    if verbose == 2 or verbose >= 5:
        (all_tasks, ignore_param1, ignore_param2,
         ignore_param3) = topologically_sorted_nodes(target_tasks, True,
                                                     gnu_make_maximal_rebuild_mode,
                                                     extra_data_for_signal = [t_verbose_logger(0, 0, None, runtime_data), job_history])
        # indent hardcoded to 4
        for m in get_completed_task_strings (incomplete_tasks, all_tasks, forcedtorun_tasks, verbose, verbose_abbreviated_path, 4, runtime_data, job_history):
            logger.info(m)


    #print json.dumps(task_parents.items(), indent=4, cls=task_encoder)
    logger.info("")
    logger.info("_" * 40)
    logger.info("Tasks which will be run:")
    logger.info("")
    logger.info("")



    # prepare tasks for pipeline run:
    #
    #   clear task outputs
    #       task.output_filenames = None
    #
    #    **********
    #      BEWARE
    #    **********
    #
    #    Because state is stored, ruffus is *not* reentrant.
    #
    #    **********
    #      BEWARE
    #    **********
    for t in incomplete_tasks:
        t._init_for_pipeline()


    #
    # prime queue with initial set of job parameters
    #
    death_event = syncmanager.Event()
    #death_event = None
    parameter_q = queue.Queue()
    task_with_completed_job_q = queue.Queue()
    parameter_generator = make_job_parameter_generator (incomplete_tasks, task_parents,
                                                        logger, forcedtorun_tasks,
                                                        task_with_completed_job_q,
                                                        runtime_data, verbose,
                                                        verbose_abbreviated_path,
                                                        syncmanager,
                                                        death_event,
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
        pool_func = map



    feed_job_params_to_process_pool = feed_job_params_to_process_pool_factory (parameter_q, death_event, logger, verbose)

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
    #   Rewrite for loop so we can call iter.next() with a timeout
    try:

        #for job_result in pool_func(run_pooled_job_without_exceptions, feed_job_params_to_process_pool()):
        ii  = iter(pool_func(run_pooled_job_without_exceptions, feed_job_params_to_process_pool()))
        while 1:
            #   Use a timeout of 3 years per job..., so that the condition we are waiting for in the thread
            #       can be interrupted by signals... In other words, so that Ctrl-C works
            #   Yucky part is that timeout is an extra parameter to IMapIterator.next(timeout=None)
            #       but next() for normal iterators do not take any extra parameters.
            if pool:
                job_result = ii.next(timeout=99999999)
            else:
                job_result = next(ii)
            # run next task
            log_at_level (logger, 11, verbose, "r" * 80 + "\n")
            t = node._lookup_node_from_index(job_result.node_index)

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
                log_at_level (logger, 10, verbose, "   Exception caught for %s" % job_result.job_name)
                job_errors.append(job_result.exception)
                tasks_with_errors.add(t)

                #
                # print to logger immediately
                #
                if log_exceptions:
                    log_at_level (logger, 10, verbose, "   Log Exception")
                    logger.error(job_errors.get_nth_exception_str())

                #
                # break if too many errors
                #
                if len(job_errors) >= parallelism or exceptions_terminate_immediately:
                    log_at_level (logger, 10, verbose, "   Break loop %s %s %s " % (exceptions_terminate_immediately, len(job_errors), parallelism) )
                    parameter_q.put(all_tasks_complete())
                    break


            # break immediately if the user says stop
            elif job_result.state == JOB_SIGNALLED_BREAK:
                job_errors.append(job_result.exception)
                job_errors.specify_task(t, "Exceptions running jobs")
                log_at_level (logger, 10, verbose, "   Break loop JOB_SIGNALLED_BREAK %s %s " % (len(job_errors), parallelism) )
                parameter_q.put(all_tasks_complete())
                break

            else:
                if job_result.state == JOB_UP_TO_DATE:
                    # LOGGER: All Jobs in Out-of-date Tasks
                    log_at_level (logger, 5, verbose, "    %s unnecessary: already up to date" % job_result.job_name)
                else:
                    # LOGGER: Out-of-date Jobs in Out-of-date Tasks
                    log_at_level (logger, 3, verbose, "    %s completed" % job_result.job_name)
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
                        # Remember to expand globs
                        #
                        for possible_glob_str in get_strings_in_nested_sequence(output_file_name):
                            for o_f_n in glob.glob(possible_glob_str):
                                #
                                # use paths relative to working directory
                                #
                                o_f_n = os.path.relpath(o_f_n)
                                try:
                                    log_at_level (logger, 10, verbose, "   Job History for : " + o_f_n)
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
                                            log_at_level (logger, 10, verbose, "   Switch to one second per job")
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


            log_at_level (logger, 10, verbose, "   _stop_dfs completed task after checksumming...")
            #
            #   _stop_dfs completed task after checksumming
            #
            task_with_completed_job_q.put((t, job_result.task_name, job_result.node_index, job_result.job_name))


            # make sure queue is still full after each job is retired
            # do this after undating which jobs are incomplete
            log_at_level (logger, 10, verbose, "   job errors?")
            if len(job_errors):
                #parameter_q.clear()
                #if len(job_errors) == 1 and not parameter_q._closed:
                log_at_level (logger, 10, verbose, "   all tasks completed...")
                parameter_q.put(all_tasks_complete())
            else:
                log_at_level (logger, 10, verbose, "   Fill queue with more parameter...")
                fill_queue_with_job_parameters(job_parameters, parameter_q, parallelism, logger, verbose)
    # The equivalent of the normal end of a fall loop
    except StopIteration as e:
        pass
    except:
        exception_name, exception_value, exception_Traceback = sys.exc_info()
        exception_stack  = traceback.format_exc()
        # save exception to rethrow later
        job_errors.append((None, None, exception_name, exception_value, exception_stack))
        log_at_level (logger, 10, verbose, "       Exception caught %s" % (exception_value))
        log_at_level (logger, 10, verbose, "       Exception caught %s" % (exception_name))
        log_at_level (logger, 10, verbose, "       Exception caught %s" % (exception_stack))
        log_at_level (logger, 10, verbose, "   Get next parameter size = %d" %
                                                    parameter_q.qsize())
        log_at_level (logger, 10, verbose, "   Task with completed jobs size = %d" %
                                                    task_with_completed_job_q.qsize())
        parameter_q.put(all_tasks_complete())
        try:
            death_event.clear()
        except:
            pass

        if pool:
            log_at_level (logger, 10, verbose, "       pool.close")
            pool.close()
            log_at_level (logger, 10, verbose, "       pool.terminate")
            try:
                pool.terminate()
            except:
                pass
            log_at_level (logger, 10, verbose, "       pool.terminated")
        raise job_errors


    #log_at_level (logger, 10, verbose, "       syncmanager.shutdown")
    #syncmanager.shutdown()


    if pool:
        log_at_level (logger, 10, verbose, "       pool.close")
        #pool.join()
        pool.close()
        log_at_level (logger, 10, verbose, "       pool.terminate")
        # an exception may be thrown after a signal is caught (Ctrl-C)
        #   when the EventProxy(s) for death_event might be left hanging
        try:
            pool.terminate()
        except:
            pass
        log_at_level (logger, 10, verbose, "       pool.terminated")

    # Switch back off EXTRA pipeline_run DEBUGGING
    EXTRA_PIPELINERUN_DEBUGGING = False

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
