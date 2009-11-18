.. _manual_2nd_chapter:


.. index:: 
    pair: tasks as recipes; Manual


###################################################################
**Chapter 2**: `Tasks and Recipes`
###################################################################
    * :ref:`Manual overview <manual>` 

    | The python functions which do the actual work of each stage  or
      :term:`task` of a **Ruffus** pipeline are written by you.
    | The role of **Ruffus** is to make sure these functions are called in the right order, 
      with the right parameters, running in parallel using multiprocessing if desired.

    **Ruffus** manages the data flowing through your pipeline by supplying the correct
    parameters to your pipeline functions. In this way, you will get the following features
    for free: 
    
        #. only out-of-date parts of the pipeline will be re-run
        #. multiple jobs can be run in parallel (on different processors if possible)
        #. pipeline stages can be chained together automatically
        
    Much of the functionality of **ruffus** involves determining the data flow through
    your pipeline, by governing how the output of one stage of the pipeline is supplied
    as parameters to the functions of the next.
    
.. index:: 
    pair: skip up-to-date; Manual


.. _manual.skip_up_to_date:

=======================================
Skip jobs which are up to date
=======================================

    Very often it will necessary to re-run a computational pipeline, because part of the 
    data has changed. **Ruffus** will run only those stages of the pipeline 
    which are absolutely necessary.
    
    By default, **Ruffus** uses file modification times to see which parts of the pipeline
    are out of date, and which :term:`task`\s need to be run again. This is so convenient that
    even if a pipeline is not file-based (if it, for example, uses database tables instead),
    it may be worth while to use dummy, "sentinel" files to manage the stages of a pipeline.

    (It is also possible, as we shall
    see later, to add custom functions to determine which parts of the pipeline are out
    of date. see :ref:`@parallel <decorators.parallel>` and 
    :ref:`@check_if_uptodate <decorators.check_if_uptodate>`.)
    
.. index:: 
    single: inputs / outputs parameters

.. _manual.io_parameters:

.. index:: 
    pair: inputs / outputs parameters; Manual

=================================
*Inputs* and *Outputs* parameters
=================================
    **Ruffus** treats the first two parameters of each job in each task as the *inputs* and
    *outputs* parameters respectively. If these parameters are strings, or are sequences
    which contain strings, these will be treated as the names of files required by and
    produced by that job. The presence and modification times of the *inputs* and *outputs* files 
    will be used to check if it is necessry to rerun the job.
    
    Apart from this, **Ruffus** imposes no other restrictions on the parameters for jobs, which
    are passed verbatim to task functions.
    
    Most of the time, it is sensible to stick with file names (strings) in the *inputs* and
    *outputs* parameters but **Ruffus** does not try to second-guess what sort of data you
    will be passing through your pipelines (except that strings represent file names). 

    Thus, given the following over-elaborate parameters (parameter passing will be discussed in 
    :ref:`chapter 4 <manual_4th_chapter>`):

        ::

            [   [[1, 3], "afile.name", ("bfile.name", 72)], 
                [[56, 3.3], set(custom_object(), "output.file")], 
                33.3, 
                "oops"]
            
    This will be passed `"as is"` to your task function:

        ::
        
            do_something([[1, 3], "afile.name", ("bfile.name", 72)],        # input
                        [[56, 3.3], set(custom_object(), "output.file")],   # output
                        33.3,                                               # extra parameter
                        "oops")                                             # extra parameter

            
        **Ruffus** will interprete this as:

        ::
        
            Input_parameter   = [[1, 3], "afile.name", ("bfile.name", 72)]
            Output_parameter  = [[56, 3.3], set(custom_object(), "output.file")]
            Other_parameter_1 = 33.3
            Other_parameter_2 = "oops"
            
        **Ruffus** disregards the *structure* of your data, only identifying the (nested) strings. 
        Thus there are 2 input files:

            ::
            
                "afile.name"
                "bfile.name"
                
        and 1 output file:

            ::
                
                "output.file"
            


