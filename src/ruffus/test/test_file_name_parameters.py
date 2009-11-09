#!/usr/bin/env python
################################################################################
#
#   test_file_name_parameters
#
#
#   Copyright (c) 11/9/2009 Leo Goodstadt
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

    test_file_name_parameters.py

"""


import sys, os
# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Unit Tests


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import sys
from ruffus import *
from ruffus.file_name_parameters import *

# use simplejson in place of json for python < 2.6
try:                           
    import json                
except ImportError:            
    import simplejson          
    json = simplejson          
                               
                               
dumps = json.dumps             

exe_path = os.path.join(os.path.split(os.path.abspath(sys.argv[0]))[0], "..")
test_path = os.path.join(exe_path, "test", "file_name_parameters")









#=========================================================================================

#   args_param_factory

#=========================================================================================
import unittest, time
from random import randint
class Test_args_param_factory(unittest.TestCase):

    #       self.assertEqual(self.seq, range(10))
    #       self.assert_(element in self.seq)
    #       self.assertRaises(ValueError, random.sample, self.seq, 20)

    def forwarded_function (self, params):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        it = args_param_factory(params)
        return list(it())

    def test_single_job_per_task(self):
        """
        test convenience form for single job per task
        """
        self.assertEqual(self.forwarded_function([["file.input", "file.output", "other", 1]]),
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

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
#=========================================================================================

#   files_re_param_factory

#=========================================================================================

def recursive_replace(p, from_s, to_s):
    """
    recursively replaces file name specifications using regular expressions
    Non-strings are left alone
    """
    if isinstance(p, str):
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
    
l1 = [["input1", "output1.test"], [3, "output2.test"], ["input3", "output3.test"], [3, ["output4.test", "output.ignored"]], [], [4, 5]]
l2 = [["output4.test", "output.ignored"]]
l3 = []
l4 = [[1, (2,"output5.test")]]
t1 = task._task("module", "func1"); t1.param_generator_func = list_generator_factory(l1)
t2 = task._task("module", "func2"); t2.param_generator_func = list_generator_factory(l2)
t2.single_job_single_output = True
t3 = task._task("module", "func3"); t3.param_generator_func = list_generator_factory(l3)
t4 = task._task("module", "func4"); t4.param_generator_func = list_generator_factory(l4)
t4.single_job_single_output = True
t5 = task._task("module", "func5"); t5.param_generator_func = None

class Test_files_re_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        open("%s/f%d.output" % (test_path, 0), "w")
        for i in range(3):
            open("%s/f%d.test" % (test_path, i), "w")
        time.sleep(1)
        open("%s/f%d.output" % (test_path, 1), "w")
        open("%s/f%d.output" % (test_path, 2), "w")
        
        self.tasks = [t1, t2, t3, t4, t5]
        

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

    #def get_param_iterator (self, *old_args):
    def get_param_iterator (self, *orig_args):
        # 
        # replace function / function names with tasks
        # 
        # fake virgin task
        fake_task = task._task("module", "func_fake%d" % randint(1, 1000000))
        fake_task.task_files_re(orig_args)
        return fake_task.param_generator_func

    def files_re (self, *old_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        return list(self.get_param_iterator (*old_args)())
        
    def check_input_files_exist(self, *old_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        it = self.get_param_iterator (*old_args)
        for param in it():
            check_input_files_exist (*param)
        return True
        
    def needs_update_check_modify_time(self, *old_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        it = self.get_param_iterator (*old_args)
        return [needs_update_check_modify_time (*p) for p in it()]


    def test_combine(self):
        """
        test combining operator
        """
        paths = self.files_re(test_path + "/*", r"(.*).test$", combine(r"\1.input"), r"\1.output")
        self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                            [
                             [['DIR/f0.input'], 'DIR/f0.output'], 
                             [['DIR/f1.input'], 'DIR/f1.output'],
                             [['DIR/f2.input'], 'DIR/f2.output'], 
                             ]
            )
        paths = self.files_re(test_path + "/*", "(.*).test$", combine(r"\1.input"), r"combined.output")
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
        paths = self.files_re(test_path + "/*", "(.*).test$", r"\1.input", r"\1.output")
        self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                        [['DIR/f0.input', 'DIR/f0.output'], 
                         ['DIR/f1.input', 'DIR/f1.output'], 
                         ['DIR/f2.input', 'DIR/f2.output']])
        self.assert_(self.check_input_files_exist(test_path + "/*", "(.*).test$", 
                                                        r"\1.test", r"\1.output"))
                        

        # 
        # nested forms
        # 
        paths = self.files_re(test_path + "/*", "(.*).test$", [r"\1.input",2,["something", r"\1"]], r"\1.output", r"\1.extra", 5)
        self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                        [[['DIR/f0.input', 2, ['something', 'DIR/f0']], 'DIR/f0.output', 'DIR/f0.extra', 5], 
                         [['DIR/f1.input', 2, ['something', 'DIR/f1']], 'DIR/f1.output', 'DIR/f1.extra', 5], 
                         [['DIR/f2.input', 2, ['something', 'DIR/f2']], 'DIR/f2.output', 'DIR/f2.extra', 5]])

        #
        # only output
        # 
        paths = self.files_re(test_path + "/*", ".*/(.*).test$", r"\1.output")
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
        self.assertEqual([res[0] for res in self.needs_update_check_modify_time(test_path + "/*", 
                            "(.*).test$", r"\1.output")], [True, False, False])
        #
        # check complex is up to date
        # 
        self.assertEqual([res[0] for res in self.needs_update_check_modify_time(test_path + "/*", 
                            "(.*).test$", [1,2,[[r"\1.output", 
                                                 r"\1.output"]]])], [True, False, False])
        
    def test_filelist(self):
        """
        test file list form
        """
        file_list = ["DIR/f0.test", "DIR/f1.test", "DIR/f2.test"]
        # 
        # simple 1 input, 1 output
        # 
        paths = self.files_re(file_list, r"(.*).test$", r"\1.input", r"\1.output")
        self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                        [['DIR/f0.input', 'DIR/f0.output'], 
                         ['DIR/f1.input', 'DIR/f1.output'], 
                         ['DIR/f2.input', 'DIR/f2.output']])

        # 
        # nested forms
        # 
        paths = self.files_re(file_list, "(.*).test$", [r"\1.input",2,["something", r"\1"]], r"\1.output", r"\1.extra", 5)
        self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                        [[['DIR/f0.input', 2, ['something', 'DIR/f0']], 'DIR/f0.output', 'DIR/f0.extra', 5], 
                         [['DIR/f1.input', 2, ['something', 'DIR/f1']], 'DIR/f1.output', 'DIR/f1.extra', 5], 
                         [['DIR/f2.input', 2, ['something', 'DIR/f2']], 'DIR/f2.output', 'DIR/f2.extra', 5]])

        #
        # only output
        # 
        paths = self.files_re(file_list, ".*/(.*).test$", r"\1.output")
        self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                            [['DIR/f0.test', 'f0.output'], 
                             ['DIR/f1.test', 'f1.output'], 
                             ['DIR/f2.test', 'f2.output']])


    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """

        paths = self.files_re(task.output_from("module.func1", 
                                               "module.func2", 
                                               "module.func3", 
                                               "module.func4", 
                                               "module.func5"), r"(.test)", r"\1.yes")
        self.assertEqual(paths,
                        [
                         (['output4.test', 'output.ignored'], 'output4.test.yes'), 
                         ('output1.test', 'output1.test.yes'), 
                         ('output2.test', 'output2.test.yes'), 
                         ('output3.test', 'output3.test.yes'), 
                         ((2, 'output5.test'), 'output5.test.yes')])


        paths = self.files_re(task.output_from("module.func2"), r"(.ignored)", r"\1.yes")
        self.assertEqual(paths,
                        [('output.ignored', 'output.ignored.yes')])
        paths = self.files_re([task.output_from("module.func2")], r"(.ignored)", r"\1.yes")
        self.assertEqual(paths,
                    [('output.ignored', 'output.ignored.yes')])
        
        
        
        
        
        
        
        
        
        
        
        
        
