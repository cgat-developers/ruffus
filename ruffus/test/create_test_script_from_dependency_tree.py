#!/usr/bin/env python
from __future__ import print_function
from adjacent_pairs_iterate import adjacent_pairs_iterate
import random
from collections import defaultdict
import sys
import operator
import re
from ruffus import *
"""

    draw_specified_dependency_tree.py

"""


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys
import os
import os.path
try:
    import StringIO as io
except:
    import io as io

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0]
else:
    module_name = __name__

# graph, task etc are one directory down
if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(exe_path, "..", "..")))


parser = OptionParser(version="%prog 1.0")
parser.add_option("-i", "--input_dot_file", dest="dot_file",
                  metavar="FILE",
                  default=os.path.join(
                      exe_path, "dependency_data", "simple.dag"),
                  type="string",
                  help="name and path of tree file in modified DOT format used to generate "
                  "test script dependencies.")
parser.add_option("-o", "--output_file", dest="output_file",
                  metavar="FILE",
                  default=os.path.join(exe_path, "pipelines", "simple.py"),
                  type="string",
                  help="name and path of output python test script.")
parser.add_option("-v", "--verbose", dest="verbose",
                  action="count", default=0,
                  help="Print more verbose messages for each additional verbose level.")
parser.add_option("-J", "--jumble_task_order", dest="jumble_task_order",
                  action="store_true", default=False,
                  help="Do not define task functions in order of dependency.")

parameters = [
]

mandatory_parameters = ["dot_file"]


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

dumps = json.dumps

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# _________________________________________________________________________________________

#   make_tree_from_dotfile

# _________________________________________________________________________________________


# _________________________________________________________________________________________

#   task_dependencies_from_dotfile

# _________________________________________________________________________________________
def task_dependencies_from_dotfile(stream):
    """
    Read programme task specified in dot file format
    """

    decorator_regex = re.compile(r"([a-z_]+) *(\(.*)")
    attributes_regex = re.compile(r"\[.*\]")

    which_task_follows = defaultdict(list)
    task_decorators = defaultdict(list)
    task_descriptions = dict()

    #
    #   remember node
    #

    all_tasks = dict()
    io_tasks = set()
    for linenum, line in enumerate(stream):
        # remove heading and trailing spaces
        line = line.strip()

        if "digraph" in line:
            continue
        if not len(line):
            continue

        #
        #   decorators
        #
        if line[0:2] == '#@':
            fields = line[2:].split('::', 2)
            if len(fields) != 3:
                raise Exception("Unexpected task specification on line# %d\n(%s)" %
                                (linenum, line))
            task_name, decorators, description = fields
            if decorators[0] != '@':
                raise Exception("Task decorator missing starting ampersand '@' on line# %d\n(%s)" %
                                (linenum, line))
            for d in decorators[1:].split("@"):
                m = decorator_regex.match(d)
                if not m:
                    raise Exception("Task decorator (%s) missing parentheses on line# %d\n(%s)" %
                                    (d, linenum, line))
                task_decorators[task_name].append((m.group(1), m.group(2)))
                if m.group(1)[0:5] == "files" or m.group(1) == "parallel":
                    io_tasks.add(task_name)

            task_descriptions[task_name] = description
            continue

        #
        #   other comments
        #
        if line[0] in '#{}/':
            continue
        line = line.strip(';')
        line = attributes_regex.sub("", line)

        #
        #   ignore assignments
        #
        if "=" in line:
            continue
        nodes = [x.strip() for x in line.split('->')]
        for name1, name2 in adjacent_pairs_iterate(nodes):
            which_task_follows[name2].append(name1)
            all_tasks[name1] = 1
            all_tasks[name2] = 1

    for task in task_decorators:
        if task not in all_tasks:
            raise Exception("Decorated task %s not in dependencies")

    # order tasks by precedence the dump way: iterating until true
    disordered = True
    while (disordered):
        disordered = False
        for to_task, from_tasks in which_task_follows.items():
            for f in from_tasks:
                if all_tasks[to_task] <= all_tasks[f]:
                    all_tasks[to_task] += all_tasks[f]
                    disordered = True

    sorted_task_names = list(
        sorted(list(all_tasks.keys()), key=lambda x: all_tasks[x]))
    return which_task_follows, sorted_task_names, task_decorators, io_tasks, task_descriptions


# _________________________________________________________________________________________

#   generate_program_task_file

# _________________________________________________________________________________________
def generate_program_task_file(stream, task_dependencies, task_names,
                               task_decorators, io_tasks, task_descriptions):

    print("task_decorators   = ", dumps(
        task_decorators, indent=4), file=sys.stderr)
    print("task_names        = ", dumps(task_names), file=sys.stderr)
    print("task_dependencies = ", dumps(task_dependencies), file=sys.stderr)
    print("io_tasks          = ", dumps(list(io_tasks)), file=sys.stderr)

    if options.jumble_task_order:
        random.shuffle(task_names)
    defined_tasks = set()

    #
    #   iterate through tasks
    #
    for task_name in task_names:
        defined_tasks.add(task_name)
        stream.write("\n#\n#    %s\n#\n" % task_name)
        #
        #   write task decorators
        #
        if task_name in task_decorators:
            for decorator, decorator_parameters in task_decorators[task_name]:
                stream.write("@" + decorator + decorator_parameters + "\n")

        #
        #   write task dependencies
        #
        if task_name in task_dependencies:
            params = ", ".join(t if t in defined_tasks else '"%s"' % t
                               for t in task_dependencies[task_name])
            stream.write("@follows(%s)\n" % params)

        #
        #   Function body
        #
        # if task_name in io_tasks:
        if 1:
            stream.write(
                "def %s(infiles, outfiles, *extra_params):\n" % task_name)
            stream.write('    """\n')
            description = task_descriptions[task_name]
            description = description.replace("\n", "    \n")
            stream.write('    %s\n' % description)
            stream.write('    """\n')

            stream.write("    test_job_io(infiles, outfiles, extra_params)\n")
        # else:
        #    stream.write("def %s(*params):\n" % task_name)

        stream.write("\n\n")

    stream.write(
        """
#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    try:
        if options.just_print:
            pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks,
                                long_winded=True,
                                gnu_make_maximal_rebuild_mode = not options.minimal_rebuild_mode)

        elif options.dependency_file:
            pipeline_printout_graph (     open(options.dependency_file, "w"),
                                 options.dependency_graph_format,
                                 options.target_tasks,
                                 options.forced_tasks,
                                 draw_vertically = not options.draw_horizontally,
                                 gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                                 no_key_legend  = options.no_key_legend_in_graph)
        else:
            pipeline_run(options.target_tasks, options.forced_tasks, multiprocess = options.jobs,
                            gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                            pipeline= "main")
except Exception, e:
    print e.args
    \n""")


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# get help string
f = io.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
(options, remaining_args) = parser.parse_args()
# mandatory options
for parameter in mandatory_parameters:
    if options.__dict__[parameter] is None:
        die_error("Please specify a file in --%s.\n\n" % parameter + helpstr)


(task_dependencies, task_names,
    task_decorators, io_tasks,
    task_descriptions) = task_dependencies_from_dotfile(open(options.dot_file))

output_file = open(options.output_file, "w")

#
#   print template for python file output
#
output_file.write(open(os.path.join(exe_path, "test_script.py_template")).read().
                  replace("PYPER_PATH",
                          os.path.abspath(os.path.join(exe_path, "..", ".."))))
generate_program_task_file(output_file, task_dependencies, task_names,
                           task_decorators, io_tasks, task_descriptions)
