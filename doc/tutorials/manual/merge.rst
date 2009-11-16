.. _manual_7th_chapter:

#####################################################################
**Chapter 7**: **Merge** `multiple input into a single result`
#####################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 
        * :ref:`@merge <decorators.merge>` syntax in detail

    At the conclusion of our pipeline, or at key selected points, we might need a 
    summary of our progress, gathering data from a multitude of files or disparate *inputs*, 
    and summarised in the *output*  of a single :term:`job`.
    
    *Ruffus* uses the :ref:`@merge <decorators.merge>` decorator for this purpose.
    
    Although, **@merge** tasks multiple *inputs* and produces a single *output*, **Ruffus**
    is again agnostic as to the sort of data contained within *output*. It can be a single
    (string) file name, or an arbitrary complicated nested structure with numbers, objects etc.
    As always, strings contained (even with nested sequences) within *output* will be treated
    as file names for the purpose of checking if the :term:`task` is up-to-date.
    
.. index:: 
    pair: @merge; Manual
    
.. _manual.merge:

=================
**@merge**
=================

This example is borrowed from :ref:`step 6 <Simple_Tutorial_6th_step>` of the simple tutorial.

    .. note:: :ref:`Accompanying Python Code  <Simple_Tutorial_6th_step_code>` 

**************************************************************************************
Combining partial solutions: Calculating variances
**************************************************************************************

    .. csv-table:: 
        :widths: 1,99
        :class: borderless

        ".. centered::
            Step 6 from:

        .. image:: ../../images/simple_tutorial_step4.png", "
            We wanted to calculate the sample variance of a large list of random numbers. We                                 
            have seen previously how we can split up this large problem into small pieces                                      
            (using @merge in :ref:`chapter 5 <manual_5th_chapter>`), and work out the                                        
            partial solutions for each sub-problem (calculaing sums with @transform in                                       
            :ref:`chapter 6 <manual_6th_chapter>`).                                                                          
                                                                                                                             
            All that remains is to join up the partial solutions from the different ``.sums`` files                          
            and turn these into the variance as follows::                                                                    
                                                                                                                             
                variance = (sum_squared - sum * sum / N)/N                                                                   
                                                                                                                             
            where ``N`` is the number of values                                                                              
                                                                                                                             
            See the `wikipedia <http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance>`_ entry for a discussion of
            why this is a very naive approach!"

    
    
    To do this, all we have to do is go through all the values in ``*.sums``, i.e.
    add up the ``sums`` and ``sum_squared`` for each chunk. We can then apply the above (naive) formula.
    
    Merging files is straightforward in **Ruffus**:
        ::

            @merge(step_5_calculate_sum_of_squares, "variance.result")
            def step_6_calculate_variance (input_file_names, output_file_name):
                #
                #   add together sums and sums of squares from each input_file_name
                #       calculate variance and write to output_file_name
                ""


    The :ref:`@merge <decorators.merge>` decorator tells *Ruffus* to take all the files from the step 5 task (i.e. ``*.sums``),
    and produced a merge file in the form of ``variance.result``.
    
    Thus if ``step_5_calculate_sum_of_squares`` created
        | ``1.sums`` and 
        | ``2.sums`` etc.
        
    This would result in the following function call:
    
        ::
        
            step_6_calculate_variance (["1.sums", "2.sums"], "variance.result")
            

    The final result is, of course, in ``variance.result``.
            




