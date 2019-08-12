from __future__ import print_function
import re
from . import dbdict
from .ruffus_utility import *
from .ruffus_utility import shorten_filenames_encoder, FILE_CHECK_RETRY, FILE_CHECK_SLEEP
from .ruffus_exceptions import *

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


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
import os
import sys
import time
import glob
from itertools import groupby
import itertools
from collections import defaultdict
from time import strftime, gmtime

if sys.hexversion >= 0x03000000:
    # everything is unicode in python3
    path_str_type = str
else:
    path_str_type = basestring


class t_combinatorics_type:
    (COMBINATORICS_PRODUCT, COMBINATORICS_PERMUTATIONS,
        COMBINATORICS_COMBINATIONS, COMBINATORICS_COMBINATIONS_WITH_REPLACEMENT) = list(range(4))


def get_readable_path_str(original_path, max_len):
    """
    Truncates path to max_len characters if necessary
    If the result is a path within nested directory, will remove partially
        truncated directories names
    """
    if len(original_path) < max_len:
        return original_path
    truncated_name = original_path[-(max_len - 5):]
    if "/" not in truncated_name:
        return "[...]" + truncated_name
    return "[...]" + re.sub("^[^/]+", "", truncated_name)


def epoch_seconds_to_str(epoch_seconds):
    """
    Converts seconds since epoch into nice string with date and time to 2 significant
        digits for seconds
    """
    #   returns 24 char long  25 May 2011 23:37:40.12
    time_str = strftime("%d %b %Y %H:%M:%S", gmtime(epoch_seconds))
    #
    fraction_of_second_as_str = (
        "%.2f" % (epoch_seconds - int(epoch_seconds)))[1:]
    #   or fraction = ("%.2f" % (divmod(epoch_seconds, 1)[1]))[1:]
    return (time_str + fraction_of_second_as_str)


err_msg_no_regex_match = ("No jobs were run because no file names matched.\n"
                          "Please make sure that the regular expression is correctly specified.")
err_msg_empty_files_parameter = ("@files() was empty, i.e. no files were specified.\n"
                                 "Please make sure this is by design.")


class t_file_names_transform(object):
    """
    Does the work for generating output / "extra input" / "extra" filenames
        input
            - a set of file names (derived from tasks, globs, hard coded file names)
            - a specification (e.g. a new suffix, a regular expression substitution pattern)
        output
            - a new file name

    N.B. Is this level of abstraction adequate?
        1) On one hand, this is a simple extension of the current working design
        2) On the other, we throw away the nested structure of tasks / globs on one hand
           and the nested structure of the outputs on the other hand.
    """

    def substitute(self, starting_file_names, pattern):
        pass

    # overriden only in t_suffix_file_names_transform
    # only suffix() behaves differently for output and extra files...
    def substitute_output_files(self, starting_file_names, pattern):
        return self.substitute(starting_file_names, pattern)


class t_suffix_file_names_transform(t_file_names_transform):
    """
    Does the work for generating output / "extra input" / "extra" filenames
        replacing a specified suffix
    """

    def __init__(self, enclosing_task, suffix_object, error_type, descriptor_string, output_dir):
        self.matching_regex = compile_suffix(
            enclosing_task, suffix_object, error_type, descriptor_string)
        self.matching_regex_str = suffix_object.args[0]
        self.output_dir = output_dir

    def substitute(self, starting_file_names, pattern):
        if self.output_dir == []:
            return regex_replace(starting_file_names[0], self.matching_regex_str, self.matching_regex, pattern)
        else:
            # change directory of starting file and return substitution
            starting_file_name = os.path.join(
                self.output_dir, os.path.split(starting_file_names[0])[1])
            return regex_replace(starting_file_name, self.matching_regex_str, self.matching_regex, pattern)
        return

    def substitute_output_files(self, starting_file_names, pattern):
        if self.output_dir == []:
            return regex_replace(starting_file_names[0], self.matching_regex_str, self.matching_regex, pattern, SUFFIX_SUBSTITUTE)
        else:
            # change directory of starting file and return substitution
            starting_file_name = os.path.join(
                self.output_dir, os.path.split(starting_file_names[0])[1])
            return regex_replace(starting_file_name, self.matching_regex_str, self.matching_regex, pattern, SUFFIX_SUBSTITUTE)


class t_regex_file_names_transform(t_file_names_transform):
    """
    Does the work for generating output / "extra input" / "extra" filenames
        replacing a specified regular expression
    """

    def __init__(self, enclosing_task, regex_object, error_type, descriptor_string):
        self.matching_regex = compile_regex(
            enclosing_task, regex_object, error_type, descriptor_string)
        self.matching_regex_str = regex_object.args[0]

    def substitute(self, starting_file_names, pattern):
        return regex_replace(starting_file_names[0], self.matching_regex_str, self.matching_regex, pattern)