.. index:: 
    pair: inputs parameters; tasks
    pair: inputs parameters; globs
            
.. index:: 
    pair: globs in input parameters; Manual

.. _manual.globs_as_input:

=======================================
Globs in the *inputs* parameters
=======================================

    If a `glob pattern <http://docs.python.org/library/glob.html>`_ is encountered (e.g. ``*.txt``) in an *input* parameter, it will be expanded
       automatically to the actually matching file names. This applies to any strings within
       *inputs* which contain the letters: ``*?[]``.
    
.. _manual.tasks_as_input:

.. index:: 
    pair: tasks; as input parameters (Manual)
    pair: tasks as input parameters; Manual

==========================================================
Tasks in the *inputs* parameters: Implicit dependencies
==========================================================
    If the *inputs* parameter contains any :term:`task`\ s, each of these will also be substituted by the *output* 
    generated by the specified task. In addition, such tasks will be listed as prequisites,
    much as if you had included them in a separate ``@follows`` decorator.
    
    For example, and without going too much syntactic detail (see :ref:`Chapter 4: @split <manual.split>`),

        the following concise syntax::
    
            @split(["*.bak", task1], "*.split")
            def task2(input, output):
                pass
                        

    Is equivalent to:

        ::
        
            current_bak_files = ("1.bak", "2.bak", "3.bak", "4.bak", "5.bak")
            task1_ouput_files = ("a.output", "b.output", "c.output")
    
            @follows(task1)
            @split([current_bak_files, task1_ouput_files], "*.split")
            def task2(input, output):
                pass
            
    This is both a great convenience and makes the flow of data through a pipeline much clearer.
    
.. _manual.output_from:
.. index:: 
    pair: output_from; Manual

==========================================================
Refering to tasks by name in the *inputs* parameters
==========================================================

    :ref:`Chapter 1 <manual.follows.out_of_order>` explains that task functions can be 
    defined in any order so long as undefined tasks are referred to by their (fully qualified if
    necessary) function name string.
    
    You can similarly refer to tasks in the *inputs* parameter by name. To tell **ruffus** that
    strings refer to task function names rather than file names, you need to
    wrap the relevant parameter or (nested) parts of the parameter with the indicator object
    :ref:`output_from("task_name") <decorators.output_from>`:
    
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
    pair: rules; for rerunning jobs
            
.. _manual.skip_up_to_date.rules:

=======================================
Checking if files are up to date
=======================================
    The following simple rules are used by **Ruffus**.
    
    #. The pipeline stage will be rerun if:
    
        * If any of the *inputs* files are new (newer than the *output* files)
        * If any of the *output* files are missing
        
    #. In addition, it is possible to run jobs which create files from scratch.
            
        * If no *inputs* file names are supplied, the job will only run if any *output* file is missing.
        
    #. Finally, if no *outputs* file names are supplied, the job will always run.
    
    
    The :ref:`example <manual.files.example>` in the next chapter shows how this works in practice.


.. index:: 
    pair: Exception; Missing input files 

=======================================
Missing files
=======================================

    If the *inputs* files for a job are missing, the task function will have no way
    to produce its *output*. In this case, a ``MissingInputFileError`` exception will be raised
    automatically. For example,
    
        ::
        
            task.MissingInputFileError: No way to run job: Input file ['a.1'] does not exist
            for Job = ["a.1" -> "a.2", "A file"]

.. index:: 
    single: Timestamp resolution

=======================================
Caveats: Timestamp resolution
=======================================

    | Note that modification times have precision to the nearest second under certain versions of Linux and
      Windows. This is especially true for networked file systems.
    | This may result in some jobs re-running even when
      they are up-to-date because the modification times appear to be identical (and **Ruffus**
      is very conservative).
    
    This is seldom a problem in real life code where pipeline stages rarely take < 1 second.
    *In extremis*, it may be necessary to add some calls to ``time.sleep(1)`` judiciously (as in
    some of the example here).


    Later versions of **Ruffus** will allow file modification times to be saved at higher precision
    in a log file or database to get around this.



