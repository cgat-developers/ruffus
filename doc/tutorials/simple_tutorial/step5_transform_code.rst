.. _Simple_Tutorial_5th_step_code:

###################################################################
Code for Step 5: Running jobs in parallel
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`@transform in detail <task.transform>`
* :ref:`back to step 5 <Simple_Tutorial_5th_step>`

************************************
Code
************************************
    ::
        
        NUMBER_OF_RANDOMS = 10000
        CHUNK_SIZE = 1000
        
        
        from ruffus import *
        import time
        
        import random
        import glob
        
        #---------------------------------------------------------------
        #
        #   Create random numbers 
        #
        @files(None, "random_numbers.list")
        def create_random_numbers(input_file_name, output_file_name):
            f = open(output_file_name, "w")
            for i in range(NUMBER_OF_RANDOMS):
                f.write("%g\n" % (random.random() * 100.0))
        
        #---------------------------------------------------------------
        #
        #   Split initial file
        #
        @follows(create_random_numbers)        
        @split("random_numbers.list", "*.chunks")
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
            #
            #   create new file every CHUNK_SIZE lines and 
            #       copy each line into current file
            # 
            output_file = None
            cnt_files = 0
            for i, line in enumerate(open(input_file_name)):
                if i % CHUNK_SIZE == 0:
                    cnt_files += 1
                    output_file = open("%d.chunks" % cnt_files, "w")
                output_file.write(line)
        
        #---------------------------------------------------------------
        #
        #   Calculate sum and sum of squares for each chunk file
        #
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

        pipeline_run([step_5_calculate_sum_of_squares], verbose = 1)

                                                                   
************************************
Resulting Output
************************************
    ::

        >>> pipeline_run([step_5_calculate_sum_of_squares], verbose = 1)
            Job = [None -> random_numbers.list] unnecessary: already up to date
        Completed Task = create_random_numbers
            Job = [random_numbers.list -> *.chunks] unnecessary: already up to date
        Completed Task = step_4_split_numbers_into_chunks
            Job = [6.chunks -> 6.sums] completed
            Job = [1.chunks -> 1.sums] completed
            Job = [4.chunks -> 4.sums] completed
            Job = [7.chunks -> 7.sums] completed
            Job = [2.chunks -> 2.sums] completed
            Job = [9.chunks -> 9.sums] completed
            Job = [10.chunks -> 10.sums] completed
            Job = [3.chunks -> 3.sums] completed
            Job = [5.chunks -> 5.sums] completed
            Job = [8.chunks -> 8.sums] completed
        Completed Task = step_5_calculate_sum_of_squares

