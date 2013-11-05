.. include:: ../../global.inc
.. include:: chapter_numbers.inc

.. _manual.logging:

###################################################################################################
|manual.logging.chapter_num|: `Logging progress through a pipeline`
###################################################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 

    
    .. index:: 
        pair: Logging; Manual
    

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
    
        Because **Ruffus** may run these in separate process (multiprocessing), some
        attention has to be paid to how to send and synchronise your log messages
        across process boundaries.
        
    
    We shall deal with these in turn.


.. _manual.logging.pipeline:

=================================
Logging task/job completion
=================================
    By default, *Ruffus* logs each task and each job as it is completed to
    ``sys.stderr``. 
    
    :ref:`pipeline_run() <pipeline_functions.pipeline_run>`  includes an optional ``logger`` parameter which defaults to
    ``stderr_logger``. Set this to ``black_hole_logger`` to turn off all tracking messages as
    the pipeline runs:
    
        ::
                
            pipeline_run([pipelined_task], logger = black_hole_logger)
            

**********************************
Controlling logging verbosity
**********************************
    :ref:`pipeline_run() <pipeline_functions.pipeline_run>` currently has five levels of verbosity, set by the optional ``verbose``
    parameter which defaults to 1:
    
        ::
        
                verbose = 0: nothing
                verbose = 1: logs completed jobs/tasks; 
                verbose = 2: logs up to date jobs in incomplete tasks
                verbose = 3: logs reason for running job
                verbose = 4: logs messages useful only for debugging ruffus pipeline code


        ``Verbose`` > 2 are intended for debugging **Ruffus** by the developers and the details
        are liable to change from release to release

    
**********************************
Using your own logging
**********************************
    You can specify your own logging by providing a log object  to :ref:`pipeline_run() <pipeline_functions.pipeline_run>` .
    This log object should have ``debug()`` and ``info()`` methods.
    
    Instead of writing your own, it is usually more convenient to use the python
    `logging <http://docs.python.org/library/logging.html>`_
    module which provides logging classes with rich functionality. The following sets up
    a logger to a rotating set of files:

        ::
    
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
    

    The contents of ``/tmp/ruffus.log`` are as specified:
        ::
    
            Task = create_if_necessary
                Description: Create the file if it does not exists
                Job = [null -> "a.1"] completed
    
.. _manual.logging.per_job:

=======================================
Your own logging *within* each job
=======================================

    It is often useful to log the messages from within each of your pipelined functions.
    
    However, each job runs in a separate process, and it is *not* a good
    idea to pass the logging object itself between jobs:
    
    #. logging is not synchronised between processes
    #. `logging <http://docs.python.org/library/logging.html>`_ objects can not be 
       `pickle <http://docs.python.org/library/pickle.html>`_\ d and sent across processes
        
    The best thing to do is to have a centralised log and to have each job invoke the
    logging methods (e.g. `debug`, `warning`, `info` etc.) across the process boundaries in
    the centralised log.
    
    The **Ruffus** :ref:`proxy_logger <proxy-logger>` module provides an easy way to share 
    `logging <http://docs.python.org/library/logging.html>`_ objects among
    jobs. This requires just two simple steps:

    .. note::    
        :ref:`The full code <manual.logging_code>` shows how this can be coded.
    
    
    
****************************************
    1. Set up log from config file
****************************************
    ::
    
        from ruffus.proxy_logger import *
        (logger_proxy, 
         logging_mutex) = make_shared_logger_and_proxy (setup_std_shared_logger, 
                                                        "my_logger", 
                                                        {"file_name" :"/my/lg.log"})
                                                        
****************************************
    2. Give each job proxy to logger
****************************************
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
                    logger_proxy.info("Here we go logging")

