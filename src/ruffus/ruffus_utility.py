#!/usr/bin/env python
################################################################################
#
#   ruffus_utility.py
#
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
:mod:`ruffus_utility` -- Overview
********************************************


.. moduleauthor:: Leo Goodstadt <ruffus@llew.org.uk>

    Common utility functions


"""




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
import os,copy
import re
import types
import glob    
if __name__ == '__main__':
    import sys
    sys.path.insert(0,".")
from ruffus_exceptions import *
#import task

                                
                                
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888



#_________________________________________________________________________________________
#
#   construct_filename_parameters_with_regex
# 
#_________________________________________________________________________________________
def construct_filename_parameters_with_regex(filename, regex, p):
    """
    recursively replaces file name specifications using regular expressions
    Non-strings are left alone
    """
    if isinstance(p, str):
        return regex.sub(p, filename) 
    elif non_str_sequence (p):
        return type(p)(construct_filename_parameters_with_regex(filename, regex, pp) for pp in p)
    else:
        return p
        
#_________________________________________________________________________________________
#
#   construct_filename_parameters_with_regex
# 
#_________________________________________________________________________________________
#def construct_filename_parameters_with_regex(filename, regex, p):
#    """
#    recursively replaces file name specifications using regular expressions
#    Non-strings are left alone
#    """
#    if isinstance(p, str):
#        return regex.sub(p, filename) 
#    elif non_str_sequence (p):
#        return tuple(construct_filename_parameters_with_regex(filename, regex, pp) for pp in p)
#    else:
#        return p

#_________________________________________________________________________________________


##_________________________________________________________________________________________
#
##   deprecated _is_str
#
##_________________________________________________________________________________________
#def _is_str(arg):
#    return isinstance(arg, str)

#_________________________________________________________________________________________

#   non_str_sequence

#_________________________________________________________________________________________
def non_str_sequence (arg):
    """
    Whether arg is a sequence.
    We treat strings / dicts however as a singleton not as a sequence
    
    """
    if (isinstance(arg, str)        or 
        isinstance(arg, unicode)    or 
        isinstance(arg, dict))       :
        return False
    try:
        test = iter(arg)
        return True
    except TypeError:
        return False

#_________________________________________________________________________________________

#   get_strings_in_nested_sequence_aux

#       helper function for next function

#_________________________________________________________________________________________
def get_strings_in_nested_sequence_aux(p, l = None):
    """
    Unravels arbitrarily nested sequence and returns lists of strings
    """
    if l == None:
        l = []
    if isinstance(p, str):
        l.append(p)
    elif non_str_sequence (p):
        for pp in p:
            get_strings_in_nested_sequence_aux(pp, l)
    return l

    
#_________________________________________________________________________________________

#   non_str_sequence

#_________________________________________________________________________________________
def get_strings_in_nested_sequence (p, first_only = False):
    """
    Traverses nested sequence and for each element, returns first string encountered
    """
    if p == None:
        return []
    
    #
    #  string is returned as list of single string
    # 
    if isinstance(p, str):
        return [p]
        
    #
    #  Get all strings flattened into list
    # 
    if not first_only:
        return get_strings_in_nested_sequence_aux(p)
        
        
    #
    #  Get all first string in each element
    # 
    elif non_str_sequence (p):
        filenames = []
        for pp in p:
            l = get_strings_in_nested_sequence_aux(pp)
            if len(l):
                filenames.append(l[0])
        return filenames

    return []

#_________________________________________________________________________________________

#   get_first_string_in_nested_sequence

