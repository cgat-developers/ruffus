.. include:: global.inc
.. _drmaa_functions:

.. comments: function name

.. |run_job| replace:: `drmaa_wrapper.run_job`
.. _run_job: `drmaa_wrapper.run_job`_

.. comments: parameters

.. |dw_cmd_str| replace:: `cmd_str`
.. _dw_cmd_str: `drmaa_wrapper.run_job.cmd_str`_

.. |dw_job_script_directory| replace:: `job_script_directory`
.. _dw_job_script_directory: `drmaa_wrapper.run_job.job_script_directory`_
.. |dw_job_environment| replace:: `job_environment`
.. _dw_job_environment: `drmaa_wrapper.run_job.job_environment`_
.. |dw_working_directory| replace:: `working_directory`
.. _dw_working_directory: `drmaa_wrapper.run_job.working_directory`_
.. |dw_retain_job_scripts| replace:: `retain_job_scripts`
.. _dw_retain_job_scripts: `drmaa_wrapper.run_job.retain_job_scripts`_
.. |dw_job_name| replace:: `job_name`
.. _dw_job_name: `drmaa_wrapper.run_job.job_name`_
.. |dw_job_other_options| replace:: `job_other_options`
.. _dw_job_other_options: `drmaa_wrapper.run_job.job_other_options`_
.. |dw_logger| replace:: `logger`
.. _dw_logger: `drmaa_wrapper.run_job.logger`_
.. |dw_drmaa_session| replace:: `drmaa_session`
.. _dw_drmaa_session: `drmaa_wrapper.run_job.drmaa_session`_
.. |dw_run_locally| replace:: `run_locally`
.. _dw_run_locally: `drmaa_wrapper.run_job.run_locally`_
.. |dw_output_files| replace:: `output_files`
.. _dw_output_files: `drmaa_wrapper.run_job.output_files`_
.. |dw_touch_only| replace:: `touch_only`
.. _dw_touch_only: `drmaa_wrapper.run_job.touch_only`_


################################################
drmaa functions
################################################

    ``drmaa_wrapper`` is not exported automatically by ruffus and must be specified explicitly:

        .. code-block:: python
            :emphasize-lines: 1


            # imported ruffus.drmaa_wrapper explicitly
            from ruffus.drmaa_wrapper import run_job, error_drmaa_job

.. _drmaa_wrapper.run_job:

.. index::
    single: drmaa ; run_job
    pair: run_job; Run drmaa


************************************************************************************************************************************************************************************************************************************************************************************
*run_job*
************************************************************************************************************************************************************************************************************************************************************************************
**run_job** (|dw_cmd_str|_, |dw_job_name|_ = None, |dw_job_other_options|_ = None, |dw_job_script_directory|_ = None, |dw_job_environment|_ = None, |dw_working_directory|_ = None, |dw_logger|_ = None, |dw_drmaa_session|_ = None, |dw_retain_job_scripts|_ = False, |dw_run_locally|_ = False, |dw_output_files|_ = None, |dw_touch_only|_ = False)

    **Purpose:**

        ``ruffus.drmaa_wrapper.run_job`` dispatches a command with arguments to a cluster or Grid Engine node and waits for the command to complete.

        It is the semantic equivalent of calling `os.system  <http://docs.python.org/2/library/os.html#os.system>`__  or
        `subprocess.check_output  <http://docs.python.org/2/library/subprocess.html#subprocess.check_call>`__.

    **Example**:

        .. code-block:: python

            from ruffus.drmaa_wrapper import run_job, error_drmaa_job
            import drmaa
            my_drmaa_session = drmaa.Session()
            my_drmaa_session.initialize()

            run_job("ls",
                    job_name = "test",
                    job_other_options="-P mott-flint.prja -q short.qa",
                    job_script_directory = "test_dir",
                    job_environment={ 'BASH_ENV' : '~/.bashrc' },
                    retain_job_scripts = True, drmaa_session=my_drmaa_session)
            run_job("ls",
                    job_name = "test",
                    job_other_options="-P mott-flint.prja -q short.qa",
                    job_script_directory = "test_dir",
                    job_environment={ 'BASH_ENV' : '~/.bashrc' },
                    retain_job_scripts = True,
                    drmaa_session=my_drmaa_session,
                    working_directory = "/gpfs1/well/mott-flint/lg/src/oss/ruffus/doc")

            #
            #   catch exceptions
            #
            try:
                stdout_res, stderr_res  = run_job(cmd,
                                                  job_name          = job_name,
                                                  logger            = logger,
                                                  drmaa_session     = drmaa_session,
                                                  run_locally       = options.local_run,
                                                  job_other_options = get_queue_name())

            # relay all the stdout, stderr, drmaa output to diagnose failures
            except error_drmaa_job as err:
                raise Exception("\n".join(map(str,
                                    ["Failed to run:",
                                     cmd,
                                     err,
                                     stdout_res,
                                     stderr_res])))

            my_drmaa_session.exit()



    **Parameters:**

