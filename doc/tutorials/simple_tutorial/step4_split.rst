.. _Simple_Tutorial_4th_step:
.. index:: 
    pair: @split; Tutorial


###################################################################
Step 4: Splitting up large tasks / files
###################################################################
    * :ref:`Simple tutorial overview <Simple_Tutorial>` 
    * :ref:`@split in detail <decorators.split>`

    .. note::
        Remember to look at the example code:
    
        * :ref:`Python Code for step 4 <Simple_Tutorial_4th_step_code>` 
    
    | The second half of this tutorial is a worked example to calculate 
      the sample variance of 10,000 random numbers.
    | This is similar to many computational projects: we are tackling a big problem
      by splitting it up into many tiny problems solved in parallel. We can then
      merge our piecemeal solutions into our final answer. These 
      `embarassingly parallel <http://en.wikipedia.org/wiki/Embarrassingly_parallel>`_
      problems motivated the original design of **Ruffus**.
    
    **Ruffus** has three dedicated decorators to handle these problems with ease:
    
        * :ref:`@split<decorators.split>` to break up the big problem
        * :ref:`@transfrom<decorators.split>` to solve the parts in parallel
        * :ref:`@merge<decorators.split>` to merge our piecemeal solutions into the final answer.
    
    
**************************************************************************************
Splitting up a long list of random numbers to calculate their variance
**************************************************************************************

    .. csv-table:: 
        :widths: 1,99
        :class: borderless

        ".. centered::
            Step 4 from:

        .. image:: ../../images/simple_tutorial_step4.png", "
            Suppose we had a list of 100,000 random numbers in the file ``random_numbers.list``:
            
                ::
                
                    import random
                    f = open('random_numbers.list', 'w')
                    for i in range(NUMBER_OF_RANDOMS):
                        f.write('%g\n' % (random.random() * 100.0))
            
            
            We might want to calculate the sample variance more quickly by splitting them 
            into ``NNN`` parcels of 1000 numbers each and working on them in parallel. 
            In this case we known that ``NNN == 100`` but usually the number of resulting files
            is only apparent after we have finished processing our starting file."
    

    Our pipeline function needs to take the random numbers file ``random_numbers.list``,
    read the random numbers from it, and write to a new file every 100 lines.
    
    The *Ruffus* decorator :ref:`@split<decorators.split>` is designed specifically for 
    splitting up input into an indeterminate ``NNN`` number of output files:
    
        .. image:: ../../images/simple_tutorial_split.png
        
    .. ::
    
        ::
        
            @split("random_numbers.list", "*.chunks")
            def step_4_split_numbers_into_chunks (input_file_name, output_files):
                #
                """code goes here"""
            

    Ruffus will set 

        | ``input_file_name`` to ``"random_numbers.list"``
        | ``output_files`` to all files which match ``*.chunks`` (i.e. ``"1.chunks"``, ``"2.chunks"`` etc.).
    
    The first time you run this function ``*.chunks`` will return an empty list because
    no ``.chunks`` files have been created, resulting in the following:
    
        ::
        
            step_4_split_numbers_into_chunks ("random_numbers.list", [])
    
    After that ``*.chunks`` will match the list of current ``.chunks`` files created by
    the previous pipeline run. Some of these files will be out of date or superfluous.
    These file names are usually only useful for removing detritus from previous runs 
    (have a look at :ref:`step_4_split_numbers_into_chunks(...) <Simple_Tutorial_4th_step_code>`).
    
    .. note ::

        The great value of specifying correctly the list of *output* files will become apparent in the next
        step of this tutorial when we shall see how pipeline tasks can be "chained" together conveniently.
        
        Remember to specify ``globs`` patterns which match *all* the files you are splitting up. You can
        cover different directories, or groups of file names by using a list of ``globs``:
        e.g.   ::
            
                @split("input.file", ['a*.bits', 'b*.pieces', 'somewhere_else/c*.stuff'])
                def split_function (input_filename, output_files):
                    "Code to split up 'input.file'"
                    



