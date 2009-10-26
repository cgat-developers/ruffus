.. _Simple_Tutorial_2nd_step:


###################################################################
Step 2: Passing parameters to the pipeline
###################################################################
* :ref:`Up <Simple_Tutorial>` 
* :ref:`Prev <Simple_Tutorial_1st_step>` 
* :ref:`Python Code <Simple_Tutorial_2nd_step_code>` 
* :ref:`Next <Simple_Tutorial_3rd_step>` 
* :ref:`@files syntax <task.files>` in detail

************************************
*@files*
************************************
    | The :ref:`@files <task.files>` decorator provides parameters to a task.
    | The task function is called in parallel with each set of parameters.

    (We describe each task function call as a separate **job**.)
    
    
    | The first two parameters of each job are the input and output files (respectively).
    | A job will be run only if the file timestamps are out of date.
        
    Let us provide input and outputs to our new pipeline:
        ::
            
            task_param = [
                                [ 'job1.stage1', "job1.stage2"], # 1st job
                                [ 'job2.stage1', "job2.stage2"], # 2nd job
                          ]
            
            @files(task_param)
            def second_task(input_file, output_file):
                pass


    The full python code is available :ref:`here.<Simple_Tutorial_2nd_step_code>` 
            
    
    The result of running this would be:
        ::
            
            Start Task = second_task
                1st_job
                Job = [job1.stage1 -> job1.stage2,     1st_job] completed
                2nd_job
                Job = [job2.stage1 -> job2.stage2,     2nd_job] completed
            Completed Task = second_task


************************************
Up-to-date jobs are not re-run
************************************
        

    | If you ran the same code a second time, nothing would happen because 
    | ``job1.stage2`` is more recent than ``job1.stage1`` and
    | ``job2.stage2`` is more recent than ``job2.stage1`` and
        
    However, if you subsequently modified ``job1.stage1`` again:
        ::
    
            >>> open("job1.stage1", "w")
        
    
    You would see the following:
        ::
    
            >>> pipeline_run([second_task])
            
            Start Task = second_task
                1st_job
                Job = [job1.stage1 -> job1.stage2,     1st_job] completed
                Job = [job2.stage1 -> job2.stage2,     2nd_job] unnecessary: already up to date
            Completed Task = second_task
        
    
    The 2nd job is up to date and will be skipped.
    
