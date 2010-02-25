#!/usr/bin/env python
# make sure using local ruffus
import sys, os
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))



NUMBER_OF_RANDOMS = 10000
CHUNK_SIZE = 1000
working_dir = "temp_tutorial7/"



import time, sys, os
from ruffus import *

import random
import glob


#---------------------------------------------------------------
# 
#   make sure tasks take long enough to register as separate
#       entries in the file system
# 
def sleep_a_while ():
    time.sleep(1)


#---------------------------------------------------------------
#
#   Create random numbers
#
@posttask(sleep_a_while)
@follows(mkdir(working_dir))
@files(None, working_dir + "random_numbers.list")
def create_random_numbers(input_file_name, output_file_name):
    f = open(output_file_name, "w")
    for i in range(NUMBER_OF_RANDOMS):
        f.write("%g\n" % (random.random() * 100.0))

#---------------------------------------------------------------
#
#   Split initial file
#
@follows(create_random_numbers)
@posttask(sleep_a_while)
@split(working_dir + "random_numbers.list", working_dir + "*.chunks")
def step_4_split_numbers_into_chunks (input_file_name, output_files):
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
    for i, line in enumerate(open(input_file_name)):
        if i % CHUNK_SIZE == 0:
            cnt_files += 1
            output_file = open(working_dir + "%d.chunks" % cnt_files, "w")
        output_file.write(line)

#---------------------------------------------------------------
#
#   Calculate sum and sum of squares for each chunk file
#
@posttask(sleep_a_while)
@transform(step_4_split_numbers_into_chunks, suffix(".chunks"), ".sums")
def step_5_calculate_sum_of_squares (input_file_name, output_file_name):
    output = open(output_file_name,  "w")
    sum_squared, sum = [0.0, 0.0]
    cnt_values = 0
    for line in open(input_file_name):
        cnt_values += 1
        val = float(line.rstrip())
        sum_squared += val * val
        sum += val
    output.write("%s\n%s\n%d\n" % (repr(sum_squared), repr(sum), cnt_values))


def print_hooray_again():
    print "hooray again"

def print_whoppee_again():
    print "whoppee again"


#---------------------------------------------------------------
#
#   Calculate sum and sum of squares for each chunk
#
@posttask(lambda: sys.stdout.write("hooray\n"))
@posttask(print_hooray_again, print_whoppee_again, touch_file("done"))
@merge(step_5_calculate_sum_of_squares, "variance.result")
@posttask(sleep_a_while)
def step_6_calculate_variance (input_file_names, output_file_name):
    """
    Calculate variance naively
    """
    output = open(output_file_name,  "w")
    #
    #   initialise variables
    #
    all_sum_squared = 0.0
    all_sum         = 0.0
    all_cnt_values  = 0.0
    #
    # added up all the sum_squared, and sum and cnt_values from all the chunks
    #
    for input_file_name in input_file_names:
        sum_squared, sum, cnt_values = map(float, open(input_file_name).readlines())
        all_sum_squared += sum_squared
        all_sum         += sum
        all_cnt_values  += cnt_values
    all_mean = all_sum / all_cnt_values
    variance = (all_sum_squared - all_sum * all_mean)/(all_cnt_values)
    #
    #   print output
    #
    print >>output, variance

#---------------------------------------------------------------
#
#       Run
#
pipeline_run([step_6_calculate_variance], verbose = 1)

