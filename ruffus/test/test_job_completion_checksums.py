#!/usr/bin/env python
from __future__ import print_function
import re
import time
import shutil
import unittest
from ruffus.ruffus_exceptions import RethrownJobError
from ruffus.ruffus_utility import RUFFUS_HISTORY_FILE, CHECKSUM_FILE_TIMESTAMPS, \
    CHECKSUM_HISTORY_TIMESTAMPS, CHECKSUM_FUNCTIONS, CHECKSUM_FUNCTIONS_AND_PARAMS
from ruffus.ruffus_utility import get_default_history_file_name
from ruffus import pipeline_run, pipeline_printout, suffix, transform, split, merge, dbdict, Pipeline
import sys

"""

    test_job_completion_transform.py

        test several cases where the dbdict should be updated

"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# ___________________________________________________________________________
#
#   imports
# ___________________________________________________________________________


try:
    from StringIO import StringIO
except:
    from io import StringIO


possible_chksms = list(range(CHECKSUM_FUNCTIONS_AND_PARAMS + 1))
tempdir = 'tmp_test_job_completion/'
input_file = os.path.join(tempdir, 'input.txt')
transform1_out = input_file.replace('.txt', '.output')
split1_outputs = [os.path.join(tempdir, 'split.out1.txt'),
                  os.path.join(tempdir, 'split.out2.txt')]
merge2_output = os.path.join(tempdir, 'merged.out')

runtime_data = []


@transform(input_file, suffix('.txt'), '.output', runtime_data)
def transform1(in_name, out_name, how_many):
    with open(out_name, 'w') as outfile:
        with open(in_name) as ii:
            outfile.write(ii.read())


@transform(input_file, suffix('.txt'), '.output', runtime_data)
def transform_raise_error(in_name, out_name, how_many):
    # raise an error unless runtime_data has 'okay' in it
    with open(out_name, 'w') as outfile:
        with open(in_name) as ii:
            outfile.write(ii.read())
    if 'okay' not in how_many:
        raise RuntimeError("'okay' wasn't in runtime_data!")


@split(input_file, split1_outputs)
def split1(in_name, out_names):
    for n in out_names:
        with open(n, 'w') as outfile:
            with open(in_name) as ii:
                outfile.write(ii.read() + '\n')


@merge(split1, merge2_output)
def merge2(in_names, out_name):
    with open(out_name, 'w') as outfile:
        for n in in_names:
            with open(n) as ii:
                outfile.write(ii.read() + '\n')


# CHECKSUM_FILE_TIMESTAMPS      = 0     # only rerun when the file timestamps are out of date (classic mode)
# CHECKSUM_HISTORY_TIMESTAMPS   = 1     # also rerun when the history shows a job as being out of date
# CHECKSUM_FUNCTIONS            = 2     # also rerun when function body has changed
# CHECKSUM_FUNCTIONS_AND_PARAMS = 3     # also rerun when function parameters have changed


def cleanup_tmpdir():
    os.system('rm -f %s %s' %
              (os.path.join(tempdir, '*'), get_default_history_file_name()))


count_pipelines = 0


class TestJobCompletion(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(tempdir)
        except OSError:
            pass

    def create_pipeline(self):
        """
        Create new pipeline on the fly without using decorators
        """
        global count_pipelines
        count_pipelines = count_pipelines + 1
        test_pipeline = Pipeline("test %d" % count_pipelines)

        test_pipeline.transform(task_func=transform1,
                                input=input_file,
                                filter=suffix('.txt'),
                                output='.output',
                                extras=[runtime_data])

        test_pipeline.transform(task_func=transform_raise_error,
                                input=input_file,
                                filter=suffix('.txt'),
                                output='.output',
                                extras=[runtime_data])

        test_pipeline.split(task_func=split1,
                            input=input_file,
                            output=split1_outputs)

        test_pipeline.merge(task_func=merge2,
                            input=split1,
                            output=merge2_output)
        return test_pipeline

    def test_output_doesnt_exist(self):
        """Input file exists, output doesn't exist"""
        # output doesn't exist-- should run for all levels
        # create a new input file
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=6,
                              checksum_level=chksm, pipeline="main")
            self.assertTrue(re.search(
                r'Job needs update:.*Missing file.*\[tmp_test_job_completion/input.output\]', s.getvalue(), re.DOTALL))

    def test_output_out_of_date(self):
        """Input file exists, output out of date"""
        # output exists but is out of date-- should run for all levels
        cleanup_tmpdir()
        with open(transform1_out, 'w') as outfile:
            outfile.write('testme')
        time.sleep(0.1)
        with open(input_file, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=6,
                              checksum_level=chksm, pipeline="main")
            self.assertIn('Job needs update:', s.getvalue())
            if chksm == CHECKSUM_FILE_TIMESTAMPS:
                self.assertIn('Input files:', s.getvalue())
                self.assertIn('Output files:', s.getvalue())
            else:
                self.assertIn('left over from a failed run?', s.getvalue())

    def test_output_timestamp_okay(self):
        """Input file exists, output timestamp up to date"""
        # output exists and timestamp is up to date-- not run for lvl 0, run for all others
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        time.sleep(0.1)
        with open(transform1_out, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=6,
                              checksum_level=chksm, pipeline="main")
            if chksm == CHECKSUM_FILE_TIMESTAMPS:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass
            else:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('left over from a failed run?',
                              s.getvalue())

    def test_output_up_to_date(self):
        """Input file exists, output up to date"""
        # output is up to date-- not run for any levels
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([transform1], verbose=0,
                     checksum_level=CHECKSUM_HISTORY_TIMESTAMPS, pipeline="main")

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=6,
                              checksum_level=chksm, pipeline="main")
            #self.assertIn('Job up-to-date', s.getvalue())
            pass

    def test_output_up_to_date_func_changed(self):
        """Input file exists, output up to date, function body changed"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([transform1], verbose=0,
                     checksum_level=CHECKSUM_HISTORY_TIMESTAMPS, pipeline="main")
        if sys.hexversion >= 0x03000000:
            transform1.__code__ = split1.__code__  # simulate source change
        else:
            transform1.func_code = split1.func_code  # simulate source change

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=6,
                              checksum_level=chksm, pipeline="main")
            if chksm >= CHECKSUM_FUNCTIONS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Pipeline function has changed',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

    def test_output_up_to_date_func_changed(self):
        """Input file exists, output up to date, function body changed"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([transform1], verbose=0,
                     checksum_level=CHECKSUM_HISTORY_TIMESTAMPS, pipeline="main")
        # simulate source change
        if sys.hexversion >= 0x03000000:
            split1.__code__, transform1.__code__ = transform1.__code__, split1.__code__
        else:
            split1.func_code, transform1.func_code = transform1.func_code, split1.func_code

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=6,
                              checksum_level=chksm, pipeline="main")
            if chksm >= CHECKSUM_FUNCTIONS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Pipeline function has changed',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass
        # clean up our function-changing mess!
        if sys.hexversion >= 0x03000000:
            split1.__code__, transform1.__code__ = transform1.__code__, split1.__code__
        else:
            split1.func_code, transform1.func_code = transform1.func_code, split1.func_code

    def test_output_up_to_date_param_changed(self):
        """Input file exists, output up to date, parameter to function changed"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([transform1], verbose=0,
                     checksum_level=CHECKSUM_HISTORY_TIMESTAMPS, pipeline="main")
        runtime_data.append('different')  # simulate change to config file

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform1], verbose=6,
                              checksum_level=chksm, pipeline="main")
            if chksm >= CHECKSUM_FUNCTIONS_AND_PARAMS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Pipeline parameters have changed',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

    def test_split_output(self):
        """test multiple-output checksums"""
        # outputs out of date
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([split1], verbose=0,
                     checksum_level=CHECKSUM_HISTORY_TIMESTAMPS, pipeline="main")
        time.sleep(.5)
        with open(input_file, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [split1], verbose=6,
                              checksum_level=chksm, pipeline="main")
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
            pipeline_printout(s, [split1], verbose=6,
                              checksum_level=chksm, pipeline="main")
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('left over from a failed run?',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

        # one output incorrectly generated
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([split1], verbose=0,
                     checksum_level=CHECKSUM_HISTORY_TIMESTAMPS, pipeline="main")
        job_history = dbdict.open(
            get_default_history_file_name(), picklevalues=True)
        del job_history[os.path.relpath(split1_outputs[0])]

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [split1], verbose=6,
                              checksum_level=chksm, pipeline="main")
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('left over from a failed run?',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

    def test_merge_output(self):
        """test multiple-input checksums"""
        # one output incorrectly generated
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([split1], verbose=0,
                     checksum_level=CHECKSUM_HISTORY_TIMESTAMPS, pipeline="main")
        job_history = dbdict.open(
            get_default_history_file_name(), picklevalues=True)
        del job_history[os.path.relpath(split1_outputs[0])]

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [merge2], verbose=6,
                              checksum_level=chksm, pipeline="main")
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('left over from a failed run?', s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

        # make sure the jobs run fine
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        pipeline_run([merge2], verbose=0,
                     checksum_level=CHECKSUM_HISTORY_TIMESTAMPS, pipeline="main")
        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [merge2], verbose=6,
                              checksum_level=chksm, pipeline="main")
            #self.assertIn('Job up-to-date', s.getvalue())
            self.assertNotIn('Job needs update:', s.getvalue())
            self.assertNotIn('left over from a failed run?', s.getvalue())

    def test_newstyle_output_doesnt_exist(self):
        """Input file exists, output doesn't exist"""
        # output doesn't exist-- should run for all levels
        # create a new input file
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            self.create_pipeline().printout(
                s, [transform1], verbose=6, checksum_level=chksm)
            self.assertTrue(re.search(
                r'Job needs update:.*Missing file.*\[tmp_test_job_completion/input.output\]', s.getvalue(), re.DOTALL))

    def test_newstyle_output_out_of_date(self):
        """Input file exists, output out of date"""
        # output exists but is out of date-- should run for all levels
        cleanup_tmpdir()
        with open(transform1_out, 'w') as outfile:
            outfile.write('testme')
        time.sleep(0.1)
        with open(input_file, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            self.create_pipeline().printout(
                s, [transform1], verbose=6, checksum_level=chksm)
            self.assertIn('Job needs update:', s.getvalue())
            if chksm == CHECKSUM_FILE_TIMESTAMPS:
                self.assertIn('Input files:', s.getvalue())
                self.assertIn('Output files:', s.getvalue())
            else:
                self.assertIn('left over from a failed run?', s.getvalue())

    def test_newstyle_output_timestamp_okay(self):
        """Input file exists, output timestamp up to date"""
        # output exists and timestamp is up to date-- not run for lvl 0, run for all others
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        time.sleep(0.1)
        with open(transform1_out, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            self.create_pipeline().printout(
                s, [transform1], verbose=6, checksum_level=chksm)
            if chksm == CHECKSUM_FILE_TIMESTAMPS:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass
            else:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('left over from a failed run?',
                              s.getvalue())

    def test_newstyle_output_up_to_date(self):
        """Input file exists, output up to date"""
        test_pipeline = self.create_pipeline()
        # output is up to date-- not run for any levels
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        test_pipeline.run([transform1], verbose=0,
                          checksum_level=CHECKSUM_HISTORY_TIMESTAMPS)

        for chksm in possible_chksms:
            s = StringIO()
            test_pipeline.printout(
                s, [transform1], verbose=6, checksum_level=chksm)
            #self.assertIn('Job up-to-date', s.getvalue())
            pass

    def test_newstyle_output_up_to_date_func_changed(self):
        """Input file exists, output up to date, function body changed"""
        test_pipeline = self.create_pipeline()
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        test_pipeline.run([transform1], verbose=0,
                          checksum_level=CHECKSUM_HISTORY_TIMESTAMPS)
        if sys.hexversion >= 0x03000000:
            transform1.__code__ = split1.__code__  # simulate source change
        else:
            transform1.func_code = split1.func_code  # simulate source change

        for chksm in possible_chksms:
            s = StringIO()
            test_pipeline.printout(
                s, [transform1], verbose=6, checksum_level=chksm)
            if chksm >= CHECKSUM_FUNCTIONS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Pipeline function has changed',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

    def test_newstyle_output_up_to_date_func_changed(self):
        """Input file exists, output up to date, function body changed"""
        test_pipeline = self.create_pipeline()
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        test_pipeline.run([transform1], verbose=0,
                          checksum_level=CHECKSUM_HISTORY_TIMESTAMPS)
        # simulate source change
        if sys.hexversion >= 0x03000000:
            split1.__code__, transform1.__code__ = transform1.__code__, split1.__code__
        else:
            split1.func_code, transform1.func_code = transform1.func_code, split1.func_code

        for chksm in possible_chksms:
            s = StringIO()
            test_pipeline.printout(
                s, [transform1], verbose=6, checksum_level=chksm)
            if chksm >= CHECKSUM_FUNCTIONS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Pipeline function has changed',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass
        # clean up our function-changing mess!
        if sys.hexversion >= 0x03000000:
            split1.__code__, transform1.__code__ = transform1.__code__, split1.__code__
        else:
            split1.func_code, transform1.func_code = transform1.func_code, split1.func_code

    def test_newstyle_output_up_to_date_param_changed(self):
        """Input file exists, output up to date, parameter to function changed"""
        test_pipeline = self.create_pipeline()
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        test_pipeline.run([transform1], verbose=0,
                          checksum_level=CHECKSUM_HISTORY_TIMESTAMPS)
        runtime_data.append('different')  # simulate change to config file

        for chksm in possible_chksms:
            s = StringIO()
            test_pipeline.printout(
                s, [transform1], verbose=6, checksum_level=chksm)
            if chksm >= CHECKSUM_FUNCTIONS_AND_PARAMS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('Pipeline parameters have changed',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

    def test_raises_error(self):
        """run a function that fails but creates output, then check what should run"""
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        time.sleep(.5)
        del runtime_data[:]
        # poo. Shouldn't this be RuntimeError?
        with self.assertRaises(RethrownJobError):
            # generates output then fails
            pipeline_run([transform_raise_error], verbose=0,
                         checksum_level=CHECKSUM_HISTORY_TIMESTAMPS, pipeline="main")

        for chksm in possible_chksms:
            s = StringIO()
            pipeline_printout(s, [transform_raise_error],
                              verbose=6, checksum_level=chksm, pipeline="main")
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('left over from a failed run?',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

    def test_newstyle_raises_error(self):
        """run a function that fails but creates output, then check what should run"""
        test_pipeline = self.create_pipeline()
        # output is up to date, but function body changed (e.g., source different)
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        time.sleep(.5)
        del runtime_data[:]
        # poo. Shouldn't this be RuntimeError?
        with self.assertRaises(RethrownJobError):
            # generates output then fails
            test_pipeline.run([transform_raise_error], verbose=0,
                              checksum_level=CHECKSUM_HISTORY_TIMESTAMPS)
        for chksm in possible_chksms:
            s = StringIO()
            test_pipeline.printout(
                s, [transform_raise_error], verbose=6, checksum_level=chksm)
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('left over from a failed run?',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

    def test_newstyle_split_output(self):
        """test multiple-output checksums"""
        test_pipeline = self.create_pipeline()
        # outputs out of date
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        test_pipeline.run([split1], verbose=0,
                          checksum_level=CHECKSUM_HISTORY_TIMESTAMPS)
        time.sleep(.5)
        with open(input_file, 'w') as outfile:
            outfile.write('testme')

        for chksm in possible_chksms:
            s = StringIO()
            test_pipeline.printout(
                s, [split1], verbose=6, checksum_level=chksm)
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
            test_pipeline.printout(
                s, [split1], verbose=6, checksum_level=chksm)
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('left over from a failed run?',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

        # one output incorrectly generated
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        test_pipeline.run([split1], verbose=0,
                          checksum_level=CHECKSUM_HISTORY_TIMESTAMPS)
        job_history = dbdict.open(
            get_default_history_file_name(), picklevalues=True)
        del job_history[os.path.relpath(split1_outputs[0])]

        for chksm in possible_chksms:
            s = StringIO()
            test_pipeline.printout(
                s, [split1], verbose=6, checksum_level=chksm)
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('left over from a failed run?',
                              s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

    def test_newstyle_merge_output(self):
        """test multiple-input checksums"""
        test_pipeline = self.create_pipeline()
        # one output incorrectly generated
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        test_pipeline.run([split1], verbose=0,
                          checksum_level=CHECKSUM_HISTORY_TIMESTAMPS)
        job_history = dbdict.open(
            get_default_history_file_name(), picklevalues=True)
        del job_history[os.path.relpath(split1_outputs[0])]

        for chksm in possible_chksms:
            s = StringIO()
            test_pipeline.printout(
                s, [merge2], verbose=6, checksum_level=chksm)
            if chksm >= CHECKSUM_HISTORY_TIMESTAMPS:
                self.assertIn('Job needs update:', s.getvalue())
                self.assertIn('left over from a failed run?', s.getvalue())
            else:
                #self.assertIn('Job up-to-date', s.getvalue())
                pass

        # make sure the jobs run fine
        cleanup_tmpdir()
        with open(input_file, 'w') as outfile:
            outfile.write('testme')
        test_pipeline.run([merge2], verbose=0,
                          checksum_level=CHECKSUM_HISTORY_TIMESTAMPS)
        for chksm in possible_chksms:
            s = StringIO()
            test_pipeline.printout(
                s, [merge2], verbose=6, checksum_level=chksm)
            #self.assertIn('Job up-to-date', s.getvalue())
            self.assertNotIn('Job needs update:', s.getvalue())
            self.assertNotIn('left over from a failed run?', s.getvalue())

    def tearDown(self):
        shutil.rmtree(tempdir)
        pass


if __name__ == '__main__':
    unittest.main()

#        try:
#            os.mkdir(tempdir)
#        except OSError:
#            pass
#        #os.system('rm %s/*' % tempdir)
#        #open(input_file, 'w').close()
#        s = StringIO()
#        pipeline_run([transform1], checksum_level=CHECKSUM_HISTORY_TIMESTAMPS, pipeline= "main")
#        pipeline_printout(s, [transform1], verbose=6, checksum_level=0, pipeline= "main")
#        print s.getvalue()
#        #open(transform1_out)  # raise an exception if test fails
