#!/usr/bin/env python
from __future__ import print_function
import unittest
from ruffus.ruffus_utility import *
from ruffus import *

################################################################################
#
#   test_ruffus_utility.py
#
#################################################################################
"""
    test_ruffus_utility.py
"""


import os
import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# _________________________________________________________________________________________

#   get_nested_tasks_or_globs

# _________________________________________________________________________________________
class Test_get_nested_tasks_or_globs(unittest.TestCase):
    def setUp(self):
        exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
        os.chdir(exe_path)

    #       self.assertEqual(self.seq, range(10))
    #       self.assertTrue(element in self.seq)
    #       self.assertRaises(ValueError, random.sample, self.seq, 20)

    def check_equal(self, a, b):
        self.assertEqual(get_nested_tasks_or_globs(a), b)

    def test_get_nested_tasks_or_globs(self):

        #
        # test strings
        #
        self.check_equal("test", (list(), set(), set()))
        self.check_equal([("test1",), "test2", 3], (list(), set(), set()))

        #
        # test missing
        #
        self.check_equal((1, 3, [5]), (list(), set(), set()))
        self.check_equal(None, (list(), set(), set()))

        #
        # test glob
        #
        self.check_equal([("test1.*",), "test?2", 3],
                         (list(), set(['test1.*', 'test?2']), set()))

        #
        # test glob and string
        #
        self.check_equal([("test*1",), (("test3",),), "test2",
                          3], (list(), set(['test*1']), set()))

        #
        # test task function
        #
        self.check_equal(is_glob, (list([is_glob]), set([]), set()))
        self.check_equal([is_glob, [1, "this", ["that*", 5]], [(get_strings_in_flattened_sequence,)]], (
            [is_glob, get_strings_in_flattened_sequence], set(["that*"]), set()))
        #
        # test wrapper
        #
        self.check_equal(output_from(is_glob, ["what", 7], 5), ([
                         is_glob, "what"], set([]), set()))

# _________________________________________________________________________________________

#   replace_placeholders_with_tasks_in_input_params

# _________________________________________________________________________________________


