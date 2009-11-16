.. _manual_16th_chapter_code:
.. _manual.logging_code:

########################################################################################
Code for Chapter 16: Logging progress through a pipeline
########################################################################################
    * :ref:`Manual overview <manual>` 
    * :ref:`Back <manual.logging.per_job>` 

    This example shows how to log messages from within each of your pipelined functions.
              
    
************************************
Code
************************************
    ::

        
        from ruffus import *
        from ruffus.proxy_logger import *
        import logging
        
        import sys,os
        # use simplejson in place of json for python < 2.6
        try:
            import json
        except ImportError:
            import simplejson
            json = simplejson
        
            
        
        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        
        #   Shared logging
        
        
        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        
        logger_args={}
        logger_args["file_name"] = "pipeline.log"
        logger_args["level"] = logging.DEBUG
        logger_args["rotating"] = True
        logger_args["maxBytes"]=20000
        logger_args["backupCount"]=10
        logger_args["formatter"]="%(asctime)s - %(name)s - %(levelname)6s - %(message)s"
    
        (logger_proxy, 
         logging_mutex) = make_shared_logger_and_proxy (setup_std_shared_logger, 
                                                        "my_logger", logger_args)
    
        
        
            
            
        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        
        #   Helper Function which writes to a shared log
        
        
        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        
        import time
        def test_job_io(infiles, outfiles, extra_params):
            """
            cat input files content to output files
                after writing out job parameters
            """
            #
            # dump parameters
            params = (infiles, outfiles)# + extra_params[0:-3]
            #
            logger_proxy, logging_mutex = extra_params
            with logging_mutex:
                logger_proxy.debug("job = %s, process name = %s" % 
                                    (json.dumps(params),
                                        multiprocessing.current_process().name))
            #
            #
            sys.stdout.write('    job = %s\n' % json.dumps(params))
            #
            if isinstance(infiles, str):
                infiles = [infiles]
            elif infiles == None:
                infiles = []
            if isinstance(outfiles, str):
                outfiles = [outfiles]
            output_text = list()
            for f in infiles:
                output_text.append(open(f).read())
            output_text = "".join(sorted(output_text))
            output_text += json.dumps(infiles) + " -> " + json.dumps(outfiles) + "\n"
            for f in outfiles:
                open(f, "w").write(output_text)
            time.sleep(1)
        
            
        
        
        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        
        #   Tasks
        
        
        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        
        #
        #    task1
        #
        @files(None, 'a.1', logger_proxy, logging_mutex)
        def task1(infiles, outfiles, *extra_params):
            """
            First task
            """
            test_job_io(infiles, outfiles, extra_params)
        
        
        
        #
        #    task2
        #
        @transform(task1, regex('.1'), '.2', logger_proxy, logging_mutex)
        def task2(infiles, outfiles, *extra_params):
            """
            Second task
            """
            test_job_io(infiles, outfiles, extra_params)
        
        
        
        #
        #    task3
        #
        @transform(task2, regex('.2'), '.3', logger_proxy, logging_mutex)
        def task3(infiles, outfiles, *extra_params):
            """
            Third task
            """
            test_job_io(infiles, outfiles, extra_params)
        
        
        
        #
        #    task4
        #
        @transform(task3, regex('.3'), '.4', logger_proxy, logging_mutex)
        def task4(infiles, outfiles, *extra_params):
            """
            Fourth task
            """
            test_job_io(infiles, outfiles, extra_params)
        

        # 
        #   Necessary to protect the "entry point" of the program under windows.
        #       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
        #
        pipeline_run([task4], multiprocess = 10, logger = logger_proxy)
            

************************************
Resulting Output
************************************
    ::
    
        >>> pipeline_run([task4], multiprocess = 10, logger = logger_proxy)
            job = [null, "a.1"]
            job = ["a.1", "a.2"]
            job = ["a.2", "a.3"]
            job = ["a.3", "a.4"]

    Pipeline.log will contain our unimaginative log messages:
    
    ::

        2009-11-15 03:04:55,884 - my_logger -  DEBUG - job = [null, "a.1"], process name = PoolWorker-2
        2009-11-15 03:04:56,941 - my_logger -   INFO -     Job = [None -> a.1, <LoggingProxy>, <thread.lock>] completed
        2009-11-15 03:04:56,942 - my_logger -   INFO - Completed Task = task1
        2009-11-15 03:04:56,945 - my_logger -  DEBUG - job = ["a.1", "a.2"], process name = PoolWorker-4
        2009-11-15 03:04:57,962 - my_logger -   INFO -     Job = [a.1 -> a.2, <LoggingProxy>, <thread.lock>] completed
        2009-11-15 03:04:57,962 - my_logger -   INFO - Completed Task = task2
        2009-11-15 03:04:57,965 - my_logger -  DEBUG - job = ["a.2", "a.3"], process name = PoolWorker-3
        2009-11-15 03:04:59,009 - my_logger -   INFO -     Job = [a.2 -> a.3, <LoggingProxy>, <thread.lock>] completed
        2009-11-15 03:04:59,010 - my_logger -   INFO - Completed Task = task3
        2009-11-15 03:04:59,013 - my_logger -  DEBUG - job = ["a.3", "a.4"], process name = PoolWorker-5
        2009-11-15 03:05:00,024 - my_logger -   INFO -     Job = [a.3 -> a.4, <LoggingProxy>, <thread.lock>] completed
        2009-11-15 03:05:00,025 - my_logger -   INFO - Completed Task = task4

