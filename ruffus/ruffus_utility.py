from __future__ import print_function
import copy
import os
from itertools import chain
from . import dbdict
import operator
import marshal
import hashlib
import multiprocessing.managers
from collections import defaultdict
from .ruffus_exceptions import *
from functools import reduce
import glob
import types
import sys
import re
if sys.hexversion < 0x03000000:
    from future_builtins import zip
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


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#import task
try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable
try:
    import cPickle as pickle
except:
    import pickle as pickle
if sys.hexversion >= 0x03000000:
    # everything is unicode in python3
    path_str_type = str
else:
    path_str_type = basestring

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Constants


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
# file to store history out to
#
RUFFUS_HISTORY_FILE = '.ruffus_history.sqlite'
# If DEFAULT_RUFFUS_HISTORY_FILE is specified in the environment variables, use that instead
if "DEFAULT_RUFFUS_HISTORY_FILE" in os.environ:
    RUFFUS_HISTORY_FILE = os.environ["DEFAULT_RUFFUS_HISTORY_FILE"]


# only rerun when the file timestamps are out of date (classic mode)
CHECKSUM_FILE_TIMESTAMPS = 0
# also rerun when the history shows a job as being out of date
CHECKSUM_HISTORY_TIMESTAMPS = 1
CHECKSUM_FUNCTIONS = 2     # also rerun when function body has changed
# also rerun when function parameters or function body change
CHECKSUM_FUNCTIONS_AND_PARAMS = 3

CHECKSUM_REGENERATE = 2     # regenerate checksums


# number of times to check if an input file exists
FILE_CHECK_RETRY = 5
# number of seconds to sleep before retrying a file check
FILE_CHECK_SLEEP = 10
# _________________________________________________________________________________________

#   t_extra_inputs
#       namespaced enum

# _________________________________________________________________________________________


class t_extra_inputs:
    (ADD_TO_INPUTS, REPLACE_INPUTS, KEEP_INPUTS, KEEP_OUTPUTS) = list(range(4))


class inputs(object):
    def __init__(self, *args):
        self.args = args

    def __repr__(self, *args):
        return 'inputs%r' % (self.args,)


class add_inputs(object):
    def __init__(self, *args):
        self.args = args

    def __repr__(self, *args):
        return 'add_inputs%r' % (self.args,)


def get_default_checksum_level():
    """
    Use the checksum level from the environmental variable DEFAULT_RUFFUS_CHECKSUM_LEVEL
    Otherwise default to CHECKSUM_HISTORY_TIMESTAMPS
    """

    #
    #   environmental variable not set
    #
    if "DEFAULT_RUFFUS_CHECKSUM_LEVEL" not in os.environ:
        return CHECKSUM_HISTORY_TIMESTAMPS

    #
    # lookup value from list of CHECKSUM_XXX constants
    #
    checksum_level = None
    env_checksum_level = os.environ["DEFAULT_RUFFUS_CHECKSUM_LEVEL"]
    if len(env_checksum_level) == 1 and env_checksum_level in "0123":
        checksum_level = int(env_checksum_level)
    else:
        global_var = globals()
        for key in global_var:
            if key.startswith('CHECKSUM') and global_var[key] == env_checksum_level:
                checksum_level = value

    #
    #   check environmental variable is valid string
    #
    if checksum_level is None:
        raise error_checksum_level(("The environmental value "
                                    "DEFAULT_RUFFUS_CHECKSUM_LEVEL should be: [0-3 | "
                                    "CHECKSUM_FILE_TIMESTAMPS | "
                                    "CHECKSUM_HISTORY_TIMESTAMPS | "
                                    "CHECKSUM_FUNCTIONS | "
                                    "CHECKSUM_FUNCTIONS_AND_PARAMS] (rather than '%s') ")
                                   % (env_checksum_level,))

    return checksum_level


# _________________________________________________________________________________________

#   open_job_history

# _________________________________________________________________________________________
def get_default_history_file_name():
    history_file = RUFFUS_HISTORY_FILE
    #
    #   try path expansion using the main script name
    #
    try:
        import __main__ as main
        path_parts = path_decomposition(os.path.abspath(main.__file__))
        history_file = history_file.format(**path_parts)
    except Exception:
        pass
    return history_file


def open_job_history(history_file):
    """
    Given a history file name, opens the correspond sqllite db file and returns the handle
    """
    if not history_file:
        history_file = get_default_history_file_name()

    return dbdict.open(history_file, picklevalues=True)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

class JobHistoryChecksum:
    """Class to remember exactly how an output file was created and when."""

    def __str__(self):
        from time import strftime, gmtime
        if hasattr(self, "params"):
            return str([self.outfile,
                        strftime("%d %b %Y %H:%M:%S", gmtime(self.mtime)),
                        self.params,
                        self.task_name
                        ])
        else:
            return strftime("%d %b %Y %H:%M:%S", gmtime(self.mtime))

    def __init__(self, outfile, mtime, params, task):
        # filename and modification time
        self.outfile = outfile
        self.mtime = mtime

        # Uncomment next two lines to debug:
        #self.params = params
        #self.task_name = task._name

        # checksum exact params used to generate this output file
        self.chksum_params = hashlib.md5(pickle.dumps(params)).hexdigest()
        # checksum the function bytecode as well as the function context
        # Don't use func_code alone-- changing the line number of the function,
        # what global variables are available, etc would all change the checksum
        if sys.hexversion >= 0x03000000:
            code = task.user_defined_work_func.__code__
            func_defaults = task.user_defined_work_func.__defaults__
        else:
            code = task.user_defined_work_func.func_code
            func_defaults = task.user_defined_work_func.func_defaults
        func_code = marshal.dumps(code.co_code)

        #
        #   pickle code very defensively, but hopefully without breaking Jake Biesinger's pipelines!
        #
        attributes_to_pickle = [func_defaults,
                                code.co_argcount,
                                code.co_consts,
                                code.co_names,
                                code.co_nlocals,
                                code.co_varnames]

        pickle_results = []
        for aa in attributes_to_pickle:
            # Can't cpickle nested functions: typically blows up with func_code.co_consts
            try:
                pickle_results.append(pickle.dumps(aa))
                continue
            except:
                pass
            # Marshal seems to be less sensitive: try that
            try:
                pickle_results.append(marshal.dumps(aa))
                continue
            except:
                pass
            # Just make a string out of the attribute
            try:
                pickle_results.append(str(aa))
                continue
            except:
                pass
            # OK give up, do nothing: On your head it is

        func_extras = reduce(operator.add, pickle_results)
        self.chksum_func = hashlib.md5(func_code + func_extras).hexdigest()


# _________________________________________________________________________________________
#
#   parameter_list_as_string
#
# _________________________________________________________________________________________
def parameter_list_as_string(parameters):
    """
    Input list of parameters
       Turn this into a string for display

        E.g.

    """
    if parameters is None:
        return ""
    elif not isinstance(parameters, list):
        raise Exception("Unexpected parameter list %s" % (parameters,))
    else:
        return str(parameters)[1:-1]