class Test_replace_placeholders_with_tasks_in_input_params(unittest.TestCase):
    def setUp(self):
        exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
        os.chdir(exe_path)

    #       self.assertEqual(self.seq, range(10))
    #       self.assertTrue(element in self.seq)
    #       self.assertRaises(ValueError, random.sample, self.seq, 20)

    def check_equal(self, a, b, d):
        self.assertEqual(
            replace_placeholders_with_tasks_in_input_params(a, d), b)

    def test_replace_placeholders_with_tasks_in_input_params(self):
        func_or_name_to_task = {is_glob: "FF is_glob", "what": "FF what",
                                get_strings_in_flattened_sequence: "FF get_strings_in_flattened_sequence"}

        #
        # test strings
        #
        self.check_equal("test", "test", func_or_name_to_task)
        self.check_equal([("test1",), "test2", 3],
                         [("test1",), "test2", 3],
                         func_or_name_to_task)

        #
        # test missing
        #
        self.check_equal((1, 3, [5]), (1, 3, [5]), func_or_name_to_task)
        self.check_equal(None, None, func_or_name_to_task)

        #
        # test task function
        #
        self.check_equal(is_glob, "FF is_glob", func_or_name_to_task)
        self.check_equal([is_glob, [1, "this", ["that*", 5]], [(get_strings_in_flattened_sequence,)]],
                         ["FF is_glob", [1, "this", ["that*", 5]],
                             [("FF get_strings_in_flattened_sequence",)]],
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


# _________________________________________________________________________________________

#   non_str_sequence

# _________________________________________________________________________________________
class Test_non_str_sequence(unittest.TestCase):

    def test_non_str_sequence(self):
        """
            non_str_sequence()
        """
        test_str1 = "asfas"

        class inherited_str (str):
            #
            # use __new__ instead of init because str is immutable
            #
            def __new__(cls, a):
                obj = super(inherited_str, cls).__new__(inherited_str, a)
                return obj

        test_str2 = inherited_str("test")

        class inherited_list (list):
            def __init__(self, *param):
                list.__init__(self, *param)
        test_str3 = list(test_str1)
        test_str4 = inherited_list(test_str2)
        self.assertTrue(not non_str_sequence(test_str1))
        self.assertTrue(not non_str_sequence(test_str2))
        self.assertTrue(non_str_sequence(test_str3))
        self.assertTrue(non_str_sequence(test_str4))

# _________________________________________________________________________________________

#   get_strings_in_flattened_sequence

# _________________________________________________________________________________________


class Test_get_strings_in_flattened_sequence(unittest.TestCase):

    def test_get_strings_in_flattened_sequence(self):
        """
            get_strings_in_flattened_sequence()
        """
        class inherited_str (str):
            #
            # use __new__ instead of init because str is immutable
            #
            def __new__(cls, a):
                obj = super(inherited_str, cls).__new__(inherited_str, a)
                return obj

        class inherited_list (list):
            def __init__(self, *param):
                list.__init__(self, *param)

        self.assertEqual(get_strings_in_flattened_sequence("one"), ["one"])
        self.assertEqual(get_strings_in_flattened_sequence(
            ["one", "two"]), ["one", "two"])
        self.assertEqual(get_strings_in_flattened_sequence(
            ["one", 1, "two"]), ["one", "two"])
        self.assertEqual(get_strings_in_flattened_sequence(
            ["one", [1, ["two"]]]), ["one", "two"])
        self.assertEqual(get_strings_in_flattened_sequence(
            [inherited_str("one"), [1, ["two"]]]), [inherited_str("one"), "two"])
        self.assertEqual(get_strings_in_flattened_sequence(inherited_list([inherited_str("one"), [1, ["two"]]])),
                         inherited_list([inherited_str("one"), "two"]))


# _________________________________________________________________________________________

#   get_first_strings_in_nested_sequence

# _________________________________________________________________________________________
class Test_get_first_strings_in_nested_sequence(unittest.TestCase):

    def test_get_first_strings_in_nested_sequence(self):
        """
            get_first_strings_in_nested_sequence()
        """
        class inherited_str (str):
            #
            # use __new__ instead of init because str is immutable
            #
            def __new__(cls, a):
                obj = super(inherited_str, cls).__new__(inherited_str, a)
                return obj

        class inherited_list (list):
            def __init__(self, *param):
                list.__init__(self, *param)

        self.assertEqual(get_strings_in_flattened_sequence("one"), ["one"])
        self.assertEqual(get_strings_in_flattened_sequence(
            ["one", "two"]), ["one", "two"])
        self.assertEqual(get_strings_in_flattened_sequence(
            ["one", 1, "two"]), ["one", "two"])
        self.assertEqual(get_strings_in_flattened_sequence(
            ["one", [1, ["two"]]]), ["one", "two"])
        self.assertEqual(get_strings_in_flattened_sequence(
            [inherited_str("one"), [1, ["two"]]]), [inherited_str("one"), "two"])
        self.assertEqual(get_strings_in_flattened_sequence(inherited_list([inherited_str("one"), [1, ["two"]]])),
                         inherited_list([inherited_str("one"), "two"]))
        self.assertEqual(get_strings_in_flattened_sequence(
            ["one", [1, ["two"], "three"]]), ["one", "two", "three"])
        d = {"four": 4}
        self.assertEqual(get_strings_in_flattened_sequence(
            ["one", [1, [d, "two"], "three"]]), ["one", "two", "three"])
        self.assertEqual(get_strings_in_flattened_sequence(None), [])
        self.assertEqual(get_strings_in_flattened_sequence([]), [])
        self.assertEqual(get_strings_in_flattened_sequence([1, 2, 3, d]), [])


# _________________________________________________________________________________________

#   Test_compile_regex

# _________________________________________________________________________________________
class Test_compile_regex (unittest.TestCase):
    def test_compile_regex(self):
        compile_regex("Dummy Task", regex(".*"), Exception, "test1")

        # bad regex
        self.assertRaises(Exception, compile_regex,
                          "Dummy Task", regex(".*)"), Exception, "test1")
        try:
            compile_regex("Dummy Task", regex(".*)"), Exception, "test1")
        except Exception as e:
            self.assertTrue(e.args == ('Dummy Task', "test1: regular expression regex('.*)') is malformed\n[sre_constants.error: (unbalanced parenthesis at position 2)]") or
                            e.args == ('Dummy Task', "test1: regular expression regex('.*)') is malformed\n[sre_constants.error: (unbalanced parenthesis)]") or
                            e.args == ('Dummy Task', "test1: regular expression regex('.*)') is malformed\n[re.error: (unbalanced parenthesis at position 2)]"))

        # bad number of items regex
        self.assertRaises(Exception, compile_regex, "Dummy Task",
                          regex(".*", "o"), Exception, "test1")
        try:
            compile_regex("Dummy Task", regex(".*", "o"), Exception, "test1")
        except Exception as e:
            self.assertEqual(
                e.args, ('Dummy Task', "test1: regex('.*', 'o') is malformed\nregex(...) should only be used to wrap a single regular expression string"))

        # 0 number of items regex
        self.assertRaises(Exception, compile_regex,
                          "Dummy Task", regex(), Exception, "test1")
        try:
            compile_regex("Dummy Task", regex(), Exception, "test1")
        except Exception as e:
            self.assertEqual(
                e.args, ('Dummy Task', 'test1: regex() is malformed\nregex(...) should only be used to wrap a single regular expression string'))

        # bad number of items suffix
        self.assertRaises(Exception, compile_suffix, "Dummy Task",
                          suffix(".*", "o"), Exception, "test1")
        try:
            compile_suffix("Dummy Task", suffix(".*", "o"), Exception, "test1")
        except Exception as e:
            self.assertEqual(
                e.args, ('Dummy Task', "test1: suffix('('.*', 'o')') is malformed.\nsuffix(...) should only be used to wrap a single string matching the suffices of file names"))

        # 0 number of items suffix
        self.assertRaises(Exception, compile_suffix,
                          "Dummy Task", suffix(), Exception, "test1")
        try:
            compile_suffix("Dummy Task", suffix(), Exception, "test1")
        except Exception as e:
            self.assertEqual(
                e.args, ('Dummy Task', 'test1: suffix() is malformed.\nsuffix(...) should be used to wrap a string matching the suffices of file names'))

# _________________________________________________________________________________________

#   Test_check_files_io_parameters

# _________________________________________________________________________________________


class Test_check_files_io_parameters (unittest.TestCase):
    def test_check_files_io_parameters(self):

        class t_fake_task(object):
            def __init__(self):
                self._action_type = None
                self._name = "fake task"
        fake_task = t_fake_task()

        single_job_params = [["input", "output"]]
        multiple_job_params = [["input1", "output1"], ["input2", "output2"]]

        check_files_io_parameters(
            fake_task, single_job_params, error_task_files)
        check_files_io_parameters(
            fake_task, multiple_job_params, error_task_files)

        # Bad format
        bad_single_job_params = ["input", "output"]
        self.assertRaises(error_task_files, check_files_io_parameters,
                          fake_task, bad_single_job_params, error_task_files)

        # Missing output files for job
        bad_multiple_job_params = [["input1", "output1"], ["input2"]]
        self.assertRaises(error_task_files, check_files_io_parameters,
                          fake_task, bad_multiple_job_params, error_task_files)

        # Missing input files for job
        bad_multiple_job_params = [["input1", "output1"], []]
        self.assertRaises(error_task_files, check_files_io_parameters,
                          fake_task, bad_multiple_job_params, error_task_files)

        # Input or output file parameters should contain at least one or more file names strings
        #bad_multiple_job_params = [[1, 2]]
        #self.assertRaises(error_task_files, check_files_io_parameters, fake_task, bad_multiple_job_params, error_task_files)

# _________________________________________________________________________________________

#   Test_get_first_string_in_nested_sequence

# _________________________________________________________________________________________


class Test_get_first_string_in_nested_sequence (unittest.TestCase):
    def test_get_first_string_in_nested_sequence(self):

        self.assertEqual(get_first_string_in_nested_sequence("a"),  "a")
        self.assertEqual(get_first_string_in_nested_sequence(None),  None)
        self.assertEqual(get_first_string_in_nested_sequence(1),  None)
        self.assertEqual(get_first_string_in_nested_sequence((1, 2)),  None)
        self.assertEqual(
            get_first_string_in_nested_sequence((1, 2, "a")),  "a")
        self.assertEqual(
            get_first_string_in_nested_sequence((1, 2, "a")),  "a")
        self.assertEqual(get_first_string_in_nested_sequence(
            (1, [2, "b"], "a")),  "b")
        self.assertEqual(get_first_string_in_nested_sequence(
            (1, set([2, "b"]), "a")),  "b")

# _________________________________________________________________________________________

#   Test_check_parallel_parameters

# _________________________________________________________________________________________


class Test_check_parallel_parameters (unittest.TestCase):
    def test_check_parallel_parameters(self):

        class t_fake_task(object):
            def __init__(self):
                self._action_type = None
                self._name = "fake task"
        fake_task = t_fake_task()

        single_job_params = [["input", "output"]]
        multiple_job_params = [["input1", "output1"], ["input2", "output2"]]

        check_parallel_parameters(
            fake_task, single_job_params, error_task_files)
        check_parallel_parameters(
            fake_task, multiple_job_params, error_task_files)

        # Bad format
        bad_single_job_params = ["input", "output"]
        self.assertRaises(error_task_parallel, check_parallel_parameters,
                          fake_task, bad_single_job_params, error_task_parallel)

# _________________________________________________________________________________________

#   expand_nested_tasks_or_globs

# _________________________________________________________________________________________


class Test_expand_nested_tasks_or_globs(unittest.TestCase):
    def setUp(self):
        exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
        os.chdir(exe_path)
        t1 = task.Task(print, "module.func1")
        t2 = task.Task(print, "module.func2")
        t3 = task.Task(print, "module.func3")
        self.tasks = [t1, t2, t3]

    #       self.assertEqual(self.seq, range(10))
    #       self.assertTrue(element in self.seq)
    #       self.assertRaises(ValueError, random.sample, self.seq, 20)

    def check_equal(self, a, b):

        tasks, globs, runtime_data_names = get_nested_tasks_or_globs(a)
        func_or_name_to_task = dict(list(
            zip((non_str_sequence, get_strings_in_flattened_sequence, "what"), self.tasks)))

        task_or_glob_to_files = dict()
        # for f in func_or_name_to_task:
        #    print f, task_or_glob_to_files[func_or_name_to_task[f]]

        task_or_glob_to_files[self.tasks[0]] = [
            "t1a", "t1b"]       # non_str_sequence
        # get_strings_in_flattened_sequence
        task_or_glob_to_files[self.tasks[1]] = ["t2"]
        task_or_glob_to_files[self.tasks[2]] = ["t3"]               # "what"
        task_or_glob_to_files["that*"] = ["that1", "that2"]
        task_or_glob_to_files["test*1"] = ["test11", "test21"]
        task_or_glob_to_files["test1.*"] = ["test1.1", "test1.2"]
        task_or_glob_to_files["test?2"] = ["test12"]

        param_a = replace_placeholders_with_tasks_in_input_params(
            a, func_or_name_to_task)
        self.assertEqual(expand_nested_tasks_or_globs(
            param_a, task_or_glob_to_files), b)

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
                         [("test1.1", "test1.2"), "test12", 3])
        self.check_equal(["test1.*", "test?2", 3],
                         ["test1.1", "test1.2", "test12", 3])

        #
        # test glob and string
        #
        self.check_equal([("test*1",), (("test3",),), "test2", 3],
                         [("test11", "test21"), (("test3",),), "test2", 3])

        #
        # test task function
        #
        self.check_equal(non_str_sequence, ["t1a", "t1b"])
        self.check_equal(get_strings_in_flattened_sequence, ["t2"])
        self.check_equal([get_strings_in_flattened_sequence,
                          non_str_sequence], ["t2", "t1a", "t1b"])
        self.check_equal([non_str_sequence, [1, "this", ["that*", 5]], [(get_strings_in_flattened_sequence,)]],
                         ['t1a', 't1b', [1, 'this', ['that1', 'that2', 5]], [('t2',)]])
        #
        # test wrapper
        #
        self.check_equal(output_from(non_str_sequence, ["what", 7], 5),
                         ['t1a', 't1b', ['t3', 7], 5])
