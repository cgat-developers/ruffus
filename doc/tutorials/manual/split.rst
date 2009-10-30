.. _manual_5th_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run

###################################################################
Chapter 5: Splitting up large tasks / files
###################################################################
    .. hlist::
    
        * :ref:`Manual overview <manual>` 
        * :ref:`@split <decorators.split>` syntax in detail

    A common requirement in computational pipelines is to split up a large task into
    small jobs which can be run on different processors, (or sent to a computational
    cluster). Very often, the number of jobs depends dynamically on the size of the
    task, and cannot be known for sure beforehand. 

    *Ruffus* uses the :ref:`@split <decorators.split>` decorator to indicate that
    the |task|_ functions produces an indeterminate number of output files.
    
    
    
.. index:: 
    single: @split; Manual
    
.. _manual.split:

=================
**@split**
=================
This example is from :ref:`step 4 <Simple_Tutorial_4th_step>` of the simple tutorial.


**************************************************************************************
Remember to look at the example code:
**************************************************************************************
* :ref:`Python Code for Simple Tutorial step 4 <Simple_Tutorial_4th_step_code>` 
    
**************************************************************************************
Splitting up a long list of random numbers to calculate their variance
**************************************************************************************

    Suppose we had a list of 100,000 random numbers:

        ::
        
            import random
            f = open(output_file_name, "w")
            for i in range(NUMBER_OF_RANDOMS):
                f.write("%g\n" % (random.random() * 100.0))

    
    We might want to calculate the sample variance for these numbers more quickly by splitting them 
    into ``NNN`` parcels of 1000 numbers each and working on them in parallel. 
    In this case we known that ``NNN`` == ``100`` but usually the number of resulting files
    is only apparent after we have finished processing the starting file.
    
    This is step 4 from:
    
    .. image:: ../../images/simple_tutorial_step4.png
        :scale: 50
       

    The code for this is easy to write because of the *Ruffus* decorator :ref:`@split<decorators.split>` which is
    designed to specifically for splitting up input into an indeterminate ``NNN`` number of 
    output files:
    
        ::
        
            @split("random_numbers.list", "*.chunks")
            def step_4_split_numbers_into_chunks (input_file_name, output_files):
                #
                """code goes here"""
            

    ``input_file_name`` will be set to the starting file, in this case, ``random_numbers.list``.
    
.. _manual.split.output_files:

=================
Output files
=================

    The second, ``output`` parameter of **@split** usually contains a glob specification like
    the ``*.chunks`` above. 

    .. note::
        **Ruffus** is quite relaxed about the contents of the ``output`` parameter.
        Strings are treated as file names. Strings containing glob specifications are expanded.
        Other types are passed verbatim to the decorated task function.
    
    The files which match the glob specification will be passed as the actual parameters to the job
    function. These lists of files do not in any way constrain the number of files you actually 
    want to produce. The contents of ``output`` are unknown, beforehand, after all. Otherwise,
    you could just use :ref:`@files <manual.files>`!
    
    Thus in the above example, the first time you run ``step_4_split_numbers_into_chunks``, no ``*.chunks``
    files will have been created so the task function receives the following parameters:
    
        ::
        
            step_4_split_numbers_into_chunks("random_numbers.list", [])
            
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

    This list of existing files may be useful for cleaning up detritus from previous runs 
    (have a look at :ref:`step_4_split_numbers_into_chunks(...) <Simple_Tutorial_4th_step_code>`).
    In some cases, existing files may be out of date or superfluous but you are free to retain
    them if necessary.    

    .. note::
        Any tasks **@follow**\ ing and specifying 
        ``step_4_split_numbers_into_chunks(...)`` as its *input* parameter is going to receive
        ``1.chunks``, ``...``, ``10.chunks`` and not merely the first four files.

        In other words, Dependent / down stream tasks which obtain output files automatically from the task decorated by @split
        receive the most current file list. The glob specifications will be matched again to see exactly what files the task function
        has created in reality *after* it runs.

    


