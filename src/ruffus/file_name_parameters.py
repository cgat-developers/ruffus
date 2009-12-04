#!/usr/bin/env python
################################################################################
#
#   file_name_parameters
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
:mod:`file_name_parameters` -- Overview
********************************************


.. moduleauthor:: Leo Goodstadt <ruffus@llew.org.uk>

    Handles file names for ruffus


"""




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
import os,copy
import re
import glob    
from operator import itemgetter
from itertools import groupby

if __name__ == '__main__':
    import sys
    sys.path.insert(0,".")

from ruffus_exceptions import *
from file_name_parameters import *
from ruffus_utility import *


                                
                                
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888




       
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
            return True, "Directory [%s] is missing" % d
        if not os.path.isdir(d):
            raise error_not_a_directory("%s already exists but as a file, not a directory" % d )
    return False, "All directories exist"

#_________________________________________________________________________________________

#   check_input_files_exist

#_________________________________________________________________________________________
def check_input_files_exist (*params):
    """
    If inputs are missing then there is no way a job can run successful.
    Must throw exception.
    This extra function is a hack to make sure input files exists right before 
        job is called for better error messages, and to save things from blowing
        up inside the task function
    """
    if len(params):
        input_files = params[0]
        for f in get_strings_in_nested_sequence(input_files):
            if not os.path.exists(f):
                raise MissingInputFileError("No way to run job: "+
                                            "Input file ['%s'] does not exist" % f)

#_________________________________________________________________________________________

#   needs_update_check_modify_time

#_________________________________________________________________________________________
def needs_update_check_modify_time (*params):
    """
    Given input and output files, see if all exist and whether output files are later than input files
    Each can be 
        #. string: assumed to be a filename "file1"
        #. any other type 
        #. arbitrary nested sequence of (1) and (2)
        
    """
    # missing output means build
    if len(params) < 2:
        return True


    i, o = params[0:2]
    i = get_strings_in_nested_sequence(i)
    o = get_strings_in_nested_sequence(o)

    # 
    # build: missing output file
    # 
    if len(o) == 0:
        return True, "Missing output file"

    # missing input / output file means always build                
    for io in (i, o):
        for p in io:
            if not os.path.exists(p):
                return True, "Missing file %s" % p

    #
    #   missing input -> build only if output absent
    # 
    if len(i) == 0:
        return False, "Missing input files"
    
    
    #
    #   get sorted modified times for all input and output files 
    #
    filename_to_times = [[], []]
    file_times = [[], []]
    for index, io in enumerate((i, o)):
        for f in io:
            mtime = os.path.getmtime(f)
            file_times[index].append(mtime)
            filename_to_times[index].append((mtime, f))
        filename_to_times[index].sort()

    # 
    #   update if any input file >= (more recent) output fifle
    #
    if max(file_times[0]) >= min(file_times[1]):
        return True, "Need update file times= %s" % str(filename_to_times)
    return False, "Up to date"


    
    
#_________________________________________________________________________________________
#
#   is_file_re_combining
# 
#_________________________________________________________________________________________
def is_file_re_combining (old_args):
    """
    Helper function for @files_re
    check if parameters wrapped in combine
    """
    combining_all_jobs = False
    orig_args = []
    for arg in old_args:
        if isinstance(arg, combine):
            combining_all_jobs = True
            if len(arg.args) == 1:
                orig_args.append(arg.args[0])
            else:
                orig_args.append(arg[0].args)
        else:
            orig_args.append(arg)
    return combining_all_jobs, orig_args


#_________________________________________________________________________________________

#   file_names_from_tasks_globs 

#_________________________________________________________________________________________
def file_names_from_tasks_globs(input_params, tasks, globs, runtime_data_names, 
                                runtime_data, do_not_expand_single_job_tasks = False):
    """
    Replaces glob specifications and tasks with actual files / task output
    """
    
    #
    # N.B. get_output_files() should never have the flattened flag == True
    #       do that later in get_strings_in_nested_sequence
    # 
    
    # special handling for chaining tasks which conceptual have a single job
    #       i.e. @merge and @files/@parallel with single job parameters
    if input_params.__class__.__name__ == '_task' and do_not_expand_single_job_tasks:
        return input_params.get_output_files(True, runtime_data)


    task_or_glob_to_files = dict()
    
    # look up globs and tasks    
    for g in globs:
        task_or_glob_to_files[g] = sorted(glob.glob(g))
    for t in tasks:
        of = t.get_output_files(False, runtime_data)
        task_or_glob_to_files[t] = of
    for n in runtime_data_names:
        data_name = n.args[0]
        if data_name in runtime_data:
            task_or_glob_to_files[n] = runtime_data[data_name]
        else:
            raise error_missing_runtime_parameter("The inputs of this task depends on " +
                                                  "the runtime parameter " +
                                                  "'%s' which is missing " %  data_name)
        
        

    return expand_nested_tasks_or_globs(input_params, task_or_glob_to_files)
    

    
    
    
    
    
    
    
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
#       Test Usage:
#
#
#       param_func = xxx_factory(tasks, globs, orig_input_params, ...)
#
#        for params in param_func():                                                                          
#           i, o = params[0:1]
#           print " input_params = " , i                                                                
#           print "output  = " , o                                                                
#
# 
# 
# 
# 
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#_________________________________________________________________________________________

#   touch_file_factory

#_________________________________________________________________________________________
def touch_file_factory (orig_args, register_cleanup):
    """
    Creates function, which when called, will touch files
    """
    file_names = orig_args
    if isinstance (orig_args, str):
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


#_________________________________________________________________________________________

#   file_param_factory 

#       orig_args = ["input", "output", 1, 2, ...] 
#       orig_args = [
#                       ["input0",               "output0",                1, 2, ...]   # job 1
#                       [["input1a", "input1b"], "output1",                1, 2, ...]   # job 2
#                       ["input2",               ["output2a", "output2b"], 1, 2, ...]   # job 3
#                       ["input3",               "output3",                1, 2, ...]   # job 4
#                   ] 
#       
#_________________________________________________________________________________________
def args_param_factory (orig_args):
    """
    Factory for functions which 
        yield tuples of inputs, outputs / extras                            

    ..Note::

        1. Each job requires input/output file names
        2. Input/output file names can be a string, an arbitrarily nested sequence
        3. Non-string types are ignored
        3. Either Input or output file name must contain at least one string

    """
    def iterator(runtime_data):
        for job_param in orig_args:
            yield job_param
    return iterator

#_________________________________________________________________________________________

#   file_param_factory 

#       orig_args = ["input", "output", 1, 2, ...] 
#       orig_args = [
#                       ["input0",               "output0",                1, 2, ...]   # job 1
#                       [["input1a", "input1b"], "output1",                1, 2, ...]   # job 2
#                       ["input2",               ["output2a", "output2b"], 1, 2, ...]   # job 3
#                       ["input3",               "output3",                1, 2, ...]   # job 4
#                   ] 
#       
#_________________________________________________________________________________________
def files_param_factory (tasks, globs, input_params, runtime_data_names, 
                                flatten_input, 
                                do_not_expand_single_job_tasks, output_extras):
    """
    Factory for functions which 
        yield tuples of inputs, outputs / extras                            

    ..Note::

        1. Each job requires input/output file names
        2. Input/output file names can be a string, an arbitrarily nested sequence
        3. Non-string types are ignored
        3. Either Input or output file name must contain at least one string

    """
    def iterator(runtime_data):
        for input_param, output_extra_param in zip(input_params, output_extras):
            if flatten_input:
                yield (get_strings_in_nested_sequence(input_param),) + output_extra_param
            else:
                yield (file_names_from_tasks_globs(input_param, tasks, globs, runtime_data_names, 
                                                    runtime_data,
                                                    do_not_expand_single_job_tasks),) + output_extra_param
    return iterator

def files_runtime_param_factory (input_params, runtime_data_names, 
                                 flatten_input):
    """
    Factory for functions which 
        yield tuples of inputs, outputs / extras                            
    """
    def iterator(runtime_data):
        params = file_names_from_tasks_globs(input_params, [], [], runtime_data_names, 
                                                    runtime_data,
                                                    False) # do_not_expand_single_job_tasks is irrelevant
        if non_str_sequence(params):
            for p in params:
                yield p
        else:
            yield params

    return iterator

def files_custom_generator_param_factory (generator):
    """
    Factory for @files taking custom generators
        wraps so that the generator swallows the extra runtime_data argument

    """
    def iterator(runtime_data):
        for params in generator():
                yield params
    return iterator

#_________________________________________________________________________________________

#   split_param_factory

#_________________________________________________________________________________________
def split_param_factory (tasks, globs, orig_input_params, runtime_data_names, output_globs, output_runtime_data_names, output_files_specification, *extras):
    """
    Factory for task_split
    """
    def iterator(runtime_data):
        # flattened  = False
        # do_not_expand_single_job_tasks = True
        orig_filenames = file_names_from_tasks_globs(orig_input_params, tasks, globs, runtime_data_names, 
                                                    runtime_data, True)

        output_files   = file_names_from_tasks_globs(output_files_specification, [], output_globs,
                                                    output_runtime_data_names, 
                                                    runtime_data)
        yield (orig_filenames, output_files) + extras


    return iterator

    
    
#
#_________________________________________________________________________________________

#   transform_param_factory

#_________________________________________________________________________________________
def transform_param_factory (tasks, globs, orig_input_params, runtime_data_names, 
                                flatten_input, regex, 
                                regex_substitute_extra_parameters, 
                                input_pattern, output_pattern, 
                                *extras):
    """
    Factory for task_transform
    """
    def iterator(runtime_data):

        # 
        # get list of input_params
        # 
        input_params = file_names_from_tasks_globs(orig_input_params, tasks, globs,
                                                    runtime_data_names, runtime_data)

        if flatten_input:
            input_params = get_strings_in_nested_sequence(input_params)
            
        for input_param in sorted(input_params):
          
            #
            #   turn input param into a string and match with regular expression
            #   
            filename = get_first_string_in_nested_sequence(input_param)
            if filename == None or not regex.search(filename):
                continue

            #   
            #   "inputs" defined  turn input string into i/o/extras with regex
            # 
            if input_pattern != None:
                if regex_substitute_extra_parameters:
                    yield tuple(construct_filename_parameters_with_regex(filename, regex, p) 
                                        for p in (input_pattern, output_pattern) + extras)
                else:
                    yield tuple(construct_filename_parameters_with_regex(filename, regex, p) 
                                        for p in (input_pattern, output_pattern)) + extras
            #   
            #   "inputs" not defined:
            #       keep real input param and turn input string into o/extras with regex
            # 
            else:
                if regex_substitute_extra_parameters:
                    yield (input_param,) + \
                            tuple(construct_filename_parameters_with_regex(filename, regex, p) 
                                        for p in (output_pattern,) + extras)
                else:
                    yield (input_param, 
                            construct_filename_parameters_with_regex(filename, regex, output_pattern)) + \
                            extras
                
    return iterator
                

#_________________________________________________________________________________________

#   merge_param_factory

#_________________________________________________________________________________________
def merge_param_factory (tasks, globs, orig_input_params, runtime_data_names,  
                                output_files, 
                                *extras):
    """
    Factory for task_merge
    """
    # 
    def iterator(runtime_data):
        # flattened  = False
        # do_not_expand_single_job_tasks = True
        orig_filenames = file_names_from_tasks_globs(orig_input_params, tasks, globs,
                                                    runtime_data_names, runtime_data, 
                                                    True)
        yield (orig_filenames, output_files) + extras
    return iterator

    
#_________________________________________________________________________________________

#   collate_param_factory

#_________________________________________________________________________________________
def collate_param_factory (tasks, globs, orig_input_params, runtime_data_names, 
                                flatten_input,
                                regex,
                                input_pattern,
                                *output_and_extras):
    """
    Factory for task_collate
    all [input] which lead to the same [output / extra] are combined together
    """
    # 
    def iterator(runtime_data):

        # 
        # one job per unique [output / extra] parameter
        #   
        #   can't use set or dict because parameters might not be hashable!!!
        #   use list and itertools group by
        # 
        params_per_job = []

        # flattened  = flatten_input
        # do_not_expand_single_job_tasks = False
        input_params = file_names_from_tasks_globs(orig_input_params, tasks, globs,
                                                    runtime_data_names, runtime_data)

        if flatten_input:
            input_params = get_strings_in_nested_sequence(input_params)

        for input_param in sorted(input_params):
            
            #
            #   turn input param into a string and match with regular expression
            #   
            filename = get_first_string_in_nested_sequence(input_param)
            if filename == None or not regex.search(filename):
                continue

            if input_pattern != None:
                actual_input_param = construct_filename_parameters_with_regex(filename, regex, input_pattern) 
            else:
                actual_input_param = input_param
                
            #   
            #   "inputs" defined  turn input string into i/o/extras with regex
            # 
            output_extra_param = tuple(construct_filename_parameters_with_regex(filename, regex, p) 
                                            for p in output_and_extras)
            # 
            #   nothing matched
            # 
            if len(output_extra_param) == 0:
                continue
                
            params_per_job.append((output_extra_param, actual_input_param))

        # combine inputs which lead to the same output/extras into one tuple
        for output_params, params_grouped_by_output in groupby(sorted(params_per_job), itemgetter(0)):
            yield (tuple(input_param for input_param, ignore in 
                            groupby(list(params_grouped_by_output), itemgetter(1))),) + output_params
                        
    return iterator


    
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Legacy code

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#_________________________________________________________________________________________


#   files_re_param_factory                                                                        

#      iterable list of input / output files from

#                1) glob/filelist
#                2) regex
#                3) input_filename_str (optional)
#                4) output_filename_str
#_________________________________________________________________________________________
def files_re_param_factory( tasks, globs, orig_input_params, runtime_data_names, combining_all_jobs, 
                            regex, input_pattern, *output_and_extras):
    """
    Factory for functions which in turn
        yield tuples of input_file_name, output_file_name                                     
                                                                                                   
    Usage:
                                         

        for i, o in param_func():                                                                          
            print " input file name = " , i                                                                
            print "output file name = " , o                                                                
                                                                                                       
                                                                                                       
    ..Note::
        1. `param_func` has to be called each time
        2. `glob` is called each time.
           So do not expect the file lists in `param_func()` to be the same for each invocation
        3. A "copy" of the file list is saved
           So do not expect to modify your copy of the original list and expect changes
           to the input/export files
        
    
    """
    if combining_all_jobs:
        return collate_param_factory (tasks, globs, orig_input_params, runtime_data_names, 
                                        False,
                                        regex,
                                        input_pattern,
                                        *output_and_extras)
    else:
        return transform_param_factory (tasks, globs, orig_input_params, runtime_data_names, 
                                        False, regex, 
                                        True,
                                        input_pattern, 
                                        *output_and_extras)










#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Unit Tests in test/test_file_name_parameters.py


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

