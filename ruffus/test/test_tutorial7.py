#!/usr/bin/env python
from __future__ import print_function
import shutil
import unittest
import glob
import random
from ruffus import follows, split, mkdir, files, transform, suffix, posttask, touch_file, merge, Pipeline
import sys
import os



NUMBER_OF_RANDOMS = 10000
CHUNK_SIZE = 1000


tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0])) + "/"

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# ---------------------------------------------------------------
#
#   Create random numbers
#
@follows(mkdir(tempdir))
@files(None, tempdir + "random_numbers.list")
def create_random_numbers(input_file_name, output_file_name):
    f = open(output_file_name, "w")
    for i in range(NUMBER_OF_RANDOMS):
        f.write("%g\n" % (random.random() * 100.0))
    f.close()

# ---------------------------------------------------------------
#
#   Split initial file
#


@follows(create_random_numbers)
@split(tempdir + "random_numbers.list", tempdir + "*.chunks")
def step_4_split_numbers_into_chunks(input_file_name, output_files):
    """
        Splits random numbers file into XXX files of CHUNK_SIZE each
    """
    #
    #   clean up files from previous runs
    #
    for f in glob.glob("*.chunks"):
        os.unlink(f)
    #
    #   create new file every CHUNK_SIZE lines and
    #       copy each line into current file
    #
    output_file = None
    cnt_files = 0
    with open(input_file_name) as ii:
        for i, line in enumerate(ii):
            if i % CHUNK_SIZE == 0:
                cnt_files += 1
                if output_file:
                    output_file.close()
                output_file = open(tempdir + "%d.chunks" % cnt_files, "w")
            output_file.write(line)
    if output_file:
        output_file.close()

# ---------------------------------------------------------------
#
#   Calculate sum and sum of squares for each chunk file
#


@transform(step_4_split_numbers_into_chunks, suffix(".chunks"), ".sums")
def step_5_calculate_sum_of_squares(input_file_name, output_file_name):
    with open(output_file_name,  "w") as oo:
        sum_squared, sum = [0.0, 0.0]
        cnt_values = 0
        with open(input_file_name) as ii:
            for line in ii:
                cnt_values += 1
                val = float(line.rstrip())
                sum_squared += val * val
                sum += val
        oo.write("%s\n%s\n%d\n" % (repr(sum_squared), repr(sum), cnt_values))


def print_hooray_again():
    print("     hooray again")


def print_whoppee_again():
    print("     whoppee again")


# ---------------------------------------------------------------
#
#   Calculate sum and sum of squares for each chunk
#
@posttask(lambda: sys.stdout.write("     hooray\n"))
@posttask(print_hooray_again, print_whoppee_again, touch_file(os.path.join(tempdir, "done")))
@merge(step_5_calculate_sum_of_squares, os.path.join(tempdir, "variance.result"))
def step_6_calculate_variance(input_file_names, output_file_name):
    """
    Calculate variance naively
    """
    output = open(output_file_name,  "w")
    #
    #   initialise variables
    #
    all_sum_squared = 0.0
    all_sum = 0.0
    all_cnt_values = 0.0
    #
    # added up all the sum_squared, and sum and cnt_values from all the chunks
    #
    for input_file_name in input_file_names:
        with open(input_file_name) as ii:
            sum_squared, sum, cnt_values = list(map(float, ii.readlines()))
        all_sum_squared += sum_squared
        all_sum += sum
        all_cnt_values += cnt_values
    all_mean = all_sum / all_cnt_values
    variance = (all_sum_squared - all_sum * all_mean)/(all_cnt_values)
    #
    #   print output
    #
    print(variance, file=output)
    output.close()


try:
    from StringIO import StringIO
except:
    from io import StringIO


class Test_ruffus(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
            pass
        except:
            pass

    def atest_ruffus(self):
        pipeline_run(multiprocess=50, verbose=0, pipeline="main")
        output_file = os.path.join(tempdir, "variance.result")
        if not os.path.exists(output_file):
            raise Exception("Missing %s" % output_file)

    def test_newstyle_ruffus(self):
        test_pipeline = Pipeline("test")

        test_pipeline.files(create_random_numbers, None, tempdir + "random_numbers.list")\
            .follows(mkdir(tempdir))

        test_pipeline.split(task_func=step_4_split_numbers_into_chunks,
                            input=tempdir + "random_numbers.list",
                            output=tempdir + "*.chunks")\
            .follows(create_random_numbers)

        test_pipeline.transform(task_func=step_5_calculate_sum_of_squares,
                                input=step_4_split_numbers_into_chunks,
                                filter=suffix(".chunks"),
                                output=".sums")

        test_pipeline.merge(task_func=step_6_calculate_variance, input=step_5_calculate_sum_of_squares, output=os.path.join(tempdir, "variance.result"))\
            .posttask(lambda: sys.stdout.write("     hooray\n"))\
            .posttask(print_hooray_again, print_whoppee_again, touch_file(os.path.join(tempdir, "done")))

        test_pipeline.run(multiprocess=50, verbose=0)
        output_file = os.path.join(tempdir, "variance.result")
        if not os.path.exists(output_file):
            raise Exception("Missing %s" % output_file)


if __name__ == '__main__':
    unittest.main()
