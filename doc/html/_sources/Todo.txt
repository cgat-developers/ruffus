#######################
What is left to do:
#######################

    I would appreciated feedback and help on all these issues and where
    next to take *ruffus*. 

    Please write to me ( ruffus_lib at llew.org.uk)
    or join the project.
    

    Some of these proposals are well-fleshed-out:
    
    * :ref:`Clean up <todo-cleanup>` 
    * :ref:`(Plug-in) File Dependency Checking via MD5 or Databases <file-dependency-checking>`
    
    Others require some more user feedback about semantics:
    
    * :ref:`Combining output from multiple jobs automatically <todo-combining>`
    * :ref:`Harvesting return values from jobs <todo-return-values>`
    * :ref:`Linking the output from one task as the input to the next automatically <todo-dependencies>`
    
    Some issues are do-able but difficult and I don't have the experience:
    
    * :ref:`Run jobs on remote (clustered) processes via SGE/Hadoop <todo-multiprocessing>`


    
.. _todo-dependencies:

************************************************************************
Linking the output from one task as the input to the next automatically
************************************************************************

    For each task, we would have to log all the output files from each job, and
    use that as the input into the next stage.

    This is, after all, what make does. 
    
    Except that we would be creating the dependency tree on the fly.
    
    Syntactically, it would make things a bit easier for the user, with
    minor additions to the `@file` and `@file_re` syntax.
    
    



.. _todo-cleanup:

************************
Clean up
************************

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


        
    

.. _file-dependency-checking:

*********************************************************************
(Plug-in) File Dependency Checking via MD5 or Databases
*********************************************************************
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
    

************************
SQL hooks
************************
    See above.
    
    I have no experience with systems which link to SQL. What would people want from such a
    feature?

    Ian Holmes?
    

.. _todo-combining:

************************
Combining files
************************

    A common operation (See :ref:`intermediate example <intermediate-pipelines>` and
    :ref:`complicated example <complicated-pipelines>`) seems to be combining multiple
    input files into one or more output files (i.e. a "many->1" operation). 
    
    A the moment, this can be easily done by writing a simple parameter generating function
    with a glob (see :ref:`this code <intermediate-pipelines-combining_files>`.)
    
    However, we could directly support this in *ruffus* in two ways, both leveraging ``@files_re``.
    
    The idea is that input files to be grouped together should share similar
    traits identified by either a regular expression or a function.
    
    Suppose we had the following files::
    
        cows.mammals.animal
        horses.mammals.animal
        sheep.mammals.animal
        
        snake.reptile.animal
        lizard.reptile.animal
        crocodile.reptile.animal
        
        pufferfish.fish.animal
        
    and we wanted to end up with three different resulting output::
    
        cow.mammals.animal
        horse.mammals.animal
        sheep.mammals.animal
            -> mammals.results
        
        snake.reptile.animal
        lizard.reptile.animal
        crocodile.reptile.animal
            -> reptile.results
        
        pufferfish.fish.animal
            -> fish.results
    
    We could either add a "combining" regex parameter::
    
        # \1 = species [cow, horse]
        # \2 = phylogenetics group [mammals, reptile, fish]
        @files_re(  "*.animal", 
                    r"(.+)\.(.+)\.animal",        
                    combining(r"\2"),           # regular expression showing that 
                                                # "mammals/reptile" etc. groups files
                    r"\1.\2.animal",            # input file
                    r"\2.results")              # output file(s)
        def sort_animals_into_groups(species_file, result_file):
            " ... more code here"
            
    Or we could allow a grouping function like the *key* parameter 
    in `itertools.groupby <http://docs.python.org/library/itertools.html#itertools.groupby>`_::
    
        @files_re(  "*.animal", 
                    r"(.+)\.(.+)\.animal",        
                    combining_func(lambda x: x.split(".")[1]),
                    r"\1.\2.animal",            # input file
                    r"\2.results")              # output file(s)
        def sort_animals_into_groups(species_file, result_file):
            " ... more code here"
            
    In both cases, the extra parameter would be wrapped by a "tagging" class 
    (``combining`` and ``combining_func``) for clarity.
    
    Is this too much extra complexity for *ruffus* or ``@files_re`` to support? 
    
    Is the syntactic convenience worthwhile?
    
.. _todo-return-values:
    
************************
Return values
************************
    Is it a good idea to allow jobs to pass back calculated values?
    
    This requires trivial modifications to run_pooled_job_without_exceptions
    
    The user function cannot return `False`. That is reserved for signalling breaks.
    
    The most useful thing would be to associate job parameters with results.
    
    What should be the syntax for getting the results back?

.. _todo-multiprocessing:

************************************************************
Run jobs on remote (clustered) processes via SGE/Hadoop
************************************************************
    Can we run jobs on remote processes using SGE / Hadoop?
    
    Can we abstract all job management using drmaa?
    
    Python examples at http://gridengine.sunsource.net/howto/drmaa_python.html
    
=========
SGE
=========

    Look at Qmake execution model:


1)  SGE nodes are taken over completely
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
    
    
    
2)  Start a qrsh per job
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Advantages:
    
    * jobs look like any other SGE task

    Disadvantages:
    
    * Slower. Overheads might be high.
    * We might have to create a new pool per task
    * If we maintain an empty pool, and then dynamically attach processes,
      the code might be difficult to write (may not fit into the multiprocessing
      way of doing things / race-conditions etc.)
    
=========
Hadoop
=========

Can anyone help me with this / have any experience?

                                           


