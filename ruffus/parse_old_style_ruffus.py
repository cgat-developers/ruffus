#!/usr/bin/env python
import logging.handlers
import logging
import re
"""
    Parse Ruffus pipelines using old fashioned decorator syntax
"""

################################################################################
#
#   parse_old_style_ruffus.py
#
#
#   Copyright (c) 25 February 2015 Leo Goodstadt
#   This is free software, and you are welcome to redistribute it
#   under the "MIT" license; See http://opensource.org/licenses/MIT for details.
#
#################################################################################

import sys
import os

# Use import path from ~/python_modules
if __name__ == '__main__':
    sys.path.insert(0, os.path.expanduser("~lg/src/oss/ruffus"))
    sys.path.append(os.path.expanduser("~lg/src/python_modules"))


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)

    common_group = parser.add_argument_group('Common arguments')
    common_group.add_argument('--verbose', "-v", const=1, metavar="VERBOSITY", default=0, nargs='?', type=int,
                              help="Print more verbose messages for each additional verbose level.")
    common_group.add_argument(
        '--version', action='version', version='%(prog)s 1.0')
    common_group.add_argument("-L", "--log_file", metavar="FILE", type=str,
                              help="Name and path of log file")

    options = parser.parse_args()

    if not options.log_file:
        options.log_file = os.path.join("parse_old_style_ruffus.log")


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#from json import dumps
#from collections import defaultdict


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Logger


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


MESSAGE = 15
logging.addLevelName(MESSAGE, "MESSAGE")


def setup_std_logging(module_name, log_file, verbose):
    """
    set up logging using programme options
    """

    logger = logging.getLogger(module_name)

    # We are interesting in all messages
    logger.setLevel(logging.DEBUG)
    has_handler = False

    #
    #   log to file if that is specified
    #
    if log_file:
        handler = logging.FileHandler(log_file, delay=False)

        class stripped_down_formatter(logging.Formatter):
            def format(self, record):
                prefix = ""
                if not hasattr(self, "first_used"):
                    self.first_used = True
                    prefix = "\n" + self.formatTime(record, "%Y-%m-%d")
                    prefix += " %(name)s\n" % record.__dict__
                if record.levelname in ("INFO", "MESSAGE", "DEBUG"):
                    self._fmt = " %(asctime)s - %(message)s"
                else:
                    self._fmt = " %(asctime)s - %(levelname)-7s - %(message)s"
                return prefix + logging.Formatter.format(self, record)
        handler.setFormatter(stripped_down_formatter(
            "%(asctime)s - %(name)s - %(levelname)6s - %(message)s", "%H:%M:%S"))
        handler.setLevel(MESSAGE)
        logger.addHandler(handler)
        has_handler = True

    #
    #   log to stderr if verbose
    #
    if verbose:
        stderrhandler = logging.StreamHandler(sys.stderr)
        stderrhandler.setFormatter(logging.Formatter("    %(message)s"))
        stderrhandler.setLevel(logging.DEBUG)
        if log_file:
            class debug_filter(logging.Filter):
                """
                Ignore INFO messages
                """

                def filter(self, record):
                    return logging.INFO != record.levelno
            stderrhandler.addFilter(debug_filter())
        logger.addHandler(stderrhandler)
        has_handler = True

    #
    #   no logging
    #
    if not has_handler:
        class NullHandler(logging.Handler):
            """
            for when there is no logging
            """

            def emit(self, record):
                pass
        logger.addHandler(NullHandler())

    return logger


if __name__ == '__main__':

    #
    #   set up log: name = script name sans extension
    #
    module_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    logger = setup_std_logging(module_name, options.log_file, options.verbose)

    #
    #   log programme parameters
    #
    logger.info(" ".join(sys.argv))


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

func_re = re.compile("^\s*def.*\(")


def get_decorators(line_num, decorated_lines, all_lines):
    for line in sys.stdin:
        line_num += 1
        mm = func_re.search(line)
        if mm:
            decorated_lines.append(line + "\n")
            all_lines.append(line)
            return line_num
        else:
            decorated_lines.append(line)

    raise Exception("Unterminated decorators %s" % (decorated_lines,))


decorator_re = re.compile("^\s*@")
no_white_space_re = re.compile("^[^#\s]")
if __name__ == '__main__':
    line_num = 1
    last_decorated_line_num = 1
    pipeline_insertion_line_num = 1
    decorated_lines = []
    all_lines = []
    for line in sys.stdin:
        line_num += 1
        # decorator start
        if decorator_re.search(line):
            decorated_lines.append(line)
            line_num = get_decorators(line_num, decorated_lines, all_lines)
            last_decorated_line_num = len(all_lines)
            continue
        if no_white_space_re.search(line):
            if pipeline_insertion_line_num < last_decorated_line_num:
                pipeline_insertion_line_num = len(all_lines)
        all_lines.append(line)

    for line in all_lines[0: pipeline_insertion_line_num]:
        sys.stdout.write(line)
    sys.stdout.write("\n" * 3)

    sys.stdout.write('pipeline = Pipeline.pipelines["main"]\n\n')

    for line in decorated_lines:
        sys.stdout.write(line)
    sys.stdout.write("\n" * 3)

    for line in all_lines[pipeline_insertion_line_num:]:
        sys.stdout.write(line)


#        for aa in active_if.py \
#        branching_dependencies.py \
#        cmdline.py \
#        collate.py \
#        empty_files_decorator.py \
#        exceptions.py \
#        file_name_parameters.py \
#        files_decorator.py \
#        filesre_combine.py \
#        filesre_split_and_combine.py \
#        follows_mkdir.py \
#        graphviz.py \
#        inputs_with_multiple_args_raising_exception.py \
#        job_completion_checksums.py \
#        job_history_with_exceptions.py \
#        mkdir.py \
#        N_x_M_and_collate.py \
#        pausing.py \
#        pipeline_printout_graph.py \
#        posttask_merge.py \
#        regex_error_messages.py \
#        ruffus_utility_parse_task_arguments.py \
#        ruffus_utility.py \
#        runtime_data.py \
#        softlink_uptodate.py \
#        split_and_combine.py \
#        split_regex_and_collate.py \
#        split_subdivide_checkpointing.py \
#        task_file_dependencies.py \
#        task_misc.py \
#        transform_add_inputs.py \
#        transform_inputs.py \
#        transform_with_no_re_matches.py \
#        tutorial7.py \
#        unicode_filenames.py \
#        verbosity.py; \
#        do echo test_$aa; ../parse_old_style_ruffus.py < test_$aa >| test_newstyle_$aa; done
