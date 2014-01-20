.. include:: ../../global.inc

.. _code_template:

******************************************************
Standard code for developing Ruffus pipelines
******************************************************



We find that much of our Ruffus pipeline code is built on the same template and this is generally
a good place to start developing a new pipeline.

From version 2.4 up, Ruffus therefore includes an optional ``Ruffus.cmdline`` module which provides
support for a set of common command line arguments which make writing *Ruffus* much more pleasant

******************************************************
``argparse``
******************************************************
    All you need to do is copy these 6 lines


    .. code-block:: python
        :emphasize-lines: 5,13
        :linenos:

        from ruffus import *

        parser = cmdline.get_argparse(description='WHAT DOES THIS PIPELINE DO?')

        #   <<<---- add your own command line options like --input_file here
        # parser.add_argument("--input_file")

        options = parser.parse_args()

        #  logger which can be passed to multiprocessing ruffus tasks
        logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

        #   <<<----  pipelined functions go here

        cmdline.run (options)

    You are recommended to use the standard `argparse  <http://docs.python.org/2.7/library/argparse.html>`__ module
    but the deprecated `optparse  <http://docs.python.org/2.7/library/optparse.html>`__ module works as well. (See :ref:`below <code_template.optparse>` for the template)


##################################
1) Command Line Arguments
##################################

     ``Ruffus.cmdline`` by default provides these predefined options:

        .. code-block:: bash
            :emphasize-lines: 5,12,22

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


#################
1) Logging
#################

    The script provides for logging both to the command line:

        .. code-block:: bash

            myscript -v
            myscript --verbose

    and an optional log file:

        .. code-block:: bash

            myscript --log_file PIPELINE.LOG_FILE

    Loggin is ignored if ``--verbose`` or ``--log_file`` are not specified
    on the command line

    ``Ruffus.cmdline`` automatically allows you to access the same log file from multiple processes, via a proxy.
    You need to use ``logging_mutex`` as well for the log files to be synchronised properly
    across different jobs:

        .. code-block:: bash

            with logging_mutex:

                logger_proxy.info("Look Ma. No hands")

    Logging is set up so that you can write


=================================
        A) Only to the log file:
=================================
            ::

                logger.info("A message")

=================================
        B) Only to the display:
=================================
            ::

                logger.debug("A message")

======================================
        C) To both simultaneously:
======================================

        .. code-block:: bash

                from ruffus.cmdline import MESSAGE

                logger.log(MESSAGE, "A message")


##################################
3) Tracing pipeline progress
##################################

    This is extremely useful for understanding what is happening with your pipeline, what tasks and which
    jobs are up-to-date etc.

    See the :ref:`manual <manual.tracing_pipeline_parameters>` for a full discussion

    To trace the pipeline, call script with the following options

        .. code-block:: bash

            myscript -n

            or

            myscript --just_print

    Increasing levels of verbosity (``-v`` to ``-v 5``) provide more detailed output


##################################
4) Printing a flowchart
##################################

    This can be specified using the following option:

        .. code-block:: bash

            myscript --flowchart xxxchart.svg

    The extension of the flowchart file indicates what format the flowchart should take,
    for example, ``svg``, ``jpg`` etc.

    Override with ``--flowchart_format``


#######################################################
5) Running the pipeline on multiple processors
#######################################################

    Optionally specify the number of parallel strands of execution and which the final task is::

        myscript --jobs 15 --target_tasks "final_task"
        myscript -j 15


##############################################################################################################
6) Setup checkpointing so that Ruffus knows which files are out of date
##############################################################################################################

    The checkpoint file defaults to ``.ruffus_history.sqlite`` in the script current working directory. This file name can be set via

        .. code-block:: bash

            myscript --checksum_file_name mychecksum.sqlite

    The command line settings override what is set in the environment (``DEFAULT_RUFFUS_HISTORY_FILE``)

============================================================================================================================================================
Example 1: same directory, different name
============================================================================================================================================================
    If the environment variable is:

    ::

        export DEFAULT_RUFFUS_HISTORY_FILE=.{basename}.ruffus_history.sqlite

    Then the job history database for ``run.me.py`` will be ``.run.me.ruffus_history.sqlite``

    .. code-block:: bash

        /common/path/for/job_history/scripts/run.me.py
        /common/path/for/job_history/scripts/.run.me.ruffus_history.sqlite

============================================================================================================================================================
Example 2: nested in common directory
============================================================================================================================================================

    .. code-block:: bash

        export DEFAULT_RUFFUS_HISTORY_FILE=/common/path/for/job_history/{path}/.{basename}.ruffus_history.sqlite

    .. code-block:: bash

            /test/bin/scripts/run.me.py
            /common/path/for/job_history/test/bin/scripts/.run.me.ruffus_history.sqlite


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


##############################################################################################################
7) Skipping specified options
##############################################################################################################
    Note that particular options can be skipped (not added to the command line, for example, if they conflict with your own options:

        .. code-block:: python
            :emphasize-lines: 3

            # see below for how to use get_argparse
            parser = cmdline.get_argparse(  description='WHAT DOES THIS PIPELINE DO?',
                                            # skip the following options
                                            ignored_args = ["log_file", "key_legend_in_graph"])


##############################################################################################################
8) Script versions
##############################################################################################################
    Note that the version for ``get_argparse`` defaults to ``"%(prog)s 1.0"`` unless specified:

        .. code-block:: python

            :emphasize-lines: 3

            # see below for how to use get_argparse
            parser = cmdline.get_argparse(  description='WHAT DOES THIS PIPELINE DO?',
                                            version = "my_programme.py v. 2.23")








.. _code_template.optparse:

******************************************************
``optparse``
******************************************************

    deprecated since python 2.7

        .. code-block:: python

            #
            #   Using optparse (new in python v 2.6)
            #
            from ruffus import *

            parser = cmdline.get_optgparse(version="%prog 1.0", usage = "\n\n    %prog [options]")

            #   <<<---- add your own command line options like --input_file here
            # parser.add_option("-i", "--input_file", dest="input_file", help="Input file")

            (options, remaining_args) = parser.parse_args()

            #  logger which can be passed to ruffus tasks
            logger, logger_mutex = cmdline.setup_logging ("this_program", options.log_file, options.verbose)

            #   <<<----  pipelined functions go here

            cmdline.run (options)

