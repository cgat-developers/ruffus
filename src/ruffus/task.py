#!/usr/bin/env python
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
# add self to search path for testing
if __name__ == '__main__':
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "python_modules")))
    myname = os.path.split(sys.argv[0])[1]
    myname = os.path.splitext(myname)[0];
else:
    myname = __name__


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
        print >>sys.stderr, message
    def debug (self, message):
         print >>sys.stderr, message


black_hole_logger = t_black_hole_logger()
stderr_logger     = t_stderr_logger()


       
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   needs_update_func

#       functions which are called to see if a job needs to be updated
#
#   Each task is a series of parallel jobs
#           each of which has the following pseudo-code
# 
#   for param in param_generator_func():
#       if needs_update_func(*param):
#           job_wrapper(*param)
# 
#   N.B. param_generator_func yields iterators of *sequences*
#   if you are generating single parameters, turn them into lists:
#   
#       for a in alist:
#           yield (a,)
#
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#_________________________________________________________________________________________

#   needs_update_check_directory_missing 

#       N.B. throws exception if this is an ordinary file, not a directory


#_________________________________________________________________________________________
def needs_update_check_directory_missing (dirs):
    """
    Called per directory:
        Does it exist?
        Is it an ordinary file not a directory? (throw exception
    """
    for d in dirs:
        #print >>sys.stderr, "check directory missing %d " % os.path.exists(d) # DEBUG
        if not os.path.exists(d):
            return True
        if not os.path.isdir(d):
            raise error_not_a_directory("%s already exists but as a file, not a directory" % d )
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

    
    
    
    
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   param_factories

#       makes python generators which yield parameters for
#
#           A) needs_update_func 
#           B) job_wrapper

#       Each task is a series of parallel jobs
#           each of which has the following pseudo-code
# 
#       for param in param_generator_func():
#           if needs_update_func(*param):
#               act_func(*param)
#
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#_________________________________________________________________________________________

#   args_param_factory

#       iterates through supplied list 
#_________________________________________________________________________________________
def args_param_factory (orig_args):
    """
so that::
    
        @parallel('a', 'b', 'c') 
        def task_func (A, B, C):
            pass

and::
   
        parameters=[
                     ['a', 'b', 'c'],        # first job
                   ]        
        @parallel(parameters) 
        def task_func (A, B, C):
            pass

both call::
    
            task_func(A='a', B = 'b', C = 'c')
    """
    # multiple jobs with input/output parameters etc.
    if len(orig_args) > 1:
        params = copy.copy([list(orig_args)])
    else:
        params = copy.copy(orig_args[0])

    def iterator():
        for job_param in params:
            #print >> sys.stderr, dumps(job_param, indent=4) # DEBUG
            yield job_param
    return iterator

    
    
    
    
    
    
#_________________________________________________________________________________________

#   touch_file_factory

#_________________________________________________________________________________________
def _touch_file_factory (orig_args, register_cleanup):
    """
    Creates function, which when called, will touch files
    """
    file_names = orig_args
    if is_str (orig_args):
        file_names = [orig_args]
    else:
        # make copy so when original is modifies, we don't get confused!
        file_names = list(orig_args)
        
    def do_touch_file ():
        for f  in file_names:
            if not os.path.exists(f):
                open(f, 'w')
            else:
                os.utime(f, None)
            register_cleanup(f, "touch")
    return do_touch_file
        
    
    
    
    
    
    
        
        
        

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



class follows(task_decorator):
    """
    **@follows** (parent_task1, "module_X.parent_task2")

        Takes a list of tasks which have to be run *before* this function
        Dependencies can be quoted or unquoted function names.
        Quoted function names allow dependencies to be added before the function is defined

        Functions in other modules need to be fully qualified


        For convenience, ``mkdir`` can be used to specify 
        directories which need to be created (if they don't exist) before
        the task is run.

        e.g::
            
            @follows(task_x, mkdir("/output/directory") ...)
    """
    pass
    
