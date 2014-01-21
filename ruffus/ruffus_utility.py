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
import collections
from collections import defaultdict
import multiprocessing.managers
import hashlib
import marshal
import cPickle as pickle
from itertools import izip
import operator
import dbdict


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Constants


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
# file to store history out to
#
RUFFUS_HISTORY_FILE = '.ruffus_history.sqlite'
# If DEFAULT_RUFFUS_HISTORY_FILE is specified in the environment variables, use that instead
if "DEFAULT_RUFFUS_HISTORY_FILE" in os.environ:
    RUFFUS_HISTORY_FILE = os.environ["DEFAULT_RUFFUS_HISTORY_FILE"]


CHECKSUM_FILE_TIMESTAMPS      = 0     # only rerun when the file timestamps are out of date (classic mode)
CHECKSUM_HISTORY_TIMESTAMPS   = 1     # also rerun when the history shows a job as being out of date
CHECKSUM_FUNCTIONS            = 2     # also rerun when function body has changed
CHECKSUM_FUNCTIONS_AND_PARAMS = 3     # also rerun when function parameters or function body change

CHECKSUM_REGENERATE           = 2     # regenerate checksums

#_________________________________________________________________________________________

#   open_job_history

#_________________________________________________________________________________________
def get_default_history_file_name ():
    history_file = RUFFUS_HISTORY_FILE
    #
    #   try path expansion using the main script name
    #
    try:
        import __main__ as main
        path_parts = path_decomposition (os.path.abspath(main.__file__))
        history_file = history_file.format(**path_parts)
    except Exception as err:
        pass
    return history_file

def open_job_history (history_file):
    """
    Given a history file name, opens the correspond sqllite db file and returns the handle
    """
    if not history_file:
        history_file = get_default_history_file_name ()

    return dbdict.open(history_file, picklevalues=True)


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

class JobHistoryChecksum:
    """Class to remember exactly how an output file was created and when."""
    def __init__(self, outfile, mtime, params, task):
        # filename and modification time
        self.outfile = outfile
        self.mtime = mtime
        # checksum exact params used to generate this output file
        self.chksum_params = hashlib.md5(pickle.dumps(params)).hexdigest()
        # checksum the function bytecode as well as the function context
        # Don't use func_code alone-- changing the line number of the function,
        # what global variables are available, etc would all change the checksum
        func_code = marshal.dumps(task.user_defined_work_func.func_code.co_code)


        #
        #   pickle code very defensively, but hopefully without breaking Jake Biesinger's pipelines!
        #
        attributes_to_pickle = [task.user_defined_work_func.func_defaults,
                                task.user_defined_work_func.func_code.co_argcount,
                                task.user_defined_work_func.func_code.co_consts,
                                task.user_defined_work_func.func_code.co_names,
                                task.user_defined_work_func.func_code.co_nlocals,
                                task.user_defined_work_func.func_code.co_varnames]

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





#_________________________________________________________________________________________
#
#   path_decomposition
#
#_________________________________________________________________________________________
def path_decomposition (orig_path):
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
    def recursive_split (a_path):
        """
        split the path into its subdirectories recursively
        """
        if not len(a_path):
            return [[],[]]
        if a_path == "/" or a_path == "//":
            return [ [a_path] , [a_path]]
        sub_path_part, sub_dir_part = os.path.split(a_path)
        if sub_dir_part:
            sub_path_parts, sub_dir_parts = recursive_split (sub_path_part)
            return [ [a_path] + sub_path_parts,
                      [sub_dir_part] + sub_dir_parts]
        else:
            return [ [] , ["/"]]
    #
    if not len(orig_path):
        return {'path': [], 'basename': '', 'ext': '', 'subdir': []}

    # stop normpath from being too clever and removing initial ./ and terminal slash, turning paths into filenames
    if orig_path in [ "./", "/."]:
        a_path = orig_path
    else:
        a_path = os.path.normpath(orig_path)
        if orig_path[0:2] == "./" and a_path[0:2] != "./":
            a_path = "./" + a_path

        if orig_path[-1] == "/" and a_path[-1:] != "/":
            a_path += "/"

    path_part, file_part = os.path.split(a_path)
    file_part, ext_part = os.path.splitext(file_part)
    subpaths, subdirs = recursive_split (path_part)
    return {'basename': file_part,
            'ext':      ext_part,
            'subpath':  subpaths,
            'subdir':   subdirs,
            'path':     path_part}



