.. _Simple_Tutorial_2nd_step:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator


###################################################################
Step 2: Passing parameters to the pipeline
###################################################################
.. hlist::
   * :ref:`Simple tutorial overview <Simple_Tutorial>` 
   * :ref:`@files syntax in detail <decorators.files>`


************************************************
Remember to look at the example code:
************************************************

* :ref:`Python Code for step 2 <Simple_Tutorial_2nd_step_code>` 

***************************************
Overview
***************************************
    Each |task|_  or stage of the pipeline can also be a recipe or 
    `rule <http://www.gnu.org/software/make/manual/make.html#Rule-Introduction>`_  
    which can be applied at the same time to many different parameters.
    
    For example, one can have a *compile task* which will compile any source code, or
    a *count_lines task* which will count the number of lines in any file.
    
    Each |task|_, then, is a recipe for making specified files using supplied parameters.
    
    These files can be made in parallel, with each task function call in a separate |job|_.
    

************************************
*@files*
************************************
    | The :ref:`@files <decorators.files>` |decorator|_ provides parameters to a task.
    
    
    | The first two parameters of each job contain input and output files (respectively).
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
    | ``job2.stage2`` is more recent than ``job2.stage1``.
        
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
        
    
    Note that the other was up to date and skipped accordingly.
    
