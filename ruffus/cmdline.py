#!/usr/bin/env python
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


def get_argparse (*args, **args_dict):
    """
    Common options:

            --verbose
            --version
            --log_file
    """
    import argparse

    parser = argparse.ArgumentParser(*args, **args_dict)

    return append_to_argparse(parser)

def append_to_argparse (parser):
    """
    Common options:

            --verbose
            --version
            --log_file
    """



    common_options = parser.add_argument_group('Common options')
    common_options.add_argument('--verbose', "-v", const=1, default=0, nargs='?', type= int,
                                help="Print more verbose messages for each additional verbose level.")
    common_options.add_argument('--version', action='version', version='%(prog)s 1.0')
    common_options.add_argument("-L", "--log_file", metavar="FILE", type=str,
                                  help="Name and path of log file")


    #
    #   pipeline
    #
    pipline_options = parser.add_argument_group('pipeline arguments')
    pipline_options.add_argument("-T", "--target_tasks", action="append",
                                metavar="JOBNAME", type=str,
                                help="Target task(s) of pipeline.", default = [])
    pipline_options.add_argument("-j", "--jobs", default=1, metavar="N", type=int,
                                help="Allow N jobs (commands) to run simultaneously.")
    pipline_options.add_argument("-n", "--just_print", action="store_true",
                                help="Don't actually run any commands; just print the pipeline.")
    pipline_options.add_argument("--flowchart", metavar="FILE", type=str,
                                help="Don't run any commands; just print pipeline as a flowchart.")

    #
    #   Less common pipeline options
    #
    pipline_options.add_argument("--key_legend_in_graph",     action="store_true",
                                help="Print out legend and key for dependency graph.")
    pipline_options.add_argument("--draw_graph_horizontally", action="store_true",
                                help="Draw horizontal dependency graph.")
    pipline_options.add_argument("--flowchart_format", metavar="FORMAT",
                                type=str, choices = ["svg", "svgz", "png", "jpg", "pdf", "dot"],
                                #  "eps", "jpeg", "gif", "plain", "ps", "wbmp", "canon",
                                #  "cmap", "cmapx", "cmapx_np", "fig", "gd", "gd2",
                                # "gv", "imap", "imap_np", "ismap", "jpe", "plain-ext",
                                # "ps2", "tk", "vml", "vmlz", "vrml", "x11", "xdot", "xlib"
                                default = 'svg',
                                help="format of dependency graph file. Can be 'pdf', " +
                                      "'svg', 'svgz' (Structured Vector Graphics), 'pdf', " +
                                      "'png' 'jpg' (bitmap  graphics) etc ")
    pipline_options.add_argument("--forced_tasks", action="append",
                                metavar="JOBNAME", type=str,
                                help="Task(s) which will be included even if they are up to date.", default = [])



    return parser




def get_optparse (*args, **args_dict):
    """
    Common options:

            --verbose
            --version
            --log_file
    """
    from optparse import OptionParser

    parser = OptionParser(*args, **args_dict)

    return append_to_argparse(parser)

