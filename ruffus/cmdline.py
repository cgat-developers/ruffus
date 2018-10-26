################################################################################
#
#
#   cmd_line_helper.py
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
from .ruffus_utility import CHECKSUM_REGENERATE
from . import proxy_logger
from . import task
import logging.handlers
import logging
"""

********************************************
:mod:`ruffus.cmdline` -- Overview
********************************************

.. moduleauthor:: Leo Goodstadt <ruffus@llew.org.uk>


    #
    #   Using argparse (new in python v 2.7)
    #
    from ruffus import *

    parser = cmdline.get_argparse(   description='WHAT DOES THIS PIPELINE DO?')

    parser.add_argument("--input_file")

    options = parser.parse_args()

    #  logger which can be passed to ruffus tasks
    logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

    #_____________________________________________________________________________________

    #   pipelined functions go here

    #_____________________________________________________________________________________

    cmdline.run (options)



    #
    #   Using optparse (new in python v 2.6)
    #
    from ruffus import *

    parser = cmdline.get_optgparse(version="%prog 1.0", usage = "\n\n    %prog [options]")

    parser.add_option("-c", "--custom", dest="custom", action="count")


    (options, remaining_args) = parser.parse_args()

    #  logger which can be passed to ruffus tasks
    logger, logger_mutex = cmdline.setup_logging ("this_program", options.log_file, options.verbose)

    #_____________________________________________________________________________________

    #   pipelined functions go here

    #_____________________________________________________________________________________

    cmdline.run (options)


"""


#
#   print options
#
flowchart_formats = ["svg", "svgz", "png",
                     "jpg", "psd", "tif", "eps", "pdf", "dot"]
#  "jpeg", "gif", "plain", "ps", "wbmp", "canon",
#  "cmap", "cmapx", "cmapx_np", "fig", "gd", "gd2",
# "gv", "imap", "imap_np", "ismap", "jpe", "plain-ext",
# "ps2", "tk", "vml", "vmlz", "vrml", "x11", "xdot", "xlib"
# Replace last comma with " and". Mad funky, unreadable reverse replace code: couldn't resist!
flowchart_formats_str = ", ".join(["%r" % ss for ss in flowchart_formats])[
    ::-1].replace(" ,", ", or "[::-1], 1)[::-1]


# _________________________________________________________________________________________

#   get_argparse
# _________________________________________________________________________________________
def get_argparse(*args, **args_dict):
    """
    Set up argparse
        to allow for ruffus specific options:

            --verbose
            --version
            --log_file

        -t, --target_tasks
        -j, --jobs
        -n, --just_print
            --flowchart
            --touch_files_only
            --recreate_database
            --checksum_file_name
            --key_legend_in_graph
            --draw_graph_horizontally
            --flowchart_format
            --forced_tasks

    Optionally specify ignored_args = ["verbose", "recreate_database",...]
        listing names which will not be added as valid options on the command line

    Optionally specify version = "%(prog)s version 1.234"

    """
    import argparse

    # version and ignored_args are for append_to_argparse
    orig_args_dict = dict(args_dict)
    if "version" in args_dict:
        del args_dict["version"]
    if "ignored_args" in args_dict:
        del args_dict["ignored_args"]

    parser = argparse.ArgumentParser(*args, **args_dict)

    return append_to_argparse(parser, **orig_args_dict)

# _________________________________________________________________________________________

#   append_to_argparse
# _________________________________________________________________________________________


