#!/usr/bin/env python
from __future__ import print_function
import unittest
from ruffus.ruffus_utility import CHECKSUM_HISTORY_TIMESTAMPS
from ruffus.file_name_parameters import open_job_history
from ruffus import parallel, pipeline_run, Pipeline, task
import ruffus
import sys
import os

"""
    test_task_file_dependencies.py
"""
history_file = ':memory:'
history_file = False


# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name


class dummy_task (object):
    checksum_level = CHECKSUM_HISTORY_TIMESTAMPS

    def user_defined_work_func(self):
        pass


class Test_needs_update_check_modify_time(unittest.TestCase):

    def setUp(self):
        """
        Create a list of files separated in time so we can do dependency checking
        """
        import tempfile
        import time
        self.files = list()
        job_history = open_job_history(history_file)
        for i in range(6):
            #test_file =tempfile.NamedTemporaryFile(delete=False, prefix='testing_tmp')
            #self.files.append (test_file.name)
            # test_file.close()

            fh, temp_file_name = tempfile.mkstemp(suffix='.dot')
            self.files.append(temp_file_name)
            os.fdopen(fh, "w").close()

            # Save modify time in history file
            mtime = os.path.getmtime(temp_file_name)
            epoch_seconds = time.time()
            # Use epoch seconds unless there is a > 1 second discrepancy between system clock
            # and file system clock
            if epoch_seconds > mtime and epoch_seconds - mtime < 1.1:
                mtime = epoch_seconds
            else:
                # file system clock out of sync:
                #   Use file modify times: slow down in case of low counter resolution
                #       (e.g. old versions of NFS and windows)
                time.sleep(2)
            chksum = task.JobHistoryChecksum(
                temp_file_name, mtime, "", dummy_task())
            job_history[os.path.relpath(temp_file_name)] = chksum

    def tearDown(self):
        """
        delete files
        """
        for f in self.files:
            os.unlink(f)

    def test_up_to_date(self):
        #
        #   lists of files
        #
        self.assertTrue(not task.needs_update_check_modify_time(self.files[0:2],
                                                                self.files[2:6],
                                                                job_history=open_job_history(
                                                                    history_file),
                                                                task=dummy_task())[0])
        self.assertTrue(task.needs_update_check_modify_time(self.files[2:6],
                                                            self.files[0:2],
                                                            job_history=open_job_history(
                                                                history_file),
                                                            task=dummy_task())[0])
        #
        #   singletons and lists of files
        #
        self.assertTrue(not task.needs_update_check_modify_time(self.files[0],
                                                                self.files[2:6],
                                                                job_history=open_job_history(
                                                                    history_file),
                                                                task=dummy_task())[0])
        self.assertTrue(task.needs_update_check_modify_time(self.files[2:6],
                                                            self.files[0],
                                                            job_history=open_job_history(
                                                                history_file),
                                                            task=dummy_task())[0])

        #
        #   singletons
        #
        self.assertTrue(task.needs_update_check_modify_time(self.files[3],
                                                            self.files[0],
                                                            job_history=open_job_history(
                                                                history_file),
                                                            task=dummy_task())[0])

        # self -self = no update
        self.assertTrue(not task.needs_update_check_modify_time(self.files[0],
                                                                self.files[0],
                                                                job_history=open_job_history(
                                                                    history_file),
                                                                task=dummy_task())[0])

        #
        #   missing files means need update
        #
        self.assertTrue(task.needs_update_check_modify_time(self.files[0:2] +
                                                            ["uncreated"],
                                                            self.files[3:6],
                                                            job_history=open_job_history(
                                                                history_file),
                                                            task=dummy_task())[0])

        self.assertTrue(task.needs_update_check_modify_time(self.files[0:2],
                                                            self.files[3:6] +
                                                            ["uncreated"],
                                                            job_history=open_job_history(
                                                                history_file),
                                                            task=dummy_task())[0])

        #
        #   None means need update
        #
        self.assertTrue(task.needs_update_check_modify_time(self.files[0:2],
                                                            None,
                                                            job_history=open_job_history(
                                                                history_file),
                                                            task=dummy_task())[0])

        #
        #   None input means need update only if do not exist
        #
        self.assertTrue(not task.needs_update_check_modify_time(None,
                                                                self.files[3:6],
                                                                job_history=open_job_history(
                                                                    history_file),
                                                                task=dummy_task())[0])

        #
        #   None + missing file means need update
        #
        self.assertTrue(task.needs_update_check_modify_time(self.files[0:2] +
                                                            ["uncreated"],
                                                            None,
                                                            job_history=open_job_history(
                                                                history_file),
                                                            task=dummy_task())[0])

        self.assertTrue(task.needs_update_check_modify_time(None,
                                                            self.files[3:6] +
                                                            ["uncreated"],
                                                            job_history=open_job_history(
                                                                history_file),
                                                            task=dummy_task())[0])


if __name__ == '__main__':
    unittest.main()
