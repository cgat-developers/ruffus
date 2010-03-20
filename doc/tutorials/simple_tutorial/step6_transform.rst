.. _Simple_Tutorial_5th_step:

.. index:: 
    pair: @transform; Tutorial



###################################################################
Step 5: Running jobs in parallel
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`@transform in detail <decorators.transform>`

.. note::
    Remember to look at the example code:

    * :ref:`Python Code for step 5 <Simple_Tutorial_5th_step_code>` 

**************************************************************************************
Calculating sums and sum of squares in parallel
**************************************************************************************
    Now that we have many smaller lists of numbers in separate files, we can calculate their sums and 
    sum of squares in parallel.
    
    All we need is a function which takes a ``*.chunk`` file, reads the numbers, calculates
    the answers and writes them back out to a corresponding ``*.sums`` file.
    
    *Ruffus* magically takes care of applying this task function to all the different
    data files in parallel.
    
        .. image:: ../../images/simple_tutorial_transform.png
      
    .. ::
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

       

    | The first thing to note about this example is that the *input* files are not specified
      as a ``glob`` (e.g. ``*.chunk``) but as the preceding task. 
    | *Ruffus* will take all
      the files produced by ``step_4_split_numbers_into_chunks()`` and feed them as the *input*
      into step 5. 
    
    This handy shortcut also means that **Ruffus** knows that ``step_5_calculate_sum_of_squares``
    depends on ``step_4_split_numbers_into_chunks`` and an additional ``@follows`` directive
    is unnecessary.
    
    The use of :ref:`suffix<decorators.transform.suffix_string>` within the decorator tells 
    *Ruffus* to take all *input* files with the ``.chunks`` suffix and substitute a ``.sums`` 
    suffix to generate the corresponding *output* file name.
    
    
    Thus if ``step_4_split_numbers_into_chunks`` created
        ::
        
            "1.chunks"
            "2.chunks"
            "3.chunks"
        
    This would result in the following function calls:
    
        ::
        
            step_5_calculate_sum_of_squares ("1.chunk", "1.sums")
            step_5_calculate_sum_of_squares ("2.chunk", "2.sums")
            step_5_calculate_sum_of_squares ("3.chunk", "3.sums")
            
            # etc...
            


    .. note::    

        It is possible to generate *output* filenames using more powerful regular expressions
        as well. See the :ref:`@transform <decorators.transform>` syntax documentation for more details.