#
#
# _________________________________________________________________________________________

#   Test_regex_replace

# _________________________________________________________________________________________


class Test_regex_replace (unittest.TestCase):
    def helper(self, data, result):
        regex_str = "([a-z]+)\.([a-z]+)\.([a-z]+)\.([a-z]+)"
        try_result = regex_replace("aaa.bbb.ccc.aaa",
                                   regex_str,
                                   re.compile(regex_str),
                                   data)
        self.assertEqual(try_result,  result)

    def test_regex_replace(self):
        self.helper(r"\3.\2.\1", "ccc.bbb.aaa")
        self.helper(None, None)
        self.helper(1, 1)
        self.helper([r"\3.\2.\1", 1], ["ccc.bbb.aaa", 1])
        # note set is constructed with substituted results!
        self.helper([r"\3.\2.\1", 1, (set([r"\1\2", r"\4\2", "aaabbb"]), "whatever", {1: 2, 3: 4})],
                    ['ccc.bbb.aaa', 1, (set(['aaabbb']), 'whatever', {1: 2, 3: 4})])


# _________________________________________________________________________________________

#   Test_path_decomposition

# _________________________________________________________________________________________
class Test_path_decomposition (unittest.TestCase):
    def helper(self, test_path, expected_result):
        try_result = path_decomposition(test_path)
        self.assertEqual(try_result,  expected_result)

    def test_path_decomposition(self):
        # normal path
        self.helper("/a/b/c/d/filename.txt",
                    {'basename': 'filename',
                        'ext':      '.txt',
                        'subpath':     ['/a/b/c/d', '/a/b/c', '/a/b', '/a', '/'],
                        'subdir': ['d', 'c', 'b', 'a', '/'],
                        'path':    '/a/b/c/d'
                     })
        # double slash
        self.helper("//a/filename.txt",
                    {'basename': 'filename',
                        'ext':      '.txt',
                        'subpath':     ['//a', '//'],
                        'path':    '//a',
                        'subdir': ['a', '//']
                     })
        # test no path
        self.helper("filename.txt",
                    {'basename': 'filename',
                        'ext':      '.txt',
                        'subpath':     [],
                        'path':   '',
                        'subdir': []
                     })
        # root
        self.helper("/filename.txt",
                    {'basename': 'filename',
                        'ext':      '.txt',
                        'path':     '/',
                        'subpath':     ['/'],
                        'subdir':   ['/']
                     })
        # unrooted
        self.helper("a/b/filename.txt",
                    {'basename': 'filename',
                        'ext':      '.txt',
                        'subpath':     ['a/b', 'a'],
                        'path':     'a/b',
                        'subdir':   ['b', 'a']
                     })
        # glob
        self.helper("/a/b/*.txt",
                    {'basename': '*',
                        'ext':      '.txt',
                        'path':     '/a/b',
                        'subpath':     ['/a/b', '/a', '/'],
                        'subdir':   ['b', 'a', '/']
                     })
        # no basename
        # extention becomes basename
        self.helper("/a/b/.txt",
                    {'basename': '.txt',
                        'ext':      '',
                        'path':     '/a/b',
                        'subpath':     ['/a/b', '/a', '/'],
                        'subdir':   ['b', 'a', '/']
                     })
        # no ext
        self.helper("/a/b/filename",
                    {'basename': 'filename',
                        'ext':      '',
                        'path':     '/a/b',
                        'subpath':     ['/a/b', '/a', '/'],
                        'subdir':   ['b', 'a', '/']
                     })
        # empty ext
        self.helper("/a/b/filename.",
                    {'basename': 'filename',
                        'ext':      '.',
                        'path':     '/a/b',
                        'subpath':  ['/a/b', '/a', '/'],
                        'subdir':   ['b', 'a', '/']
                     })
        # only path
        self.helper("/a/b/",
                    {'basename': '',
                        'ext':      '',
                        'path':     '/a/b',
                        'subpath':     ['/a/b', '/a', '/'],
                        'subdir':   ['b', 'a', '/']
                     })