# _________________________________________________________________________________________
#
#   path_decomposition
#
# _________________________________________________________________________________________


def path_decomposition(orig_path):
    """
    returns a dictionary identifying the components of a file path:
        This has the following keys
            basename: (any) base (file) name of the path not including the extension. No slash included
            ext:      (any) extension of the path including the "."
            path:     a list of subpaths created by removing subdirectory names
            subdir:   a list of subdirectory names from the most nested to the root
        For example
            apath = "/a/b/c/d/filename.txt"
            {   'basename': 'filename',
                'ext':      '.txt'
                'path':     ['/a/b/c/d', '/a/b/c', '/a/b', '/a', '/'], ,
                'subdir': ['d', 'c', 'b', 'a', '/']
            }
            "{path[2]}/changed/{subdir[0]}".format(**res) = '/a/b/changed/d'
            "{path[3]}/changed/{subdir[1]}".format(**res) = '/a/changed/c'
    """
    def recursive_split(a_path):
        """
        split the path into its subdirectories recursively
        """
        if not len(a_path):
            return [[], []]
        if a_path == "/" or a_path == "//":
            return [[a_path], [a_path]]
        sub_path_part, sub_dir_part = os.path.split(a_path)
        if sub_dir_part:
            sub_path_parts, sub_dir_parts = recursive_split(sub_path_part)
            return [[a_path] + sub_path_parts,
                    [sub_dir_part] + sub_dir_parts]
        else:
            return [[], ["/"]]
    #
    if not len(orig_path):
        return {'path': [], 'basename': '', 'ext': '', 'subdir': []}

    # stop normpath from being too clever and removing initial ./ and terminal slash, turning paths into filenames
    if orig_path in ["./", "/."]:
        a_path = orig_path
    else:
        a_path = os.path.normpath(orig_path)
        if orig_path[0:2] == "./" and a_path[0:2] != "./":
            a_path = "./" + a_path

        if orig_path[-1] == "/" and a_path[-1:] != "/":
            a_path += "/"

    path_part, file_part = os.path.split(a_path)
    file_part, ext_part = os.path.splitext(file_part)
    subpaths, subdirs = recursive_split(path_part)
    return {'basename': file_part,
            'ext':      ext_part,
            'subpath':  subpaths,
            'subdir':   subdirs,
            'path':     path_part}


# _________________________________________________________________________________________
#
#   get_nth_nested_level_of_path
#
# _________________________________________________________________________________________
def get_nth_nested_level_of_path(orig_path, n_levels):
    """
    Return path with up to N levels of subdirectories
    0 = full path
    N = 1 : basename
    N = 2 : basename + one subdirectory

    For example
        0   /test/this/now/or/not.txt
        1   not.txt
        2   or/not.txt
        3   now/or/not.txt
        4   this/now/or/not.txt
        5   test/this/now/or/not.txt
        6   /test/this/now/or/not.txt
        7   /test/this/now/or/not.txt
    """
    # FIXME: consider returning full path to make debugging easier or at least
    # make it optional
    if not n_levels or n_levels < 0:
        return orig_path
    res = path_decomposition(orig_path)
    basename = res["basename"] + res["ext"]
    shortened_path = os.path.join(
        *(list(reversed(res["subdir"][0:(n_levels - 1)]))+[basename]))
    if len(shortened_path) < len(orig_path):
        return ".../" + shortened_path


# _________________________________________________________________________________________
#
#   swap_nesting_order
#
# _________________________________________________________________________________________
def swap_nesting_order(orig_coll):
    """
    Reverse nested order so that coll[3]['a'] becomes coll['a'][3]
    """
    new_dict = defaultdict(dict)
    new_list = []
    for ii, ii_item in enumerate(orig_coll):
        for jj, value in ii_item.items():
            if isinstance(jj, int):
                # resize
                new_list += [{}]*(jj + 1 - len(new_list))
                new_list[jj][ii] = value
            else:
                new_dict[jj][ii] = value
    return new_list, dict(new_dict)

# _________________________________________________________________________________________
#
#   swap_doubly_nested_order
#
# _________________________________________________________________________________________


def swap_doubly_nested_order(orig_coll):
    """
    Reverse nested order so that coll[3]['a'] becomes coll['a'][3]
    """
    new_dict = dict()
    new_list = []
    for ii, ii_item in enumerate(orig_coll):
        for jj, jj_item in enumerate(ii_item):
            for kk, value in jj_item.items():
                if isinstance(kk, int):
                    # resize
                    new_list += [{}]*(kk + 1 - len(new_list))
                    if ii not in new_list[kk]:
                        new_list[kk][ii] = dict()
                    new_list[kk][ii][jj] = value
                else:
                    if kk not in new_dict:
                        new_dict[kk] = dict()
                    if ii not in new_dict[kk]:
                        new_dict[kk][ii] = dict()
                    new_dict[kk][ii][jj] = value

    return new_list, new_dict


# _________________________________________________________________________________________
#
#   regex_matches_as_dict
#
# _________________________________________________________________________________________
def regex_matches_as_dict(test_str, compiled_regex):
    """
    Returns result of regular expression match in a dictionary
        combining both named and unnamed captures
    """
    if compiled_regex:
        if isinstance(compiled_regex, path_str_type):
            compiled_regex = re.compile(compiled_regex)
        mm = compiled_regex.search(test_str)
        # Match failed
        if mm is None:
            return False
        else:
            # No capture
            if mm.lastindex is None:
                return {0: mm.group(0)}
            # Combined named and unnamed captures
            else:
                # no dictionary comprehensions in python 2.6 :-(
                #matchdicts.append({i : mm.group(i) for i in (range(mm.lastindex) + mm.groupdict().keys())})
                #   Keys for captures:
                #       1) unnamed captures = range(mm.lastindex + 1)
                #       2) named captures   = mm.groupdict().keys()
                return dict((i, mm.group(i)) for i in (chain(iter(range(mm.lastindex + 1)),
                                                             iter(mm.groupdict().keys()))))

    else:
        return None


