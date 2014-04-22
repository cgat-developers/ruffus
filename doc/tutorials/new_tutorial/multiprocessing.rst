.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: multiprocessing; Tutorial

.. _new_manual.multiprocessing:

####################################################################################################################################################
|new_manual.multiprocessing.chapter_num|: Multiprocessing, ``drmaa`` and Computation Clusters
####################################################################################################################################################


.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`@jobs_limit <decorators.jobs_limit>` syntax
    * :ref:`pipeline_run() <pipeline_functions.pipeline_run>` syntax
    * :ref:`drmaa_wrapper.run_job() <drmaa_wrapper.run_job>` syntax

.. note::

    Remember to look at the example code:

        * :ref:`new_manual.multiprocessing.code`

***********************
Overview
***********************

.. index::
    pair: pipeline_run(multiprocess); Tutorial

=====================
Multi Processing
=====================

    *Ruffus* uses python `multiprocessing <http://docs.python.org/library/multiprocessing.html>`_ to run
    each job in a separate process.

    This means that jobs do *not* necessarily complete in the order of the defined parameters.
    Task hierachies are, of course, inviolate: upstream tasks run before downstream, dependent tasks.

    Tasks that are independent (i.e. do not precede each other) may be run in parallel as well.

    The number of concurrent jobs can be set in :ref:`pipeline_run<pipeline_functions.pipeline_run>`:

        ::

            pipeline_run([parallel_task], multiprocess = 5)


    If ``multiprocess`` is set to 1, then jobs will be run on a single process.



.. index::
    pair: data sharing across processes; Tutorial

=====================
Data sharing
=====================

    Running jobs in separate processes allows *Ruffus* to make full use of the multiple
    processors in modern computers. However, some `multiprocessing guidelines <http://docs.python.org/library/multiprocessing.html#multiprocessing-programming>`_
    should be borne in mind when writing *Ruffus* pipelines. In particular:

    * Try not to pass large amounts of data between jobs, or at least be aware that this has to be marshalled
      across process boundaries.

    * Only data which can be `pickled <http://docs.python.org/library/pickle.html>`_ can be passed as
      parameters to *Ruffus* task functions. Happily, that applies to almost any native Python data type.
      The use of the rare, unpicklable object will cause python to complain (fail) loudly when *Ruffus* pipelines
      are run.



.. index::
    pair: @jobs_limit; Tutorial

.. _new_manual.jobs_limit:


********************************************************************************************
Restricting parallelism with :ref:`@jobs_limit <decorators.jobs_limit>`
********************************************************************************************

    Calling :ref:`pipeline_run(multiprocess = NNN)<pipeline_functions.pipeline_run>` allows
    multiple jobs (from multiple independent tasks) to be run in parallel. However, there
    are some operations that consume so many resources that we might want them to run
    with less or no concurrency.

    For example, we might want to download some files via FTP but the server restricts
    requests from each IP address. Even if the rest of the pipeline is running 100 jobs in
    parallel, the FTP downloading must be restricted to 2 files at a time. We would really
    like to keep the pipeline running as is, but let this one operation run either serially,
    or with little concurrency.


    * :ref:`pipeline_run(multiprocess = NNN)<pipeline_functions.pipeline_run>` sets the pipeline-wide concurrency but
    * :ref:`@jobs_limit(MMM)<decorators.jobs_limit>` sets concurrency at ``MMM`` only for jobs in the decorated task.

    The optional name (e.g. ``@jobs_limit(3, "ftp_download_limit")``) allows the same limit to
    be shared across multiple tasks. To be pedantic: a limit of ``3`` jobs at a time would be applied
    across all tasks which have a ``@jobs_limit`` named ``"ftp_download_limit"``.

    The :ref:`example code<new_manual.multiprocessing.code>` uses up to 10 processes across the
    pipeline, but runs the ``stage1_big`` and ``stage1_small`` tasks 3 at a time (shared across
    both tasks). ``stage2`` jobs run 5 at a time.



.. _new_manual.ruffus.drmaa_wrapper.run_job:

********************************************************************************************
Using ``drmaa`` to dispatch work to Computational Clusters or Grid engines from Ruffus jobs
********************************************************************************************

    Ruffus has been widely used to manage work on computational clusters or grid engines. Though Ruffus
    task functions cannot (yet!) run natively and transparently on remote cluster nodes, it is trivial
    to dispatch work across the cluster.

    From version 2.4 onwards, Ruffus includes an optional helper module which interacts with
    `python bindings  <https://github.com/drmaa-python/drmaa-python>`__ for the widely used `drmaa  <http://en.wikipedia.org/wiki/DRMAA>`__
    Open Grid Forum API specification. This allows jobs to dispatch work to a computational cluster and wait until it completes.


    Here are the necessary steps

==============================================================================
1) Use a shared drmaa session:
==============================================================================

    Before your pipeline runs:

    .. code-block:: python

        #
        #   start shared drmaa session for all jobs / tasks in pipeline
        #
        import drmaa
        drmaa_session = drmaa.Session()
        drmaa_session.initialize()


    Cleanup after your pipeline completes:

    .. code-block:: python

        #
        #   pipeline functions go here
        #
        if __name__ == '__main__':
            drmaa_session.exit()


==============================================================================
2) import ``ruffus.drmaa_wrapper``
==============================================================================

    * The optional ``ruffus.drmaa_wrapper`` module needs to be imported explicitly:

    .. code-block:: python
        :emphasize-lines: 1

        # imported ruffus.drmaa_wrapper explicitly
        from ruffus.drmaa_wrapper import run_job, error_drmaa_job


