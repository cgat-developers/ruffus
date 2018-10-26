#!/usr/bin/env python
from __future__ import print_function
from ruffus.ruffus_utility import *
from ruffus import *

################################################################################
#
#   test_ruffus_utility_parse_task_arguments.py
#
#################################################################################
"""
    test_ruffus_utility.py
"""

import unittest

import os
import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# _________________________________________________________________________________________

#   Test_parse_transform_args

# _________________________________________________________________________________________

class Test_parse_transform_args (unittest.TestCase):

    def test_parse_transform_args(self):
        expected_arguments = ["input", "filter",
                              "modify_inputs", "output", "extras"]

        empty_unnamed_arguments = []
        empty_named_arguments = {}
        orig_unnamed_arguments = [
            "*.txt", suffix(".txt"), ".result", 1, 2, 3, 4]
        task_description = "@transform(%s)\ndef myfunc(...)\n"
        expected_results = {'input': orig_unnamed_arguments[0],
                            'filter': orig_unnamed_arguments[1],
                            'output': orig_unnamed_arguments[2],
                            'extras': orig_unnamed_arguments[3:],
                            'named_extras': {},
                            'modify_inputs_mode': 2,
                            'modify_inputs': None}
        add_inputs_expected_results = {'input': orig_unnamed_arguments[0],
                                       'filter': orig_unnamed_arguments[1],
                                       'output': orig_unnamed_arguments[2],
                                       'extras': orig_unnamed_arguments[3:],
                                       'named_extras': {},
                                       'modify_inputs_mode': 0,
                                       'modify_inputs': ("a.test", "b.test")}
        replace_inputs_expected_results = {'input': orig_unnamed_arguments[0],
                                           'filter': orig_unnamed_arguments[1],
                                           'output': orig_unnamed_arguments[2],
                                           'extras': orig_unnamed_arguments[3:],
                                           'named_extras': {},
                                           'modify_inputs_mode': 1,
                                           'modify_inputs': ("a.test", "b.test")}

        # Error: empty list
        with self.assertRaises(error_missing_args):
            parse_task_arguments(
                empty_named_arguments, empty_named_arguments, expected_arguments, task_description)

        # parse complete correctly
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {}, expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # Error: missing argument
        unnamed_arguments = orig_unnamed_arguments[0:1]
        with self.assertRaises(error_missing_args):
            results = parse_task_arguments(unnamed_arguments,
                                           {}, expected_arguments, task_description)

        # parse almost complete and rescued with named parameter
        unnamed_arguments = orig_unnamed_arguments[0:2]
        results = parse_task_arguments(unnamed_arguments,
                                       {'output': orig_unnamed_arguments[2],
                                        'extras': orig_unnamed_arguments[3:]},
                                       expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # All named parameters
        results = parse_task_arguments([],
                                       {'input': orig_unnamed_arguments[0],
                                        'filter': orig_unnamed_arguments[1],
                                        'output': orig_unnamed_arguments[2],
                                        'extras': orig_unnamed_arguments[3:],
                                        },
                                       expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # filter not regex suffix or formatter
        with self.assertRaises(TypeError):
            results = parse_task_arguments([],
                                           {'input': orig_unnamed_arguments[0],
                                            'filter': "a",
                                            'output': orig_unnamed_arguments[2],
                                            'extras': orig_unnamed_arguments[3:],
                                            },
                                           expected_arguments, task_description)

        # Error: Unknown named arguments
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments([],
                                           {'input': orig_unnamed_arguments[0],
                                            'filter': orig_unnamed_arguments[1],
                                            'output': orig_unnamed_arguments[2],
                                            'what': orig_unnamed_arguments[3:]
                                            },
                                           expected_arguments, task_description)

        # Error: Duplicate named arguments
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {'input': orig_unnamed_arguments[0],
                                            'extras': orig_unnamed_arguments[3:],
                                            'named_extras': {},
                                            },
                                           expected_arguments, task_description)

        # add_inputs correct via named
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"add_inputs": ("a.test", "b.test")}, expected_arguments, task_description)
        self.assertEqual(results, add_inputs_expected_results)

        # add_inputs correct via named and paranoid add_inputs wrapping
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"add_inputs": add_inputs("a.test", "b.test")}, expected_arguments, task_description)
        self.assertEqual(results, add_inputs_expected_results)

        # add_inputs correct via unnamed
        unnamed_arguments = list(orig_unnamed_arguments)
        unnamed_arguments.insert(2, add_inputs("a.test", "b.test"))
        results = parse_task_arguments(unnamed_arguments, {},
                                       expected_arguments, task_description)
        self.assertEqual(results, add_inputs_expected_results)

        # replace_inputs correct via named
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"replace_inputs": ("a.test", "b.test")}, expected_arguments, task_description)
        self.assertEqual(results, replace_inputs_expected_results)

        # replace_inputs correct via named and paranoid inputs() wrapping
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"replace_inputs": inputs(("a.test", "b.test"))}, expected_arguments, task_description)
        self.assertEqual(results, replace_inputs_expected_results)

        # replace_inputs correct via unnamed
        unnamed_arguments = list(orig_unnamed_arguments)
        unnamed_arguments.insert(2, inputs(("a.test", "b.test")))
        results = parse_task_arguments(unnamed_arguments, {},
                                       expected_arguments, task_description)
        self.assertEqual(results, replace_inputs_expected_results)

        # Error: both add_inputs and replace_inputs via named
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {"replace_inputs": ("a.test", "b.test"),
                                            "add_inputs": ("a.test", "b.test")}, expected_arguments, task_description)

        # Error: both add_inputs and replace_inputs via named / unnamed
        with self.assertRaises(error_too_many_args):
            unnamed_arguments = list(orig_unnamed_arguments)
            unnamed_arguments.insert(2, inputs(("a.test", "b.test")))
            results = parse_task_arguments(unnamed_arguments, {"add_inputs": ("a.test", "b.test")},
                                           expected_arguments, task_description)

        # Error: both add_inputs and replace_inputs via named / unnamed
        with self.assertRaises(error_too_many_args):
            unnamed_arguments = list(orig_unnamed_arguments)
            unnamed_arguments.insert(2, add_inputs("a.test", "b.test"))
            results = parse_task_arguments(unnamed_arguments, {"replace_inputs": ("a.test", "b.test")},
                                           expected_arguments, task_description)

        # Error: wrong number of arguments
        with self.assertRaises(error_inputs_multiple_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {"replace_inputs": inputs("a.test", "b.test")}, expected_arguments, task_description)

        with self.assertRaises(error_inputs_multiple_args):
            unnamed_arguments = orig_unnamed_arguments[0:2] + [
                inputs("a.test", "b.test")] + orig_unnamed_arguments[2:]
            results = parse_task_arguments(
                unnamed_arguments, {}, expected_arguments, task_description)

        # Error: no arguments
        with self.assertRaises(error_inputs_multiple_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {"replace_inputs": inputs()}, expected_arguments, task_description)


