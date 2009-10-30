.. _manual_9th_chapter:

###################################################################
Step 9: Logging messages with *Ruffus*
###################################################################
* :ref:`Up <manual>` 
* :ref:`Prev <manual_8th_chapter>` 
* :ref:`Next <manual_10th_chapter>` 
* :ref:`logging<ruffus.logging>` syntax in detail

***************************************
Logging
***************************************

=================================
Logging task/job completion
=================================
    *Ruffus* logs each task and each job as it is completed. The results of each
    of the examples in this tutorial were produced by default logging to ``stderr``.
    
    You can specify your own logging by providing a log object  to ``pipeline_run``.
    This log object should have ``debug()`` and ``info()`` methods.
    
    Instead of writing your own, it is usually more convenient to use the python
    `logging <http://docs.python.org/library/logging.html>`_
    module which provides logging classes with rich functionality::
    
    
    
        import logging
        import logging.handlers
        
        LOG_FILENAME = '/tmp/ruffus.log'
        
        # Set up a specific logger with our desired output level
        my_ruffus_logger = logging.getLogger('My_Ruffus_logger')
        my_ruffus_logger.setLevel(logging.DEBUG)
        
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME, maxBytes=2000, backupCount=5)
        
        my_ruffus_logger.addHandler(handler)
        
        
        from ruffus import *
        
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            """Description: Create the file if it does not exists"""
            open(output_file, "w")
        
        pipeline_run([create_if_necessary], [create_if_necessary], logger=my_ruffus_logger)
        print open("/tmp/ruffus.log").read()

        
    .. ???

    The contents of ``/tmp/ruffus.log`` are, as expected::
    
        Task = create_if_necessary
            Description: Create the file if it does not exists
            Job = [null -> "a.1"] completed

=======================================
Your own logging *within* each job
=======================================

    It is often useful to log the progress within each job.
    
    However, each job runs in a separate process, and it is *not* a good
    idea to pass the logging object itself between jobs:
    
    #) logging is not synchronised between processes
    #) `logging <http://docs.python.org/library/logging.html>`_ objects can not be 
       `pickle <http://docs.python.org/library/pickle.html>`_\ d and sent across processes
        
    The best thing to do is to have a centralised log and to have each job invoke the
    logging methods (e.g. `debug`, `warning`, `info` etc.) across the process boundaries in
    the centralised log.
    
    :ref:`This example <sharing-data-across-jobs-example>` shows how this can be coded.
    
    The :ref:`proxy_logger <proxy-logger>` module also provides an easy way to share 
    `logging <http://docs.python.org/library/logging.html>`_ objects among
    jobs. This requires just two simple steps:
    
    
-------------------------------------
    1. Set up log from config file
-------------------------------------
    ::
    
        from ruffus.proxy_logger import *
        (logger_proxy, 
         logging_mutex) = make_shared_logger_and_proxy (setup_std_shared_logger, 
                                                        "my_logger", 
                                                        {"file_name" :"/my/lg.log"})
                                                        
-------------------------------------
    2. Give each job proxy to logger
-------------------------------------
        Now, pass:
        
            * ``logger_proxy`` (which forwards logging calls across jobs) and
            * ``logging_mutex`` (which prevents different jobs which are logging simultaneously 
              from being jumbled up) 
            
        to each job::
    
            @files(None, 'a.1', logger_proxy, logging_mutex)
            def task1(ignore_infile, outfile, logger_proxy, logging_mutex):
                """
                Log within task
                """
                open(outfile, "w").write("Here we go")
                with logging_mutex:
                    logger.proxy.info("Here we go logging")

