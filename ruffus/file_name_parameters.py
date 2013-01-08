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
from operator import itemgetter
from itertools import groupby
from collections import defaultdict
from time import strftime, gmtime
if __name__ == '__main__':
    import sys
    sys.path.insert(0,".")

from ruffus_exceptions import *
#from file_name_parameters import *
from ruffus_utility import *

import dbdict


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
import re

#_________________________________________________________________________________________

#   get_readable_path_str

#_________________________________________________________________________________________
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



#_________________________________________________________________________________________

#   epoch_seconds_to_str

#_________________________________________________________________________________________
def epoch_seconds_to_str (epoch_seconds):
    """
    Converts seconds since epoch into nice string with date and time to 2 significant
        digits for seconds
    """
    if epoch_seconds in [float('inf'), float('-inf')]:
        return 'Missing/incomplete run '
    #   returns 24 char long  25 May 2011 23:37:40.12
    time_str = strftime("%d %b %Y %H:%M:%S", gmtime(epoch_seconds))

    #
    fraction_of_second_as_str = ("%.2f" % (epoch_seconds - int(epoch_seconds)))[1:]
    #   or fraction = ("%.2f" % (divmod(epoch_seconds, 1)[1]))[1:]
    return (time_str + fraction_of_second_as_str)


err_msg_no_regex_match = ("No jobs were run because no files names matched. "
                        "Please make sure that the regular expression is correctly specified.")
err_msg_empty_files_parameter= ("@files() was empty, i.e. no files were specified. "
                        "Please make sure this is by design.")
#_________________________________________________________________________________________

#   t_params_tasks_globs_run_time_data

#_________________________________________________________________________________________
class t_params_tasks_globs_run_time_data(object):
    """
    After parameters are parsed into tasks, globs, runtime data
    """
    def __init__ (self, params, tasks, globs, runtime_data_names):
        self.params              = params
        self.tasks               = tasks
        self.globs               = globs
        self.runtime_data_names  = runtime_data_names

    def __str__ (self):
        return str(self.params)

    def param_iter (self):
        for p in self.params:
            yield t_params_tasks_globs_run_time_data(p, self.tasks, self.globs,
                                                        self.runtime_data_names)


    def unexpanded_globs (self):
        """
        do not expand globs
        """
        return t_params_tasks_globs_run_time_data(self.params, self.tasks, [],
                                                    self.runtime_data_names)


    def single_file_to_list (self):
        """
        if parameter is a simple string, wrap that in a list unless it is glob
        Useful for simple @transform cases
        """
        if isinstance(self.params, basestring) and not is_glob(self.params):
            self.params = [self.params]
            return True
        return False

    def regex_replaced (self, filename, regex, regex_or_suffix = REGEX_SUBSTITUTE):
        output_glob  = regex_replace(filename, regex, self.globs, regex_or_suffix)
        output_param = regex_replace(filename, regex, self.params, regex_or_suffix)
        return t_params_tasks_globs_run_time_data(output_param, self.tasks, output_glob,
                                                    self.runtime_data_names)




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

#   needs_update_check_directory_missing

#       N.B. throws exception if this is an ordinary file, not a directory


#_________________________________________________________________________________________
def needs_update_check_directory_missing (dirs):
    """
    Called per directory:
        Does it exist?
        Is it an ordinary file not a directory? (throw exception
    """
    for d in dirs:
        #print >>sys.stderr, "check directory missing %d " % os.path.exists(d) # DEBUG
        if not os.path.exists(d):
            return True, "Directory [%s] is missing" % d
        if not os.path.isdir(d):
            raise error_not_a_directory("%s already exists but as a file, not a directory" % d )
    return False, "All directories exist"

#_________________________________________________________________________________________

#   check_input_files_exist