# ________________________________________________________________________________________________________

#   Test_parse_product_args

# ________________________________________________________________________________________________________
class Test_parse_product_args (unittest.TestCase):
    """
    Make sure (input, filter, input2, filter2, input3, filter3,..., output, extras...) works
    for @product
    """

    def test_parse_product_args(self):
        self.maxDiff = None
        expected_arguments = ["input", "filter",
                              "inputN", "modify_inputs", "output", "extras"]

        empty_unnamed_arguments = []
        empty_named_arguments = {}
        orig_unnamed_arguments = ["*.txt", formatter(".txt"), "*.contig", formatter(
        ), "*.genome", formatter(), "{basename[0][0]}_{basename[1][0]}.result", 1, 2, 3, 4]
        task_description = "@product(%s)\ndef myfunc(...)\n"
        expected_results = {'input': [orig_unnamed_arguments[0], orig_unnamed_arguments[2], orig_unnamed_arguments[4]],
                            'filter': [orig_unnamed_arguments[1], orig_unnamed_arguments[3], orig_unnamed_arguments[5]],
                            'output': orig_unnamed_arguments[6],
                            'extras': orig_unnamed_arguments[7:],
                            'named_extras': {},
                            'modify_inputs_mode': 2,
                            'modify_inputs': None}
        add_inputs_expected_results = {'input': [orig_unnamed_arguments[0], orig_unnamed_arguments[2], orig_unnamed_arguments[4]],
                                       'filter': [orig_unnamed_arguments[1], orig_unnamed_arguments[3], orig_unnamed_arguments[5]],
                                       'output': orig_unnamed_arguments[6],
                                       'extras': orig_unnamed_arguments[7:],
                                       'named_extras': {},
                                       'modify_inputs_mode': 0,
                                       'modify_inputs': ("a.test", "b.test")}
        replace_inputs_expected_results = {'input': [orig_unnamed_arguments[0], orig_unnamed_arguments[2], orig_unnamed_arguments[4]],
                                           'filter': [orig_unnamed_arguments[1], orig_unnamed_arguments[3], orig_unnamed_arguments[5]],
                                           'output': orig_unnamed_arguments[6],
                                           'extras': orig_unnamed_arguments[7:],
                                           'named_extras': {},
                                           'modify_inputs_mode': 1,
                                           'modify_inputs': ("a.test", "b.test")}

        # Error: empty list
        with self.assertRaises(error_missing_args):
            parse_task_arguments(
                empty_named_arguments, empty_named_arguments, expected_arguments, task_description)

        # parse complete correctly
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {}, expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # Error: missing argument
        unnamed_arguments = orig_unnamed_arguments[0:6]
        with self.assertRaises(error_missing_args):
            results = parse_task_arguments(unnamed_arguments,
                                           {}, expected_arguments, task_description)

        # parse almost complete and rescued with named parameter
        unnamed_arguments = orig_unnamed_arguments[0:6]
        results = parse_task_arguments(unnamed_arguments,
                                       {'output': expected_results['output'],
                                        'extras': expected_results['extras']},
                                       expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # All named parameters
        results = parse_task_arguments([],
                                       {'input': orig_unnamed_arguments[0],
                                        'filter': orig_unnamed_arguments[1],
                                        'input2': orig_unnamed_arguments[2],
                                        'filter2': orig_unnamed_arguments[3],
                                        'input3': orig_unnamed_arguments[4],
                                        'filter3': orig_unnamed_arguments[5],
                                        'output': orig_unnamed_arguments[6],
                                        'extras': orig_unnamed_arguments[7:],
                                        },
                                       expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # Error: Unknown named arguments
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments([],
                                           {'input': orig_unnamed_arguments[0],
                                            'filter': orig_unnamed_arguments[1],
                                            'input2': orig_unnamed_arguments[2],
                                            'filter2': orig_unnamed_arguments[3],
                                            'input3': orig_unnamed_arguments[4],
                                            'filter3': orig_unnamed_arguments[5],
                                            'output': orig_unnamed_arguments[6],
                                            'what': orig_unnamed_arguments[7:]
                                            },
                                           expected_arguments, task_description)

        # Error: Duplicate named arguments
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {'input': orig_unnamed_arguments[0],
                                            'extras': orig_unnamed_arguments[7:],
                                            },
                                           expected_arguments, task_description)

        # add_inputs correct via named
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"add_inputs": ("a.test", "b.test")}, expected_arguments, task_description)
        self.assertEqual(results, add_inputs_expected_results)

        # add_inputs correct via named and paranoid add_inputs wrapping
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"add_inputs": add_inputs("a.test", "b.test")}, expected_arguments, task_description)
        self.assertEqual(results, add_inputs_expected_results)

        # add_inputs correct via unnamed
        unnamed_arguments = list(orig_unnamed_arguments)
        unnamed_arguments.insert(6, add_inputs("a.test", "b.test"))
        results = parse_task_arguments(unnamed_arguments, {},
                                       expected_arguments, task_description)
        self.assertEqual(results, add_inputs_expected_results)

        # replace_inputs correct via named
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"replace_inputs": ("a.test", "b.test")}, expected_arguments, task_description)
        self.assertEqual(results, replace_inputs_expected_results)

        # replace_inputs correct via named and paranoid inputs() wrapping
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"replace_inputs": inputs(("a.test", "b.test"))}, expected_arguments, task_description)
        self.assertEqual(results, replace_inputs_expected_results)

        # replace_inputs correct via unnamed
        unnamed_arguments = list(orig_unnamed_arguments)
        unnamed_arguments.insert(6, inputs(("a.test", "b.test")))
        results = parse_task_arguments(unnamed_arguments, {},
                                       expected_arguments, task_description)
        self.assertEqual(results, replace_inputs_expected_results)

        # Error: both add_inputs and replace_inputs via named
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {"replace_inputs": ("a.test", "b.test"),
                                            "add_inputs": ("a.test", "b.test")}, expected_arguments, task_description)

        # Error: both add_inputs and replace_inputs via named / unnamed
        with self.assertRaises(error_too_many_args):
            unnamed_arguments = list(orig_unnamed_arguments)
            unnamed_arguments.insert(6, inputs(("a.test", "b.test")))
            results = parse_task_arguments(unnamed_arguments, {"add_inputs": ("a.test", "b.test")},
                                           expected_arguments, task_description)

        # Error: both add_inputs and replace_inputs via named / unnamed
        with self.assertRaises(error_too_many_args):
            unnamed_arguments = list(orig_unnamed_arguments)
            unnamed_arguments.insert(6, add_inputs("a.test", "b.test"))
            results = parse_task_arguments(unnamed_arguments, {"replace_inputs": ("a.test", "b.test")},
                                           expected_arguments, task_description)

        # Error: wrong number of arguments
        with self.assertRaises(error_inputs_multiple_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {"replace_inputs": inputs("a.test", "b.test")}, expected_arguments, task_description)

        # Error: no arguments
        with self.assertRaises(error_inputs_multiple_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {"replace_inputs": inputs()}, expected_arguments, task_description)


