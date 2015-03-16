#!/usr/bin/env python
from __future__ import print_function
"""

    test_cmdline.py



"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"
import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
import ruffus
from ruffus import *
from ruffus.cmdline import handle_verbose
from ruffus.proxy_logger import make_shared_logger_and_proxy, setup_std_shared_logger

import logging
import unittest
import re
import shutil



#import traceback


class Test_Logging(unittest.TestCase):



    def test_rotating_log(self):
        """
            test rotating via proxy
        """
        open("/tmp/lg.log", "w").close()
        args={}
        args["file_name"] = "/tmp/lg.log"
        args["rotating"] = True
        args["maxBytes"]=20000
        args["backupCount"]=10
        #args["level"]= logging.INFO
        (my_log,
         logging_mutex) = make_shared_logger_and_proxy (setup_std_shared_logger,
                                                        "my_logger", args)
        with logging_mutex:
            my_log.debug('This is a debug message')
            my_log.info('This is an info message')
            my_log.warning('This is a warning message')
            my_log.error('This is an error message')
            my_log.critical('This is a critical error message')
            my_log.log(logging.ERROR, 'This is a debug message')
        with open("/tmp/lg.log") as ii:
            self.assertTrue(ii.read() == \
"""This is a warning message
This is an error message
This is a critical error message
This is a debug message
""")


#
#   debug code not run if called as a module
#
if __name__ == '__main__':
    unittest.main()