#_________________________________________________________________________________________
def get_first_string_in_nested_sequence (p):
    if p == None:
        return None

    #
    #  string is returned as list of single string
    # 
    if isinstance(p, str):
        return p

    #
    #  Get all first string in each element
    # 
    elif non_str_sequence (p):
        filenames = []
        for pp in p:
            l = get_strings_in_nested_sequence_aux(pp)
            if len(l):
                return l[0]

    return None

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Encoders: turn objects and filenames into a more presentable format

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
def ignore_unknown_encoder(obj):
    if non_str_sequence (obj):
        return "[%s]" % ", ".join(map(ignore_unknown_encoder, obj))
    try:
        s= str(obj)
        if "object at " in s and s[0] == '<' and s[-1] == '>':
            pos = s.find(" object at ")
            s = "<" + s[1:pos].replace("__main__.", "") + ">"
        return s.replace('"', "'")
    except:
        return "<%s>" % str(obj.__class__).replace('"', "'")

def shorten_filenames_encoder (obj):
    if non_str_sequence (obj):
        return "[%s]" % ", ".join(map(shorten_filenames_encoder, obj))
    if isinstance(obj, str):
        if os.path.isabs(obj) and obj[1:].count('/') > 1:
            return os.path.split(obj)[1]
    return ignore_unknown_encoder(obj)



#
#_________________________________________________________________________________________
#
#   get_tasks_filename_globs_in_nested_sequence
#
#________________________________________________________________________________________ 
glob_letters = set('*[]?')
def is_glob(s):
    """Check whether 's' contains ANY of glob chars"""
    return len(glob_letters.intersection(s)) > 0

   
   
#_________________________________________________________________________________________
#
#   get_nested_tasks_or_globs
#
#________________________________________________________________________________________ 
def get_nested_tasks_or_globs(p, treat_strings_as_tasks = False, runtime_data_names=None, tasks=None, globs = None):
    """
    Get any tasks or globs which are within parameter
        tasks are returned as functions or function names
    """
    # 
    # create storage if this is not a recursive call
    # 
    if globs == None:
        runtime_data_names, tasks, globs = set(), set(), set()

    #
    #   task function
    # 
    if (type(p) == types.FunctionType):
        tasks.add(p)
    elif isinstance(p, runtime_parameter):
        runtime_data_names.add(p)

    #
    #   output_from treats all arguments as tasks or task names
    # 
    elif isinstance(p, output_from):
        for pp in p.args:
            get_nested_tasks_or_globs(pp, True, runtime_data_names, tasks, globs)

    elif isinstance(p, str):
        if treat_strings_as_tasks:
            tasks.add(p)
        elif is_glob(p):
            globs.add(p)

    elif non_str_sequence (p):
        for pp in p:
            get_nested_tasks_or_globs(pp, treat_strings_as_tasks, runtime_data_names, tasks, globs)
    return tasks, globs, runtime_data_names

#_________________________________________________________________________________________
#
#   replace_func_names_with_tasks
#
#________________________________________________________________________________________ 
def replace_func_names_with_tasks(p, func_or_name_to_task, treat_strings_as_tasks = False):
    """
    Replaces task functions or task name (strings) with the tasks they represent
    func_or_name_to_task are a dictionary of function and task names to tasks
    
    """
    # 
    # Expand globs or tasks as a list only if they are top level
    # 
    if type(p) == types.FunctionType:
        return func_or_name_to_task[p]

    #
    #   output_from treats all arguments as tasks or task names
    # 
    if isinstance(p, output_from):
        if len(p.args) == 1:
            return replace_func_names_with_tasks(p.args[0], func_or_name_to_task, True) 
        else:
            return [replace_func_names_with_tasks(pp, func_or_name_to_task, True) for pp in p.args]

    # 
    # strings become tasks if treat_strings_as_tasks
    # 
    if isinstance(p, str):
        if treat_strings_as_tasks:
            return func_or_name_to_task[p]
        return p
        
    # 
    # No conversions within dictionaries
    # 
    if isinstance(p, dict):
        return p

    # 
    # Other sequences are recursed down
    # 
    elif non_str_sequence(p):
        l = list()
        for pp in p:
            
            # 
            #   To be intuitive:
            #   arguments wrapped by output_from are always treated "in-line"
            #           e.g. 1, output_from("a") => 1, task_a
            #           e.g. 1, output_from("a", 2) => 1, task_a, 2
            # 
            if isinstance(pp, output_from):
                if len(pp.args) > 1:
                    l.extend(tuple(replace_func_names_with_tasks(pp, func_or_name_to_task, True)))
                elif len(pp.args) == 1:
                    l.append(replace_func_names_with_tasks(pp.args[0], func_or_name_to_task, True))
                # else len(pp.args) == 0 !! do nothing
                    
            else:
                l.append(replace_func_names_with_tasks(pp, func_or_name_to_task, treat_strings_as_tasks))
        return type(p)(l)

    # 
    # No expansions of non-string/non-sequences
    # 
    else:
        return p
        
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   compiling regular expressions

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#_________________________________________________________________________________________