#=========================================================================================

#   split_param_factory

#=========================================================================================

class Test_split_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        open("%s/f%d.output" % (test_path, 0), "w")
        for i in range(3):
            open("%s/f%d.test" % (test_path, i), "w")
        time.sleep(1)
        open("%s/f%d.output" % (test_path, 1), "w")
        open("%s/f%d.output" % (test_path, 2), "w")

        self.tasks = [t1, t2, t3, t4, t5]


    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (test_path, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (test_path, i))
        os.removedirs(test_path)
        pass




    #_____________________________________________________________________________

    #   wrappers

    #_____________________________________________________________________________
    def get_param_iterator (self, *orig_args):
        # 
        # replace function / function names with tasks
        # 
        # fake virgin task
        fake_task = task._task("module", "func_fake%d" % randint(1, 1000000))
        fake_task.task_split(orig_args)
        return fake_task.param_generator_func


    def do_task_split (self, *old_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        # extra dereference because we are only interested in the first (only) job
        return list(self.get_param_iterator (*old_args)())[0]


    def test_glob(self):
        """
        test globbed form
        """
        # 
        # simple 1 input, 1 output
        # 
        paths = self.do_task_split(test_path + "/*", [exe_path + "/a*.py", exe_path + "/r*.py"])
        self.assertEqual(recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR"),
                        [   ['DIR/f0.output', 
                             'DIR/f0.test', 
                             'DIR/f1.output', 
                             'DIR/f1.test', 
                             'DIR/f2.output', 
                             'DIR/f2.test',
                             ],
                            ['DIR/adjacent_pairs_iterate.py',
                             'DIR/ruffus_exceptions.py',
                             'DIR/ruffus_utility.py',
                             'DIR/ruffus_version.py'
                             ]              ])
    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """

        paths = self.do_task_split([task.output_from("module.func1",       # input params
                                                  "module.func2", 
                                                  "module.func3", 
                                                  "module.func4", 
                                                  "module.func5"),
                                 test_path + "/*"],                     
                                [exe_path + "/a*.py",                   # output params
                                 exe_path + "/r*.py",
                                 "extra.file"],
                                6)                                      # extra params
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR")
        self.assertEqual(paths,
                        [[  
                         'output1.test', 
                         'output2.test', 
                         'output3.test', 
                         ['output4.test', 'output.ignored'], 
                         5,  
                         'output.ignored',
                         [2, 'output5.test'], 
                         'DIR/f0.output', 
                         'DIR/f0.test', 
                         'DIR/f1.output', 
                         'DIR/f1.test', 
                         'DIR/f2.output', 
                         'DIR/f2.test'], 
                        ['DIR/adjacent_pairs_iterate.py', 
                         'DIR/ruffus_exceptions.py', 
                         'DIR/ruffus_utility.py', 
                         'DIR/ruffus_version.py', 
                         'extra.file'], 
                        6])

        # single job output consisting of a single file
        paths = self.do_task_split(task.output_from("module.func2"), exe_path + "/a*.py")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, ['output.ignored', ['DIR_E/adjacent_pairs_iterate.py']])

        paths = self.do_task_split([task.output_from("module.func2")], exe_path + "/a*.py")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [['output.ignored'], ['DIR_E/adjacent_pairs_iterate.py']])

        # single job output consisting of a list
        paths = self.do_task_split(task.output_from("module.func4"), exe_path + "/a*.py")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [[2, 'output5.test'], ['DIR_E/adjacent_pairs_iterate.py']] )

        paths = self.do_task_split([task.output_from("module.func4")], exe_path + "/a*.py")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [[[2, 'output5.test']], ['DIR_E/adjacent_pairs_iterate.py']])

#=========================================================================================

#   merge_param_factory

#=========================================================================================

class Test_merge_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        open("%s/f%d.output" % (test_path, 0), "w")
        for i in range(3):
            open("%s/f%d.test" % (test_path, i), "w")
        time.sleep(1)
        open("%s/f%d.output" % (test_path, 1), "w")
        open("%s/f%d.output" % (test_path, 2), "w")

        self.tasks = [t1, t2, t3, t4, t5]


    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (test_path, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (test_path, i))
        os.removedirs(test_path)
        pass




    #_____________________________________________________________________________

    #   wrappers

    #_____________________________________________________________________________
    def get_param_iterator (self, *orig_args):
        # 
        # replace function / function names with tasks
        # 
        # fake virgin task
        fake_task = task._task("module", "func_fake%d" % randint(1, 1000000))
        fake_task.task_merge(orig_args)
        return fake_task.param_generator_func

    def do_task_merge (self, *old_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        # extra dereference because we are only interested in the first (only) job
        return list(self.get_param_iterator (*old_args)())[0]


    def test_glob(self):
        """
        test globbed form
        """
        # 
        # simple 1 input, 1 output
        # 
        paths = self.do_task_merge(test_path + "/*", 
                                ["test1",                               # output params
                                 "test2",
                                 "extra.file"])
        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [   ['DIR/f0.output', 
                             'DIR/f0.test', 
                             'DIR/f1.output', 
                             'DIR/f1.test', 
                             'DIR/f2.output', 
                             'DIR/f2.test',
                             ],
                            ["test1",
                             "test2",
                             "extra.file"]
                                           ])
    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """

        paths = self.do_task_merge([task.output_from("module.func1",       # input params
                                                  "module.func2", 
                                                  "module.func3", 
                                                  "module.func4", 
                                                  "module.func5"),
                                 test_path + "/*"],                     
                                ["test1",                               # output params
                                 "test2",
                                 "extra.file"],
                                6)                                      # extra params
        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [[  
                         'output1.test', 
                         'output2.test', 
                         'output3.test', 
                         ['output4.test', 'output.ignored'], 
                         5,  
                         'output.ignored',
                         [2, 'output5.test'], 
                         'DIR/f0.output', 
                         'DIR/f0.test', 
                         'DIR/f1.output', 
                         'DIR/f1.test', 
                         'DIR/f2.output', 
                         'DIR/f2.test'], 
                         ["test1",                               # output params
                          "test2",
                          "extra.file"],
                        6])
        paths = self.do_task_merge(task.output_from("module.func2"), "output", "extra")
        paths = self.do_task_merge(task.output_from("module.func1", "module.func2"), "output", "extra")

        # single job output consisting of a single file
        paths = self.do_task_merge(task.output_from("module.func2"), "output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, ['output.ignored', "output"])

        paths = self.do_task_merge([task.output_from("module.func2")], "output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [['output.ignored'], "output"])

        # single job output consisting of a list
        paths = self.do_task_merge(task.output_from("module.func4"), "output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [[2, 'output5.test'], "output"] )

        paths = self.do_task_merge([task.output_from("module.func4")], "output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [[[2, 'output5.test']], "output"])
        
#=========================================================================================

#   transform_param_factory

#=========================================================================================

class Test_transform_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        open("%s/f%d.output" % (test_path, 0), "w")
        for i in range(3):
            open("%s/f%d.test" % (test_path, i), "w")
        time.sleep(1)
        open("%s/f%d.output" % (test_path, 1), "w")
        open("%s/f%d.output" % (test_path, 2), "w")

        self.tasks = [t1, t2, t3, t4, t5]


    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (test_path, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (test_path, i))
        os.removedirs(test_path)
        pass




    #_____________________________________________________________________________

    #   wrappers

    #_____________________________________________________________________________
    def get_param_iterator (self, *orig_args):
        # 
        # replace function / function names with tasks
        # 
        # fake virgin task
        fake_task = task._task("module", "func_fake%d" % randint(1, 1000000))
        fake_task.task_transform(orig_args)
        return fake_task.param_generator_func


    def do_task_transform (self, *old_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        # extra dereference because we are only interested in the first (only) job
        return list(self.get_param_iterator (*old_args)())


    def test_suffix(self):
        """
        test suffix transform with globs
        """
        # 
        # simple 1 input, 1 output
        # 
        paths = self.do_task_transform(test_path + "/*.test", task.suffix(".test"),  
                                            [".output1", ".output2"], ".output3")
            
        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            ['DIR/f0.test', ['DIR/f0.output1', 'DIR/f0.output2'], ".output3"], 
                            ['DIR/f1.test', ['DIR/f1.output1', 'DIR/f1.output2'], ".output3"],
                            ['DIR/f2.test', ['DIR/f2.output1', 'DIR/f2.output2'], ".output3"],
                                           ])
    def test_regex(self):
        """
        test regex transform with globs
        """
        # 
        # simple 1 input, 1 output
        # 
        paths = self.do_task_transform(test_path + "/*.test", task.regex(r"(.*)\.test"),  
                                            [r"\1.output1", r"\1.output2"], r"\1.output3")

        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            ['DIR/f0.test', ['DIR/f0.output1', 'DIR/f0.output2'], 'DIR/f0.output3'], 
                            ['DIR/f1.test', ['DIR/f1.output1', 'DIR/f1.output2'], 'DIR/f1.output3'],
                            ['DIR/f2.test', ['DIR/f2.output1', 'DIR/f2.output2'], 'DIR/f2.output3'],
                                           ])
    def test_inputs(self):
        """
        test transform with inputs in both regex and suffix forms
        """
        # 
        # simple 1 input, 1 output
        # 
        paths = self.do_task_transform(test_path + "/*.test", task.regex(r"(.*)\.test"),  
                                            task.inputs(r"\1.testwhat"),
                                            [r"\1.output1", r"\1.output2"])

        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            ['DIR/f0.testwhat', ['DIR/f0.output1', 'DIR/f0.output2']], 
                            ['DIR/f1.testwhat', ['DIR/f1.output1', 'DIR/f1.output2']],
                            ['DIR/f2.testwhat', ['DIR/f2.output1', 'DIR/f2.output2']],
                                           ])
        paths = self.do_task_transform(test_path + "/*.test", task.suffix(".test"),  
                                            task.inputs(r".testwhat"),
                                            [".output1", ".output2"], ".output3")

        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            ['DIR/f0.testwhat', ['DIR/f0.output1', 'DIR/f0.output2'], '.output3'], 
                            ['DIR/f1.testwhat', ['DIR/f1.output1', 'DIR/f1.output2'], '.output3'], 
                            ['DIR/f2.testwhat', ['DIR/f2.output1', 'DIR/f2.output2'], '.output3']])

    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """
    
        paths = self.do_task_transform([task.output_from( "module.func1",       # input params
                                                          "module.func2", 
                                                          "module.func3", 
                                                          "module.func4", 
                                                          "module.func5"),
                                        test_path + "/*.test"], 
                                        task.regex(r"(.*)\.test"),  
                                        [r"\1.output1", r"\1.output2"], r"\1.output3")
        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                                [
                                        [['output4.test', 'output.ignored'], ['output4.output1', 'output4.output2'], 'output4.output3'], 
                                        ['DIR/f0.test', ['DIR/f0.output1', 'DIR/f0.output2'], 'DIR/f0.output3'], 
                                        ['DIR/f1.test', ['DIR/f1.output1', 'DIR/f1.output2'], 'DIR/f1.output3'], 
                                        ['DIR/f2.test', ['DIR/f2.output1', 'DIR/f2.output2'], 'DIR/f2.output3'],
                                        ['output1.test', ['output1.output1', 'output1.output2'], 'output1.output3'], 
                                        ['output2.test', ['output2.output1', 'output2.output2'], 'output2.output3'], 
                                        ['output3.test', ['output3.output1', 'output3.output2'], 'output3.output3'], 
                                        [[2, 'output5.test'], ['output5.output1', 'output5.output2'], 'output5.output3'], 
                                ])
    
        # single job output consisting of a single file
        paths = self.do_task_transform(task.output_from("module.func2"), task.regex(r"(.*)\..*"),  r"\1.output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [['output.ignored', 'output.output']])
        

        # Same output if task specified as part of a list of tasks
        paths = self.do_task_transform([task.output_from("module.func2")], task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [['output.ignored', 'output']])

        # single job output consisting of a list
        paths = self.do_task_transform(task.output_from("module.func4"), task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [[[2, 'output5.test'], 'output']]  )

        # Same output if task specified as part of a list of tasks
        paths = self.do_task_transform([task.output_from("module.func4")], task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [[[2, 'output5.test'], 'output']]  )
    
    
#=========================================================================================

#   collate_param_factory

#=========================================================================================

class Test_collate_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        open("%s/f%d.output" % (test_path, 0), "w")
        open("%s/e%d.output" % (test_path, 0), "w")
        for i in range(3):
            open("%s/f%d.test" % (test_path, i), "w")
        for i in range(3):
            open("%s/e%d.test" % (test_path, i), "w")
        time.sleep(1)
        open("%s/f%d.output" % (test_path, 1), "w")
        open("%s/f%d.output" % (test_path, 2), "w")
        open("%s/e%d.output" % (test_path, 1), "w")
        open("%s/e%d.output" % (test_path, 2), "w")

        self.tasks = [t1, t2, t3, t4, t5]


    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (test_path, i))
            os.unlink("%s/e%d.test" % (test_path, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (test_path, i))
            os.unlink("%s/e%d.output" % (test_path, i))
        os.removedirs(test_path)
        pass




    #_____________________________________________________________________________

    #   wrappers

    #_____________________________________________________________________________
    def get_param_iterator (self, *orig_args):
        # 
        # replace function / function names with tasks
        # 
        # fake virgin task
        fake_task = task._task("module", "func_fake%d" % randint(1, 1000000))
        fake_task.task_collate(orig_args)
        return fake_task.param_generator_func


    def do_task_collate (self, *old_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        # extra dereference because we are only interested in the first (only) job
        return list(self.get_param_iterator (*old_args)())


    def test_regex(self):
        """
        test regex collate with globs
        """
        paths = self.do_task_collate(test_path + "/*", task.regex(r"(.*).test$"), r"\1.output")
        self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                            [
                                [['DIR/e0.test'], 'DIR/e0.output'], 
                                [['DIR/e1.test'], 'DIR/e1.output'],
                                [['DIR/e2.test'], 'DIR/e2.output'], 
                                [['DIR/f0.test'], 'DIR/f0.output'], 
                                [['DIR/f1.test'], 'DIR/f1.output'],
                                [['DIR/f2.test'], 'DIR/f2.output'], 
                             ]
            )
        paths = self.do_task_collate(test_path + "/*", task.regex("(.*).test$"), task.inputs(r"\1.input2"), r"combined.output")
        self.assertEqual(recursive_replace(paths, test_path, "DIR"),
                            [[[
                               'DIR/e0.input2', 
                               'DIR/e1.input2', 
                               'DIR/e2.input2',
                               'DIR/f0.input2', 
                               'DIR/f1.input2', 
                               'DIR/f2.input2',
                               ], 'combined.output']])

        # 
        # simple 1 input, 1 output
        # 
        paths = self.do_task_collate(test_path + "/*.test", task.regex(r"(.*/[ef]).*\.test"),  
                                            [r"\1.output1", r"\1.output2"], r"\1.extra")

        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            [
                                ['DIR/e0.test', 'DIR/e1.test', 'DIR/e2.test'],      # input
                                ['DIR/e.output1', 'DIR/e.output2'],                 # output
                                'DIR/e.extra'                                       # extra
                            ],
                            [
                                ['DIR/f0.test', 'DIR/f1.test', 'DIR/f2.test'],      # input 
                                ['DIR/f.output1', 'DIR/f.output2'],                 # output
                                'DIR/f.extra'                                       # extra 
                            ]
                        ] )
    def test_inputs(self):
        """
        test collate with task.inputs
        """
        # 
        # collating using inputs
        # 
        paths = self.do_task_collate(test_path + "/*.test", task.regex(r"(.*/[ef])(.).*\.test"),  
                                            task.inputs(r"\1\2.whoopee"),  [r"\1.output1", r"\1.output2"], r"\1.extra")

        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            [
                                ['DIR/e0.whoopee', 'DIR/e1.whoopee', 'DIR/e2.whoopee'],      # input
                                ['DIR/e.output1', 'DIR/e.output2'],                          # output
                                'DIR/e.extra'                                                # extra
                            ],
                            [
                                ['DIR/f0.whoopee', 'DIR/f1.whoopee', 'DIR/f2.whoopee'],      # input 
                                ['DIR/f.output1', 'DIR/f.output2'],                          # output
                                'DIR/f.extra'                                                # extra 
                            ]
                        ] )
        # 
        # collating using inputs where some files do not match regex
        # 
        paths = self.do_task_collate(test_path + "/*.test", task.regex(r"(.*/f)[a-z0-9]+\.test"),  
                                            task.inputs(r"\1.whoopee"),  [r"\1.output1", r"\1.output2"], r"\1.extra")

        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            [
                                ['DIR/f.whoopee'],                                  # input 
                                ['DIR/f.output1', 'DIR/f.output2'],                 # output
                                'DIR/f.extra'                                       # extra 
                            ]
                        ] )


        # 
        # collating using inputs where multiple copies of the same input names are removed
        # 
        paths = self.do_task_collate(test_path + "/*.test", task.regex(r"(.*/[ef])[a-z0-9]+\.test"),  
                                            task.inputs(r"\1.whoopee"),  [r"\1.output1", r"\1.output2"], r"\1.extra")

        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            [
                                ['DIR/e.whoopee'],                                 # input
                                ['DIR/e.output1', 'DIR/e.output2'],                # output
                                'DIR/e.extra'                                      # extra
                            ],                                                     
                            [                                                      
                                ['DIR/f.whoopee'],                                 # input 
                                ['DIR/f.output1', 'DIR/f.output2'],                # output
                                'DIR/f.extra'                                      # extra 
                            ]
                        ] )
        
        #
        #   test python set object. Note that set is constructed with the results of the substitution
        #
        paths = self.do_task_collate(test_path + "/*.test", task.regex(r"(.*/[ef])[a-z0-9]+\.test"),  
                                            task.inputs(r"\1.whoopee"),  set([r"\1.output1", r"\1.output2", test_path + "e.output2"]), r"\1.extra")

        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            [
                                ['DIR/e.whoopee'],                                 # input
                                set(['DIR/e.output1', 'DIR/e.output2']),           # output
                                'DIR/e.extra'                                      # extra
                            ],                                                     
                            [                                                      
                                ['DIR/f.whoopee'],                                 # input 
                                set(['DIR/f.output1', 'DIR/f.output2', 'DIR/e.output2']),                # output
                                'DIR/f.extra'                                      # extra 
                            ]
                        ] )

    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """

        paths = self.do_task_collate([task.output_from( "module.func1",       # input params
                                                          "module.func2", 
                                                          "module.func3", 
                                                          "module.func4", 
                                                          "module.func5"),
                                        test_path + "/*.test"], 
                                        task.regex(r"(.*[oef])[a-z0-9]+\.test"),  
                                        [r"\1.output1", r"\1.output2"], r"\1.extra")
        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            [
                                ["DIR/e0.test", "DIR/e1.test", "DIR/e2.test"],  # input  
                                ["DIR/e.output1", "DIR/e.output2"],             # output 
                                "DIR/e.extra"                                   # extra  
                            ], 
                            [
                                ["DIR/f0.test", "DIR/f1.test", "DIR/f2.test"],  # input  
                                ["DIR/f.output1", "DIR/f.output2"],             # output 
                                "DIR/f.extra"                                   # extra  
                            ],
                            [
                                [                                               # input    
                                    [                                           # input    
                                        "output4.test", "output.ignored"        # input    
                                    ],                                          # input    
                                    "output1.test",                             # input    
                                    "output2.test",                             # input    
                                    "output3.test",                             # input    
                                    [2, "output5.test"]                         # input    
                                ],                                              # input   
                                [ "o.output1", "o.output2" ],                   # output  
                                "o.extra"                                       # extra   
                            ]

                        ])
        
        paths = self.do_task_collate([task.output_from( "module.func1",       # input params
                                                          "module.func2", 
                                                          "module.func3", 
                                                          "module.func4", 
                                                          "module.func5"),
                                        test_path + "/*.test"], 
                                        task.regex(r"(.*[oef])[a-z0-9]+\.test"),  
                                        task.inputs(r"\1.whoopee"),  
                                        [r"\1.output1", r"\1.output2"], r"\1.extra")
        paths = recursive_replace(paths, test_path, "DIR")
        self.assertEqual(paths,
                        [
                            [
                                ["DIR/e.whoopee"],                              # input  
                                ["DIR/e.output1", "DIR/e.output2"],             # output 
                                "DIR/e.extra"                                   # extra  
                            ], 
                            [
                                ["DIR/f.whoopee"],                              # input  
                                ["DIR/f.output1", "DIR/f.output2"],             # output 
                                "DIR/f.extra"                                   # extra  
                            ],
                            [
                                ["o.whoopee"],                                  # input  
                                ["o.output1", "o.output2"],                     # output 
                                "o.extra"                                       # extra  
                            ]
                        ] )
            
        
        
        # single job output consisting of a single file
        paths = self.do_task_collate(task.output_from("module.func2"), task.regex(r"(.*)\..*"),  r"\1.output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        #print dumps(paths, indent = 4)
        self.assertEqual(paths, [[["output.ignored"], "output.output"]])


        # Same output if task specified as part of a list of tasks
        paths = self.do_task_collate([task.output_from("module.func2")], task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [[["output.ignored"], "output"]])

        # 
        # single job output consisting of a list
        #
        paths = self.do_task_collate(task.output_from("module.func4"), task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [[[[ 2, "output5.test" ] ], "output"]])

        
        # Same output if task specified as part of a list of tasks
        paths = self.do_task_collate([task.output_from("module.func4")], task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [[[[ 2, "output5.test" ] ], "output"]] )


class Test_files_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        open("%s/f%d.output" % (test_path, 0), "w")
        for i in range(3):
            open("%s/f%d.test" % (test_path, i), "w")
        time.sleep(1)
        open("%s/f%d.output" % (test_path, 1), "w")
        open("%s/f%d.output" % (test_path, 2), "w")

        self.tasks = [t1, t2, t3, t4, t5]


    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (test_path, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (test_path, i))
        os.removedirs(test_path)
        pass


    def get_param_iterator (self, *orig_args):
        # 
        # replace function / function names with tasks
        # 
        # fake virgin task
        fake_task = task._task("module", "func_fake%d" % randint(1, 1000000))
        fake_task.task_files(orig_args)
        return fake_task.param_generator_func

    def files (self, *old_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        return list(self.get_param_iterator (*old_args)())

    def test_glob(self):
        """
        test globbed form
        """
        # 
        # Replacement of globs in first parameter
        # 
        paths = self.files(test_path + "/*", "a.test", "b.test")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [
                                    [
                                        [
                                            "DIR/f0.output",
                                            "DIR/f0.test",
                                            "DIR/f1.output",
                                            "DIR/f1.test",
                                            "DIR/f2.output",
                                            "DIR/f2.test"
                                        ],
                                        "a.test",
                                        "b.test"
                                    ]
                                ])
        # 
        # Replacement of globs in first parameter in-place
        # 
        paths = self.files([test_path + "/*", "robbie.test"], "a.test", "b.test")
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [
                                    [
                                        [
                                            "DIR/f0.output",
                                            "DIR/f0.test",
                                            "DIR/f1.output",
                                            "DIR/f1.test",
                                            "DIR/f2.output",
                                            "DIR/f2.test",
                                            "robbie.test"
                                        ],
                                        "a.test",
                                        "b.test"
                                    ]
                                ])
        # 
        # No Replacement of globs in other parameter of multi-job task
        # 
        paths = self.files([[[test_path + "/*", "robbie.test"], "a.test", "b.test"], ["a.test", ["b.test", 2], "a.*"]])
        paths = recursive_replace(recursive_replace(paths, test_path, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [
                                    [
                                        [
                                            "DIR/f0.output",
                                            "DIR/f0.test",
                                            "DIR/f1.output",
                                            "DIR/f1.test",
                                            "DIR/f2.output",
                                            "DIR/f2.test",
                                            "robbie.test"
                                        ],
                                        "a.test",
                                        "b.test"
                                    ],
                                    ["a.test", ["b.test", 2], "a.*"]
                                ])

    def test_filelist(self):
        """
        test file list form
        """
        # simple list
        file_list = ["DIR/f0.test", "DIR/f1.test", "DIR/f2.test"]
        paths = self.files(*file_list)
        self.assertEqual(paths, [
                                    ("DIR/f0.test", "DIR/f1.test", "DIR/f2.test"),
                                ])

        # complex list
        file_list = [[["DIR/e0.test", set([5, "DIR/e1.test"]), "DIR/e2.test"], ["DIR/f0.test", "DIR/f1.test", "DIR/f2.test"]]]
        paths = self.files(*file_list)
        self.assertEqual(paths, [
                                    ("DIR/e0.test", set([5, "DIR/e1.test"]), "DIR/e2.test"),
                                    ("DIR/f0.test", "DIR/f1.test", "DIR/f2.test"),
                                ])

        # bad list: missing list enclosure
        file_list = [["DIR/f0.test", "DIR/f1.test", "DIR/f2.test"]]
        self.assertRaises(error_task_files, self.files, *file_list)
        
        # bad list: missing io
        file_list = [[[1,2], ["DIR/e0.test", [5, "DIR/e1.test"], "DIR/e2.test"], ["DIR/f0.test", "DIR/f1.test", "DIR/f2.test"]]]
        self.assertRaises(error_task_files, self.files, *file_list)
        
    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """
        #
        #   substitution of tasks
        # 
        paths = self.files(task.output_from(   "module.func1", 
                                               "module.func2", 
                                               "module.func3", 
                                               "module.func4", 
                                               "module.func5"), "rob.test", "b.test")
        self.assertEqual(paths, [(['output1.test', 'output2.test', 'output3.test', ['output4.test', 'output.ignored'], 5, 
                                   'output.ignored', (2, 'output5.test')], 
                                  'rob.test', 
                                  'b.test')])

        #
        #   nested in place substitution of tasks
        # 
        paths = self.files([task.output_from("module.func1", 
                                               "module.func2", 
                                               "module.func3", 
                                               "module.func4", 
                                               "module.func5"), 
                            "robbie.test"], "a.test", "b.test")
        self.assertEqual(paths, [(
                                    ['output1.test', 'output2.test', 'output3.test', ['output4.test', 'output.ignored'], 5,     # input
                                     'output.ignored', (2, 'output5.test'), 'robbie.test'],                                     # input
                                    'a.test',                                                                                   # output
                                    'b.test')])                                                                                  # extra)

        # single job output consisting of a single file
        paths = self.files(task.output_from("module.func2"), "output", "extra")
        self.assertEqual(paths, [('output.ignored', 'output', 'extra')])


        # Different output if task specified as part of a list of tasks
        paths = self.files([task.output_from("module.func2"), task.output_from("module.func2")], "output", "extra")
        self.assertEqual(paths, [(['output.ignored','output.ignored'], 'output', 'extra')])

        # single job output consisting of a list
        paths = self.files(task.output_from("module.func4"), "output", "extra")
        self.assertEqual(paths, [((2, 'output5.test'), 'output', 'extra')])

        # Same output if task specified as part of a list of tasks
        paths = self.files([task.output_from("module.func4"), task.output_from("module.func2")], "output", "extra")
        self.assertEqual(paths,  [([(2, 'output5.test'), 'output.ignored'], 'output', 'extra')])
                
                
                

#
#   debug parameter ignored if called as a module
#     
if sys.argv.count("--debug"):
    sys.argv.remove("--debug")
#sys.argv.append("Test_split_param_factory")
#sys.argv.append("Test_merge_param_factory")
#sys.argv.append("Test_transform_param_factory")
#sys.argv.append("Test_files_param_factory")
unittest.main()



    
