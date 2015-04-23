.. include:: ../global.inc
.. _decorators.follows:
.. index::
    pair: @follows; Syntax

.. seealso::

    * :ref:`@follows <new_manual.follows>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

    .. note::

        Only missing directories are created.

        In other words, the same directory can be specified multiple times safely without, for example, being recreated repeatedly.
        Sometimes, for pipelines with multiple entry points, this is the only way to make sure that certain working or output
        directories are always created or available *before* the pipeline runs.


############
follows
############

.. _decorators.follows.mkdir:

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

        Indicates either

            * task dependencies
            * that the task requires a directory to be created first *if necessary*. (Existing directories will not be overwritten)


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
        Directories which need to be created (*only if they don't exist*) before
        the task is run can be specified via a ``mkdir`` indicator object:

            ::

                @follows(task_x, mkdir("/output/directory") ...)
                def task():
                    pass


