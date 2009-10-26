.. _Full_Tutorial_1st_step:

###################################################################
Step 1: Arranging tasks into a pipeline
###################################################################

* :ref:`Up <Full_Tutorial>` 
* :ref:`Next <Full_Tutorial_2nd_step>` 
* :ref:`@follows syntax <task.follows>` in detail


***************************************
**@follows**
***************************************

    Use the **@follows(...)** python decorator before the function definitions:
    
        ::
    
            from ruffus import *
            import sys
            
            def first_task():
                print "First task"
        
            @follows(first_task)
            def second_task():
                print "Second task"
        
            @follows(second_task)
            def final_task():
                print "Final task"

    
    the ``@follows`` decorator indicate that the ``first_task`` function precedes ``second_task`` in 
    the pipeline.


=====================
Running
=====================

    Now we can run the pipeline by::
        
        pipeline_run([final_task])
    
    
    Because ``final_task`` depends on ``second_task`` which depends on ``first_task`` , all 
    three functions will be executed in order.
    
=====================
Displaying
=====================

    We can see a flowchart of our fledgling pipeline by executing::
    
        pipeline_printout_graph ( open("tutorial_flowchart_ex1.jpg", "w"),
                                 "jpg",
                                 [final_task], 
                                 no_key_legend=True)
    
    producing the following flowchart
    
    .. image:: ../../images/tutorial_flowchart_ex1.jpg
        
.. ???

    or in text format with::
    
        pipeline_printout(sys.stdout, [final_task])
    
.. ???

.. _follows-out-of-order:

***************************************
More to **@follows**
***************************************

    All this assumes that all your pipelined tasks are defined in order.
    (``first_task`` before ``second_task`` before ``final_task``)
    
    This is usually the most sensible way to arrange your code.
    If you wish to refer to tasks which are not yet defined, you can do so by quoting the
    function name. This is also a way of referring to tasks in other modules::
    
    
        @follows(first_task, "fifth_task", "another_module.useful_task")
        def second_task():
            print "Second task"

.. ???
            
    
    Note that the ``@follows`` decorator can refer to multiple antecedent tasks.
    Alternatively, the same code can be written as::
    
        @follows(first_task)
        @follows("fifth_task")
        @follows("another_module.useful_task")
        def second_task():
            print "Second task"

.. ???

.. _follow-mkdir:

.. index:: 
    pair: @follows; mkdir

******************************************************************************
Making directories automatically with :ref:`mkdir <task.mkdir>`
******************************************************************************


    A common prerequisite for any computational task, is making sure that the destination
    directories exist. As a shortcut, we can define a special :ref:`mkdir <task.mkdir>` dependency. For example::
    
        @follows(first_task, mkdir("output/results/here"))
        def second_task():
            print "Second task"
            
    will make sure that ``output/results/here`` exists before `second_task` is run.
    
    In other words, it will make the ``output/results/here`` directory if it does not exist.



