#!/usr/bin/env python
"""

    exceptions.py

"""

################################################################################
#
#   exceptions.py
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

import sys
import os
from collections import defaultdict


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Exceptions


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

# if __name__ != '__main__':
#    import task

class error_task(Exception):
    def __init__(self, *errmsg):
        Exception.__init__(self, *errmsg)

        # list of associated tasks
        self.tasks = set()

        # error message
        self.main_msg = ""

    def get_main_msg(self):
        """
        Make main message with lists of task names
        Prefix with new lines for added emphasis
        """
        # turn tasks names into 'def xxx(...): format
        task_names = "\n".join("task = %r" % t._name for t in self.tasks)
        if len(self.main_msg):
            return "\n\n" + self.main_msg + " for\n\n%s\n" % task_names
        else:
            return "\n\n%s\n" % task_names

    def __str__(self):
        # indent
        msg = self.get_main_msg() + " ".join(map(str, self.args))
        return "    " + msg.replace("\n", "\n    ")

    def specify_task(self, task, main_msg):
        self.tasks.add(task)
        self.main_msg = main_msg
        return self


class error_task_contruction(error_task):
    """
    Exceptions when contructing pipeline tasks
    """

    def __init__(self, task, main_msg, *errmsg):
        error_task.__init__(self, *errmsg)
        self.specify_task(task, main_msg)


class RethrownJobError(error_task):
    """
    Wrap up one or more exceptions rethrown across process boundaries

        See multiprocessor.Server.handle_request/serve_client for an analogous function
    """

    def __init__(self, job_exceptions=[]):
        error_task.__init__(self)
        self.job_exceptions = list(job_exceptions)

    def __len__(self):
        return len(self.job_exceptions)

    def append(self, job_exception):
        self.job_exceptions.append(job_exception)

    def task_to_func_name(self, task_name):
        if "mkdir " in task_name:
            return task_name

        return "def %s(...):" % task_name.replace("__main__.", "")

    def get_nth_exception_str(self, nn=-1):
        if nn == -1:
            nn = len(self.job_exceptions) - 1
        task_name, job_name, exception_name, exception_value, exception_stack = self.job_exceptions[
            nn]
        message = "\nException #%d\n" % (nn + 1)
        message += "  '%s%s' raised in ...\n" % (exception_name, exception_value)
        if task_name:
            message += "   Task = %s\n   %s\n\n" % (self.task_to_func_name(task_name),
                                                    job_name)
        message += "%s\n" % (exception_stack, )
        return message.replace("\n", "\n    ")

    def __str__(self):
        message = ["\nOriginal exception%s:\n" %
                   ("s" if len(self.job_exceptions) > 1 else "")]
        for ii in range(len(self.job_exceptions)):
            message += self.get_nth_exception_str(ii)
        #
        #   For each exception:
        #       turn original exception stack message into an indented string
        #
        return (self.get_main_msg()).replace("\n", "\n    ") + "".join(message)


class error_input_file_does_not_match(error_task):
    pass


class fatal_error_input_file_does_not_match(error_task):
    pass


class task_FilesArgumentsError(error_task):
    pass


class task_FilesreArgumentsError(error_task):
    pass


class MissingInputFileError(error_task):
    pass


class JobSignalledBreak(error_task):
    pass


class JobSignalledSuspend(error_task):
    pass


class JobSignalledResume(error_task):
    pass


class JobFailed(error_task):
    pass


class PostTaskArgumentError(error_task):
    pass


class JobsLimitArgumentError(error_task):
    pass


class error_task_get_output(error_task_contruction):
    pass


class error_task_transform_inputs_multiple_args(error_task_contruction):
    pass


class error_task_transform(error_task_contruction):
    pass


class error_task_product(error_task_contruction):
    pass


class error_task_mkdir(error_task_contruction):
    pass


class error_task_permutations(error_task_contruction):
    pass


class error_task_combinations(error_task_contruction):
    pass


class error_task_combinations_with_replacement(error_task_contruction):
    pass


class error_task_merge(error_task_contruction):
    pass


class error_task_subdivide(error_task_contruction):
    pass


class error_task_originate(error_task_contruction):
    pass


class error_task_collate(error_task_contruction):
    pass


class error_task_collate_inputs_multiple_args(error_task_contruction):
    pass


class error_task_split(error_task_contruction):
    pass


class error_task_files_re(error_task_contruction):
    pass


class error_task_files(error_task_contruction):
    pass


class error_task_parallel(error_task_contruction):
    pass


class error_making_directory(error_task):
    pass


class error_duplicate_task_name(error_task):
    pass


class error_decorator_args(error_task):
    pass


class error_task_name_lookup_failed(error_task):
    pass


