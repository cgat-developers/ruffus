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
    
    These files can be made in parallel, with each task function call in a separate |job|_
    but let us start with the simplest case where a pipeline stage consists of a single
    job with one *input*, one *output*, and an optional number of extra parameters
    

************************************
*@files*
************************************
    | The :ref:`@files <decorators.files>` |decorator|_ provides parameters to a task.
    
    
    | The first two parameters of each job contain *input* and *output* files (respectively).
    | A job will be run only if the file timestamps are out of date.
        
    Let us provide `input` and `outputs` to our new pipeline:
        ::
        
            from ruffus import *            

            @files("task1.input", "task1.output", "optional_1.extra", "optional_2.extra")
            def pipeline_task(input_file, output_file, extra_parameter1, extra_parameter2):
                pass
        
            # make sure the input file is there
            open("task1.input", "w")        
        
            pipeline_run([pipeline_task])
        
        
    The results of running our pipeline will be:
    
        ::
        
            >>> pipeline_run([pipeline_task])

                Job = [task1.input -> task1.output, optional_1.extra, optional_2.extra] completed
            Completed Task = pipeline_task
        
        
************************************
Running jobs in parallel
************************************
    The same syntax can be used to specify multiple jobs which can all be run at the same time.
    The time, instead of providing a single *input*, and a single *output*, we are going to specify
    the parameters for two jobs at once:
    
        ::
            
            task_param = [
                                [ 'job1.stage1', "job1.stage2"], # 1st job
                                [ 'job2.stage1', "job2.stage2"], # 2nd job
                          ]
            
            @files(task_param)
            def second_task(input_file, output_file):
                pass


    (Copy and paste the code :ref:`here.<Simple_Tutorial_2nd_step_code>` into your python interpreter. )
            
    
    The result of running this should look familiar:
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
        

    | If you ran the same code a second time,

        ::
        
            >>> pipeline_run([pipeline_task])


    | nothing would happen because 
    | ``job1.stage2`` is more recent than ``job1.stage1`` and
    | ``job2.stage2`` is more recent than ``job2.stage1``.
        
    However, if you subsequently modified ``job1.stage1`` again:
        ::
    
            open("job1.stage1", "w")
            pipeline_run([second_task], verbose =2)
        
    
    You would see the following:
        ::
    
            >>> pipeline_run([second_task])
            
            Start Task = second_task
                1st_job
                Job = [job1.stage1 -> job1.stage2,     1st_job] completed
                Job = [job2.stage1 -> job2.stage2,     2nd_job] unnecessary: already up to date
            Completed Task = second_task
        
    
    Note that the other job was up to date and skipped accordingly.
    
    
***************************************
*Input* and *output* data for each job
***************************************

    In the above examples, the *input* and *output* parameters are single file names. In a real
    computational pipeline, the *input* parameter could be all sorts of data, from
    lists of files, to numbers, sets or tuples. Ruffus will look inside each
    of your *input* and *output* parameters to see if they contain any names of up to date files. 
    Otherwise, Ruffus puts few constraints in your way.

    **Ruffus** will even automatically expand ``glob`` specifiers for you.
    
    For example, 
    
        | the *input* parameter for our task function might be all files which match ``*.input``
        | the *output* parameter could be a list: ``[13, (28.5, "task1.output")]``
    
    Running the following code:
    
        ::
            
            from ruffus import *            

            @files("*.input", [13, (28.5, "task1.output")])
            def pipeline_task(inputs, outputs):
                pass
        
            # make sure the input files are there
            open("task1a.input", "w")        
            open("task1b.input", "w")        
        
            pipeline_run([pipeline_task])


    will give the following results:
    
        ::
        
            >>> pipeline_run([pipeline_task])

                Job = [[task1a.input, task1b.input] -> [13, [28.5, task1.output]]] completed
            Completed Task = pipeline_task
            
    


    