# _________________________________________________________________________________________
#
#   path_decomposition_regex_match
#
# _________________________________________________________________________________________
def path_decomposition_regex_match(test_str, compiled_regex):
    """
    Returns a dictionary identifying the components of a file path.

    This includes both the components of a path:
        basename: (any) base (file) name of the path not including the extension. No slash included
        ext:      (any) extension of the path including the "."
        path:     a list of subpaths created by removing subdirectory names
        subdir:   a list of subdirectory names from the most nested to the root
    and regular expression matches
        The keys are the index or name of the capturing group.


    If compiled_regexes is not specified, return path decomposition only

    If compiled_regexes is specified, and the corresponding regular expression does not match,
        the entire match fails

    For example

        path_decomposition_regex_match("/a/b/c/sample1.bam", r"(.*)(?P<id>\d+)\..+")

            {
                0:          '/a/b/c/sample1.bam',           // captured by index
                1:          '/a/b/c/sample',                // captured by index
                'id':       '1'                             // captured by name
                'ext':      '.bam',
                'subdir':   ['c', 'b', 'a', '/'],
                'subpath':  ['/a/b/c', '/a/b', '/a', '/'],
                'path':     '/a/b/c',
                'basename': 'sample1',
            },

        path_decomposition_regex_match("dbsnp15.vcf", r"(.*)(?P<id>\d+)\..+")
            {
                0: 'dbsnp15.vcf',                           // captured by index
                1: 'dbsnp1',                                // captured by index
                'id': '5'                                   // captured by name
                'ext': '.vcf',
                'subdir': [],
                'path': [],
                'basename': 'dbsnp15',
            },


        // fail
        path_decomposition_regex_match("/test.txt", r"(.*)(?P<id>\d+)\..+")
            {}

        // path components only
        path_decomposition_regex_match("/test.txt", None)
            {
                'ext': '.txt',
                'subdir': ['/']
                'subpath': ['/'],
                'path': '/',
                'basename': 'test',
            }

    """
    pp = path_decomposition(test_str)

    # regular expression not specified
    # just path
    if compiled_regex is None:
        return pp

    rr = regex_matches_as_dict(test_str, compiled_regex)

    # regular expression match failed
    # nothing
    if rr == False:
        return {}

    #
    #   regular expression matches override file decomposition values in
    #       case of clashes between predefined keys such as "basename" and
    #       regular expression named capture groups
    #
    pp.update(rr)
    return pp


# _________________________________________________________________________________________
#
#   check_compiled_regexes
#
# _________________________________________________________________________________________
def check_compiled_regexes(compiled_regexes, expected_num):
    """
    check compiled_regexes are of the right type and number
    """
    if compiled_regexes is None:
        return [None] * expected_num

    if not isinstance(compiled_regexes, list):
        raise Exception("Expecting list of None and strings")

    #   pad compiled_regexes with None
    if len(compiled_regexes) < expected_num:
        compiled_regexes.extend(
            [None] * (expected_num - len(compiled_regexes)))

    #   Turn strings to regular expression just in case
    #   We don't want to do this here because the error messages are not very nice:
    #   There is not much context left
    compiled_regexes = [re.compile(rr) if isinstance(
        rr, path_str_type) else rr for rr in compiled_regexes]

    #   check types
    regex_types = type(re.compile("")), type(None)
    for rr in compiled_regexes:
        if not isinstance(rr, regex_types):
            raise Exception(
                "Unexpected type %s ('%s') specified in regular expression list. Expecting string or compiled regular expression" % (type(rr), rr))

    return compiled_regexes


# _________________________________________________________________________________________
#
#   get_all_paths_components
#
# _________________________________________________________________________________________
def get_all_paths_components(paths, compiled_regexes):
    """
        For each path in a list,
            If any of the regular expression matches fails, the whole list fails
    """
    #
    #   merge regular expression matches and path decomposition
    #
    compiled_regexes = check_compiled_regexes(compiled_regexes, len(paths))
    results = []
    for (pp, rr) in zip(paths, compiled_regexes):
        result = path_decomposition_regex_match(pp, rr)
        if result == {}:
            return [{}] * len(paths)
        results.append(result)
    return results


# _________________________________________________________________________________________
#
#   apply_func_to_sequence
#
# _________________________________________________________________________________________
def apply_func_to_sequence(seq, func, tuple_of_conforming_types=(path_str_type,), tuple_of_sequences_types=(list, tuple, set)):
    """
    Recurses into list/tuple/set sequences to apply func to conforming types
    Non-conforming types are left alone
    """
    if isinstance(seq, tuple_of_conforming_types):
        return func(seq)
    elif isinstance(seq, tuple_of_sequences_types):
        return type(seq)(apply_func_to_sequence(pp, func, tuple_of_conforming_types, tuple_of_sequences_types) for pp in seq)
    else:
        return seq


# _________________________________________________________________________________________
#
#   t_regex_replace
#
# _________________________________________________________________________________________
class t_regex_replace(object):
    def __init__(self, filename, regex_str, compiled_regex, regex_or_suffix):
        self.regex_or_suffix = regex_or_suffix
        self.compiled_regex = compiled_regex
        self.regex_str = regex_str
        self.filename = filename

    def __call__(self, p):
        #
        #   check if substitution pattern is mis-specified
        #
        if "\1"in p or "\2" in p:
            raise error_unescaped_regular_expression_forms("['%s'] " % (p.replace("\1", r"\1").replace("\2", r"\2")) +
                                                           "The special regular expression characters "
                                                           r"\1 and \2 need to be 'escaped' in python. "
                                                           r"The easiest option is to use python 'raw' strings "
                                                           r"e.g. r'\1_in_a string\2'. See http://docs.python.org/library/re.html.")
        #
        #   For suffix(), replaces the suffix part by adding leading r"\1" to the substitution pattern
        #
        #   If r"\1" is specified, then we presume you know what you are doing...
        #
        if self.regex_or_suffix == SUFFIX_SUBSTITUTE:
            if r"\1" not in p and r"\g<1>" not in p:
                match_p = r"\g<1>" + p
            else:
                match_p = p

            # throw exception if doesn't match regular expression at all
            (res_str, cnt_replacements) = self.compiled_regex.subn(
                match_p, self.filename)
            if cnt_replacements == 0:
                raise error_input_file_does_not_match(
                    "File '%s' does not match suffix('%s') and pattern '%s'" % (self.filename, self.regex_str, p))
            return res_str

        #
        #   Normal substitution
        #
        #   For suffix(), complete replacement by the specified pattern text
        #           only substitute if r"\1" or r"\g<1>" is specified
        #
        #
        err_str = ""
        try:
            (res_str, cnt_replacements) = self.compiled_regex.subn(p, self.filename)
            if cnt_replacements > 0:
                return res_str
        except re.error:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            err_str = str(exceptionValue)
            raise fatal_error_input_file_does_not_match(
                "File '%s' does not match regex('%s') and pattern '%s':\n\t%s\n" % (self.filename, self.regex_str, p, err_str))
        except IndexError:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            err_str = str(exceptionValue)
            raise fatal_error_input_file_does_not_match(
                "File '%s' does not match regex('%s') and pattern '%s':\n\t%s\n" % (self.filename, self.regex_str, p, err_str))

        # except (re.error, IndexError):
            #err_str = str(sys.exc_info()[1]),

        raise error_input_file_does_not_match("File '%s' does not match regex('%s') and pattern '%s'\n%s\n" % (
            self.filename, self.regex_str, p, err_str))


