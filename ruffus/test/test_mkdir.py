#!/usr/bin/env python
from __future__ import print_function
"""

    test_mkdir.py
        test product, combine, permute, combine_with_replacement

"""

workdir = 'tmp_test_mkdir'


import os
import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ruffus_name = os.path.basename(parent_dir)
ruffus = __import__ (ruffus_name)

for attr in "pipeline_run", "pipeline_printout", "transform", "split", "mkdir", "formatter", "Pipeline":
    globals()[attr] = getattr (ruffus, attr)
RethrownJobError = ruffus.ruffus_exceptions.RethrownJobError
RUFFUS_HISTORY_FILE      = ruffus.ruffus_utility.RUFFUS_HISTORY_FILE
CHECKSUM_FILE_TIMESTAMPS = ruffus.ruffus_utility.CHECKSUM_FILE_TIMESTAMPS

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#   imports
#
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import unittest
import shutil
try:
    from StringIO import StringIO
except:
    from io import StringIO
import time


#sub-1s resolution in system?
#___________________________________________________________________________
#
#   generate_initial_files1
#___________________________________________________________________________
@split(1, [workdir +  "/" + prefix + "_name.tmp1" for prefix in "abcd"])
def generate_initial_files1(in_name, out_names):
    for on in out_names:
        with open(on, 'w') as outfile:
            pass

#___________________________________________________________________________
#
#   test_product_task
#___________________________________________________________________________
@mkdir(workdir + "/test1")
@mkdir(workdir + "/test2")
@mkdir(generate_initial_files1, formatter(),
            ["{path[0]}/{basename[0]}.dir", 3, "{path[0]}/{basename[0]}.dir2"])
@transform( generate_initial_files1,
            formatter(),
            "{path[0]}/{basename[0]}.dir/{basename[0]}.tmp2")
def test_transform( infiles, outfile):
    with open(outfile, "w") as p: pass


@mkdir(workdir + "/test3")
@mkdir(generate_initial_files1, formatter(),
            "{path[0]}/{basename[0]}.dir2")
def test_transform2():
    print("    Loose cannon!", file=sys.stderr)



def cleanup_tmpdir():
    os.system('rm -f %s %s' % (os.path.join(workdir, '*'), RUFFUS_HISTORY_FILE))


class Testmkdir(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(workdir)
        except OSError:
            pass

    #___________________________________________________________________________
    #
    #   test mkdir() pipeline_printout and pipeline_run
    #___________________________________________________________________________
    def test_mkdir_printout(self):
        """Input file exists, output doesn't exist"""
        cleanup_tmpdir()

        s = StringIO()
        pipeline_printout(s, [test_transform, test_transform2], verbose=5, wrap_width = 10000)
        #self.assertIn('Job needs update: Missing files '
        #              '[tmp_test_mkdir/a_name.tmp1, '
        #              'tmp_test_mkdir/e_name.tmp1, '
        #              'tmp_test_mkdir/h_name.tmp1, '
        #              'tmp_test_mkdir/a_name.e_name.h_name.tmp2]', s.getvalue())

    def test_mkdir_run(self):
        """Run mkdir"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        pipeline_run([test_transform, test_transform2], verbose=0, multiprocess = 2)


    def test_newstyle_mkdir_run(self):
        test_pipeline = Pipeline("test")

        test_pipeline.split(task_func = generate_initial_files1,
                            input = 1,
                            output = [workdir +  "/" + prefix + "_name.tmp1" for prefix in "abcd"])

        test_pipeline.transform( task_func = test_transform,
                                 input     = generate_initial_files1,
                                 filter    = formatter(),
                                 output    = "{path[0]}/{basename[0]}.dir/{basename[0]}.tmp2")\
            .mkdir(workdir + "/test1")\
            .mkdir(workdir + "/test2")\
            .mkdir(generate_initial_files1, formatter(),
                        ["{path[0]}/{basename[0]}.dir", 3, "{path[0]}/{basename[0]}.dir2"])

        test_pipeline.mkdir(test_transform2, workdir + "/test3")\
            .mkdir(generate_initial_files1, formatter(),
                    "{path[0]}/{basename[0]}.dir2")
        cleanup_tmpdir()
        pipeline_run([test_transform, test_transform2], verbose=0, multiprocess = 2)




    #___________________________________________________________________________
    #
    #   cleanup
    #___________________________________________________________________________
    def tearDown(self):
        shutil.rmtree(workdir)



#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    unittest.main()
