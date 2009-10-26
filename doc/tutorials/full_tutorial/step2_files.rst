.. _Full_Tutorial_2nd_step:


###################################################################
Step 2: Passing parameters to the pipeline
###################################################################
* :ref:`Up <Full_Tutorial>` 
* :ref:`Prev <Full_Tutorial_1st_step>` 
* :ref:`Next <Full_Tutorial_3rd_step>` 
* :ref:`@files <task.files>` syntax in detail


***************************************
**@files**
***************************************

=======================================
Skip jobs which are up to date
=======================================

    Usually it will not be necessary to run all the tasks in a pipeline but only where
    the input data has changed or the task is no longer up to date.
    
    One easy way to do this is to check the modification times for the input
    and output files of a job. The job will only be rerun if the input file has changed
    since the output file was produced.
    
    *Ruffus* treats the first two parameters of each job as the input and output files
    and checks timestamps for you.
    
    From the command prompt, make our starting files::
    
        > echo "start 1" > a.1
        > echo "start 2" > a.2
    
        
        
    .. ???

    Then run the following python code::
    
        from ruffus import *
        parameters = [
                            [ 'a.1', 'a.2', 'A file'], # 1st job
                            [ 'b.1', 'b.2', 'B file'], # 2nd job
                      ]
        
        @files(parameters)
        def parallel_io_task(infile, outfile, text):
            infile_text = open(infile).read()
            f = open(outfile, "w").write(infile_text + "\n" + text)
        
        pipeline_run([parallel_io_task])
       
        
    .. ???

    Gives::
        
        Task = parallel_io_task
            Job = ["a.1" -> "a.2", "A file"] completed
            Job = ["b.1" -> "b.2", "B file"] completed
    
        
    .. ???

    If you ran the same code a second time, nothing would happen because 
    ``a.2`` is more recent than ``a.1`` and
    ``b.2`` is more recent than ``b.1`` .
    
    However, if you subsequently modified ``a.1`` again::
    
        > echo touch a.1
        
        
    .. ???

    You would see the following::
    
        >>> pipeline_run([parallel_io_task])
        Task = parallel_io_task
            Job = ["a.1" -> "a.2", "A file"] completed
            Job = ["b.1" -> "b.2", "B file"] unnecessary: already up to date
    
        
    .. ???

    The 2nd job is up to date and will be skipped.

.. index:: timestamp, resolution, precision

.. ???

=======================================
Caveats: Timestamp resolution
=======================================

    Note that modification times have one second precision under certain versions of Linux and
    Windows, especially over the network. This may result in some jobs running even when
    they are up-to-date because the modification times appear to be identical.

=======================================
Input/Output **@files**
=======================================
    The input and output files for each job can be 
        * A single file name
        * A list of files
        * ``None``
    
    If the input file is ``None``, the job will run if any output file is missing.
    
    If the output file is ``None``, the job will always run.
    
    If any of the output files is missing, the job will run.
    
    If any of the input files is missing when the job is run, a
    ``MissingInputFileError`` exception will be raised, For example,
    ::
    
        task.MissingInputFileError: No way to run job: Input file ['a.1'] does not exist
        for Job = ["a.1" -> "a.2", "A file"]
    
        
.. ???

    

***********************************************
Short hand for simple tasks with single jobs
***********************************************

    If you are specifying the parameters for only one job, you can leave off the brackets,
    greatly improving clarity::
    
        from ruffus import *
        @files('a.1', ['a.2', 'b.2'], 'A file')
        def single_job_io_task(infile, outfile, text):
            infile_text = open(infile).read()
            f = open(outfile, "w").write(infile_text + "\n" + text)
        
        pipeline_run([parallel_io_task])
        
        
    .. ???

    Produces::
    
        Task = single_job_io_task
            Job = ["a.1" -> ["a.2", "b.2"], "A file"] completed
            
.. ???



=====================
Multi Processing
=====================

    *Ruffus* uses python `multiprocessing <http://docs.python.org/library/multiprocessing.html>`_ to run
    each job in a separate process.
    
    This means that jobs do *not* necessarily complete in the order of the defined parameters.
    Task hierachies are, of course, inviolate: upstream tasks run before downstream, dependent tasks.
    
    The number of concurrent jobs can be set in ``pipeline_run``::
    
        pipeline_run([parallel_task], multiprocess = 5)
        
        
    .. ???

    if ``multiprocess`` is set to 1, then jobs will be run on a single process.

.. index:: errors, exceptions

.. ???

.. _exceptions:


.. index:: 
    pair: dynamic;  parameters
    pair: on the fly; parameters

.. ???

.. _on_the_fly:
    
=======================================
Generating parameters on the fly
=======================================

    The above examples assume you know the parameters each job takes beforehand.
    Sometimes, it is necessary, or perhaps more convenient, to generate parameters on the fly or
    at runtime.
    
    All this requires is a function which generate one list (or any sequence) of
    parameters per job. For example::
    
        from ruffus import *
        def generate_parameters_on_the_fly():
            """
            returns one list of parameters per job
            """
            parameters = [
                                ['A', 1, 2], # 1st job
                                ['B', 3, 4], # 2nd job
                                ['C', 5, 6], # 3rd job
                            ]
            for job_parameters in parameters:
                yield job_parameters
        
        @parallel(generate_parameters_on_the_fly)
        def parallel_task(name, param1, param2):
            sys.stderr.write("    Parallel task %s: " % name)
            sys.stderr.write("%d + %d = %d\n" % (param1, param2, param1 + param2))
        
        pipeline_run([parallel_task])
        
        
    .. ???

    Similarly produces::
   
        Task = parallel_task
            Parallel task A: 1 + 2 = 3
            Job = ["A", 1, 2] completed
            Parallel task B: 3 + 4 = 7
            Job = ["B", 3, 4] completed
            Parallel task C: 5 + 6 = 11
            Job = ["C", 5, 6] completed
    
        
    .. ???

    
    The parameters often need to be generated more than once (see 
    :ref:`below <checking-multiple-times>`).