# _________________________________________________________________________________________
#
#   raise_formatter_substitution_exception
#
# _________________________________________________________________________________________
def raise_formatter_substitution_exception(exceptionValue, formatter_str, pattern, filenames,
                                           substitutes_list, substitutes_dict):
    """
    Throws an exception when formatter fails to make a substitution
    """
    # convert to string to get just the missing key
    missing_key = str(exceptionValue.args[0])
    # strip quotes
    if missing_key[0:1] in '\'"' and missing_key[-1:] in '\'"':
        missing_key = missing_key[1:-1]
    raise error_input_file_does_not_match("Unmatched field {%s} in '%s' where\n  input =  %r,\n"
                                          "  filter = formatter(%s). Possible substitutions= %s, %s."
                                          % (missing_key,
                                             pattern,
                                             filenames,
                                             formatter_str,
                                             substitutes_list, substitutes_dict))


# _________________________________________________________________________________________
#
#   t_formatter_replace
#
# _________________________________________________________________________________________
class t_formatter_replace(object):
    def __init__(self, filenames, regex_strings, compiled_regexes=None):
        self.filenames = filenames
        # get the full absolute, normalised paths
        filenames = [os.path.abspath(f) for f in filenames]
        self.path_regex_components = get_all_paths_components(
            filenames, compiled_regexes)
        self.display_regex_strings = parameter_list_as_string(regex_strings)

    def __call__(self, pattern):
        # swapped nesting order makes the syntax easier to explain:
        #   The first level of indirection is always the path component
        #   So basename[0] is the file name for the first file
        #   This looks better than the normal 0[basename]

        # some contortions because format decodes {0} as an offset into a list and not not a lookup into a dict...
        substitutes_list, substitutes_dict = swap_nesting_order(
            self.path_regex_components)

        try:
            return pattern.format(*substitutes_list, **substitutes_dict)
        except (KeyError, IndexError):
            raise_formatter_substitution_exception(sys.exc_info()[1], self.display_regex_strings,
                                                   pattern, self.filenames,
                                                   substitutes_list, substitutes_dict)


# _________________________________________________________________________________________
#
#   t_nested_formatter_replace
#
# _________________________________________________________________________________________
class t_nested_formatter_replace(object):
    """
    Like  t_formatter_replace but with one additional level of nesting
    I.e. everything is a list comprehension!
    For combinatorics @decorators
    """

    def __init__(self, filenames, regex_strings, compiled_regexes):
        # make sure that we have the same level of nestedness for regular expressions and file names etc.
        if len(filenames) != len(regex_strings) or len(filenames) != len(compiled_regexes):
            raise Exception("Logic Error.")
        self.filenames = filenames
        # get the full absolute, normalised paths
        filenames = [[os.path.abspath(f) for f in filegroups]
                     for filegroups in filenames]
        self.path_regex_components = [get_all_paths_components(
            f, r) for (f, r) in zip(filenames, compiled_regexes)]
        self.display_regex_strs = [
            parameter_list_as_string(ss) for ss in regex_strings]

    def __call__(self, pattern):
        # swapped nesting order makes the syntax easier to explain:
        #   The first level of indirection is always the path component
        #   So basename[0] is the file name for the first file
        #   This looks better than the normal 0[basename]

        # some contortions because format decodes {0} as an offset into a list and not not a lookup into a dict...
        substitutes_list, substitutes_dict = swap_doubly_nested_order(
            self.path_regex_components)
        try:
            return pattern.format(*substitutes_list, **substitutes_dict)
        except (KeyError, IndexError):
            formatter_str = ", ".join("formatter(%s)" %
                                      ss for ss in self.display_regex_strs)
            raise_formatter_substitution_exception(sys.exc_info()[1], formatter_str, pattern, self.filenames,
                                                   substitutes_list, substitutes_dict)

# _________________________________________________________________________________________
#
#   t_nested_string_replace
#
# _________________________________________________________________________________________


class t_nested_string_replace(object):
    """
    Replaces path with directory
    """

    def __init__(self, prev_str, new_str):
        self.prev_str = prev_str
        self.new_str = new_str

    def __call__(self, p):
        return p.replace(prev_str, new_str)


# _________________________________________________________________________________________
#
#   regex_replace
#
# _________________________________________________________________________________________

#
#   Perform normal regular expression substitution
#
REGEX_SUBSTITUTE = 0
#
#   An extra peculiar mode to help suffix along:
#   Suffix regular expression have an implicit capture for everything up to the specified
#       suffix text

#
#   By default, replaces the suffix part by adding leading r"\1" to the substitution pattern
#       If r"\1" is already specified in the pattern, then we presume you know what
#       you are doing, and will let you get along with it
#
SUFFIX_SUBSTITUTE = 1

#
#   REGEX_SUBSTITUTE is used for suffix() matches in 'extra' arguments (additional to output)
#   which are strings
#
#   Complete replacement happens. If you wish to retain the prefix text
#       before the suffix, you can do so by adding r"\1"
#


def regex_replace(filename, regex_str, compiled_regex, substitution_patterns, regex_or_suffix=REGEX_SUBSTITUTE):
    return apply_func_to_sequence(substitution_patterns, t_regex_replace(filename, regex_str, compiled_regex, regex_or_suffix))


def formatter_replace(filenames, regex_str, compiled_regex, substitution_patterns):
    return apply_func_to_sequence(substitution_patterns, t_formatter_replace(filenames, regex_str, compiled_regex))


def nested_formatter_replace(filenames, regex_strings, compiled_regexes, substitution_patterns):
    return apply_func_to_sequence(substitution_patterns, t_nested_formatter_replace(filenames, regex_strings, compiled_regexes))


def nested_string_replace(prev_str, new_str, substitution_patterns):
    return apply_func_to_sequence(substitution_patterns, t_nested_string_replace(prev_str, new_str))


# _________________________________________________________________________________________

#   non_str_sequence

# _________________________________________________________________________________________
def non_str_sequence(arg):
    """
    Whether arg is a sequence.
    We treat strings / dicts however as a singleton not as a sequence

    """
    # will only dive into list and set, everything else is not regarded as a sequence
    # loss of flexibility but more conservative
    # if (isinstance(arg, (basestring, dict, multiprocessing.managers.DictProxy))):
    if (not isinstance(arg, (list, tuple, set))):
        return False
    try:
        test = iter(arg)
        return True
    except TypeError:
        return False

# _________________________________________________________________________________________

#   get_strings_in_flattened_sequence_aux

#       helper function for next function

# _________________________________________________________________________________________


def get_strings_in_flattened_sequence_aux(p, l=None):
    """
    Unravels arbitrarily nested sequence and returns lists of strings
    """
    if l is None:
        l = []
    if isinstance(p, path_str_type):
        l.append(p)
    elif non_str_sequence(p):
        for pp in p:
            get_strings_in_flattened_sequence_aux(pp, l)
    return l


# _________________________________________________________________________________________

#   non_str_sequence

