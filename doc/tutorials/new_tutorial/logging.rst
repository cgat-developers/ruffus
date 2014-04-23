.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: logging; Tutorial

.. _new_manual.logging:

######################################################################################################
|new_manual.logging.chapter_num|: Logging progress through a pipeline
######################################################################################################


.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`

.. note::

    Remember to look at the :ref:`example code <new_manual.logging.code>`

*************************
Overview
*************************

    There are two parts to logging with **Ruffus**:

    * Logging progress through the pipeline

        This produces the sort of output displayed in this manual:

        ::

            >>> pipeline_run([parallel_io_task])
            Task = parallel_io_task
                Job = ["a.1" -> "a.2", "A file"] completed
                Job = ["b.1" -> "b.2", "B file"] unnecessary: already up to date
            Completed Task = parallel_io_task


    * Logging your own messages from within your pipelined functions.

        Because **Ruffus** may run each task function in separate process on a separate
        CPU (multiprocessing), some attention has to be paid to how to send and
        synchronise your log messages across process boundaries.


    We shall deal with these in turn.


.. _new_manual.logging.pipeline:

**********************************
Logging task/job completion
**********************************
    By default, *Ruffus* logs each task and each job as it is completed to
    `sys.stderr  <http://docs.python.org/2/library/sys.html#sys.stderr>`__.

    By default, Ruffus logs to ``STDERR``: :ref:`pipeline_run(logger = stderr_logger) <pipeline_functions.pipeline_run>`.

    If you want to turn off all tracking messages as the pipeline runs, apart from setting ``verbose = 0``, you
    can also use the aptly named Ruffus ``black_hole_logger``:

        .. code-block:: python

            pipeline_run(logger = black_hole_logger)

.. index::
    pair: pipeline_run verbosity; Tutorial

=================================
Controlling logging verbosity
=================================
    :ref:`pipeline_run() <pipeline_functions.pipeline_run>` currently has five levels of verbosity, set by the optional ``verbose``
    parameter which defaults to 1:

        ::

                verbose = 0: nothing
                verbose = 1: logs completed jobs/tasks;
                verbose = 2: logs up to date jobs in incomplete tasks
                verbose = 3: logs reason for running job
                verbose = 4: logs messages useful only for debugging ruffus pipeline code


        ``verbose`` > ``5`` are intended for debugging **Ruffus** by the developers and the details
        are liable to change from release to release


.. index::
    pair: logging with ruffus.cmdline; Tutorial

********************************************************************************
Use :ref:`ruffus.cmdline <new_manual.cmdline>`
********************************************************************************

    As always, it is easiest to use :ref:`ruffus.cmdline <new_manual.cmdline>`.

    Set your script to

        * write messages to ``STDERR`` with the ``--verbose`` option and
        * to a log file with the ``--log_file`` option.

        .. code-block:: python
           :emphasize-lines: 3

            from ruffus import *

            #  Python logger which can be synchronised across concurrent Ruffus tasks
            logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

            @transform( ["job1.input"], suffix(".input"), ".output1"),
            def first_task(input_file, output_file):
                pass

            pipeline_run(logger=logger)


.. index::
    pair: logging customising; Tutorial

****************************************
Customising logging
****************************************

    You can also specify exactly how logging works by providing a `logging <http://docs.python.org/library/logging.html>`_ object
    to :ref:`pipeline_run() <pipeline_functions.pipeline_run>` .
    This log object should have ``debug()`` and ``info()`` methods.

    Instead of writing your own, it is usually more convenient to use the python
    `logging <http://docs.python.org/library/logging.html>`_
    module which provides logging classes with rich functionality.

    The :ref:`example code<new_manual.logging.code>` sets up a logger to a rotating set of files


.. index::
    pair: logging your own message; Tutorial

.. _new_manual.logging.per_job:

****************************************
Log your own messages
****************************************

    You need to take a little care when logging your custom messages *within* your pipeline.

    * If your Ruffus pipeline may run in parallel, make sure that logging is synchronised.
    * If your Ruffus pipeline may run across separate processes, send your logging object across process boundaries.


    `logging <http://docs.python.org/library/logging.html>`_ objects can not be
    `pickled <http://docs.python.org/library/pickle.html>`_ and shared naively across
    processes. Instead, we need to create proxies which forward the logging to a single
    shared log.

    The :ref:`ruffus.proxy_logger <proxy-logger>` module provides an easy way to share
    `logging <http://docs.python.org/library/logging.html>`_ objects among
    jobs. This requires just two simple steps:




.. note::

    * This is a good template for sharing `non-picklable objects <http://docs.python.org/2/library/pickle.html#what-can-be-pickled-and-unpickled>`_
      across processes.


.. _new_manual.sharing_proxy_object:


============================================================
    1. Set up logging
============================================================

    Things are easiest if you are using ``ruffus.cmdline``:

    .. code-block:: python

        #  standard python logger which can be synchronised across concurrent Ruffus tasks
        logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)


    Otherwise, manually:

    .. code-block:: python


        from ruffus.proxy_logger import *
        (logger,
         logging_mutex) = make_shared_logger_and_proxy (setup_std_shared_logger,
                                                        "my_logger",
                                                        {"file_name" :"/my/lg.log"})

============================================================
    2. Share the proxy
============================================================
        Now, pass:

            * ``logger`` (which forwards logging calls across jobs) and
            * ``logging_mutex`` (which prevents different jobs which are logging simultaneously
              from being jumbled up)

        to each job:

        .. code-block:: python
            :emphasize-lines: 4,6,9

            @transform( initial_file,
                        suffix(".input"),
                        ".output1",
                        logger, logging_mutex),         # pass log and synchronisation as parameters
            def first_task(input_file, output_file,
                        logger, logging_mutex):         # pass log and synchronisation as parameters
                pass

                # synchronise logging
                with logging_mutex:
                    logger.info("Here we go logging...")

