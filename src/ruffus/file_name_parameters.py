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
from ruffus_exceptions import *
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

#   check_input_files_exist

#_________________________________________________________________________________________
def check_input_files_exist (input_files, *other_parameters_ignored):
    """
    Clunky hack to make sure input files exists right before 
        job is called for better error messages
    Input files in first argument
    """
    for f in get_strings_in_nested_sequence(input_files):
        if not os.path.exists(f):
            raise MissingInputFileError("No way to run job: "+
                                        "Input file ['%s'] does not exist" % f)

#_________________________________________________________________________________________

#   needs_update_check_modify_time

#_________________________________________________________________________________________
def needs_update_check_modify_time (i, o, *other_parameters_ignored):
    """
    Given input and output files
        see if all exist and whether output files are later than input files
        Each can be 
            1) string: assumed to be a filename "file1"
            2) any other type 
            3) arbitrary nested sequence of (1) and (2)
        
    """
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
        return True, "Need update %s" % str(filename_to_times)
    return False, "Up to date"


    
    
    
 
    
    
    
    
    
    
    
    
    
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

class pass_thru:
    pass
def construct_filename_parameters_with_regex(filename, regex, p):
    """
    recursively replaces file name specifications using regular expressions
    Non-strings are left alone
    """
    if isinstance(p, pass_thru):
        return filename
    elif is_str(p):
        return regex.sub(p, filename) 
    elif non_str_sequence (p):
        return tuple(construct_filename_parameters_with_regex(filename, regex, pp) for pp in p)
    else:
        return p

#_________________________________________________________________________________________

#   glob_regex_io_param_factory                                                                        

#      iterable list of input / output files from