#_________________________________________________________________________________________
def check_input_files_exist (*params):
    """
    If inputs are missing then there is no way a job can run successful.
    Must throw exception.
    This extra function is a hack to make sure input files exists right before
        job is called for better error messages, and to save things from blowing
        up inside the task function
    """
    if len(params):
        input_files = params[0]
        for f in get_strings_in_nested_sequence(input_files):
            if not os.path.exists(f):
                raise MissingInputFileError("No way to run job: "+
                                            "Input file ['%s'] does not exist" % f)


#_________________________________________________________________________________________

#   needs_update_check_exist

#_________________________________________________________________________________________
def needs_update_check_exist (*params):
    """
    Given input and output files, see if all exist
    Each can be

        #. string: assumed to be a filename "file1"
        #. any other type
        #. arbitrary nested sequence of (1) and (2)

    """
    # missing output means build
    if len(params) < 2:
        return True, "i/o files not specified"


    i, o = params[0:2]
    i = get_strings_in_nested_sequence(i)
    o = get_strings_in_nested_sequence(o)

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
        return True, "Missing file%s [%s]" % ("s" if len(missing_files) > 1 else "",
                                            ", ".join(missing_files))

    #
    #   missing input -> build only if output absent
    #
    if len(i) == 0:
        return False, "Missing input files"


    return False, "Up to date"


#_________________________________________________________________________________________

#   needs_update_check_modify_time

#_________________________________________________________________________________________
def needs_update_check_modify_time (*params):
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
    
    needs_update, err_msg = needs_update_check_exist (*params)
    if (needs_update, err_msg) != (False, "Up to date"):
        return needs_update, err_msg

    i, o = params[0:2]
    i = get_strings_in_nested_sequence(i)
    o = get_strings_in_nested_sequence(o)

    #
    #   get sorted modified times for all input and output files
    #
    filename_to_times = [[], []]
    file_times = [[], []]
    
    job_history = dbdict.open(RUFFUS_HISTORY_FILE)


    #_____________________________________________________________________________________

    #   pretty_io_with_date_times

    #_____________________________________________________________________________________
    def pretty_io_with_date_times (filename_to_times):

        # sort
        for io in range(2) :
            filename_to_times[io].sort()


        #
        #   add asterisk for all files which are causing this job to be out of date
        #
        file_name_to_asterisk = dict()
        oldest_output_mtime = filename_to_times[1][0][0]
        for mtime, file_name in filename_to_times[0]:
            file_name_to_asterisk[file_name] = "*" if mtime >= oldest_output_mtime or mtime in [float('inf'), float('-inf')] else " "
        newest_output_mtime = filename_to_times[0][-1][0]
        for mtime, file_name  in filename_to_times[1]:
            file_name_to_asterisk[file_name] = "*" if mtime <= newest_output_mtime or mtime in [float('inf'), float('-inf')] else " "
            


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
                        file_name_to_asterisk[file_name] + " " +        # asterisked out of date files
                        file_datetime_str + ": " +                      # date time of file
                        get_readable_path_str(file_name, 55) + "\n")    # file name truncated to 55
        return msg


    #
    #   Ignore output file if it is found in the list of input files
    #       By definition they have the same timestamp,
    #       and the job will otherwise appear to be out of date
    #
    #   Symbolic links followed
    real_input_file_names = set()
    for input_file_name in i:
        real_input_file_names.add(os.path.realpath(input_file_name))
        # Are there cases when we *should* be looking at the real mtime?
        #   if the job died, we shouldn't look at mtime
        #       but what if the job ran successfully previously, then died on a
        #       rerun? we would have an outofdate history!
        #   if the job finished, but user changed the output, how would we know?
        #       what if a later job would be out of date if we used mtime, but
        #       uptodate if using our job completion time?
        # Seems like the answer is to remove the file from history when its
        #   job is submitted (handles 1st case above), and use the later of
        #   the two timestamps. If user modifies the file, we'll handle outofdate
        #   properly for downstream jobs.
        try:
            mtime = job_history[input_file_name]
        except KeyError:
            # job didn't complete successfully-- force a rerun
            mtime = float('inf')
        else:
            mtime = max(os.path.getmtime(input_file_name), mtime)
        filename_to_times[0].append((mtime, input_file_name))
        file_times[0].append(mtime)

    for output_file_name in o:
        real_file_name = os.path.realpath(output_file_name)
        try:
            mtime = job_history[output_file_name]
        except KeyError:
            # job didn't complete successfully-- force a rerun
            mtime = float('-inf')
        else:
            mtime = min(os.path.getmtime(output_file_name), mtime)
        if real_file_name not in real_input_file_names:
            file_times[1].append(mtime)
        filename_to_times[1].append((mtime, output_file_name))


    #
    #   Debug: Force print modified file names and times
    #
    #if len(file_times[0]) and len (file_times[1]):
    #    print >>sys.stderr, pretty_io_with_date_times(filename_to_times), file_times, (max(file_times[0]) >= min(file_times[1]))
    #else:
    #    print >>sys.stderr, i, o

    #
    #   update if any input file >= (more recent) output file
    #
    if len(file_times[0]) and len (file_times[1]) and max(file_times[0]) >= min(file_times[1]):
        return True, pretty_io_with_date_times(filename_to_times)
    return False, "Up to date"


