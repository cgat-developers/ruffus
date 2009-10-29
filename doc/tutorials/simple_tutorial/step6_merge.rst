.. _Simple_Tutorial_6th_step:

###################################################################
Step 6: Merging results back together
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`@merge in detail <task.merge>`

**************************************************************************************
Remember to look at the example code:
**************************************************************************************
* :ref:`Python Code for step 6 <Simple_Tutorial_6th_step_code>` 

**************************************************************************************
Calculating variances from the sums and sum of squares of all chunks
**************************************************************************************

    If we add up all the sums, and sum of squares we calculated previously, we can
    obtain the variance as follows::
    
        variance = (sum_squared - sum * sum / N)/N
        
    where ``N`` is the number of values

    See the `wikipedia <http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance>`_ entry for a discussion of 
    why this is a very naive approach!
    
    To do this, all we have to do is merge together all the values in ``*.sums``, i.e.
    add up the ``sums`` and ``sum_squared`` for each chunk. We can then apply the above (naive) formula.
    
    Merging files is straightforward in **Ruffus**:
        ::

            @merge(step_5_calculate_sum_of_squares, "variance.result")
            def step_6_calculate_variance (input_file_names, output_file_name):
                #
                #   add together sums and sums of squares from each input_file_name
                #       calculate variance and write to output_file_name
                ""


    This is step 6 from:
    
    .. image:: ../../images/simple_tutorial_step4.png
        :scale: 50
       

    The :ref:`@merge <task.merge>` decorator tells *Ruffus* to take all the files from the step 5 task (i.e. ``*.sums``),
    and produced a merge file in the form of ``variance.result``.
    
    Thus if ``step_5_calculate_sum_of_squares`` created
        | ``1.sums`` and 
        | ``2.sums`` etc.
    This would result in the following function call:
    
        ::
        
            step_6_calculate_variance (["1.sums", "2.sums"], "variance.result")
            

    The final result is, of course, in ``variance.result``.
            




