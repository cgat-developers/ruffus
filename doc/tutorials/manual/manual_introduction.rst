.. _manual.introduction:

####################################################################
**Ruffus** Manual: A work in progress
####################################################################

.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator


***************************************
Introduction
***************************************

    The **Ruffus** module is a lightweight way to add support 
    for running computational pipelines.
    
    Computational pipelines are often conceptually quite simple, especially
    if we breakdown the process into simple stages, or separate |task|_\ s.
    
    Each stage or |task|_ of a pipeline is represented by an ordinary python function.
    
    Membership of a *Ruffus* pipeline is indicated using special |decorator|_\ s, such as 
    :ref:`@follows <decorators.follows>` (which governs the order of tasks should run, 
    (see :ref:`chapter 1 <manual_1st_chapter>` of this manual for more details.)
    
        ::
        
            @follows(first_task)
            def second_task():
                # do something here
                ""

    | Multiple |decorator|_\ s can be used for each |task|_ function to add functionality
      to *Ruffus* pipeline functions. 
    | However, these remain ordinary python functions which can still be
      called normally, outside of *Ruffus*.
    
    *Ruffus* |decorator|_\ s can be added (stacked on top of) to any function in any order.


    The following chapters go through each of the features of **Ruffus** in turn.
    Many of these (especially those labelled **esoteric** or **deprecated**) may not
    be of interest to all users of **Ruffus**.
    
    If you are looking for a quick introduction to **Ruffus**, you may want to look at the
    :ref:`Simple Tutorial <Simple_Tutorial>` first.