# _________________________________________________________________________________________
def get_strings_in_flattened_sequence(p):
    """
    Traverses nested sequence and for each element, returns first string encountered
    """
    if p is None:
        return []

    #
    #  string is returned as list of single string
    #
    if isinstance(p, path_str_type):
        return [p]

    #
    #  Get all strings flattened into list
    #
    return get_strings_in_flattened_sequence_aux(p)


# _________________________________________________________________________________________

#   get_first_string_in_nested_sequence

# _________________________________________________________________________________________
def get_first_string_in_nested_sequence(p):
    strings = get_strings_in_flattened_sequence(p)
    if len(strings):
        return strings[0]
    return None


#
#   TODOOO third object could be a dict or a list
#
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Encoders: turn objects and filenames into a more presentable format

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
def ignore_unknown_encoder(obj):
    if non_str_sequence(obj):
        return "[%s]" % ", ".join(map(ignore_unknown_encoder, obj))
    try:
        s = str(obj)
        if " object" in s and s[0] == '<' and s[-1] == '>':
            pos = s.find(" object")
            s = "<" + s[1:pos].replace("__main__.", "") + ">"
        return s.replace('"', "'")
    except:
        return "<%s>" % str(obj.__class__).replace('"', "'")

# _________________________________________________________________________________________
#
#   shorten_filenames_encoder
# ________________________________________________________________________________________


def shorten_filenames_encoder(obj, n_levels=2):
    """
    Convert a set of parameters into a string
        Paths with > N levels of nested-ness are truncated
    """

    #
    #   if < 0, nest by 2
    #
    if n_levels < 0:
        desired_len = -n_levels
        prev_encoded_len = 0
        #
        #   try more and more nestedness up to 9 if that fits inside desired length
        #       stop when increasing nestedness makes no difference
        #
        for nestedness in range(1, 20):
            res = shorten_filenames_encoder(obj, nestedness)
            if len(res) > desired_len or "..." not in res:
                break
            prev_encoded_len = len(res)
        desired_len = max(4, desired_len - 5)
        offset = len(res) - desired_len
        if offset < 0:
            return res
        return "<???> " + res[offset:]

    #
    #   Recurse into lists and tuples
    #
    if non_str_sequence(obj):
        return "[%s]" % ", ".join(map(shorten_filenames_encoder, obj, [n_levels] * len(obj)))

    #
    #   Only shorten strings
    #
    if not isinstance(obj, path_str_type):
        return ignore_unknown_encoder(obj)

    #
    #   level = 0 means return full absolute path
    #
    if not n_levels:
        return ignore_unknown_encoder(os.path.abspath(obj))

    #
    # Shorten both relative and absolute (full) paths
    #

    # if within bounds, return that
    if obj[1:].count('/') < n_levels:
        return ignore_unknown_encoder(obj)

    # use relative path if that has <= nested level
    rel_path = os.path.relpath(obj)
    if rel_path.count('/') <= n_levels:
        #print >>sys.stderr, "relative path only one nested level"
        return ignore_unknown_encoder(rel_path)

    # get last N nested levels
    # print >>sys.stderr, "full path last N nested level"
    return ignore_unknown_encoder(get_nth_nested_level_of_path(obj, n_levels))


# _________________________________________________________________________________________
#
#   get_tasks_filename_globs_in_nested_sequence
#
# ________________________________________________________________________________________
glob_letters = set('*[]?')


def is_glob(s):
    """Check whether 's' contains ANY of glob chars"""
    return len(glob_letters.intersection(s)) > 0


# _________________________________________________________________________________________
#
#   get_nested_tasks_or_globs
#
# ________________________________________________________________________________________
def get_nested_tasks_or_globs(p, treat_strings_as_tasks=False, runtime_data_names=None, tasks=None, globs=None):
    """
    Get any tasks or globs which are within parameter
        tasks are returned as functions or function names
    """
    #
    # create storage if this is not a recursive call
    #
    if globs is None:
        runtime_data_names, tasks, globs = set(), list(), set()

    #
    #   task function
    #
    if isinstance(p, Callable):
        tasks.append(p)
    elif p.__class__.__name__ == 'Task' or p.__class__.__name__ == 'Pipeline':
        tasks.append(p)
    elif isinstance(p, runtime_parameter):
        runtime_data_names.add(p)

    #
    #   output_from treats all arguments as tasks or task names
    #
    elif isinstance(p, output_from):
        for pp in p.args:
            get_nested_tasks_or_globs(
                pp, True, runtime_data_names, tasks, globs)

    elif isinstance(p, path_str_type):
        if treat_strings_as_tasks:
            tasks.append(p)
        elif is_glob(p):
            globs.add(p)

    elif non_str_sequence(p):
        for pp in p:
            get_nested_tasks_or_globs(
                pp, treat_strings_as_tasks, runtime_data_names, tasks, globs)
    return tasks, globs, runtime_data_names

# _________________________________________________________________________________________
#
#   replace_placeholders_with_tasks_in_input_params
#
# ________________________________________________________________________________________


def replace_placeholders_with_tasks_in_input_params(p, func_or_name_to_task, treat_strings_as_tasks=False):
    """
    Replaces task functions or task name (strings) with the tasks they represent
    Also replaces Tasks and Pipelines with the correct Tasks
    func_or_name_to_task are a dictionary of function and task names to tasks

    """
    if p.__class__.__name__ == 'Pipeline':
        return func_or_name_to_task["PIPELINE=%s=PIPELINE" % p.name]

    if p.__class__.__name__ == 'Task' and p in func_or_name_to_task:
        return func_or_name_to_task[p]

    #
    # Expand globs or tasks as a list only if they are top level
    #
    if isinstance(p, Callable):
        # if type(p) == types.FunctionType:
        return func_or_name_to_task[p]

    #
    #   output_from treats all arguments as tasks or task names
    #
    if isinstance(p, output_from):
        if len(p.args) == 1:
            return replace_placeholders_with_tasks_in_input_params(p.args[0], func_or_name_to_task, True)
        else:
            return [replace_placeholders_with_tasks_in_input_params(pp, func_or_name_to_task, True) for pp in p.args]

    #
    # strings become tasks if treat_strings_as_tasks
    #
    if isinstance(p, path_str_type):
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
                    l.extend(tuple(replace_placeholders_with_tasks_in_input_params(
                        pp, func_or_name_to_task, True)))
                elif len(pp.args) == 1:
                    l.append(replace_placeholders_with_tasks_in_input_params(
                        pp.args[0], func_or_name_to_task, True))
                # else len(pp.args) == 0 !! do nothing

            else:
                l.append(replace_placeholders_with_tasks_in_input_params(
                    pp, func_or_name_to_task, treat_strings_as_tasks))
        return type(p)(l)

    #
    # No expansions of non-string/non-sequences
    #
    else:
        return p

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   compiling regular expressions

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
# _________________________________________________________________________________________

#   suffix

# _________________________________________________________________________________________