#_________________________________________________________________________________________
#
#   is_file_re_combining
#
#_________________________________________________________________________________________
def is_file_re_combining (old_args):
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


#_________________________________________________________________________________________

#   file_names_from_tasks_globs

#_________________________________________________________________________________________
def file_names_from_tasks_globs(files_task_globs,
                                runtime_data, do_not_expand_single_job_tasks = False):
    """
    Replaces glob specifications and tasks with actual files / task output
    """

    #
    # N.B. get_output_files() should never have the flattened flag == True
    #       do that later in get_strings_in_nested_sequence
    #

    # special handling for chaining tasks which conceptual have a single job
    #       i.e. @merge and @files/@parallel with single job parameters
    if files_task_globs.params.__class__.__name__ == '_task' and do_not_expand_single_job_tasks:
        return files_task_globs.params.get_output_files(True, runtime_data)


    task_or_glob_to_files = dict()

    # look up globs and tasks
    for g in files_task_globs.globs:
        task_or_glob_to_files[g] = sorted(glob.glob(g))
    for t in files_task_globs.tasks:
        of = t.get_output_files(False, runtime_data)
        task_or_glob_to_files[t] = of
    for n in files_task_globs.runtime_data_names:
        data_name = n.args[0]
        if data_name in runtime_data:
            task_or_glob_to_files[n] = runtime_data[data_name]
        else:
            raise error_missing_runtime_parameter("The inputs of this task depends on " +
                                                  "the runtime parameter " +
                                                  "'%s' which is missing " %  data_name)



    return expand_nested_tasks_or_globs(files_task_globs.params, task_or_glob_to_files)









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
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#_________________________________________________________________________________________

#   touch_file_factory

#_________________________________________________________________________________________
def touch_file_factory (orig_args, register_cleanup):
    """
    Creates function, which when called, will touch files
    """
    file_names = orig_args
    # accepts unicode
    if isinstance (orig_args, basestring):
        file_names = [orig_args]
    else:
        # make copy so when original is modifies, we don't get confused!
        file_names = list(orig_args)

    def do_touch_file ():
        for f  in file_names:
            if not os.path.exists(f):
                open(f, 'w')
            else:
                os.utime(f, None)
            register_cleanup(f, "touch")
    return do_touch_file


#_________________________________________________________________________________________

#   file_param_factory

#       orig_args = ["input", "output", 1, 2, ...]
#       orig_args = [
#                       ["input0",               "output0",                1, 2, ...]   # job 1
#                       [["input1a", "input1b"], "output1",                1, 2, ...]   # job 2
#                       ["input2",               ["output2a", "output2b"], 1, 2, ...]   # job 3
#                       ["input3",               "output3",                1, 2, ...]   # job 4
#                   ]
#
#_________________________________________________________________________________________
def args_param_factory (orig_args):
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

