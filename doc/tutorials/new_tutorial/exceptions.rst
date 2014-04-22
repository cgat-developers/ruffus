.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: exceptions; Tutorial

.. _new_manual.exceptions:

###################################################################################################
|new_manual.exceptions.chapter_num|: Exceptions thrown inside pipelines
###################################################################################################

**************************************
Overview
**************************************


    The goal for *Ruffus* is that exceptions should just work *out-of-the-box* without any fuss.
    This is especially important for exceptions that come from your code which may be raised
    in a different process. Often multiple parallel operations (jobs or tasks) fail at the
    same time. *Ruffus* will forward each of these exceptions with the tracebacks so you
    can jump straight to the offending line.

    This example shows separate exceptions from two jobs running in parallel:


    .. code-block:: python

            from ruffus import *

            @originate(["a.start", "b.start", "c.start", "d.start", "e.start"])
            def throw_exceptions_here(output_file):
                raise Exception("OOPS")

            pipeline_run(multiprocess = 2)

    .. code-block:: pycon
        :emphasize-lines: 5, 21

            >>> pipeline_run(multiprocess = 2)

            ruffus.ruffus_exceptions.RethrownJobError:

            Original exceptions:

                Exception #1
                  'exceptions.Exception(OOPS)' raised in ...
                   Task = def throw_exceptions_here(...):
                   Job  = [None -> b.start]

                Traceback (most recent call last):
                  File "/usr/local/lib/python2.7/dist-packages/ruffus/task.py", line 685, in run_pooled_job_without_exceptions
                    return_value =  job_wrapper(param, user_defined_work_func, register_cleanup, touch_files_only)
                  File "/usr/local/lib/python2.7/dist-packages/ruffus/task.py", line 549, in job_wrapper_output_files
                    job_wrapper_io_files(param, user_defined_work_func, register_cleanup, touch_files_only, output_files_only = True)
                  File "/usr/local/lib/python2.7/dist-packages/ruffus/task.py", line 504, in job_wrapper_io_files
                    ret_val = user_defined_work_func(*(param[1:]))
                  File "<stdin>", line 3, in throw_exceptions_here
                Exception: OOPS


                Exception #2
                  'exceptions.Exception(OOPS)' raised in ...
                   Task = def throw_exceptions_here(...):
                   Job  = [None -> a.start]

                Traceback (most recent call last):
                  File "/usr/local/lib/python2.7/dist-packages/ruffus/task.py", line 685, in run_pooled_job_without_exceptions
                    return_value =  job_wrapper(param, user_defined_work_func, register_cleanup, touch_files_only)
                  File "/usr/local/lib/python2.7/dist-packages/ruffus/task.py", line 549, in job_wrapper_output_files
                    job_wrapper_io_files(param, user_defined_work_func, register_cleanup, touch_files_only, output_files_only = True)
                  File "/usr/local/lib/python2.7/dist-packages/ruffus/task.py", line 504, in job_wrapper_io_files
                    ret_val = user_defined_work_func(*(param[1:]))
                  File "<stdin>", line 3, in throw_exceptions_here
                Exception: OOPS


        .. image:: ../../images/manual_exceptions.png


.. _new_manual.exceptions.multiple_errors:

.. index:: signalling, interrupts, break, errors, exceptions, multiple errors

****************************************************************
Pipelines running in parallel accumulate Exceptions
****************************************************************

    As show above, by default *Ruffus* accumulates ``NN`` exceptions before interrupting the pipeline prematurely where
    ``NN`` is the specified parallelism for :ref:`pipeline_run(multiprocess = NN) <pipeline_functions.pipeline_run>`

    This seems a fair tradeoff between being able to gather detailed error information for
    running jobs, and not wasting too much time for a task that is going to fail anyway.


****************************************************************
Terminate pipeline immediately upon Exceptions
****************************************************************


==============================================================================================================================
Set :ref:`pipeline_run(exceptions_terminate_immediately = True) <pipeline_functions.pipeline_run>`
==============================================================================================================================

    To have all exceptions interrupt the pipeline immediately, invoke:

        .. code-block:: python

            pipeline_run(exceptions_terminate_immediately = True)


    For example, with this change, only a single exception will be thrown before the pipeline is interrupted:

        .. code-block:: python

            from ruffus import *

            @originate(["a.start", "b.start", "c.start", "d.start", "e.start"])
            def throw_exceptions_here(output_file):
                raise Exception("OOPS")

            pipeline_run(multiprocess = 2, exceptions_terminate_immediately = True)

    .. code-block:: pycon
        :emphasize-lines: 5, 21

            >>> pipeline_run(multiprocess = 2)

            ruffus.ruffus_exceptions.RethrownJobError:

            Original exception:

                Exception #1
                  'exceptions.Exception(OOPS)' raised in ...
                   Task = def throw_exceptions_here(...):
                   Job  = [None -> a.start]

                Traceback (most recent call last):
                  [Tedious traceback snipped out!!!....]
                Exception: OOPS


==============================================================================================================================
raise ``Ruffus.JobSignalledBreak``
==============================================================================================================================

    The same can be accomplished on a finer scale by throwing the ``Ruffus.JobSignalledBreak`` Exception. Unlike
    other exceptions, this causes an immediate halt in pipeline execution. If there are other exceptions in play at that
    point, they will be rethrown in the main process but no new exceptions will be added.

        .. code-block:: python

            from ruffus import *

            @originate(["a.start", "b.start", "c.start", "d.start", "e.start"])
            def throw_exceptions_here(output_file):
                raise JobSignalledBreak("OOPS")

            pipeline_run(multiprocess = 2)


****************************************************************
Display exceptions as they occur
****************************************************************

    In the following example, the jobs throw exceptions
    at two second staggered intervals into the job. With ``log_exceptions = True``, the
    exceptions are displayed as they occur even though the pipeline continues running.

    logger.error(...) will be invoked with the string representation of the each exception, and associated stack trace.

    The default logger prints to sys.stderr, but as usual can be changed to any class from the logging module or compatible object via
    :ref:`pipeline_run(logger = XXX) <pipeline_functions.pipeline_run>`


        .. code-block:: python

            from ruffus import *
            import time, os

            @originate(["1.start", "2.start", "3.start", "4.start", "5.start"])
            def throw_exceptions_here(output_file):
                delay = int(os.path.splitext(output_file)[0])
                time.sleep(delay * 2)
                raise JobSignalledBreak("OOPS")

            pipeline_run(log_exceptions = True, multiprocess = 5)




