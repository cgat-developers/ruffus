.. _Simple_Tutorial_4th_step_code:

###################################################################
Code for Step 4: Splitting up large tasks / files
###################################################################
    * :ref:`Simple tutorial overview <Simple_Tutorial>` 
    * :ref:`@split in detail <task.split>`
    * :ref:`back to step 4 <Simple_Tutorial_4th_step>`

************************************
Code
************************************
    ::
        
        NUMBER_OF_RANDOMS = 10000
        CHUNK_SIZE = 1000
        
        
        from ruffus import *
        import time
        
        import random
        
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

        pipeline_run([step_4_split_numbers_into_chunks], verbose = 2)

************************************
Resulting Output
************************************
    ::
                           
        >>> pipeline_run([step_4_split_numbers_into_chunks], verbose = 2)
        
            Start Task = create_random_numbers
            
                Job = [None -> random_numbers.list] Missing file random_numbers.list
                Job = [None -> random_numbers.list] completed
            Completed Task = create_random_numbers
            Start Task = step_4_split_numbers_into_chunks
            Splits random numbers file into XXX files of CHUNK_SIZE each
                Job = [random_numbers.list -> *.chunks] Missing output file
                Job = [random_numbers.list -> *.chunks] completed
            Completed Task = step_4_split_numbers_into_chunks