class t_formatter_file_names_transform(t_file_names_transform):
    """
    Does the work for generating output / "extra input" / "extra" filenames
        replacing a specified regular expression
    """

    def __init__(self, enclosing_task, format_object, error_type, descriptor_string):
        self.matching_regexes = []
        self.matching_regex_strs = []
        if len(format_object.args):
            self.matching_regexes = compile_formatter(
                enclosing_task, format_object, error_type, descriptor_string)
            self.matching_regex_strs = list(format_object.args)

    def substitute(self, starting_file_names, pattern):
        # note: uses all file names
        return formatter_replace(starting_file_names, self.matching_regex_strs, self.matching_regexes, pattern)


class t_nested_formatter_file_names_transform(t_file_names_transform):
    """
    Does the work for generating output / "extra input" / "extra" filenames
        apply a whole series of regular expresions to a whole series of input
    """

    def __init__(self, enclosing_task, format_objects, error_type, descriptor_string):
        self.list_matching_regex = []
        self.list_matching_regex_str = []

        for format_object in format_objects:
            if len(format_object.args):
                self.list_matching_regex.append(compile_formatter(
                    enclosing_task, format_object, error_type, descriptor_string))
                self.list_matching_regex_str.append(list(format_object.args))
            else:
                self.list_matching_regex.append([])
                self.list_matching_regex_str.append([])

    def substitute(self, starting_file_names, pattern):
        # note: uses all file names
        return nested_formatter_replace(starting_file_names, self.list_matching_regex_str, self.list_matching_regex, pattern)


# _________________________________________________________________________________________

#   t_params_tasks_globs_run_time_data

# _________________________________________________________________________________________
class t_params_tasks_globs_run_time_data(object):
    """
    After parameters are parsed into tasks, globs, runtime data
    """

    def __init__(self, params, tasks, globs, runtime_data_names):
        self.params = params
        self.tasks = tasks
        self.globs = globs
        self.runtime_data_names = runtime_data_names

    def __str__(self):
        return str(self.params)

    def param_iter(self):
        for p in self.params:
            yield t_params_tasks_globs_run_time_data(p, self.tasks, self.globs,
                                                     self.runtime_data_names)

    def unexpanded_globs(self):
        """
        do not expand globs
        """
        return t_params_tasks_globs_run_time_data(self.params, self.tasks, [],
                                                  self.runtime_data_names)

    def single_file_to_list(self):
        """
        if parameter is a simple string, wrap that in a list unless it is glob
        Useful for simple @transform cases
        """
        if isinstance(self.params, path_str_type) and not is_glob(self.params):
            self.params = [self.params]
            return True
        return False

    def file_names_transformed(self, filenames, file_names_transform):
        """
        return clone with the filenames / globs transformed by the supplied transform object
        """
        output_glob = file_names_transform.substitute(filenames, self.globs)
        output_param = file_names_transform.substitute(filenames, self.params)
        return t_params_tasks_globs_run_time_data(output_param, self.tasks, output_glob,
                                                  self.runtime_data_names)

    def output_file_names_transformed(self, filenames, file_names_transform):
        """
        return clone with the filenames / globs transformed by the supplied transform object
        """
        output_glob = file_names_transform.substitute_output_files(
            filenames, self.globs)
        output_param = file_names_transform.substitute_output_files(
            filenames, self.params)
        return t_params_tasks_globs_run_time_data(output_param, self.tasks, output_glob,
                                                  self.runtime_data_names)
    #
    #   deprecated
    #

    def regex_replaced(self, filename, regex, regex_or_suffix=REGEX_SUBSTITUTE):
        output_glob = regex_replace(
            filename, regex, self.globs, regex_or_suffix)
        output_param = regex_replace(
            filename, regex, self.params, regex_or_suffix)
        return t_params_tasks_globs_run_time_data(output_param, self.tasks, output_glob,
                                                  self.runtime_data_names)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

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
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
# _________________________________________________________________________________________

#   needs_update_check_directory_missing

#       N.B. throws exception if this is an ordinary file, not a directory


# _________________________________________________________________________________________
def needs_update_check_directory_missing(*params, **kwargs):
    """
    Called per directory:
        Does it exist?
        Is it an ordinary file not a directory? (throw exception
    """
    if len(params) == 1:
        dirs = params[0]
    elif len(params) == 2:
        dirs = params[1]
    else:
        raise Exception(
            "Wrong number of arguments in mkdir check %s" % (params,))

    missing_directories = []
    for d in get_strings_in_flattened_sequence(dirs):
        # print >>sys.stderr, "check directory missing %d " % os.path.exists(d) # DEBUG
        if not os.path.exists(d):
            missing_directories.append(d)
            continue
            # return True, "Directory [%s] is missing" % d
        if not os.path.isdir(d):
            raise error_not_a_directory(
                "%s already exists but as a file, not a directory" % d)

    if len(missing_directories):
        if len(missing_directories) > 1:
            return True, ": Directories %r are missing" % (", ".join(missing_directories))
        else:
            return True, ": Directories %r is missing" % (missing_directories[0])
    return False, "All directories exist"