class error_task_decorator_takes_no_args(error_task):
    pass


class error_function_is_not_a_task(error_task):
    pass


class error_ambiguous_task(error_task):
    pass


class error_not_a_pipeline(error_task):
    pass


class error_circular_dependencies(error_task):
    pass


class error_not_a_directory(error_task):
    pass


class error_missing_output(error_task):
    pass


class error_job_signalled_interrupt(error_task):
    pass


class error_node_not_task(error_task):
    pass


class error_missing_runtime_parameter(error_task):
    pass


class error_unescaped_regular_expression_forms(error_task):
    pass


class error_checksum_level(error_task):
    pass


class error_missing_args(error_task):
    pass


class error_too_many_args(error_task):
    pass


class error_inputs_multiple_args(error_task):
    pass


class error_set_input(error_task):
    pass


class error_set_output(error_task):
    pass


class error_no_head_tasks(error_task):
    pass


class error_no_tail_tasks(error_task):
    pass


class error_executable_str(error_task):
    pass


class error_extras_wrong_type(error_task):
    pass


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Testing
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
if __name__ == '__main__':
    import unittest

    #
    #   minimal task object to test exceptions
    #
    class task:
        class Task (object):
            """
            dummy task
            """
            _action_mkdir = 1

            def __init__(self, _name,  _action_type=0):
                self._action_type = _action_type
                self._name = _name

    class Test_exceptions(unittest.TestCase):

        #       self.assertEqual(self.seq, range(10))
        #       self.assert_(element in self.seq)
        #       self.assertRaises(ValueError, random.sample, self.seq, 20)

        def test_error_task(self):
            """
                test
            """
            fake_task1 = task.Task("task1")
            fake_task2 = task.Task("task2")
            fake_mkdir_task3 = task.Task("task3", task.Task._action_mkdir)
            fake_mkdir_task4 = task.Task("task4", task.Task._action_mkdir)
            e = error_task()
            e.specify_task(fake_task1, "Some message 0")
            e.specify_task(fake_task2, "Some message 1")
            e.specify_task(fake_mkdir_task3, "Some message 2")
            e.specify_task(fake_mkdir_task4, "Some message 3")
            self.assertEqual(str(e),
                             """

    Some message 3 for

    'def task1(...):'
    'def task2(...):'
    task3
    task4
    """)

        def test_RethrownJobError(self):
            """
                test
            """
            #job_name, exception_name, exception_value, exception_stack
            exception_data = [
                [
                    "task1",
                    "[[temp_branching_dir/a.2, a.1] -> temp_branching_dir/a.3]",
                    "ruffus.task.MissingInputFileError",
                    "(instance value)",
                    "Traceback (most recent call last):\n  File \"what.file.py\", line 333, in some_func\n  somecode(sfasf)\n"
                ],
                [
                    "task1",
                    "[None -> [temp_branching_dir/a.1, temp_branching_dir/b.1, temp_branching_dir/c.1]]",
                    "exceptions.ZeroDivisionError:",
                    "(1)",
                    "Traceback (most recent call last):\n  File \"anotherfile.py\", line 345, in other_func\n  badcode(rotten)\n"
                ]

            ]
            e = RethrownJobError(exception_data)
            fake_task1 = task.Task("task1")
            fake_task2 = task.Task("task2")
            fake_mkdir_task3 = task.Task("task3", task.Task._action_mkdir)
            fake_mkdir_task4 = task.Task("task4", task.Task._action_mkdir)
            e.specify_task(fake_task1, "Exceptions running jobs")
            e.specify_task(fake_task2, "Exceptions running jobs")
            e.specify_task(fake_mkdir_task3, "Exceptions running jobs")
            e.specify_task(fake_mkdir_task4, "Exceptions running jobs")
            self.assertEqual(str(e),
                             """

    Exceptions running jobs for

    'def task1(...):'
    'def task2(...):'
    task3
    task4

    Original exceptions:

    Exception #1
    ruffus.task.MissingInputFileError(instance value):
    for task1.[[temp_branching_dir/a.2, a.1] -> temp_branching_dir/a.3]

    Traceback (most recent call last):
      File "what.file.py", line 333, in some_func
      somecode(sfasf)


    Exception #2
    exceptions.ZeroDivisionError:(1):
    for task1.[None -> [temp_branching_dir/a.1, temp_branching_dir/b.1, temp_branching_dir/c.1]]

    Traceback (most recent call last):
      File "anotherfile.py", line 345, in other_func
      badcode(rotten)

    """)


#
#   debug code not run if called as a module
#
if __name__ == '__main__':
    if sys.argv.count("--debug"):
        sys.argv.remove("--debug")
    unittest.main()
