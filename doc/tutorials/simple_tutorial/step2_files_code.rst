.. _Simple_Tutorial_2nd_step_code:
###################################################################
Code for Step 2: Passing parameters to the pipeline
###################################################################
* :ref:`Up <Simple_Tutorial>` 
* :ref:`Back <Simple_Tutorial_2nd_step>` 
* :ref:`@files syntax <task.files>` in detail

************************************
Code
************************************
    ::
        
        from ruffus import *
        import time
        
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
            time.sleep(1)


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
        
        #---------------------------------------------------------------
        #
        #       Run
        #
        pipeline_run([second_task])
       

************************************
Resulting Output
************************************
    ::
        
        Start Task = first_task
            Job = [None -> job1.stage1] completed
            Job = [None -> job2.stage1] completed
        Completed Task = first_task
        Start Task = second_task
            1st_job
            Job = [job1.stage1 -> job1.stage2,     1st_job] completed
            2nd_job
            Job = [job2.stage1 -> job2.stage2,     2nd_job] completed
        Completed Task = second_task
