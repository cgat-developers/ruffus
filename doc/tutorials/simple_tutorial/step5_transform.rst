.. _Simple_Tutorial_5th_step:

###################################################################
Step 5: Running jobs in parallel
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`@transform in detail <decorators.transform>`

**************************************************************************************
Remember to look at the example code:
**************************************************************************************
* :ref:`Python Code for step 5 <Simple_Tutorial_5th_step_code>` 

**************************************************************************************
Calculating sums and sum of squares in parallel
**************************************************************************************

    For each chunk of random numbers, we can calculate their sums and sum of squares.
    
    The easiest way to do this is by providing a recipe for transforming a ``*.chunk`` file
    into a ``*.sums`` file which would contain our sums and sum of squares.
    
    *Ruffus* magically takes care of applying the same recipe (task function) to all the different
    data files in parallel.
    
    ::
        
        #---------------------------------------------------------------
        #
        #   Calculate sum and sum of squares for each chunk file
        #
        @transform(step_4_split_numbers_into_chunks, suffix(".chunks"), ".sums")
        def step_5_calculate_sum_of_squares (input_file_name, output_file_name):
            #
            #   calculate sums and sums of squares for all values in the input_file_name
            #       writing to output_file_name
            ""

    This is step 5 from:
    
    .. image:: ../../images/simple_tutorial_step4.png
        :scale: 50
       

    The :ref:`@transform <decorators.transform>` decorator tells *Ruffus* to take files from the step 4 task (i.e. ``*.chunks``),
    and produce files having the ``.sums`` suffix instead.
    ending.
    
    Thus if ``step_4_split_numbers_into_chunks`` created
        | ``1.chunks`` and 
        | ``2.chunks`` etc.
        
    This would result in the following function calls:
    
        ::
        
            step_5_calculate_sum_of_squares ("1.chunk", "1.sums")
            step_5_calculate_sum_of_squares ("2.chunk", "2.sums")
            
            # etc...
            