def append_to_argparse(parser, **args_dict):
    """
    Common options:

            --verbose
            --version
            --log_file
    """

    if "version" in args_dict:
        prog_version = args_dict["version"]
    else:
        prog_version = "%(prog)s 1.0"

    #
    #   ignored_args contains a list of options which will *not* be added
    #
    if "ignored_args" in args_dict:
        if isinstance(args_dict["ignored_args"], str):
            ignored_args = set([args_dict["ignored_args"]])
        else:
            try:
                ignored_args = set(args_dict["ignored_args"])
            except:
                raise Exception(
                    "Error: expected ignored_args = ['list_of', 'option_names']")
    else:
        ignored_args = set()

    common_options = parser.add_argument_group('Common options')
    if "verbose" not in ignored_args:
        common_options.add_argument(
            '--verbose', "-v", const="+", default=[], nargs='?',
            action="append",
            help="Print more verbose messages for each additional verbose level.")
    if "version" not in ignored_args:
        common_options.add_argument(
            '--version', action='version', version=prog_version)
    if "log_file" not in ignored_args:
        common_options.add_argument("-L", "--log_file", metavar="FILE", type=str,
                                    help="Name and path of log file")

    #
    #   pipeline
    #
    pipeline_options = parser.add_argument_group('pipeline arguments')
    if "target_tasks" not in ignored_args:
        pipeline_options.add_argument("-T", "--target_tasks", action="append",
                                      metavar="JOBNAME", type=str,
                                      help="Target task(s) of pipeline.", default=[])
    if "jobs" not in ignored_args:
        pipeline_options.add_argument("-j", "--jobs", default=1, metavar="N", type=int,
                                      help="Allow N jobs (commands) to run simultaneously.")
    if "use_threads" not in ignored_args:
        pipeline_options.add_argument("--use_threads", action="store_true",
                                      help="Use multiple threads rather than processes. Needs --jobs N with N > 1")
    if "just_print" not in ignored_args:
        pipeline_options.add_argument("-n", "--just_print", action="store_true",
                                      help="Don't actually run any commands; just print the pipeline.")
    if "touch_files_only" not in ignored_args:
        pipeline_options.add_argument("--touch_files_only", action="store_true",
                                      help="Don't actually run any commands; just 'touch' the output for each task to make them appear up to date.")
    if "recreate_database" not in ignored_args:
        pipeline_options.add_argument("--recreate_database", action="store_true",
                                      help="Don't actually run any commands; just recreate the checksum database.")
    if "checksum_file_name" not in ignored_args:
        pipeline_options.add_argument("--checksum_file_name", dest="history_file", metavar="FILE", type=str,
                                      help="Path of the checksum file.")
    if "flowchart" not in ignored_args:
        pipeline_options.add_argument("--flowchart", metavar="FILE", type=str,
                                      help="Don't run any commands; just print pipeline as a flowchart.")

    #
    #   Less common pipeline options
    #
    if "key_legend_in_graph" not in ignored_args:
        pipeline_options.add_argument("--key_legend_in_graph",     action="store_true",
                                      help="Print out legend and key for dependency graph.")
    if "draw_graph_horizontally" not in ignored_args:
        pipeline_options.add_argument("--draw_graph_horizontally", action="store_true", dest="draw_horizontally",
                                      help="Draw horizontal dependency graph.")
    if "flowchart_format" not in ignored_args:
        pipeline_options.add_argument("--flowchart_format", metavar="FORMAT",
                                      type=str, choices=flowchart_formats,
                                      default=None,
                                      help="format of dependency graph file. Can be %s. Defaults to the "
                                      "file name extension of --flowchart FILE." % flowchart_formats_str)
    if "forced_tasks" not in ignored_args:
        pipeline_options.add_argument("--forced_tasks", action="append",
                                      metavar="JOBNAME", type=str,
                                      help="Task(s) which will be included even if they are up to date.", default=[])

    return parser


# _________________________________________________________________________________________

#   Hacky extension to *deprecated!!* optparse to support variable number of arguments
#       for --verbose
# _________________________________________________________________________________________
def vararg_callback(option, opt_str, value, parser):
    #
    #   get current value
    #
    if hasattr(parser.values, option.dest):
        value = getattr(parser.values, option.dest)
    else:
        value = []
    if not len(parser.rargs):
        value.append("+")
    else:
        arg = parser.rargs[0]
        # stop on --foo like options
        if arg[:1] == "-":
            value.append("+")
        else:
            value.append(arg)
            del parser.rargs[:1]
    setattr(parser.values, option.dest, value)


# _________________________________________________________________________________________

