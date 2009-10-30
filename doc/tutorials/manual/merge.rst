.. _manual_7th_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run

#####################################################
Chapter 7: Merging many files into a single result
#####################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 
        * :ref:`@merge <decorators.merge>` syntax in detail

    At the conclusion of our pipeline, or at key selected points, we might need a 
    summary of our progress, gathering data from a multitude of files or disparate *input*, 
    and summarised in the *output*  of a single |job|_.
    
    *Ruffus* uses the :ref:`@merge <decorators.merge>` decorator for this purpose.
    
    Although, **@merge** tasks multiple *inputs* and produces a single *output*, **Ruffus**
    is again agnostic as to the sort of data contained within *output*. It can be a single
    (string) file name, or an arbitrary complicated nested structure with numbers, objects etc.
    As always, strings contained (even with nested sequences) within *output* will be treated
    as file names for the purpose of checking if the |task|_ is up-to-date.
    
.. index:: 
    single: @merge; Manual
    
.. _manual.merge:

=================
**@merge**
=================
This example is from :ref:`step 6 <Simple_Tutorial_6th_step>` of the simple tutorial.

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
       

    The :ref:`@merge <decorators.merge>` decorator tells *Ruffus* to take all the files from the step 5 task (i.e. ``*.sums``),
    and produced a merge file in the form of ``variance.result``.
    
    Thus if ``step_5_calculate_sum_of_squares`` created
        | ``1.sums`` and 
        | ``2.sums`` etc.
        
    This would result in the following function call:
    
        ::
        
            step_6_calculate_variance (["1.sums", "2.sums"], "variance.result")
            

    The final result is, of course, in ``variance.result``.
            




