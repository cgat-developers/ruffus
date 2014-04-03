.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: deprecated @files; Tutorial

.. _new_manual.deprecated_files:

#####################################################################################################################
|new_manual.deprecated_files.chapter_num|: **@files**: Deprecated syntax
#####################################################################################################################

.. warning ::

    -

        **This is deprecated syntax**

        **which is no longer supported and**

        **should NOT be used in new code.**

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`decorators <decorators>`
    * :ref:`@files <decorators.files>` syntax in detail


***************************************
Overview
***************************************


    | The python functions which do the actual work of each stage  or
      :term:`task` of a *Ruffus* pipeline are written by you.
    | The role of *Ruffus* is to make sure these functions are called in the right order,
      with the right parameters, running in parallel using multiprocessing if desired.

    The easiest way to specify parameters to *Ruffus* :term:`task` functions is to use
    the :ref:`@files <decorators.files>` decorator.

    .. index::
        pair: @files; Manual


***************************************
**@files**
***************************************

    Running this code:

        ::

            from ruffus import *

            @files('a.1', ['a.2', 'b.2'], 'A file')
            def single_job_io_task(infile, outfiles, text):
                for o in outfiles: open(o, "w")

            # prepare input file
            open('a.1', "w")

            pipeline_run()


        Is equivalent to calling:
            ::

                single_job_io_task('a.1', ['a.2', 'b.2'], 'A file')


        And produces:
            ::

                >>> pipeline_run()
                    Job = [a.1 -> [a.2, b.2], A file] completed
                Completed Task = single_job_io_task

    *Ruffus* will automatically check if your task is up to date. The second time :ref:`pipeline_run() <pipeline_functions.pipeline_run>`
    is called, nothing will happen. But if you update ``a.1``, the task will rerun:

        ::

            >>> open('a.1', "w")
            >>> pipeline_run()
                Job = [a.1 -> [a.2, b.2], A file] completed
            Completed Task = single_job_io_task

    See :ref:`chapter 2 <new_manual.skip_up_to_date.rules>` for a more in-depth discussion of how *Ruffus*
    decides which parts of the pipeline are complete and up-to-date.


.. index::
    pair: @files; in parallel

.. _new_manual.files.parallel:

******************************************************************************
Running the same code on different parameters in parallel
******************************************************************************

    Your pipeline may require the same function to be called multiple times on independent parameters.
    In which case, you can supply all the parameters to @files, each will be sent to separate jobs that
    may run in parallel if necessary. *Ruffus* will check if each separate :term:`job` is up-to-date using
    the *inputs* and *outputs* (first two) parameters (See the :ref:`new_manual.only_rerun_out_of_date` ).


    For example, if a sequence
    (e.g. a list or tuple) of 5 parameters are passed to **@files**, that indicates
    there will also be 5 separate jobs:

        ::

            from ruffus import *
            parameters = [
                                [ 'job1.file'           ],             # 1st job
                                [ 'job2.file', 4        ],             # 2st job
                                [ 'job3.file', [3, 2]   ],             # 3st job
                                [ 67, [13, 'job4.file'] ],             # 4st job
                                [ 'job5.file'           ],             # 5st job
                          ]
            @files(parameters)
            def task_file(*params):
                ""

    | *Ruffus* creates as many jobs as there are elements in ``parameters``.
    | In turn, each of these elements consist of series of parameters which will be
      passed to each separate job.

    Thus the above code is equivalent to calling:

        ::

             task_file('job1.file')
             task_file('job2.file', 4)
             task_file('job3.file', [3, 2])
             task_file(67, [13, 'job4.file'])
             task_file('job5.file')


    What ``task_file()`` does with these parameters is up to you!

    The only constraint on the parameters is that *Ruffus* will treat any first
    parameter of each job as the *inputs* and any second as the *output*. Any
    strings in the *inputs* or *output* parameters (including those nested in sequences)
    will be treated as file names.

    Thus, to pick the parameters out of one of the above jobs:

        ::

             task_file(67, [13, 'job4.file'])

        | *inputs*  == ``67``
        | *outputs* == ``[13, 'job4.file']``
        |
        |   The solitary output filename is ``job4.file``


.. index::
    pair: @files; check if up to date

.. _new_manual.files.is_uptodate:
.. _new_manual.files.example:

=======================================
Checking if jobs are up to date
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


    | If you called :ref:`pipeline_run() <pipeline_functions.pipeline_run>` again, nothing would happen because the files are up to date:
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





