.. _decorators.follows:
.. index:: 
    pair: @follows; Syntax

.. seealso::

    * :ref:`Decorators <decorators>` for more decorators
    * More on @follows in :ref:`step 1 <manual_1st_chapter>` of the full tutorial


############
@follows
############

.. |task| replace:: `task`
.. _task: `decorators.follows.task`_
.. |task_name| replace:: `"task_name"`
.. _task_name: `decorators.follows.task_name`_
.. |directory_name| replace:: `directory_name`
.. _directory_name: `decorators.follows.directory_name`_

***************************************************************************************************************************************************
*@follows*\ (|task|_ | |task_name|_ | :ref:`mkdir<decorators.mkdir>` (|directory_name|_), [more_tasks, ...])
***************************************************************************************************************************************************
    **Purpose:**
    
        Indicates task dependencies


    **Example**::
    
        def task1():
            print "doing task 1"
    
        @follows(task1)
        def task2():
            print "doing task 2"


    **Parameters:**
                
.. _decorators.follows.task:
 
    * *task*: 
        a list of tasks which have to be run **before** this function
                
.. _decorators.follows.task_name:
 
    * *"task_name"*: 
        Dependencies can be quoted function names.
        Quoted function names allow dependencies to be added before the function is defined.

        Functions in other modules need to be fully qualified.
                
                
.. _decorators.follows.directory_name:
 
    * *directory_name*:
        Directories which need to be created (if they don't exist) before
        the task is run can be specified via a ``mkdir`` indicator object:

            ::

                @follows(task_x, mkdir("/output/directory") ...)
                def task():
                    pass


