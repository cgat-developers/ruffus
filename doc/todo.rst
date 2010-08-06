.. include:: global.inc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Future plans for *Ruffus*:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. _todo.update_documentation:

###################################
Update documentation
###################################
    There have been major changes in Ruffus and not all of the documentation has caught up yet.
    This will be the top priority.

    Outstand topics are:

    * Add Manual Chapter for using **@split** with **regex** and **add_inputs** 
        see :ref:`@split syntax <decorators.split_ex>`
    * Update collate to include **add_inputs** 
    * Add Manual Chapter on "best practices" in constructing pipelines
    * Revise chapter on :ref:`Design and Architecture <design.file_based_pipelines>`



^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Completed already:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _todo.dependencies:
.. _todo.combining:

    Theses were previous "Future plan" items

    * Linking the output from one task as the input to the next automatically*
        See :ref:`split <decorators.split>`, :ref:`transform <decorators.transform>` or :ref:`merge <decorators.merge>`
    * Combining files*
        See :ref:`merge <decorators.merge>`

    

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Left to do:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    I would appreciated feedback and help on all these issues and where
    next to take *ruffus*. 

    Please write to me ( ruffus_lib at llew.org.uk)
    or join the project.
    

    Some of these proposals are well-fleshed-out:
    
    * :ref:`Clean up <todo-cleanup>` 
    * :ref:`(Plug-in) File Dependency Checking via MD5 or Databases <file-dependency-checking>`
    
    Others require some more user feedback about semantics:
    
    * :ref:`Harvesting return values from jobs <todo-return-values>`
    
    Some issues are do-able but difficult and I don't have the experience:
    
    * :ref:`Run jobs on remote (clustered) processes via SGE/Hadoop <todo-multiprocessing>`


    
.. _todo.multiple_exception:
###################################
Exceptions
###################################

.. _manual.exceptions.multiple_errors:

    The current behaviour is to continue executing all the jobs currently in progress
    when an exception is thrown (See the :ref:`manual <manual.exceptions.multiple_errors>`).

    A.H. has suggested that

        * Exceptions should be displayed early
        * Ctrl-C should not leave dangling jobs
        * As an option, Ruffus should try to keep running as far as possible (i.e. ignoring downstream tasks)


.. _todo.cleanup:

###################################
Clean up
###################################

    The plan is to store the files and directories created via
    a standard interface.
    
    The placeholders for this are a function call ``register_cleanup``.
    
    Jobs can specify the files they created and which need to be
    deleted by returning a list of file names from the job function.
    
    So::
    
        raise Exception = Error
        
        return False = halt pipeline now
        
        return string / list of strings = cleanup files/directories later
        
        return anything else = ignored
        
    
    The cleanup file/directory store interface can be connected to
    a text file or a database.
    
    The cleanup function would look like this::
    
        pipeline_cleanup(cleanup_log("../cleanup.log"), [instance ="october19th" ])
        pipeline_cleanup(cleanup_msql_db("user", "password", "hash_record_table"))
        
    The parameters for where and how to store the list of created files could be
    similarly passed to pipeline_run as an extra parameter::

        pipeline_run(cleanup_log("../cleanup.log"), [instance ="october19th" ]) 
        pipeline_run(cleanup_msql_db("user", "password", "hash_record_table")) 
        
    where `cleanup_log` and `cleanup_msql_db` are classes which have functions for

        #) storing file
        #) retrieving file
        #) clearing entries
        
    
    * Files would be deleted in reverse order, and directories after files.
    * By default, only empty directories would be removed. 
    
      But this could be changed with a ``--forced_remove_dir`` option 
      
    * An ``--remove_empty_parent_directories`` option would be 
      supported by `os.removedirs(path) <http://docs.python.org/library/os.html#os.removedirs>`_.


        
    

.. _file.dependency_checking:

######################################################################
(Plug-in) File Dependency Checking via MD5 or Databases
######################################################################
    So that MD5 / a database can be used instead of coarse-grained file modification times.
    
    As always, the design is a compromise between flexibility and easy of use.
    
    The user can already write their own file dependency checking function and
    supply this::
    
        @check_if_uptodate(check_md5_func)
        @files(io_files)
        def task_func (input_file, output_file):
            pass
    
    The question is can we 
    
        #) supply a check_md5() function
        #) allow the whole pipeline to use this.
        
    Most probably we need an extra parameter somewhere::
    
        pipeline_run(md5_hash_database = "current/location/files.md5")
        
    There is prior art on this in ``scons``.
    

    If we use a custom object/function, can we use orthogonal syntax for 

    #) disk modifications times,
    #) md5 hashes saved to a file,
    #) md5 hashes saved to a database?
    
    ::

        pipeline_run(file_up_to_date_lookup = md5_hash_file("current/location/files.md5"))
        pipeline_run(file_up_to_date_lookup = mysql_hash_store("user", "password", "hash_record_table"))
        
    where ``md5_hash_file`` and ``mysql_hash_store`` are objects which have
    get/set functions for looking up modification times from file names.
    
    Of course that allows you to fake the whole process and not even use real files...
    
    