#   optparse is deprecated!
# _________________________________________________________________________________________
def get_optparse(*args, **args_dict):
    """
    Set up OptionParser from optparse
        to allow for ruffus specific options:

            --verbose
            --version
            --log_file

        -t, --target_tasks
        -j, --jobs
        -n, --just_print
            --flowchart
            --touch_files_only
            --recreate_database
            --checksum_file_name
            --key_legend_in_graph
            --draw_graph_horizontally
            --flowchart_format
            --forced_tasks

    Optionally specify ignored_args = ["verbose", "recreate_database",...]
        listing names which will not be added as valid options on the command line

    N.B. optparse is deprecated since python version 2.7.
    """
    from optparse import OptionParser

    # ignored_args are for append_to_optparse
    orig_args_dict = dict(args_dict)
    if "ignored_args" in args_dict:
        del args_dict["ignored_args"]

    parser = OptionParser(*args, **args_dict)

    return append_to_optparse(parser, **orig_args_dict)

# _________________________________________________________________________________________

#   optparse is deprecated!
# _________________________________________________________________________________________


def append_to_optparse(parser, **args_dict):
    """
    Set up OptionParser from optparse
        to allow for ruffus specific options:

            --verbose
            --version
            --log_file

        -t, --target_tasks
        -j, --jobs
        -n, --just_print
            --flowchart
            --touch_files_only
            --recreate_database
            --checksum_file_name
            --key_legend_in_graph
            --draw_graph_horizontally
            --flowchart_format
            --forced_tasks

    Optionally specify ignored_args = ["verbose", "recreate_database",...]
        listing names which will not be added as valid options on the command line
    """

    #
    #   ignored_args contains a list of options which will *not* be added
    #
    if "ignored_args" in args_dict:
        if isinstance(args_dict["ignored_args"], str):
            ignored_args = set([args_dict["ignored_args"]])
        else:
            try:
                ignored_args = set(args_dict["ignored_args"])
            except:
                raise Exception(
                    "Error: expected ignored_args = ['list_of', 'option_names']")
    else:
        ignored_args = set()

    #
    #   general options: verbosity / logging
    #
    if "verbose" not in ignored_args:
        parser.add_option("-v", "--verbose", dest="verbose",
                          action="callback", default=[],
                          # ---------------------------------------------------------------
                          # hack to get around unreasonable discrimination against
                          # --long_options=with_equals in opt_parse::_process_long_opt()
                          # when using a callback
                          type=int,
                          nargs=0,
                          # ---------------------------------------------------------------
                          callback=vararg_callback,
                          help="Print more verbose messages for each additional verbose level.")
    if "log_file" not in ignored_args:
        parser.add_option("-L", "--log_file", dest="log_file",
                          metavar="FILE",
                          type="string",
                          help="Name and path of log file")
    #
    #   pipeline
    #
    if "target_tasks" not in ignored_args:
        parser.add_option("-t", "--target_tasks", dest="target_tasks",
                          action="append",
                          default=list(),
                          metavar="JOBNAME",
                          type="string",
                          help="Target task(s) of pipeline.")
    if "jobs" not in ignored_args:
        parser.add_option("-j", "--jobs", dest="jobs",
                          default=1,
                          metavar="N",
                          type="int",
                          help="Allow N jobs (commands) to run simultaneously.")
    if "use_threads" not in ignored_args:
        parser.add_option("--use_threads", dest="use_threads",
                          action="store_true", default=False,
                          help="Use multiple threads rather than processes. Needs --jobs N with N > 1")
    if "just_print" not in ignored_args:
        parser.add_option("-n", "--just_print", dest="just_print",
                          action="store_true", default=False,
                          help="Don't actually run any commands; just print the pipeline.")
    if "touch_files_only" not in ignored_args:
        parser.add_option("--touch_files_only", dest="touch_files_only",
                          action="store_true", default=False,
                          help="Don't actually run any commands; just 'touch' the output for each task to make them appear up to date.")
    if "recreate_database" not in ignored_args:
        parser.add_option("--recreate_database", dest="recreate_database",
                          action="store_true", default=False,
                          help="Don't actually run any commands; just recreate the checksum database.")
    if "checksum_file_name" not in ignored_args:
        parser.add_option("--checksum_file_name", dest="history_file",
                          metavar="FILE",
                          type="string",
                          help="Path of the checksum file.")
    if "flowchart" not in ignored_args:
        parser.add_option("--flowchart", dest="flowchart",
                          metavar="FILE",
                          type="string",
                          help="Don't actually run any commands; just print the pipeline "
                          "as a flowchart.")

    #
    #   Less common pipeline options
    #
    if "key_legend_in_graph" not in ignored_args:
        parser.add_option("--key_legend_in_graph", dest="key_legend_in_graph",
                          action="store_true", default=False,
                          help="Print out legend and key for dependency graph.")
    if "flowchart_format" not in ignored_args:
        parser.add_option("--draw_graph_horizontally", dest="draw_horizontally",
                          action="store_true", default=False,
                          help="Draw horizontal dependency graph.")
    if "flowchart_format" not in ignored_args:
        parser.add_option("--flowchart_format", dest="flowchart_format",
                          metavar="FORMAT",
                          type="string",
                          default=None,
                          help="format of dependency graph file. Can be %s. Defaults to the "
                          "file name extension of --flowchart FILE." % flowchart_formats_str)
    if "forced_tasks" not in ignored_args:
        parser.add_option("--forced_tasks", dest="forced_tasks",
                          action="append",
                          default=list(),
                          metavar="JOBNAME",
                          type="string",
                          help="Pipeline task(s) which will be included even if they are up to date.")

        return parser