def check_input_files_exist(*params):
    """If inputs are missing then there is no way a job can run
    successful. Must throw exception.

    This extra function is a hack to make sure input files exists
    right before job is called for better error messages, and to save
    things from blowing up inside the task function.

    In practice, we have observed a sporadic time-lag between a task
    completing on a remote node and an output file appearing in the
    expected location on the host running the ruffus pipeline. This
    causes a subsequent task to fail with missing input file even
    though the file will appear a few seconds later. It is not clear
    if this is an issue of a poorly configured storage, but a retry
    behaviour has been implemented to work around such issues.

    """
    if len(params):
        input_files = params[0]

        for f in get_strings_in_flattened_sequence(input_files):
            tries = FILE_CHECK_RETRY
            while tries > 0:
                if not os.path.exists(f):
                    if os.path.lexists(f):
                        raise MissingInputFileError("No way to run job: " +
                                                    "Input file '%s' is a broken symbolic link." % f)
                    tries -= 1
                    time.sleep(FILE_CHECK_SLEEP)
                    continue
                break
            if tries <= 0:
                raise MissingInputFileError("No way to run job: " +
                                            "Input file '%s' does not exist" % f)


def needs_update_check_exist(*params, **kwargs):
    """
    Given input and output files, see if all exist
    Each can be

        #. string: assumed to be a filename "file1"
        #. any other type
        #. arbitrary nested sequence of (1) and (2)

    """
    if "verbose_abbreviated_path" in kwargs:
        verbose_abbreviated_path = kwargs["verbose_abbreviated_path"]
    else:
        verbose_abbreviated_path = -55

    # missing output means build
    if len(params) < 2:
        return True, "i/o files not specified"

    i, o = params[0:2]
    i = get_strings_in_flattened_sequence(i)
    o = get_strings_in_flattened_sequence(o)

    #
    # build: missing output file
    #
    if len(o) == 0:
        return True, "Missing output file"

    # missing input / output file means always build
    missing_files = []
    for io in (i, o):
        for p in io:
            if not os.path.exists(p):
                missing_files.append(p)
    if len(missing_files):
        return True, "...\n        Missing file%s %s" % ("s" if len(missing_files) > 1 else "",
                                                         shorten_filenames_encoder(missing_files,
                                                                                   verbose_abbreviated_path))

    #
    #   missing input -> build only if output absent
    #
    if len(i) == 0:
        return False, "Missing input files"

    return False, "Up to date"


# _________________________________________________________________________________________

#   needs_update_check_modify_time

