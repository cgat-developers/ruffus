.. _manual_15th_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run

###################################################################################
Chapter 15: Exceptions thrown inside a pipeline
###################################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 

    
.. index:: 
    single: Exceptions; Manual
    
.. _manual.exceptions:

=====================
Exceptions
=====================
    Python exceptions or syntax errors are gathered from all the parallel jobs before
    being reraised as an aggregate Exception. A full stack trace is provided so that you can
    see where errors occurred.
    
    In the previous example, if the number of parameters is incorrect::
    
        from ruffus import *
        @parallel([['A', 1], ['B',3]])
        def parallel_task(name, param1, param2):
            sys.stderr.write("    Parallel task %s: " % name)
            sys.stderr.write("%d + %d = %d\n" % (param1, param2, param1 + param2))
        
        pipeline_run([parallel_task])
    
        
    .. ???

    This would have produced these detailed error messages for each of the two jobs::
    
        task.RethrownJobError:
        
            Exceptions running jobs for
            'def parallel_task(...):'
        
            Original exceptions:
        
            Exception #1
            exceptions.TypeError: parallel_task() takes exactly 3 arguments (2 given)
            for Job = ["A", 1]
        
            Traceback (most recent call last):
              File "task.py", line 1022 [...]
            TypeError: parallel_task() takes exactly 3 arguments (2 given)
        
        
            Exception #2
            exceptions.TypeError: parallel_task() takes exactly 3 arguments (2 given)
            for Job = ["B", 3]
        
            Traceback (most recent call last):
              File "task.py", line 1022 [...]
            TypeError: parallel_task() takes exactly 3 arguments (2 given)
    
        
    .. ???

    (Parts of the traceback have been removed for brevity)

.. index:: signalling, interrupts, break

.. ???

    
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
        
            

    produces the following (abbreviated)::
    
        task.RethrownJobError:
        
            Exceptions running jobs for
            'def parallel_task(...):'
        
            Original exception:
        
            Exception #1
            task.JobSignalledBreak: Job = ["A", 1] returned False
            for Job = ["A", 1]
        
.. ???

    
=====================
Multiple Errors
=====================
    For any task where exceptions are thrown, *Ruffus* will continue executing until
    the number of exceptions is equal to the number of concurrent jobs (``multiprocess``) set in
    ``pipeline_run``. This seems a fair tradeoff between being able to gather detailed
    error information for running jobs, and not wasting too much time for a task
    that is going to fail anyway.
    
    *Ruffus* always exits concurrent task operations as soon as possible if the
    pipeline is interrupted by a job returning false (see :ref:`previous section <interrupting>`).

