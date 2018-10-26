#!/usr/bin/env python
from __future__ import print_function
import shutil
import logging
import unittest
from ruffus.proxy_logger import make_shared_logger_and_proxy, setup_std_shared_logger
from ruffus import originate, transform, suffix, merge, pipeline_run, Pipeline
import sys

"""

    test_with_logger.py

"""


import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"
input_file_names = [os.path.join(tempdir, "%d.1" % fn) for fn in range(20)]
final_file_name = os.path.join(tempdir, "final.result")
try:
    os.makedirs(tempdir)
except:
    pass


# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

def write_input_output_filenames_to_output(infiles, outfile, logger_proxy, logging_mutex):
    """
    Helper function: Writes input output file names and input contents to outfile
    """
    with open(outfile, "w") as oo:
        # save file name strings before we turn infiles into a list
        fn_str = "%s -> %s" % (infiles, outfile)

        # None = []
        if infiles is None:
            infiles = []
        # str = [str]
        if not isinstance(infiles, list):
            infiles = [infiles]

        max_white_space = -2
        # write content of infiles indented
        for infile in infiles:
            with open(infile) as ii:
                for line in ii:
                    oo.write(line)
                    max_white_space = max(
                        [max_white_space, len(line) - len(line.lstrip())])
        # add extra spaces before filenames
        oo.write(" " * (max_white_space + 2) + fn_str + "\n")

    with logging_mutex:
        logger_proxy.info(fn_str)


#
#   Make logger
#
#import logging
args = dict()
args["file_name"] = os.path.join(tempdir, module_name + ".log")
args["level"] = logging.DEBUG
args["rotating"] = True
args["maxBytes"] = 20000
args["backupCount"] = 10
args["formatter"] = "%(asctime)s - %(name)s - %(levelname)6s - %(message)s"

if sys.version_info[0] == 3 and sys.version_info[1] == 2 and __name__ != "__main__":
    print(
        """
    888888888888888888888888888888888888888888888888888888888888888888888888888

        ERROR:

    This unit test can not be run as a python module (python -m unittest xxx)
    due to the interaction of bugs / misfeatures in the multiprocessing module
    and python3.2

        See http://bugs.python.org/issue15914
            http://bugs.python.org/issue9573

    In detail:

    Making a shared logger calls code within the multiprocessing module.
    This in turn tries to import the hmac module inside deliver_challenge().
    This hangs if it happens after a module fork.

    The only way around this is to only make calls to multiprocessing
    (i.e. make_shared_logger_and_proxy(...)) after the import phase of
    module loading.

    This python bug will be triggered if your make_shared_logger_and_proxy()
    call is at global scope in a module (i.e. not __main__) and only for
    python version 3.2

    888888888888888888888888888888888888888888888888888888888888888888888888888

""")
    sys.exit()

(logger_proxy,
 logging_mutex) = make_shared_logger_and_proxy(setup_std_shared_logger,
                                               "my_logger", args)


#
#    task1
#
@originate(input_file_names, logger_proxy, logging_mutex)
def task1(outfile, logger_proxy, logging_mutex):
    write_input_output_filenames_to_output(
        None, outfile, logger_proxy, logging_mutex)


#
#    task2
#
@transform(task1, suffix(".1"), ".2", logger_proxy, logging_mutex)
def task2(infile, outfile, logger_proxy, logging_mutex):
    write_input_output_filenames_to_output(
        infile, outfile, logger_proxy, logging_mutex)


#
#    task3
#
@transform(task2, suffix(".2"), ".3", logger_proxy, logging_mutex)
def task3(infile, outfile, logger_proxy, logging_mutex):
    """
    Third task
    """
    write_input_output_filenames_to_output(
        infile, outfile, logger_proxy, logging_mutex)


#
#    task4
#
@merge(task3, final_file_name, logger_proxy, logging_mutex)
def task4(infile, outfile, logger_proxy, logging_mutex):
    """
    Fourth task
    """
    write_input_output_filenames_to_output(
        infile, outfile, logger_proxy, logging_mutex)


class Test_ruffus(unittest.TestCase):
    def setUp(self):
        self.tearDown()
        try:
            os.makedirs(tempdir)
            #sys.stderr.write("    Created %s\n" % tempdir)
        except:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
            #sys.stderr.write("    Removed %s\n" % tempdir)
            pass
        except:
            pass

    def test_simpler(self):
        pipeline_run(multiprocess=500, verbose=0, pipeline="main")

    def test_newstyle_simpler(self):
        test_pipeline = Pipeline("test")
        test_pipeline.originate(task1, input_file_names, extras=[
                                logger_proxy, logging_mutex])
        test_pipeline.transform(task2, task1, suffix(
            ".1"), ".2", extras=[logger_proxy, logging_mutex])
        test_pipeline.transform(task3, task2, suffix(
            ".2"), ".3", extras=[logger_proxy, logging_mutex])
        test_pipeline.merge(task4, task3, final_file_name,
                            extras=[logger_proxy, logging_mutex])
        #test_pipeline.merge(task4, task3, final_file_name, extras = {"logger_proxy": logger_proxy, "logging_mutex": logging_mutex})
        test_pipeline.run(multiprocess=500, verbose=0)


if __name__ == '__main__':
    unittest.main()