# _________________________________________________________________________________________
def needs_update_check_modify_time(*params, **kwargs):
    """
    Given input and output files, see if all exist and whether output files are later than input files
    Each can be

        #. string: assumed to be a filename "file1"
        #. any other type
        #. arbitrary nested sequence of (1) and (2)

    """
    # conditions for rerunning a job:
    #   1. forced to rerun entire taskset
    #   2. 1+ Output files don't exist
    #   3. 1+ of input files is newer than 1+ output files  -- ruffus does this level right now...
    #   4. internal completion time for that file is out of date   # incomplete runs will be rerun automatically
    #   5. checksum of code that ran the file is out of date       # changes to function body result in rerun
    #   6. checksum of the args that ran the file are out of date  # appropriate config file changes result in rerun
    try:
        task = kwargs['task']
    except KeyError:
        # allow the task not to be specified and fall back to classic
        # file timestamp behavior (either this or fix all the test cases,
        # which often don't have proper tasks)
        class Namespace:
            pass
        task = Namespace()
        task.checksum_level = CHECKSUM_FILE_TIMESTAMPS

    if "verbose_abbreviated_path" in kwargs:
        verbose_abbreviated_path = kwargs["verbose_abbreviated_path"]
    else:
        verbose_abbreviated_path = -55

    try:
        job_history = kwargs['job_history']
    except KeyError:
        # allow job_history not to be specified and reopen dbdict file redundantly...
        #   Either this or fix all the test cases
        #job_history = dbdict.open(RUFFUS_HISTORY_FILE, picklevalues=True)
        print("Oops: Should only appear in test code", file=sys.stderr)
        job_history = open_job_history(None)

    # missing output means build
    if len(params) < 2:
        return True, ""

    i, o = params[0:2]
    i = get_strings_in_flattened_sequence(i)
    o = get_strings_in_flattened_sequence(o)

    #
    # build: missing output file
    #
    if len(o) == 0:
        return True, "Missing output file"

    # missing input / output file means always build
    missing_files = []
    for io in (i, o):
        for p in io:
            if not os.path.exists(p):
                missing_files.append(p)
    if len(missing_files):
        return True, "...\n        Missing file%s %s" % ("s" if len(missing_files) > 1 else "",
                                                         shorten_filenames_encoder(missing_files,
                                                                                   verbose_abbreviated_path))
    #
    #   N.B. Checkpointing uses relative paths
    #

    # existing files, but from previous interrupted runs
    if task.checksum_level >= CHECKSUM_HISTORY_TIMESTAMPS:
        incomplete_files = []
        set_incomplete_files = set()
        func_changed_files = []
        set_func_changed_files = set()
        param_changed_files = []
        set_param_changed_files = set()
        # for io in (i, o):
        #    for p in io:
        #        if p not in job_history:
        #            incomplete_files.append(p)
        for p in o:
            if os.path.relpath(p) not in job_history and p not in set_incomplete_files:
                incomplete_files.append(p)
                set_incomplete_files.add(p)
        if len(incomplete_files):
            return True, "Uncheckpointed file%s (left over from a failed run?):\n        %s" % ("s" if len(incomplete_files) > 1 else "",
                                                                                                shorten_filenames_encoder(incomplete_files,
                                                                                                                          verbose_abbreviated_path))
        # check if function that generated our output file has changed
        for o_f_n in o:
            rel_o_f_n = os.path.relpath(o_f_n)
            old_chksum = job_history[rel_o_f_n]
            new_chksum = JobHistoryChecksum(rel_o_f_n, None, params[2:], task)
            if task.checksum_level >= CHECKSUM_FUNCTIONS_AND_PARAMS and \
                    new_chksum.chksum_params != old_chksum.chksum_params and \
                    o_f_n not in set_func_changed_files:
                param_changed_files.append(o_f_n)
                set_param_changed_files.add(o_f_n)
            elif task.checksum_level >= CHECKSUM_FUNCTIONS and \
                    new_chksum.chksum_func != old_chksum.chksum_func and \
                    o_f_n not in set_func_changed_files:
                func_changed_files.append(o_f_n)
                set_func_changed_files.add(o_f_n)

        if len(func_changed_files):
            return True, "Pipeline function has changed:\n        %s" % (shorten_filenames_encoder(func_changed_files,
                                                                                                   verbose_abbreviated_path))
        if len(param_changed_files):
            return True, "Pipeline parameters have changed:\n        %s" % (shorten_filenames_encoder(param_changed_files,
                                                                                                      verbose_abbreviated_path))

    #
    #   missing input -> build only if output absent or function is out of date
    #
    if len(i) == 0:
        return False, "Missing input files"

    #
    #   get sorted modified times for all input and output files
    #
    filename_to_times = [[], []]
    file_times = [[], []]

    # _____________________________________________________________________________________

    #   pretty_io_with_date_times

    # _____________________________________________________________________________________

    def pretty_io_with_date_times(filename_to_times):

        # sort
        for io in range(2):
            filename_to_times[io].sort()

        #
        #   add asterisk for all files which are causing this job to be out of date
        #
        file_name_to_asterisk = dict()
        oldest_output_mtime = filename_to_times[1][0][0]
        for mtime, file_name in filename_to_times[0]:
            file_name_to_asterisk[file_name] = "*" if mtime >= oldest_output_mtime else " "
        newest_output_mtime = filename_to_times[0][-1][0]
        for mtime, file_name in filename_to_times[1]:
            file_name_to_asterisk[file_name] = "*" if mtime <= newest_output_mtime else " "

        #
        #   try to fit in 100 - 15 = 85 char lines
        #   date time ~ 25 characters so limit file name to 55 characters
        #
        msg = "\n"
        category_names = "Input", "Output"
        for io in range(2):
            msg += "  %s files:\n" % category_names[io]
            for mtime, file_name in filename_to_times[io]:
                file_datetime_str = epoch_seconds_to_str(mtime)
                msg += ("   " +                                         # indent
                        # asterisked out of date files
                        file_name_to_asterisk[file_name] + " " +
                        file_datetime_str + ": " +                      # date time of file
                        shorten_filenames_encoder(file_name,
                                                  verbose_abbreviated_path) + "\n")    # file name truncated to 55
        return msg

    #
    #   Ignore output file if it is found in the list of input files
    #       By definition they have the same timestamp,
    #       and the job will otherwise appear to be out of date
    #
    #   Symbolic links followed
    real_input_file_names = set()
    for input_file_name in i:
        rel_input_file_name = os.path.relpath(input_file_name)
        real_input_file_names.add(os.path.realpath(input_file_name))
        file_timestamp = os.path.getmtime(input_file_name)
        if task.checksum_level >= CHECKSUM_HISTORY_TIMESTAMPS and rel_input_file_name in job_history:
            old_chksum = job_history[rel_input_file_name]
            mtime = max(file_timestamp, old_chksum.mtime)
        else:
            mtime = file_timestamp
        filename_to_times[0].append((mtime, input_file_name))
        file_times[0].append(mtime)

    # for output files, we need to check modification time *in addition* to
    # function and argument checksums...
    for output_file_name in o:
        #
        #   Ignore output files which are just symbolic links to input files or passed through
        #       from input to output
        #
        real_file_name = os.path.realpath(output_file_name)
        if real_file_name in real_input_file_names:
            continue

        rel_output_file_name = os.path.relpath(output_file_name)
        file_timestamp = os.path.getmtime(output_file_name)
        if task.checksum_level >= CHECKSUM_HISTORY_TIMESTAMPS:
            old_chksum = job_history[rel_output_file_name]
            if old_chksum.mtime > file_timestamp and old_chksum.mtime - file_timestamp > 1.1:
                mtime = file_timestamp
            # use check sum time in preference if both are within one second
            #   (suggesting higher resolution
            else:
                mtime = old_chksum.mtime
        else:
            mtime = file_timestamp
        file_times[1].append(mtime)
        filename_to_times[1].append((mtime, output_file_name))

    #
    #   Debug: Force print modified file names and times
    #
    # if len(file_times[0]) and len (file_times[1]):
    #    print >>sys.stderr, pretty_io_with_date_times(filename_to_times), file_times, (max(file_times[0]) >= min(file_times[1]))
    # else:
    #    print >>sys.stderr, i, o

    #
    #   update if any input file >= (more recent) output file
    #
    if len(file_times[0]) and len(file_times[1]) and max(file_times[0]) >= min(file_times[1]):
        return True, pretty_io_with_date_times(filename_to_times)

    if "return_file_dates_when_uptodate" in kwargs and kwargs["return_file_dates_when_uptodate"]:
        return False, "Up to date\n" + pretty_io_with_date_times(filename_to_times)

    return False, "Up to date"


