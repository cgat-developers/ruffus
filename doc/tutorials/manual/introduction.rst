.. _manual:

##################################
Manual: Introduction
##################################

.. |task| replace:: **task**
.. _task: glossary.html#term-task
.. |job| replace:: **job**
.. _job: glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: glossary.html#term-decorator


***************************************
Introduction
***************************************

    The ``ruffus`` module is a lightweight way to add support 
    for running computational pipelines.
    
    Computational pipelines are often conceptually quite simple, especially
    if we breakdown the process into simple stages, or separate |task|_\ s.
    
    Each stage or |task|_ of a pipeline is represented by an ordinary python function.
    
    Membership of a *Ruffus* pipeline is indicated using special |decorator|_\ s, such as 
    :ref:`@follows <decorators.follows>` (which governs the order of tasks should run, 
    (see :ref:`step 1 <manual_1st_chapter>` of this tutorial for more details.)
    
        ::
        
            @follows(first_task)
            def second_task():
                # do something here
                ""

    | Multiple |decorator|_\ s can be used for each |task|_ function to add functionality
      to *Ruffus* pipeline functions. 
    | However, these remain ordinary python functions which can still be
      called normally, outside of *Ruffus*.
    
    *Ruffus* |decorator|_\ s can be added in any order.



.. comment::

    Because of this, each |task|_ represent not only a single action in a pipeline,
    but also a recipe or `rule <http://www.gnu.org/software/make/manual/make.html#Rule-Introduction>`_  
    which can be applied at the same time to many different parameters.
    
    For example, one can have a *compile task* which will compile any source code, or
    a *count_lines task* which will count the number of lines in any file.
    
    Each |task|_, then, is a recipe for making specified files using supplied parameters.