#   suffix

#_________________________________________________________________________________________
class suffix(object):
    def __init__ (self, *args):
        self.args = args

#_________________________________________________________________________________________

#   regex

#_________________________________________________________________________________________
class regex(object):
    def __init__ (self, *args):
        self.args = args

#_________________________________________________________________________________________

#   wrap_exception_as_string

#_________________________________________________________________________________________
def wrap_exception_as_string ():
    """
    return exception as string to be rethrown
    """
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    msg = "%s.%s" % (exceptionType.__module__, exceptionType.__name__)
    exception_value  = str(exceptionValue)
    if len(exception_value):
        return msg + ": (%s)" % exception_value
    return msg


#_________________________________________________________________________________________

#   compile_regex

#_________________________________________________________________________________________
def compile_regex(enclosing_task, regex, error_object, descriptor_string):
    """
    throw error unless regular expression compiles
    """
    if not len(regex.args):
        raise error_object(enclosing_task, "%s: " % descriptor_string +
                                   "regex() is malformed\n" +
                                    "regex(...) should be used to wrap a regular expression string")
    if len(regex.args) > 1 or not isinstance(regex.args[0], str):
        raise error_object(enclosing_task, "%s: " % descriptor_string +
                                   "regex('%s') is malformed\n" % (regex.args,) +
                                    "regex(...) should only be used to wrap a single regular expression string")
    try:
        matching_regex = re.compile(regex.args[0])
        return matching_regex
    except:
        raise error_object(enclosing_task, "%s: regular expression " % descriptor_string +
                                                   "regex('%s') is malformed\n" % regex.args[0] +
                                                    "[%s]" %  wrap_exception_as_string())

#_________________________________________________________________________________________

#   compile_suffix

#_________________________________________________________________________________________
def compile_suffix(enclosing_task, regex, error_object, descriptor_string):
    """
    throw error unless regular expression compiles
    """
    if not len(regex.args):
        raise error_object(enclosing_task, "%s: " % descriptor_string +
                                    "suffix() is malformed.\n" +
                                     "suffix(...) should be used to wrap a string matching the suffices of file names")
    if len(regex.args) > 1 or not isinstance(regex.args[0], str):
        raise error_object(enclosing_task, "%s: " % descriptor_string +
                                   "suffix('%s') is malformed.\n" % (regex.args,) +
                                    "suffix(...) should only be used to wrap a single string matching the suffices of file names")
    try:
        matching_regex = re.compile(re.escape(regex.args[0]) + "$")
        return matching_regex
    except:
        raise error_object(enclosing_task, "%s: " % descriptor_string +
                                   "suffix('%s') is somehow malformed\n" % regex.args[0] +
                                    "[%s]" %  wrap_exception_as_string())

#_________________________________________________________________________________________

#   check_parallel_parameters

#_________________________________________________________________________________________
def check_parallel_parameters (enclosing_task, params, error_object):
    """
    Helper function for @files
    Checks format of parameters and
    whether there are input and output files specified for each job
    """
    if not len(params):
        raise Exception("@parallel parameters is empty.")

    for job_param in params:
        if isinstance(job_param, str):
            message = ("Wrong syntax for @parallel.\n"
                        "@parallel(%s)\n" % ignore_unknown_encoder(params) +
                        "If you are supplying parameters for a task " 
                        "running as a single job, "
                        "either don't put enclosing brackets at all (with each parameter "
                        "separated by commas) or enclose all parameters as a nested list of "
                        "lists, e.g. [['input', 'output' ...]]. "
                        )
            raise error_object(enclosing_task, message)