MESSAGE = 15
logging.addLevelName(MESSAGE, "MESSAGE")

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Logger


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#   Allow logging across Ruffus pipeline
#
def setup_logging(module_name, log_file_name, verbose):
    return proxy_logger.make_shared_logger_and_proxy(setup_logging_factory, module_name, [log_file_name, verbose])


def setup_logging_factory(logger_name, args):
    log_file_name, verbose = args
    """
    This function is a simple around wrapper around the python
    `logging <http://docs.python.org/library/logging.html>`_ module.

    This *logger_factory* example creates logging objects which can
    then be managed by proxy via ``ruffus.proxy_logger.make_shared_logger_and_proxy()``

    This can be:

        * a `disk log file <http://docs.python.org/library/logging.html#filehandler>`_
        * a automatically backed-up `(rotating) log <http://docs.python.org/library/logging.html#rotatingfilehandler>`_.
        * any log specified in a `configuration file <http://docs.python.org/library/logging.html#configuration-file-format>`_

    These are specified in the ``args`` dictionary forwarded by ``make_shared_logger_and_proxy()``

    :param logger_name: name of log
    :param args: a dictionary of parameters forwarded from ``make_shared_logger_and_proxy()``

        Valid entries include:

            .. describe:: "level"

                Sets the `threshold <http://docs.python.org/library/logging.html#logging.Handler.setLevel>`_ for the logger.

            .. describe:: "config_file"

                The logging object is configured from this `configuration file <http://docs.python.org/library/logging.html#configuration-file-format>`_.

            .. describe:: "file_name"

                Sets disk log file name.

            .. describe:: "rotating"

                Chooses a `(rotating) log <http://docs.python.org/library/logging.html#rotatingfilehandler>`_.

            .. describe:: "maxBytes"

                Allows the file to rollover at a predetermined size

            .. describe:: "backupCount"

                If backupCount is non-zero, the system will save old log files by appending the extensions ``.1``, ``.2``, ``.3`` etc., to the filename.

            .. describe:: "delay"

                Defer file creation until the log is written to.

            .. describe:: "formatter"

                `Converts <http://docs.python.org/library/logging.html#formatter-objects>`_ the message to a logged entry string.
                For example,
                ::

                    "%(asctime)s - %(name)s - %(levelname)6s - %(message)s"



    """

    #
    #   Log file name with logger level
    #
    new_logger = logging.getLogger(logger_name)

    class debug_filter(logging.Filter):
        """
        Ignore INFO messages
        """

        def filter(self, record):
            return logging.INFO != record.levelno

    class NullHandler(logging.Handler):
        """
        for when there is no logging
        """

        def emit(self, record):
            pass

    # We are interesting in all messages
    new_logger.setLevel(logging.DEBUG)
    has_handler = False

    # log to file if that is specified
    if log_file_name:
        handler = logging.FileHandler(log_file_name, delay=False)

        class stipped_down_formatter(logging.Formatter):
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
        handler.setFormatter(stipped_down_formatter(
            "%(asctime)s - %(name)s - %(levelname)6s - %(message)s", "%H:%M:%S"))
        handler.setLevel(MESSAGE)
        new_logger.addHandler(handler)
        has_handler = True

    # log to stderr if verbose
    if verbose:
        stderrhandler = logging.StreamHandler(sys.stderr)
        stderrhandler.setFormatter(logging.Formatter("    %(message)s"))
        stderrhandler.setLevel(logging.DEBUG)
        if log_file_name:
            stderrhandler.addFilter(debug_filter())
        new_logger.addHandler(stderrhandler)
        has_handler = True

    # no logging
    if not has_handler:
        new_logger.addHandler(NullHandler())

    #
    #   This log object will be wrapped in proxy
    #
    return new_logger