class Test_apply_func_to_sequence (unittest.TestCase):
    def helper(self, test_seq, func, tuple_of_conforming_types, expected_result):
        try_result = apply_func_to_sequence(
            test_seq, func, tuple_of_conforming_types)
        self.assertEqual(try_result, expected_result)

    def test_apply_func_to_sequence(self):

        self.helper([
            ["saf", "sdfasf", 1],
            2,
            set([2, "odd"]),
            {1: 2},
            [
                ["sadf", 3]
            ]
        ],
            len, (str,),
            [
            [3, 6, 1],
            2,
            set([2, 3]),
            {1: 2},
            [
                [4, 3]
            ]
        ])

# _________________________________________________________________________________________

#   Test_parameter_list_as_string

# _________________________________________________________________________________________


class Test_parameter_list_as_string (unittest.TestCase):

    def test_conversion(self):

        self.assertEqual(parameter_list_as_string([1, 2, 3]),
                         '1, 2, 3')
        self.assertEqual(parameter_list_as_string([1, "2", 3]),
                         "1, '2', 3")
        self.assertEqual(parameter_list_as_string([1, None, 3]),
                         '1, None, 3')
        self.assertEqual(parameter_list_as_string([1, [2, 3], 3]),
                         '1, [2, 3], 3')
        self.assertEqual(parameter_list_as_string([1, [], 3]),
                         '1, [], 3')
        self.assertEqual(parameter_list_as_string(None),
                         '')
        self.assertRaises(TypeError, parameter_list_as_string)

