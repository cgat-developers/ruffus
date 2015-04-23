.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: command line; Tutorial

.. _new_manual.cmdline:

######################################################################################################
|new_manual.cmdline.chapter_num|: Running *Ruffus* from the command line with ruffus.cmdline
######################################################################################################

.. seealso::

   * :ref:`Manual table of Contents <new_manual.table_of_contents>`


We find that much of our *Ruffus* pipeline code is built on the same template and this is generally
a good place to start developing a new pipeline.

From version 2.4, *Ruffus* includes an optional ``Ruffus.cmdline`` module that provides
support for a set of common command line arguments. This makes writing *Ruffus* pipelines much more pleasant.


.. _new_manual.cmdline.get_argparse:

.. _new_manual.cmdline.run:

.. _new_manual.cmdline.setup_logging:

************************************************************************************************************
Template for `argparse  <http://docs.python.org/2.7/library/argparse.html>`__
************************************************************************************************************
    All you need to do is copy these 6 lines


    .. code-block:: python
        :emphasize-lines: 5, 13

        import ruffus.cmdline as cmdline

        parser = cmdline.get_argparse(description='WHAT DOES THIS PIPELINE DO?')

        #   <<<---- add your own command line options like --input_file here
        # parser.add_argument("--input_file")

        options = parser.parse_args()

        #  standard python logger which can be synchronised across concurrent Ruffus tasks
        logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

        #   <<<----  pipelined functions go here

        cmdline.run (options)

    You are recommended to use the standard `argparse  <http://docs.python.org/2.7/library/argparse.html>`__ module
    but the deprecated `optparse  <http://docs.python.org/2.7/library/optparse.html>`__ module works as well. (See :ref:`below <code_template.optparse>` for the template)


******************************************************
Command Line Arguments
******************************************************

     ``Ruffus.cmdline`` by default provides these predefined options:

        .. code-block:: bash
            :emphasize-lines: 5,12,15,22

            -v, --verbose
                --version
            -L, --log_file

                # tasks
            -T, --target_tasks
                --forced_tasks
            -j, --jobs
                --use_threads


                # printout
            -n, --just_print

                # flow chart
                --flowchart
                --key_legend_in_graph
                --draw_graph_horizontally
                --flowchart_format


                # check sum
                --touch_files_only
                --checksum_file_name
                --recreate_database


******************************************************
1) Logging
******************************************************

    The script provides for logging both to the command line:

        .. code-block:: bash

            myscript -v
            myscript --verbose

    and an optional log file:

        .. code-block:: bash

            # keep tabs on yourself
            myscript --log_file /var/log/secret.logbook

    Logging is ignored if neither ``--verbose`` or ``--log_file`` are specified on the command line

    ``Ruffus.cmdline`` automatically allows you to write to a shared log file via a proxy from multiple processes.
    However, you do need to use ``logging_mutex`` for the log files to be synchronised properly across different jobs:

        .. code-block:: python

            with logging_mutex:

                logger_proxy.info("Look Ma. No hands")

    Logging is set up so that you can write


=================================
        A) Only to the log file:
=================================

        .. code-block:: python

                logger.info("A message")

=================================
        B) Only to the display:
=================================

        .. code-block:: python

                logger.debug("A message")


.. _new_manual.cmdline.MESSAGE:

======================================
        C) To both simultaneously:
======================================

        .. code-block:: python

                from ruffus.cmdline import MESSAGE

                logger.log(MESSAGE, "A message")


******************************************************
2) Tracing pipeline progress
******************************************************

    This is extremely useful for understanding what is happening with your pipeline, what tasks and which
    jobs are up-to-date etc.

    See :ref:`new_manual.pipeline_printout`

    To trace the pipeline, call script with the following options

        .. code-block:: bash

            # well-mannered, reserved
            myscript --just_print
            myscript -n

            or

            # extremely loquacious
            myscript --just_print --verbose 5
            myscript -n -v5

    Increasing levels of verbosity (``--verbose`` to ``--verbose 5``) provide more detailed output



******************************************************
3) Printing a flowchart
******************************************************

    This is the subject of :ref:`new_manual.pipeline_printout_graph`.

    Flowcharts can be specified using the following option:

        .. code-block:: bash

            myscript --flowchart xxxchart.svg

    The extension of the flowchart file indicates what format the flowchart should take,
    for example, ``svg``, ``jpg`` etc.

    Override with ``--flowchart_format``

