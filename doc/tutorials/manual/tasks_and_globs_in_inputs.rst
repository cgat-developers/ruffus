.. include:: ../../global.inc
.. include:: chapter_numbers.inc

.. _manual.tasks_and_globs_in_inputs:

#################################################################################################################
|manual.tasks_and_globs_in_inputs.chapter_num|: Chaining pipeline `Tasks` together automatically
#################################################################################################################
    * :ref:`Manual overview <manual>` 


    .. index:: 
        pair: tasks as recipes; Manual
    
    In the previous chapter, we explained that **ruffus** determines the data flow through
    your pipeline by calling your :term:`task` functions (normal python functions written 
    by you) with the right parameters at the right time, making sure that

        #. only out-of-date parts of the pipeline will be re-run
        #. multiple jobs can be run in parallel (on different processors if possible)
        #. pipeline stages can be chained together automatically
        
    This chapter is devoted to the last item: how the output of one stage of the pipeline 
    is piped into as the input of the next stage.
    
.. _manual.tasks_as_input:

.. index:: 
    pair: tasks; as input parameters (Manual)
    pair: tasks as input parameters; Manual
    pair: inputs parameters; tasks

    
   
==========================================================
Tasks in the *inputs* parameters: Implicit dependencies
==========================================================
    **Ruffus** treats the first two parameters of each job in each task as the *inputs* and
    *outputs* parameters respectively. If the *inputs* parameter contains strings, these 
    will be treated as the names of files required by that job. 

    If the *inputs* parameter contains any :term:`task`\ s, **Ruffus** will take the output
    from these specified tasks as part of the current *inputs* parameter. In addition, 
    such tasks will be listed as prequisites, much as if you had included them in a 
    separate ``@follows`` decorator.
    
    For example, supposed we wanted to take the output files from ``task1`` and feed
    them automatically to ``task2``, we might write the following code

        ::
        
            task1_ouput_files = ("task1.output_a", "task1.output_b", "task1.output_c")
    
            @follows(task1)
            @files(task1_ouput_files, "task2.output")
            def task2(input, output):
                pass



    This can be replaced by the much more concise syntax:

        ::
    
            @files(task1, "task2.output")
            def task2(input, output):
                pass
                        

    This means: 
        * Take the output from ``task1``, and feed it automatically into ``task2``. 
        * Also make sure that ``task2`` becomes a dependency of ``task1``.

            
    In other words, ``task1`` and ``task2`` have been chained together automatically.
    This is both a great convenience and makes the flow of data through a pipeline much clearer.
    
    

.. index:: 
    pair: tasks; refering to by name
    pair: inputs parameters; refering to tasks by name            

.. _manual.output_from:

==========================================================
Refering to tasks by name in the *inputs* parameters
==========================================================

    :ref:`Chapter 1 <manual.follows.out_of_order>` explains that task functions can be 
    defined in any order so long as undefined tasks are referred to by their (fully qualified if
    necessary) function name string.
    
    You can similarly refer to tasks in the *inputs* parameter by name, as a text string. 
    Normally **Ruffus** assumes that strings are file names. To indicate that that 
    you are referring to task function names instead, you need to
    wrap the relevant parameter or (nested) parts of the parameter with the indicator object
    :ref:`output_from("task_name") <decorators.output_from>`. Thus,
    
        ::
        
            @split(["a.file", ("b.file", output_from("task1", 76, "task2"))], "*.split")
            def task2(input, output):
                pass
                        

    is equivalent to:

        ::
        
            @split(["a.file", ("b.file", (task1, 76, task2))], "*.split")
            def task2(input, output):
                pass
    
.. index:: 
    pair: inputs parameters; globs
    pair: globs in input parameters; Manual

.. _manual.globs_as_input:

=======================================
Globs in the *inputs* parameters
=======================================

    As a syntactic convenience, **Ruffus** also allows you to specify a 
    |glob|_ pattern (e.g. ``*.txt``) in the
    *input* parameter, it will be expanded automatically to the actually matching 
    file names. This applies to any strings within *inputs* which contain the letters: ``*?[]``.
    
    
    
.. index:: 
    pair: tasks; combined with globs and files as input parameters (Manual)
    pair: tasks combined with globs and files as input parameters; Manual
    pair: globs; combined with tasks and files as input parameters (Manual)
    pair: globs combined with tasks and files as input parameters; Manual

    
.. _manual.mixing_tasks_globs_files:
    
=========================================================
Mixing globs, tasks and files as **inputs**
=========================================================

    **Ruffus** is very flexible in allowing you to mix 
    |glob|_ patterns, references to tasks and file names
    in the data structures you pass as the **inputs** parameters. 

    Suppose, in the previous example, 

        * that ``task1`` produces the files
            ::

            "task1.output_a"
            "task1.output_b"
            "task1.output_c"
            
        * that the following additional files are also present 
            ::

            "extra.a"
            "extra.c"

    Then,
    
        ::
    
            @files(["1_more.file", "2_more.file", task1, "extra.*"], "task2.output")
            def task2(input, output):
                pass
                

    would result in the combination of the specified file name, the expansion of the |glob|_, 
    and the results from the previous task:
    
        ::
    
            input == [
                        "1_more.file"   ,           # specified file
                        "2_more.file"   ,           # specified file
                        "task1.output_a",           # from previous task
                        "task1.output_b",           # from previous task 
                        "task1.output_c",           # from previous task 
                        "extra.a"       ,           # from glob expansion
                        "extra.c"       ,           # from glob expansion
                     ]
            

    In other words, |glob|_ patterns and tasks are expanded "in place" when they are part of
    python lists, sets, or tuples.
    
.. _manual.appending_tasks_globs_to_lists_sets_tuples:
    
===============================================================
Appending globs or tasks to pre-existing lists, sets or tuples
===============================================================

    Sometimes we want to the *inputs* parameter to contain be a combination of |glob|_\ s and tasks,
    and an existing list of file names.
    
    To elaborate on the above example, suppose we have a list of files:
    
        ::
        
            file_list = [   "1_more.file", 
                            "2_more.file"]
                            
    Now we want the input to ``task2`` to be:
    
        ::
        
            file_list + task1 + "extra.*"
            
    The closest that we can express this in python syntax is by turning task1 and the |glob|_
    to a list first then adding them together:
    
        ::
    
            @files(file_list + [task1] + ["extra.*"], "task2.output")
            def task2(input, output):
                pass
    

    The same also works with tuples:
    
        ::
    
            file_list = (   "1_more.file", 
                            "2_more.file")

            @files(file_list + (task1, "extra.*"), "task2.output")
            def task2(input, output):
                pass

    
    and sets (using the set concatenation operator):
        
        ::
    
            file_list = set([   "1_more.file", 
                                "2_more.file"])

            @files(file_list | set([task1 + "extra.*"]), "task2.output")
            def task2(input, output):
                pass

.. _manual.understanding_complex_inputs:

===============================================================
Understanding complex *inputs* and *outputs* parameters
===============================================================

    In all cases, **Ruffus** tries to do the right thing, and to make the simple or
    obvious case require the simplest, least onerous syntax.
    
    If sometimes **Ruffus** does not behave the way you expect, please write to the authors:
    it may be a bug!
    
    In all other cases, the best thing to do, is write your **Ruffus** specifications, and 
    check the results of :ref:`pipeline_printout <pipeline_functions.pipeline_printout>` 
    to make sure that your wishes are properly
    reflected in the parameters sent to your pipelined tasks.
    
    In other words, read the :ref:`next chapter <manual.tracing_pipeline_parameters>`!
    