#
#   valid arguments to each function which are not exposed by any options in the command line
#
extra_pipeline_printout_graph_options = [
    "ignore_upstream_of_target",
    "skip_uptodate_tasks",
    "gnu_make_maximal_rebuild_mode",
    "test_all_task_for_update",
    "minimal_key_legend",
    "user_colour_scheme",
    "pipeline_name",
    "size",
    "dpi",
    "history_file",
    "checksum_level",
    "runtime_data",
]
extra_pipeline_printout_options = [
    "indent",
    "gnu_make_maximal_rebuild_mode",
    "checksum_level",
    "history_file",
    "wrap_width",
    "runtime_data"]


extra_pipeline_run_options = [
    "gnu_make_maximal_rebuild_mode",
    "runtime_data",
    "one_second_per_job",
    # exposed directly in command line
    #"touch_files_only"                  ,
    "history_file",
    "logger",
    "exceptions_terminate_immediately",
    "log_exceptions",
    "checksum_level",
    "multithread"]


# _________________________________________________________________________________________

#   get_extra_options_appropriate_for_command

# _________________________________________________________________________________________
def get_extra_options_appropriate_for_command(appropriate_option_names, extra_options):
    """
    Get extra options which are appropriate for
        pipeline_printout
        pipeline_printout_graph
        pipeline_run
    """

    appropriate_options = dict()
    for option_name in appropriate_option_names:
        if option_name in extra_options:
            appropriate_options[option_name] = extra_options[option_name]
    return appropriate_options


# _________________________________________________________________________________________

#   handle_verbose

# _________________________________________________________________________________________
def handle_verbose(options):
    """
    raw options.verbose is a list of specifiers
         '+'         : i.e. --verbose. This just increases the current verbosity value by 1
         '\d+'       : e.g. --verbose 6. This (re)sets the verbosity value
         '\d+:\d+'   : e.g. --verbose 7:-5 The second number is the verbose_abbreviated_path
        Set
            options.verbosity
            options.verbose_abbreviated_path

        Since the latter cannot be disabled via ignored_args (it never appears as a
            command line option), we do the next best thing
            by not overriding whatever the user sets

    """
    #
    #   verbosity specified manually or deliberately disabled: use that
    #
    if options.verbose is None or isinstance(options.verbose, int):
        #   verbose_abbreviated_path default to None unless set explicity by the user
        #       in which case we shall prudently not override it!
        #   verbose_abbreviated_path of None will be set to the default at
        #       pipeline_run() / pipeline_printout()
        if not hasattr(options, "verbose_abbreviated_path"):
            setattr(options, "verbose_abbreviated_path", None)
        return options
    #
    #   The user is having a laugh by passing in a string!
    #       wrap in list
    if isinstance(options.verbose, str):
        options.verbose = [options.verbose]
    #
    #
    curr_verbosity = 0
    curr_verbose_abbreviated_path = None
    import re
    match_regex = re.compile(r"(\+)|(\d+)(?::(\-?\d+))?")
    #
    #   Each verbosity specifier can be
    #       '+'         : i.e. --verbose. This just increases the current verbosity value by 1
    #       '\d+'       : e.g. --verbose 6. This (re)sets the verbosity value
    #       '\d+:\d+'   : e.g. --verbose 7:-5 The second number is the verbose_abbreviated_path
    #
    for vv in options.verbose:
        mm = match_regex.match(vv)
        if not mm:
            raise Exception(
                "error: verbosity argument is specified as --verbose INT or --verbose INT:INT. invalid value '%s'" % vv)
        if mm.group(1):
            curr_verbosity += 1
        else:
            curr_verbosity = int(mm.group(2))
            if mm.group(3):
                curr_verbose_abbreviated_path = int(mm.group(3))
    #
    # set verbose_abbreviated_path unless set explicity by the user
    #   in which case we shall prudently not override it!
    if not hasattr(options, "verbose_abbreviated_path"):
        setattr(options, "verbose_abbreviated_path",
                curr_verbose_abbreviated_path)
    options.verbose = curr_verbosity
    #
    return options


