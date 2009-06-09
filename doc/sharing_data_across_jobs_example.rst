.. _sharing-data-across-jobs-example:

################################################
How to share data across jobs
################################################

*****************************************
Python Code
*****************************************
The full code is available :ref:`here <code-for-sharing-data-across-jobs-example.rst>`.

.. index:: 
    single: Example Programme; 4. Sharing data across parallel jobs

***************************************************
Background:
***************************************************

    Each *Ruffus* job runs in a separate process. 
    To synchronise across multiple jobs requires passing data across processes.
    
    `This is generally to be avoided <http://docs.python.org/library/multiprocessing.html#programming-guidelines>`_ because
    
    1) Synchronising across parallel tasks is inherently tricky
    2) Passing large amounts of data across processes is inefficient
    3) Some objects are not suitable for passing across the process boundary.
    
    For more information, see the documentation for the python
    `multiprocessing module <http://docs.python.org/library/multiprocessing.html>`_.


***************************************************
Aim: 
***************************************************
    We create a shared python `logging <http://docs.python.org/library/logging.html>`_ 
    object. All the jobs will write to this log without trampling over each other.
    
    This programme demonstrates 

    * calling functions in shared objects from different jobs
    * synchronising calls to prevent them from being mixed up
     

=======================================
Create the shared object
=======================================

    The object which will be shared between the jobs will be created in a separate
    Manager Server Process (See `Server Process <http://docs.python.org/library/multiprocessing.html#sharing-state-between-processes>`_)
    
    We need to write a function which will be called in this process::

        #
        #   Create logger object
        #
        def setup_shared_logger(LOGGING_LEVEL, LOG_FILENAME):
            """
            Function to setup logger shared between all processes
            The logger object will be created within a separate (special) process 
                run by multiprocessing.BaseManager.start()
            """
        
            #
            #   Log file name with logger level
            # 
            my_ruffus_logger = logging.getLogger('simpler_example_logger')
            my_ruffus_logger.setLevel(LOGGING_LEVEL)
        
            # 
            #   Add handler to print to file, with the specified format  
            #
            handler = logging.handlers.RotatingFileHandler(
                          LOG_FILENAME, maxBytes=100000, backupCount=5)

            return my_ruffus_logger

=========================================================
Create proxies to forward calls to the shared object
=========================================================

    We then need to specify proxy objects which will forward function calls to the
    real (shared) object which is owned by the Manager Server Process::

        #
        #   Proxy object for logging
        #       Logging messages will be marshalled (forwarded) to the process where the 
        #       shared log lives
        #
        class LoggerProxy(multiprocessing.managers.BaseProxy):
            def debug(self, message):
                return self._callmethod('debug', [message])
            def info(self, message):
                return self._callmethod('info', [message])
            def __str__ (self):
                return "Logging proxy"

    In this case, we are only interested in two function calls to forward: `debug` and
    `info`. We also override the `__str__` function so that *ruffus* output looks nicer.
    

=========================================================
Register proxy and shared object with Manager Server
=========================================================

    Now we need to tell the multiprocessing library how to create our shared object,
    and forward calls from the proxies::
    
        # 
        #   Register the setup_logger function as a proxy for setup_logger
        #   
        #   We use SyncManager as a base class so we can get a lock proxy for synchronising 
        #       logging later on
        #
        class LoggingManager(multiprocessing.managers.SyncManager):
            """
            Logging manager sets up its own process and will create the real Log object there
            We refer to this (real) log via proxies
            """
            pass
        LoggingManager.register('setup_logger', setup_shared_logger, proxytype=LoggerProxy, exposed = ('info', 'debug', '__str__'))
        

    We link the proxy by creating an instance of `SyncManager <http://docs.python.org/library/multiprocessing.html#multiprocessing.managers.SyncManager>`_.

    We could also have used `multiprocessing::BaseManager <http://docs.python.org/library/multiprocessing.html#multiprocessing.managers.BaseManager>`_
    but `SyncManager <http://docs.python.org/library/multiprocessing.html#multiprocessing.managers.SyncManager>`_ 
    includes the `Lock()` function which we shall use to synchronise the writing to the
    log.
    

=========================================================
Create Manager Server Process
=========================================================

    We need to create the Manager Server Process, the logs and the proxy::

        if __name__ == '__main__':
        
            #
            #   make shared log and proxy 
            #
            manager = LoggingManager()
            manager.register('setup_logger', setup_shared_logger, 
                             proxytype=LoggerProxy, exposed = ('info', 'debug'))
            
            manager.start()
            LOG_FILENAME  = options.log_file_name
            LOGGING_LEVEL = logging.DEBUG
            logger_proxy = manager.setup_logger(LOGGING_LEVEL, LOG_FILENAME)
            
            #
            #   make sure we are not logging at the same time in different processes
            #
            logging_mutex = manager.Lock()


=========================================================
Run *ruffus*
=========================================================

    The shared proxy can be passed to the task function::


        @files(None, 'a.1', logger_proxy, logging_mutex)
        def task1(no_infile, outfile, *extra_params):

            # Synchronised logging
            logger_proxy, logging_mutex = extra_params
            with logging_mutex:
                logger_proxy.debug("task1, process name = %s" % 
                                    (multiprocessing.current_process().name))

            # do actual work
            do_some_hard_task(outfile)
            

    
    Because ``logging_mutex`` is used, log entries will not be jumbled up or interleaved.