# _________________________________________________________________________________________
#
#   is_file_re_combining
#
# _________________________________________________________________________________________
def is_file_re_combining(old_args):
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


# _________________________________________________________________________________________

#   file_names_from_tasks_globs

# _________________________________________________________________________________________
def file_names_from_tasks_globs(files_task_globs,
                                runtime_data, do_not_expand_single_job_tasks=False):
    """
    Replaces glob specifications and tasks with actual files / task output
    """

    # special handling for chaining tasks which conceptual have a single job
    #       i.e. @merge and @files/@parallel with single job parameters
    if files_task_globs.params.__class__.__name__ == 'Task' and do_not_expand_single_job_tasks:
        return files_task_globs.params._get_output_files(True, runtime_data)

    task_or_glob_to_files = dict()

    # look up globs and tasks
    for g in files_task_globs.globs:
        # check whether still is glob pattern after transform
        # {} are particularly suspicious...
        if is_glob(g):
            task_or_glob_to_files[g] = sorted(glob.glob(g))
    for t in files_task_globs.tasks:
        of = t._get_output_files(False, runtime_data)
        task_or_glob_to_files[t] = of
    for n in files_task_globs.runtime_data_names:
        data_name = n.args[0]
        if data_name in runtime_data:
            task_or_glob_to_files[n] = runtime_data[data_name]
        else:
            raise error_missing_runtime_parameter("The inputs of this task depends on " +
                                                  "the runtime parameter " +
                                                  "'%s' which is missing " % data_name)

    return expand_nested_tasks_or_globs(files_task_globs.params, task_or_glob_to_files)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

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
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

# _________________________________________________________________________________________

#   touch_file_factory

# _________________________________________________________________________________________
def touch_file_factory(orig_args, register_cleanup):
    """
    Creates function, which when called, will touch files
    """
    file_names = orig_args
    # accepts unicode
    if isinstance(orig_args, path_str_type):
        file_names = [orig_args]
    else:
        # make copy so when original is modifies, we don't get confused!
        file_names = list(orig_args)

    def do_touch_file():
        for f in file_names:
            if not os.path.exists(f):
                with open(f, 'w') as ff:
                    pass
            else:
                os.utime(f, None)
            register_cleanup(f, "touch")
    return do_touch_file


# _________________________________________________________________________________________

#   file_param_factory

#       orig_args = ["input", "output", 1, 2, ...]
#       orig_args = [
#                       ["input0",               "output0",                1, 2, ...]   # job 1
#                       [["input1a", "input1b"], "output1",                1, 2, ...]   # job 2
#                       ["input2",               ["output2a", "output2b"], 1, 2, ...]   # job 3
#                       ["input3",               "output3",                1, 2, ...]   # job 4
#                   ]
#
# _________________________________________________________________________________________
def args_param_factory(orig_args):
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
            yield job_param, job_param
    return iterator

# _________________________________________________________________________________________

#   file_param_factory

#       orig_args = ["input", "output", 1, 2, ...]
#       orig_args = [
#                       ["input0",               "output0",                1, 2, ...]   # job 1
#                       [["input1a", "input1b"], "output1",                1, 2, ...]   # job 2
#                       ["input2",               ["output2a", "output2b"], 1, 2, ...]   # job 3
#                       ["input3",               "output3",                1, 2, ...]   # job 4
#                   ]
#
# _________________________________________________________________________________________