.. _todo.intermediate:

######################################################################
Remove intermediate files
######################################################################

    Often large intermediate files are produced in the middle of a pipeline which could be
    removed. However, their absence would cause the pipeline to appear out of date. What is
    the best way to solve this?

    In gmake, all intermediate files which are not marked ``.PRECIOUS`` are deleted.

    We do not want to manually mark intermediate files for several reasons:
        * The syntax would be horrible and clunky
        * The gmake distinction between ``implicit`` and ``explicit`` rules is not one we
          would like to impose on Ruffus
        * Gmake uses statically determined (DAG) dependency trees so it is quite natural and
          easy to prune intermediate paths

    Our preferred solution should impose little to no semantic load on Ruffus, i.e. it should
    not make it more complex / difficult to use. There are several alternatives we are 
    considering:

        #) Have an **update** mode in which pipeline_run would ignore missing files and only run tasks with existing, out-of-date files.
        #) Optionally ignore all out-of-date dependencies beyond a specified point in the pipeline
        #) Add a decorator to flag sections of the pipeline where intermediate files can be removed


    Option (1) is rather unnerving because it makes inadvertent errors difficult to detect.

    Option (2) involves relying on the user of a script to remember the corect chain of dependencies in
    often complicated pipelines. It would be advised to keep a flowchart to hand. Again,
    the chances of error are much greater.

    Option (3) springs from the observation by Andreas Heger that parts of a pipeline with 
    disposable intermediate files can usually be encapsulated as an autonomous section.
    Within this subpipeline, all is well provided that the outputs of the last task are complete
    and up-to-date with reference to the inputs of the first task. Intermediate files
    could be removed with impunity.

    The suggestion is that these autonomous subpipelines could be marked out using the Ruffus
    decorator syntax::
    
        #
        #   First task in autonomous subpipeline 
        #
        @files("who.isit", "its.me")
        def first_task(*args):
            pass

        #   
        #   Several intermediate tasks
        #
        @transform(subpipeline_task1, suffix(".me"), ".her")
        def task2_etc(*args):
           pass

        #   
        #   Final task
        #
        @sub_pipeline(subpipeline_task1)
        @transform(subpipeline_task1, suffix(".her"), ".you")
        def final_task(*args):
           pass

    **@sub_pipeline** marks out all tasks between ``first_task`` and ``final_task`` and
    intermediate files such as ``"its.me"``, ``"its.her`` can be deleted. The pipeline will
    only run if ``"its.you"`` is missing or out-of-date compared with ``"who.isit"``.

    Over the next few Ruffus releases we will see if this is a good design, and whether
    better keyword can be found than **@sub_pipeline** (candidates include **@shortcut**
    and **@intermediate**)



.. _todo.pre_post_job:
    
######################################################################
Extra signalling before and after each task and job
######################################################################
    @pretask(custom_func)
    @prejob(custom_func)
    @postjob(custom_func)
    
    @pretask would be run in the master process while @prejob / @postjob would be run
    in the child processes (if any).


######################################################################
SQL hooks
######################################################################
    See above.
    
    I have no experience with systems which link to SQL. What would people want from such a
    feature?

    Ian Holmes?
    
    
.. _todo.return_values:
    
######################################################################
Return values
######################################################################
    Is it a good idea to allow jobs to pass back calculated values?
    
    This requires trivial modifications to run_pooled_job_without_exceptions
    
    The most useful thing would be to associate job parameters with results.
    
    What should be the syntax for getting the results back?

.. _todo.hadoop:

######################################################################
Run jobs on remote (clustered) processes via SGE/Hadoop
######################################################################
    Can we run jobs on remote processes using SGE / Hadoop?
    
    Can we abstract all job management using drmaa?
    
    Python examples at http://gridengine.sunsource.net/howto/drmaa_python.html
    
***************
SGE
***************
    Look at Qmake execution model:


===================================================
1)  SGE nodes are taken over completely
===================================================

    See last example in `multiprocessing <http://docs.python.org/library/multiprocessing.html#examples>`_
    for creating a distributed queue.
    
    We would use qrsh instead of ssh. The size of the pool would be the (maximum) number of jobs
    
    Advantages:

    * Simple to implement
    * Efficient

    Disadvantages:

    * Other users might not appreciate having python jobs taking over the nodes for a 
      protracted length of time
    * We would not be able to use SGE to view / manage jobs
    
    
    
===================================================
2)  Start a qrsh per job
===================================================

    Advantages:
    
    * jobs look like any other SGE task

    Disadvantages:
    
    * Slower. Overheads might be high.
    * We might have to create a new pool per task
    * If we maintain an empty pool, and then dynamically attach processes,
      the code might be difficult to write (may not fit into the multiprocessing
      way of doing things / race-conditions etc.)
    
***************
Hadoop
***************
Can anyone help me with this / have any experience?

                                           


