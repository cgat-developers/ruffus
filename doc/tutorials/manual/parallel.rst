.. _manual_13th_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run

###################################################################################
Chapter 13: Esoteric: Running jobs in parallel without using files
###################################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 
        * :ref:`@parallel<decorators.parallel>` syntax in detail

    
.. index:: 
    single: @parallel; Manual
    
.. _manual.parallel:




***************************************
**@parallel** 
***************************************

    Often each task consists of multiple **jobs** (in GNU make terminology) which can be
    run concurrently. 
    
    Each **job** is a separate call to the same task function but with different parameters.
    Let us try to add up (1+2), (3+4) and (5+6) in parallel::
    
        from ruffus import *
        parameters = [
                         ['A', 1, 2], # 1st job
                         ['B', 3, 4], # 2nd job
                         ['C', 5, 6], # 3rd job
                     ]
        @parallel(parameters)                                                     
        def parallel_task(name, param1, param2):                                  
            sys.stderr.write("    Parallel task %s: " % name)                     
            sys.stderr.write("%d + %d = %d\n" % (param1, param2, param1 + param2))
        
        pipeline_run([parallel_task])
        
    .. ???

    Produces the following::
    
        Task = parallel_task
            Parallel task A: 1 + 2 = 3
            Job = ["A", 1, 2] completed
            Parallel task B: 3 + 4 = 7
            Job = ["B", 3, 4] completed
            Parallel task C: 5 + 6 = 11
            Job = ["C", 5, 6] completed
        