# ________________________________________________________________________________________________________

#   Test_parse_combinatorics_args

# ________________________________________________________________________________________________________
class Test_parse_combinatorics_args (unittest.TestCase):
    """
    Make sure (input, filter, tuple_size, output, extras...) works
    for @combinations
    """

    def test_parse_combinations_args(self):
        expected_arguments = ["input", "filter",
                              "tuple_size", "modify_inputs", "output", "extras"]

        empty_unnamed_arguments = []
        empty_named_arguments = {}
        orig_unnamed_arguments = [
            "*.txt", suffix(".txt"), 5, ".result", 1, 2, 3, 4]
        task_description = "@combinations(%s)\ndef myfunc(...)\n"
        expected_results = {'input': orig_unnamed_arguments[0],
                            'filter': orig_unnamed_arguments[1],
                            'tuple_size': orig_unnamed_arguments[2],
                            'output': orig_unnamed_arguments[3],
                            'extras': orig_unnamed_arguments[4:],
                            'named_extras': {},
                            'modify_inputs_mode': 2,
                            'modify_inputs': None}
        add_inputs_expected_results = {'input': orig_unnamed_arguments[0],
                                       'filter': orig_unnamed_arguments[1],
                                       'tuple_size': orig_unnamed_arguments[2],
                                       'output': orig_unnamed_arguments[3],
                                       'extras': orig_unnamed_arguments[4:],
                                       'named_extras': {},
                                       'modify_inputs_mode': 0,
                                       'modify_inputs': ("a.test", "b.test")}
        replace_inputs_expected_results = {'input': orig_unnamed_arguments[0],
                                           'filter': orig_unnamed_arguments[1],
                                           'tuple_size': orig_unnamed_arguments[2],
                                           'output': orig_unnamed_arguments[3],
                                           'extras': orig_unnamed_arguments[4:],
                                           'named_extras': {},
                                           'modify_inputs_mode': 1,
                                           'modify_inputs': ("a.test", "b.test")}

        # Error: empty list
        with self.assertRaises(error_missing_args):
            parse_task_arguments(
                empty_named_arguments, empty_named_arguments, expected_arguments, task_description)

        # parse complete correctly
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {}, expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # Error tuple_size not int
        unnamed_arguments = orig_unnamed_arguments[:]
        unnamed_arguments[2] = 'a'
        with self.assertRaises(TypeError):
            results = parse_task_arguments(unnamed_arguments,
                                           {}, expected_arguments, task_description)

        # Error: missing argument
        unnamed_arguments = orig_unnamed_arguments[0:2]
        with self.assertRaises(error_missing_args):
            results = parse_task_arguments(unnamed_arguments,
                                           {}, expected_arguments, task_description)

        # parse almost complete and rescued with named parameter
        unnamed_arguments = orig_unnamed_arguments[0:2]
        results = parse_task_arguments(unnamed_arguments,
                                       {
                                           'tuple_size': orig_unnamed_arguments[2],
                                           'output': orig_unnamed_arguments[3],
                                           'extras': orig_unnamed_arguments[4:]},
                                       expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # All named parameters
        unnamed_arguments = orig_unnamed_arguments[0:2]
        results = parse_task_arguments([],
                                       {'input': orig_unnamed_arguments[0],
                                        'filter': orig_unnamed_arguments[1],
                                        'tuple_size': orig_unnamed_arguments[2],
                                        'output': orig_unnamed_arguments[3],
                                        'extras': orig_unnamed_arguments[4:],
                                        },
                                       expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # Error tuple_size not int
        unnamed_arguments = orig_unnamed_arguments[0:2]
        with self.assertRaises(TypeError):
            results = parse_task_arguments([],
                                           {'input': orig_unnamed_arguments[0],
                                            'filter': orig_unnamed_arguments[1],
                                            'tuple_size': "a",
                                            'output': orig_unnamed_arguments[3],
                                            'extras': orig_unnamed_arguments[4:],
                                            },
                                           expected_arguments, task_description)

        # Error: Unknown named arguments
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments([],
                                           {'input': orig_unnamed_arguments[0],
                                            'filter': orig_unnamed_arguments[1],
                                            'tuple_size': orig_unnamed_arguments[2],
                                            'output': orig_unnamed_arguments[3],
                                            'what': orig_unnamed_arguments[4:]
                                            },
                                           expected_arguments, task_description)

        # Error: Duplicate named arguments
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {'input': orig_unnamed_arguments[0],
                                            'extras': orig_unnamed_arguments[3:],
                                            },
                                           expected_arguments, task_description)

        # add_inputs correct via named
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"add_inputs": ("a.test", "b.test")}, expected_arguments, task_description)
        self.assertEqual(results, add_inputs_expected_results)

        # add_inputs correct via named and paranoid add_inputs wrapping
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"add_inputs": add_inputs("a.test", "b.test")}, expected_arguments, task_description)
        self.assertEqual(results, add_inputs_expected_results)

        # add_inputs correct via unnamed
        unnamed_arguments = list(orig_unnamed_arguments)
        unnamed_arguments.insert(3, add_inputs("a.test", "b.test"))
        results = parse_task_arguments(unnamed_arguments, {},
                                       expected_arguments, task_description)
        self.assertEqual(results, add_inputs_expected_results)

        # replace_inputs correct via named
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"replace_inputs": ("a.test", "b.test")}, expected_arguments, task_description)
        self.assertEqual(results, replace_inputs_expected_results)

        # replace_inputs correct via named and paranoid inputs() wrapping
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {"replace_inputs": inputs(("a.test", "b.test"))}, expected_arguments, task_description)
        self.assertEqual(results, replace_inputs_expected_results)

        # replace_inputs correct via unnamed
        unnamed_arguments = list(orig_unnamed_arguments)
        unnamed_arguments.insert(3, inputs(("a.test", "b.test")))
        results = parse_task_arguments(unnamed_arguments, {},
                                       expected_arguments, task_description)
        self.assertEqual(results, replace_inputs_expected_results)

        # Error: both add_inputs and replace_inputs via named
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {"replace_inputs": ("a.test", "b.test"),
                                            "add_inputs": ("a.test", "b.test")}, expected_arguments, task_description)

        # Error: both add_inputs and replace_inputs via named / unnamed
        with self.assertRaises(error_too_many_args):
            unnamed_arguments = list(orig_unnamed_arguments)
            unnamed_arguments.insert(3, inputs(("a.test", "b.test")))
            results = parse_task_arguments(unnamed_arguments, {"add_inputs": ("a.test", "b.test")},
                                           expected_arguments, task_description)

        # Error: both add_inputs and replace_inputs via named / unnamed
        with self.assertRaises(error_too_many_args):
            unnamed_arguments = list(orig_unnamed_arguments)
            unnamed_arguments.insert(3, add_inputs("a.test", "b.test"))
            results = parse_task_arguments(unnamed_arguments, {"replace_inputs": ("a.test", "b.test")},
                                           expected_arguments, task_description)

        # Error: wrong number of arguments
        with self.assertRaises(error_inputs_multiple_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {"replace_inputs": inputs("a.test", "b.test")}, expected_arguments, task_description)

        # Error: no arguments
        with self.assertRaises(error_inputs_multiple_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {"replace_inputs": inputs()}, expected_arguments, task_description)


