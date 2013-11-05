#!/usr/bin/env python
"""

    test_active_if.py

"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys, os
import os.path
import StringIO

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__




from ruffus import *

parser = cmdline.get_argparse(   description='Test @active_if')


options = parser.parse_args()

#  optional logger which can be passed to ruffus tasks
logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)





#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import StringIO
import re
import operator
import sys,os
from collections import defaultdict


import json

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888






def helper (infiles, outfiles):
    if not isinstance(infiles, tuple) and not isinstance(infiles, list):
        infiles = [infiles]
    if not isinstance(outfiles, list):
        outfiles = [outfiles]

    output_text = ""
    preamble_len = 0
    for infile in infiles:
        if infile:
            for line in open(infile):
                output_text  += line
                preamble_len = max(preamble_len, len(line) - len(line.lstrip()))

    preamble = " " * (preamble_len + 4) if len(output_text) else ""

    for outfile in outfiles:
        file_output_text = preamble + json.dumps(infile) + " -> " + json.dumps(outfile) + "\n"
        open(outfile, "w").write(output_text + file_output_text)



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

pipeline_active_if = True
#
#    task1
#
@follows(mkdir("test_active_if"))
@split(None, ['test_active_if/a.1', 'test_active_if/b.1'])
def task1(infile, outfiles):
    """
    First task
    """
    helper (infile, outfiles)



#
#    task2
#
@transform(task1, suffix(".1"), ".2")
def task2(infile, outfile):
    """
    Second task
    """
    helper (infile, outfile)


#
#    task3
#
@active_if(lambda:pipeline_active_if)
@transform(task1, suffix(".1"), ".3")
def task3(infile, outfile):
    """
    Third task
    """
    helper (infile, outfile)



#
#    task4
#
@collate([task2, task3], regex(r"(.+)\.[23]"), r"\1.4")
def task4(infiles, outfile):
    """
    Fourth task
    """
    helper (infiles, outfile)

#
#    task4
#
@merge(task4, "test_active_if/summary.5")
def task5(infiles, outfile):
    """
    Fifth task
    """
    helper (infiles, outfile)


expected_active_text = """null -> "test_active_if/a.1"
    "test_active_if/a.1" -> "test_active_if/a.2"
null -> "test_active_if/a.1"
    "test_active_if/a.1" -> "test_active_if/a.3"
        "test_active_if/a.3" -> "test_active_if/a.4"
null -> "test_active_if/b.1"
    "test_active_if/b.1" -> "test_active_if/b.2"
null -> "test_active_if/b.1"
    "test_active_if/b.1" -> "test_active_if/b.3"
        "test_active_if/b.3" -> "test_active_if/b.4"
            "test_active_if/b.4" -> "test_active_if/summary.5"
"""

expected_inactive_text = """null -> "test_active_if/a.1"
    "test_active_if/a.1" -> "test_active_if/a.2"
        "test_active_if/a.2" -> "test_active_if/a.4"
null -> "test_active_if/b.1"
    "test_active_if/b.1" -> "test_active_if/b.2"
        "test_active_if/b.2" -> "test_active_if/b.4"
            "test_active_if/b.4" -> "test_active_if/summary.5"
"""

# 
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':

    # active run
    cmdline.run (options)
    active_text = open("test_active_if/summary.5").read()
    if active_text != expected_active_text:
        raise Exception("Error:\n\tExpected\n%s\nInstead\n%s\n"  % (active_text, expected_active_text))
    os.system("rm -rf test_active_if")


    # inactive run
    pipeline_active_if = False
    cmdline.run (options)
    inactive_text = open("test_active_if/summary.5").read()
    if inactive_text != expected_inactive_text:
        raise Exception("Error:\n\tExpected\n%s\nInstead\n%s\n"  % (inactive_text, expected_inactive_text))
    os.system("rm -rf test_active_if")

