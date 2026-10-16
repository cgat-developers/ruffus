#!/usr/bin/env python
from __future__ import print_function
import unittest
from ruffus import pipeline_run, Pipeline, parallel, proxy_logger
import ruffus

"""

    test_exceptions.py

"""


import os
import sys
import logging

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def logging_factory(logger_name, listargs):
    root_logger = logging.getLogger(logger_name)
    root_logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stderr)
    formatter_ = logging.Formatter("%(levelname)7s - %(message)s")
    handler.setFormatter(formatter_)
    handler.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    return root_logger
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

def parallel_task(name, param1, log, log_mutex):
    sys.stderr.write("    Parallel task %s: \n" % name)
    #raise task.JobSignalledBreak("Oops! I did it again!")
    with log_mutex:
        log.info("    Raising exception")
    raise Exception("new")


try:
    from StringIO import StringIO
except:
    from io import StringIO


class Test_ruffus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Spawn/forkserver workers import this module: only the parent creates
        # the manager, and workers receive its proxies as explicit job arguments.
        global log, log_mutex
        log, log_mutex = proxy_logger.make_shared_logger_and_proxy(
            logging_factory, __name__, [])
        cls.jobs = [[name, value, log, log_mutex] for name, value in
                    [('A', 1), ('B', 3), ('C', 3), ('D', 4), ('E', 4), ('F', 4)]]
        parallel(cls.jobs)(parallel_task)

    def test_ruffus(self):
        try:
            pipeline_run(multiprocess=4, verbose=0, pipeline="main")
        except ruffus.ruffus_exceptions.RethrownJobError:
            return
        raise Exception("Missing exception")

    def test_exception_logging(self):
        try:
            pipeline_run(multiprocess=4, verbose=0, pipeline="main")
        except ruffus.ruffus_exceptions.RethrownJobError as e:
            log.info(e)
            self.assertTrue(e.job_exceptions)
            for exc in e.job_exceptions:
                task_name, job_name, exc_name, exc_value, exc_stack = exc
                self.assertEqual(exc_name, 'builtins.Exception')
                self.assertEqual(exc_value, '(new)')
            return
        raise Exception("Missing exception")

    def test_newstyle_ruffus(self):
        test_pipeline = Pipeline("test")
        test_pipeline.parallel(parallel_task, self.jobs)
        try:
            test_pipeline.run(multiprocess=4, verbose=0)
        except ruffus.ruffus_exceptions.RethrownJobError:
            return
        raise Exception("Missing exception")


if __name__ == '__main__':
    unittest.main()
