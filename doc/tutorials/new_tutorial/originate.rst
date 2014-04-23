.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc


.. index::
    pair: originate; Tutorial

.. _new_manual.originate:

######################################################################################################
|new_manual.originate.chapter_num|: Creating files with ``@originate``
######################################################################################################

.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@originate syntax in detail <decorators.originate>`

.. note::

    Remember to look at the example code:

    * :ref:`new_manual.originate.code`

********************************************************************************************
Simplifying our example with :ref:`@originate <decorators.originate>`
********************************************************************************************

    Our previous pipeline example started off with a set of files which we had to create first.

    This is a common task: pipelines have to start *somewhere*.

    Ideally, though, we would only want to create these starting files if they didn't already exist. In other words, we want a sort of ``@transform`` which makes files from nothing (``None``?).

    This is exactly what :ref:`@originate <decorators.originate>` helps you to do.

    Rewriting our pipeline with :ref:`@originate <decorators.originate>` gives the following three steps:


    .. code-block:: python
        :emphasize-lines: 6

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



