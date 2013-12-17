.. include:: ../../global.inc
.. _Simple_Tutorial_4th_step:



###################################################################
Step 4: Understanding how your pipeline works
###################################################################
    * :ref:`Simple tutorial overview <Simple_Tutorial>`
    * :ref:`pipeline functions <pipeline_functions>` in detail


.. note::
    Remember to look at the example code:

    * :ref:`Python Code for step 4 <Simple_Tutorial_4th_step_code>`

.. index::
    pair: pipeline_printout; Tutorial



The trickiest part of developing pipelines is understanding how your
data flows through the pipeline.

Parameters and files are passed from one task to another down the chain
of pipelined functions.

Whether you are learning how to use **ruffus**, or trying out a new
feature in **ruffus**, or just have a horrendously complicated pipeline
to debug (we have colleagues with >100 criss-crossing pipelined stages),
your best friend is **pipeline_printout**


If fact, this is so important, we recommend you use the ``Ruffus.cmdline`` convenience module which
will take care of all the command line arguments for you. See below for more details



=======================================
Printing out which jobs will be run
=======================================

    **pipeline_printout** takes the same parameters as pipeline_run but just prints
    the tasks which are and are not up-to-date.

    The ``verbose`` parameter controls how much detail is displayed.

    Let us take the three step  :ref:`example <Simple_Tutorial_3nd_step_code>` pipelined code we have previously written,
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
    (see :ref:`example <Simple_Tutorial_4th_step_code>`)

    This is very useful for checking that the input and output parameters have been specified
        correctly.

=============================================
Determining which jobs are out-of-date or not
=============================================

    It is often useful to see which tasks are or are not up-to-date. For example, if we
    were to run the pipeline in full, and then modify one of the intermediate files, the
    pipeline would be partially out of date.


    Let us start by run the pipeline in full but then modify ``job1.a.output.1`` so that the second task no longer appears up-to-date:

        .. code-block:: python
            :emphasize-lines: 3

            pipeline_run([second_task])

            # "touch" job1.stage1
            open("job1.a.output.1", "w").close()


    We can now see that the there is only one job in ``second_task(...)`` which needs to be re-run
    because the modication times for ``job1.a.output.1`` is after that of ``job1.a.output.2`` (highlighted):


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

================================================================
Command line options made easier with ``ruffus.cmdline``
================================================================


    Given how often pipeline developers need to

        * printout the pipeline steps without running it, or
        * run the pipeline only to a set point, or
        * change the verbosity of a pipeline, or
        * note the progress of the pipeline to a log file

    Ruffus provides an optional lightweight wrapper around the standard python `argparse  <http://docs.python.org/dev/library/argparse.html>`__ module to provide the following coommand line options.
    (You can use the deprecated ``optparse`` as well.)

        ::

                    --verbose
                    --version
                    --log_file

                -T, --target_tasks
                -j, --jobs
                -n, --just_print
                    --flowchart
                    --key_legend_in_graph
                    --draw_graph_horizontally
                    --flowchart_format
                    --forced_tasks
                    --touch_files_only
                    --checksum_file_name
                    --recreate_database



    This only requires five lines of code:

        .. code-block:: python
            :emphasize-lines: 5, 13

            from ruffus import *

            parser = cmdline.get_argparse(description='WHAT DOES THIS PIPELINE DO?')

            #   <<<---- add your own command line options like --input_file here
            #parser.add_argument("--input_file")

            options = parser.parse_args()

            #  logger which can be passed to multiprocessing ruffus tasks
            logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

            #   <<<----  pipelined functions go here

            cmdline.run (options)

_____________________________________________________________________________________
Tracing pipeline progress
_____________________________________________________________________________________

    Now to understand what is happening with your pipeline, what tasks and which
    jobs are up-to-date etc, call your script with the following options:

        .. code-block:: bash

            myscript -n

            or

            myscript --just_print


    Increase levels of verbosity to provide more detailed output

        .. code-block:: bash

            # well-mannered, reserved
            myscript -n -v

            or

            # extremely loquacious
            myscript --just_print --verbose 5



_____________________________________________________________________________________
Running in parallel
_____________________________________________________________________________________

    Optionally specify the number of parallel strands of execution and which is the final task is

        .. code-block:: bash

            # run all tasks
            myscript --j 3 --target_tasks "second_task"

            # force just the first task to rerun even if it is up-to-date
            myscript --jobs 15 --forced_tasks "first_task"


_____________________________________________________________________________________
Log to a file
_____________________________________________________________________________________

    Optionally set up logger (as in the example) so that it will log error messages,
    or anything you want, using the standard python `logging  <http://docs.python.org/2/library/logging.html>`_ module.

        .. code-block:: bash

            # keep tabs on yourself
            myscript --log_file /var/log/secret.logbook
