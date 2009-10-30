.. _manual_2nd_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run


###################################################################
Chapter 3: Running Tasks and Jobs in parallel
###################################################################
.. hlist::
   * :ref:`Manual overview <manual>` 

=====================
Multi Processing
=====================

    *Ruffus* uses python `multiprocessing <http://docs.python.org/library/multiprocessing.html>`_ to run
    each job in a separate process.
    
    This means that jobs do *not* necessarily complete in the order of the defined parameters.
    Task hierachies are, of course, inviolate: upstream tasks run before downstream, dependent tasks.
    
    Tasks that are independent (i.e. do not precede each other) may be run in parallel as well.
    
    The number of concurrent jobs can be set in |pipeline_run|_:

        ::
        
            pipeline_run([parallel_task], multiprocess = 5)
        
        
    If ``multiprocess`` is set to 1, then jobs will be run on a single process.

    
=====================
Data sharing
=====================
    
    Running jobs in separate processes allows *Ruffus* to make full use of the multiple
    processors in modern computers. However, some of the 
    `multiprocessing guidelines <http://docs.python.org/library/multiprocessing.html#multiprocessing-programming>`_
    should be borne in mind when writing *Ruffus* pipelines. In particular:
    
    * Try not to pass large amounts of data between jobs, or at least be aware that this has to be marshalled
      across process boundaries.
      
    * Only data which can be `pickled <http://docs.python.org/library/pickle.html>`_ can be passed as 
      parameters to *Ruffus* task functions. Happily, that applies to almost any Python data type.
      The use of the rare, unpicklable object will cause python to complain (fail) loudly when *Ruffus* pipelines
      are run.
      