class suffix(object):
    def __init__(self, *args):
        self.args = args

    def __repr__(self, *args):
        return 'suffix%r' % (self.args,)

# _________________________________________________________________________________________

#   regex

# _________________________________________________________________________________________


class regex(object):
    def __init__(self, *args):
        self.args = args

    def __repr__(self, *args):
        return 'regex%r' % (self.args,)

# _________________________________________________________________________________________

#   regex

# _________________________________________________________________________________________


class formatter(object):
    def __init__(self, *args):
        self.args = args

    def __repr__(self, *args):
        return 'formatter%r' % (self.args,)

# _________________________________________________________________________________________

#   wrap_exception_as_string

# _________________________________________________________________________________________


def wrap_exception_as_string():
    """
    return exception as string to be rethrown
    """
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    msg = "%s.%s" % (exceptionType.__module__, exceptionType.__name__)
    exception_value = str(exceptionValue)
    if len(exception_value):
        return msg + ": (%s)" % exception_value
    return msg


# _________________________________________________________________________________________

#   compile_formatter

# _________________________________________________________________________________________
def compile_formatter(enclosing_task, formatter_obj, error_object, descriptor_string):
    """
    Given list of [string|None]
    Return compiled regular expressions.
    """

    compiled_regexes = []
    for ss in formatter_obj.args:
        # ignore None
        if ss is None:
            compiled_regexes.append(None)
            continue

        formatter_args = str(formatter_obj.args)[1:-1]
        # regular expression should be strings
        if not isinstance(ss, path_str_type):
            raise error_object(enclosing_task, ("{descriptor_string}: "
                                                "formatter({formatter_args}) is malformed\n"
                                                "formatter(...) should only be used to wrap "
                                                'regular expression strings or None (not "{ss}")')
                               .format(descriptor_string=descriptor_string,
                                       formatter_args=formatter_args,
                                       ss=ss)
                               )

        try:
            compiled_regexes.append(re.compile(ss))
        except:
            raise error_object(enclosing_task, ("{descriptor_string}: "
                                                "in formatter({formatter_args}) \n"
                                                'regular expression "{ss}" is malformed\n'
                                                "[{except_str}]")
                               .format(descriptor_string=descriptor_string,
                                       formatter_args=formatter_args,
                                       ss=ss,
                                       except_str=wrap_exception_as_string())
                               )
    return compiled_regexes


# _________________________________________________________________________________________

#   compile_regex

# _________________________________________________________________________________________
def compile_regex(enclosing_task, regex, error_object, descriptor_string, regex_object_name="regex"):
    """
    throw error unless regular expression compiles
    """
    if not len(regex.args) or len(regex.args) > 1 or not isinstance(regex.args[0], path_str_type):
        regex_str = str(regex.args)
        if len(regex.args) > 1:
            regex_str = regex_str[1:-1]
        elif len(regex.args) == 0:
            regex_str = ''
        else:
            regex_str = regex_str
        raise error_object(enclosing_task, ("{descriptor_string}: "
                                            "{regex_object_name}({regex_str}) is malformed\n"
                                            "{regex_object_name}(...) should only be used to wrap a single regular expression string")
                           .format(descriptor_string=descriptor_string,
                                   regex_str=regex_str,
                                   regex_object_name=regex_object_name)
                           )
    try:
        matching_regex = re.compile(regex.args[0])
        return matching_regex
    except:
        raise error_object(enclosing_task, ("{descriptor_string}: "
                                            "regular expression {regex_object_name}('{regex_str}') is malformed\n"
                                            "[{except_str}]")
                           .format(descriptor_string=descriptor_string,
                                   regex_object_name=regex_object_name,
                                   regex_str=regex.args[0],
                                   except_str=wrap_exception_as_string())
                           )

# _________________________________________________________________________________________

#   compile_suffix

# _________________________________________________________________________________________


def compile_suffix(enclosing_task, regex, error_object, descriptor_string):
    """
    throw error unless regular expression compiles
    """
    if not len(regex.args):
        raise error_object(enclosing_task, "%s: " % descriptor_string +
                           "suffix() is malformed.\n" +
                           "suffix(...) should be used to wrap a string matching the suffices of file names")
    if len(regex.args) > 1 or not isinstance(regex.args[0], path_str_type):
        raise error_object(enclosing_task, "%s: " % descriptor_string +
                           "suffix('%s') is malformed.\n" % (regex.args,) +
                           "suffix(...) should only be used to wrap a single string matching the suffices of file names")
    try:
        matching_regex = re.compile("(.*)" + re.escape(regex.args[0]) + "$")
        return matching_regex
    except:
        raise error_object(enclosing_task, "%s: " % descriptor_string +
                           "suffix('%s') is somehow malformed\n" % regex.args[0] +
                           "[%s]" % wrap_exception_as_string())

# _________________________________________________________________________________________

#   check_parallel_parameters

# _________________________________________________________________________________________


def check_parallel_parameters(enclosing_task, params, error_object):
    """
    Helper function for @files
    Checks format of parameters and
    whether there are input and output files specified for each job
    """
    if not len(params):
        raise Exception("@parallel parameters is empty.")

    for job_param in params:
        if isinstance(job_param, path_str_type):
            message = ("Wrong syntax for @parallel.\n"
                       "@parallel(%s)\n" % ignore_unknown_encoder(params) +
                       "If you are supplying parameters for a task "
                       "running as a single job, "
                       "either don't put enclosing brackets at all (with each parameter "
                       "separated by commas) or enclose all parameters as a nested list of "
                       "lists, e.g. [['input', 'output' ...]]. "
                       )
            raise error_object(enclosing_task, message)


# _________________________________________________________________________________________

#   check_files_io_parameters

# _________________________________________________________________________________________
def check_files_io_parameters(enclosing_task, params, error_object):
    """
    Helper function for @files
    Checks format of parameters and
    whether there are input and output files specified for each job
    """
    # if not len(params):
    #    raise Exception("@files I/O parameters is empty.")

    try:
        for job_param in params:
            if isinstance(job_param, path_str_type):
                raise TypeError

            if len(job_param) < 1:
                raise error_object(enclosing_task, "Missing input files for job " +
                                   ignore_unknown_encoder(job_param))
            if len(job_param) < 2:
                raise error_object(enclosing_task, "Missing output files for job " +
                                   ignore_unknown_encoder(job_param))
            # if len(get_strings_in_flattened_sequence(job_param[0:2])) == 0:
            #    raise error_object(enclosing_task, "Input or output file parameters should "
            #                                        "contain at least one or more file names strings. "
            #                                        "Consider using @parallel if you are not using files. " +
            #                                        ignore_unknown_encoder(job_param))
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

