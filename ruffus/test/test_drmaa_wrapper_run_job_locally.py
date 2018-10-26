#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
from ruffus.drmaa_wrapper import write_job_script_to_temp_file, read_stdout_stderr_from_files
import ruffus.drmaa_wrapper
import ruffus
import sys

"""

    test_drmaa_wrapper_run_job_locally.py

"""

import os
script_dir = os.path.abspath(os.path.dirname(__file__))
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0]))

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class Test_ruffus(unittest.TestCase):

    class t_test_logger:

        """
        Does nothing!
        """

        def __init__(self):
            self.clear()

        def clear(self):
            self.info_msg = []
            self.debug_msg = []
            self.warning_msg = []
            self.error_msg = []

        def info(self, message, *args, **kwargs):
            self.info_msg.append(message)

        def debug(self, message, *args, **kwargs):
            self.debug_msg.append(message)

        def warning(self, message, *args, **kwargs):
            self.warning_msg.append(message)

        def error(self, message, *args, **kwargs):
            self.error_msg.append(message)

    # ___________________________________________________________________________
    #
    #   setup and cleanup
    # ___________________________________________________________________________

    def setUp(self):
        try:
            os.mkdir(tempdir)
        except OSError:
            pass

    def tearDown(self):
        shutil.rmtree(tempdir)

    def test_read_stdout_stderr_from_files(self):
        #
        #   Test missing stdout and stderr files
        #
        stdout_path = os.path.join(tempdir, "stdout.txt")
        stderr_path = os.path.join(tempdir, "stderr.txt")
        logger = Test_ruffus.t_test_logger()
        read_stdout_stderr_from_files(
            stdout_path, stderr_path, logger, cmd_str="test_cmd", tries=0)
        self.assertTrue("could not open stdout" in "".join(logger.warning_msg))
        self.assertTrue("could not open stderr" in "".join(logger.warning_msg))
        logger.clear()

        #
        #   Test present stdout and stderr files
        #
        with open(stdout_path, "w") as so:
            so.write("STDOUT\nSTDOUT\n")
        with open(stderr_path, "w") as se:
            se.write("STDERR\nSTDERR\n")

        stdout_msg, stderr_msg = read_stdout_stderr_from_files(
            stdout_path, stderr_path, logger, cmd_str="test_cmd", tries=1)
        self.assertEqual(logger.warning_msg, [])
        self.assertEqual(stdout_msg, ["STDOUT\n", "STDOUT\n"])
        self.assertEqual(stderr_msg, ["STDERR\n", "STDERR\n"])

    def test_run_job(self):
        environ = {"RUFFUS_HEEHEE": "what?"}
        home_dir = os.path.expanduser("~")
        sys.stderr.write("    Run echoing to screen...\n")
        stdout, stderr = ruffus.drmaa_wrapper.run_job(cmd_str="python %s/slow_process_for_testing.py" % script_dir,
                                                      job_environment=environ,
                                                      working_directory=home_dir,
                                                      run_locally=True,
                                                      verbose=1,
                                                      local_echo=True)
        sys.stderr.write("    Run silently...\n")
        stdout, stderr = ruffus.drmaa_wrapper.run_job(cmd_str="python %s/slow_process_for_testing.py" % script_dir,
                                                      job_environment=environ,
                                                      working_directory=home_dir,
                                                      run_locally=True,
                                                      verbose=1,
                                                      local_echo=False)
        self.assertEqual(
            stdout,
            ['    Stdout 0\n', '    Stdout 1\n', '    Stdout 2\n', '    Stdout 3\n'])

        stderr_fixed = [stderr[x] for x in (0, 2, 3, 4, 5)]
        stderr_variable = stderr[1]
        self.assertEqual(
            stderr_fixed,
            ['     %s\n' % home_dir,
             '    Stderr 0\n',
             '    Stderr 1\n',
             '    Stderr 2\n',
             '    Stderr 3\n'])
        self.assertTrue("'PWD': '{}'".format(home_dir) in stderr_variable)
        self.assertTrue("'RUFFUS_HEEHEE': 'what?'" in stderr_variable)

    def test_write_job_script_to_temp_file(self):
        sys.stderr.write("    Write to temp_file...\n")
        job_script_path, stdout_path, stderr_path = write_job_script_to_temp_file(
            "ls", None, "job_name", "", None, None)
        os.unlink(job_script_path)
        job_script_path, stdout_path, stderr_path = write_job_script_to_temp_file(
            "ls", tempdir, "job_name", "", None, None)

    def test_ls(self):
        sys.stderr.write("    ls...\n")
        with open(os.path.join(tempdir, "temp.txt"), "w") as oo:
            oo.write("done")
        stdout, stderr = ruffus.drmaa_wrapper.run_job(cmd_str="ls %s" % tempdir,
                                                      run_locally=True,
                                                      verbose=1,
                                                      local_echo=True)
        self.assertEqual(stdout, ['temp.txt\n'])


if __name__ == '__main__':
    unittest.main()
