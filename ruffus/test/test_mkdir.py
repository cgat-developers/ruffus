#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
from ruffus.ruffus_utility import RUFFUS_HISTORY_FILE, CHECKSUM_FILE_TIMESTAMPS
from ruffus import pipeline_run, pipeline_printout, transform, split, mkdir, formatter, Pipeline
import sys

"""

    test_mkdir.py
        test product, combine, permute, combine_with_replacement

"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0]))


# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#   imports
#
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

try:
    from StringIO import StringIO
except:
    from io import StringIO


# sub-1s resolution in system?
# ___________________________________________________________________________
#
#   generate_initial_files1
# ___________________________________________________________________________
@split(1, [tempdir + "/" + prefix + "_name.tmp1" for prefix in "abcd"])
def generate_initial_files1(in_name, out_names):
    for on in out_names:
        with open(on, 'w') as outfile:
            pass

# ___________________________________________________________________________
#
#   check_product_task
# ___________________________________________________________________________


@mkdir(tempdir + "/test1")
@mkdir(tempdir + "/test2")
@mkdir(generate_initial_files1, formatter(),
       ["{path[0]}/{basename[0]}.dir", 3, "{path[0]}/{basename[0]}.dir2"])
@transform(generate_initial_files1,
           formatter(),
           "{path[0]}/{basename[0]}.dir/{basename[0]}.tmp2")
def check_transform(infiles, outfile):
    with open(outfile, "w") as p:
        pass


@mkdir(tempdir + "/test3")
@mkdir(generate_initial_files1, formatter(),
       "{path[0]}/{basename[0]}.dir2")
def check_transform2():
    print("    Loose cannon!", file=sys.stderr)


def cleanup_tmpdir():
    os.system('rm -f %s %s' %
              (os.path.join(tempdir, '*'), RUFFUS_HISTORY_FILE))


class Testmkdir(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(tempdir)
        except OSError:
            pass

    # ___________________________________________________________________________
    #
    #   test mkdir() pipeline_printout and pipeline_run
    # ___________________________________________________________________________
    def test_mkdir_printout(self):
        """Input file exists, output doesn't exist"""
        cleanup_tmpdir()

        s = StringIO()
        pipeline_printout(s, [check_transform, check_transform2],
                          verbose=5, wrap_width=10000, pipeline="main")
        # self.assertIn('Job needs update: Missing files '
        #              '[tmp_test_mkdir/a_name.tmp1, '
        #              'tmp_test_mkdir/e_name.tmp1, '
        #              'tmp_test_mkdir/h_name.tmp1, '
        #              'tmp_test_mkdir/a_name.e_name.h_name.tmp2]', s.getvalue())

    def test_mkdir_run(self):
        """Run mkdir"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([check_transform, check_transform2],
                     verbose=0, multiprocess=2, pipeline="main")

    def test_newstyle_mkdir_run(self):
        test_pipeline = Pipeline("test")

        test_pipeline.split(task_func=generate_initial_files1,
                            input=1,
                            output=[tempdir + "/" + prefix + "_name.tmp1" for prefix in "abcd"])

        test_pipeline.transform(task_func=check_transform,
                                input=generate_initial_files1,
                                filter=formatter(),
                                output="{path[0]}/{basename[0]}.dir/{basename[0]}.tmp2")\
            .mkdir(tempdir + "/test1")\
            .mkdir(tempdir + "/test2")\
            .mkdir(generate_initial_files1, formatter(),
                   ["{path[0]}/{basename[0]}.dir", 3, "{path[0]}/{basename[0]}.dir2"])

        test_pipeline.mkdir(check_transform2, tempdir + "/test3")\
            .mkdir(generate_initial_files1, formatter(),
                   "{path[0]}/{basename[0]}.dir2")
        cleanup_tmpdir()
        pipeline_run([check_transform, check_transform2],
                     verbose=0, multiprocess=2, pipeline="main")

    # ___________________________________________________________________________
    #
    #   cleanup
    # ___________________________________________________________________________

    def tearDown(self):
        shutil.rmtree(tempdir)


#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    unittest.main()