.. _drmaa_wrapper.run_job.cmd_str:

    * *cmd_str*

        The command which will be run remotely including all parameters

.. _drmaa_wrapper.run_job.job_name:

    * *job_name*

        A descriptive name for the command. This will be displayed by `SGE qstat  <http://gridscheduler.sourceforge.net/htmlman/htmlman1/qstat.html>`__, for example.
        Defaults to "ruffus_job"

.. _drmaa_wrapper.run_job.job_other_options:

    * *job_other_options*

        Other drmaa parameters can be passed verbatim as a string.

        Examples for SGE include project name (``-P project_name``), parallel environment (``-pe parallel_environ``), account (``-A account_string``), resource (``-l resource=expression``),
        queue name (``-q a_queue_name``), queue priority (``-p 15``).

        These are parameters which you normally need to include when submitting jobs interactively, for example via
        `SGE qsub  <http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html>`__
        or `SLURM  <http://apps.man.poznan.pl/trac/slurm-drmaa/wiki/WikiStart#Nativespecification>`__ (`srun <https://computing.llnl.gov/linux/slurm/srun.html>`__)

.. _drmaa_wrapper.run_job.job_script_directory:

    * *job_script_directory*

        The directory where drmaa temporary script files will be found. Defaults to the current working directory.


.. _drmaa_wrapper.run_job.job_environment:

    * *job_environment*

        A dictionary of key / values with environment variables. E.g. ``"{'BASH_ENV': '~/.bashrc'}"``


.. _drmaa_wrapper.run_job.working_directory:

    * *working_directory*

        * Sets the working directory.
        * Should be a fully qualified path.
        * Defaults to the current working directory.


.. _drmaa_wrapper.run_job.retain_job_scripts:

    * *retain_job_scripts*

        Do not delete temporary script files containg drmaa commands. Useful for
        debugging, running on the command line directly, and can provide a useful record of the commands.

.. _drmaa_wrapper.run_job.logger:

    * *logger*

        For logging messages indicating the progress of the pipeline in terms of tasks and jobs. Takes objects with the standard python
        `logging  <https://docs.python.org/2/library/logging.html>`__ module interface.

.. _drmaa_wrapper.run_job.drmaa_session:

    * *drmaa_session*

        A shared drmaa session created and managed separately.

        In the main part of your **Ruffus** pipeline script somewhere there should be code looking like this:

        .. code-block:: python

            #
            #   start shared drmaa session for all jobs / tasks in pipeline
            #
            import drmaa
            drmaa_session = drmaa.Session()
            drmaa_session.initialize()


            #
            #   pipeline functions
            #

            if __name__ == '__main__':
                cmdline.run (options, multithread = options.jobs)
                drmaa_session.exit()

.. _drmaa_wrapper.run_job.run_locally:

    * *run_locally*

        Runs commands locally using the standard python `subprocess  <https://docs.python.org/2/library/subprocess.html>`__ module
        rather than dispatching remotely. This allows scripts to be debugged easily

.. _drmaa_wrapper.run_job.touch_only:

    * *touch_only*

        Create or update :ref:`Output files <drmaa_wrapper.run_job.output_files>`
        only to simulate the running of the pipeline.
        Does not dispatch commands remotely or locally. This is most useful to force a
        pipeline to acknowledge that a particular part is now up-to-date.

        See also: :ref:`pipeline_run(touch_files_only=True) <pipeline_functions.pipeline_run.touch_files_only>`


.. _drmaa_wrapper.run_job.output_files:

    * *output_files*

        Output files which will be created or updated if  :ref:`touch_only <drmaa_wrapper.run_job.touch_only>` ``=True``


