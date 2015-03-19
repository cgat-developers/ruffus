#!/usr/bin/env python
from __future__ import print_function
"""

    test_drmaa_wrapper_run_job_locally.py

"""

import os
script_dir = os.path.abspath(os.path.dirname(__file__))
import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


import ruffus
import ruffus.drmaa_wrapper

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import unittest
import shutil

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class Test_ruffus(unittest.TestCase):
    def test_ruffus (self):
        environ = {"RUFFUS_HEEHEE":"what?"}
        home_dir = os.path.expanduser("~")
        sys.stderr.write("    Run silently...\n")
        stdout, stderr = ruffus.drmaa_wrapper.run_job(cmd_str = "python %s/slow_process_for_testing.py" % script_dir,
                                                         job_environment = environ,
                                                         working_directory = home_dir,
                                                         run_locally = True,
                                                         verbose = 1,
                                                         local_echo = False)
        sys.stderr.write("    Run echoing to screen...\n")
        stdout, stderr = ruffus.drmaa_wrapper.run_job(cmd_str = "python %s/slow_process_for_testing.py" % script_dir,
                                                         job_environment = environ,
                                                         working_directory = home_dir,
                                                         run_locally = True,
                                                         verbose = 1,
                                                         local_echo = True)

        self.assertEqual(stdout, ['    Stdout 0\n', '    Stdout 1\n', '    Stdout 2\n', '    Stdout 3\n'])
        self.assertEqual(stderr, ['     %s\n' % home_dir, "     {'PWD': '%s', 'RUFFUS_HEEHEE': 'what?'}\n" % home_dir, '    Stderr 0\n', '    Stderr 1\n', '    Stderr 2\n', '    Stderr 3\n'])

if __name__ == '__main__':
    unittest.main()