# _________________________________________________________________________________________

#   run

# _________________________________________________________________________________________
def run(options, **extra_options):
    """
    Take action depending on options
    extra_options are passed (as appropriate to the underlying functions
    Returns True if pipeline_run
    """

    #
    #   be very defensive: these options names are use below. Make sure they already
    #       exist in ``options`` , even if they have a value of None
    #
    for attr_name in ["just_print",
                      "verbose",
                      "flowchart",
                      "flowchart_format",
                      "target_tasks",
                      "forced_tasks",
                      "draw_horizontally",
                      "key_legend_in_graph",
                      "use_threads",
                      "jobs",
                      "recreate_database",
                      "touch_files_only",
                      "history_file"]:
        if not hasattr(options, attr_name):
            setattr(options, attr_name, None)

    #
    #   handle verbosity specification
    #
    #       the special attribute verbose_abbreviated_path is set in this function
    options = handle_verbose(options)

    #
    #   touch files or not
    #
    if options.recreate_database:
        touch_files_only = CHECKSUM_REGENERATE
    elif options.touch_files_only:
        touch_files_only = True
    else:
        touch_files_only = False

    if options.just_print:
        appropriate_options = get_extra_options_appropriate_for_command(
            extra_pipeline_printout_options, extra_options)
        task.pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks,
                               history_file=options.history_file,
                               verbose_abbreviated_path=options.verbose_abbreviated_path,
                               verbose=options.verbose, **appropriate_options)
        return False

    elif options.flowchart:
        appropriate_options = get_extra_options_appropriate_for_command(
            extra_pipeline_printout_graph_options, extra_options)
        task.pipeline_printout_graph(open(options.flowchart, "wb"),
                                     options.flowchart_format,
                                     options.target_tasks,
                                     options.forced_tasks,
                                     history_file=options.history_file,
                                     draw_vertically=not options.draw_horizontally,
                                     no_key_legend=not options.key_legend_in_graph,
                                     **appropriate_options)
        return False
    else:

        #
        #   turn on multithread if --use_threads specified and --jobs > 1
        #       ignore if manually specified
        #
        if (options.use_threads
                # ignore if manual override
                and not "multithread" in extra_options
                and options.jobs and options.jobs > 1):
            multithread = options.jobs
        elif "multithread" in extra_options:
            multithread = extra_options["multithread"]
            del extra_options["multithread"]
        else:
            multithread = None

        if not "logger" in extra_options:
            extra_options["logger"] = None
        if extra_options["logger"] == False:
            extra_options["logger"] = task.black_hole_logger
        elif extra_options["logger"] is None:
            extra_options["logger"] = task.stderr_logger
        appropriate_options = get_extra_options_appropriate_for_command(
            extra_pipeline_run_options, extra_options)
        task.pipeline_run(options.target_tasks,
                          options.forced_tasks,
                          multiprocess=options.jobs,
                          multithread=multithread,
                          verbose=options.verbose,
                          touch_files_only=touch_files_only,
                          history_file=options.history_file,
                          verbose_abbreviated_path=options.verbose_abbreviated_path,
                          **appropriate_options)
        return True
