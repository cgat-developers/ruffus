.. include:: ../../global.inc
.. include:: chapter_numbers.inc

.. _manual.jobs_limit:

####################################################################################################################
|manual.jobs_limit.chapter_num|: `Manage concurrency for a specific task with` **@jobs_limit**
####################################################################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 
        * :ref:`@jobs_limit <decorators.jobs_limit>` syntax in detail

    .. index:: 
        pair: @jobs_limit; Manual
    

=================
**@jobs_limit**
=================
    
    Calling :ref:`pipeline_run(multiprocess = NNN)<pipeline_functions.pipeline_run>` allows
    multiple jobs (from multiple independent tasks) to be run in parallel. However, there
    are some operations which consume so many resources that we might want them to run
    with less or no concurrency.
    
    For example, we might want to download some files via FTP but the server restricts 
    requests from each IP address. Even if the rest of the pipeline is running 100 jobs in
    parallel, the FTP downloading must be restricted to 2 files at a time. We would really
    like to keep the pipeline running as is, but let this one operation run either serially,
    or with little concurrency.
    

    If setting ``multiprocess = NNN`` sets the pipeline-wide concurrency to ``NNN``, then
    ``@jobs_limit(MMM)`` sets concurrency at a much finer level, at ``MMM`` just for jobs
    in the indicated task.
    
    The optional name (e.g. ``@jobs_limit(3, "ftp_download_limit")``) allows the same limit to
    be shared across multiple tasks. To be pedantic: a limit of ``3`` jobs at a time would be applied
    across all tasks which have a ``@jobs_limit`` named ``"ftp_download_limit"``:

        ::
    
            from ruffus import *
            
            # make list of 10 files
            @split(None, "*stage1")
            def make_files(input_file, output_files):
                for i in range(10):
                    if i < 5:
                        open("%d.small_stage1" % i, "w")
                    else:
                        open("%d.big_stage1" % i, "w")
                
            @jobs_limit(3, "ftp_download_limit")
            @transform(make_files, suffix(".small_stage1"), ".stage2")
            def stage1_small(input_file, output_file):
                open(output_file, "w")

            @jobs_limit(3, "ftp_download_limit")
            @transform(make_files, suffix(".big_stage1"), ".stage2")
            def stage1_big(input_file, output_file):
                open(output_file, "w")
    
            @jobs_limit(5)
            @transform([stage1_small, stage1_big], suffix(".stage2"), ".stage3")
            def stage2(input_file, output_file):
                open(output_file, "w")

            pipeline_run([stage2], multiprocess = 10)

        will run the 10 jobs of ``stage1_big`` and ``stage1_small`` 3 at a time (highlighted in blue), 
        a limit shared across the two tasks. ``stage2`` jobs run 5 at a time (in red). 
        These limits override the numbers set in ``pipeline_run`` (``multiprocess = 10``):
        
            .. image:: ../../images/jobs_limit2.png
        
        

