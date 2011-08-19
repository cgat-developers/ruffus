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


    parser = OptionParser(version="%prog 1.0", usage = "\n\n    %prog [options]")
    parser.add_option("-c", "--custom", dest="custom", action="count",
                      help = "Some custom option comes first")


    parser = cmdline.prepare_optparse(parser)

    logger, logger_mutex = cmdline.setup_logging ("this_program", options.log_file, options.verbose)

    (options, remaining_args) = parser.parse_args()

    cmdline.run (options)

"""



def prepare_optparse (parser = None):
    """
    Set up OptionParser from optparse
        to allow for ruffus specific options:

            --verbose
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
    from optparse import OptionParser

    if not parser:
        parser = OptionParser(version="%prog 1.0", usage = "\n\n    %prog [options]")

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
global_logger = None
def get_logger (logger_name, args):
    return global_logger

def setup_logging (module_name, log_file, verbose):
    """
    Set up log using module_name

    """
    global global_logger
    global_logger = logging.getLogger(module_name)

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
    global_logger.setLevel(logging.DEBUG)
    has_handler = False

    # log to file if that is specified
    if log_file:
        handler = logging.FileHandler(log_file, delay=False)
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
        global_logger.addHandler(handler)
        has_handler = True

    # log to stderr if verbose
    if verbose:
        stderrhandler = logging.StreamHandler(sys.stderr)
        stderrhandler.setFormatter(logging.Formatter("    %(message)s"))
        stderrhandler.setLevel(logging.DEBUG)
        if log_file:
            stderrhandler.addFilter(debug_filter())
        global_logger.addHandler(stderrhandler)
        has_handler = True

    # no logging
    if not has_handler:
        global_logger.addHandler(NullHandler())



    return proxy_logger.make_shared_logger_and_proxy (get_logger, module_name, {})



def run (options, option_logger = None):
    """
    Take action depending on options
    """
    global global_logger
    if option_logger == False:
        option_logger = task.black_hole_logger
    elif option_logger == None:
        if global_logger == None:
            raise("Need to call setup_logging() first. For no logging using option_logger = False.")
        option_logger = global_logger

    if options.just_print:
        task.pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks,
                                verbose=options.verbose)

    elif options.flowchart:
        task.pipeline_printout_graph (   open(options.flowchart, "w"),
                                        options.flowchart_format,
                                        options.target_tasks,
                                        options.forced_tasks,
                                        draw_vertically = not options.draw_horizontally,
                                        no_key_legend   = not options.key_legend_in_graph)
    else:
        task.pipeline_run(  options.target_tasks,
                            options.forced_tasks,
                            multiprocess    = options.jobs,
                            logger          = option_logger,
                            verbose         = options.verbose)