******************************************************
4) Running in parallel on multiple processors
******************************************************


    Optionally specify the number of parallel strands of execution and which is the last *target* task to run.
    The pipeline will run starting from any out-of-date tasks which precede the *target* and proceed no further
    beyond the *target*.

        .. code-block:: bash

            myscript --jobs 15 --target_tasks "final_task"
            myscript -j 15




******************************************************************************************************
5) Setup checkpointing so that *Ruffus* knows which files are out of date
******************************************************************************************************

    The :ref:`checkpoint file <new_manual.checkpointing>` uses to the value set in the
    environment (``DEFAULT_RUFFUS_HISTORY_FILE``).

    If this is not set, it will default to ``.ruffus_history.sqlite`` in the current working directory.

    Either can be changed on the command line:

        .. code-block:: bash

            myscript --checksum_file_name mychecksum.sqlite


============================================================================================================================================================
Recreating checkpoints
============================================================================================================================================================

    Create or update the checkpoint file so that all existing files in completed jobs appear up to date

    Will stop sensibly if current state is incomplete or inconsistent

        ::

            myscript --recreate_database

============================================================================================================================================================
Touch files
============================================================================================================================================================

    As far as possible, create empty files with the correct timestamp to make the pipeline appear up to date.

    .. code-block:: bash

        myscript --touch_files_only


******************************************************************************************************
6) Skipping specified options
******************************************************************************************************
    Note that particular options can be skipped (not added to the command line), if they conflict with your own options, for example:

        .. code-block:: python
            :emphasize-lines: 3

            # see below for how to use get_argparse
            parser = cmdline.get_argparse(  description='WHAT DOES THIS PIPELINE DO?',
                                            # Exclude the following options:
                                            #     --log_file --key_legend_in_graph
                                            ignored_args = ["log_file", "key_legend_in_graph"])


******************************************************************************************************
7) Specifying verbosity and abbreviating long paths
******************************************************************************************************

    The verbosity can be specified on the command line

        .. code-block:: bash

            myscript --verbose 5

            # verbosity of 5 + 1 = 6
            myscript --verbose 5 --verbose

            # verbosity reset to 2
            myscript --verbose 5 --verbose --verbose 2

    If the printed paths are too long, and need to be abbreviated, or alternatively, if you want see the full absolute paths of your input and output parameters,
    you can specify an extension to the verbosity. See the manual discussion of :ref:`verbose_abbreviated_path <new_manual.pipeline_printout.verbose_abbreviated_path>` for
    more details. This is specified as ``--verbose VERBOSITY:VERBOSE_ABBREVIATED_PATH``. (No spaces!)

    For example:

        .. code-block:: bash
           :emphasize-lines: 4,7

            # verbosity of 4
            myscript.py --verbose 4

            # display three levels of nested directories
            myscript.py --verbose 4:3

            # restrict input and output parameters to 60 letters
            myscript.py --verbose 4:-60


******************************************************************************************************
8) Displaying the version
******************************************************************************************************
    Note that the version for your script will default to ``"%(prog)s 1.0"`` unless specified:

        .. code-block:: python

            parser = cmdline.get_argparse(  description='WHAT DOES THIS PIPELINE DO?',
                                            version = "my_programme.py v. 2.23")







.. _code_template.optparse:

************************************************************************************************************
Template for `optparse  <http://docs.python.org/2.7/library/optparse.html>`__
************************************************************************************************************

    deprecated since python 2.7

        .. code-block:: python
            :emphasize-lines: 8

            #
            #   Using optparse (new in python v 2.6)
            #
            from ruffus import *

            parser = cmdline.get_optgparse(version="%prog 1.0", usage = "\n\n    %prog [options]")

            #   <<<---- add your own command line options like --input_file here
            # parser.add_option("-i", "--input_file", dest="input_file", help="Input file")

            (options, remaining_args) = parser.parse_args()

            #  logger which can be passed to ruffus tasks
            logger, logger_mutex = cmdline.setup_logging ("this_program",
                                                          options.log_file,
                                                          options.verbose)

            #   <<<----  pipelined functions go here

            cmdline.run (options)

