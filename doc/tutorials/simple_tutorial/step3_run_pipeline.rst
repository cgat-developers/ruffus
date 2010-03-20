.. _Simple_Tutorial_3rd_step:



###################################################################
Step 3: Understanding how your pipeline works
###################################################################
    * :ref:`Simple tutorial overview <Simple_Tutorial>` 
    * :ref:`pipeline functions <pipeline_functions>` in detail

.. note::
    Remember to look at the example code:

    * :ref:`Python Code for step 3 <Simple_Tutorial_3nd_step_code>` 
    
.. index:: 
    pair: pipeline_printout; Tutorial


..comment::


The trickiest part of developing pipelines is understanding how your
data flows through the pipeline.

Parameters and files are passed from one task to another down the chain
of pipelined functions.

Whether you are trying to learn to use **ruffus**, or try out a new
feature in **ruffus** or just have a horrendously complicated pipeline
to debug (we have colleagues with >100 criss-crossing pipelined stages),
your best friend is **pipeline_printout**
    

    
=======================================
Printing out which jobs will be run
=======================================

    **pipeline_printout** takes the same parameters as pipeline_run but just print 
    the tasks which are and are not up-to-date to a specified file stream (like
    ``sys.stdout``)
    
    The verbose parameter controls in how much detail your pipeline should be displayed.
    
    Let us take the :ref:`pipelined code<Simple_Tutorial_3nd_step_code>` we have written already, 
    but call ``pipeline_printout`` instead of ``pipeline_run``::

        >>> pipeline_printout(sys.stdout, [second_task])
        
        ________________________________________
        Tasks which will be run:
        
        Task = first_task
        Task = second_task
        ________________________________________
        

    This lists the tasks which will be run in the pipeline.
    
    To see the input and output parameters of each job in the pipeline, we can increase the verbosity::      
    
        >>> pipeline_printout(sys.stdout, [second_task], verbose = 3)

        ________________________________________
        Tasks which will be run:
        
        Task = first_task
               Job = [None
                     ->job1.stage1]
                 Job needs update: Missing file job1.stage1
               Job = [None
                     ->job2.stage1]
                 Job needs update: Missing file job2.stage1
        
        Task = second_task
               Job = [job1.stage1
                     ->job1.stage2,     1st_job]
                 Job needs update: Missing file job1.stage1
               Job = [job2.stage1
                     ->job2.stage2,     2nd_job]
                 Job needs update: Missing file job2.stage1
        
        ________________________________________


    This is very useful for checking that the input and output parameters have been specified
        correctly.

=============================================
Determining which jobs are out-of-date or not
=============================================

    It is often useful to see which tasks are or are not up-to-date. For example, if we
    were to run the pipeline in full, and then modify one of the intermediate files, the
    pipeline would be partially out of date.
    

    Let us run the pipeline in full but then modify ``job1.stage`` so that the second task is no longer up-to-date.
        
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


            
    
     