.. _manual_6th_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run

###################################################################
Chapter 6: Applying the same recipe to create many different files
###################################################################
    .. hlist::
    
        * :ref:`Manual overview <manual>` 
        * :ref:`@transform <decorators.transform>` syntax in detail

    Often we have a list of files for which we would like to take the same action.
    The easiest way to manage this is by deriving a matching set of resulgin output files 
    with related file names. For example, compiling c source files transforms ``*.c``
    files to ``*.o`` files. Many pipelines can be (and have been) easily constructed by
    tracing the data files as they flow through the computational process, with each stage
    giving a new file suffix.
    
    *Ruffus* uses the :ref:`@transform <decorators.transform>` decorator for this purpose.
    In the interests of maximal flexibility, you are not restricted to changing suffixes
    when you **transform** your data from one file type to another. We shall see how,
    with the full power of regular expressions, you can move different data into different directories,
    add indices and so on.
    
    
    
.. index:: 
    single: @transform; Manual
    
.. _manual.transform:

=================
**@transform**
=================
This example is from :ref:`step 5 <Simple_Tutorial_5th_step>` of the simple tutorial.

**************************************************************************************
Remember to look at the example code:
**************************************************************************************
* :ref:`Python Code for step 5 <Simple_Tutorial_5th_step_code>` 

**************************************************************************************
Calculating sums and sum of squares in parallel
**************************************************************************************

    Given a set of files, each with a set of random numbers, we want to calculate thier
    sums and sum of squares.
    
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
            


*********************************************************************************************
Using :ref:`suffix(...) <decorators.suffix>` to change give each output file a new suffix
*********************************************************************************************


*********************************************************************************************
Regular expressions :ref:`regex(...) <decorators.regex>` provide maximum flexibility
*********************************************************************************************