==============================================================================
3) call :ref:`drmaa_wrapper.run_job()<drmaa_wrapper.run_job>`
==============================================================================

    :ref:`drmaa_wrapper.run_job() <drmaa_wrapper.run_job>` dispatches the work to a cluster node within a normal Ruffus job and waits for completion

    This is the equivalent of `os.system  <http://docs.python.org/2/library/os.html#os.system>`__  or
    `subprocess.check_output  <http://docs.python.org/2/library/subprocess.html#subprocess.check_call>`__ but the code will run remotely as specified:

        .. code-block:: python
            :emphasize-lines: 1

                # ruffus.drmaa_wrapper.run_job
                stdout_res, stderr_res  = run_job(cmd_str           = "touch " + output_file,
                                                  job_name          = job_name,
                                                  logger            = logger,
                                                  drmaa_session     = drmaa_session,
                                                  run_locally       = options.local_run,
                                                  job_other_options = job_other_options)

        The complete code is available :ref:`here <using_ruffus.drmaa_wrapper>`

    * :ref:`drmaa_wrapper.run_job() <drmaa_wrapper.run_job>` is a convenience wrapper around the `python drmaa bindings <https://github.com/drmaa-python/drmaa-python>`__
      `RunJob <http://drmaa-python.readthedocs.org/en/latest/tutorials.html#waiting-for-a-job>`__ function.
      It takes care of writing drmaa *job templates* for you.
    * Each call creates a separate drmaa *job template*.

==================================================================================================
4) Use multithread: :ref:`pipeline_run(multithread = NNN) <pipeline_functions.pipeline_run>`
==================================================================================================

    .. warning ::

        :ref:`drmaa_wrapper.run_job()<drmaa_wrapper.run_job>`

            **requires** ``pipeline_run`` :ref:`(multithread = NNN)<pipeline_functions.pipeline_run>`

            **and will not work with**  ``pipeline_run`` :ref:`(multiprocess = NNN)<pipeline_functions.pipeline_run>`


    Using multithreading rather than multiprocessing
        * allows the drmaa session to be shared
        * prevents "processing storms" which lock up the queue submission node when hundreds or thousands of grid engine / cluster commands complete at the same time.

        .. code-block:: python

            pipeline_run (..., multithread = NNN, ...)

        or if you are using ruffus.cmdline:

        .. code-block:: python

            cmdline.run (options, multithread = options.jobs)


    Normally multithreading reduces the amount of parallelism in python due to the python `Global interpreter Lock (GIL)  <http://en.wikipedia.org/wiki/Global_Interpreter_Lock>`__.
    However, as the work load is almost entirely on another computer (i.e. a cluster / grid engine node) with a separate python interpreter, any cost benefit calculations of this sort are moot.

==================================================================================================
5) Develop locally
==================================================================================================

    :ref:`drmaa_wrapper.run_job() <drmaa_wrapper.run_job>` provides two convenience parameters for developing grid engine pipelines:

    * commands can run locally, i.e. on the local machine rather than on cluster nodes:

          .. code-block:: python

              run_job(cmd_str, run_locally = True)

    * Output files can be `touch  <http://en.wikipedia.org/wiki/Touch_(Unix)>`__\ed, i.e. given the appearance of the work having being done without actually running the commands

          .. code-block:: python

              run_job(cmd_str, touch_only = True)


.. index::
    pair: pipeline_run touch mode; Tutorial
    pair: touch mode pipeline_run; Tutorial

.. _new_manual.pipeline_run_touch:


********************************************************************************************
Forcing a pipeline to appear up to date
********************************************************************************************

    Sometimes, we *know* that a pipeline has run to completion, that everything is up-to-date. However, Ruffus still insists on the basis
    of file modification times that you need to rerun.

    For example, sometimes a trivial accounting modification needs to be made to a data file.
    Even though you know that this changes nothing in practice, Ruffus will detect the modification and
    ask to rerun everything from that point forwards.

    One way to convince Ruffus that everything is fine is to manually `touch  <http://en.wikipedia.org/wiki/Touch_(Unix)>`__
    all subsequent data files one by one in sequence so that the file timestamps follow the appropriate progression.

    You can also ask *Ruffus* to do this automatically for you by running the pipeline in `touch  <http://en.wikipedia.org/wiki/Touch_(Unix)>`__
    mode:

        .. code-block:: python

            pipeline_run( touch_files_only = True)


    :ref:`pipeline_run <pipeline_functions.pipeline_run>` will run your pipeline script normally working backwards from any specified final target, or else the
    last task in the pipeline. It works out where it should begin running, i.e. with the first out-of-date data files.
    After that point, instead of calling your pipeline task functions, each missing or out-of-date file is
    `touch-ed  <http://en.wikipedia.org/wiki/Touch_(Unix)>`__ in turn so that the file modification dates
    follow on successively.


    This turns out to be useful way to check that your pipeline runs correctly by creating a series of dummy (empty files).
    However, *Ruffus* does not know how to read your mind to know which files to create from :ref:`@split <decorators.split>` or
    :ref:`@subdivide <decorators.subdivide>` tasks.


    Using :ref:`ruffus.cmdline <new_manual.cmdline>` from version 2.4, you can just specify:

        .. code-block:: bash

            your script --touch_files_only [--other_options_of_your_own_etc]

