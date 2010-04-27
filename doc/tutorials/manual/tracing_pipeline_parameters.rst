.. include:: ../../global.inc
.. include:: chapter_numbers.inc

.. _manual.tracing_pipeline_parameters:

#################################################################################################################
|manual.tracing_pipeline_parameters.chapter_num|: Tracing pipeline parameters
#################################################################################################################
    * :ref:`Manual overview <manual>` 


    .. index:: 
        pair: pipeline_printout; Manual
        pair: Tracing pipeline parameters; Manual
        pair: Debugging; Manual
    
        
    The trickiest part of developing pipelines is understanding how your
    data flows through the pipeline.
    
    In **Ruffus**, your data is passed from one task function to another down
    the pipeline by the chain of linked parameters. Sometimes, it may be difficult to 
    choose the right **Ruffus** syntax at first, or to understand which parameters in
    what format are being passed to your function.

    Whether you are learning how to use **ruffus**, or trying out a new
    feature in **ruffus**, or just have a horrendously complicated pipeline
    to debug (we have colleagues with >100 criss-crossing pipelined stages),
    your best friend is :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>`.
    
    **pipeline_printout** displays the parameters which would be passed to each task function
    for each job in your pipeline. In other words, it traces how each of the functions in
    the pipeline are called in detail.
   
    It makes good sense to alternate between calls to **pipeline_printout** and **pipeline_run** 
    in the development of **Ruffus** pipelines (perhaps with the use of a command-line option), 
    so that you always know exactly how the pipeline is being invoked. 
    
   
=======================================
Printing out which jobs will be run
=======================================

    **pipeline_printout** is called in exactly the same way as **pipeline_run** but 
    instead of running the pipeline, just prints the tasks which are and are not up-to-date.
        
    The ``verbose`` parameter controls how much detail is displayed.

        ::
    
            verbose = 0 : prints nothing
            verbose = 1 : logs warnings and tasks which are not up-to-date and which will be run
            verbose = 2 : logs doc strings for task functions as well
            verbose = 3 : logs job parameters for jobs which are out-of-date
            verbose = 4 : logs list of up-to-date tasks but parameters for out-of-date jobs
            verbose = 5 : logs parameters for all jobs whether up-to-date or not
            verbose = 10: logs messages useful only for debugging ruffus pipeline code

    
    Let us take the two step :ref:`pipeline<Simple_Tutorial_3nd_step_code>` from
    the tutorial. :ref:`Pipeline_printout(...) <pipeline_functions.pipeline_printout>` 
    by default merely lists the two tasks which will be run in the pipeline:


        .. image:: ../../images/simple_tutorial_pipeline_printout1.png

    .. ::
    
        ::
    
            >>> pipeline_printout(sys.stdout, [second_task])
            
            ________________________________________
            Tasks which will be run:
            
            Task = first_task
            Task = second_task
            ________________________________________
        

    
    To see the input and output parameters of out-of-date jobs in the pipeline, we can increase the verbosity from the default (``1``) to ``3``:

        .. image:: ../../images/simple_tutorial_pipeline_printout2.png
        
    This is very useful for checking that the input and output parameters have been specified
        correctly.

=============================================
Determining which jobs are out-of-date or not
=============================================

    It is often useful to see which tasks are or are not up-to-date. For example, if we
    were to run the pipeline in full, and then modify one of the intermediate files, the
    pipeline would be partially out of date.
    

    Let us start by run the pipeline in full but then modify ``job1.stage`` so that the second task is no longer up-to-date::
        
        pipeline_run([second_task])
   
        # modify job1.stage1
        open("job1.stage1", "w").close()
   

    At a verbosity of ``5``, even jobs which are up-to-date will be displayed.
    We can now see that the there is only one job in ``second_task(...)`` which needs to be re-run
    because ``job1.stage1`` has been modified after ``job1.stage2`` (highlighted in blue):
    
        .. image:: ../../images/simple_tutorial_pipeline_printout3.png
        


            
    
