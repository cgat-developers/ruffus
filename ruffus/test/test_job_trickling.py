#!/usr/bin/env python
"""

    test_job_trickling.py

        test if the jobs are trickling to their child tasks

"""


import unittest
import os
import sys
import shutil
from StringIO import StringIO
import time
import glob
from multiprocessing.pool import ThreadPool

exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import (pipeline_run, pipeline_printout, suffix, transform, split,
                    merge, dbdict, mkdir, follows)
from ruffus.ruffus_utility import RUFFUS_HISTORY_FILE
from ruffus.ruffus_exceptions import RethrownJobError

workdir = 'tmp_test_job_trickling/'
input_file = os.path.join(workdir, 'input.txt')
split1_outputs = [os.path.join(workdir, 'split.%s.txt' % i) for i in range(5)]
transform2_outputs = [f.replace('.txt', '.output1') for f in split1_outputs]
transform3_outputs = [f.replace('.output1', '.output2') for f in transform2_outputs]
merge4_output =  os.path.join(workdir, 'merged.out')

@split(input_file, split1_outputs)
def split1(in_name, out_names):
    for n in out_names:
        with open(n, 'w') as outfile:
            outfile.write(open(in_name).read() + '\n')

@transform(split1, suffix('.txt'), '.output1')
def transform2_variable_wait(in_name, out_name):
    if 'split.0.txt' in in_name:
        print 'waiting'
        time.sleep(5)  # simulate a long-running job
    with open(out_name, 'w') as outfile:
        outfile.write(open(in_name).read())

@transform(transform2_variable_wait, suffix('.output1'), '.output2')
def transform3(in_name, out_name):
    with open(out_name, 'w') as outfile:
        outfile.write(open(in_name).read())

@merge(transform3, merge4_output)
def merge4(in_names, out_name):
    with open(out_name, 'w') as outfile:
        for n in in_names:
            outfile.write(open(n).read() + '\n')

def cleanup_tmpdir():
    os.system('rm -f %s %s' % (os.path.join(workdir, '*'), RUFFUS_HISTORY_FILE))


class TestJobCompletion(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(workdir)
        except OSError:
            pass
        
    def test_fast_jobs_done(self):
        """Validate that fast outputs are available before the slow outputs"""
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        
        def step2_output_when_step1_was_running():
            """assert that there was a time when step 3 was running, but step 2 hadn't finished"""
            found = False
            for i in range(15):
                time.sleep(1)
                num_step2 = sum(map(os.path.exists, transform2_outputs))
                num_step3 = sum(map(os.path.exists, transform3_outputs))
                #print 'found %s step2 and %s step3'% (num_step2, num_step3)
                if num_step3 > 0 and num_step2 < len(transform2_outputs):
                    return True
            return found
        
        p = ThreadPool(processes=1)
        r = p.apply_async(step2_output_when_step1_was_running)
        pipeline_run([merge4], verbose=10, multiprocess=len(transform2_outputs))
        self.assertTrue(r.get())

    def tearDown(self):
        cleanup_tmpdir()
        shutil.rmtree(workdir)
