.. _Simple_Tutorial_3nd_step_code:


###################################################################
Code for Step 3: Displaying the pipeline visually
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`pipeline functions <pipeline_functions>` in detail
* :ref:`Back to Step 3 <Simple_Tutorial_3rd_step>` 

******************************************
Display the initial state of the pipeline
******************************************
    ::
        
        from ruffus import *
        import sys
        
        #---------------------------------------------------------------
        #
        #   first task
        #
        task1_param = [
                            [ None, 'job1.stage1'], # 1st job
                            [ None, 'job2.stage1'], # 2nd job
                      ]
                                            
        @files(task1_param)
        def first_task(no_input_file, output_file):
            open(output_file, "w")
            #
            # pretend we have worked hard


        #---------------------------------------------------------------
        #
        #   second task
        #
        task2_param = [
                            [ 'job1.stage1', "job1.stage2", "    1st_job"], # 1st job
                            [ 'job2.stage1', "job2.stage2", "    2nd_job"], # 2nd job
                      ]
        
        @follows(first_task)
        @files(task2_param)
        def second_task(input_file, output_file, extra_parameter):
            open(output_file, "w")
            print extra_parameter
        
        pipeline_printout(sys.stdout, [second_task], verbose = 3)
        
************************************
Resulting Output
************************************
    ::

        >>> pipeline_printout(sys.stdout, [second_task])

            Task = first_task
                   Job = [None -> job1.stage1]
                   Job = [None -> job2.stage1]
            
            Task = second_task
                   Job = [job1.stage1 -> job1.stage2,     1st_job]
                   Job = [job2.stage1 -> job2.stage2,     2nd_job]
            
******************************************
Display the partially up-to-date pipeline
******************************************
    Run the pipeline, modify ``job1.stage`` so that the second task is no longer up-to-date
    and printout the pipeline stage again::
        
        pipeline_run([second_task])
   
        # modify job1.stage1
        open("job1.stage1", "w").close()
   

    At a verbosity of 5, even jobs which are up-to-date will be displayed::
    
        >>> pipeline_printout(sys.stdout, [second_task], verbose = 5)
        ________________________________________
        Tasks which are up-to-date:
        
        Task = first_task
               Job = [None
                     ->job1.stage1]
                 Job up-to-date
               Job = [None
                     ->job2.stage1]
                 Job up-to-date
        
        
        ________________________________________
        Tasks which will be run:
        
        Task = second_task
               Job = [job1.stage1
                     ->job1.stage2,     1st_job]
                 Job needs update: Need update file times= [[(1269025787.0, 'job1.stage1')], [(1269025785.0,
                       'job1.stage2')]]
               Job = [job2.stage1
                     ->job2.stage2,     2nd_job]
                 Job up-to-date
        
        ________________________________________

    We can now see that the there is only one job in "second_task" which needs to be re-run
    because 'job1.stage1' has been modified after 'job1.stage2'


