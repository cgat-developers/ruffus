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
.. hlist::
   * :ref:`Manual overview <manual>` 

    *Ruffus* |task|_\ s are ordinary python functions. 

    Because of this, each |task|_ can represent not only a single action in a pipeline,
    but also a recipe or `rule <http://www.gnu.org/software/make/manual/make.html#Rule-Introduction>`_  
    which can be applied again and again to many different parameters.
    
    For example, one can have a *compile task*, a function which will compile any supplied 
    source code file, or a *count_lines task* which will count the number of lines in any file.
    
    |task|_\ s are thus a recipe for making specified files using supplied parameters.
    These files can be made in parallel, with each task function running as a separate |job|_.

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
    

=================================
Input and Output parameters
=================================
    **Ruffus** treats the first two parameters of each job wi[[1, 3], "afile.name", ("bfile.name", 72)]thin each task as the *input* and
    *output* parameters respectively. If these parameters are strings, or are sequences
    which contain strings, these will be treated as the names of files required by and
    produced by that job. The presence and modification times of the input and output files 
    will be used to check if it is necessry to rerun the job.
    
    Apart from this, **Ruffus** imposes no other restrictions on the parameters for jobs, which
    are passed verbatim to task functions.
    
    For example, given the following jobs parameters:
        ::

            [ [[1, 3], "afile.name", ("bfile.name", 72)], [[56, 3.3], set(custom_object(), "output.file")], 33.3, "oops"]
            
        **Ruffus** will interprete this as:
        ::
        
            Input parameter = [[1, 3], "afile.name", ("bfile.name", 72)]
            Output parameter= [[56, 3.3], set(custom_object(), "output.file")]
            Other parameter #1 = 33.3
            Other parameter #2 = "oops"
            
        The actual data structures do not matter but **Ruffus** will identify 2 input files:
        ::
        
            "afile.name"
            "bfile.name"
            
        and 1 output file:
        ::
            
            "output.file"
            

=======================================
Checking if files are up to date
=======================================
    The following simple rules are used by **Ruffus**:
    
    The pipeline stage will be rerun if:
    
        * If any of the input files are new (newer than the output files)
        * If any of the output files are missing
        
    In addition, it is possible to run jobs which create files from scratch.
            
        * If no input file names supplied, the job will only run if any output file is missing.
        
    Finally, if no output file names are supplied, the job will always run.
    

=======================================
Missing files
=======================================

    If the input files for a job are missing, the task function will have no way
    to produce its output. In this case, a ``MissingInputFileError`` exception will be raised
    automatically. For example,
        ::
        
            task.MissingInputFileError: No way to run job: Input file ['a.1'] does not exist
            for Job = ["a.1" -> "a.2", "A file"]

=======================================
Caveats: Timestamp resolution
=======================================

    | Note that modification times have one second precision under certain versions of Linux and
      Windows, especially over the network. 
    | This may result in some jobs running even when
      they are up-to-date because the modification times appear to be identical.

    Later versions of **Ruffus** will allow file modification times to be saved at higher precision
    in a log file or database to get around this.


=====================
Multi Processing
=====================

    *Ruffus* uses python `multiprocessing <http://docs.python.org/library/multiprocessing.html>`_ to run
    each job in a separate process.
    
    This means that jobs do *not* necessarily complete in the order of the defined parameters.
    Task hierachies are, of course, inviolate: upstream tasks run before downstream, dependent tasks.
    
    Tasks that are independent (i.e. do not precede each other) may be run in parallel as well.
    
    The number of concurrent jobs can be set in |pipeline_run|_:

        ::
        
            pipeline_run([parallel_task], multiprocess = 5)
        
        
    If ``multiprocess`` is set to 1, then jobs will be run on a single process.

    
=====================
Data sharing
=====================
    
    Running jobs in separate processes allows *Ruffus* to make full use of the multiple
    processors in modern computers. However, some of the 
    `multiprocessing guidelines <http://docs.python.org/library/multiprocessing.html#multiprocessing-programming>`_
    should be borne in mind when writing *Ruffus* pipelines. In particular:
    
    * Try not to pass large amounts of data between jobs, or at least be aware that this has to be marshalled
      across process boundaries.
      
    * Only data which can be `pickled <http://docs.python.org/library/pickle.html>`_ can be passed as 
      parameters to *Ruffus* task functions. Happily, that applies to almost any Python data type.
      The use of the rare, unpicklable object will cause python to complain (fail) loudly when *Ruffus* pipelines
      are run.
      

