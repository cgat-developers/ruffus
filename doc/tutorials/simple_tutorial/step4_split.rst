.. _Simple_Tutorial_4th_step:

###################################################################
Step 4: Splitting up large tasks / files
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`@split in detail <task.split>`

**************************************************************************************
Remember to look at the example code:
**************************************************************************************
* :ref:`Python Code for step 4 <Simple_Tutorial_4th_step_code>` 
    
**************************************************************************************
Splitting up a long list of random numbers to calculate their variance
**************************************************************************************

    Suppose we had a list of 100,000 random numbers:

        ::
        
            import random
            f = open(output_file_name, "w")
            for i in range(NUMBER_OF_RANDOMS):
                f.write("%g\n" % (random.random() * 100.0))

    
    We might want to calculate the sample variance more quickly by splitting them 
    into ``NNN`` parcels of 1000 numbers each and working on them in parallel. 
    In this case we known that ``NNN == 100`` but usually the number of resulting files
    is only apparent after we have finished processing the starting file.
    
    This is step 4 from:
    
    .. image:: ../../images/simple_tutorial_step4.png
        :scale: 50
       

    The code for this is easy to write because of the *Ruffus* decorator :ref:`@split<task.split>` which is
    designed to specifically for splitting up input into an indeterminate ``NNN`` number of 
    output files:
    
        ::
        
            @split("random_numbers.list", "*.chunks")
            def step_4_split_numbers_into_chunks (input_file_name, output_files):
                #
                """code goes here"""
            

    ``input_file_name`` will be set to the starting file, in this case, ``random_numbers.list``.
    
    ``output_files`` is a list of files which match ``*.chunks``.
    
    The first time you run this function ``*.chunks`` will return an empty list but at other
    times, ``*.chunks`` will match a list of previously created file names some of which will 
    be out of date or superfluous.

    These do not in any way constrain the number of files you actually want to split ``random_numbers.list``
    into.

    However, they may be useful for cleaning up detritus from previous runs 
    (have a look at :ref:`step_4_split_numbers_into_chunks(...) <Simple_Tutorial_4th_step_code>`).



