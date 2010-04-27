.. include:: ../../global.inc
.. include:: chapter_numbers.inc

.. _manual.exceptions:

###################################################################################################
|manual.exceptions.chapter_num|: `Exceptions thrown inside a pipeline`
###################################################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 

    
    .. index:: 
        pair: Exceptions; Manual
    

    The goal for **Ruffus** is that exceptions should just work *out-of-the-box* without any fuss.
    This is especially important for exceptions that come from your code which may be raised
    in a different process. Often multiple parallel operations (jobs or tasks) fail at the
    same time. **Ruffus** will forward each of these exceptions with the tracebacks so you
    can jump straight to the offending line.
    
    This example shows separate exceptions from two jobs running in parallel:
    
        .. image:: ../../images/manual_exceptions.png


.. index:: signalling, interrupts, break

.. _interrupting:

=================================
Interrupting the pipeline
=================================

    If your task function raises a ``Ruffus.JobSignalledBreak`` Exception, this will immediately
    halt the pipeline at that point, without waiting for other jobs in the queue to complete:
    
        ::
        
            from ruffus import *
            @parallel([['A', 1], ['B',3]])
            def parallel_task(name, param1):
                if name == 'A': return False
            
            pipeline_run([parallel_task])
        
            

    produces the following (abbreviated):

        ::
        
            task.RethrownJobError:
            
                Exceptions running jobs for
                'def parallel_task(...):'
            
                Original exception:
            
                Exception #1
                task.JobSignalledBreak: Job = ["A", 1] returned False
                for Job = ["A", 1]
        
    
=====================
Multiple Errors
=====================
    For any task where exceptions are thrown, *Ruffus* will continue executing all the jobs
    currently in progress (up to the maximum number of concurrent jobs 
    (``multiprocess``) set in :ref:`pipeline_run <pipeline_functions.pipeline_run>`). 
    Each of these may raise separate exceptions.
    This seems a fair tradeoff between being able to gather detailed error information for
    running jobs, and not wasting too much time for a task that is going to fail anyway.
    
