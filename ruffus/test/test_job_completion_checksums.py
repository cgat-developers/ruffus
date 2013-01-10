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
                    merge, dbdict)
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
                   os.path.join(workdir, 'split.out2.txt')]
merge2_output =  os.path.join(workdir, 'merged.out')

runtime_data = []

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
            pipeline_printout(s, [transform1], verbose=5, checksum_level=chksm)
            self.assertIn('Job needs update: Missing file [tmp_test_job_completion/input.output]',
                          s.getvalue())

    def test_ouput_out_of_date(self):
        """Input file exists, output out of date"""
        # output exists but is out of date-- should run for all levels
        cleanup_tmpdir()
        with open(transform1_out, 'w') as outfile:
            outfile.write('testme')
        time.sleep(1)
        with open(input_file, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=5, checksum_level=chksm)
            self.assertIn('Job needs update:', s.getvalue())
            if chksm == CHECKSUM_FILE_TIMESTAMPS:
                self.assertIn('Input files:', s.getvalue())
                self.assertIn('Output files:', s.getvalue())
            else:
                self.assertIn('Previous incomplete run leftover', s.getvalue())

    def test_ouput_timestamp_okay(self):
        """Input file exists, output timestamp up to date"""
        # output exists and timestamp is up to date-- not run for lvl 0, run for all others
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        time.sleep(1)
        with open(transform1_out, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=5, checksum_level=chksm)
            if chksm == CHECKSUM_FILE_TIMESTAMPS:
                self.assertIn('Job up-to-date', s.getvalue())
            else:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Previous incomplete run leftover',
                              s.getvalue())

    def test_ouput_up_to_date(self):
        """Input file exists, output up to date"""
        # output is up to date-- not run for any levels
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([transform1], verbose=0)

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=5, checksum_level=chksm)
            self.assertIn('Job up-to-date', s.getvalue())

    def test_ouput_up_to_date_func_changed(self):
        """Input file exists, output up to date, function body changed"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([transform1], verbose=0)
        transform1.func_code = split1.func_code  # simulate source change

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=5, checksum_level=chksm)
            if chksm >= CHECKSUM_FUNCTIONS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Pipeline function has changed',
                              s.getvalue())
            else:
                self.assertIn('Job up-to-date', s.getvalue())

    def test_ouput_up_to_date_func_changed(self):
        """Input file exists, output up to date, function body changed"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([transform1], verbose=0)
        # simulate source change
        split1.func_code, transform1.func_code = transform1.func_code, split1.func_code

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=5, checksum_level=chksm)
            if chksm >= CHECKSUM_FUNCTIONS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Pipeline function has changed',
                              s.getvalue())
            else:
                self.assertIn('Job up-to-date', s.getvalue())
        # clean up our function-changing mess!
        split1.func_code, transform1.func_code = transform1.func_code, split1.func_code

    def test_ouput_up_to_date_param_changed(self):
        """Input file exists, output up to date, parameter to function changed"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([transform1], verbose=0)
        runtime_data.append('different')  # simulate change to config file

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=5, checksum_level=chksm)
            if chksm >= CHECKSUM_FUNCTIONS_AND_PARAMS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Pipeline parameters have changed',
                              s.getvalue())
            else:
                self.assertIn('Job up-to-date', s.getvalue())

    def test_raises_error(self):
        """run a function that fails but creates output, then check what should run"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        time.sleep(.5)
        del runtime_data[:]
        with self.assertRaises(RethrownJobError):  # poo. Shouldn't this be RuntimeError?
            pipeline_run([transform_raise_error], verbose=0) # generates output then fails

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform_raise_error], verbose=5, checksum_level=chksm)
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Previous incomplete run leftover',
                              s.getvalue())
            else:
                self.assertIn('Job up-to-date', s.getvalue())

    def test_split_output(self):
        """test multiple-output checksums"""
        # outputs out of date
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([split1], verbose=0)
        time.sleep(.5)
        with open(input_file, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [split1], verbose=5, checksum_level=chksm)
            self.assertIn('Job needs update:', s.getvalue())

        # all outputs incorrectly generated
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        time.sleep(.5)
        for f in split1_outputs:
            with open(f, 'w') as outfile:
                outfile.write('testme')
        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [split1], verbose=5, checksum_level=chksm)
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Previous incomplete run leftover',
                              s.getvalue())
            else:
                self.assertIn('Job up-to-date', s.getvalue())

        # one output incorrectly generated
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([split1], verbose=0)
        job_history = dbdict.open(RUFFUS_HISTORY_FILE, picklevalues=True)
        del job_history[split1_outputs[0]]

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [split1], verbose=5, checksum_level=chksm)
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Previous incomplete run leftover',
                              s.getvalue())
            else:
                self.assertIn('Job up-to-date', s.getvalue())

    def test_merge_output(self):
        """test multiple-input checksums"""
        # one output incorrectly generated
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([split1], verbose=0)
        job_history = dbdict.open(RUFFUS_HISTORY_FILE, picklevalues=True)
        del job_history[split1_outputs[0]]

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [merge2], verbose=5, checksum_level=chksm)
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Previous incomplete run leftover', s.getvalue())
            else:
                self.assertIn('Job up-to-date', s.getvalue())

        # make sure the jobs run fine
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([merge2], verbose=0)
        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [merge2], verbose=5, checksum_level=chksm)
            self.assertIn('Job up-to-date', s.getvalue())
            self.assertNotIn('Job needs update:', s.getvalue())
            self.assertNotIn('Previous incomplete run leftover', s.getvalue())


    def tearDown(self):
        shutil.rmtree(workdir)

#if __name__ == '__main__':
#        try:
#            os.mkdir(workdir)
#        except OSError:
#            pass
#        #os.system('rm %s/*' % workdir)
#        #open(input_file, 'w').close()
#        s = StringIO()
#        pipeline_run([transform1])
#        pipeline_printout(s, [transform1], verbose=5, checksum_level=0)
#        print s.getvalue()
#        #open(transform1_out)  # raise an exception if test fails