#
# _________________________________________________________________________________________

#   Test_regex_match_str

# _________________________________________________________________________________________


class Test_regex_match_str (unittest.TestCase):

    def test_matches(self):

        # first string named and unamed captures, second string no captures
        test_str_list = ["aaa.bbb.ccc", "ddd.eee.fff"]
        compiled_regexes = ["aaa.(b+).(?P<CCC>c+)", "ddd.eee.fff"]
        results = [{0: 'aaa.bbb.ccc', 1: 'bbb',
                    2: 'ccc', 'CCC': 'ccc'}, {0: 'ddd.eee.fff'}]
        for ss, rr, result in zip(test_str_list, compiled_regexes, results):
            self.assertEqual(regex_matches_as_dict(ss, rr), result)

        # first string named and unamed captures, second string unnamed captures
        compiled_regexes = ["aaa.(b+).(?P<CCC>c+)", ".+(f)"]
        results = [{0: 'aaa.bbb.ccc', 1: 'bbb', 2: 'ccc',
                    'CCC': 'ccc'}, {0: 'ddd.eee.fff', 1: 'f'}]
        for ss, rr, result in zip(test_str_list, compiled_regexes, results):
            self.assertEqual(regex_matches_as_dict(ss, rr), result)

        # first string named and unamed captures, second string no capture
        compiled_regexes = ["aaa.(b+).(?P<CCC>c+)", ".+"]
        results = [{0: 'aaa.bbb.ccc', 1: 'bbb',
                    2: 'ccc', 'CCC': 'ccc'}, {0: 'ddd.eee.fff'}]
        for ss, rr, result in zip(test_str_list, compiled_regexes, results):
            self.assertEqual(regex_matches_as_dict(ss, rr), result)

        # first string named and unamed captures, second string None
        compiled_regexes = ["aaa.(b+).(?P<CCC>c+)", None]
        results = [{0: 'aaa.bbb.ccc', 1: 'bbb', 2: 'ccc', 'CCC': 'ccc'}, None]
        for ss, rr, result in zip(test_str_list, compiled_regexes, results):
            self.assertEqual(regex_matches_as_dict(ss, rr), result)

        # Both None
        compiled_regexes = []
        results = [None, None]
        for ss, rr, result in zip(test_str_list, compiled_regexes, results):
            self.assertEqual(regex_matches_as_dict(ss, rr), result)

        # first string named and unamed captures, second string Failed
        compiled_regexes = ["aaa.(b+).(?P<CCC>c+)", "PP"]
        results = [{0: 'aaa.bbb.ccc', 1: 'bbb', 2: 'ccc', 'CCC': 'ccc'}, False]
        for ss, rr, result in zip(test_str_list, compiled_regexes, results):
            self.assertEqual(regex_matches_as_dict(ss, rr), result)

        # first string named and unamed captures, second parameter number not string
        self.assertRaises(Exception, regex_matches_as_dict,
                          test_str_list[0], 6)