# _________________________________________________________________________________________
#
#   expand_nested_tasks_or_globs
#
# ________________________________________________________________________________________


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
    if ((isinstance(p, path_str_type) and is_glob(p) and p in tasksglobs_to_filenames) or
            p.__class__.__name__ == 'Task' or
            isinstance(p, runtime_parameter)):
        return tasksglobs_to_filenames[p]

    #
    # No expansions of strings and dictionaries
    #
    if isinstance(p, (path_str_type, dict)):
        return p

    #
    # Other sequences are recursed down
    #
    elif non_str_sequence(p):
        l = list()
        for pp in p:
            if (isinstance(pp, path_str_type) and pp in tasksglobs_to_filenames):
                l.extend(tasksglobs_to_filenames[pp])
            elif pp.__class__.__name__ == 'Task' or isinstance(pp, runtime_parameter):
                files = tasksglobs_to_filenames[pp]
                # task may have produced a single output: in which case append
                if non_str_sequence(files):
                    l.extend(files)
                else:
                    l.append(files)
            else:
                l.append(expand_nested_tasks_or_globs(
                    pp, tasksglobs_to_filenames))
        return type(p)(l)

    #
    # No expansions of non-string/non-sequences
    #
    else:
        return p


# _________________________________________________________________________________________

#   get_parsed_arguments_str_for_errors

#       helper funciton for parse_task_arguments()

# _________________________________________________________________________________________
def get_parsed_arguments_str_for_errors(task_description, bad_arg_str, unnamed_result_strs, named_result_strs):
    """
    Helper function for parse_task_arguments
        Prints out offending argument (bad_arg_str) in the context of already parsed
        arguments so that we can quickly figure out where the error is coming from
    """
    indent = task_description.find("(") + 1
    parsed_arg_str = ", ".join(unnamed_result_strs + named_result_strs)
    # make function names clearer in arg list
    parsed_arg_str = re.sub(
        r"<function (\w+) at 0x[0-9a-f]+>", r"\1", parsed_arg_str)
    return "\n" + task_description % (parsed_arg_str + ", ...\n" +
                                      # mark out problem
                                      (" " * (indent-5 if indent - 5 > 0 else 0)) + "===> " +
                                      bad_arg_str)


# _________________________________________________________________________________________

#   parse_task_arguments

