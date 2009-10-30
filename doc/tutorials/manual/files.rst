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
    there will also be 5 separate jobs:
        ::

            from ruffus import *
            parameters = [
                                [ 'job1.file'           ],             # 1st job
                                [ 'job2.file', 4        ],             # 2st job
                                [ 'job3.file', [3, 2]   ],             # 3st job
                                [ 67, [13, 'job4.file']],             # 4st job
                                [ 'job5.file'           ],             # 5st job
                          ]
            @files(parameters)
            def task_file(*params):
                ""

    **Ruffus** creates as many jobs as there are elements in ``parameters``.
    Each element consist of another sequence of the actual parameters which will be
    passed to each job.
    
    Thus the above code is equivalent to calling:
        ::
             task_file('job1.file')
             task_file('job2.file', 4)
             task_file('job3.file', [3, 2])   
             task_file(67, [13, 'job4.file'])
             task_file('job5.file')
        
        
    What task_file does with these parameters is up to you!
    
    The only constraint on the parameters is that **Ruffus** will treat any first 
    parameter of each job as the ``input`` and any second as the ``output``. Any
    ``input`` or ``output`` parameters which are strings, or contain strings in
    any nested sequence will be treated as a file name.

    Thus in the job above:
        
        ::
        
             task_file(67, [13, 'job4.file'])
    
        | ``input`` == ``67``
        | ``output`` == ``[13, 'job4.file']``
        |
        |   The solitary output filename is ``job4.file``
        

=======================================
Skip jobs which are up to date
=======================================

    | Usually we do not want to run all the stages in a pipeline but only where
      the input data has changed or is no longer up to date.
    | One easy way to do this is to check the modification times for files produced
      at each stage of the pipeline.

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

            



