#!/usr/bin/env python
from __future__ import print_function
import time
import unittest
from random import randint
import inspect
from ruffus.file_name_parameters import needs_update_check_modify_time, check_input_files_exist, \
    args_param_factory, open_job_history
from ruffus.file_name_parameters import non_str_sequence
from ruffus import output_from, add_inputs
from ruffus import task, combine
import sys

"""

    test_file_name_parameters.py

"""


import os
tempdir = os.path.abspath(os.path.abspath(os.path.splitext(__file__)[0]))
exe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Unit Tests


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

# print ruffus.__version__
history_file = ':memory:'
history_file = None

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson


dumps = json.dumps


def touch(filename):
    with open(filename, "w"):
        pass


# =========================================================================================
#   args_param_factory
# =========================================================================================


def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


def double_parameters(params):
    return [(p, p) for p in params]


class Test_args_param_factory(unittest.TestCase):

    #       self.assertEqual(self.seq, range(10))
    #       self.assertTrue(element in self.seq)
    #       self.assertRaises(ValueError, random.sample, self.seq, 20)

    def forwarded_function(self, params):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        it = args_param_factory(params)
        return list(it(None))

    def test_single_job_per_task(self):
        """
        test convenience form for single job per task
        """
        self.assertEqual(self.forwarded_function([["file.input", "file.output", "other", 1]]),
                         double_parameters([['file.input', 'file.output', 'other', 1]]))

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
                         double_parameters(params))

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
                         double_parameters(params))


# =========================================================================================

#   files_re_param_factory

# =========================================================================================

def recursive_replace(p, from_s, to_s):
    """
    recursively replaces file name specifications using regular expressions
    Non-strings are left alone
    """
    if isinstance(p, str):
        return p.replace(from_s, to_s)
    elif non_str_sequence(p):
        return type(p)(recursive_replace(pp, from_s, to_s) for pp in p)
    else:
        return p


def list_generator_factory(list):
    def list_generator(ignored_args):
        for i in list:
            yield i, i
    return list_generator


l1 = [["input1", "output1.test"], [3, "output2.test"], [
    "input3", "output3.test"], [3, ["output4.test", "output.ignored"]], [], [4, 5]]
l2 = [["output4.test", "output.ignored"]]
l3 = []
l4 = [[1, (2, "output5.test")]]
t1 = task.Task(list_generator_factory, "module.func1")
t1.param_generator_func = list_generator_factory(l1)
t2 = task.Task(list_generator_factory, "module.func2")
t2.param_generator_func = list_generator_factory(l2)
t2._is_single_job_single_output = t2._single_job_single_output
t3 = task.Task(list_generator_factory, "module.func3")
t3.param_generator_func = list_generator_factory(l3)
t4 = task.Task(list_generator_factory, "module.func4")
t4.param_generator_func = list_generator_factory(l4)
t4._is_single_job_single_output = t4._single_job_single_output
t5 = task.Task(list_generator_factory, "module.func5")
t5.param_generator_func = None

next_task_id = 1