# _________________________________________________________________________________________

#   Test_path_decomposition

# _________________________________________________________________________________________
class Test_get_all_paths_components (unittest.TestCase):
    def helper(self, test_paths, regex_str, expected_result):
        try_result = get_all_paths_components(test_paths, regex_str)
        self.assertEqual(try_result,  expected_result)

    def test_get_all_paths_components(self):
        # no regex
        self.helper(["/a/b/c/sample1.bam"], None,
                    [
                        {'basename': 'sample1',
                         'ext': '.bam',
                         'subpath': ['/a/b/c', '/a/b', '/a', '/'],
                         'path': '/a/b/c',
                         'subdir': ['c', 'b', 'a', '/']
                         }
        ])

        # regex
        self.helper(["/a/b/c/sample1.bam"], [r"(.*)(?P<id>\d+)\..+"],
                    [
                        {
                            0: '/a/b/c/sample1.bam',
                            1: '/a/b/c/sample',
                            2: '1',
                            'id': '1',
                            'basename': 'sample1',
                            'ext': '.bam',
                            'subpath': ['/a/b/c', '/a/b', '/a', '/'],
                            'path': '/a/b/c',
                            'subdir': ['c', 'b', 'a', '/']
                        }
        ])
        # nameclash
        # "basename" overridden by named regular expression capture group
        self.helper(["/a/b/c/sample1.bam"], [r"(.*)(?P<basename>\d+)\..+"],
                    [
                        {
                            0: '/a/b/c/sample1.bam',
                            1: '/a/b/c/sample',
                            2: '1',
                            'basename': '1',
                            'ext': '.bam',
                            'subpath': ['/a/b/c', '/a/b', '/a', '/'],
                            'path': '/a/b/c',
                            'subdir': ['c', 'b', 'a', '/']
                        }
        ])

        # empty path
        self.helper([""], [r"(.*)(?P<basename>\d+)\..+"], [{}])
        self.helper(
            [""], [], [{'path': [], 'basename': '', 'ext': '', 'subdir': []}])
        # not matching regular expression
        self.helper(["/a/b/c/nonumber.txt"], [r"(.*)(?P<id>\d+)\..+"], [{}])
        # multiple paths
        self.helper(["/a/b/c/sample1.bam",
                     "dbsnp15.vcf",
                     "/test.txt"],
                    [
                        r"(.*)(?P<id>\d+)\..+",
                        r"(.*)(?P<id>\d+)\..+"],
                    [{
                        0:          '/a/b/c/sample1.bam',           # captured by index
                        1:          '/a/b/c/sample',                # captured by index
                        2:          '1',                            # captured by index
                        'id':       '1',                            # captured by name
                        'ext':      '.bam',
                        'subdir':   ['c', 'b', 'a', '/'],
                        'subpath':     ['/a/b/c', '/a/b', '/a', '/'],
                        'path': '/a/b/c',
                        'basename': 'sample1',
                    },
                        {
                            0: 'dbsnp15.vcf',                           # captured by index
                            1: 'dbsnp1',                                # captured by index
                            2: '5',                                     # captured by index
                            'id': '5',                                  # captured by name
                            'ext': '.vcf',
                            'subdir': [],
                            'subpath': [],
                            'path': '',
                            'basename': 'dbsnp15',
                    },

                        # no regular expression match
                        {
                            'ext': '.txt',
                            'subdir': ["/"],
                            'subpath': ["/"],
                            'path': '/',
                            'basename': 'test',
                    },
        ])
        # multiple paths : a single regular expression mismatch prevents any matches
        self.helper(["/a/b/c/sample1.bam",
                     "dbsnp15.vcf",
                     "/test.txt"],
                    [None,
                        r"(.*)(?P<id>\d+)\..+",
                        r"(.*)(?P<id>\d+)\..+"],
                    [{}, {}, {}])

        # _________________________________________________________________________________________

        #   Test_path_decomposition

        # _________________________________________________________________________________________

        class Test_get_all_paths_components (unittest.TestCase):
            def helper(self, test_paths, regex_str, expected_result):
                try_result = get_all_paths_components(test_paths, regex_str)
                self.assertEqual(try_result,  expected_result)

            def test_get_all_paths_components(self):
                # no regex
                self.helper(["/a/b/c/sample1.bam"], None,
                            [
                                {'basename': 'sample1',
                                 'ext': '.bam',
                                 'subpath': ['/a/b/c', '/a/b', '/a', '/'],
                                 'path': '/a/b/c',
                                 'subdir': ['c', 'b', 'a', '/']
                                 }
                ])

                # regex
                self.helper(["/a/b/c/sample1.bam"],
                            [r"(.*)(?P<id>\d+)\..+"],
                            [
                                {
                                    0: '/a/b/c/sample1.bam',
                                    1: '/a/b/c/sample',
                                    2: '1',
                                    'id': '1',
                                    'basename': 'sample1',
                                    'ext': '.bam',
                                    'subpath': ['/a/b/c', '/a/b', '/a', '/'],
                                    'path': '/a/b/c',
                                    'subdir': ['c', 'b', 'a', '/']
                                }
                ])
                # nameclash
                # "basename" overridden by named regular expression capture group
                self.helper(["/a/b/c/sample1.bam"], [r"(.*)(?P<basename>\d+)\..+"],
                            [
                                {
                                    0: '/a/b/c/sample1.bam',
                                    1: '/a/b/c/sample',
                                    'basename': '1',
                                    'ext': '.bam',
                                    'subpath': ['/a/b/c', '/a/b', '/a', '/'],
                                    'path': '/a/b/c',
                                    'subdir': ['c', 'b', 'a', '/']
                                }
                ])

                # empty path
                self.helper([""], [r"(.*)(?P<basename>\d+)\..+"], [{}])
                # not matching regular expression
                self.helper(["/a/b/c/nonumber.txt"],
                            [r"(.*)(?P<id>\d+)\..+"], [{}])
                # multiple paths
                self.helper(["/a/b/c/sample1.bam",
                             "dbsnp15.vcf",
                             "/test.txt"], [r"(.*)(?P<id>\d+)\..+"],
                            [{
                                0:          '/a/b/c/sample1.bam',           # captured by index
                                1:          '/a/b/c/sample',                # captured by index
                                2:          '1',                            # captured by index
                                'id':       '1',                            # captured by name
                                'ext':      '.bam',
                                'subdir':   ['c', 'b', 'a', '/'],
                                'subpath':     ['/a/b/c', '/a/b', '/a', '/'],
                                'path': '/a/b/c',
                                'basename': 'sample1',
                            },
                                {
                                    0: 'dbsnp15.vcf',                           # captured by index
                                    1: 'dbsnp1',                                # captured by index
                                    2: '5',                                     # captured by index
                                    'id': '5',                                  # captured by name
                                    'ext': '.vcf',
                                    'subdir': [],
                                    'subpath': [],
                                    'path': '',
                                    'basename': 'dbsnp15',
                            },

                                # no regular expression match
                                # everything fails!
                                {
                            }
                ])