# ________________________________________________________________________________________________________

#   Test_parse_originate_args

# ________________________________________________________________________________________________________
class Test_parse_originate_args (unittest.TestCase):
    """
    Make sure @originate(output, extras...) works
    """

    def test_parse_originate_args(self):
        expected_arguments = ["output", "extras"]

        empty_unnamed_arguments = []
        empty_named_arguments = {}
        orig_unnamed_arguments = [["a.1", "b.1"], 1, 2, 3, 4]
        task_description = "@originate(%s)\ndef myfunc(...)\n"
        expected_results = {'output': orig_unnamed_arguments[0],
                            'extras': orig_unnamed_arguments[1:],
                            'named_extras': {},
                            }

        # Error: empty list
        with self.assertRaises(error_missing_args):
            parse_task_arguments(
                empty_named_arguments, empty_named_arguments, expected_arguments, task_description)

        # parse complete correctly
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {}, expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # All named parameters
        unnamed_arguments = orig_unnamed_arguments[0:2]
        results = parse_task_arguments([],
                                       {'output': orig_unnamed_arguments[0],
                                        'extras': orig_unnamed_arguments[1:]
                                        },
                                       expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # Error: Unknown named arguments
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments([],
                                           {'output': orig_unnamed_arguments[0],
                                            'what': orig_unnamed_arguments[1:]
                                            },
                                           expected_arguments, task_description)

        # Error: Duplicate named arguments
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {'output': orig_unnamed_arguments[0],
                                            },
                                           expected_arguments, task_description)