class Test_files_re_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        touch("%s/f%d.output" % (tempdir, 0))
        for i in range(3):
            touch("%s/f%d.test" % (tempdir, i))
        time.sleep(0.1)
        touch("%s/f%d.output" % (tempdir, 1))
        touch("%s/f%d.output" % (tempdir, 2))
        self.tasks = [t1, t2, t3, t4, t5]

    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (tempdir, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (tempdir, i))
        os.removedirs(tempdir)
        pass

    #       self.assertEqual(self.seq, range(10))
    #       self.assertTrue(element in self.seq)
    #       self.assertRaises(ValueError, random.sample, self.seq, 20)

    # def get_param_iterator (self, *old_args):

    def get_param_iterator(self, *unnamed_args, **named_args):
        #
        # replace function / function names with tasks
        #
        # fake virgin task
        # use global incrementing index to avoid name clashes
        #fake_task = task.Task("module", "func_fake%d" % randint(1, 1000000))
        global next_task_id
        next_task_id += 1
        fake_task = task.Task(list_generator_factory,
                              "module.func_fake%d" % next_task_id)
        fake_task._decorator_files_re(*unnamed_args, **named_args)
        fake_task._complete_setup()
        return fake_task.param_generator_func, fake_task

    def files_re(self, *unnamed_args, **named_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        return list(p1 for (p1, ps) in self.get_param_iterator(*unnamed_args, **named_args)[0](None))
        # return list(self.get_param_iterator (*old_args)(None))

    def check_input_files_exist(self, *unnamed_args, **named_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        it = self.get_param_iterator(*unnamed_args, **named_args)[0]
        for param, param2 in it(None):
            check_input_files_exist(*param)
        return True

    def needs_update_check_modify_time(self, *unnamed_args, **named_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        it, task = self.get_param_iterator(*unnamed_args, **named_args)
        #print >> sys.stderr, [p for (p, param2) in it(None)], "??"
        return [needs_update_check_modify_time(*p, task=task,
                                               job_history=open_job_history(history_file)) for (p, param2) in it(None)]

    def test_combine(self):
        """
        test combining operator
        """
        paths = self.files_re(tempdir + "/*", r"(.*).test$",
                              combine(r"\1.input"), r"\1.output")
        self.assertEqual(recursive_replace(paths, tempdir, "DIR"),
                         [
            (('DIR/f0.input',), 'DIR/f0.output'),
                             (('DIR/f1.input',), 'DIR/f1.output'),
                             (('DIR/f2.input',), 'DIR/f2.output'),
        ]
        )
        paths = self.files_re(tempdir + "/*", "(.*).test$",
                              combine(r"\1.input"), r"combined.output")
        self.assertEqual(recursive_replace(paths, tempdir, "DIR"),
                         [(('DIR/f0.input',
                            'DIR/f1.input',
                            'DIR/f2.input'), 'combined.output')])

    def test_glob(self):
        """
        test globbed form
        """
        #
        # simple 1 input, 1 output
        #
        paths = self.files_re(tempdir + "/*", "(.*).test$",
                              r"\1.input", r"\1.output")
        self.assertEqual(recursive_replace(paths, tempdir, "DIR"),
                         [('DIR/f0.input', 'DIR/f0.output'),
                          ('DIR/f1.input', 'DIR/f1.output'),
                          ('DIR/f2.input', 'DIR/f2.output')])
        self.assertTrue(self.check_input_files_exist(tempdir + "/*", "(.*).test$",
                                                     r"\1.test", r"\1.output"))

        #
        # nested forms
        #
        paths = self.files_re(tempdir + "/*", "(.*).test$",
                              [r"\1.input", 2, ["something", r"\1"]], r"\1.output", r"\1.extra", 5)
        self.assertEqual(recursive_replace(paths, tempdir, "DIR"),
                         [(['DIR/f0.input', 2, ['something', 'DIR/f0']], 'DIR/f0.output', 'DIR/f0.extra', 5),
                          (['DIR/f1.input', 2, ['something', 'DIR/f1']],
                           'DIR/f1.output', 'DIR/f1.extra', 5),
                          (['DIR/f2.input', 2, ['something', 'DIR/f2']], 'DIR/f2.output', 'DIR/f2.extra', 5)])

        #
        # only output
        #
        paths = self.files_re(tempdir + "/*", ".*/(.*).test$", r"\1.output")
        self.assertEqual(recursive_replace(paths, tempdir, "DIR"),
                         [('DIR/f0.test', 'f0.output'),
                             ('DIR/f1.test', 'f1.output'),
                             ('DIR/f2.test', 'f2.output')])

    def test_globbed_up_to_date(self):
        """
        test glob form
        """
        #
        # check simple is up to date
        #
        self.assertEqual([res[0] for res in self.needs_update_check_modify_time(tempdir + "/*",
                                                                                "(.*).test$", r"\1.output")], [True, False, False])
        #
        # check complex is up to date
        #
        self.assertEqual([res[0] for res in self.needs_update_check_modify_time(tempdir + "/*",
                                                                                "(.*).test$", [1, 2, [[r"\1.output",
                                                                                                       r"\1.output"]]])], [True, False, False])

    def test_filelist(self):
        """
        test file list form
        """
        file_list = ["DIR/f0.test", "DIR/f1.test", "DIR/f2.test"]
        #
        # simple 1 input, 1 output
        #
        paths = self.files_re(file_list, r"(.*).test$",
                              r"\1.input", r"\1.output")
        self.assertEqual(recursive_replace(paths, tempdir, "DIR"),
                         [('DIR/f0.input', 'DIR/f0.output'),
                          ('DIR/f1.input', 'DIR/f1.output'),
                          ('DIR/f2.input', 'DIR/f2.output')])

        #
        # nested forms
        #
        paths = self.files_re(
            file_list, "(.*).test$", [r"\1.input", 2, ["something", r"\1"]], r"\1.output", r"\1.extra", 5)
        self.assertEqual(recursive_replace(paths, tempdir, "DIR"),
                         [(['DIR/f0.input', 2, ['something', 'DIR/f0']], 'DIR/f0.output', 'DIR/f0.extra', 5),
                          (['DIR/f1.input', 2, ['something', 'DIR/f1']],
                           'DIR/f1.output', 'DIR/f1.extra', 5),
                          (['DIR/f2.input', 2, ['something', 'DIR/f2']], 'DIR/f2.output', 'DIR/f2.extra', 5)])

        #
        # only output
        #
        paths = self.files_re(file_list, ".*/(.*).test$", r"\1.output")
        self.assertEqual(recursive_replace(paths, tempdir, "DIR"),
                         [('DIR/f0.test', 'f0.output'),
                             ('DIR/f1.test', 'f1.output'),
                             ('DIR/f2.test', 'f2.output')])

    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """

        paths = self.files_re(output_from("module.func1",
                                               "module.func2",
                                               "module.func3",
                                               "module.func4",
                                               "module.func5"), r"(.test)", r"\1.yes")
        self.assertEqual(paths,
                         [
                             ((2, 'output5.test'), 'output5.test.yes'),
                             (['output4.test', 'output.ignored'],
                              'output4.test.yes'),
                             ('output1.test', 'output1.test.yes'),
                             ('output2.test', 'output2.test.yes'),
                             ('output3.test', 'output3.test.yes'),
                         ])

        paths = self.files_re(output_from(
            "module.func2"), r"(.ignored)", r"\1.yes")
        self.assertEqual(paths,
                         [('output.ignored', 'output.ignored.yes')])
        paths = self.files_re(
            [output_from("module.func2")], r"(.ignored)", r"\1.yes")
        self.assertEqual(paths,
                         [('output.ignored', 'output.ignored.yes')])


# =========================================================================================

#   split_param_factory

# =========================================================================================

class Test_split_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        touch("%s/f%d.output" % (tempdir, 0))
        for i in range(3):
            touch("%s/f%d.test" % (tempdir, i))
        time.sleep(0.1)
        touch("%s/f%d.output" % (tempdir, 1))
        touch("%s/f%d.output" % (tempdir, 2))
        for ii in range(3):
            touch("%s/%d.test_match1" % (tempdir, ii))
            touch("%s/%d.test_match2" % (tempdir, ii))

        self.tasks = [t1, t2, t3, t4, t5]

    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (tempdir, i))
            os.unlink("%s/%d.test_match1" % (tempdir, i))
            os.unlink("%s/%d.test_match2" % (tempdir, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (tempdir, i))
        os.removedirs(tempdir)
        pass

    # _____________________________________________________________________________

    #   wrappers

    # _____________________________________________________________________________

    def get_param_iterator(self, *unnamed_args, **named_args):
        #
        # replace function / function names with tasks
        #
        # fake virgin task
        fake_task = task.Task(list_generator_factory,
                              "module.func_fake%d" % randint(1, 1000000))
        fake_task._decorator_split(*unnamed_args, **named_args)
        fake_task._complete_setup()
        return fake_task.param_generator_func

    def do_task_split(self, *unnamed_args, **named_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        # extra dereference because we are only interested in the first (only) job
        # return list(self.get_param_iterator (*unnamed_args, **named_args)(None))[0]
        return list(p1 for (p1, ps) in self.get_param_iterator(*unnamed_args, **named_args)(None))[0]

    def test_glob(self):
        """
        test globbed form
        """
        #
        # simple 1 input, 1 output
        #
        paths = self.do_task_split(
            tempdir + "/*", [tempdir + "/*.test_match1", tempdir + "/*.test_match2"])
        self.assertEqual(recursive_replace(recursive_replace(paths, tempdir, "DIR"), exe_path, "DIR"),
                         (['DIR/0.test_match1',
                           'DIR/0.test_match2',
                             'DIR/1.test_match1',
                             'DIR/1.test_match2',
                             'DIR/2.test_match1',
                             'DIR/2.test_match2',
                             'DIR/f0.output',
                             'DIR/f0.test',
                             'DIR/f1.output',
                             'DIR/f1.test',
                             'DIR/f2.output',
                             'DIR/f2.test'],
                          ['DIR/0.test_match1',
                             'DIR/1.test_match1',
                             'DIR/2.test_match1',
                             'DIR/0.test_match2',
                             'DIR/1.test_match2',
                             'DIR/2.test_match2']))

    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """

        paths = self.do_task_split([output_from("module.func1",       # input params
                                                     "module.func2",
                                                     "module.func3",
                                                     "module.func4",
                                                     "module.func5"),
                                    tempdir + "/*"],
                                   [tempdir + "/*.test_match1",                    # output params
                                    tempdir + "/*.test_match2",
                                    "extra.file"],
                                   6)                                      # extra params
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR")
        self.assertEqual(paths,
                         ([5,
                           ['output4.test', 'output.ignored'],
                           'output1.test',
                           'output2.test',
                           'output3.test',
                           'output.ignored',
                           (2, 'output5.test'),
                           'DIR/0.test_match1',
                           'DIR/0.test_match2',
                           'DIR/1.test_match1',
                           'DIR/1.test_match2',
                           'DIR/2.test_match1',
                           'DIR/2.test_match2',
                           'DIR/f0.output',
                           'DIR/f0.test',
                           'DIR/f1.output',
                           'DIR/f1.test',
                           'DIR/f2.output',
                           'DIR/f2.test'],
                          ['DIR/0.test_match1',
                             'DIR/1.test_match1',
                             'DIR/2.test_match1',
                             'DIR/0.test_match2',
                             'DIR/1.test_match2',
                             'DIR/2.test_match2',
                             'extra.file'],
                          6))

        # single job output consisting of a single file
        paths = self.do_task_split(output_from(
            "module.func2"), tempdir + "/*.test_match1")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths,  ('output.ignored', [
                         'DIR/0.test_match1', 'DIR/1.test_match1', 'DIR/2.test_match1']))

        paths = self.do_task_split(
            [output_from("module.func2")], tempdir + "/*.test_match1")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths,  (['output.ignored'], [
                         'DIR/0.test_match1', 'DIR/1.test_match1', 'DIR/2.test_match1']))

        # single job output consisting of a list
        paths = self.do_task_split(output_from(
            "module.func4"), tempdir + "/*.test_match1")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths,  ((2, 'output5.test'), [
                         'DIR/0.test_match1', 'DIR/1.test_match1', 'DIR/2.test_match1']))

        paths = self.do_task_split(
            [output_from("module.func4")], tempdir + "/*.test_match1")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, ([(2, 'output5.test')], [
                         'DIR/0.test_match1', 'DIR/1.test_match1', 'DIR/2.test_match1']))

