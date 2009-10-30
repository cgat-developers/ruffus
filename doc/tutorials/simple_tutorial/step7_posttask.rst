.. _Simple_Tutorial_7th_step:
.. |task| replace:: **task**
.. _task: glossary.html#term-task
.. |jobs| replace:: **jobs**
.. _jobs: glossary.html#term-job
.. |touch_file| replace:: *touch_file*
.. _touch_file: indicator_objects.html#decorators.touch_file

###################################################################
Step 7: Signal the completion of each stage of our pipeline
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`@posttask<decorators.posttask>` in detail

**************************************************************************************
Remember to look at the example code:
**************************************************************************************
* :ref:`Python Code for step 7 <Simple_Tutorial_7th_step_code>` 

**************************************************************************************
Running some code to show that a stage of the pipeline has finished
**************************************************************************************

    A common requirement is to take some extra action when a particular 
    |task|_ or stage of a pipeline is complete.
    
    This can range from printing out some message, or ``touching`` some sentinel file,
    to emailing the author.
    
    This is particular useful if the |task|_ is a recipe apply to an unspecified number
    of parameters in parallel in different |jobs|_
    
    This can be added to a *Ruffus* pipeline using the :ref:`@posttask<decorators.posttask>`
    decorator.
    
    Let us print a "hooray" message to show that we have finished calculating variances.
    
        ::
        
            def print_hooray():
                sys.stdout.write("hooray\n")
        
            @posttask(print_hooray)
            @merge(step_5_calculate_sum_of_squares, "variance.result")
            def step_6_calculate_variance (input_file_names, output_file_name):
                ""
    
    This is such a short function, we can even write it in-line:
    
        ::
        
            @posttask(lambda: sys.stdout.write("hooray\n"))
            @merge(step_5_calculate_sum_of_squares, "variance.result")
            def step_6_calculate_variance (input_file_names, output_file_name):
                ""
    
**************************************************************************************
*Touching* a sentinel file after finishing a pipeline stage
**************************************************************************************
    This is such a common requirement that *Ruffus* even has special syntax for this
    in the form of |touch_file|_
    
        ::
        
            @posttask(touch_file("sentinel_flag"))
            def your_pipeline_function (input_file_names, output_file_name):
                ""
                
    The file ``sentinel_flag`` will be created (if it did not exist) or its
    date/time stamp changed to the current time whenever this stage of the pipeline is
    completed.
    

**************************************************************************************
Adding several post task actions
**************************************************************************************
    You can, of course, add more than one different action to be taken on completion of the 
    task, either by stacking up :ref:`@posttask<decorators.posttask>` decorators or by including
    several functions in the same **@posttask**:
    
        ::
        
            @posttask(print_hooray, print_whopee)
            @posttask(touch_file("sentinel_flag"))
            def your_pipeline_function (input_file_names, output_file_name):
                ""