# _________________________________________________________________________________________
def parse_task_arguments(orig_unnamed_arguments, orig_named_arguments, expected_arguments, task_description):
    """
    Parse arguments parsed into decorators or Pipeline.transform etc.
        Special handling for optional arguments in the middle of argument list
            1) @product
                can have (input, filter, input1, filter1, input2, filter2....)
            2) @transform, @subdivide, @collate, @product, @combinatorics which have
                    (..., [add_inputs(...)|inputs(...)],...)
                    or ([add_inputs=...|replace_inputs=...])
                    or ([add_inputs=add_inputs(...)|replace_inputs=inputs(...)])
        Special handling for variable number of arguments at the end of the argument list
            which all become "extras"

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #   N.B. Missing non-mandatory arguments are returned as an empty list
    #
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                """
    results = {}
    unnamed_arguments = list(orig_unnamed_arguments)
    named_arguments = dict(orig_named_arguments)
    # parsed results in string form for error messages
    unnamed_result_strs = []
    named_result_strs = []

    def parse_add_inputs_args(parsed_arg, input_type, arg_name, modify_inputs_mode, result_strs):
        """
        Parse arguments for add_inputs and replace_inputs, i.e. 'inputs()' and 'add_inputs()'
            input_type =inputs|add_inputs
            arg_name = replace_inputs | add_inputs
            modify_inputs_mode = t_extra_inputs.REPLACE_INPUTS| t_extra_inputs.ADD_TO_INPUTS
        """
        results["modify_inputs_mode"] = modify_inputs_mode
        if input_type == inputs:
            # inputs() only takes a single argument. Throw error otherwise
            if len(parsed_arg.args) != 1:
                err_msg = "inputs() expects a single argument:\n%s" % (
                    get_parsed_arguments_str_for_errors(task_description,   # bad arg in context of parsed
                                                        "%s%r" % (input_type.__name__, tuple(
                                                            parsed_arg.args)),
                                                        unnamed_result_strs,
                                                        named_result_strs))
                raise error_inputs_multiple_args(err_msg)
            # unpack add_inputs / inputs and save results
            results["modify_inputs"] = parsed_arg.args[0]
        else:
            results["modify_inputs"] = parsed_arg.args
        result_strs.append("%s=%r" % (arg_name, parsed_arg.args))

    def check_argument_type(arg_name, parsed_arg, argument_types):
        """
        check if parsed_arg is right type
        """
        if argument_types and not isinstance(parsed_arg, argument_types):
            err_msg = ("The '%s' argument should be %s:\n%s" %
                       (arg_name,                                                  # argument name
                        # type names
                        " or ".join("%s" %
                                    tt.__name__ for tt in argument_types),
                        get_parsed_arguments_str_for_errors(task_description,       # bad arg in context of parsed
                                                            "%s = %r" % (
                                                                arg_name, parsed_arg),
                                                            unnamed_result_strs, named_result_strs)))
            #print (err_msg, file=sys.stderr)
            raise TypeError(err_msg)

        return parsed_arg

    def parse_argument(arg_name, expected_arguments, unnamed_arguments, named_arguments,
                       results, task_description, mandatory, argument_types=None):
        """
        All missing, non-mandatory are empty list
        """

        # ignore if not on list
        if not arg_name in expected_arguments:
            return

        #
        # look among unnamed arguments first
        #
        if len(unnamed_arguments):
            # check correct type
            parsed_arg = check_argument_type(
                arg_name, unnamed_arguments[0], argument_types)
            # save parsed results
            results[arg_name] = parsed_arg
            unnamed_result_strs.append("%s=%r" % (arg_name, parsed_arg))
            del unnamed_arguments[0]

        #
        # then named
        #
        elif arg_name in named_arguments:
            #
            # check correct type
            #
            parsed_arg = check_argument_type(
                arg_name, named_arguments[arg_name], argument_types)
            #
            #   Save parsed results
            #
            results[arg_name] = parsed_arg
            named_result_strs.append("%s=%r" % (arg_name, parsed_arg))
            del named_arguments[arg_name]

        #
        # complain or ignore missing?
        #
        else:
            if mandatory:
                err_msg = "Missing '%s' argument:\n%s" % (
                    arg_name,                                               # argument name
                    get_parsed_arguments_str_for_errors(task_description,   # bad arg in
                                                        arg_name + " = ???",  # context of parsed
                                                        unnamed_result_strs,
                                                        named_result_strs))
                #print (err_msg, file=sys.stderr)
                raise error_missing_args(err_msg)

            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #
            #   N.B. Missing non-mandatory arguments are returned as an empty list
            #
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            else:
                results[arg_name] = []

    #
    #   Missing input is empty list
    #
    parse_argument('input', expected_arguments, unnamed_arguments,
                   named_arguments, results, task_description, mandatory=False)

    #
    #   filter is mandatory if expected
    #
    parse_argument('filter', expected_arguments, unnamed_arguments, named_arguments, results,
                   task_description, mandatory=True, argument_types=(formatter, regex, suffix))

    if "filter" in results:
        if isinstance(results["filter"], suffix):
            parse_argument("output_dir", expected_arguments, [
            ], named_arguments, results, task_description, mandatory=False)

    #
    #   inputN
    #
    if 'inputN' in expected_arguments:
        #
        # put already parsed input and filter into the list
        #
        results["input"] = [results["input"]]
        results["filter"] = [results["filter"]]
        cnt_inputN = 1
        #
        #   parse argument pairs at a time, so long as the second argument is a formatter
        #
        while len(unnamed_arguments) >= 2 and isinstance(unnamed_arguments[1], formatter):
            filter_name = "filter%d" % (cnt_inputN + 1)
            input_name = "input%d" % (cnt_inputN + 1)
            unnamed_result_strs.append("%s=%r" % (
                input_name, unnamed_arguments[0]))
            unnamed_result_strs.append("%s=%r" % (
                filter_name, unnamed_arguments[1]))
            results["input"].append(unnamed_arguments[0])
            results["filter"].append(unnamed_arguments[1])
            cnt_inputN += 1
            del unnamed_arguments[0:2]

        #
        #   parse named arguments while there is a filter2, filter3 etc.
        #
        filter_name = "filter%d" % (cnt_inputN + 1)
        input_name = "input%d" % (cnt_inputN + 1)
        while filter_name in named_arguments:
            results["filter"].append(named_arguments[filter_name])
            named_result_strs.append("%s=%r" % (
                filter_name, named_arguments[filter_name]))
            del named_arguments[filter_name]
            #   parse input2, input3 or leave blank as empty list
            if input_name in named_arguments:
                results["input"].append(named_arguments[input_name])
                named_result_strs.append("%s=%r" % (
                    input_name, named_arguments[input_name]))
                del named_arguments[input_name]
            else:
                results["input"].append([])
            cnt_inputN += 1
            filter_name = "filter%d" % (cnt_inputN + 1)
            input_name = "input%d" % (cnt_inputN + 1)

    #
    #   tuple size is int and mandatory if exists
    #
    parse_argument('tuple_size', expected_arguments, unnamed_arguments, named_arguments,
                   results, task_description, mandatory=True, argument_types=(int,))

    #
    #   add_inputs / inputs are optional
    #
    if 'modify_inputs' in expected_arguments:
        results["modify_inputs_mode"] = t_extra_inputs.KEEP_INPUTS
        results["modify_inputs"] = None
        parse_add_inputs = ((inputs, "inputs", "replace_inputs", t_extra_inputs.REPLACE_INPUTS),
                            (add_inputs, "add_inputs", "add_inputs", t_extra_inputs.ADD_TO_INPUTS))

        if len(unnamed_arguments):
            #
            #   Is add_inputs or inputs in unnamed arguments?
            #       Parse out contents and save in results["replace_inputs"] or results["add_inputs"]
            #
            for input_type, input_type_name, arg_name, modify_inputs_mode in parse_add_inputs:
                parsed_arg = unnamed_arguments[0]
                if isinstance(parsed_arg, input_type):
                    parse_add_inputs_args(
                        parsed_arg, input_type, arg_name, modify_inputs_mode, unnamed_result_strs)
                    del unnamed_arguments[0]
                    break
        #
        #   Otherwise is add_inputs or inputs in named arguments?
        #       Parse out contents only if necessary and save in results["replace_inputs"] or results["add_inputs"]
        #
        if results["modify_inputs_mode"] == t_extra_inputs.KEEP_INPUTS:
            for input_type, input_type_name, arg_name, modify_inputs_mode in parse_add_inputs:
                if arg_name in named_arguments:
                    parsed_arg = named_arguments[arg_name]
                    if isinstance(parsed_arg, input_type):
                        parse_add_inputs_args(
                            parsed_arg, input_type, arg_name, modify_inputs_mode, named_result_strs)
                    else:
                        results["modify_inputs"] = parsed_arg
                    results["modify_inputs_mode"] = modify_inputs_mode
                    del named_arguments[arg_name]
                    break

    #
    #   output is mandatory if exists
    #
    parse_argument('output', expected_arguments, unnamed_arguments,
                   named_arguments, results, task_description, mandatory=True)

    #
    #   extras is mandatory if exists
    #
    if 'extras' in expected_arguments:
        results['extras'] = []
        results['named_extras'] = {}
        if len(unnamed_arguments):
            # move list to results: remember python does shallow copies of lists
            results['extras'] = unnamed_arguments
            unnamed_result_strs.append("%s=%r" % ("extras", unnamed_arguments))
            unnamed_arguments = []
            #del unnamed_arguments[:]
        elif 'extras' in named_arguments:
            # Named extras only
            if isinstance(named_arguments['extras'], dict):
                results["named_extras"] = named_arguments['extras']
            # Unnamed extras only
            elif isinstance(named_arguments['extras'], list):
                results["extras"] = named_arguments['extras']
            # Wrong type: blow up
            else:
                err_msg = ("The extras paramter must be either a list of values\nor a dictionary of named parameter values:\n%s" %
                           get_parsed_arguments_str_for_errors(task_description,
                                                               "extras=%r" % (
                                                                   named_arguments['extras'],),
                                                               unnamed_result_strs,
                                                               named_result_strs))
                raise error_extras_wrong_type(err_msg)

            named_result_strs.append("%s=%r" % (
                "extras", named_arguments['extras']))
            del named_arguments['extras']

    if len(unnamed_arguments):
        err_msg = ("Too many unnamed arguments leftover:\n%s" %
                   get_parsed_arguments_str_for_errors(task_description,       # bad arg in context of parsed
                                                       (", ".join(("%r" % a)
                                                                  for a in unnamed_arguments)),
                                                       unnamed_result_strs, named_result_strs))
        #print (err_msg, file=sys.stderr)
        raise error_too_many_args(err_msg)
    if len(named_arguments):
        err_msg = ("Duplicate, conflicting or unrecognised arguments:\n%s" %
                   get_parsed_arguments_str_for_errors(task_description,       # bad arg in context of parsed
                                                       ", ".join("%s=%r" % (
                                                           k, v) for k, v in named_arguments.items()),
                                                       unnamed_result_strs, named_result_strs))
        #print (err_msg, file=sys.stderr)
        raise error_too_many_args(err_msg)

    return results

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   special markers used by @files_re

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


class combine(object):
    def __init__(self, *args):
        self.args = args


class output_from(object):
    def __init__(self, *args):
        self.args = args

    def __repr__(self, *args):
        return 'output_from%r' % (self.args,)


class runtime_parameter(object):
    def __init__(self, *args):
        if len(args) != 1 or not isinstance(args[0], path_str_type):
            raise Exception(
                "runtime_parameter takes the name of the run time parameter as a single string")
        self.args = args


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Unit Testing code in test/test_ruffus_utility.py


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
