.. _Simple_Tutorial_3nd_step_code:


###################################################################
Code for Step 3: Displaying the pipeline visually
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`pipeline functions <pipeline_functions>` in detail
* :ref:`Back to Step 3 <Simple_Tutorial_3rd_step>` 

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
        #       Show flow chart and tasks before running the pipeline
        #
        print "Show flow chart and tasks before running the pipeline"
        pipeline_printout_graph ( open("flowchart_before.png", "w"),
                                 "png",
                                 [second_task],
                                 no_key_legend=True)
        pipeline_printout(sys.stdout, [second_task])
        
        
        #---------------------------------------------------------------
        #
        #       Run
        #
        pipeline_run([second_task])
    
   
        # modify job1.stage1
        open("job1.stage1", "w").close()
   
       
        #---------------------------------------------------------------
        #
        #       Show flow chart and tasks after running the pipeline
        #
        print "Show flow chart and tasks after running the pipeline"
        pipeline_printout_graph ( open("flowchart_after.png", "w"),
                                 "png",
                                 [second_task],
                                 no_key_legend=True)
        pipeline_printout(sys.stdout, [second_task])
        
        
************************************
Resulting Flowcharts
************************************
   +-------------------------------------------------------------+-----------------------------------------------------------------------+
   | .. image:: ../../images/simple_tutorial_stage3_before.png   | .. image::  ../../images/simple_tutorial_stage3_after.png             |
   |           :alt: Before running the pipeline                 |     :alt: After running the pipeline                                  |                           
   |           :scale: 50                                        |     :scale: 50                                                        |                           
   |           :align: center                                    |     :align: center                                                    |                           
   |                                                             |                                                                       |                           
   | .. centered:: Before                                        | .. centered:: After                                                   |                           
   |                                                             |                                                                       |                           
   +-------------------------------------------------------------+-----------------------------------------------------------------------+
   | .. image:: ../../images/tutorial_key.jpg                                                                                            |
   |           :alt: Legend key                                                                                                          |                           
   |           :scale: 75                                                                                                                |                           
   |           :align: center                                                                                                            |                           
   |                                                                                                                                     |                           
   | .. centered:: Legend                                                                                                                |                           
   |                                                                                                                                     |                           
   +-------------------------------------------------------------------------------------------------------------------------------------+



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
        
        >>> pipeline_run([second_task])

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

        >>> # modify job1.stage1
        ... open("job1.stage1", "w").close()

        >>> pipeline_printout(sys.stdout, [second_task])
        
            Task = second_task
                   Job = [job1.stage1 -> job1.stage2,     1st_job]
                U: Job = [job2.stage1 -> job2.stage2,     2nd_job]

                                                   
    producing the following flowchart
    

