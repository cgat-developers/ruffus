.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: pipeline_printout; Tutorial

.. _new_manual.pipeline_printout:

############################################################################################################################################################################################################
|new_manual.pipeline_printout.chapter_num|: Understanding how your pipeline works with :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>`
############################################################################################################################################################################################################


.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>` syntax
   * :ref:`Python Code for this chapter <new_manual.pipeline_printout.code>`


.. note::

    * **Whether you are learning or developing ruffus pipelines, your best friend is** :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>`
      **This shows the exact parameters and files as they are passed through the pipeline.**

    * **We also** *strongly* **recommend you use the** ``Ruffus.cmdline`` **convenience module which**
      **will take care of all the command line arguments for you. See** :ref:`new_manual.cmdline`.



=======================================
Printing out which jobs will be run
=======================================

    :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>` takes the same parameters as pipeline_run but just prints
    the tasks which are and are not up-to-date.

    The ``verbose`` parameter controls how much detail is displayed.

    Let us take the pipelined code we previously wrote in
    |new_manual.transform_in_parallel.chapter_num| :ref:`More on @transform-ing data and @originate <new_manual.transform_in_parallel.code>`
    but call :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>` instead of
    :ref:`pipeline_run(...) <pipeline_functions.pipeline_run>`.
    This lists the tasks which will be run in the pipeline:

        ::

            >>> import sys
            >>> pipeline_printout(sys.stdout, [second_task])

            ________________________________________
            Tasks which will be run:

            Task = create_initial_file_pairs
            Task = first_task
            Task = second_task
            ________________________________________



    To see the input and output parameters of each job in the pipeline, try increasing the verbosity from the default (``1``) to ``3``
    (See :ref:`code  <new_manual.pipeline_printout.code>`)

    This is very useful for checking that the input and output parameters have been specified correctly.

=============================================
Determining which jobs are out-of-date or not
=============================================

    It is often useful to see which tasks are or are not up-to-date. For example, if we
    were to run the pipeline in full, and then modify one of the intermediate files, the
    pipeline would be partially out of date.


    Let us start by run the pipeline in full but then modify ``job1.a.output.1`` so that the second task appears out-of-date:

        .. code-block:: python
            :emphasize-lines: 3

            pipeline_run([second_task])

            # "touch" job1.stage1
            open("job1.a.output.1", "w").close()


    Run :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>` with a verbosity of ``5``.

    This will tell you exactly why ``second_task(...)`` needs to be re-run:
    because ``job1.a.output.1`` has a file modification time *after* ``job1.a.output.2`` (highlighted):


        .. code-block:: pycon
            :emphasize-lines: 9

            >>> pipeline_printout(sys.stdout, [second_task], verbose = 5)

            ________________________________________
            Tasks which are up-to-date:

            Task = create_initial_file_pairs
            Task = first_task

            ________________________________________

            ________________________________________
            Tasks which will be run:

            Task = second_task
                   Job  = [job1.a.output.1
                         -> job1.a.output.2]
            >>> # File modification times shown for out of date files
                     Job needs update:
                     Input files:
                      * 22 Jul 2014 15:29:19.33: job1.a.output.1
                     Output files:
                      * 22 Jul 2014 15:29:07.53: job1.a.output.2

                   Job  = [job2.a.output.1
                         -> job2.a.output.2]
                   Job  = [job3.a.output.1
                         -> job3.a.output.2]

            ________________________________________


    N.B. At a verbosity of 5, even jobs which are up-to-date in ``second_task`` are displayed.



=============================================
Verbosity levels
=============================================

    The verbosity levels for :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>` and :ref:`pipeline_run(...) <pipeline_functions.pipeline_run>`
    can be specified from ``verbose = 0`` (print out nothing) to the extreme verbosity of ``verbose=6``.  A verbosity of above 10 is reserved for the internal
    debugging of Ruffus

        * level **0** : *nothing*
        * level **1** : *Out-of-date Task names*
        * level **2** : *All Tasks (including any task function docstrings)*
        * level **3** : *Out-of-date Jobs in Out-of-date Tasks, no explanation*
        * level **4** : *Out-of-date Jobs in Out-of-date Tasks, with explanations and warnings*
        * level **5** : *All Jobs in Out-of-date Tasks,  (include only list of up-to-date tasks)*
        * level **6** : *All jobs in All Tasks whether out of date or not*
        * level **10**: *logs messages useful only for debugging ruffus pipeline code*

.. _new_manual.pipeline_printout.verbose_abbreviated_path:

==========================================================================================
Abbreviating long file paths with ``verbose_abbreviated_path``
==========================================================================================

    Pipelines often produce interminable lists of deeply nested filenames. It would be nice to be able to abbreviate this
    to just enough information to follow the progress.

    The ``verbose_abbreviated_path`` parameter specifies that   :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>` and :ref:`pipeline_run(...) <pipeline_functions.pipeline_run>` only display

        1) the ``NNN`` th top level sub-directories to be included, or that
        2) the message to be truncated to a specified ```MMM`` characters (to fit onto a line, for example). ``MMM`` is specified by setting ``verbose_abbreviated_path = -MMM``, i.e. negative values.

           Note that the number of characters specified is just the separate lengths of the input and output parameters,
           not the entire indented line. You many need to specify a smaller limit that you expect (e.g. ``60`` rather than `80`)

        .. code-block:: python

            pipeline_printout(verbose_abbreviated_path = NNN)
            pipeline_run(verbose_abbreviated_path = -MMM)



    ``verbose_abbreviated_path`` defaults to ``2``


    For example:

        Given ``["aa/bb/cc/dddd.txt", "aaa/bbbb/cccc/eeed/eeee/ffff/gggg.txt"]``


        .. code-block:: python
           :emphasize-lines: 1,4,8,19

            # Original relative paths
            "[aa/bb/cc/dddd.txt, aaa/bbbb/cccc/eeed/eeee/ffff/gggg.txt]"

            # Full abspath
            verbose_abbreviated_path = 0
            "[/test/ruffus/src/aa/bb/cc/dddd.txt, /test/ruffus/src/aaa/bbbb/cccc/eeed/eeee/ffff/gggg.txt]"

            # Specifed level of nested directories
            verbose_abbreviated_path = 1
            "[.../dddd.txt, .../gggg.txt]"

            verbose_abbreviated_path = 2
            "[.../cc/dddd.txt, .../ffff/gggg.txt]"

            verbose_abbreviated_path = 3
            "[.../bb/cc/dddd.txt, .../eeee/ffff/gggg.txt]"


            # Truncated to MMM characters
            verbose_abbreviated_path = -60
            "<???> /bb/cc/dddd.txt, aaa/bbbb/cccc/eeed/eeee/ffff/gggg.txt]"


=============================================
Getting a list of all tasks in a pipeline
=============================================

    If you just wanted a list of all tasks (Ruffus decorated function names), then you can
    just run Run :ref:`pipeline_get_task_names(...) <pipeline_functions.pipeline_get_task_names>`.

    This doesn't touch any pipeline code or even check to see if the pipeline is connected up properly.

    However, it is sometimes useful to allow users at the command line to choose from a list of
    possible tasks as a target.