#_________________________________________________________________________________________

#   check_files_io_parameters

#_________________________________________________________________________________________
def check_files_io_parameters (enclosing_task, params, error_object):
    """
    Helper function for @files
    Checks format of parameters and
    whether there are input and output files specified for each job
    """
    if not len(params):
        raise Exception("@files I/O parameters is empty.")

    try:
        for job_param in params:
            if isinstance(job_param, str):
                raise TypeError
            
            if len(job_param) < 1:
                raise error_object(enclosing_task, "Missing input files for job " +   
                                                    ignore_unknown_encoder(job_param))      
            if len(job_param) < 2:
                raise error_object(enclosing_task, "Missing output files for job " +   
                                                    ignore_unknown_encoder(job_param))      
            if len(get_strings_in_nested_sequence(job_param[0:2])) == 0:            
                raise error_object(enclosing_task, "Input or output file parameters should "
                                                    "contain at least one or more file names strings." + 
                                                    ignore_unknown_encoder(job_param))
    except TypeError:
        # 
        # job_param was not a list
        # 
        message = ("Wrong syntax for @files.\n@files(%s)\n" % ignore_unknown_encoder(params) +
                    "If you are supplying parameters for a task " 
                    "running as a single job, "
                    "either don't put enclosing brackets at all (with each parameter "
                    "separated by commas) or enclose all parameters as a nested list of "
                    "lists, e.g. [['input', 'output' ...]]. "
                    )
        raise error_object(enclosing_task, message)

#_________________________________________________________________________________________
#
#   expand_nested_tasks_or_globs
#
#________________________________________________________________________________________ 
def expand_nested_tasks_or_globs(p, tasksglobs_to_filenames):
    """
    Expand globs and tasks "in-line", unless they are the top level, in which case turn
    it into a list
    
    N.B. Globs are only expanded if they are in tasksglobs_to_filenames
         This function is called for @split descriptors which leave output globs untouched
         for clarity. Thanks to Noah Spies for spotting this!
    """

    # 
    # Expand globs or tasks as a list only if they are top level
    # 
    if (    (isinstance(p, str) and is_glob(p) and p in tasksglobs_to_filenames) or 
            p.__class__.__name__ == '_task'     or 
            isinstance(p, runtime_parameter)    ):
        return tasksglobs_to_filenames[p]

    # 
    # No expansions of strings and dictionaries
    # 
    if isinstance(p, str) or isinstance(p, dict):
        return p

    # 
    # Other sequences are recursed down
    # 
    elif non_str_sequence(p):
        l = list()
        for pp in p:
            if (isinstance(pp, str) and pp in tasksglobs_to_filenames):
                l.extend(tasksglobs_to_filenames[pp])
            elif pp.__class__.__name__ == '_task' or isinstance(pp, runtime_parameter):
                files = tasksglobs_to_filenames[pp]
                # task may have produced a single output: in which case append
                if isinstance(files, str):
                    l.append(files)
                else:
                    l.extend(files)
            else:
                l.append(expand_nested_tasks_or_globs(pp, tasksglobs_to_filenames))
        return type(p)(l)

    # 
    # No expansions of non-string/non-sequences
    # 
    else:
        return p



        
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   special markers used by @files_re

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class combine(object):
    def __init__ (self, *args):
        self.args = args

class output_from(object):
    def __init__ (self, *args):
        self.args = args
    
class runtime_parameter(object):
    def __init__ (self, *args):
        if len(args) != 1 or not isinstance(args[0], str):
            raise Exception("runtime_parameter takes the name of the run time parameter as a single string")
        self.args = args

    
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Unit Testing code in test/test_ruffus_utility.py


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        
