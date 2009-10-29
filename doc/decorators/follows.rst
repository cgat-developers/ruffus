.. _task.follows:

.. seealso::

    * :ref:`Decorators <decorators>` for more decorators
    * More on @follows in :ref:`step 1 <manual_1st_chapter>` of the full tutorial


############
@follows
############

.. |task| replace:: `task`
.. _task: `task.follows.task`_
.. |task_name| replace:: `"task_name"`
.. _task_name: `task.follows.task_name`_
.. |directory_name| replace:: `directory_name`
.. _directory_name: `task.follows.directory_name`_

.. |mkdir| replace:: *mkdir*
.. _mkdir: indicator_objects.html#task.mkdir

*******************************************************************************************
*@follows*\ (|task|_ | |task_name|_ | |mkdir|_ (|directory_name|_), [more_tasks, ...])
*******************************************************************************************
    **Purpose:**
    
        Indicates task dependencies


    **Example**::
    
        def task1():
            print "doing task 1"
    
        @follows(task1)
        def task2():
            print "doing task 2"


    **Parameters:**
                
.. _task.follows.task:
 
    * *task*: 
        a list of tasks which have to be run **before** this function
                
.. _task.follows.task_name:
 
    * *"task_name"*: 
        Dependencies can be quoted function names.
        Quoted function names allow dependencies to be added before the function is defined.

        Functions in other modules need to be fully qualified.
                
                
.. _task.follows.directory_name:
 
    * *directory_name*:
        Directories which need to be created (if they don't exist) before
        the task is run can be specified via a ``mkdir`` indicator object:

            ::

                @follows(task_x, mkdir("/output/directory") ...)
                def task():
                    pass


