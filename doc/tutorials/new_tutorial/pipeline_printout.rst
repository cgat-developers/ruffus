.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: pipeline_printout; Tutorial

.. _new_manual.pipeline_printout:

######################################################################################################
|new_manual.pipeline_printout.chapter_num|: Understanding how your pipeline works
######################################################################################################


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

    This is very useful for checking that the input and output parameters have been specified
        correctly.

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
            Tasks which will be run:

            Task = second_task
                   Job  = [job1.a.output.1
                         -> job1.a.output.2]

            >>> # File modification times shown for out of date files
                     Job needs update:
                     Input files:
                      * 05 Dec 2013 12:04:52.80: job1.a.output.1
                     Output files:
                      * 05 Dec 2013 12:01:29.01: job1.a.output.2

                   Job  = [job2.a.output.1
                         -> job2.a.output.2]
                     Job up-to-date
                   Job  = [job3.a.output.1
                         -> job3.a.output.2]
                     Job up-to-date

            ________________________________________

    N.B. At a verbosity of 5, even jobs which are up-to-date will be displayed.

