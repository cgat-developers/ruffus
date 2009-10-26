.. _Simple_Tutorial_1st_step:

###################################################################
Step 1: Arranging tasks into a pipeline
###################################################################
* :ref:`Up <Simple_Tutorial>` 
* :ref:`Next <Simple_Tutorial_2nd_step>` 
* :ref:`More on @follows in the full tutorial <Full_Tutorial_1st_step>`
* :ref:`@follows syntax in detail <task.follows>`




************************************
*@follows*
************************************

The :ref:`@follows(...) <task.follows>` python decorator indicates the order in which tasks
should be run:

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