def append_to_optparse (parser):
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
            --key_legend_in_graph
            --draw_graph_horizontally
            --flowchart_format
            --forced_tasks

    """
    #
    #   general options: verbosity / logging
    #
    parser.add_option("-v", "--verbose", dest = "verbose",
                      action="count", default=0,
                      help="Print more verbose messages for each additional verbose level.")
    parser.add_option("-L", "--log_file", dest="log_file",
                      metavar="FILE",
                      type="string",
                      help="Name and path of log file")
    #
    #   pipeline
    #
    parser.add_option("-t", "--target_tasks", dest="target_tasks",
                        action="append",
                        default = list(),
                        metavar="JOBNAME",
                        type="string",
                        help="Target task(s) of pipeline.")
    parser.add_option("-j", "--jobs", dest="jobs",
                        default=1,
                        metavar="N",
                        type="int",
                        help="Allow N jobs (commands) to run simultaneously.")
    parser.add_option("-n", "--just_print", dest="just_print",
                        action="store_true", default=False,
                        help="Don't actually run any commands; just print the pipeline.")
    parser.add_option("--flowchart", dest="flowchart",
                        metavar="FILE",
                        type="string",
                        help="Don't actually run any commands; just print the pipeline "
                             "as a flowchart.")

    #
    #   Less common pipeline options
    #
    parser.add_option("--key_legend_in_graph", dest="key_legend_in_graph",
                        action="store_true", default=False,
                        help="Print out legend and key for dependency graph.")
    parser.add_option("--draw_graph_horizontally", dest="draw_horizontally",
                        action="store_true", default=False,
                        help="Draw horizontal dependency graph.")
    parser.add_option("--flowchart_format", dest="flowchart_format",
                        metavar="FORMAT",
                        type="string",
                        default = 'svg',
                        help="format of dependency graph file. Can be 'ps' (PostScript), "+
                              "'svg' 'svgz' (Structured Vector Graphics), " +
                              "'png' 'gif' (bitmap  graphics) etc ")
    parser.add_option("--forced_tasks", dest="forced_tasks",
                        action="append",
                        default = list(),
                        metavar="JOBNAME",
                        type="string",
                        help="Pipeline task(s) which will be included even if they are up to date.")


    return parser




import logging
import logging.handlers
MESSAGE = 15
logging.addLevelName(MESSAGE, "MESSAGE")
import task
import proxy_logger
import sys

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Logger


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#   Allow logging across Ruffus pipeline
#
def setup_logging (module_name, log_file_name, verbose):
    return proxy_logger.make_shared_logger_and_proxy (setup_logging_factory, module_name, [log_file_name, verbose])


def setup_logging_factory (logger_name, args):
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
        handler.setFormatter(stipped_down_formatter("%(asctime)s - %(name)s - %(levelname)6s - %(message)s", "%H:%M:%S"))
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




extra_pipeline_printout_graph_options = [
                                            "ignore_upstream_of_target"      ,
                                            "skip_uptodate_tasks"            ,
                                            "gnu_make_maximal_rebuild_mode"  ,
                                            "test_all_task_for_update"       ,
                                            "minimal_key_legend"             ,
                                            "user_colour_scheme"             ,
                                            "pipeline_name"                  ,
                                            "size"                           ,
                                            "dpi"                            ,
                                            "runtime_data"                   ,
                                         ]
extra_pipeline_printout_options   = [
                                            "indent"                        ,
                                            "gnu_make_maximal_rebuild_mode" ,
                                            "wrap_width"                    ,
                                            "runtime_data"]

extra_pipeline_run_options = [
                                "gnu_make_maximal_rebuild_mode"     ,
                                "runtime_data"                      ,
                                "one_second_per_job"                ,
                                "touch_files_only"                  ,
                                "logger"                            ,
                                "exceptions_terminate_immediately"  ,
                                "log_exceptions"]


def get_extra_options_appropriate_for_command (appropriate_option_names, extra_options):
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



def run (options, **extra_options):
    """
    Take action depending on options
    extra_options are passed (as appropriate to the underlying functions
    Returns True if pipeline_run
    """


    if options.just_print:
        appropriate_options = get_extra_options_appropriate_for_command (extra_pipeline_printout_options, extra_options)
        task.pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks,
                                verbose=options.verbose, **appropriate_options)
        return False

    elif options.flowchart:
        appropriate_options = get_extra_options_appropriate_for_command (extra_pipeline_printout_graph_options, extra_options)
        task.pipeline_printout_graph (   open(options.flowchart, "w"),
                                        options.flowchart_format,
                                        options.target_tasks,
                                        options.forced_tasks,
                                        draw_vertically = not options.draw_horizontally,
                                        no_key_legend   = not options.key_legend_in_graph,
                                        **appropriate_options)
        return False
    else:
        if not "logger" in extra_options:
            extra_options["logger"] = None
        if extra_options["logger"] == False:
           extra_options["logger"] = task.black_hole_logger
        elif extra_options["logger"] == None:
            extra_options["logger"] = task.stderr_logger
        appropriate_options = get_extra_options_appropriate_for_command (extra_pipeline_run_options, extra_options)
        task.pipeline_run(  options.target_tasks,
                            options.forced_tasks,
                            multiprocess    = options.jobs,
                            verbose         = options.verbose,
                            **appropriate_options)
        return True


