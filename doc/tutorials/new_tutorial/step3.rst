.. include:: ../../global.inc
.. _New_Tutorial_3rd_step:

.. index::
    pair: @transform; Tutorial

######################################################################################################################################
New Tutorial in revision Step 3: More on ``@transform``-ing data
######################################################################################################################################

   * :ref:`New tutorial overview <New_Tutorial>`
   * :ref:`@transform syntax in detail <decorators.transform>`

.. note::

    Remember to look at the example code:

    * :ref:`Python Code for step 3 <New_Tutorial_3rd_step_code>`

***************************************
Review
***************************************
    .. image:: ../../images/theoretical_pipeline_schematic.png
       :scale: 50

    Computational pipelines transform your data in stages until the final result is produced.
    Ruffus automates the plumbing in your pipeline. You supply the python functions which perform the data transformation,
    and tell Ruffus how these pipeline stages or :term:`task` functions are connected together.

    .. note::

        **The best way to design a pipeline is to:**

            * **write down the file names of the data as it flows across your pipeline**
            * **write down the names of functions which transforms the data at each stage of the pipeline.**


    By letting **Ruffus** manage your pipeline parameters, you will get the following features
    for free:

        #. only out-of-date parts of the pipeline will be re-run
        #. multiple jobs can be run in parallel (on different processors if possible)
        #. pipeline stages can be chained together automatically




************************************
Running pipelines in parallel
************************************


    The example pipeline from the previous chapter involved processing three *independent* sets of files.

    ::

        from ruffus import *

        # create initial files
        first_task_params = [   ['job1.a.start', 'job1.b.start'],
                                ['job2.a.start', 'job2.b.start'],
                                ['job3.a.start', 'job3.b.start']    ]
        for input_file_pairs in first_task_params:
            for input_file in input_file_pairs:
                open(input_file, "w")


        #---------------------------------------------------------------
        #   first task
        @transform(first_task_params, suffix(".start"), ".output.1")
        def first_task(input_files, output_file):
            with open(output_file, "w"): pass


        #---------------------------------------------------------------
        #   second task
        @transform(first_task, suffix(".output.1"), ".output.2")
        def second_task(input_files, output_file):
            with open(output_file, "w"): pass

        #
        #       Run
        #
        pipeline_run([second_task])



    Though, three jobs have been specified in parallel, **Ruffus** defaults to running
    each of them successively. With modern CPUs, it is often a lot faster to run parts
    of your pipeline in parallel, all at the same time.

    To do this, all you have to do is to add a multiprocess parameter to ``pipeline_run``:

        ::

            >>> pipeline_run([second_task], multiprocess = 5)

    In this case, we are telling ruffus to run a maximum of 5 jobs at the same time. Since we only have
    three sets of data, that is as much parallelism as we are going to get...



**************************************************
Up-to-date jobs are not re-run unnecessarily
**************************************************

    A job will be run only if the output file timestamps are out of date.
    If you ran the same code a second time, nothing would happen because all the work is already complete.

    We can check the details by asking *Ruffus* for more ``verbose`` output

        ::

            >>> pipeline_run([second_task], verbose = 4)
              Task = first_task
                All jobs up to date
              Task = second_task
                All jobs up to date


    Nothing happens because:
        * ``job1.a.output.2`` is more recent than ``job1.a.output.1`` and
        * ``job2.a.output.2`` is more recent than ``job2.a.output.1`` and
        * ``job3.a.output.2`` is more recent than ``job3.a.output.1``.

    and so on...


    Let us see what happens if we recreated the file ``job1.a.start`` so that it appears as if (1 out of 3) a files is out of date
        ::

            open("job1.a.start", "w")
            pipeline_run([second_task], multiprocess = 5)


    Only the out of date jobs (highlighted) are re-run:

        .. code-block:: python
           :emphasize-lines: 4,8

            >>> pipeline_run([second_task], multiprocess = 5, verbose = 2)
                Job  = [[job2.a.start, job2.b.start] -> job2.a.output.1] unnecessary: already up to date
                Job  = [[job3.a.start, job3.b.start] -> job3.a.output.1] unnecessary: already up to date
                Job  = [[job1.a.start, job1.b.start] -> job1.a.output.1] completed
            Completed Task = first_task
                Job  = [job2.a.output.1 -> job2.a.output.2] unnecessary: already up to date
                Job  = [job3.a.output.1 -> job3.a.output.2] unnecessary: already up to date
                Job  = [job1.a.output.1 -> job1.a.output.2] completed
            Completed Task = second_task



.. index::
    pair: input / output parameters; Tutorial

***************************************
Intermediate files
***************************************

    In the above examples, the *input* and *output* parameters are file names.
    Ruffus was designed for pipelines which save intermediate data in files. This is not
    compulsory but saving your data in files at each step provides many advantages:

        #) Ruffus can use file system time stamps to check if your pipeline is up to date
        #) Your data is persistent across runs
        #) This is a good way to pass large amounts of data across processes and computational nodes

    Otherwise, task parameters could be all sorts of data, from lists of files, to numbers,
    sets or tuples. Ruffus imposes few constraints on what *you*
    would like to send to each stage of your pipeline.

    **Ruffus** does, however, assume that all strings in your *input* and *output*
    parameters represent file names.

    *input* parameters which contains a |glob|_ pattern (e.g. ``*.txt``) are expanded to the matching file names.


**********************************************
Simplifying our example with ``@originate``
**********************************************

    Our previous pipeline example started off with a set of files which we had to create first.

    This is a common task: pipelines have to start *somewhere*.

    Ideally, though, we would only want to create these starting files if they didn't already exist. In other words, we want a sort of ``@transform`` which makes files from nothing (``None``?).

    This is exactly what ``@originate`` helps you to do.

    Rewriting our pipeline with ``@originate`` gives the following three steps:


    ::

        from ruffus import *

        #---------------------------------------------------------------
        #   create initial files
        #
        @originate([   ['job1.a.start', 'job1.b.start'],
                       ['job2.a.start', 'job2.b.start'],
                       ['job3.a.start', 'job3.b.start']    ])
        def create_initial_file_pairs(output_files):
            # create both files as necessary
            for output_file in output_files:
                with open(output_file, "w") as oo: pass

        #---------------------------------------------------------------
        #   first task
        @transform(create_initial_file_pairs, suffix(".start"), ".output.1")
        def first_task(input_files, output_file):
            with open(output_file, "w"): pass


        #---------------------------------------------------------------
        #   second task
        @transform(first_task, suffix(".output.1"), ".output.2")
        def second_task(input_files, output_file):
            with open(output_file, "w"): pass

        #
        #       Run
        #
        pipeline_run([second_task])



    ::

            Job  = [None -> [job1.a.start, job1.b.start]] completed
            Job  = [None -> [job2.a.start, job2.b.start]] completed
            Job  = [None -> [job3.a.start, job3.b.start]] completed
        Completed Task = create_initial_file_pairs
            Job  = [[job1.a.start, job1.b.start] -> job1.a.output.1] completed
            Job  = [[job2.a.start, job2.b.start] -> job2.a.output.1] completed
            Job  = [[job3.a.start, job3.b.start] -> job3.a.output.1] completed
        Completed Task = first_task
            Job  = [job1.a.output.1 -> job1.a.output.2] completed
            Job  = [job2.a.output.1 -> job2.a.output.2] completed
            Job  = [job3.a.output.1 -> job3.a.output.2] completed
        Completed Task = second_task



