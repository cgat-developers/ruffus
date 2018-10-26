#!/usr/bin/env python
from __future__ import print_function
import re
import shutil
import unittest
from ruffus.ruffus_utility import CHECKSUM_FILE_TIMESTAMPS, RUFFUS_HISTORY_FILE, get_default_history_file_name
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus import pipeline_run, pipeline_printout, Pipeline, collate, mkdir, regex, \
    suffix, formatter, originate, transform
import sys
import os

"""

    test_job_history_with_exceptions.py

        Make sure that when an exception is thrown only the current and following tasks fail

"""

# sub-1s resolution in system?
one_second_per_job = None
throw_exception = False

tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#   imports
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

try:
    from StringIO import StringIO
except:
    from io import StringIO


# ___________________________________________________________________________
#
#   generate_initial_files1
# ___________________________________________________________________________
@originate([tempdir + prefix + "_name.tmp1" for prefix in "abcd"])
def generate_initial_files1(on):
    with open(on, 'w') as outfile:
        pass

# ___________________________________________________________________________
#
#   generate_initial_files2
# ___________________________________________________________________________


@originate([tempdir + "e_name.tmp1", tempdir + "f_name.tmp1"])
def generate_initial_files2(on):
    with open(on, 'w') as outfile:
        pass

# ___________________________________________________________________________
#
#   generate_initial_files3
# ___________________________________________________________________________


@originate([tempdir + "/g_name.tmp1", tempdir + "/h_name.tmp1"])
def generate_initial_files3(on):
    with open(on, 'w') as outfile:
        pass

# ___________________________________________________________________________
#
#   generate_initial_files1
# ___________________________________________________________________________


@originate(tempdir + "i_name.tmp1")
def generate_initial_files4(on):
    with open(on, 'w') as outfile:
        pass

# ___________________________________________________________________________
#
#   check_task2
# ___________________________________________________________________________


@collate([generate_initial_files1, generate_initial_files2, generate_initial_files3,
          generate_initial_files4],
         formatter(),
         "{path[0]}/all.tmp2")
# @transform([generate_initial_files1, generate_initial_files2, generate_initial_files3,
#            generate_initial_files4],
#            formatter( ),
#            "{path[0]}/{basename[0]}.tmp2")
def check_task2(infiles, outfile):
    with open(outfile, "w") as p:
        pass
    #print >>sys.stderr, "8" * 80, "\n", "    task2 :%s %s " % (infiles, outfile)

# ___________________________________________________________________________
#
#   check_task3
# ___________________________________________________________________________


@transform(check_task2, suffix(".tmp2"), ".tmp3")
def check_task3(infile, outfile):
    global throw_exception
    if throw_exception != None:
        throw_exception = not throw_exception
    if throw_exception:
        #print >>sys.stderr, "Throw exception for ", infile, outfile
        raise Exception("oops")
    else:
        #print >>sys.stderr, "No throw exception for ", infile, outfile
        pass
    with open(outfile, "w") as p:
        pass
    #print >>sys.stderr, "8" * 80, "\n", "    task3 :%s %s " % (infile, outfile)

# ___________________________________________________________________________
#
#   check_task4
# ___________________________________________________________________________


@transform(check_task3, suffix(".tmp3"), ".tmp4")
def check_task4(infile, outfile):
    with open(outfile, "w") as p:
        pass
    #print >>sys.stderr, "8" * 80, "\n", "    task4 :%s %s " % (infile, outfile)


def cleanup_tmpdir():
    os.system('rm -f %s %s' %
              (os.path.join(tempdir, '*'), RUFFUS_HISTORY_FILE))


VERBOSITY = 5
VERBOSITY = 11

cnt_pipelines = 0


