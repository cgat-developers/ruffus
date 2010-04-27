.. include:: ../../global.inc
.. include:: chapter_numbers.inc

.. _manual.transform:

#######################################################################################################################
|manual.transform.chapter_num|: `Applying the same recipe to create many different files with` **@transform**
#######################################################################################################################
    .. hlist::
    
        * :ref:`Manual overview <manual>` 
        * :ref:`@transform <decorators.transform>` syntax in detail

    Sometimes you might have a list of data files which you might want to send to the
    same pipelined function, to apply
    the same operation. The best way to manage this would be to produce a corresponding 
    list of results files:
    
        | Compiling c source files might *@transform* an ``a.c`` file to an ``a.o`` file.
        | A ``grep`` operation might *@transform* a ``plays.king_lear.txt`` file to an ``plays.king_lear.counts`` file.
    
    *Ruffus* uses the :ref:`@transform <decorators.transform>` decorator for this purpose.

    When you **@transform** your data from one file type to another, you are not restricted just
    to changing the file suffix. We shall see how, with the full power of regular 
    expressions behind you, you can sort the resulting
    data into different directories, add indices and so on.
    
    
    
    .. index:: 
        pair: @transform; Manual
    

=================
**@transform**
=================
**************************************************************************************
Worked example: calculating sums and sum of squares in parallel
**************************************************************************************
    This example is borrowed from :ref:`step 5 <Simple_Tutorial_5th_step>` of the simple tutorial.
    
        .. note:: See :ref:`example code here <Simple_Tutorial_5th_step_code>` 
    

    Given a set of files, each with a set of random numbers, we want to calculate thier
    sums and sum of squares. The easiest way to do this is by providing a recipe for 
    transforming a ``*.chunk`` file containing a list of numbers into a ``*.sums`` file 
    with our sums and sum of squares.
    
    *Ruffus* magically takes care of applying the same recipe (task function) to all the different
    data files in parallel.

        .. image:: ../../images/simple_tutorial_transform.png

    The :ref:`@transform <decorators.transform>` decorator tells *Ruffus* to take files from the step 4 task (i.e. ``*.chunks``),
    and produce files having the ``.sums`` suffix instead.
    ending.
    
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
            
================================================================================================
Using :ref:`suffix(...) <decorators.suffix>` to change give each output file a new suffix
================================================================================================


    The :ref:`suffix<decorators.suffix>` specification indicates that
    
        * only filenames with ending with the suffix term (e.g. ``.chunk``) should be considered
        * The text matching the suffix term should be replaced with the string in the output pattern.
        

    This example assumes that both the *inputs* and the *outputs* consist each of a single string but
    **Ruffus** places no such constraints on the data flowing through your pipeline. 

        * If there are multiple file names (strings) contained within each *inputs* parameter,
          then only the first will be used to generate the *output*
        * Each string that is encountered in each *output* parameter will be used for suffix replacement.
        
        
************************************************        
An example with more complex data structures
************************************************        
    This will become much clearer with this example:
    

        ::
    
                inputs = [                                                                    
                                ["file1.ext", 10   ],               #job 1
                                [37.0, "file2.wrong_extension",     
                                       "file2_ignored.ext"],        #job 2
                                "file3.ext"                         #job 3
                                ]
            
            @transform(inputs, suffix(".ext"), [(".ext1", ), ".ext2"])
            def pipelinetask (input_file_name, output_file_name):
                ""
                

    | Granted, it may seem rather odd that the *inputs* parameter including numbers as well
      as file names, but **Ruffus** does not second guess how you wish to arrange your pipelines.
    | ``inputs`` contains the parameters for three jobs.
    | In each case, the first file name string encountered will be used to generate the *output* parameter:
    
        .. image:: ../../images/manual_transform_complex_outputs.png

        .. note:: 
            The first filename in the prospective job #2 does not have the ``.ext`` suffix so this job will be eliminated.
    
    Thus, the original code:
    
        ::
        
            @transform(inputs, suffix(".ext"), [(15, ".ext1"), ".ext2"])
            def pipelinetask (input_file_name, output_file_name):
                ""
                
    is equivalent to calling:
            
        ::
        
            pipelinetask(["file1.ext", 10], [(15, 'file1.ext1'), 'file1.ext2'])  # job 1
            pipelinetask("file3.ext",       [(15, 'file3.ext1'), 'file3.ext2'])  # job 3
            
    Hopefully, your code will simpler than this rather pathological case!


================================================================================================
Regular expressions :ref:`regex(...) <decorators.regex>` provide maximum flexibility
================================================================================================

    Exactly the same function could be written using regular expressions:
    
        ::
        
            @transform(inputs, regex(".ext"), [(15, ".ext1"), ".ext2"])
            def pipelinetask (input_file_name, output_file_name):
                ""
                

    | However, regular expressions are not limited to suffix matches. 
    | We can sort our *ouputs* to different subdirectories, depending on category.
    |
    | Our example starts off with data file for different zoo animals.
    | We are only interested in mammals, and we would like the files of each species to 
    | end up in its own directory after processing.                                     
    | Starting with these species files:
    
        ::
        
            "mammals.tiger.wild.animals"     
            "mammals.lion.wild.animals"      
            "mammals.lion.handreared.animals"
            "mammals.dog.tame.animals"       
            "mammals.dog.wild.animals"       
            "reptiles.crocodile.wild.animals"
            
    Then, the following:
        .. image:: ../../images/manual_transform.png
    
    will put each captured mammal in its own directory:
        ::

            >>> pipeline_run([capture_mammals])
                Job = [mammals.dog.tame.animals        -> dog/dog.tame.in_my_zoo, dog] completed
                Job = [mammals.dog.wild.animals        -> dog/dog.wild.in_my_zoo, dog] completed
                Job = [mammals.lion.handreared.animals -> lion/lion.handreared.in_my_zoo, lion] completed
                Job = [mammals.lion.wild.animals       -> lion/lion.wild.in_my_zoo, lion] completed
                Job = [mammals.tiger.wild.animals      -> tiger/tiger.wild.in_my_zoo, tiger] completed
            Completed Task = capture_mammals

    .. note:: The code can be found :ref:`here <manual.transform_code>` 


        



