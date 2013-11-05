.. include:: ../../global.inc
.. _Simple_Tutorial_8th_step_code:

#########################################################################
Code for Step 8: Signal the completion of each stage of our pipeline
#########################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`@posttask in detail <decorators.posttask>`
* :ref:`back to step 8 <Simple_Tutorial_8th_step>`

************************************
Code
************************************
    ::
    
        NUMBER_OF_RANDOMS = 10000
        CHUNK_SIZE = 1000
        working_dir = "temp_tutorial8/"
        
        
        
        import time, sys, os
        from ruffus import *
        
        import random
        import glob
        
        
        
        
        #---------------------------------------------------------------
        #
        #   Create random numbers
        #
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
        @split(working_dir + "random_numbers.list", working_dir + "*.chunks")
        def step_5_split_numbers_into_chunks (input_file_name, output_files):
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
        @transform(step_5_split_numbers_into_chunks, suffix(".chunks"), ".sums")
        def step_6_calculate_sum_of_squares (input_file_name, output_file_name):
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
        @merge(step_6_calculate_sum_of_squares, "variance.result")
        def step_7_calculate_variance (input_file_names, output_file_name):
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
        pipeline_run([step_7_calculate_variance], verbose = 1)

        

************************************
Resulting Output
************************************
    ::

        >> pipeline_run([step_7_calculate_variance], verbose = 1)
            Make directories [temp_tutorial8/] completed
        Completed Task = create_random_numbers_mkdir_1
            Job = [None -> temp_tutorial8/random_numbers.list] completed
        Completed Task = create_random_numbers
            Job = [temp_tutorial8/random_numbers.list -> temp_tutorial8/*.chunks] completed
        Completed Task = step_5_split_numbers_into_chunks
            Job = [temp_tutorial8/1.chunks -> temp_tutorial8/1.sums] completed
            Job = [temp_tutorial8/10.chunks -> temp_tutorial8/10.sums] completed
            Job = [temp_tutorial8/2.chunks -> temp_tutorial8/2.sums] completed
            Job = [temp_tutorial8/3.chunks -> temp_tutorial8/3.sums] completed
            Job = [temp_tutorial8/4.chunks -> temp_tutorial8/4.sums] completed
            Job = [temp_tutorial8/5.chunks -> temp_tutorial8/5.sums] completed
            Job = [temp_tutorial8/6.chunks -> temp_tutorial8/6.sums] completed
            Job = [temp_tutorial8/7.chunks -> temp_tutorial8/7.sums] completed
            Job = [temp_tutorial8/8.chunks -> temp_tutorial8/8.sums] completed
            Job = [temp_tutorial8/9.chunks -> temp_tutorial8/9.sums] completed
        Completed Task = step_6_calculate_sum_of_squares
            Job = [[temp_tutorial8/1.sums, temp_tutorial8/10.sums, temp_tutorial8/2.sums, temp_tutorial8/3.sums, temp_tutorial8/4.sums, temp_tutorial8/5.sums, temp_tutorial8/6.sums, temp_tutorial8/7.sums, temp_tutorial8/8.sums, temp_tutorial8/9.sums] -> variance.result] completed
        hooray again
        whoppee again
        hooray
        Completed Task = step_7_calculate_variance
        