#                1) glob/filelist
#                2) regex
#                3) input_filename_str (optional)
#                4) output_filename_str
#_________________________________________________________________________________________
def glob_regex_io_param_factory (glob_str_or_list_or_tasks, matching_regex, *parameters):
    """
    Factory for functions which in turn
        yield tuples of input_file_name, output_file_name                                     
                                                                                                   
    Usage:
                                         
    1.::
    
        param_func = glob_regex_io_param_factory("/etc/*",          # glob                                  
                                                 "(file_)(\d+)",    # which match this regex                
                                                 "input_file_\2",   # pattern to generate input file names    
                                                 "output_file_\2")  # pattern to generate output file names  
                                                 
    or                                                                                                 
    2.::
    
        param_func = glob_regex_io_param_factory("/etc/*",         # glob                                  
                                                 "(file_)(\d+)",   # which match this regex                
                                                 None,             # use originals as input file names     
                                                 "output_file_\2") # pattern to generate output file names   

    or 
    3.::
    
        param_func = glob_regex_io_param_factory(file_list,        # list of files
                                                 "(file_)(\d+)",   # which match this regex                
                                                 None,             # use originals as input file names     
                                                 "output_file_\2") # pattern to generate output file names   
    
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
    parameters = list(parameters)
    if len(parameters) == 0:
        raise task_FilesreArgumentsError("Missing arguments for @files_re(%s)" % 
                                         ignore_unknown_encoder([glob_str_or_list_or_tasks, 
                                                                matching_regex] + 
                                                                parameters))
    
    #
    #   special marker combining object: mark either regex or input file parameter
    # 
    combining_all_jobs = False
    
    if isinstance(parameters[0], combine):
        combining_all_jobs = True
        if len(parameters[0].args) == 1:
            parameters[0] = parameters[0].args[0]
        else:
            parameters[0] = parameters[0].args
            
    if isinstance(matching_regex, combine):
        combining_all_jobs = True
        if len(matching_regex.args) == 1:
            matching_regex = matching_regex.args[0]
        else:
            matching_regex = matching_regex.args
        
        
    if len(get_strings_in_nested_sequence(parameters)) == 0:
        raise task_FilesreArgumentsError("Input or output file parameters should "
                                        "contain at least one or more file names or "
                                        "regular expression patterns to generate "
                                        "file names (string or nested collection of "
                                        "strings) "  +   
                                        ignore_unknown_encoder(parameters))

    
    
    regex = re.compile(matching_regex)

    #  make (expensive) copy so that changes to the original sequence don't confuse us
    parameters = copy.copy(parameters)

    
    # if the input file term is missing, just use the original
    if len(parameters) == 1:
        parameters.insert(0, pass_thru())
        

            
    #
    #   make copy of file list? 
    #
    if not is_str(glob_str_or_list_or_tasks) and not isinstance(glob_str_or_list_or_tasks, output_from):
        glob_str_or_list_or_tasks = copy.copy(glob_str_or_list_or_tasks)

    def iterator ():
        #
        #   glob or file list? 
        #
        if is_str(glob_str_or_list_or_tasks):
            #import time                                                                          # DEBUG GLOB TIME
            #start_time = time.time()                                                             # DEBUG GLOB TIME
            filenames = sorted(glob.glob(glob_str_or_list_or_tasks))                             
            #end_time = time.time()                                                               # DEBUG GLOB TIME
            #print >>sys.stderr, 'glob took %0.3f ms [%s]' % ((end_time-start_time)*1000.0,       # DEBUG GLOB TIME
            #                                                        glob_str_or_list_or_tasks)   # DEBUG GLOB TIME
        
        # 
        #   get output file names from specified tasks
        #       assumes that 2nd parameter contain output files
        #
        elif isinstance(glob_str_or_list_or_tasks, output_from):
            filenames = []
            for task in glob_str_or_list_or_tasks.args:
                
                
                # skip tasks which don't have parameters
                if task.param_generator_func == None:
                    continue

                for param in task.param_generator_func():
                    
                    # skip tasks which don't have output parameters
                    if len(param) < 2:
                        continue
                        
                    #   get 
                    #   
                    filenames.extend(get_strings_in_nested_sequence(param[1]))
                
                
        else:
            filenames = sorted(glob_str_or_list_or_tasks)
            
        if combining_all_jobs:
            #
            # This is intended as a many -> few combining operation 
            #   so all [input] which lead to the same [output / extra] are combined together
            # 
            # This function delivers one job per unique [output / extra] parameter
            input_params_per_output_extra_params = defaultdict(list)
            for filename in filenames:
                #   regular expression has to match 
                if not regex.search(filename):
                    continue
                    
                #   input parameters                    
                input_param = construct_filename_parameters_with_regex(filename, regex, parameters[0])

                output_param = tuple(construct_filename_parameters_with_regex(filename, regex, p) 
                                        for p in parameters[1:])
                input_params_per_output_extra_params[output_param].append(input_param)
                
            for output_param, input_params in input_params_per_output_extra_params.iteritems():
                yield (tuple(input_params),) + output_param
        else:
            
            for filename in filenames:
                #   regular expression has to match 
                if not regex.search(filename):
                    continue
    
                yield tuple(construct_filename_parameters_with_regex(filename, regex, p) 
                                        for p in parameters)
        

    return iterator
    
#_________________________________________________________________________________________

#   file_list_io_param_factory 

#       iterates through a list of input output files

#
#       orig_args = ["input", "output", 1, 2, ...] 
#       orig_args = [None,    "output", 1, 2, ...] 
#       orig_args = [
#                       ["input0",               "output0",                1, 2, ...]
#                       [["input1a", "input1b"], "output1",                1, 2, ...]
#                       ["input2",               ["output2a", "output2b"], 1, 2, ...]
#                       ["input3",               "output3",                1, 2, ...]
#                   ] 
#       
#       N.B. There is not much checking of parameters up front
#_________________________________________________________________________________________
def check_file_list_io_param (params):
    """
    Helper function for file_list_io_param_factory
    Checks there are input and output files specified for each job
    """
    if not len(params):
        return
    
        
    try:
        for job_param in params:
            if len(job_param) < 1:
                raise task_FilesArgumentsError("Missing input files for job " +   
                                                ignore_unknown_encoder(job_param))      
            if len(job_param) < 2:
                raise task_FilesArgumentsError("Missing output files for job " +   
                                                ignore_unknown_encoder(job_param))      
            if list(job_param[0:2]) == [None, None]:                                    
                raise task_FilesArgumentsError("Either the input or output file "       +   
                                                "must be defined for job "              +   
                                                ignore_unknown_encoder(job_param))      
            if len(get_strings_in_nested_sequence(job_param[0:2])) == 0:            
                raise task_FilesArgumentsError("Input or output file parameters should "
                                                "contain at least one or more file names "
                                                "(a string or nested collection of strings) "  +   
                                                ignore_unknown_encoder(job_param))
    except TypeError:
        message = ("Enclosing brackets are needed even if you are "
                   "only supplying parameters for a single job: "     +
                    ignore_unknown_encoder(job_param))
        raise task_FilesArgumentsError(message)
    
def file_list_io_param_factory (orig_args):
    """
    Factory for functions which 
        yield tuples of input_file_name, output_file_name                            
        
    Examples of orig_args:

    1.::
        
        orig_args = "input1", "output1", any_other_parameters1, ...       # files for job 1 
    
    2.::
        
        orig_args = None,     "output1", any_other_parameters2, ...       # files for job 1 
    
    3.::
    
        orig_args = [                                                               
                      ["input0",               "output0",                ...] # files for job 1
                      [["input1a", "input1b"], "output1",                ...] # files for job 2 
                      ["input2",               ["output2a", "output2b"], ...] # files for job 3 
                      ["input3",               "output3",                ...] # files for job 4 
                    ]                                                                 


    Usage:

        param_func = file_list_io_param_factory(orig_args)
        
        for params in param_func():                                                                          
            i,o = params[0:2]
            print " input file name(s) = " , i                                                                
            print "output file name(s) = " , o                                                                


    ..Note::
    
        1. Each job requires input/output file names
        2. Input/output file names can be a string, an arbitrarily nested sequence
        3. Non-string types are ignored
        3. Either Input or output file name must contain at least one string
        
    """
    # multiple jobs with input/output parameters etc.
    if len(orig_args) > 1:
        params = copy.copy([list(orig_args)])
    else:
        params = copy.copy(orig_args[0])

    check_file_list_io_param(params)
      

    def iterator():
        for job_param in params:
            yield job_param
    return iterator

    
    
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Testing


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

if __name__ == '__main__':
    import sys
    
    # use simplejson in place of json for python < 2.6
    try:                           
        import json                
    except ImportError:            
        import simplejson          
        json = simplejson          
                                   
                                   
    dumps = json.dumps             

    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    test_path = os.path.join(exe_path, "test", "file_name_parameters")









#=========================================================================================

#   file_list_io_param_factory
 
#=========================================================================================
    import unittest, time
    class Test_file_list_io_param_factory(unittest.TestCase):
    
        #       self.assertEqual(self.seq, range(10))
        #       self.assert_(element in self.seq)
        #       self.assertRaises(ValueError, random.sample, self.seq, 20)
    
        def forwarded_function (self, *params):
            """
            This extra function is to simulate the forwarding from the decorator to
                the task creation function
            """
            it = file_list_io_param_factory(params)
            return list(it())
    
        def test_single_job_per_task(self):
            """
            test convenience form for single job per task
            """
            self.assertEqual(self.forwarded_function("file.input", "file.output", "other", 1),
                                [['file.input', 'file.output', 'other', 1]])
    
        def test_multiple_jobs_per_task(self):
            """
            test normal form for multiple job per task
            """
            params = [
                        ["file0input", "file0.output", "other", 1],
                        ["file1input", "file1.output", "other", 1],
                        ["file2input", "file2.output", "other", 1],
                     ]
            self.assertEqual(self.forwarded_function(params),
                                params)
    
        def test_nested_multiple_jobs_per_task(self):
            """
            test normal form for multiple job per task
            """
            params = [
                        [[["file0input"]], "file0.output", "other", 1],
                        ["file1input", "file1.output", "other", 1],
                        ["file2input", "file2.output", "other", 1],
                     ]
            self.assertEqual(self.forwarded_function(params),
                                params)
    
        def test_errors_raise_exceptions(self):
            """
            test if errors raise exceptions properly
            """
            params = [
                        [1, 2, 3],
                        [1, 2, 3],
                        [1, 2, 3],
                     ]
            self.assertRaises(task_FilesArgumentsError, self.forwarded_function, params)
            #Enclosing brackets are needed even if you are only supplying parameters for a single job: 1
            self.assertRaises(task_FilesArgumentsError, self.forwarded_function, [1,])
            #Missing input files for job []
            self.assertRaises(task_FilesArgumentsError, self.forwarded_function, [[],])
            #Missing output files for job [1]
            self.assertRaises(task_FilesArgumentsError, self.forwarded_function, [[1],])
            #Either the input or output file must be defined for job [None, None]
            self.assertRaises(task_FilesArgumentsError, self.forwarded_function, [None, None])
            #Input or output file parameters should contain at least one or more file names (a string or nested collection of strings) [1, 2]
            self.assertRaises(task_FilesArgumentsError, self.forwarded_function, [1, 2])
    
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
                
#=========================================================================================

#   glob_regex_io_param_factory

#=========================================================================================
    
    def recursive_replace(p, from_s, to_s):
        """
        recursively replaces file name specifications using regular expressions
        Non-strings are left alone
        """
        if is_str(p):
            return p.replace(from_s, to_s)
        elif non_str_sequence (p):
            return [recursive_replace(pp, from_s, to_s) for pp in p]
        else:
            return p

    def list_generator_factory (list):
        def list_generator ():
            for i in list:
                yield i
        return list_generator
        
    class Test_glob_regex_io_param_factory(unittest.TestCase):
        def setUp(self):
            if not os.path.exists(test_path):
                os.makedirs(test_path)
            open("%s/f%d.output" % (test_path, 0), "w")
            for i in range(3):
                open("%s/f%d.test" % (test_path, i), "w")
            time.sleep(1)
            open("%s/f%d.output" % (test_path, 1), "w")
            open("%s/f%d.output" % (test_path, 2), "w")
    
        def tearDown(self):
            for i in range(3):
                os.unlink("%s/f%d.test" % (test_path, i))
            for i in range(3):
                os.unlink("%s/f%d.output" % (test_path, i))
            os.removedirs(test_path)
            pass
    
        #       self.assertEqual(self.seq, range(10))
        #       self.assert_(element in self.seq)
        #       self.assertRaises(ValueError, random.sample, self.seq, 20)

        def forwarded_function (self, glob_or_str, regex, *params):
            """
            This extra function is to simulate the forwarding from the decorator to
                the task creation function
            """
            it = glob_regex_io_param_factory(glob_or_str, regex, *params)
            return list(it())
            
        def check_input_files_exist(self, glob_or_str, regex, *params):
            """
            This extra function is to simulate the forwarding from the decorator to
                the task creation function
            """
            it = glob_regex_io_param_factory(glob_or_str, regex, *params)
            for param in it():
                check_input_files_exist (*param)
            return True
            
        def needs_update_check_modify_time(self, glob_or_str, regex, *params):
            """
            This extra function is to simulate the forwarding from the decorator to
                the task creation function
            """
            it = glob_regex_io_param_factory(glob_or_str, regex, *params)
            return [needs_update_check_modify_time (*p) for p in it()]


        def test_combine(self):
            """
            test combining operator
            """
            paths = self.forwarded_function(test_path + "/*", "(.*).test$", combine(r"\1.input"), r"\1.output")
            self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                                [[['DIR/f2.input'], 'DIR/f2.output'], 
                                 [['DIR/f0.input'], 'DIR/f0.output'], 
                                 [['DIR/f1.input'], 'DIR/f1.output']])
            paths = self.forwarded_function(test_path + "/*", "(.*).test$", combine(r"\1.input"), r"combined.output")
            self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                                [[['DIR/f0.input', 
                                   'DIR/f1.input', 
                                   'DIR/f2.input'], 'combined.output']])
            
            
        def test_glob(self):
            """
            test globbed form
            """
            # 
            # simple 1 input, 1 output
            # 
            paths = self.forwarded_function(test_path + "/*", "(.*).test$", r"\1.input", r"\1.output")
            self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                            [['DIR/f0.input', 'DIR/f0.output'], 
                             ['DIR/f1.input', 'DIR/f1.output'], 
                             ['DIR/f2.input', 'DIR/f2.output']])
            self.assert_(self.check_input_files_exist(test_path + "/*", "(.*).test$", 
                                                            r"\1.test", r"\1.output"))
                            

            # 
            # nested forms
            # 
            paths = self.forwarded_function(test_path + "/*", "(.*).test$", [r"\1.input",2,["something", r"\1"]], r"\1.output", r"\1.extra", 5)
            self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                            [[['DIR/f0.input', 2, ['something', 'DIR/f0']], 'DIR/f0.output', 'DIR/f0.extra', 5], 
                             [['DIR/f1.input', 2, ['something', 'DIR/f1']], 'DIR/f1.output', 'DIR/f1.extra', 5], 
                             [['DIR/f2.input', 2, ['something', 'DIR/f2']], 'DIR/f2.output', 'DIR/f2.extra', 5]])

            #
            # only output
            # 
            paths = self.forwarded_function(test_path + "/*", ".*/(.*).test$", r"\1.output")
            self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                                [['DIR/f0.test', 'f0.output'], 
                                 ['DIR/f1.test', 'f1.output'], 
                                 ['DIR/f2.test', 'f2.output']])

        def test_globbed_up_to_date(self):
            """
            test glob form
            """
            #
            # check simple is up to date
            # 
            self.assertEqual(self.needs_update_check_modify_time(test_path + "/*", 
                                "(.*).test$", r"\1.output"), [True, False, False])
            #
            # check complex is up to date
            # 
            self.assertEqual(self.needs_update_check_modify_time(test_path + "/*", 
                                "(.*).test$", [1,2,[[r"\1.output", 
                                                     r"\1.output"]]]), [True, False, False])
            
        def test_filelist(self):
            """
            test file list form
            """
            file_list = ["DIR/f0.test", "DIR/f1.test", "DIR/f2.test"]
            # 
            # simple 1 input, 1 output
            # 
            paths = self.forwarded_function(file_list, "(.*).test$", r"\1.input", r"\1.output")
            self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                            [['DIR/f0.input', 'DIR/f0.output'], 
                             ['DIR/f1.input', 'DIR/f1.output'], 
                             ['DIR/f2.input', 'DIR/f2.output']])

            # 
            # nested forms
            # 
            paths = self.forwarded_function(file_list, "(.*).test$", [r"\1.input",2,["something", r"\1"]], r"\1.output", r"\1.extra", 5)
            self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                            [[['DIR/f0.input', 2, ['something', 'DIR/f0']], 'DIR/f0.output', 'DIR/f0.extra', 5], 
                             [['DIR/f1.input', 2, ['something', 'DIR/f1']], 'DIR/f1.output', 'DIR/f1.extra', 5], 
                             [['DIR/f2.input', 2, ['something', 'DIR/f2']], 'DIR/f2.output', 'DIR/f2.extra', 5]])

            #
            # only output
            # 
            paths = self.forwarded_function(file_list, ".*/(.*).test$", r"\1.output")
            self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                                [['DIR/f0.test', 'f0.output'], 
                                 ['DIR/f1.test', 'f1.output'], 
                                 ['DIR/f2.test', 'f2.output']])
            

        def test_errors_raise_exceptions(self):
            """
            test if errors raise exceptions properly
            """
            # 
            # missing i/o parameters
            # 
            self.assertRaises(task_FilesreArgumentsError, self.forwarded_function, test_path + "/*", ".*/(.*).test$")
            
            # 
            # missing input file
            # 
            self.assertRaises(MissingInputFileError, self.check_input_files_exist,
                                test_path + "/*", "(.*).test$", r"\1.input", r"\1.output")

            #
            # No files in i/o parameters, only, for example, numbers
            # 
            self.assertRaises(task_FilesreArgumentsError, self.forwarded_function, 
                                test_path + "/*", ".*/(.*).test$", 1, 2)


        def test_tasks(self):
            """
            test if can use tasks to specify dependencies
            """
            l1 = [["input1", "output1"], [3, "output2"], [], [4, 5]]
            l2 = [["input3", "output3"], [3, ["output4", "output5"]], [], [4, 5]]
            l3 = []
            l4 = [[1, 2]]
            import task
            t1 = task._task("module", "func1"); t1.param_generator_func = list_generator_factory(l1)
            t2 = task._task("module", "func2"); t2.param_generator_func = list_generator_factory(l2)
            t3 = task._task("module", "func3"); t3.param_generator_func = list_generator_factory(l3)
            t4 = task._task("module", "func4"); t4.param_generator_func = list_generator_factory(l4)
            t5 = task._task("module", "func5"); t5.param_generator_func = None
            self.assertEqual(self.forwarded_function(output_from(t1, t2, t3, t4, t5), r"(.*)", r"\1.yes"),
                            [('output1', 'output1.yes'), 
                             ('output2', 'output2.yes'), 
                             ('output3', 'output3.yes'), 
                             ('output4', 'output4.yes'), 
                             ('output5', 'output5.yes')])



if __name__ == '__main__':
    #
    #   debug parameter ignored if called as a module
    #     
    if sys.argv.count("--debug"):
        sys.argv.remove("--debug")
    unittest.main()



    
