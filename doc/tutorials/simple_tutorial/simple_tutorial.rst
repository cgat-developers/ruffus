.. _Simple_Tutorial:

.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator


################################################
7 steps to *Ruffus* in 10 minutes
################################################

***************************************
Introduction
***************************************

    The **Ruffus** module is a lightweight way to add support 
    for running computational pipelines.
    Computational pipelines are often conceptually quite simple, especially
    if we breakdown the process into simple stages, or separate |task|_\ s.
    Each stage or |task|_ of a pipeline is represented by an ordinary python function.
    These functions do not have to be rewritten to be part of a **Ruffus** pipeline.    
    Functions can be made part a pipeline by **decorating** them using
    special **Ruffus** |decorator|_\ s.
    
    | |decorator|_\ s are the way python uses to store additional information about a function.
    | They have similar syntax to python function calls with a number of parameters in parenthesis. 
    | However, decorator names must start with the ``@`` prefix.

    For example, the **ruffus** decorator :ref:`@follows <decorators.follows>` puts the stages of a pipeline in order
    (see :ref:`Step 1 <Simple_Tutorial_1st_step>` of this tutorial for more details.)
    
        ::
        
            @follows(first_task)
            def second_stage():
                ""

    | Multiple |decorator|_\ s can be used for each |task|_ function to add functionality
      to *Ruffus* pipeline functions. 
    | However, these remain ordinary python functions which can still be
      called normally, outside of *Ruffus*.
    | *Ruffus* |decorator|_\ s can be added (stacked on top of) to any function in any order.


    All the code in the tutorial can be pasted into and run from the python interpreter after
    **ruffus** has been installed.
    
***************************************
The first steps (1-3)
***************************************

    .. image:: ../../images/simple_tutorial_step3.png
        :scale: 50

    The first half of the tutorial will show you how to:
    
    1. :ref:`Chain tasks (functions) together into a pipeline <Simple_Tutorial_1st_step>` 
    
    2. :ref:`Provide parameters to run jobs in parallel <Simple_Tutorial_2nd_step>` 
    
    3. :ref:`Displaying all the stages of your new pipeline <Simple_Tutorial_3rd_step>` 

            
    
***************************************
An Easy example (steps 4-7)
***************************************
    | A common requirement in scientific pipelines is to break a large problem into small
      pieces which can be analysed in parallel. 
    | When that is finished, we need to join up
      the partial solutions into a complete solution again.
    
    This simple example calculates the sample variance of 10,000 random numbers

    .. image:: ../../images/simple_tutorial_step4.png
        :scale: 50
   
    * It breaks the list into 100 pieces
    * Calculates the sum and sum of squares for each set of 1000 numbers
    * Combine the sums to calculate the variance

    
    4. :ref:`Split up a large task (or file) into smaller jobs <Simple_Tutorial_4th_step>`  
    
    5. :ref:`Run all the jobs in parallel, checking dependencies <Simple_Tutorial_5th_step>`  
    
    6. :ref:`Merge the results back together <Simple_Tutorial_6th_step>`  
    
    7. :ref:`Automatically signal the completion of each stage of our pipeline <Simple_Tutorial_7th_step>` 


This covers all the core functionality of *Ruffus*.
    