#
# _________________________________________________________________________________________

#   Test_swap_nesting_order

# _________________________________________________________________________________________
class Test_swap_nesting_order (unittest.TestCase):

    def test_swap_nesting_order(self):
        orig_data = [
            {'a': 1, 'b': 2},
            {'a': 3, 'b': 4, 'c': 5}
        ]

        self.assertEqual(swap_nesting_order(orig_data),
                         ([],
                             {'a': {0: 1, 1: 3},
                              'c': {1: 5},
                              'b': {0: 2, 1: 4}})
                         )
        orig_data = [
            [{'a': 1, 'b': 2},
             {'a': 3, 'b': 4, 'c': 5}],
            [{'a': 6, 'b': 7},
             {'a': 8, 'b': 9, 'd': 10}]
        ]

        self.assertEqual(swap_doubly_nested_order(orig_data),
                         ([],
                          {'a':  {0: {0: 1, 1: 3}, 1: {0: 6, 1: 8}},
                           'c':  {0: {1: 5}},
                           'b':  {0: {0: 2, 1: 4}, 1: {0: 7, 1: 9}},
                           'd':  {1: {1: 10}}
                           }))


#
# _________________________________________________________________________________________

#   Test_shorten_filenames_encoder

# _________________________________________________________________________________________
class Test_shorten_filenames_encoder (unittest.TestCase):

    def setUp(self):
        import tempfile
        import os
        self.tempdir = tempfile.mkdtemp()
        subdir = self.tempdir + '/foo/bar/baz/bo'
        os.makedirs(subdir)
        os.chdir(subdir)

    def cleanUp(self):
        from shutil import rmtree
        rmtree(self.tempdir)

    def test_shorten_filenames_encoder(self):
        relative_path = os.path.abspath("../test1/something.py")
        absolute_path = "/a/long/path/to/oss/ruffus/ruffus/test/something.py"

        #
        # test relative path
        #
        self.assertEqual(shorten_filenames_encoder(relative_path, 4),
                         '../test1/something.py')

        # list of paths
        self.assertEqual(shorten_filenames_encoder([[relative_path, relative_path]] * 2 + [6], 4),
                         '[[../test1/something.py, ../test1/something.py], [../test1/something.py, ../test1/something.py], 6]')

        #
        # test full path
        #
        self.assertEqual(shorten_filenames_encoder(absolute_path, 4),
                         '.../ruffus/ruffus/test/something.py')

        # list of paths
        self.assertEqual(shorten_filenames_encoder([[absolute_path, absolute_path]] * 2 + [6], 4),
                         '[[.../ruffus/ruffus/test/something.py, .../ruffus/ruffus/test/something.py], '
                         '[.../ruffus/ruffus/test/something.py, .../ruffus/ruffus/test/something.py], 6]')


if __name__ == '__main__':
    unittest.main()
