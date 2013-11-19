#!/usr/bin/env python
################################################################################
#
#   __init__.py
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
#from graph import *
#from print_dependencies import *
from task import pipeline_printout, pipeline_printout_graph, pipeline_run, register_cleanup, check_if_uptodate, active_if, split, transform, merge, collate, files, files_re, follows, parallel, stderr_logger, black_hole_logger, suffix, regex, inputs, add_inputs, touch_file, combine, mkdir, output_from, posttask, JobSignalledBreak, runtime_parameter, jobs_limit, formatter, subdivide, originate
from graph  import graph_colour_demo_printout
from file_name_parameters import needs_update_check_modify_time
import cmdline
import combinatorics
#output_dependency_tree_in_dot_format, output_dependency_tree_key_in_dot_format
import ruffus_version
__version__=ruffus_version.__version


