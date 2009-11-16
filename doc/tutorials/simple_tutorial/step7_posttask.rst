.. index:: 
    pair: @posttask; Tutorial

.. _Simple_Tutorial_7th_step:


###################################################################
Step 7: Signal the completion of each stage of our pipeline
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`@posttask<decorators.posttask>` in detail

.. note::
    Remember to look at the example code:

    * :ref:`Python Code for step 7 <Simple_Tutorial_7th_step_code>` 
    
Let us finish by celebrating the success of our modest pipeline example.

**************************************************************************************
Running some code to show that a stage of the pipeline has finished
**************************************************************************************

    A common requirement is to take some extra action when a particular 
    :term:`task` or stage of a pipeline is complete.
    
    This can range from printing out some message, or ``touching`` some sentinel file,
    to emailing the author.
    
    This is particular useful if the :term:`task` is a recipe apply to an unspecified number
    of parameters in parallel in different :term:`job`\s
    
    The "extra action" can be added to a *Ruffus* pipeline using the :ref:`@posttask<decorators.posttask>`
    decorator.
    
    Let us print a "hooray" message to show that we have finished calculating variances.
    
        .. image:: ../../images/simple_tutorial_posttask.png

    .. ::
    
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
    
.. index:: 
    pair: @posttask (touchfile); Tutorial
    pair: touchfile (@posttask); Tutorial

**************************************************************************************
*Touching* a sentinel file after finishing a pipeline stage
**************************************************************************************
    | Very often we would like to mark the competion of a pipeline stage by using the
      date/time stamp of a "sentinel" file.
    | This is such a common requirement that *Ruffus* even has special syntax for this
      in the form of :ref:`touch_file<decorators.touch_file>`.
      
    
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
                
**************************************************************************************
Finding out more about **Ruffus**
**************************************************************************************

    This wraps up our short tutorial on the **Ruffus**. 
    To find out more about **Ruffus**, you can read the :ref:`manual<manual.introduction>`
    or just start using **Ruffus**.
    
    Email the authors at ruffus_lib at llew.org.uk if you have any comments or suggestions.
    
    Happy pipelining!
    

