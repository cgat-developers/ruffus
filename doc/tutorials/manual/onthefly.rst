.. _manual_3rd_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run


###################################################################
Chapter 3: Passing parameters to the pipeline
###################################################################
.. hlist::
   * :ref:`Manual overview <manual>` 
   * :ref:`@files syntax in detail <decorators.files>`


    The easiest way to supply parameters to *Ruffus* |task|_ functions, to run
    as separate jobs, is to use the :ref:`@files <decorators.files>` decorator.
    
***************************************
**@files**
***************************************

    Quite simply, each parameter in @files will be sent to a separate job which 
    may run in parallel if necessary. For example, if a sequence
    (e.g. a list or tuple) of 5 parameters are passed to **@files**, that indicates
    there will also be 5 separate jobs.

=======================================
Skip jobs which are up to date
=======================================

    | Usually we do not want to run all the stages in a pipeline but only where
      the input data has changed or is no longer up to date.
    | One easy way to do this is to check the modification times for files produced
      at each stage of the pipeline.
    |
    | :ref:`@files <decorators.files>` defines the input and output files of a |job|_
      which will only be run if the input file has changed since the output file was produced.
    | *Ruffus* treats the first two parameters of each job as the input and output files
      and checks file/date timestamps for you.
    |
    | Let us first create our starting files ``a.1`` and ``b.1``
    | We can then run the following pipeline function to create
    
        * ``a.2`` from ``a.1`` and
        * ``b.2`` from ``b.1``
        
        ::
        
            # create starting files
            open("a.1", "w")
            open("b.1", "w")
            
        
            from ruffus import *
            parameters = [
                                [ 'a.1', 'a.2', 'A file'], # 1st job
                                [ 'b.1', 'b.2', 'B file'], # 2nd job
                          ]
            
            @files(parameters)
            def parallel_io_task(infile, outfile, text):
                # copy infile contents to outfile
                infile_text = open(infile).read()
                f = open(outfile, "w").write(infile_text + "\n" + text)
            
            pipeline_run()
       
        
    .. ???

    This produces the following output:
        ::
        
            >>> pipeline_run()
                Job = [a.1 -> a.2, A file] completed
                Job = [b.1 -> b.2, B file] completed
            Completed Task = parallel_io_task

        
    | If you called pipeline_run() again, nothing would happen because the files are up to date:
    | ``a.2`` is more recent than ``a.1`` and
    | ``b.2`` is more recent than ``b.1``
    
    However, if you subsequently modified ``a.1`` again:
        ::
        
            open("a.1", "w")
            pipeline_run(verbose = 1)
            
    you would see the following::
    
        >>> pipeline_run([parallel_io_task])
        Task = parallel_io_task
            Job = ["a.1" -> "a.2", "A file"] completed
            Job = ["b.1" -> "b.2", "B file"] unnecessary: already up to date
        Completed Task = parallel_io_task    
        
    The 2nd job is up to date and will be skipped.

.. index:: timestamp, resolution, precision


***********************************************
Short hand for simple tasks with single jobs
***********************************************

    If you are specifying the parameters for only one job, you can leave off the brackets,
    greatly improving clarity::
    
        from ruffus import *
        @files('a.1', ['a.2', 'b.2'], 'A file')
        def single_job_io_task(infile, outfile, text):
            pass
        
        pipeline_run()
        
        
    Produces:
        ::
        
            >>> pipeline_run()
                Job = [a.1 -> [a.2, b.2], A file] completed
            Completed Task = single_job_io_task

            

=====================
Multi Processing
=====================

    *Ruffus* uses python `multiprocessing <http://docs.python.org/library/multiprocessing.html>`_ to run
    each job in a separate process.
    
    This means that jobs do *not* necessarily complete in the order of the defined parameters.
    Task hierachies are, of course, inviolate: upstream tasks run before downstream, dependent tasks.
    
    The number of concurrent jobs can be set in |pipeline_run|_:

        ::
        
            pipeline_run([parallel_task], multiprocess = 5)
        
        
    if ``multiprocess`` is set to 1, then jobs will be run on a single process.


.. index:: 
    pair: dynamic;  parameters
    pair: on the fly; parameters

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



