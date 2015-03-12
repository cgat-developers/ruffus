.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.checkpointing.code:

#################################################################################################################
|new_manual.checkpointing.chapter_num|: Python Code for Checkpointing: Interrupted Pipelines and Exceptions
#################################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`Back to |new_manual.checkpointing.chapter_num|: Interrupted Pipelines and Exceptions <new_manual.checkpointing>`


************************************************************************
Code for the "Interrupting tasks" example
************************************************************************

    .. <<python

    .. code-block:: python



        from ruffus import *

        from ruffus import *
        import sys, time

        #   create initial files
        @originate(['job1.start'])
        def create_initial_files(output_file):
            with open(output_file, "w") as oo: pass


        #---------------------------------------------------------------
        #
        #   long task to interrupt
        #
        @transform(create_initial_files, suffix(".start"), ".output")
        def long_task(input_files, output_file):
            with open(output_file, "w") as ff:
                ff.write("Unfinished...")
                # sleep for 2 seconds here so you can interrupt me
                sys.stderr.write("Job started. Press ^C to interrupt me now...\n")
                time.sleep(2)
                ff.write("\nFinished")
                sys.stderr.write("Job completed.\n")


        #       Run
        pipeline_run([long_task])

    ..
        python