#_________________________________________________________________________________________
#
#   swap_nesting_order
#
#_________________________________________________________________________________________
def swap_nesting_order (orig_coll):
    """
    Reverse nested order so that coll[3]['a'] becomes coll['a'][3]
    """
    new_dict = defaultdict(dict)
    new_list = []
    for ii, ii_item in enumerate(orig_coll):
        for jj, value in ii_item.iteritems():
            if isinstance(jj, int):
                # resize
                new_list += [{}]*(jj + 1 - len(new_list))
                new_list[jj][ii] = value
            else:
                new_dict[jj][ii] = value
    return new_list, new_dict

#_________________________________________________________________________________________
#
#   swap_doubly_nested_order
#
#_________________________________________________________________________________________
def swap_doubly_nested_order (orig_coll):
    """
    Reverse nested order so that coll[3]['a'] becomes coll['a'][3]
    """
    new_dict = dict()
    new_list = []
    for ii, ii_item in enumerate(orig_coll):
        for jj, jj_item in enumerate(ii_item):
            for kk, value in jj_item.iteritems():
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

#_________________________________________________________________________________________
#
#   get_all_paths_components
#
#_________________________________________________________________________________________
def get_all_paths_components(paths, compiled_regex):
    """
        For each path in a list,
            returns a dictionary identifying the components of a file path.
            This includes both the components of a path:
                basename: (any) base (file) name of the path not including the extension. No slash included
                ext:      (any) extension of the path including the "."
                path:     a list of subpaths created by removing subdirectory names
                subdir:   a list of subdirectory names from the most nested to the root
            and regular expression matches
                The keys are the index or name of the capturing group.

            If compiled_regex is specified, and the regular expression does not match, an empty
            dictionary is returned.

        For example, the following three paths give:
            get_all_paths_components(["/a/b/c/sample1.bam",
                                      "dbsnp15.vcf",
                                      "/test.txt"],
                                     r"(.*)(?P<id>\d+)\..+")
            [   {
                    0:          '/a/b/c/sample1.bam',           // captured by index
                    1:          '/a/b/c/sample',                // captured by index
                    'id':       '1'                             // captured by name
                    'ext':      '.bam',
                    'subdir':   ['c', 'b', 'a', '/'],
                    'subpath':  ['/a/b/c', '/a/b', '/a', '/'],
                    'path':     '/a/b/c',
                    'basename': 'sample1',
                },
                {
                    0: 'dbsnp15.vcf',                           // captured by index
                    1: 'dbsnp1',                                // captured by index
                    'id': '5'                                   // captured by name
                    'ext': '.vcf',
                    'subdir': [],
                    'path': [],
                    'basename': 'dbsnp15',
                },

                // no regular expression match
                // everything fails!
                {
                }
            ]
    """
    def regex_match_str_list(test_str_list, compiled_regex):
        if isinstance(compiled_regex, basestring):
            compiled_regex = re.compile(compiled_regex)
        matches = [compiled_regex.search(ss) for ss in test_str_list]

        matchdicts = []
        for mm in matches:
            if mm == None:
                matchdicts.append(None)
            else:
                if mm.lastindex == None:
                    matchdicts.append({})
                else:
                    # no dictionary comprehensions in python 2.6 :-(
                    #matchdicts.append({i : mm.group(i) for i in (range(mm.lastindex) + mm.groupdict().keys())})
                    matchdicts.append(dict((i, mm.group(i)) for i in (range(mm.lastindex + 1) + mm.groupdict().keys())))
        return matchdicts
    #
    #   merge regular expression matches and path decomposition
    #
    path_components = [path_decomposition(pp) for pp in paths]
    if compiled_regex == None:
        return path_components
    else:
        regex_match_components = regex_match_str_list(paths, compiled_regex)
        both_components = []
        for rr, pp in izip(regex_match_components, path_components):
            if rr == None:
                #
                #   previously failed regular expression matches would taint file
                #   decomposition as well: too clever by half
                #
                #both_components.append({})
                #
                both_components.append(pp)
            else:
                #
                #   regular expression matches override file decomposition values in
                #       case of clashes between predefined keys such as "basename" and
                #       regular expression named capture groups
                #
                pp.update(rr)
                both_components.append(pp)
        return both_components