# _________________________________________________________________________________________

#   Test_parse_mkdir_args

# _________________________________________________________________________________________


class Test_parse_mkdir_args (unittest.TestCase):

    def test_parse_mkdir_args(self):
        expected_arguments = ["input", "filter", "output"]

        empty_unnamed_arguments = []
        empty_named_arguments = {}
        orig_unnamed_arguments = ["*.txt", suffix(".txt"), ".result"]
        task_description = "@mkdir(%s)\ndef myfunc(...)\n"
        expected_results = {'input': orig_unnamed_arguments[0],
                            'filter': orig_unnamed_arguments[1],
                            'output': orig_unnamed_arguments[2]}
        add_inputs_expected_results = {'input': orig_unnamed_arguments[0],
                                       'filter': orig_unnamed_arguments[1],
                                       'output': orig_unnamed_arguments[2]}
        replace_inputs_expected_results = {'input': orig_unnamed_arguments[0],
                                           'filter': orig_unnamed_arguments[1],
                                           'output': orig_unnamed_arguments[2]}

        # Error: empty list
        with self.assertRaises(error_missing_args):
            parse_task_arguments(
                empty_named_arguments, empty_named_arguments, expected_arguments, task_description)

        # parse complete correctly
        results = parse_task_arguments(orig_unnamed_arguments,
                                       {}, expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # Error: missing argument
        unnamed_arguments = orig_unnamed_arguments[0:1]
        with self.assertRaises(error_missing_args):
            results = parse_task_arguments(unnamed_arguments,
                                           {}, expected_arguments, task_description)

        # parse almost complete and rescued with named parameter
        unnamed_arguments = orig_unnamed_arguments[0:2]
        results = parse_task_arguments(unnamed_arguments,
                                       {'output': orig_unnamed_arguments[2]},
                                       expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # All named parameters
        unnamed_arguments = orig_unnamed_arguments[0:2]
        results = parse_task_arguments([],
                                       {'input': orig_unnamed_arguments[0],
                                        'filter': orig_unnamed_arguments[1],
                                        'output': orig_unnamed_arguments[2],
                                        },
                                       expected_arguments, task_description)
        self.assertEqual(results, expected_results)

        # Error: Unknown named arguments
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments([],
                                           {'input': orig_unnamed_arguments[0],
                                            'filter': orig_unnamed_arguments[1],
                                            'output': orig_unnamed_arguments[2],
                                            'what': orig_unnamed_arguments[3:]
                                            },
                                           expected_arguments, task_description)

        # Error: Duplicate named arguments
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments(orig_unnamed_arguments,
                                           {'input': orig_unnamed_arguments[0],
                                            },
                                           expected_arguments, task_description)

        # Error: no extras arguments allowed
        with self.assertRaises(error_too_many_args):
            results = parse_task_arguments(orig_unnamed_arguments + [1, formatter(), 'a', 4],
                                           {'input': orig_unnamed_arguments[0],
                                            },
                                           expected_arguments, task_description)


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    unittest.main()
