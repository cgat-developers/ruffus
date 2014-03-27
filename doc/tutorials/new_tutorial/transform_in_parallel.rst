.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: transforming in parallel; Tutorial

.. _new_manual.transform_in_parallel:

######################################################################################################
|new_manual.transform_in_parallel.chapter_num|: More on ``@transform``-ing data
######################################################################################################


.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@transform syntax in detail <decorators.transform>`

.. note::

    Remember to look at the example code:

    * :ref:`new_manual.transform_in_parallel.code`

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



.. index::
    pair: one to one @transform; Tutorial

***************************************
@transform is a 1 to 1 operation
***************************************


    ``@transform`` is a 1:1 operation because for each input, it generates one output.

    .. image:: ../../images/transform_1_to_1_example.png
       :scale: 50


    This is obvious when you count the number of jobs at each step. In our example pipeline, there are always
    three jobs moving through in step at each stage (:term:`task`).

    Each "input" or "output" is not limited, however, to a single filename. Each job can accept, for example,
    a pair of files as its input, or generate more than one file or a dictionary or numbers as its output.

    When each job outputs a pair of files, this does not generate two jobs downstream. It just means that the successive
    :term:`task` in the pipeline will receive a list or tuple of files as its input parameter.

    .. note::

        The different sort of decorators in Ruffus determine the *topology* of your pipeline, i.e. how the jobs from different tasks are linked together seamlessly.

        In the later parts of the tutorial, we will encounter more decorators which can *split up*, or *join together* or *group* inputs.

            In other words, inputs and output can have **many to one**, **many to many** etc. relationships.


*******************************************
Producing several items / files per job
*******************************************

    Let us demonstrate this by modifying our previous example:
        * ``first_task_params`` is changed to 3 *pairs* of file names
        * ``@transform`` for ``first_task`` is modified to produce *pairs* of file names
            * ``.output.1``
            * ``.output.extra.1``


        ::

            from ruffus import *

            #---------------------------------------------------------------
            #   Create pairs of input files
            #
            first_task_params = [
                                 ['job1.a.start', 'job1.b.start'],
                                 ['job2.a.start', 'job2.b.start'],
                                 ['job3.a.start', 'job3.b.start'],
                                ]

            for input_file_pairs in first_task_params:
                for input_file in input_file_pairs:
                    open(input_file, "w")


            #---------------------------------------------------------------
            #
            #   first task
            #
            @transform(first_task_params, suffix(".start"),
                                    [".output.1",
                                     ".output.extra.1"],
                                   "some_extra.string.for_example", 14)
            def first_task(input_files, output_file_pair,
                            extra_parameter_str, extra_parameter_num):
                for output_file in output_file_pair:
                    with open(output_file, "w"):
                        pass


            #---------------------------------------------------------------
            #
            #   second task
            #
            @transform(first_task, suffix(".output.1"), ".output2")
            def second_task(input_files, output_file):
                with open(output_file, "w"): pass


            #---------------------------------------------------------------
            #
            #       Run
            #
            pipeline_run([second_task])

        This gives the following results:

        ::

            >>> pipeline_run([second_task])
                Job  = [[job1.a.start, job1.b.start] -> [job1.a.output.1, job1.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job2.a.start, job2.b.start] -> [job2.a.output.1, job2.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job3.a.start, job3.b.start] -> [job3.a.output.1, job3.a.output.extra.1], some_extra.string.for_example, 14] completed
            Completed Task = first_task
                Job  = [[job1.a.output.1, job1.a.output.extra.1] -> job1.a.output2] completed
                Job  = [[job2.a.output.1, job2.a.output.extra.1] -> job2.a.output2] completed
                Job  = [[job3.a.output.1, job3.a.output.extra.1] -> job3.a.output2] completed
            Completed Task = second_task



        We see that apart from having a file pair where previously there was a single file,
        little else has changed. We still have three pieces of data going through the
        pipeline in three parallel jobs.


************************************
Running pipelines in parallel
************************************
    Even though three sets of files have been specified for our pipeline, and they can be
    processed completely independently, by default  **Ruffus** runs each of them serially in succession.

    To ask Ruffus to run them in parallel, all you have to do is to add a multiprocess parameter to ``pipeline_run``:

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


    Let us see what happens if we recreated the file ``job1.a.start`` so that it appears as if 1 out of the 3 files is out of date
        ::

            open("job1.a.start", "w")
            pipeline_run([second_task], multiprocess = 5)


    Only the out of date jobs (highlighted) are re-run:

        .. code-block:: pycon
           :emphasize-lines: 4,8

            >>> pipeline_run([second_task], multiprocess = 5, verbose = 2)
                Job  = [[job2.a.start, job2.b.start] -> job2.a.output.1] unnecessary: already up to date
                Job  = [[job3.a.start, job3.b.start] -> job3.a.output.1] unnecessary: already up to date
                Job  = [[job1.a.start, job1.b.start] -> job1.a.output.1] # completed
            Completed Task = first_task
                Job  = [job2.a.output.1 -> job2.a.output.2] unnecessary: already up to date
                Job  = [job3.a.output.1 -> job3.a.output.2] unnecessary: already up to date
                Job  = [job1.a.output.1 -> job1.a.output.2] # completed
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

    Nevertheless, :term:`task` parameters can be anything which suits your workflow, from lists of files, to numbers,
    sets or tuples. Ruffus imposes few constraints on what *you*
    would like to send to each stage of your pipeline.

    **Ruffus** does, however, assume that all strings in your *input* and *output*
    parameters represent file names.

    *input* parameters which contains a |glob|_ pattern (e.g. ``*.txt``) are expanded to matching file names.


.. index:: 
    pair: @follows; referring to functions before they are defined
    pair: @follows; out of order
.. _new_manual.follows.out_of_order:

***************************************
Defining pipeline tasks out of order
***************************************

    The above assumes that all your pipelined tasks are defined in order.
    (``first_task`` before ``second_task``). This is usually the most sensible way to arrange your code.

    If you wish to refer to tasks which are not yet defined, you can do so by quoting the function name as a string and wrapping
    it with the :ref:`indicator class <decorators.indicator_objects>` :ref:`output_from(...) <decorators.output_from>` so that **Ruffus**
    knowns this is a :term:`task` name, not a file name

        .. code-block:: python
           :emphasize-lines: 5
        
            #---------------------------------------------------------------
            #
            #   second task
            #
            #   task name string wrapped in output_from(...)
            @transform(output_from("first_task"), suffix(".output.1"), ".output2")
            def second_task(input_files, output_file):
                with open(output_file, "w"): pass


            #---------------------------------------------------------------
            #
            #   first task
            #
            @transform(first_task_params, suffix(".start"),
                                    [".output.1",
                                     ".output.extra.1"],
                                   "some_extra.string.for_example", 14)
            def first_task(input_files, output_file_pair,
                            extra_parameter_str, extra_parameter_num):
                for output_file in output_file_pair:
                    with open(output_file, "w"):
                        pass


            #---------------------------------------------------------------
            #
            #       Run
            #
            pipeline_run([second_task])

    You can also refer to tasks (functions) in other modules, in which case the full 
    qualified name must be used:

        ::
        
            @transform(output_from("other_module.first_task"), suffix(".output.1"), ".output2")
            def second_task(input_files, output_file):
                pass



.. index:: 
    pair: @follows; multiple dependencies
    
.. _new_manual.follows.multiple_dependencies:

***************************************
Multiple dependencies
***************************************
            
    Each task can also depend on more than one antecedent task simply by connecting a list of tasks rather than a single tasks in ``@transform``
   
        .. code-block:: python
           :emphasize-lines: 2
        
            #
            # third_task depends on both first_task() and second_task()
            #
            @transform([first_task, second_task], suffix(".output.1"), ".output2")
            def third_task(input_files, output_file):
                with open(output_file, "w"): pass


    ``third_task()`` depends on and follows both ``first_task()`` and ``second_task()``. However, these latter two tasks are independent of each other
    and will and can run in parallel. This can be clearly shown for our example if we added a little randomness to the run time of each job:

        .. code-block:: python
        
            import time
            import random
            time.sleep(random.random())

    We can see that the execution of ``first_task()`` and ``second_task()`` jobs is interleaved and they finish in no particular order:

        .. code-block:: pycon

            >>> pipeline_run([third_task], multiprocess = 6)
                Job  = [[job3.a.start, job3.b.start] -> [job3.a.output.1, job3.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job6.a.start, job6.b.start] -> [job6.a.output.1, job6.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job1.a.start, job1.b.start] -> [job1.a.output.1, job1.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job4.a.start, job4.b.start] -> [job4.a.output.1, job4.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job5.a.start, job5.b.start] -> [job5.a.output.1, job5.a.output.extra.1], some_extra.string.for_example, 14] completed
            Completed Task = second_task
                Job  = [[job2.a.start, job2.b.start] -> [job2.a.output.1, job2.a.output.extra.1], some_extra.string.for_example, 14] completed


***************************************
:ref:`@follows <decorators.follows>`
***************************************

    If there is some reason one task has to precede the other, then this can be specified explicitly using :ref:`@follows <decorators.follows>`:


        .. code-block:: python
           :emphasize-lines: 2
        
            #
            #   @follows specifies a preceding task
            #
            @follows("first_task")
            @transform(second_task_params, suffix(".start"),
                                    [".output.1",
                                     ".output.extra.1"],
                                   "some_extra.string.for_example", 14)
            def second_task(input_files, output_file_pair,
                            extra_parameter_str, extra_parameter_num):


    :ref:`@follows <decorators.follows>` specifies either a preceding task (e.g. ``first_task``), or if 
    it has not yet been defined, the name (as a string) of a task function (e.g. ``"first_task"``).

    With the addition of :ref:`@follows <decorators.follows>`, all the jobs
    of ``second_task()`` start *after* those from ``first_task()`` have finished:

        .. code-block:: pycon


            >>> pipeline_run([third_task], multiprocess = 6)
                Job  = [[job2.a.start, job2.b.start] -> [job2.a.output.1, job2.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job3.a.start, job3.b.start] -> [job3.a.output.1, job3.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job1.a.start, job1.b.start] -> [job1.a.output.1, job1.a.output.extra.1], some_extra.string.for_example, 14] completed
            Completed Task = first_task
                Job  = [[job4.a.start, job4.b.start] -> [job4.a.output.1, job4.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job6.a.start, job6.b.start] -> [job6.a.output.1, job6.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job5.a.start, job5.b.start] -> [job5.a.output.1, job5.a.output.extra.1], some_extra.string.for_example, 14] completed
            Completed Task = second_task
    
.. _new_manual.follows.mkdir:

.. index:: 
    single: @follows; mkdir (Manual)
    single: mkdir; @follows (Manual)


******************************************************************************
Making directories automatically with :ref:`mkdir <decorators.mkdir>`
******************************************************************************

    :ref:`@follows <decorators.follows>` is also useful for making sure one or more destination directories
    exist before a task is run. 

    **Ruffus** provides special syntax to support this, using the special 
    :ref:`mkdir <decorators.mkdir>` indicator class. For example:

        .. code-block:: python
            :emphasize-lines: 2
    
            #
            #   @follows specifies both a preceding task and a directory name
            #
            @follows("first_task", mkdir("output/results/here"))
            @transform(second_task_params, suffix(".start"),
                                    [".output.1",
                                     ".output.extra.1"],
                                   "some_extra.string.for_example", 14)
            def second_task(input_files, output_file_pair,
                            extra_parameter_str, extra_parameter_num):
            
    Before ``second_task()`` is run, the ``output/results/here`` directory will be created if necessary.


