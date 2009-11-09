.. _Simple_Tutorial_1st_step:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task

###################################################################
Step 1: Arranging tasks into a pipeline
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>` 
* :ref:`More on @follows in the full tutorial <manual_1st_chapter>`
* :ref:`@follows syntax in detail <decorators.follows>`




************************************
*@follows*
************************************

The :ref:`@follows(...) <decorators.follows>` python decorator indicates the order in which tasks
should be run. Remember that each stage or |task|_ of a pipeline is represented by an ordinary python function.
To show that one task function should always run after another task, we need to *decorate* the
function with **@follows**. 

(See the line above ``def second_task()``:


    ::
    
        from ruffus import *
        
        def first_task():
            print "First task"
    
        @follows(first_task)
        def second_task():
            print "Second task"


the ``@follows`` decorator indicate that ``first_task`` function precedes ``second_task`` in 
the pipeline.


************************************
Running our pipeline
************************************

    Now we can run the pipeline by::
        
        >>> pipeline_run([second_task])
        
    Which gives::
    
        Task = first_task
        First task
            Job completed
        Task = second_task
        Second task
            Job completed
    
    Because ``second_task`` depends on ``first_task`` , both
    functions will be executed in order.

