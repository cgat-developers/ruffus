.. include:: ../../global.inc
.. include:: chapter_numbers.inc

.. _manual.split:

###################################################################################
|manual.split.chapter_num|: `Splitting up large tasks / files with` **@split**
###################################################################################
    .. hlist::
    
        * :ref:`Manual overview <manual>` 
        * :ref:`@split <decorators.split>` syntax in detail

    A common requirement in computational pipelines is to split up a large task into
    small jobs which can be run on different processors, (or sent to a computational
    cluster). Very often, the number of jobs depends dynamically on the size of the
    task, and cannot be known for sure beforehand. 

    *Ruffus* uses the :ref:`@split <decorators.split>` decorator to indicate that
    the :term:`task` function will produce an indeterminate number of output files.
    
    
    
    .. index:: 
        pair: @split; Manual
    

=================
**@split**
=================
This example is borrowed from :ref:`step 4 <Simple_Tutorial_5th_step>` of the simple tutorial.

    .. note :: See :ref:`accompanying Python Code <Simple_Tutorial_5th_step_code>` 
    
**************************************************************************************
Splitting up a long list of random numbers to calculate their variance
**************************************************************************************

    .. csv-table:: 
        :widths: 1,99
        :class: borderless

        ".. centered::
            Step 5 from the tutorial:

        .. image:: ../../images/simple_tutorial_step5_sans_key.png", "
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
    splitting up *inputs* into an indeterminate ``NNN`` number of *outputs*:
    
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
    

    
.. _manual.split.output_files:

=================
Output files
=================

    The *output* (second) parameter of **@split** usually contains a 
    |glob|_ pattern like the ``*.chunks`` above. 

    .. note::
        **Ruffus** is quite relaxed about the contents of the ``output`` parameter.
        Strings are treated as file names. Strings containing |glob|_ pattern are expanded.
        Other types are passed verbatim to the decorated task function.
    
    The files which match the |glob|_ will be passed as the actual parameters to the job
    function. Thus, the first time you run the example code ``*.chunks`` will return an empty list because
    no ``.chunks`` files have been created, resulting in the following:
    
        ::
        
            step_4_split_numbers_into_chunks ("random_numbers.list", [])
    
    After that ``*.chunks`` will match the list of current ``.chunks`` files created by
    the previous pipeline run. 



    File names in *output* are generally out of date or superfluous. They are useful 
    mainly for cleaning-up detritus from previous runs 
    (have a look at :ref:`step_4_split_numbers_into_chunks(...) <Simple_Tutorial_5th_step_code>`).
    
    .. note ::

        It is important, nevertheless, to specify correctly the list of *output* files.
        Otherwise, dependent tasks will not know what files you have created, and it will
        not be possible automatically to chain together the *ouput* of this pipeline task into the
        *inputs* of the next step.
        
        You can specify multiple |glob|_ patterns to match *all* the files which are the
        result of the splitting task function. These can even cover different directories, 
        or groups of file names. This is a more extreme example:
        
            ::
            
                @split("input.file", ['a*.bits', 'b*.pieces', 'somewhere_else/c*.stuff'])
                def split_function (input_filename, output_files):
                    "Code to split up 'input.file'"
                    


    The actual resulting files of this task function are not constrained by the file names
    in the *output* parameter of the function. The whole point of **@split** is that number 
    of resulting output files cannot be known beforehand, after all. 
    
******************
Example
******************

    
    Suppose random_numbers.list can be split into four pieces, this function will create
        ``1.chunks``, ``2.chunks``, ``3.chunks``, ``4.chunks``
        
    Subsequently, we receive a larger ``random_numbers.list`` which should be split into 10
    pieces. If the pipeline is called again, the task function receives the following parameters:
    
        ::
        
            step_4_split_numbers_into_chunks("random_numbers.list", 
                                             ["1.chunks",               #   previously created files
                                              "2.chunks",               #
                                              "3.chunks",               #
                                              "4.chunks" ])             #


    This doesn't stop the function from creating the extra ``5.chunks``, ``6.chunks`` etc.

    .. note::
    
        Any tasks **@follow**\ ing and specifying 
        ``step_4_split_numbers_into_chunks(...)`` as its *inputs* parameter is going to receive
        ``1.chunks``, ``...``, ``10.chunks`` and not merely the first four files.

        In other words, dependent / down-stream tasks which obtain output files automatically 
        from the task decorated by **@split** receive the most current file list. 
        The |glob|_ patterns will be matched again to see exactly what files the task function
        has created in reality *after* the task completes.

    


