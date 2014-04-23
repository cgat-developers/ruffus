.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.split.code:

##############################################################################################################
|new_manual.split.chapter_num|: Python Code for Splitting up large tasks / files with **@split**
##############################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`@split syntax in detail <decorators.split>`
    * Back to |new_manual.split.chapter_num|: :ref:`Splitting up large tasks / files with @split <new_manual.split>`

*******************************************
Splitting large jobs
*******************************************

        ::

            from ruffus import *

            NUMBER_OF_RANDOMS = 10000
            CHUNK_SIZE = 1000


            import random, os, glob

            #---------------------------------------------------------------
            #
            #   Create random numbers
            #
            @originate("random_numbers.list")
            def create_random_numbers(output_file_name):
                f = open(output_file_name, "w")
                for i in range(NUMBER_OF_RANDOMS):
                    f.write("%g\n" % (random.random() * 100.0))

            #---------------------------------------------------------------
            #
            #   split initial file
            #
            @split(create_random_numbers, "*.chunks")
            def split_problem (input_file_names, output_files):
                """
                    splits random numbers file into xxx files of chunk_size each
                """
                #
                #   clean up any files from previous runs
                #
                #for ff in glob.glob("*.chunks"):
                for ff in input_file_names:
                    os.unlink(ff)
                #
                #
                #   create new file every chunk_size lines and
                #       copy each line into current file
                #
                output_file = None
                cnt_files = 0
                for input_file_name in input_file_names:
                    for i, line in enumerate(open(input_file_name)):
                        if i % CHUNK_SIZE == 0:
                            cnt_files += 1
                            output_file = open("%d.chunks" % cnt_files, "w")
                        output_file.write(line)

            #---------------------------------------------------------------
            #
            #   Calculate sum and sum of squares for each chunk file
            #
            @transform(split_problem, suffix(".chunks"), ".sums")
            def sum_of_squares (input_file_name, output_file_name):
                output = open(output_file_name,  "w")
                sum_squared, sum = [0.0, 0.0]
                cnt_values = 0
                for line in open(input_file_name):
                    cnt_values += 1
                    val = float(line.rstrip())
                    sum_squared += val * val
                    sum += val
                output.write("%s\n%s\n%d\n" % (repr(sum_squared), repr(sum), cnt_values))

            #---------------------------------------------------------------
            #
            #       Run
            #
            pipeline_run()




************************************
Resulting Output
************************************
    ::

            >>> pipeline_run()
                Job  = [None -> random_numbers.list] completed
            Completed Task = create_random_numbers
                Job  = [[random_numbers.list] -> *.chunks] completed
            Completed Task = split_problem
                Job  = [1.chunks -> 1.sums] completed
                Job  = [10.chunks -> 10.sums] completed
                Job  = [2.chunks -> 2.sums] completed
                Job  = [3.chunks -> 3.sums] completed
                Job  = [4.chunks -> 4.sums] completed
                Job  = [5.chunks -> 5.sums] completed
                Job  = [6.chunks -> 6.sums] completed
                Job  = [7.chunks -> 7.sums] completed
                Job  = [8.chunks -> 8.sums] completed
                Job  = [9.chunks -> 9.sums] completed
            Completed Task = sum_of_squares