class Test_job_history_with_exceptions(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(tempdir)
        except OSError:
            pass

    # ___________________________________________________________________________
    #
    #   test product() pipeline_printout and pipeline_run
    # ___________________________________________________________________________
    def test_job_history_with_exceptions(self):
        cleanup_tmpdir()
        s = StringIO()
        pipeline_printout(s, [check_task4], verbose=VERBOSITY,
                          wrap_width=10000, pipeline="main")
        # print s.getvalue()

    def create_pipeline(self):
        # each pipeline has a different name
        global cnt_pipelines
        cnt_pipelines = cnt_pipelines + 1
        test_pipeline = Pipeline("test %d" % cnt_pipelines)

        test_pipeline.originate(task_func=generate_initial_files1,
                                output=[tempdir + prefix + "_name.tmp1" for prefix in "abcd"])

        test_pipeline.originate(task_func=generate_initial_files2,
                                output=[tempdir + "e_name.tmp1", tempdir + "f_name.tmp1"])

        test_pipeline.originate(task_func=generate_initial_files3,
                                output=[tempdir + "g_name.tmp1", tempdir + "h_name.tmp1"])

        test_pipeline.originate(task_func=generate_initial_files4,
                                output=tempdir + "i_name.tmp1")

        test_pipeline.collate(task_func=check_task2,
                              input=[generate_initial_files1,
                                     generate_initial_files2,
                                     generate_initial_files3,
                                     generate_initial_files4],
                              filter=formatter(),
                              output="{path[0]}/all.tmp2")

        test_pipeline.transform(task_func=check_task3,
                                input=check_task2,
                                filter=suffix(".tmp2"),
                                output=".tmp3")

        test_pipeline.transform(task_func=check_task4,
                                input=check_task3,
                                filter=suffix(".tmp3"),
                                output=".tmp4")
        return test_pipeline

    def test_job_history_with_exceptions_run(self):
        """Run"""
        for i in range(1):
            cleanup_tmpdir()
            try:
                pipeline_run([check_task4], verbose=0,
                             #multithread = 2,
                             one_second_per_job=one_second_per_job, pipeline="main")
            except:
                pass
            s = StringIO()
            pipeline_printout(
                s, [check_task4], verbose=VERBOSITY, wrap_width=10000, pipeline="main")
            #
            # task 2 should be up to date because exception was throw in task 3
            #
            pipeline_printout_str = s.getvalue()
            correct_order = not re.search(
                'Tasks which will be run:.*\n(.*\n)*Task = check_task2', pipeline_printout_str)
            if not correct_order:
                print(pipeline_printout_str)
            self.assertTrue(correct_order)
            sys.stderr.write(".")
        print()

    def test_newstyle_recreate_job_history(self):
        """Run"""
        test_pipeline = self.create_pipeline()
        global throw_exception
        throw_exception = None
        cleanup_tmpdir()

        #
        #      print "Initial run without creating sqlite file"
        #
        test_pipeline.run([check_task4], verbose=0,
                          checksum_level=CHECKSUM_FILE_TIMESTAMPS,
                          multithread=10,
                          one_second_per_job=one_second_per_job)

        #
        #   print "printout without sqlite"
        #
        s = StringIO()
        test_pipeline.printout(
            s, [check_task4], checksum_level=CHECKSUM_FILE_TIMESTAMPS)
        self.assertTrue(not re.search(
            'Tasks which will be run:.*\n(.*\n)*Task = ', s.getvalue()))
        #
        # print "printout expecting sqlite file"
        #
        s = StringIO()
        test_pipeline.printout(s, [check_task4])
        self.assertTrue(
            re.search('Tasks which will be run:.*\n(.*\n)*Task = ', s.getvalue()))
        #
        #   print "Regenerate sqlite file"
        #
        test_pipeline.run([check_task4],
                          checksum_level=CHECKSUM_FILE_TIMESTAMPS,
                          history_file=get_default_history_file_name(),
                          multithread=1,
                          verbose=0,
                          touch_files_only=2,
                          one_second_per_job=one_second_per_job)
        #
        # print "printout expecting sqlite file"
        #
        s = StringIO()
        test_pipeline.printout(s, [check_task4], verbose=VERBOSITY)
        succeed = not re.search(
            'Tasks which will be run:.*\n(.*\n)*Task = ', s.getvalue())
        if not succeed:
            print(s.getvalue(), file=sys.stderr)
        self.assertTrue(succeed)

        throw_exception = False

    #
    def test_newstyle_job_history_with_exceptions_run(self):
        """Run"""
        test_pipeline = self.create_pipeline()
        for i in range(1):
            cleanup_tmpdir()
            try:
                test_pipeline.run([check_task4], verbose=0,
                                  #multithread = 2,
                                  one_second_per_job=one_second_per_job)
            except:
                pass
            s = StringIO()
            test_pipeline.printout(
                s, [check_task4], verbose=VERBOSITY, wrap_width=10000)
            #
            # task 2 should be up to date because exception was throw in task 3
            #
            pipeline_printout_str = s.getvalue()
            correct_order = not re.search(
                'Tasks which will be run:.*\n(.*\n)*Task = check_task2', pipeline_printout_str)
            if not correct_order:
                print(pipeline_printout_str)
            self.assertTrue(correct_order)
            sys.stderr.write(".")
        print()

    def test_recreate_job_history(self):
        """Run"""
        global throw_exception
        throw_exception = None
        cleanup_tmpdir()

        #
        #      print "Initial run without creating sqlite file"
        #
        pipeline_run([check_task4], verbose=0,
                     checksum_level=CHECKSUM_FILE_TIMESTAMPS,
                     multithread=10,
                     one_second_per_job=one_second_per_job, pipeline="main")

        #
        #   print "printout without sqlite"
        #
        s = StringIO()
        pipeline_printout(
            s, [check_task4], checksum_level=CHECKSUM_FILE_TIMESTAMPS, pipeline="main")
        self.assertTrue(not re.search(
            'Tasks which will be run:.*\n(.*\n)*Task = ', s.getvalue()))
        #
        # print "printout expecting sqlite file"
        #
        s = StringIO()
        pipeline_printout(s, [check_task4], pipeline="main")
        self.assertTrue(
            re.search('Tasks which will be run:.*\n(.*\n)*Task = ', s.getvalue()))
        #
        #   print "Regenerate sqlite file"
        #
        pipeline_run([check_task4],
                     checksum_level=CHECKSUM_FILE_TIMESTAMPS,
                     history_file=get_default_history_file_name(),
                     multithread=1,
                     verbose=0,
                     touch_files_only=2,
                     one_second_per_job=one_second_per_job, pipeline="main")
        #
        # print "printout expecting sqlite file"
        #
        s = StringIO()
        pipeline_printout(s, [check_task4], verbose=VERBOSITY, pipeline="main")
        succeed = not re.search(
            'Tasks which will be run:.*\n(.*\n)*Task = ', s.getvalue())
        if not succeed:
            print(s.getvalue(), file=sys.stderr)
        self.assertTrue(succeed)

        throw_exception = False

    # ___________________________________________________________________________
    #
    #   cleanup
    # ___________________________________________________________________________
    def tearDown(self):
        shutil.rmtree(tempdir)
        pass


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    #pipeline_printout(sys.stdout, [check_product_task], verbose = VERBOSITY, pipeline= "main")
    unittest.main()