#_________________________________________________________________________________________
#
#   apply_func_to_sequence
#
#_________________________________________________________________________________________
def apply_func_to_sequence(seq, func, tuple_of_conforming_types = (basestring,), tuple_of_sequences_types = (list, tuple,set)):
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


#_________________________________________________________________________________________
#
#   t_regex_replace
#
#_________________________________________________________________________________________
class t_regex_replace(object):
    def __init__ (self, filename, regex_str, compiled_regex, regex_or_suffix):
        self.regex_or_suffix = regex_or_suffix
        self.compiled_regex = compiled_regex
        self.regex_str = regex_str
        self.filename = filename
    def __call__(self, p):
        #
        #   check if substitution pattern is mis-specified
        #
        if "\1"in p or "\2" in p :
            raise error_unescaped_regular_expression_forms("['%s'] "  % (p.replace("\1", r"\1").replace("\2", r"\2")) +
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
            (res_str, cnt_replacements) = self.compiled_regex.subn(match_p, self.filename)
            if cnt_replacements == 0:
                raise error_input_file_does_not_match("File '%s' does not match suffix('%s') and pattern '%s'" % (self.filename, self.regex_str, p))
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
        except re.error as e:
            err_str = str(e)
            raise fatal_error_input_file_does_not_match("File '%s' does not match regex('%s') and pattern '%s':\n\t%s\n" % (self.filename, self.regex_str, p, err_str))
        except IndexError as e:
            err_str = str(e)
            raise fatal_error_input_file_does_not_match("File '%s' does not match regex('%s') and pattern '%s':\n\t%s\n" % (self.filename, self.regex_str, p, err_str))

        #except (re.error, IndexError):
            #err_str = str(sys.exc_info()[1]),

        raise error_input_file_does_not_match("File '%s' does not match regex('%s') and pattern '%s'\n%s\n" % (self.filename, self.regex_str, p, err_str))

#_________________________________________________________________________________________
#
#   t_formatter_replace
#
#_________________________________________________________________________________________
class t_formatter_replace(object):
    def __init__ (self, filenames, regex_str, compiled_regex = None):
        self.filenames = filenames
        # get the full absolute, normalised paths
        filenames = [os.path.abspath(f) for f in filenames]
        self.path_regex_components = get_all_paths_components(filenames, compiled_regex)
        self.regex_str = "'" + regex_str + "'" if regex_str else ""

    def __call__(self, p):
        # swapped nesting order makes the syntax easier to explain:
        #   The first level of indirection is always the path component
        #   So basename[0] is the file name for the first file
        #   This looks better than the normal 0[basename]

        # some contortions because format decodes {0} as an offset into a list and not not a lookup into a dict...
        dl, dd = swap_nesting_order(self.path_regex_components)
        try:
            return p.format(*dl, **dd)
        except (KeyError, IndexError):
            raise error_input_file_does_not_match("Field '%s' in ('%s') using formatter(%s) fails to match Files '%s'."
                                                  "."
                                                  % (   str(sys.exc_info()[1]),
                                                        p,
                                                        self.regex_str,
                                                        self.filenames))


#_________________________________________________________________________________________
#
#   t_nested_formatter_replace
#
#_________________________________________________________________________________________
class t_nested_formatter_replace(object):
    def __init__ (self, filenames, regex_strings, compiled_regexes):
        if len(filenames) != len(regex_strings) or len(filenames) != len(compiled_regexes):
            raise Exception("Logic Error.")
        self.filenames = filenames
        # get the full absolute, normalised paths
        filenames = [[os.path.abspath(f) for f in filegroups] for filegroups in filenames]
        self.path_regex_components = [get_all_paths_components(f, r) for (f,r) in zip(filenames, compiled_regexes)]
        self.regex_strings = regex_strings

    def __call__(self, p):
        # swapped nesting order makes the syntax easier to explain:
        #   The first level of indirection is always the path component
        #   So basename[0] is the file name for the first file
        #   This looks better than the normal 0[basename]

        # some contortions because format decodes {0} as an offset into a list and not not a lookup into a dict...
        dl, dd = swap_doubly_nested_order(self.path_regex_components)
        try:
            return p.format(*dl, **dd)
        except (KeyError, IndexError):
            formatter_str = ", ".join("formatter(%s)" % (s if not s else "'%s'" %s) for s in self.regex_strings)
            raise error_input_file_does_not_match("Unmatched field %s in ('%s') using %s fails to match Files '%s'"
                                                  "."
                                                  % (   str(sys.exc_info()[1]),
                                                        p,
                                                        formatter_str,
                                                        self.filenames))


#_________________________________________________________________________________________
#
#   regex_replace
#
#_________________________________________________________________________________________

#
#   Perform normal regular expression substitution
#
REGEX_SUBSTITUTE               = 0
#
#   An extra peculiar mode to help suffix along:
#   Suffix regular expression have an implicit capture for everything up to the specified
#       suffix text

#
#   By default, replaces the suffix part by adding leading r"\1" to the substitution pattern
#       If r"\1" is already specified in the pattern, then we presume you know what
#       you are doing, and will let you get along with it
#
SUFFIX_SUBSTITUTE              = 1

#
#   REGEX_SUBSTITUTE is used for suffix() matches in 'extra' arguments (additional to output)
#   which are strings
#
#   Complete replacement happens. If you wish to retain the prefix text
#       before the suffix, you can do so by adding r"\1"
#

def regex_replace(filename, regex_str, compiled_regex, substitution_patterns, regex_or_suffix = REGEX_SUBSTITUTE):
    return apply_func_to_sequence(substitution_patterns, t_regex_replace(filename, regex_str, compiled_regex, regex_or_suffix))

def formatter_replace (filenames, regex_str, compiled_regex, substitution_patterns):
    return apply_func_to_sequence(substitution_patterns, t_formatter_replace(filenames, regex_str, compiled_regex))

def nested_formatter_replace (filenames, regex_strings, compiled_regexes, substitution_patterns):
    return apply_func_to_sequence(substitution_patterns, t_nested_formatter_replace(filenames, regex_strings, compiled_regexes))


#_________________________________________________________________________________________

#   non_str_sequence

#_________________________________________________________________________________________
def non_str_sequence (arg):
    """
    Whether arg is a sequence.
    We treat strings / dicts however as a singleton not as a sequence

    """
    #will only dive into list and set, everything else is not regarded as a sequence
    #loss of flexibility but more conservative
    #if (isinstance(arg, (basestring, dict, multiprocessing.managers.DictProxy))):
    if (not isinstance(arg, (list, tuple, set))):
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
    if isinstance(p, basestring):
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
    if isinstance(p, basestring):
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
    if isinstance(p, basestring):
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
        if " object" in s and s[0] == '<' and s[-1] == '>':
            pos = s.find(" object")
            s = "<" + s[1:pos].replace("__main__.", "") + ">"
        return s.replace('"', "'")
    except:
        return "<%s>" % str(obj.__class__).replace('"', "'")

def shorten_filenames_encoder (obj):
    if non_str_sequence (obj):
        return "[%s]" % ", ".join(map(shorten_filenames_encoder, obj))
    if isinstance(obj, basestring):
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
    if (isinstance(p, collections.Callable)):
    #if (type(p) == types.FunctionType):
        tasks.add(p)
    elif isinstance(p, runtime_parameter):
        runtime_data_names.add(p)

    #
    #   output_from treats all arguments as tasks or task names
    #
    elif isinstance(p, output_from):
        for pp in p.args:
            get_nested_tasks_or_globs(pp, True, runtime_data_names, tasks, globs)

    elif isinstance(p, basestring):
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
    if isinstance(p, collections.Callable):
    #if type(p) == types.FunctionType:
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
    if isinstance(p, basestring):
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

#   regex

#_________________________________________________________________________________________
class formatter(object):
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
def compile_regex(enclosing_task, regex, error_object, descriptor_string, regex_object_name = "regex"):
    """
    throw error unless regular expression compiles
    """
    if not len(regex.args) or len(regex.args) > 1 or not isinstance(regex.args[0], basestring):
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
                                    .format(descriptor_string = descriptor_string,
                                            regex_str = regex_str,
                                            regex_object_name = regex_object_name)
                           )
    try:
        matching_regex = re.compile(regex.args[0])
        return matching_regex
    except:
        raise error_object(enclosing_task, ("{descriptor_string}: "
                                   "regular expression {regex_object_name}('{regex_str}') is malformed\n"
                                    "[{except_str}]")
                                    .format(descriptor_string = descriptor_string,
                                            regex_object_name = regex_object_name,
                                            regex_str = regex.args[0],
                                            except_str = wrap_exception_as_string())
                           )

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
    if len(regex.args) > 1 or not isinstance(regex.args[0], basestring):
        raise error_object(enclosing_task, "%s: " % descriptor_string +
                                   "suffix('%s') is malformed.\n" % (regex.args,) +
                                    "suffix(...) should only be used to wrap a single string matching the suffices of file names")
    try:
        matching_regex = re.compile("(.*)" + re.escape(regex.args[0]) + "$")
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
        if isinstance(job_param, basestring):
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
    #if not len(params):
    #    raise Exception("@files I/O parameters is empty.")

    try:
        for job_param in params:
            if isinstance(job_param, basestring):
                raise TypeError

            if len(job_param) < 1:
                raise error_object(enclosing_task, "Missing input files for job " +
                                                    ignore_unknown_encoder(job_param))
            if len(job_param) < 2:
                raise error_object(enclosing_task, "Missing output files for job " +
                                                    ignore_unknown_encoder(job_param))
            #if len(get_strings_in_nested_sequence(job_param[0:2])) == 0:
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
    if (    (isinstance(p, basestring) and is_glob(p) and p in tasksglobs_to_filenames) or
            p.__class__.__name__ == '_task'     or
            isinstance(p, runtime_parameter)    ):
        return tasksglobs_to_filenames[p]

    #
    # No expansions of strings and dictionaries
    #
    if isinstance(p, (basestring, dict)):
        return p

    #
    # Other sequences are recursed down
    #
    elif non_str_sequence(p):
        l = list()
        for pp in p:
            if (isinstance(pp, basestring) and pp in tasksglobs_to_filenames):
                l.extend(tasksglobs_to_filenames[pp])
            elif pp.__class__.__name__ == '_task' or isinstance(pp, runtime_parameter):
                files = tasksglobs_to_filenames[pp]
                # task may have produced a single output: in which case append
                if non_str_sequence(files):
                    l.extend(files)
                else:
                    l.append(files)
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
        if len(args) != 1 or not isinstance(args[0], basestring):
            raise Exception("runtime_parameter takes the name of the run time parameter as a single string")
        self.args = args


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Unit Testing code in test/test_ruffus_utility.py


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

