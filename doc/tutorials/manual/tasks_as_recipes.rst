.. _manual_2nd_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run


###################################################################
Chapter 2: Tasks and Recipes
###################################################################
    * :ref:`Manual overview <manual>` 

    *Ruffus* |task|_\ s are ordinary python functions. 

    Because of this, each |task|_ can represent not only a single action in a pipeline,
    but also a recipe or `rule <http://www.gnu.org/software/make/manual/make.html#Rule-Introduction>`_  
    which can be applied again and again to many different parameters.
    For example, one can have a *compile task*, a function which will compile any supplied 
    source code file, or a *count_lines task* which will count the number of lines in any file.
    
    |task|_\ s are thus a recipe for making specified files using supplied parameters.
    These files can be made in parallel, with each task function running as a separate |job|_.

.. _manual.skip_up_to_date:

=======================================
Skip jobs which are up to date
=======================================

    Very often it will necessary to re-run a computational pipeline, because part of the 
    data has changed. **Ruffus** will run only those stages of the pipeline 
    which are absolutely necessary.
    
    By default, **Ruffus** uses file modification times to see which parts of the pipeline
    are out of date, and which |task|_\s need to be run again. This is so convenient that
    even if a pipeline is not file-based (for example, using database tables instead),
    it may be worth while to use dummy, sentinel files to manage the stages of a pipeline.

    (It is also possible, as we shall
    see later, to add custom functions to determine which parts of the pipeline are out
    of date. see :ref:`@parallel <decorators.parallel>` and 
    :ref:`@check_if_uptodate <decorators.check_if_uptodate>`.)
    
.. index:: 
    single: input/output parameters

.. _manual.io_parameters:

=================================
Input and Output parameters
=================================
    **Ruffus** treats the first two parameters of each job in each task as the *input* and
    *output* parameters respectively. If these parameters are strings, or are sequences
    which contain strings, these will be treated as the names of files required by and
    produced by that job. The presence and modification times of the *input* and *output* files 
    will be used to check if it is necessry to rerun the job.
    
    Apart from this, **Ruffus** imposes no other restrictions on the parameters for jobs, which
    are passed verbatim to task functions.
    
    For example, given the following jobs parameters (parameter passing will be discussed in 
    :ref:`chapter 4 <manual_4th_chapter>`):

        ::

            [ [[1, 3], "afile.name", ("bfile.name", 72)], [[56, 3.3], set(custom_object(), "output.file")], 33.3, "oops"]
            
    This will be passed `"as is"` to your task function:

        ::
        
            do_something([[1, 3], "afile.name", ("bfile.name", 72)], 
                        [[56, 3.3], set(custom_object(), "output.file")], 
                        33.3, 
                        "oops")

            
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
    single: input parameters; tasks
    single: input parameters; globs
            
.. _manual.globs_as_input:

=======================================
Globs as input parameters
=======================================

    The decorators
       * :ref:`@split <decorators.split>`
       * :ref:`@transform <decorators.transform>`
       * :ref:`@merge <decorators.merge>`
       * :ref:`@collate <decorators.collate>`
       
    provide the greatest flexibility in the *input* parameter:
    
    If a ``glob`` specification is encountered (e.g. ``*.txt``), it will be expanded
       automatically to the actually matching file names. This applies to any strings within
       ``input`` which contain the letters: ``*?[]``.
    
.. _manual.tasks_as_input:

==========================================================
Implicit dependencies: Tasks as *input* parameters
==========================================================
    For the decorators
       * :ref:`@split <decorators.split>`
       * :ref:`@transform <decorators.transform>`
       * :ref:`@merge <decorators.merge>`
       * :ref:`@collate <decorators.collate>`
      
    if the *input* parameter contains any |task|_\ s, each of these will be substituted by the *output* 
    that the particular task has generated. In addition, such tasks will be listed as prequisites,
    much as if you had included them in a separate ``@follows`` decorator:
    
    For example, and without going too much syntactic detail (see :ref:`Chapter 4: @split <manual.split>`),

        the following::
    
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
            
    This is both a great convenience and makes the flow of execution in a pipeline much clearer.
    





.. index:: 
    single: rules; for rerunning jobs
            
.. _manual.skip_up_to_date.rules:

=======================================
Checking if files are up to date
=======================================
    The following simple rules are used by **Ruffus**.
    
    #. The pipeline stage will be rerun if:
    
        * If any of the input files are new (newer than the output files)
        * If any of the output files are missing
        
    #. In addition, it is possible to run jobs which create files from scratch.
            
        * If no input file names supplied, the job will only run if any output file is missing.
        
    #. Finally, if no output file names are supplied, the job will always run.
    
    
    The `example <manual.files.example>`_ in the next chapter shows how this works in practice.


.. index:: 
    single: Exception; Missing input files 

=======================================
Missing files
=======================================

    If the input files for a job are missing, the task function will have no way
    to produce its output. In this case, a ``MissingInputFileError`` exception will be raised
    automatically. For example,
    
        ::
        
            task.MissingInputFileError: No way to run job: Input file ['a.1'] does not exist
            for Job = ["a.1" -> "a.2", "A file"]

.. index:: 
    single: Timestamp resolution

=======================================
Caveats: Timestamp resolution
=======================================

    | Note that modification times have one second precision under certain versions of Linux and
      Windows, especially over the network. 
    | This may result in some jobs running even when
      they are up-to-date because the modification times appear to be identical.
    
    This is seldom a problem in real life code where pipeline stages rarely take < 1 second.
    *In extremis*, it may be necessary to add some calls to ``time.sleep(1)`` judiciously.      


    Later versions of **Ruffus** will allow file modification times to be saved at higher precision
    in a log file or database to get around this.