class files(task_decorator):
    """
    **@files** ([[job1.input, job1.output, job1.optional_extra_parameters], ...])
    
    **@files** (input_file, output_file, optional_extra_parameters)

    **@files** (custom_function)

    The first two parameters in each set represent the input and output of the each job.
    Only out of date jobs will be run.
    By default, this is by checking input/output file timestamps.
    (On some file systems, timestamps have a resolution in seconds.)

    The input and output files for each job can be 
        * A single file name
        * A list of files
        * ``None``
    
    If the input file is ``None``, the job will run if any output file is missing.
    
    If the output file is ``None``, the job will always run.
    
    If any of the output files is missing, the job will run.
    
    If any of the input files is missing when the job is run, a
    ``MissingInputFileError`` exception will be raised.
        
    Example::

        from ruffus import *
        parameters = [
                            [ 'a.1', 'a.2', 'A file'], # 1st job
                            [ 'b.1', 'b.2', 'B file'], # 2nd job
                      ]

        @files(parameters)
        def parallel_io_task(infile, outfile, text):
            infile_text = open(infile).read()
            f = open(outfile, "w").write(infile_text + "\\n" + text)

        pipeline_run([parallel_io_task])


    Parameters can be generated on the fly as well.
    Example::

        from ruffus import *
        def generate_parameters_on_the_fly():
            parameters = [
                                ['input_file1', 'output_file1', 1, 2], # 1st job
                                ['input_file2', 'output_file2', 3, 4], # 2nd job
                                ['input_file3', 'output_file3', 5, 6], # 3rd job
                         ]
            for job_parameters in parameters:
                yield job_parameters

        @files(generate_parameters_on_the_fly)
        def parallel_io_task(input_file, output_file, param1, param2):
            sys.stderr.write("    Parallel task %s: " % name)
            sys.stderr.write("%d + %d = %d\\n" % (param1, param2, param1 + param2))
        
        pipeline_run([parallel_task])
"""
    pass
    

class files_re(task_decorator):
    """
    **@files_re** (glob/file_list, matching_regex, output_file)
    
    **@files_re** (glob/file_list, matching_regex, input_file, output_file, [extra_parameters,...] )

    Generates a list of i/o files for each job in the task:
    Only out of date jobs will be run (See @files).
    
    #. ``matching_regex`` is a python regular expression.
    #. The first parameter are input file(s)
    #. The second parameter are output file(s)

    These are used to check if jobs are up to date.
    
    All parameters can be:
    
        #. ``None``
        #. A string
        #. A sequence of strings
        #. Anything else
    
    Strings and sequences of strings will be treated as regular expression substitution
    patterns, using matches from ``matching_regex``.
    
    See python `regular expression (re) <http://docs.python.org/library/re.html>`_ 
    documentation for details of the syntax
   
    `None` and all other types of objects are passed through unchanged.
        
        
    Operation:    

        1) For each file in the ``glob`` (See `glob <http://docs.python.org/library/glob.html>`_) 
           results or ``file_list``.
        2) Discard all file names those which don't matching ``matching_regex``
        3) Generate parameters using regular expression pattern substitution
       
    Example::
    
        from ruffus import *
        #
        #   convert all files ending in ".1" into files ending in ".2"
        #
        @files_re('*.1', '(.*).1', r'\\1.2')
        def task_re(infile, outfile):
            open(outfile, "w").write(open(infile).read() + "\\nconverted\\n")
        
        pipeline_run([task_re])
   
       
"""
    pass
class check_if_uptodate(task_decorator):
    """
    **@check_if_uptodate** (dependency_checking_func)
    
    Checks to see if a job is up to date, and needs to be run.
    dependency_checking_func() needs to handle the same number of parameters as the
    task function
    
    These two examples, using automatic and manual dependency checking produce
    the same output.
    Example 1: Automatic::

        from ruffus import *
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")
                    
        pipeline_run([create_if_necessary])


    Could be rewritten as::
    Example 2: Manual::
        
        from ruffus import *
        import os
        def check_file_exists(input_file, output_file):
            return not os.path.exists(output_file)
        
        @parallel([[None, "a.1"]])
        @check_if_uptodate(check_file_exists)
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")
        
        pipeline_run([create_if_necessary])
        
    Both produce the same output::
    
        Task = create_if_necessary
            Job = [null, "a.1"] completed
        

    """
    pass

