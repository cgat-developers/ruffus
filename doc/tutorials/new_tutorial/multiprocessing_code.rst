.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.multiprocessing.code:

################################################################################################################################################################
|new_manual.multiprocessing.chapter_num|: Python Code for Multiprocessing, ``drmaa`` and Computation Clusters
################################################################################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`@jobs_limit <decorators.jobs_limit>` syntax
    * :ref:`pipeline_run() <pipeline_functions.pipeline_run>` syntax
    * :ref:`drmaa_wrapper.run_job() <drmaa_wrapper.run_job>` syntax
    * Back to |new_manual.multiprocessing.chapter_num|: :ref:`Multiprocessing, drmaa and Computation Clusters <new_manual.multiprocessing>`

************************************************************************************
:ref:`@jobs_limit <decorators.jobs_limit>`
************************************************************************************

    * First 2 tasks are constrained to a parallelism of 3 shared jobs at a time
    * Final task is constrained to a parallelism of 5 jobs at a time
    * The entire pipeline is constrained to a (theoretical) parallelism of 10 jobs at a time

    .. code-block:: python
        :emphasize-lines: 12,17,22

        from ruffus import *
        import time

        # make list of 10 files
        @split(None, "*stage1")
        def make_files(input_files, output_files):
            for i in range(10):
                if i < 5:
                    open("%d.small_stage1" % i, "w")
                else:
                    open("%d.big_stage1" % i, "w")

        @jobs_limit(3, "ftp_download_limit")
        @transform(make_files, suffix(".small_stage1"), ".stage2")
        def stage1_small(input_file, output_file):
            print "FTP downloading %s ->Start" % input_file
            time.sleep(2)
            open(output_file, "w")
            print "FTP downloading %s ->Finished" % input_file

        @jobs_limit(3, "ftp_download_limit")
        @transform(make_files, suffix(".big_stage1"), ".stage2")
        def stage1_big(input_file, output_file):
            print "FTP downloading %s ->Start" % input_file
            time.sleep(2)
            open(output_file, "w")
            print "FTP downloading %s ->Finished" % input_file

        @jobs_limit(5)
        @transform([stage1_small, stage1_big], suffix(".stage2"), ".stage3")
        def stage2(input_file, output_file):
            print "Processing stage2 %s ->Start" % input_file
            time.sleep(2)
            open(output_file, "w")
            print "Processing stage2 %s ->Finished" % input_file

        pipeline_run(multiprocess = 10, verbose = 0)


    Giving:

    .. code-block:: pycon
        :emphasize-lines: 3,25

        >>> pipeline_run(multiprocess = 10, verbose = 0)

        >>> # 3 jobs at a time, interleaved
        FTP downloading 5.big_stage1 ->Start
        FTP downloading 6.big_stage1 ->Start
        FTP downloading 7.big_stage1 ->Start
        FTP downloading 5.big_stage1 ->Finished
        FTP downloading 8.big_stage1 ->Start
        FTP downloading 6.big_stage1 ->Finished
        FTP downloading 9.big_stage1 ->Start
        FTP downloading 7.big_stage1 ->Finished
        FTP downloading 0.small_stage1 ->Start
        FTP downloading 8.big_stage1 ->Finished
        FTP downloading 1.small_stage1 ->Start
        FTP downloading 9.big_stage1 ->Finished
        FTP downloading 2.small_stage1 ->Start
        FTP downloading 0.small_stage1 ->Finished
        FTP downloading 3.small_stage1 ->Start
        FTP downloading 1.small_stage1 ->Finished
        FTP downloading 4.small_stage1 ->Start
        FTP downloading 2.small_stage1 ->Finished
        FTP downloading 3.small_stage1 ->Finished
        FTP downloading 4.small_stage1 ->Finished

        >>> # 5 jobs at a time, interleaved
        Processing stage2 0.stage2 ->Start
        Processing stage2 1.stage2 ->Start
        Processing stage2 2.stage2 ->Start
        Processing stage2 3.stage2 ->Start
        Processing stage2 4.stage2 ->Start
        Processing stage2 0.stage2 ->Finished
        Processing stage2 5.stage2 ->Start
        Processing stage2 1.stage2 ->Finished
        Processing stage2 6.stage2 ->Start
        Processing stage2 2.stage2 ->Finished
        Processing stage2 4.stage2 ->Finished
        Processing stage2 7.stage2 ->Start
        Processing stage2 8.stage2 ->Start
        Processing stage2 3.stage2 ->Finished
        Processing stage2 9.stage2 ->Start
        Processing stage2 5.stage2 ->Finished
        Processing stage2 7.stage2 ->Finished
        Processing stage2 6.stage2 ->Finished
        Processing stage2 8.stage2 ->Finished
        Processing stage2 9.stage2 ->Finished

.. _using_ruffus.drmaa_wrapper:

************************************************************************************
Using  ``ruffus.drmaa_wrapper``
************************************************************************************

    .. code-block:: python
        :emphasize-lines: 17,31,53

        #!/usr/bin/python
        job_queue_name    = "YOUR_QUEUE_NAME_GOES_HERE"
        job_other_options = "-P YOUR_PROJECT_NAME_GOES_HERE"

        from ruffus import *
        from ruffus.drmaa_wrapper import run_job, error_drmaa_job

        parser = cmdline.get_argparse(description='WHAT DOES THIS PIPELINE DO?')

        options = parser.parse_args()

        #  logger which can be passed to multiprocessing ruffus tasks
        logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)


        #
        #   start shared drmaa session for all jobs / tasks in pipeline
        #
        import drmaa
        drmaa_session = drmaa.Session()
        drmaa_session.initialize()

        @originate(["1.chromosome", "X.chromosome"],
                   logger, logger_mutex)
        def create_test_files(output_file):
            try:
                stdout_res, stderr_res = "",""
                job_queue_name, job_other_options = get_queue_options()

                #
                #   ruffus.drmaa_wrapper.run_job
                #
                stdout_res, stderr_res  = run_job(cmd_str           = "touch " + output_file,
                                                  job_name          = job_name,
                                                  logger            = logger,
                                                  drmaa_session     = drmaa_session,
                                                  run_locally       = options.local_run,
                                                  job_queue_name    = job_queue_name,
                                                  job_other_options = job_other_options)

            # relay all the stdout, stderr, drmaa output to diagnose failures
            except error_drmaa_job as err:
                raise Exception("\n".join(map(str,
                                    "Failed to run:"
                                    cmd,
                                    err,
                                    stdout_res,
                                    stderr_res)))


        if __name__ == '__main__':
            cmdline.run (options, multithread = options.jobs)
            # cleanup drmaa
            drmaa_session.exit()


