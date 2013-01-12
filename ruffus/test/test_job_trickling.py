#!/usr/bin/env python
"""

    test_job_completion_transform.py

        test several cases where the dbdict should be updated

"""


import unittest
import os
import sys
import shutil
from StringIO import StringIO
import time

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import (pipeline_run, pipeline_printout, suffix, transform, split,
                    merge, dbdict, mkdir, follows)
from ruffus.ruffus_utility import (RUFFUS_HISTORY_FILE,
                                   CHECKSUM_FILE_TIMESTAMPS,
                                   CHECKSUM_HISTORY_TIMESTAMPS,
                                   CHECKSUM_FUNCTIONS,
                                   CHECKSUM_FUNCTIONS_AND_PARAMS)
from ruffus.ruffus_exceptions import RethrownJobError

possible_chksms = range(CHECKSUM_FUNCTIONS_AND_PARAMS + 1)
workdir = 'tmp_test_job_completion/'
input_file = os.path.join(workdir, 'input.txt')
transform1_out = input_file.replace('.txt', '.output')
split1_outputs = [ os.path.join(workdir, 'split.out1.txt'),
                   os.path.join(workdir, 'split.out2.txt'),
                   os.path.join(workdir, 'split.other.file.*.txt')]
merge2_output =  os.path.join(workdir, 'merged.out')

runtime_data = []

#@follows(mkdir(workdir + '/test'))
@transform(input_file, suffix('.txt'), '.output', runtime_data)
def transform1(in_name, out_name, how_many):
    with open(out_name, 'w') as outfile:
        outfile.write(open(in_name).read())

@transform(input_file, suffix('.txt'), '.output', runtime_data)
def transform_raise_error(in_name, out_name, how_many):
    # raise an error unless runtime_data has 'okay' in it
    with open(out_name, 'w') as outfile:
        outfile.write(open(in_name).read())
    if 'okay' not in runtime_data:
        raise RuntimeError("'okay' wasn't in runtime_data!")

@split(input_file, split1_outputs)
def split1(in_name, out_names):
    for n in out_names:
        if '*' in n:
            n = n.replace('*', 'number1')
        with open(n, 'w') as outfile:
            outfile.write(open(in_name).read() + '\n')

@merge(split1, merge2_output)
def merge2(in_names, out_name):
    with open(out_name, 'w') as outfile:
        for n in in_names:
            outfile.write(open(n).read() + '\n')


#CHECKSUM_FILE_TIMESTAMPS      = 0     # only rerun when the file timestamps are out of date (classic mode)
#CHECKSUM_HISTORY_TIMESTAMPS   = 1     # also rerun when the history shows a job as being out of date
#CHECKSUM_FUNCTIONS            = 2     # also rerun when function body has changed
#CHECKSUM_FUNCTIONS_AND_PARAMS = 3     # also rerun when function parameters have changed


def cleanup_tmpdir():
    os.system('rm -f %s %s' % (os.path.join(workdir, '*'), RUFFUS_HISTORY_FILE))


class TestJobCompletion(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(workdir)
        except OSError:
            pass

    def test_ouput_doesnt_exist(self):
        """Input file exists, output doesn't exist"""
        # output doesn't exist-- should run for all levels
        # create a new input file
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=10, checksum_level=chksm)
            self.assertIn('Job needs update: Missing file [tmp_test_job_completion/input.output]',
                          s.getvalue())



    def tearDown(self):
        shutil.rmtree(workdir)

if __name__ == '__main__':
    try:
        os.mkdir(workdir)
    except OSError:
        pass
    os.system('rm %s/*' % workdir)
    with open(input_file, 'w') as outfile:
        outfile.write('this is a test\n')
    s = StringIO()
    pipeline_run([transform1, merge2], verbose=100)
    #pipeline_printout(s, [transform1], verbose=100, checksum_level=0)
    print s.getvalue()
    #open(transform1_out)  # raise an exception if test fails