def files_param_factory(input_files_task_globs,
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
        # substitute inputs
        # input_params = file_names_from_tasks_globs(input_files_task_globs, runtime_data, False)

        if input_files_task_globs.params == []:
            if "ruffus_WARNING" not in runtime_data:
                runtime_data["ruffus_WARNING"] = defaultdict(set)
            runtime_data["ruffus_WARNING"][iterator].add(
                err_msg_empty_files_parameter)
            return

        for input_spec, output_extra_param in zip(input_files_task_globs.param_iter(), output_extras):
            input_param = file_names_from_tasks_globs(
                input_spec, runtime_data, do_not_expand_single_job_tasks)
            yield_param = (input_param, ) + output_extra_param
            yield yield_param, yield_param
    return iterator


def files_custom_generator_param_factory(generator):
    """
    Factory for @files taking custom generators
        wraps so that the generator swallows the extra runtime_data argument

    """
    def iterator(runtime_data):
        for params in generator():
            yield params, params
    return iterator

# _________________________________________________________________________________________

#   split_param_factory

# _________________________________________________________________________________________


def split_param_factory(input_files_task_globs, output_files_task_globs, *extra_params):
    """
    Factory for task_split
    """
    def iterator(runtime_data):
        # do_not_expand_single_job_tasks = True

        #
        #   substitute tasks / globs at runtime. No glob subsitution for logging
        #
        input_param = file_names_from_tasks_globs(
            input_files_task_globs,                     runtime_data, True)
        output_param = file_names_from_tasks_globs(
            output_files_task_globs,                    runtime_data)
        output_param_logging = file_names_from_tasks_globs(
            output_files_task_globs.unexpanded_globs(), runtime_data)

        yield (input_param, output_param) + extra_params, (input_param, output_param_logging) + extra_params

    return iterator


# _________________________________________________________________________________________

#   merge_param_factory

# _________________________________________________________________________________________
def merge_param_factory(input_files_task_globs,
                        output_param,
                        *extra_params):
    """
    Factory for task_merge
    """
    #
    def iterator(runtime_data):
        # do_not_expand_single_job_tasks = True
        input_param = file_names_from_tasks_globs(
            input_files_task_globs, runtime_data, True)
        yield_param = (input_param, output_param) + extra_params
        yield yield_param, yield_param

    return iterator


# _________________________________________________________________________________________

#   originate_param_factory

# _________________________________________________________________________________________
def originate_param_factory(list_output_files_task_globs,
                            *extra_params):
    """
    Factory for task_originate
    """
    #
    def iterator(runtime_data):
        for output_files_task_globs in list_output_files_task_globs:
            output_param = file_names_from_tasks_globs(
                output_files_task_globs,                    runtime_data)
            output_param_logging = file_names_from_tasks_globs(
                output_files_task_globs.unexpanded_globs(), runtime_data)
            yield (None, output_param) + tuple(extra_params), (None, output_param_logging) + tuple(extra_params)

    return iterator


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   param_factories

#       ... which take inputs(), add_inputs(), suffix(), regex(), formatter()

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# _________________________________________________________________________________________

#   input_param_to_file_name_list

# _________________________________________________________________________________________
def input_param_to_file_name_list(input_params):
    """
    Common function for
            collate_param_factory
            transform_param_factory
            subdivide_param_factory
        Creates adapter object
        Converts (on the fly) collection / iterator of input params
                ==> generator of flat list of strings (file_names)
    """
    for per_job_input_param in input_params:
        flattened_list_of_file_names = get_strings_in_flattened_sequence(
            per_job_input_param)
        yield per_job_input_param, flattened_list_of_file_names


# _________________________________________________________________________________________

#   input_param_to_file_name_list

# _________________________________________________________________________________________
def list_input_param_to_file_name_list(input_params):
    """
    Common function for
            product_param_factory
        Creates adapter object
        Converts (on the fly) collection / iterator of nested (input params)
                ==> generator of flat list of strings (file_names)
    """
    for per_job_input_param_list in input_params:
        list_of_flattened_list_of_file_names = [
            get_strings_in_flattened_sequence(ii) for ii in per_job_input_param_list]
        yield per_job_input_param_list, list_of_flattened_list_of_file_names


# _________________________________________________________________________________________

#   yield_io_params_per_job

# _________________________________________________________________________________________
def yield_io_params_per_job(input_params,
                            file_names_transform,
                            extra_input_files_task_globs,
                            replace_inputs,
                            output_pattern,
                            extra_specs,
                            runtime_data,
                            iterator,
                            expand_globs_in_output=False):
    """
    Helper function for
        transform_param_factory and
        collate_param_factory and
        subdivide_param_factory and
        combinatorics_param_factory and
        product_param_factory


    *********************************************************
    *                                                       *
    *  Bad (non-orthogonal) design here. Needs refactoring  *
    *                                                       *
    *********************************************************

        subdivide_param_factory requires globs patterns to be expanded

            yield (function call parameters, display parameters)

        all others

            yield function call parameters


        This means that

            all but @subdivide have

                for y in yield_io_params_per_job (...):
                    yield y, y

            subdivide_param_factory has:

                return yield_io_params_per_job

        We would make everything more orthogonal but the current code makes collate easier to write...

            collate_param_factory

                for output_extra_params, grouped_params in groupby(sorted(io_params_iter, key = get_output_extras), key = get_output_extras):




    """
    #
    #   Add extra warning if no regular expressions match:
    #   This is a common class of frustrating errors
    #
    no_regular_expression_matches = True

    for orig_input_param, filenames in input_params:
        try:

            #
            #   Should run job even if there are no file names, so long as there are input parameters...??
            #
            # if not orig_input_param:
            if not filenames:
                continue

            #
            #   extra input has a mixture of input and output parameter behaviours:
            #       1) If it contains tasks, the files from these are passed through unchanged
            #       2) If it contains strings which look like strings,
            #          these are transformed using regular expression, file component substitution etc.
            #          just like output params
            #
            #       So we do (2) first, ignoring tasks, then (1)
            if extra_input_files_task_globs:
                extra_inputs = extra_input_files_task_globs.file_names_transformed(
                    filenames, file_names_transform)

                #
                # add or replace existing input parameters
                #
                if replace_inputs == t_extra_inputs.REPLACE_INPUTS:
                    input_param = file_names_from_tasks_globs(
                        extra_inputs, runtime_data)
                elif replace_inputs == t_extra_inputs.ADD_TO_INPUTS:
                    input_param = (
                        orig_input_param,) + file_names_from_tasks_globs(extra_inputs, runtime_data)
                else:
                    input_param = orig_input_param
            else:
                input_param = orig_input_param

            # extras
            extra_params = tuple(file_names_transform.substitute(
                filenames, p) for p in extra_specs)

            if expand_globs_in_output:
                #
                #   do regex substitution to complete glob pattern
                #       before glob matching
                #
                output_pattern_transformed = output_pattern.output_file_names_transformed(
                    filenames, file_names_transform)
                output_param = file_names_from_tasks_globs(
                    output_pattern_transformed, runtime_data)
                output_param_unglobbed = file_names_from_tasks_globs(
                    output_pattern_transformed.unexpanded_globs(), runtime_data)
                yield ((input_param, output_param) + extra_params,
                       (input_param, output_param_unglobbed) + extra_params)
            else:

                # output
                output_param = file_names_transform.substitute_output_files(
                    filenames, output_pattern)
                yield (input_param, output_param) + extra_params

            no_regular_expression_matches = False

        # match failures are ignored
        except error_input_file_does_not_match:
            if runtime_data != None:
                if not "MATCH_FAILURE" in runtime_data:
                    runtime_data["MATCH_FAILURE"] = defaultdict(set)
                runtime_data["MATCH_FAILURE"][iterator].add(
                    str(sys.exc_info()[1]).strip())
            continue

        # all other exceptions including malformed regexes are raised
        except Exception:
            # print sys.exc_info()
            raise

    #
    #   Add extra warning if no regular expressions match:
    #   This is a common class of frustrating errors
    #
    if no_regular_expression_matches == True:
        if runtime_data != None:
            if "ruffus_WARNING" not in runtime_data:
                runtime_data["ruffus_WARNING"] = defaultdict(set)
            runtime_data["ruffus_WARNING"][iterator].add(
                err_msg_no_regex_match)


# _________________________________________________________________________________________

#   subdivide_param_factory

# _________________________________________________________________________________________
def subdivide_param_factory(input_files_task_globs,
                            file_names_transform,
                            extra_input_files_task_globs,
                            replace_inputs,
                            output_files_task_globs,
                            *extra_specs):
    """
    Factory for task_split (advanced form)
    """
    def iterator(runtime_data):

        #
        #   Convert input file names, globs, and tasks -> a list of (nested) file names
        #       Each element of the list corresponds to the input parameters of a single job
        #
        input_params = file_names_from_tasks_globs(
            input_files_task_globs, runtime_data)

        if not len(input_params):
            return []

        return yield_io_params_per_job(input_param_to_file_name_list(sorted(input_params, key=lambda x: str(x))),
                                       file_names_transform,
                                       extra_input_files_task_globs,
                                       replace_inputs,
                                       output_files_task_globs,
                                       extra_specs,
                                       runtime_data,
                                       iterator,
                                       True)

    return iterator


# _________________________________________________________________________________________

#   combinatorics_param_factory

# _________________________________________________________________________________________
def combinatorics_param_factory(input_files_task_globs,
                                combinatorics_type,
                                k_tuple,
                                file_names_transform,
                                extra_input_files_task_globs,
                                replace_inputs,
                                output_pattern,
                                *extra_specs):
    """
    Factory for task_combinations_with_replacement, task_combinations, task_permutations
    """
    def iterator(runtime_data):

        #
        #   Convert input file names, globs, and tasks -> a list of (nested) file names
        #       Each element of the list corresponds to the input parameters of a single job
        #
        input_params = file_names_from_tasks_globs(
            input_files_task_globs, runtime_data)

        if not len(input_params):
            return

        if combinatorics_type == t_combinatorics_type.COMBINATORICS_PERMUTATIONS:
            combinatoric_iter = itertools.permutations(input_params, k_tuple)
        elif combinatorics_type == t_combinatorics_type.COMBINATORICS_COMBINATIONS:
            combinatoric_iter = itertools.combinations(input_params, k_tuple)
        elif combinatorics_type == t_combinatorics_type.COMBINATORICS_COMBINATIONS_WITH_REPLACEMENT:
            combinatoric_iter = itertools.combinations_with_replacement(
                input_params, k_tuple)
        else:
            raise Exception("Unknown combinatorics type %d" %
                            combinatorics_type)

        for y in yield_io_params_per_job(list_input_param_to_file_name_list(combinatoric_iter),
                                         file_names_transform,
                                         extra_input_files_task_globs,
                                         replace_inputs,
                                         output_pattern,
                                         extra_specs,
                                         runtime_data,
                                         iterator):
            yield y, y

    return iterator


# _________________________________________________________________________________________

#   product_param_factory

# _________________________________________________________________________________________
def product_param_factory(list_input_files_task_globs,
                          file_names_transform,
                          extra_input_files_task_globs,
                          replace_inputs,
                          output_pattern,
                          *extra_specs):
    """
    Factory for task_product
    """
    def iterator(runtime_data):

        #
        #   Convert input file names, globs, and tasks -> a list of (nested) file names
        #       Each element of the list corresponds to the input parameters of a single job
        #
        input_params_list = [file_names_from_tasks_globs(
            ftg, runtime_data) for ftg in list_input_files_task_globs]

        #
        #   ignore if empty list in any of all versus all
        #
        if not len(input_params_list):
            return

        for input_params in input_params_list:
            if not len(input_params):
                return

        for y in yield_io_params_per_job(list_input_param_to_file_name_list(itertools.product(*input_params_list)),
                                         file_names_transform,
                                         extra_input_files_task_globs,
                                         replace_inputs,
                                         output_pattern,
                                         extra_specs,
                                         runtime_data,
                                         iterator):
            yield y, y

    return iterator


# _________________________________________________________________________________________

#   transform_param_factory

# _________________________________________________________________________________________
def transform_param_factory(input_files_task_globs,
                            file_names_transform,
                            extra_input_files_task_globs,
                            replace_inputs,
                            output_pattern,
                            *extra_specs):
    """
    Factory for task_transform
    """
    def iterator(runtime_data):

        #
        #   Convert input file names, globs, and tasks -> a list of (nested) file names
        #       Each element of the list corresponds to the input parameters of a single job
        #
        input_params = file_names_from_tasks_globs(input_files_task_globs, runtime_data)

        if not len(input_params):
            return

        for y in yield_io_params_per_job(input_param_to_file_name_list(sorted(input_params, key=lambda x: str(x))),
                                         file_names_transform,
                                         extra_input_files_task_globs,
                                         replace_inputs,
                                         output_pattern,
                                         extra_specs,
                                         runtime_data,
                                         iterator):
            yield y, y

    return iterator


# _________________________________________________________________________________________

#   collate_param_factory

# _________________________________________________________________________________________
def collate_param_factory(input_files_task_globs,
                          file_names_transform,
                          extra_input_files_task_globs,
                          replace_inputs,
                          output_pattern,
                          *extra_specs):
    """
    Factory for task_collate

    Looks exactly like @transform except that all [input] which lead to the same [output / extra] are combined together
    """
    #
    def iterator(runtime_data):

        #
        #   Convert input file names, globs, and tasks -> a list of (nested) file names
        #       Each element of the list corresponds to the input parameters of a single job
        #
        input_params = file_names_from_tasks_globs(
            input_files_task_globs, runtime_data)

        if not len(input_params):
            return

        io_params_iter = yield_io_params_per_job(input_param_to_file_name_list(sorted(input_params, key=lambda x: str(x))),
                                                 file_names_transform,
                                                 extra_input_files_task_globs,
                                                 replace_inputs,
                                                 output_pattern,
                                                 extra_specs,
                                                 runtime_data,
                                                 iterator)

        #
        #   group job params if their output/extra params are identical
        #
        # sort by first converted to string, and then grouped itself
        # identical things must be adjacent and sorting by strings guarantees that
        def get_output_extras(x): return x[1:]

        def get_output_extras_str(x): return str(x[1:])
        for output_extra_params, grouped_params in groupby(sorted(io_params_iter, key=get_output_extras_str), key=get_output_extras):
            #
            #   yield the different input params grouped into a tuple, followed by all the common params
            #   i.e. (input1, input2, input3), common_output, common_extra1, common_extra2...
            #

            #   Use group by to avoid successive duplicate input_param (remember we have sorted)
            #       This works even with unhashable items!

            params = (tuple(input_param for input_param, ignore in
                            groupby(g[0] for g in grouped_params)),) + output_extra_params

            # the same params twice, once for use, once for display, identical in this case
            yield params, params

    return iterator