class parallel(task_decorator):
    """
**@parallel** ([[job1_params, ...], [job2_params, ...]...])

**@parallel** (parameter_generating_func)

    The task function will be called iteratively 
    with each set of parameters (possibly in parallel)

    No dependency checking is carried out.
    
    Example::
    
        from ruffus import *
        parameters = [
                         ['A', 1, 2], # 1st job
                         ['B', 3, 4], # 2nd job
                         ['C', 5, 6], # 3rd job
                     ]
        @parallel(parameters)                                                     
        def parallel_task(name, param1, param2):                                  
            sys.stderr.write("    Parallel task %s: " % name)                     
            sys.stderr.write("%d + %d = %d\\n" % (param1, param2, param1 + param2))
        
        pipeline_run([parallel_task])

        
    """
    pass
class posttask(task_decorator):
    """
    Calls functions to signal the completion of each task::
    
        from ruffus import *
        
        def task_finished():
            print "hooray"
            
        @posttask(task_finished)
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")
                    
        pipeline_run([create_if_necessary])

    .. note::

        The function(s) provided to ``@posttask`` will be called if the ruffus passes 
        through a task, even if none of its jobs are run because they are up-to-date.
        This happens when a upstream task is out-of-date, and the execution passes through
        this point in the pipeline
        

    If ``touch_file`` is specified, the enclosed files(s) will be ``touch``\ -ed::

        from ruffus import *

        @posttask(touch_file("task_completed.flag"))
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")

        pipeline_run([create_if_necessary])
    """
    pass
     
        
        
        

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   special marker used by follows

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class mkdir(object):
    def __init__ (self, *args):
        self.args = args

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   special marker used by post_task

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class touch_file(object):
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
    extra_param = "" if len(param) == 2 else ", " + shorten_filenames_encoder(param[2:])[1:-1]
    return ("Job = [%s -> %s%s]" % (shorten_filenames_encoder(param[0]),
                                    shorten_filenames_encoder(param[1]),
                                    extra_param))

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
    elif is_str(o):
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
    
    (param, task_name, job_descriptor, needs_update_func, job_wrapper, 
        user_defined_work_func, do_log, force_rerun) = process_parameters
    
    if do_log:
        job_name = job_descriptor(param)
    else:
        job_name = None
    
    try:
        # don't run if up to date
        if not force_rerun and needs_update_func:
            if not needs_update_func (*param):
                return t_job_result(task_name, JOB_UP_TO_DATE, job_name, None, None)
                
            #    Clunky hack to make sure input files exists right before 
            #        job is called for better error messages
            if needs_update_func == needs_update_check_modify_time:
                check_input_files_exist (*param)


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
                             job_descriptor(param), 
                             exception_name, 
                             exception_value, 
                             exception_stack])
        


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
                    "task_files_func",
                    "task_files",
                    "task_mkdir",
                    "task_parallel",
                    ]
    action_unspecified      = 0
    action_task             = 1
    action_task_files_re    = 2
    action_task_files_func  = 3
    action_task_files       = 4
    action_mkdir            = 5
    action_parallel         = 6

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

        # function which is decorated and does the actual work
        self.user_defined_work_func = None
        
        # functions which will be called when task completes
        self.post_task_functions    = []
                
        # give makedir automatically made parent tasks unique names
        self.cnt_task_mkdir         = 0
        
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
            old_action = _task.action_names[self.action_type]
            new_action = _task.action_names[new_action_type]
            actions = " and ".join(list(set((old_action, new_action))))
            raise error_decorator_args(("Duplicate task names: Task/function %s has been " +
                                        "specified more than once (%s) ") % 
                                        (self._name, actions))
        self._action_type = new_action_type
        #
        #   DEBUGG
        # 
        self._action_type_desc = _task.action_names[new_action_type]


    #_________________________________________________________________________________________

    #   printout

    #_________________________________________________________________________________________
    def printout (self, stream, force_rerun, long_winded=False, indent = 4):
        """
        Print out all jobs for this task
        """
        indent_str = ' ' * indent
        
        task_name = self._name.replace("__main__.", "")
        stream.write("Task = " + task_name + ("    >>Forced to rerun<<\n" if force_rerun else "\n"))
        if long_winded:
            stream.write(indent_str + '"' + self._description + '"\n')

        #
        #   No parameters: just call task function 
        #
        if self.param_generator_func == None:
            stream.write(indent_str + self._name + "()\n")
        else:
            for param in self.param_generator_func():
                uptodate = '   '
                if self.needs_update_func and not self.needs_update_func (*param):
                    uptodate = "U: "
                stream.write(indent_str + uptodate + self.job_descriptor(param) + "\n")

        stream.write("\n")

    


    #_____________________________________________________________________________________

    #   signal
    # 
    #       returns whether up to date
    # 
    #_____________________________________________________________________________________
    def signal (self):
        """
        If up to date: signal = true
        If true, depth first search will not pass through this node
        """
        try:
            #
            #   Always needs update if no way to check if up to date
            #
            if self.needs_update_func == None:
                return False
                
            #
            #   if no parameters, just return the results of needs update
            # 
            if self.param_generator_func == None:
                return not self.needs_update_func()
            else:
                #
                #   return not up to date if ANY jobs needs update
                # 
                for param in self.param_generator_func():
                    if self.needs_update_func (*param):
                        return False
                return True
                
        # rethrow exception after adding task name
        except error_task, inst:
            inst.specify_task(self, "Exceptions in dependency checking")
            raise


        
        

        

            
            
            
            
            
            
            
            
            
            
            
            
    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888

    #       task handlers
    
    #         sets 
    #               1) action_type
    #               2) param_generator_func
    #               3) needs_update_func
    #               4) job wrapper


    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        
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

        #   Use parameters generated by a custom function
        if len(orig_args) == 1 and type(orig_args[0]) == types.FunctionType:
            self.set_action_type (_task.action_task_files_func)
            self.param_generator_func = orig_args[0]

        #   Use parameters in supplied list
        else:
            self.set_action_type (_task.action_task_files)
            self.param_generator_func = file_list_io_param_factory (orig_args)

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

        

        # no passed: single call
        if len(orig_args) == 0:
            self.param_generator_func = None
            
        # custom function will generate params 
        elif type(orig_args[0]) == types.FunctionType:
            self.param_generator_func = orig_args[0]
            
        # list of  params 
        else:
            self.param_generator_func = args_param_factory(orig_args)
            


    #_________________________________________________________________________________________

    #   task_files_re

    #_________________________________________________________________________________________
    def task_files_re (self, orig_args):
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
        self.set_action_type (_task.action_task_files_re)
        
        # glob or file name list
        if (is_str(orig_args[0]) or 
            (non_str_sequence(orig_args[0]) and is_str(orig_args[0][0]))):
            self.param_generator_func = glob_regex_io_param_factory (*orig_args)
        
        # task
        else:
            # output from wrapped tasks or task names
            if isinstance(orig_args[0], output_from):
                tasks = self.task_follows(orig_args[0].args)

            # single task decorated function
            elif (type(orig_args[0]) == types.FunctionType):
                tasks = self.task_follows([orig_args[0]])
                
            # multiple task decorated function
            else:
                tasks = self.task_follows(orig_args[0])
                
            self.param_generator_func = glob_regex_io_param_factory (output_from(*tasks), *orig_args[1:])
            
            
        self.needs_update_func    = self.needs_update_func or needs_update_check_modify_time
        self.job_wrapper          = job_wrapper_io_files
        self.job_descriptor       = io_files_job_descriptor

    

    #_________________________________________________________________________________________

    #   task_mkdir
    
    #       only called within task_follow

    #_________________________________________________________________________________________
    def task_mkdir (self, orig_args):
        """
        list of directory names or a single argument which is aa list of directory names
        Creates directory if missing
        """
        #   jump through hoops 
        #   all directories created in one job to avoid race conditions
        #    so we are converting [a,b,c] into [   [[a, b,c]]   ]
        self.set_action_type (_task.action_mkdir)
        if not is_str(orig_args[0]):
            orig_args = orig_args[0]
        param_func                = args_param_factory([[[sorted(orig_args)]]])
        
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
            if is_str(arg):
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
                self.post_task_functions.append(_touch_file_factory (arg.args, register_cleanup))
            elif type(arg) == types.FunctionType:
                self.post_task_functions.append(arg)
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
    if is_str(task_names) or type(task_names) == types.FunctionType:
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
def pipeline_printout(output_stream, target_tasks, forcedtorun_tasks = [], long_winded=False, indent = 4,
                                    gnu_make_maximal_rebuild_mode  = True,
                                    test_all_task_for_update        = True):
    """
    Printouts the parts of the pipeline which will be run

    Because the parameters of some jobs depend on the results of previous tasks, this function
    produces only the current snap-shot of task jobs. In particular, tasks which generate 
    variable number of inputs into following tasks will not produce the full range of jobs. 
    
    :param output_stream: where to print to
    :type output_stream: file-like object with ``write()`` function
    :param target_tasks: targets task functions which will be run if they are out-of-date
    :param forcedtorun_tasks: task functions which will be run whether or not they are out-of-date
    :param long_winded: More verbose output
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
    (topological_sorted,
    self_terminated_nodes,
    dag_violating_edges,
    dag_violating_nodes) = topologically_sorted_nodes(target_tasks, forcedtorun_tasks, 
                                                        gnu_make_maximal_rebuild_mode,
                                                        test_all_task_for_update)


    if len(dag_violating_nodes):
        dag_violating_tasks = ", ".join(t._name for t in dag_violating_nodes)

        e = error_circular_dependencies("Circular dependencies found in the "
                                        "pipeline involving one or more of (%s)" %
                                            (dag_violating_tasks))
        raise e

    for task in topological_sorted:
        task.printout(output_stream, task in forcedtorun_tasks, long_winded, indent)

#_________________________________________________________________________________________
#
#   Parameter generator for all jobs / tasks
#
#________________________________________________________________________________________ 
def make_job_parameter_generator (incomplete_tasks, task_parents, logger, forcedtorun_tasks, 
                                                        count_remaining_jobs):

    inprogress_tasks = set()

    def parameter_generator():
        #print >>sys.stderr, "   job_parameter_generator BEGIN" # DEBUG PIPELINE
        while len(incomplete_tasks):
            for task in list(incomplete_tasks):              
                #print >>sys.stderr, "   job_parameter_generator next task = %s" % task._name # DEBUG PIPELINE
                # ignore tasks in progress
                if task in inprogress_tasks:
                    continue

                #print >>sys.stderr, "   job_parameter_generator task %s not in progress" % task._name # DEBUG PIPELINE
                # ignore tasks with incomplete dependencies
                for parent in task_parents[task]:                  
                    if parent in incomplete_tasks:         
                        break
                else:                                        
                    #print >>sys.stderr, "   job_parameter_generator task %s parents completed" % task._name # DEBUG PIPELINE
                    force_rerun = task in forcedtorun_tasks
                    # 
                    # log task
                    # 
                    task_name = task._name.replace("__main__.", "")
                    if logger:
                        logger.info("Start Task = " + task_name + (": Forced to rerun" if force_rerun else ""))
                        if len(task._description):
                            logger.debug("    " + task._description)
                    inprogress_tasks.add(task)


                    #
                    #   If no parameters: just call task function (empty list)
                    #
                    if task.param_generator_func == None:
                        parameters = ([],)
                    else:
                        parameters = task.param_generator_func()
                    for param in parameters:
                        count_remaining_jobs[task] += 1
                        yield (param, 
                                task._name,
                                task.job_descriptor, 
                                task.needs_update_func, 
                                task.job_wrapper, 
                                task.user_defined_work_func,
                                logger != None, 
                                force_rerun)

            yield waiting_for_more_tasks_to_complete()

        yield all_tasks_complete()
        # This function is done
        #print >>sys.stderr, "   job_parameter_generator END" # DEBUG PIPELINE

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
        # only necessary for multiprocessing queue. Since we are not sharing th queue
        # with any other process...
        #parameter_q.close()
        #print >>sys.stderr, "   Parameter queue closed" # DEBUG PIPELINE
        
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
def pipeline_run(target_tasks, forcedtorun_tasks = [], multiprocess = 1, logger = stderr_logger, 
                                    gnu_make_maximal_rebuild_mode  = True):
    """
    Run pipelines.

    :param target_tasks: targets task functions which will be run if they are out-of-date
    :param forcedtorun_tasks: task functions which will be run whether or not they are out-of-date
    :param multiprocess: The number of concurrent jobs
    :param logger: Where progress will be logged. Defaults to stderr output. 
    :type logger: `logging <http://docs.python.org/library/logging.html>`_ objects
    :param gnu_make_maximal_rebuild_mode: Defaults to re-running *all* out-of-date tasks. Runs minimal
                                          set to build targets if set to ``True``. Use with caution. 


    """




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
                                                        gnu_make_maximal_rebuild_mode)

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
    for task in incomplete_tasks:
        task_parents[task] = set()
        for parent in task._outward:
            if parent in incomplete_tasks:
                task_parents[task].add(parent)
    #print json.dumps(task_parents.items(), indent=4, cls=task_encoder)
    
    
    

    # 
    # prime queue with initial set of job parameters    
    # 
    parameter_q = Queue()

    count_remaining_jobs = defaultdict(int)
    parameter_generator = make_job_parameter_generator (incomplete_tasks, task_parents, 
                                                        logger, forcedtorun_tasks, 
                                                        count_remaining_jobs)
    job_parameters = parameter_generator()
    fill_queue_with_job_parameters(job_parameters, parameter_q, multiprocess)


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
        
        task = node.lookup_node_from_name(job_result.task_name)
        count_remaining_jobs[task] = count_remaining_jobs[task] - 1
        
        last_job_in_task = False
        if count_remaining_jobs[task] == 0:
            incomplete_tasks.remove(task)
            last_job_in_task = True
            
        elif count_remaining_jobs[task] < 0:
            raise Exception("Task [%s] job count < 0" % task._name)
            
        # only save poolsize number of errors            
        if job_result.state == JOB_ERROR:
            job_errors.append(job_result.exception)
            tasks_with_errors.add(task)
            if len(job_errors) >= multiprocess:
                break
                
        # break immediately if the user says stop
        elif job_result.state == JOB_SIGNALLED_BREAK:
            job_errors.append(job_result.exception)
            tasks_with_errors.add(task)
            break

        elif logger:
            if job_result.state == JOB_UP_TO_DATE:
                logger.info("    %s unnecessary: already up to date" % job_result.job_name)
            else:
                logger.info("    %s completed" % job_result.job_name)
            
        #
        # Current Task completed
        #             
        if last_job_in_task:

            #   call job completion signals
            for f in task.post_task_functions:
                f()
            if logger:
                short_task_name = job_result.task_name.replace('__main__.', '')
                logger.info("Completed Task = " + short_task_name)

            
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
        for task in tasks_with_errors:
            errt.specify_task(task, "Exceptions running jobs")
        raise errt



        
#   use high resolution timestamps where available            
#       default in python 2.5 and greater
#   N.B. File modify times / stat values have 1 second precision for many file systems
#       and may not be accurate to boot, especially over the network.
os.stat_float_times(True)