#_________________________________________________________________________________________

#   file_param_factory

#       orig_args = ["input", "output", 1, 2, ...]
#       orig_args = [
#                       ["input0",               "output0",                1, 2, ...]   # job 1
#                       [["input1a", "input1b"], "output1",                1, 2, ...]   # job 2
#                       ["input2",               ["output2a", "output2b"], 1, 2, ...]   # job 3
#                       ["input3",               "output3",                1, 2, ...]   # job 4
#                   ]
#
#_________________________________________________________________________________________
def files_param_factory (input_files_task_globs, flatten_input,
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
        #input_params = file_names_from_tasks_globs(input_files_task_globs, runtime_data, False)

        if input_files_task_globs.params == []:
            if "ruffus_WARNING" not in runtime_data:
                runtime_data["ruffus_WARNING"] = defaultdict(set)
            runtime_data["ruffus_WARNING"][iterator].add(err_msg_empty_files_parameter)
            return

        for input_spec, output_extra_param in zip(input_files_task_globs.param_iter(), output_extras):
            input_param = file_names_from_tasks_globs(input_spec, runtime_data, do_not_expand_single_job_tasks)
            if flatten_input:
                yield_param = (get_strings_in_nested_sequence(input_param),) + output_extra_param
            else:
                yield_param = (input_param, ) + output_extra_param
            yield yield_param, yield_param
    return iterator

def files_custom_generator_param_factory (generator):
    """
    Factory for @files taking custom generators
        wraps so that the generator swallows the extra runtime_data argument

    """
    def iterator(runtime_data):
        for params in generator():
                yield params, params
    return iterator

#_________________________________________________________________________________________

#   split_param_factory

#_________________________________________________________________________________________
def split_param_factory (input_files_task_globs, output_files_task_globs, *extra_params):
    """
    Factory for task_split
    """
    def iterator(runtime_data):
        # flattened  = False
        # do_not_expand_single_job_tasks = True

        #
        #   substitute tasks / globs at runtime. No glob subsitution for logging
        #
        input_param          = file_names_from_tasks_globs(input_files_task_globs,                     runtime_data, True)
        output_param         = file_names_from_tasks_globs(output_files_task_globs,                    runtime_data)
        output_param_logging = file_names_from_tasks_globs(output_files_task_globs.unexpanded_globs(), runtime_data)

        yield (input_param, output_param) + extra_params, (input_param, output_param_logging) + extra_params



    return iterator



#_________________________________________________________________________________________

#   split_ex_param_factory

#_________________________________________________________________________________________
def split_ex_param_factory (input_files_task_globs,
                            flatten_input,
                            regex,
                            regex_or_suffix,
                            extra_input_files_task_globs,
                            replace_inputs,
                            output_files_task_globs,
                            *extra_specs):
    """
    Factory for task_split (advanced form)
    """
    def iterator(runtime_data):

        #
        # get list of input_params
        #
        input_params = file_names_from_tasks_globs(input_files_task_globs, runtime_data)

        if flatten_input:
            input_params = get_strings_in_nested_sequence(input_params)

        if not len(input_params):
            return

        #
        #   Add extra warning if no regular expressions match:
        #   This is a common class of frustrating errors
        #
        no_regular_expression_matches = True

        for orig_input_param in sorted(input_params):

            #
            #   turn input param into a string and match with regular expression
            #
            filename = get_first_string_in_nested_sequence(orig_input_param)
            if filename == None or not regex.search(filename):
                continue

            no_regular_expression_matches = False

            #
            #   if "inputs" defined  turn input string into i/o/extras with regex
            #
            if extra_input_files_task_globs != None:
                # extras
                extra_inputs = extra_input_files_task_globs.regex_replaced (filename, regex)
                if replace_inputs:
                    input_param = file_names_from_tasks_globs(extra_inputs, runtime_data)
                else:
                    input_param = (orig_input_param,) + file_names_from_tasks_globs(extra_inputs, runtime_data)
            else:
                input_param = orig_input_param

            #
            #   do regex substitution to complete glob pattern
            #       before glob matching
            #
            output_specs_with_regex = output_files_task_globs.regex_replaced (filename, regex)
            output_param        = file_names_from_tasks_globs(output_specs_with_regex, runtime_data)
            output_param_logging= file_names_from_tasks_globs(output_specs_with_regex.unexpanded_globs(), runtime_data)

            #
            #   regex substitution on everything else
            #
            extra_params =  tuple(regex_replace(filename, regex, p) for p in extra_specs)

            yield ( (input_param, output_param          ) + extra_params,
                    (input_param, output_param_logging  ) + extra_params)


        #
        #   Add extra warning if no regular expressions match:
        #   This is a common class of frustrating errors
        #
        if no_regular_expression_matches == True:
            if "ruffus_WARNING" not in runtime_data:
                runtime_data["ruffus_WARNING"] = defaultdict(set)
            runtime_data["ruffus_WARNING"][iterator].add(err_msg_no_regex_match)

    return iterator

#_________________________________________________________________________________________

#   transform_param_factory

#_________________________________________________________________________________________
def transform_param_factory (input_files_task_globs,
                             flatten_input, regex,
                             regex_or_suffix,
                             extra_input_files_task_globs,
                             replace_inputs,
                             output_pattern,
                             *extra_specs):
    """
    Factory for task_transform
    """
    def iterator(runtime_data):

        #
        # get list of input_params
        #
        input_params = file_names_from_tasks_globs(input_files_task_globs, runtime_data)

        if flatten_input:
            input_params = get_strings_in_nested_sequence(input_params)

        if not len(input_params):
            return

        #
        #   Add extra warning if no regular expressions match:
        #   This is a common class of frustrating errors
        #
        no_regular_expression_matches = True

        # for regex, always substitute whether output or extra inputs or extras
        if regex_or_suffix:
            regex_or_suffix_extras  = REGEX_SUBSTITUTE
            regex_or_suffix_outputs = REGEX_SUBSTITUTE

        # for suffix, outputs there is an implicit "\1", otherwise only substitute when there is a "\1"
        else:
            regex_or_suffix_extras  = SUFFIX_SUBSTITUTE_IF_SPECIFIED
            regex_or_suffix_outputs = SUFFIX_SUBSTITUTE_ALWAYS

        for orig_input_param in sorted(input_params):

            #
            #   turn input param into a string and match with regular expression
            #
            filename = get_first_string_in_nested_sequence(orig_input_param)
            if filename == None or not regex.search(filename):
                continue

            no_regular_expression_matches = False

            #
            #   if "inputs" defined  turn input string into i/o/extras with regex
            #
            if extra_input_files_task_globs != None:
                # extras
                extra_inputs = extra_input_files_task_globs.regex_replaced (filename, regex, regex_or_suffix_extras)


                # inputs()
                if replace_inputs:
                    input_param = file_names_from_tasks_globs(extra_inputs, runtime_data)
                # add_inputs()
                else:
                    input_param = (orig_input_param,) + file_names_from_tasks_globs(extra_inputs, runtime_data)
            else:
                input_param = orig_input_param

            # output
            output_param = regex_replace(filename, regex, output_pattern, regex_or_suffix_outputs)

            # extras
            extra_params = tuple(regex_replace(filename, regex, p, regex_or_suffix_extras) for p in extra_specs)

            yield_param = (input_param, output_param) + extra_params
            yield yield_param, yield_param

        #
        #   Add extra warning if no regular expressions match:
        #   This is a common class of frustrating errors
        #
        if no_regular_expression_matches == True:
            if "ruffus_WARNING" not in runtime_data:
                runtime_data["ruffus_WARNING"] = defaultdict(set)
            runtime_data["ruffus_WARNING"][iterator].add(err_msg_no_regex_match)

    return iterator


#_________________________________________________________________________________________

#   merge_param_factory

#_________________________________________________________________________________________
def merge_param_factory (input_files_task_globs,
                                output_param,
                                *extra_params):
    """
    Factory for task_merge
    """
    #
    def iterator(runtime_data):
        # flattened  = False
        # do_not_expand_single_job_tasks = True
        input_param = file_names_from_tasks_globs(input_files_task_globs, runtime_data,
                                                    True)
        yield_param = (input_param, output_param) + extra_params
        yield yield_param, yield_param

    return iterator


#_________________________________________________________________________________________

#   collate_param_factory

#_________________________________________________________________________________________
def collate_param_factory (input_files_task_globs,
                           flatten_input,
                           regex,
                           extra_input_files_task_globs,
                           replace_inputs,
                           *output_extra_specs):
    """
    Factory for task_collate
    all [input] which lead to the same [output / extra] are combined together
    """
    #
    def iterator(runtime_data):

        #
        # one job per unique [output / extra] parameter
        #
        #   can't use set or dict because parameters might not be hashable!!!
        #   use list and itertools group by
        #
        params_per_job = []

        # flattened  = flatten_input
        # do_not_expand_single_job_tasks = False
        input_params = file_names_from_tasks_globs(input_files_task_globs, runtime_data)

        if flatten_input:
            input_params = get_strings_in_nested_sequence(input_params)

        if not len(input_params):
            return

        for orig_input_param in sorted(input_params):

            #
            #   turn input param into a string and match with regular expression
            #
            filename = get_first_string_in_nested_sequence(orig_input_param)
            if filename == None or not regex.search(filename):
                continue

            #
            #   if "inputs" defined  turn input string into i/o/extras with regex
            #
            if extra_input_files_task_globs != None:
                extra_inputs = extra_input_files_task_globs.regex_replaced (filename, regex)
                if replace_inputs:
                    input_param = file_names_from_tasks_globs(extra_inputs, runtime_data)
                else:
                    input_param = (orig_input_param,) + file_names_from_tasks_globs(extra_inputs, runtime_data)
            else:
                input_param = orig_input_param

            #   output / extras
            output_extra_params = tuple(regex_replace(filename, regex, p)
                                            for p in output_extra_specs)
            #
            #   nothing matched
            #
            if len(output_extra_params) == 0:
                continue

            params_per_job.append((output_extra_params, input_param))

        #
        #   Add extra warning if no regular expressions match:
        #   This is a common class of frustrating errors
        #
        if len(params_per_job) == 0:
            if "ruffus_WARNING" not in runtime_data:
                runtime_data["ruffus_WARNING"] = defaultdict(set)
            runtime_data["ruffus_WARNING"][iterator].add(err_msg_no_regex_match)
            return


        # combine inputs which lead to the same output/extras into one tuple
        for output_params, params_grouped_by_output in groupby(sorted(params_per_job), itemgetter(0)):
            yield_param = (tuple(input_param for input_param, ignore in
                            groupby(list(params_grouped_by_output), itemgetter(1))),) + output_params
            yield yield_param, yield_param

    return iterator



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Legacy code

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#_________________________________________________________________________________________


#   files_re_param_factory

#      iterable list of input / output files from

#                1) glob/filelist
#                2) regex
#                3) input_filename_str (optional)
#                4) output_filename_str
#_________________________________________________________________________________________
def files_re_param_factory( input_files_task_globs, combining_all_jobs,
                            regex, extra_input_files_task_globs, *output_and_extras):
    """
    Factory for functions which in turn
        yield tuples of input_file_name, output_file_name

    Usage:


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
    if combining_all_jobs:
        return collate_param_factory (input_files_task_globs,
                                        False,
                                        regex,
                                        extra_input_files_task_globs,
                                        True,
                                        *output_and_extras)
    else:
        return transform_param_factory (input_files_task_globs,
                                        False, regex,
                                        True,
                                        extra_input_files_task_globs,
                                        True,
                                        *output_and_extras)










#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Unit Tests in test/test_file_name_parameters.py


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