# =========================================================================================

#   merge_param_factory

# =========================================================================================


class Test_merge_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        touch("%s/f%d.output" % (tempdir, 0))
        for i in range(3):
            touch("%s/f%d.test" % (tempdir, i))
        time.sleep(0.1)
        touch("%s/f%d.output" % (tempdir, 1))
        touch("%s/f%d.output" % (tempdir, 2))

        self.tasks = [t1, t2, t3, t4, t5]

    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (tempdir, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (tempdir, i))
        os.removedirs(tempdir)
        pass

    # _____________________________________________________________________________

    #   wrappers

    # _____________________________________________________________________________

    def get_param_iterator(self, *unnamed_args, **named_args):
        #
        # replace function / function names with tasks
        #
        # fake virgin task
        fake_task = task.Task(list_generator_factory,
                              "module.func_fake%d" % randint(1, 1000000))
        fake_task._decorator_merge(*unnamed_args, **named_args)
        fake_task._complete_setup()
        return fake_task.param_generator_func

    def do_task_merge(self, *unnamed_args, **named_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        # extra dereference because we are only interested in the first (only) job
        return list(p1 for (p1, ps) in self.get_param_iterator(*unnamed_args, **named_args)(None))[0]

    def test_glob(self):
        """
        test globbed form
        """
        expected_result = (['DIR/f0.output',
                            'DIR/f0.test',
                            'DIR/f1.output',
                            'DIR/f1.test',
                            'DIR/f2.output',
                            'DIR/f2.test',
                            ],
                           ["test1",
                            "test2",
                            "extra.file"]
                           )
        #
        # simple 1 input, 1 output
        #
        paths = self.do_task_merge(tempdir + "/*",
                                   ["test1",                               # output params
                                    "test2",
                                    "extra.file"])
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_result)

        #
        #   named parameters
        #
        paths = self.do_task_merge(input=tempdir + "/*",
                                   output=["test1",                               # output params
                                           "test2",
                                           "extra.file"])
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_result)

    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """

        unnamed_args = [[output_from("module.func1",       # input params
                                          "module.func2",
                                          "module.func3",
                                          "module.func4",
                                          "module.func5"),
                         tempdir + "/*"],
                        ["test1",                               # output params
                         "test2",
                         "extra.file"],
                        6]                                      # extra params

        expected_results = ([
                            5,
                            ['output4.test', 'output.ignored'],
                            'output1.test',
                            'output2.test',
                            'output3.test',
                            'output.ignored',
                            (2, 'output5.test'),
                            'DIR/f0.output',
                            'DIR/f0.test',
                            'DIR/f1.output',
                            'DIR/f1.test',
                            'DIR/f2.output',
                            'DIR/f2.test'],
                            ['test1',                          # output params
                             'test2',
                             'extra.file'],
                            6)

        # unnamed arguments
        paths = self.do_task_merge(*unnamed_args)
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

        # NAMED ARGUMENTS
        paths = self.do_task_merge(input=unnamed_args[0],
                                   output=unnamed_args[1],
                                   extras=unnamed_args[2:])
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

        paths = self.do_task_merge(output_from(
            "module.func2"), "output", "extra")
        paths = self.do_task_merge(output_from(
            "module.func1", "module.func2"), "output", "extra")

        # single job output consisting of a single file
        paths = self.do_task_merge(output_from("module.func2"), "output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, ('output.ignored', 'output'))

        paths = self.do_task_merge(
            [output_from("module.func2")], "output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, (['output.ignored'], 'output'))

        # single job output consisting of a list
        paths = self.do_task_merge(output_from("module.func4"), "output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, ((2, 'output5.test'), 'output'))

        paths = self.do_task_merge(
            [output_from("module.func4")], "output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, ([(2, 'output5.test')], 'output'))

# =========================================================================================

#   transform_param_factory

# =========================================================================================


class Test_transform_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        touch("%s/f%d.output" % (tempdir, 0))
        for i in range(3):
            touch("%s/f%d.test" % (tempdir, i))
        time.sleep(0.1)
        touch("%s/f%d.output" % (tempdir, 1))
        touch("%s/f%d.output" % (tempdir, 2))

        self.tasks = [t1, t2, t3, t4, t5]
        self.maxDiff = None

    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (tempdir, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (tempdir, i))
        os.removedirs(tempdir)
        pass

    # _____________________________________________________________________________

    #   wrappers

    # _____________________________________________________________________________

    def get_param_iterator(self, *unnamed_args, **named_args):
        #
        # replace function / function names with tasks
        #
        # fake virgin task
        fake_task = task.Task(list_generator_factory,
                              "module.func_fake%d" % randint(1, 1000000))
        fake_task._decorator_transform(*unnamed_args, **named_args)
        fake_task._complete_setup()
        return fake_task.param_generator_func

    def do_task_transform(self, *unnamed_args, **named_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        # extra dereference because we are only interested in the first (only) job
        return list(p1 for (p1, ps) in self.get_param_iterator(*unnamed_args, **named_args)(None))

    def test_simple(self):
        """
        test simple_form
        """
        #
        # simple 1 input, 1 output
        #
        paths = self.do_task_transform("a.test", task.regex("a(.+)"),  r"b\1")

        self.assertEqual(paths,
                         [('a.test', 'b.test')])

    def test_suffix(self):
        """
        test suffix transform with globs
        """
        #
        # simple 1 input, 1 output
        #
        paths = self.do_task_transform(tempdir + "/*.test", task.suffix(".test"),
                                       [".output1", ".output2"], ".output3")

        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             ('DIR/f0.test', ['DIR/f0.output1',
                                              'DIR/f0.output2'], ".output3"),
                             ('DIR/f1.test', ['DIR/f1.output1',
                                              'DIR/f1.output2'], ".output3"),
                             ('DIR/f2.test', ['DIR/f2.output1',
                                              'DIR/f2.output2'], ".output3"),
                         ])

    def test_formatter(self):
        """
        test suffix transform with globs
        """
        #
        # simple 1 input, 1 output
        #
        unnamed_args = [tempdir + "/*.test",
                        task.formatter("/(?P<name>\w+).test$"),
                        ["{path[0]}/{name[0]}.output1{ext[0]}", "{path[0]}/{name[0]}.output2"], "{path[0]}/{name[0]}.output3"]
        expected_results = [
            ('DIR/f0.test', ['DIR/f0.output1.test',
                             'DIR/f0.output2'], "DIR/f0.output3"),
            ('DIR/f1.test', ['DIR/f1.output1.test',
                             'DIR/f1.output2'], "DIR/f1.output3"),
            ('DIR/f2.test', ['DIR/f2.output1.test', 'DIR/f2.output2'], "DIR/f2.output3"), ]
        # unnamed_args                                   ]
        paths = self.do_task_transform(*unnamed_args)
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

        # named args
        paths = self.do_task_transform(
            input=unnamed_args[0], filter=unnamed_args[1], output=unnamed_args[2], extras=unnamed_args[3:])
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

    def test_regex(self):
        """
        test regex transform with globs
        """
        #
        # simple 1 input, 1 output
        #
        unnamed_args = [tempdir + "/*.test",
                        task.regex(r"(.*)\.test"),
                        [r"\1.output1", r"\1.output2"], r"\1.output3"]
        expected_results = [
            ('DIR/f0.test', ['DIR/f0.output1',
                             'DIR/f0.output2'], "DIR/f0.output3"),
            ('DIR/f1.test', ['DIR/f1.output1',
                             'DIR/f1.output2'], "DIR/f1.output3"),
            ('DIR/f2.test', ['DIR/f2.output1', 'DIR/f2.output2'], "DIR/f2.output3"), ]

        # unnamed_args                                   ]
        paths = self.do_task_transform(*unnamed_args)
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

        # named args
        paths = self.do_task_transform(
            input=unnamed_args[0], filter=unnamed_args[1], output=unnamed_args[2], extras=unnamed_args[3:])
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

    def test_inputs(self):
        """
        test transform with inputs in both regex and suffix forms
        """
        #
        # simple 1 input, 1 output
        #
        #
        paths = self.do_task_transform(tempdir + "/*.test", task.regex(r"(.*)\.test"),
                                       task.inputs(r"\1.testwhat"),
                                       [r"\1.output1", r"\1.output2"])

        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             ('DIR/f0.testwhat',
                              ['DIR/f0.output1', 'DIR/f0.output2']),
                             ('DIR/f1.testwhat',
                                 ['DIR/f1.output1', 'DIR/f1.output2']),
                             ('DIR/f2.testwhat',
                                 ['DIR/f2.output1', 'DIR/f2.output2']),
                         ])
        paths = self.do_task_transform(tempdir + "/*.test", task.suffix(".test"),
                                       task.inputs(r"a.testwhat"),
                                       [".output1", ".output2"], ".output3")

        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             ('a.testwhat', ['DIR/f0.output1',
                                             'DIR/f0.output2'], '.output3'),
                             ('a.testwhat', ['DIR/f1.output1',
                                             'DIR/f1.output2'], '.output3'),
                             ('a.testwhat', ['DIR/f2.output1', 'DIR/f2.output2'], '.output3')])
        #
        # add inputs
        #
        #
        unnamed_args = [tempdir + "/*.test", task.regex(r"(.*)\.test"),
                        add_inputs(r"\1.testwhat"),
                        [r"\1.output1", r"\1.output2"]]
        expected_results = [
            (('DIR/f0.test', 'DIR/f0.testwhat'),
             ['DIR/f0.output1', 'DIR/f0.output2']),
            (('DIR/f1.test', 'DIR/f1.testwhat'),
             ['DIR/f1.output1', 'DIR/f1.output2']),
            (('DIR/f2.test', 'DIR/f2.testwhat'),
             ['DIR/f2.output1', 'DIR/f2.output2']),
        ]

        # unnamed_args                                   ]
        paths = self.do_task_transform(*unnamed_args)
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

        # named args
        paths = self.do_task_transform(
            input=unnamed_args[0], filter=unnamed_args[1], add_inputs=unnamed_args[2], output=unnamed_args[3], extras=unnamed_args[4:])
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

        # named args
        paths = self.do_task_transform(
            *unnamed_args[0:2], add_inputs=unnamed_args[2].args, output=unnamed_args[3], extras=unnamed_args[4:])
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

        paths = self.do_task_transform(tempdir + "/*.test", task.suffix(".test"),
                                       add_inputs(r"a.testwhat"),
                                       [".output1", ".output2"], ".output3")

        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             (('DIR/f0.test', 'a.testwhat'),
                              ['DIR/f0.output1', 'DIR/f0.output2'], '.output3'),
                             (('DIR/f1.test', 'a.testwhat'),
                                 ['DIR/f1.output1', 'DIR/f1.output2'], '.output3'),
                             (('DIR/f2.test', 'a.testwhat'), ['DIR/f2.output1', 'DIR/f2.output2'], '.output3')])

    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """

        paths = self.do_task_transform([output_from("module.func1",       # input params
                                                         "module.func2",
                                                         "module.func3",
                                                         "module.func4",
                                                         "module.func5"),
                                        tempdir + "/*.test"],
                                       task.regex(r"(.*)\.test"),
                                       [r"\1.output1", r"\1.output2"], r"\1.output3")
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             ((2, 'output5.test'), [
                              'output5.output1', 'output5.output2'], 'output5.output3'),
                             ('DIR/f0.test', ['DIR/f0.output1',
                                              'DIR/f0.output2'], 'DIR/f0.output3'),
                             ('DIR/f1.test', ['DIR/f1.output1',
                                              'DIR/f1.output2'], 'DIR/f1.output3'),
                             ('DIR/f2.test', ['DIR/f2.output1',
                                              'DIR/f2.output2'], 'DIR/f2.output3'),
                             (['output4.test', 'output.ignored'], [
                                 'output4.output1', 'output4.output2'], 'output4.output3'),
                             ('output1.test', [
                                 'output1.output1', 'output1.output2'], 'output1.output3'),
                             ('output2.test', [
                                 'output2.output1', 'output2.output2'], 'output2.output3'),
                             ('output3.test', [
                                 'output3.output1', 'output3.output2'], 'output3.output3'),
                         ])

        # single job output consisting of a single file
        paths = self.do_task_transform(output_from(
            "module.func2"), task.regex(r"(.*)\..*"),  r"\1.output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [('output.ignored', 'output.output')])

        # Same output if task specified as part of a list of tasks
        paths = self.do_task_transform(
            [output_from("module.func2")], task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [('output.ignored', 'output')])

        # single job output consisting of a list
        paths = self.do_task_transform(output_from(
            "module.func4"), task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [((2, 'output5.test'), 'output')])

        # Same output if task specified as part of a list of tasks
        paths = self.do_task_transform(
            [output_from("module.func4")], task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [((2, 'output5.test'), 'output')])

#
#
# =========================================================================================

#   collate_param_factory

# =========================================================================================


class Test_collate_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        touch("%s/f%d.output" % (tempdir, 0))
        touch("%s/e%d.output" % (tempdir, 0))
        for i in range(3):
            touch("%s/f%d.test" % (tempdir, i))
        for i in range(3):
            touch("%s/e%d.test" % (tempdir, i))
        time.sleep(0.1)
        touch("%s/f%d.output" % (tempdir, 1))
        touch("%s/f%d.output" % (tempdir, 2))
        touch("%s/e%d.output" % (tempdir, 1))
        touch("%s/e%d.output" % (tempdir, 2))

        self.tasks = [t1, t2, t3, t4, t5]

    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (tempdir, i))
            os.unlink("%s/e%d.test" % (tempdir, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (tempdir, i))
            os.unlink("%s/e%d.output" % (tempdir, i))
        os.removedirs(tempdir)
        pass

    # _____________________________________________________________________________

    #   wrappers

    # _____________________________________________________________________________

    def get_param_iterator(self, *unnamed_args, **named_args):
        #
        # replace function / function names with tasks
        #
        # fake virgin task
        fake_task = task.Task(list_generator_factory,
                              "module.func_fake%d" % randint(1, 1000000))
        fake_task._decorator_collate(*unnamed_args, **named_args)
        fake_task._complete_setup()
        return fake_task.param_generator_func

    def do_task_collate(self, *unnamed_args, **named_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        # extra dereference because we are only interested in the first (only) job
        return list(p1 for (p1, ps) in self.get_param_iterator(*unnamed_args, **named_args)(None))

    def test_regex(self):
        """
        test regex collate with globs
        """
        paths = self.do_task_collate(
            tempdir + "/*", task.regex(r"(.*).test$"), r"\1.output")
        self.assertEqual(recursive_replace(paths, tempdir, "DIR"),
                         [
            (('DIR/e0.test',), 'DIR/e0.output'),
            (('DIR/e1.test',), 'DIR/e1.output'),
            (('DIR/e2.test',), 'DIR/e2.output'),
            (('DIR/f0.test',), 'DIR/f0.output'),
            (('DIR/f1.test',), 'DIR/f1.output'),
            (('DIR/f2.test',), 'DIR/f2.output'),
        ]
        )
        paths = self.do_task_collate(
            tempdir + "/*", task.regex("(.*).test$"), task.inputs(r"\1.input2"), r"combined.output")
        self.assertEqual(recursive_replace(paths, tempdir, "DIR"),
                         [((
                             'DIR/e0.input2',
                             'DIR/e1.input2',
                             'DIR/e2.input2',
                             'DIR/f0.input2',
                             'DIR/f1.input2',
                             'DIR/f2.input2',
                         ), 'combined.output')])

        #
        # simple 1 input, 1 output
        #
        paths = self.do_task_collate(tempdir + "/*.test", task.regex(r"(.*/[ef]).*\.test"),
                                     [r"\1.output1", r"\1.output2"], r"\1.extra")

        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             (
                                 ('DIR/e0.test', 'DIR/e1.test',
                                  'DIR/e2.test'),      # input
                                 # output
                                 ['DIR/e.output1', 'DIR/e.output2'],
                                 'DIR/e.extra'                                       # extra
                             ),
                             (
                                 ('DIR/f0.test', 'DIR/f1.test',
                                  'DIR/f2.test'),      # input
                                 # output
                                 ['DIR/f.output1', 'DIR/f.output2'],
                                 'DIR/f.extra'                                       # extra
                             )
                         ])

    def test_inputs(self):
        """
        test collate with task.inputs
        """
        #
        # collating using inputs
        #
        paths = self.do_task_collate(tempdir + "/*.test", task.regex(r"(.*/[ef])(.).*\.test"),
                                     task.inputs(r"\1\2.whoopee"),  [r"\1.output1", r"\1.output2"], r"\1.extra")

        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             (
                                 ('DIR/e0.whoopee', 'DIR/e1.whoopee',
                                  'DIR/e2.whoopee'),      # input
                                 # output
                                 ['DIR/e.output1', 'DIR/e.output2'],
                                 'DIR/e.extra'                                                # extra
                             ),
                             (
                                 ('DIR/f0.whoopee', 'DIR/f1.whoopee',
                                  'DIR/f2.whoopee'),      # input
                                 # output
                                 ['DIR/f.output1', 'DIR/f.output2'],
                                 'DIR/f.extra'                                                # extra
                             )
                         ])
        #
        # collating using inputs where some files do not match regex
        #
        paths = self.do_task_collate(tempdir + "/*.test", task.regex(r"(.*/f)[a-z0-9]+\.test"),
                                     task.inputs(r"\1.whoopee"),  [r"\1.output1", r"\1.output2"], r"\1.extra")

        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [(('DIR/f.whoopee',), ['DIR/f.output1', 'DIR/f.output2'], 'DIR/f.extra')])

        #
        # collating using inputs where multiple copies of the same input names are removed
        #
        paths = self.do_task_collate(tempdir + "/*.test", task.regex(r"(.*/[ef])[a-z0-9]+\.test"),
                                     task.inputs(r"\1.whoopee"),  [r"\1.output1", r"\1.output2"], r"\1.extra")

        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             (
                                 # input
                                 ('DIR/e.whoopee',),
                                 # output
                                 ['DIR/e.output1', 'DIR/e.output2'],
                                 'DIR/e.extra'                                      # extra
                             ),
                             (
                                 # input
                                 ('DIR/f.whoopee',),
                                 # output
                                 ['DIR/f.output1', 'DIR/f.output2'],
                                 'DIR/f.extra'                                      # extra
                             )
                         ])

        #
        #   test python set object. Note that set is constructed with the results of the substitution
        #

        unnamed_args = [tempdir + "/*.test",
                        task.regex(r"(.*/[ef])[a-z0-9]+\.test"),
                        task.inputs(r"\1.whoopee"),
                        set([r"\1.output1", r"\1.output2", tempdir + "/e.output2"]),
                        r"\1.extra"]
        expected_results = [
            (
                # input
                ('DIR/e.whoopee',),
                # output
                set(['DIR/e.output1', 'DIR/e.output2']),
                'DIR/e.extra'                                      # extra
            ),
            (
                # input
                ('DIR/f.whoopee',),
                set(['DIR/f.output1', 'DIR/f.output2',
                     'DIR/e.output2']),                # output
                'DIR/f.extra'                                      # extra
            )
        ]

        # unnamed_args                                   ]
        paths = self.do_task_collate(*unnamed_args)
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

        # named args
        paths = self.do_task_collate(input=unnamed_args[0], filter=unnamed_args[1],
                                     replace_inputs=unnamed_args[2], output=unnamed_args[3], extras=unnamed_args[4:])
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

        # named args
        paths = self.do_task_collate(
            *unnamed_args[0:2], replace_inputs=unnamed_args[2], output=unnamed_args[3], extras=unnamed_args[4:])
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

        # named args
        paths = self.do_task_collate(
            *unnamed_args[0:2], replace_inputs=unnamed_args[2].args[0], output=unnamed_args[3], extras=unnamed_args[4:])
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths, expected_results)

    def test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """

        paths = self.do_task_collate([output_from("module.func1",       # input params
                                                       "module.func2",
                                                       "module.func3",
                                                       "module.func4",
                                                       "module.func5"),
                                      tempdir + "/*.test"],
                                     task.regex(r"(.*[oef])[a-z0-9]+\.test"),
                                     [r"\1.output1", r"\1.output2"], r"\1.extra")
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             (('DIR/e0.test', 'DIR/e1.test', 'DIR/e2.test'),
                              ['DIR/e.output1', 'DIR/e.output2'], 'DIR/e.extra'),
                             (('DIR/f0.test', 'DIR/f1.test', 'DIR/f2.test'),
                                 ['DIR/f.output1', 'DIR/f.output2'], 'DIR/f.extra'),
                             (((2, 'output5.test'), ['output4.test', 'output.ignored'], 'output1.test', 'output2.test', 'output3.test'), [
                                 'o.output1', 'o.output2'], 'o.extra')
                         ])

        paths = self.do_task_collate([output_from("module.func1",       # input params
                                                       "module.func2",
                                                       "module.func3",
                                                       "module.func4",
                                                       "module.func5"),
                                      tempdir + "/*.test"],
                                     task.regex(r"(.*[oef])[a-z0-9]+\.test"),
                                     task.inputs(r"\1.whoopee"),
                                     [r"\1.output1", r"\1.output2"], r"\1.extra")
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             (
                                 # input
                                 ("DIR/e.whoopee",),
                                 # output
                                 ["DIR/e.output1", "DIR/e.output2"],
                                 "DIR/e.extra"                                   # extra
                             ),
                             (
                                 # input
                                 ("DIR/f.whoopee",),
                                 # output
                                 ["DIR/f.output1", "DIR/f.output2"],
                                 "DIR/f.extra"                                   # extra
                             ),
                             (
                                 # input
                                 ("o.whoopee",),
                                 # output
                                 ["o.output1", "o.output2"],
                                 "o.extra"                                       # extra
                             )
                         ])

        # single job output consisting of a single file
        paths = self.do_task_collate(output_from(
            "module.func2"), task.regex(r"(.*)\..*"),  r"\1.output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        # print dumps(paths, indent = 4)
        self.assertEqual(paths, [(('output.ignored',), 'output.output')])

        # Same output if task specified as part of a list of tasks
        paths = self.do_task_collate(
            [output_from("module.func2")], task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [(('output.ignored',), 'output')])

        #
        # single job output consisting of a list
        #
        paths = self.do_task_collate(output_from(
            "module.func4"), task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [(((2, 'output5.test'),), 'output')])

        # Same output if task specified as part of a list of tasks
        paths = self.do_task_collate(
            [output_from("module.func4")], task.regex(r"(.*)\..*"),  "output")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths, [(((2, 'output5.test'),), 'output')])

# =========================================================================================

#   files_param_factory

# =========================================================================================


class Test_files_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        touch("%s/f%d.output" % (tempdir, 0))
        for i in range(3):
            touch("%s/f%d.test" % (tempdir, i))
        time.sleep(0.1)
        touch("%s/f%d.output" % (tempdir, 1))
        touch("%s/f%d.output" % (tempdir, 2))

        self.tasks = [t1, t2, t3, t4, t5]

    def tearDown(self):
        for i in range(3):
            os.unlink("%s/f%d.test" % (tempdir, i))
        for i in range(3):
            os.unlink("%s/f%d.output" % (tempdir, i))
        os.removedirs(tempdir)
        pass

    def get_param_iterator(self, *unnamed_args, **named_args):
        #
        # replace function / function names with tasks
        #
        # fake virgin task
        fake_task = task.Task(list_generator_factory,
                              "module.func_fake%d" % randint(1, 1000000))
        fake_task._decorator_files(*unnamed_args, **named_args)
        fake_task._complete_setup()
        return fake_task.param_generator_func

    def files(self, *unnamed_args, **named_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        return list(p1 for (p1, ps) in self.get_param_iterator(*unnamed_args, **named_args)(None))

    def _test_simple(self):
        """
        test simple_form
        """
        #
        # simple 1 input, 1 output
        #
        paths = self.files("a.test", "b.test")
        self.assertEqual(paths,
                         [('a.test', 'b.test')])

    def test_glob(self):
        """
        test globbed form
        """
        #
        # Replacement of globs in first parameter
        #
        paths = self.files(tempdir + "/*", "a.test", "b.test")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths,
                         [
                             (
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
                             )
                         ])
        #
        # Replacement of globs in first parameter in-place
        #
        paths = self.files([tempdir + "/*", "robbie.test"], "a.test", "b.test")
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths,
                         [
                             (
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
                             )
                         ])
        #
        # No Replacement of globs in other parameter of multi-job task
        #
        paths = self.files([[[tempdir + "/*", "robbie.test"],
                             "a.test", "b.test"], ["a.test", ["b.test", 2], "a.*"]])
        paths = recursive_replace(recursive_replace(
            paths, tempdir, "DIR"), exe_path, "DIR_E")
        self.assertEqual(paths,
                         [
                             (
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
                             ),
                             ("a.test", ["b.test", 2], "a.*")
                         ])

    def _test_filelist(self):
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
        file_list = [[["DIR/e0.test", set([5, "DIR/e1.test"]), "DIR/e2.test"], [
            "DIR/f0.test", "DIR/f1.test", "DIR/f2.test"]]]
        paths = self.files(*file_list)
        self.assertEqual(paths, [
            ("DIR/e0.test", set([5, "DIR/e1.test"]), "DIR/e2.test"),
            ("DIR/f0.test", "DIR/f1.test", "DIR/f2.test"),
        ])

        # bad list: missing list enclosure
        file_list = [["DIR/f0.test", "DIR/f1.test", "DIR/f2.test"]]
        self.assertRaises(error_task_files, self.files, *file_list)

        # bad list: missing io
        file_list = [[[1, 2], ["DIR/e0.test", [5, "DIR/e1.test"],
                               "DIR/e2.test"], ["DIR/f0.test", "DIR/f1.test", "DIR/f2.test"]]]
        self.assertRaises(error_task_files, self.files, *file_list)

    def _test_tasks(self):
        """
        test if can use tasks to specify dependencies
        """
        #
        #   substitution of tasks
        #
        paths = self.files(output_from("module.func1",
                                            "module.func2",
                                            "module.func3",
                                            "module.func4",
                                            "module.func5"), "rob.test", "b.test")
        self.assertEqual(paths, [([5, ['output4.test', 'output.ignored'], 'output1.test', 'output2.test', 'output3.test',
                                   'output.ignored', (2, 'output5.test')],
                                  'rob.test',
                                  'b.test')])

        #
        #   nested in place substitution of tasks
        #
        paths = self.files([output_from("module.func1",
                                             "module.func2",
                                             "module.func3",
                                             "module.func4",
                                             "module.func5"),
                            "robbie.test"], "a.test", "b.test")
        self.assertEqual(paths,
                         [([5, ['output4.test', 'output.ignored'], 'output1.test', 'output2.test', 'output3.test', 'output.ignored', (2, 'output5.test'), 'robbie.test'], 'a.test', 'b.test')])

        # single job output consisting of a single file
        paths = self.files(output_from("module.func2"), "output", "extra")
        self.assertEqual(paths, [('output.ignored', 'output', 'extra')])

        # Different output if task specified as part of a list of tasks
        paths = self.files([output_from("module.func2"),
                            output_from("module.func2")], "output", "extra")
        self.assertEqual(
            paths, [(['output.ignored', 'output.ignored'], 'output', 'extra')])

        # single job output consisting of a list
        paths = self.files(output_from("module.func4"), "output", "extra")
        self.assertEqual(paths, [((2, 'output5.test'), 'output', 'extra')])

        # Same output if task specified as part of a list of tasks
        paths = self.files([output_from("module.func4"),
                            output_from("module.func2")], "output", "extra")
        self.assertEqual(
            paths,  [([(2, 'output5.test'), 'output.ignored'], 'output', 'extra')])


#
# =========================================================================================

#   product_param_factory

# =========================================================================================

class Test_product_param_factory(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        touch("%s/a.test1" % (tempdir))
        touch("%s/b.test1" % (tempdir))
        touch("%s/c.test2" % (tempdir))
        touch("%s/d.test2" % (tempdir))
        touch("%s/a.testwhat1" % (tempdir))
        touch("%s/b.testwhat1" % (tempdir))
        touch("%s/c.testwhat2" % (tempdir))
        touch("%s/d.testwhat2" % (tempdir))
        time.sleep(0.1)
        touch("%s/a.b.output" % (tempdir))
        touch("%s/a.c.output" % (tempdir))
        touch("%s/b.c.output" % (tempdir))
        touch("%s/b.d.output" % (tempdir))

        self.tasks = [t1, t2, t3, t4, t5]
        self.maxDiff = None

    def tearDown(self):
        os.unlink("%s/a.test1" % (tempdir))
        os.unlink("%s/b.test1" % (tempdir))
        os.unlink("%s/c.test2" % (tempdir))
        os.unlink("%s/d.test2" % (tempdir))
        os.unlink("%s/a.testwhat1" % (tempdir))
        os.unlink("%s/b.testwhat1" % (tempdir))
        os.unlink("%s/c.testwhat2" % (tempdir))
        os.unlink("%s/d.testwhat2" % (tempdir))
        os.unlink("%s/a.b.output" % (tempdir))
        os.unlink("%s/a.c.output" % (tempdir))
        os.unlink("%s/b.c.output" % (tempdir))
        os.unlink("%s/b.d.output" % (tempdir))

        os.removedirs(tempdir)
        pass

    # _____________________________________________________________________________

    #   wrappers

    # _____________________________________________________________________________

    def get_param_iterator(self, *unnamed_args, **named_args):
        #
        # replace function / function names with tasks
        #
        # fake virgin task
        fake_task = task.Task(list_generator_factory,
                              "module.func_fake%d" % randint(1, 1000000))
        fake_task._decorator_product(*unnamed_args, **named_args)
        fake_task._complete_setup()
        return fake_task.param_generator_func

    def do_task_product(self, *unnamed_args, **named_args):
        """
        This extra function is to simulate the forwarding from the decorator to
            the task creation function
        """
        # extra dereference because we are only interested in the first (only) job
        return list(p1 for (p1, ps) in self.get_param_iterator(*unnamed_args, **named_args)(None))

    def test_simple(self):
        """
        test simple_form
        """
        #
        # simple 1 input, 1 output
        #
        args = [[tempdir + "/a.test1", tempdir + "/b.test1"],
                task.formatter("(?:.+/)?(?P<ID>\w+)\.(.+)"),
                [tempdir + "/c.test2", tempdir + "/d.test2", tempdir + "/e.ignore"],
                task.formatter("(?:.+/)?(?P<ID>\w+)\.(test2)"),
                r"{path[0][0]}/{ID[0][0]}.{1[1][0]}.output"]
        expected_result = [
            (('DIR/a.test1', 'DIR/c.test2'), 'DIR/a.c.output'),
            (('DIR/a.test1', 'DIR/d.test2'), 'DIR/a.d.output'),
            (('DIR/b.test1', 'DIR/c.test2'), 'DIR/b.c.output'),
            (('DIR/b.test1', 'DIR/d.test2'), 'DIR/b.d.output')
        ]
        paths = self.do_task_product(*args)
        self.assertEqual(recursive_replace(
            paths, tempdir, "DIR"), expected_result)

        # named parameters
        paths = self.do_task_product(input=args[0], filter=args[1],
                                     input2=args[2], filter2=args[3],
                                     output=args[4])
        self.assertEqual(recursive_replace(
            paths, tempdir, "DIR"), expected_result)

        # named parameters
        paths = self.do_task_product(*args[0:2],
                                     input2=args[2], filter2=args[3],
                                     output=args[4])
        self.assertEqual(recursive_replace(
            paths, tempdir, "DIR"), expected_result)

        paths = self.do_task_product(*args[0:4],
                                     output=args[4])
        self.assertEqual(recursive_replace(
            paths, tempdir, "DIR"), expected_result)

    def test_inputs(self):
        """
        test transform with inputs in both regex and suffix forms
        """
        #
        # (replace) inputs
        #
        #
        paths = self.do_task_product([tempdir + "/a.test1", tempdir + "/b.test1"],                          task.formatter("(?:.+/)?(?P<ID>\w+)\.(.+)"),
                                     [tempdir + "/c.test2", tempdir + "/d.test2", tempdir +
                                         "/e.ignore"], task.formatter("(?:.+/)?(?P<ID>\w+)\.(test2)"),
                                     task.inputs(
                                         ("{path[0][0]}/{basename[0][0]}.testwhat1", "{path[1][0]}/{basename[1][0]}.testwhat2")),
                                     r"{path[0][0]}/{ID[0][0]}.{1[1][0]}.output")
        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             (('DIR/a.testwhat1', 'DIR/c.testwhat2'), 'DIR/a.c.output'),
                             (('DIR/a.testwhat1', 'DIR/d.testwhat2'), 'DIR/a.d.output'),
                             (('DIR/b.testwhat1', 'DIR/c.testwhat2'), 'DIR/b.c.output'),
                             (('DIR/b.testwhat1', 'DIR/d.testwhat2'), 'DIR/b.d.output')
                         ]
                         )
        #
        # add inputs
        #
        #
        paths = self.do_task_product([tempdir + "/a.test1", tempdir + "/b.test1"],                          task.formatter("(?:.+/)?(?P<ID>\w+)\.(.+)"),
                                     [tempdir + "/c.test2", tempdir + "/d.test2", tempdir +
                                         "/e.ignore"], task.formatter("(?:.+/)?(?P<ID>\w+)\.(test2)"),
                                     add_inputs(
                                         "{path[0][0]}/{basename[0][0]}.testwhat1", "{path[1][0]}/{basename[1][0]}.testwhat2", ),
                                     r"{path[0][0]}/{ID[0][0]}.{1[1][0]}.output")

        paths = recursive_replace(paths, tempdir, "DIR")
        self.assertEqual(paths,
                         [
                             ((('DIR/a.test1', 'DIR/c.test2'), 'DIR/a.testwhat1',
                               'DIR/c.testwhat2'), 'DIR/a.c.output'),
                             ((('DIR/a.test1', 'DIR/d.test2'), 'DIR/a.testwhat1',
                               'DIR/d.testwhat2'), 'DIR/a.d.output'),
                             ((('DIR/b.test1', 'DIR/c.test2'), 'DIR/b.testwhat1',
                               'DIR/c.testwhat2'), 'DIR/b.c.output'),
                             ((('DIR/b.test1', 'DIR/d.test2'), 'DIR/b.testwhat1',
                               'DIR/d.testwhat2'), 'DIR/b.d.output')
                         ]
                         )


if __name__ == '__main__':
    unittest.main()
