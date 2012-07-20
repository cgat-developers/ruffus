#!/usr/bin/env python
################################################################################
#
#   test_ruffus_utility.py
#
#
#   Copyright (c) 2009 Leo Goodstadt
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
    test_ruffus_utility.py
"""

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson
import unittest, os,sys
if __name__ != '__main__':
    raise Exception ("This is not a callable module [%s]"  % __main__)


exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *
from ruffus.ruffus_utility import *


os.chdir(exe_path)

import unittest, time

#_________________________________________________________________________________________

#   get_nested_tasks_or_globs

#_________________________________________________________________________________________
class Test_get_nested_tasks_or_globs(unittest.TestCase):
    def setUp(self):
        exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
        os.chdir(exe_path)

    #       self.assertEqual(self.seq, range(10))
    #       self.assert_(element in self.seq)
    #       self.assertRaises(ValueError, random.sample, self.seq, 20)

    def check_equal (self, a,b):
        self.assertEqual(get_nested_tasks_or_globs(a), b)

    def test_get_nested_tasks_or_globs(self):

        #
        # test strings
        #
        self.check_equal("test", (set(), set(), set()))
        self.check_equal([("test1",), "test2", 3], (set(), set(), set()))

        #
        # test missing
        #
        self.check_equal((1,3, [5]), (set(), set(), set()))
        self.check_equal(None, (set(), set(), set()))

        #
        # test glob
        #
        self.check_equal([("test1.*",), "test?2", 3], (set(), set(['test1.*', 'test?2']), set()))

        #
        # test glob and string
        #
        self.check_equal([("test*1",), (("test3",),),"test2", 3], (set(), set(['test*1']), set()))

        #
        # test task function
        #
        self.check_equal(is_glob, (set([is_glob]), set([]), set()))
        self.check_equal([is_glob, [1, "this", ["that*", 5]], [(get_strings_in_nested_sequence,)]], (
                        set([is_glob, get_strings_in_nested_sequence]), set(["that*"]), set()))
        #
        # test wrapper
        #
        self.check_equal(output_from(is_glob, ["what", 7], 5), (set([is_glob, "what"]), set([]), set()))

#_________________________________________________________________________________________

#   replace_func_names_with_tasks

#_________________________________________________________________________________________
class Test_replace_func_names_with_tasks(unittest.TestCase):
    def setUp(self):
        exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
        os.chdir(exe_path)

    #       self.assertEqual(self.seq, range(10))
    #       self.assert_(element in self.seq)
    #       self.assertRaises(ValueError, random.sample, self.seq, 20)

    def check_equal (self, a,b, d):
        self.assertEqual(replace_func_names_with_tasks(a, d), b)

    def test_replace_func_names_with_tasks(self):
        func_or_name_to_task = {is_glob: "FF is_glob", "what" : "FF what", get_strings_in_nested_sequence: "FF get_strings_in_nested_sequence"}


        #
        # test strings
        #
        self.check_equal("test", "test", func_or_name_to_task)
        self.check_equal(   [("test1",), "test2", 3],
                            [("test1",), "test2", 3],
                            func_or_name_to_task)

        #
        # test missing
        #
        self.check_equal((1,3, [5]), (1,3, [5]), func_or_name_to_task)
        self.check_equal(None, None, func_or_name_to_task)



        #
        # test task function
        #
        self.check_equal(is_glob, "FF is_glob", func_or_name_to_task)
        self.check_equal([is_glob, [1, "this", ["that*", 5]], [(get_strings_in_nested_sequence,)]],
                        ["FF is_glob", [1, "this", ["that*", 5]], [("FF get_strings_in_nested_sequence",)]],
                        func_or_name_to_task)
        #
        # test wrapper
        #
        self.check_equal(output_from(is_glob, ["what", 7], 5),
                        ["FF is_glob", ["FF what", 7], 5],
                        func_or_name_to_task)
        self.check_equal(output_from(is_glob),
                        "FF is_glob",
                        func_or_name_to_task)

        self.check_equal([1, output_from(is_glob, ["what", 7], 5)],
                        [1, "FF is_glob", ["FF what", 7], 5],
                        func_or_name_to_task)

        self.check_equal([1, output_from(is_glob), ["what", 7], 5],
                        [1, "FF is_glob", ["what", 7], 5],
                        func_or_name_to_task)



#_________________________________________________________________________________________

#   non_str_sequence

#_________________________________________________________________________________________
class Test_non_str_sequence(unittest.TestCase):

    def test_non_str_sequence (self):
        """
            non_str_sequence()
        """
        test_str1 = "asfas"
        class inherited_str (str):
            #
            # use __new__ instead of init because str is immutable
            #
            def __new__( cls, a):
                obj = super( inherited_str, cls).__new__( inherited_str, a )
                return obj

        test_str2 = inherited_str("test")
        class inherited_list (list):
            def __init__ (self, *param):
                list.__init__(self, *param)
        test_str3 = list(test_str1)
        test_str4 = inherited_list(test_str2)
        self.assert_(not non_str_sequence(test_str1))
        self.assert_(not non_str_sequence(test_str2))
        self.assert_(non_str_sequence(test_str3))
        self.assert_(non_str_sequence(test_str4))

#_________________________________________________________________________________________

#   get_strings_in_nested_sequence

#_________________________________________________________________________________________
class Test_get_strings_in_nested_sequence(unittest.TestCase):

    def test_get_strings_in_nested_sequence (self):
        """
            get_strings_in_nested_sequence()
        """
        class inherited_str (str):
            #
            # use __new__ instead of init because str is immutable
            #
            def __new__( cls, a):
                obj = super( inherited_str, cls).__new__( inherited_str, a )
                return obj

        class inherited_list (list):
            def __init__ (self, *param):
                list.__init__(self, *param)

        self.assertEqual(get_strings_in_nested_sequence("one"), ["one"])
        self.assertEqual(get_strings_in_nested_sequence(["one", "two"]), ["one", "two"])
        self.assertEqual(get_strings_in_nested_sequence(["one", 1, "two"]), ["one", "two"])
        self.assertEqual(get_strings_in_nested_sequence(["one", [1, ["two"]]]), ["one", "two"])
        self.assertEqual(get_strings_in_nested_sequence([inherited_str("one"), [1, ["two"]]]), [inherited_str("one"), "two"])
        self.assertEqual(get_strings_in_nested_sequence(inherited_list([inherited_str("one"), [1, ["two"]]])),
                                                    inherited_list([inherited_str("one"), "two"]))


#_________________________________________________________________________________________

#   get_first_strings_in_nested_sequence

#_________________________________________________________________________________________
class Test_get_first_strings_in_nested_sequence(unittest.TestCase):

    def test_get_first_strings_in_nested_sequence (self):
        """
            get_first_strings_in_nested_sequence()
        """
        class inherited_str (str):
            #
            # use __new__ instead of init because str is immutable
            #
            def __new__( cls, a):
                obj = super( inherited_str, cls).__new__( inherited_str, a )
                return obj

        class inherited_list (list):
            def __init__ (self, *param):
                list.__init__(self, *param)

        self.assertEqual(get_strings_in_nested_sequence("one", True), ["one"])
        self.assertEqual(get_strings_in_nested_sequence(["one", "two"], True), ["one", "two"])
        self.assertEqual(get_strings_in_nested_sequence(["one", 1, "two"], True), ["one", "two"])
        self.assertEqual(get_strings_in_nested_sequence(["one", [1, ["two"]]], True), ["one", "two"])
        self.assertEqual(get_strings_in_nested_sequence([inherited_str("one"), [1, ["two"]]], True), [inherited_str("one"), "two"])
        self.assertEqual(get_strings_in_nested_sequence(inherited_list([inherited_str("one"), [1, ["two"]]]), True),
                                                          inherited_list([inherited_str("one"), "two"]))
        self.assertEqual(get_strings_in_nested_sequence(["one", [1, ["two"], "three"]], True), ["one", "two"])
        d = {"four" :4}
        self.assertEqual(get_strings_in_nested_sequence(["one", [1, [d, "two"], "three"]], True), ["one", "two"])
        self.assertEqual(get_strings_in_nested_sequence(None, True), [])
        self.assertEqual(get_strings_in_nested_sequence([], True), [])
        self.assertEqual(get_strings_in_nested_sequence([1,2,3, d], True), [])


#_________________________________________________________________________________________

#   Test_compile_regex

#_________________________________________________________________________________________
class Test_compile_regex (unittest.TestCase):
    def test_compile_regex (self):
        compile_regex("Dummy Task", regex(".*"), Exception, "test1")

        # bad regex
        self.assertRaises(Exception, compile_regex, "Dummy Task", regex(".*)"), Exception, "test1")
        try:
            compile_regex("Dummy Task", regex(".*)"), Exception, "test1")
        except Exception, e:
            self.assertEqual(e.args, ('Dummy Task', "test1: regular expression regex('.*)') is malformed\n[sre_constants.error: (unbalanced parenthesis)]"))

        # bad number of items regex
        self.assertRaises(Exception, compile_regex, "Dummy Task", regex(".*", "o"), Exception, "test1")
        try:
            compile_regex("Dummy Task", regex(".*", "o"), Exception, "test1")
        except Exception, e:
            self.assertEqual(e.args, ('Dummy Task', "test1: regex('('.*', 'o')') is malformed\nregex(...) should only be used to wrap a single regular expression string"))

        # 0 number of items regex
        self.assertRaises(Exception, compile_regex, "Dummy Task", regex(), Exception, "test1")
        try:
            compile_regex("Dummy Task", regex(), Exception, "test1")
        except Exception, e:
            self.assertEqual(e.args, ('Dummy Task', 'test1: regex() is malformed\nregex(...) should be used to wrap a regular expression string'))

        # bad number of items suffix
        self.assertRaises(Exception, compile_suffix, "Dummy Task", suffix(".*", "o"), Exception, "test1")
        try:
            compile_suffix("Dummy Task", suffix(".*", "o"), Exception, "test1")
        except Exception, e:
            self.assertEqual(e.args, ('Dummy Task', "test1: suffix('('.*', 'o')') is malformed.\nsuffix(...) should only be used to wrap a single string matching the suffices of file names"))

        # 0 number of items suffix
        self.assertRaises(Exception, compile_suffix, "Dummy Task", suffix(), Exception, "test1")
        try:
            compile_suffix("Dummy Task", suffix(), Exception, "test1")
        except Exception, e:
            self.assertEqual(e.args, ('Dummy Task', 'test1: suffix() is malformed.\nsuffix(...) should be used to wrap a string matching the suffices of file names'))

#_________________________________________________________________________________________

#   Test_check_files_io_parameters

#_________________________________________________________________________________________
class Test_check_files_io_parameters (unittest.TestCase):
    def test_check_files_io_parameters(self):


        class t_fake_task(object):
            def __init__ (self):
                self._action_type = None
                self._name = "fake task"
        fake_task = t_fake_task()

        single_job_params = [["input", "output"]]
        multiple_job_params = [["input1", "output1"], ["input2", "output2"]]

        check_files_io_parameters (fake_task, single_job_params, error_task_files)
        check_files_io_parameters (fake_task, multiple_job_params, error_task_files)


        #Bad format
        bad_single_job_params   = ["input", "output"]
        self.assertRaises(error_task_files, check_files_io_parameters, fake_task, bad_single_job_params, error_task_files)

        #Missing output files for job
        bad_multiple_job_params = [["input1", "output1"], ["input2"]]
        self.assertRaises(error_task_files, check_files_io_parameters, fake_task, bad_multiple_job_params, error_task_files)

        #Missing input files for job
        bad_multiple_job_params = [["input1", "output1"], []]
        self.assertRaises(error_task_files, check_files_io_parameters, fake_task, bad_multiple_job_params, error_task_files)

        #Input or output file parameters should contain at least one or more file names strings
        #bad_multiple_job_params = [[1, 2]]
        #self.assertRaises(error_task_files, check_files_io_parameters, fake_task, bad_multiple_job_params, error_task_files)

#_________________________________________________________________________________________

#   Test_get_first_string_in_nested_sequence

#_________________________________________________________________________________________
class Test_get_first_string_in_nested_sequence (unittest.TestCase):
    def test_get_first_string_in_nested_sequence(self):

        self.assertEqual(get_first_string_in_nested_sequence("a") ,  "a")
        self.assertEqual(get_first_string_in_nested_sequence(None) ,  None)
        self.assertEqual(get_first_string_in_nested_sequence(1) ,  None)
        self.assertEqual(get_first_string_in_nested_sequence((1,2)) ,  None)
        self.assertEqual(get_first_string_in_nested_sequence((1,2, "a")) ,  "a")
        self.assertEqual(get_first_string_in_nested_sequence((1,2, "a")) ,  "a")
        self.assertEqual(get_first_string_in_nested_sequence((1,[2,"b"], "a")) ,  "b")
        self.assertEqual(get_first_string_in_nested_sequence((1,set([2,"b"]), "a")) ,  "b")

#_________________________________________________________________________________________

#   Test_check_parallel_parameters

#_________________________________________________________________________________________
class Test_check_parallel_parameters (unittest.TestCase):
    def test_check_parallel_parameters(self):


        class t_fake_task(object):
            def __init__ (self):
                self._action_type = None
                self._name = "fake task"
        fake_task = t_fake_task()

        single_job_params = [["input", "output"]]
        multiple_job_params = [["input1", "output1"], ["input2", "output2"]]

        check_parallel_parameters (fake_task, single_job_params, error_task_files)
        check_parallel_parameters (fake_task, multiple_job_params, error_task_files)


        #Bad format
        bad_single_job_params   = ["input", "output"]
        self.assertRaises(error_task_parallel, check_parallel_parameters, fake_task, bad_single_job_params, error_task_parallel)

#_________________________________________________________________________________________

#   expand_nested_tasks_or_globs

#_________________________________________________________________________________________
class Test_expand_nested_tasks_or_globs(unittest.TestCase):
    def setUp(self):
        exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
        os.chdir(exe_path)
        t1 = task._task("module", "func1");
        t2 = task._task("module", "func2");
        t3 = task._task("module", "func3");
        self.tasks = [t1, t2, t3]

    #       self.assertEqual(self.seq, range(10))
    #       self.assert_(element in self.seq)
    #       self.assertRaises(ValueError, random.sample, self.seq, 20)

    def check_equal (self, a,b):

        tasks, globs, runtime_data_names = get_nested_tasks_or_globs(a)
        func_or_name_to_task = dict(zip((non_str_sequence, get_strings_in_nested_sequence, "what"), self.tasks))

        task_or_glob_to_files = dict()
        #for f in func_or_name_to_task:
        #    print f, task_or_glob_to_files[func_or_name_to_task[f]]

        task_or_glob_to_files[self.tasks[0]  ] = ["t1a", "t1b"]       # non_str_sequence
        task_or_glob_to_files[self.tasks[1]  ] = ["t2"]               # get_strings_in_nested_sequence
        task_or_glob_to_files[self.tasks[2]  ] = ["t3"]               # "what"
        task_or_glob_to_files["that*"  ] = ["that1", "that2"]
        task_or_glob_to_files["test*1" ] = ["test11","test21"]
        task_or_glob_to_files["test1.*"] = ["test1.1", "test1.2"]
        task_or_glob_to_files["test?2" ] = ["test12"]


        param_a = replace_func_names_with_tasks(a, func_or_name_to_task)
        self.assertEqual(expand_nested_tasks_or_globs(param_a, task_or_glob_to_files), b)

    def test_expand_nested_tasks_or_globs(self):

        #
        # test strings
        #
        self.check_equal("test", "test")
        self.check_equal([("test1",), "test2", 3], [("test1",), "test2", 3])

        #
        # test missing
        #
        self.check_equal(None, None)

        #
        # test glob
        #
        self.check_equal([("test1.*",), "test?2", 3],
                         [("test1.1","test1.2"), "test12", 3])
        self.check_equal(["test1.*", "test?2", 3],
                         ["test1.1","test1.2", "test12", 3])

        #
        # test glob and string
        #
        self.check_equal([("test*1",), (("test3",),),"test2", 3],
                        [("test11","test21"), (("test3",),),"test2", 3])

        #
        # test task function
        #
        self.check_equal(non_str_sequence, ["t1a", "t1b"])
        self.check_equal(get_strings_in_nested_sequence, ["t2"])
        self.check_equal([get_strings_in_nested_sequence, non_str_sequence], ["t2", "t1a", "t1b"])
        self.check_equal([non_str_sequence, [1, "this", ["that*", 5]], [(get_strings_in_nested_sequence,)]],
                         ['t1a', 't1b', [1, 'this', ['that1', 'that2', 5]], [('t2',)]])
        #
        # test wrapper
        #
        self.check_equal(output_from(non_str_sequence, ["what", 7], 5),
                        ['t1a', 't1b', ['t3', 7], 5])
#
#
#_________________________________________________________________________________________

#   Test_regex_replace

#_________________________________________________________________________________________
class Test_regex_replace (unittest.TestCase):
    def helper (self, data, result):
        try_result = regex_replace("aaa.bbb.ccc.aaa",
                                                                  re.compile("([a-z]+)\.([a-z]+)\.([a-z]+)\.([a-z]+)"),
                                                                  data)
        self.assertEqual(try_result ,  result)

    def test_regex_replace(self):
        self.helper(r"\3.\2.\1", "ccc.bbb.aaa")
        self.helper(None, None)
        self.helper(1, 1)
        self.helper([r"\3.\2.\1", 1], ["ccc.bbb.aaa", 1])
        # note set is constructed with substituted results!
        self.helper([r"\3.\2.\1", 1, (set([r"\1\2", r"\4\2", "aaabbb"]), "whatever", {1:2, 3:4})],
                    ['ccc.bbb.aaa', 1, (set(['aaabbb']), 'whatever', {1: 2, 3: 4})])




#
#   debug parameter ignored if called as a module
#
if sys.argv.count("--debug"):
    sys.argv.remove("--debug")
#sys.argv.append("Test_regex_replace")
unittest.main()



