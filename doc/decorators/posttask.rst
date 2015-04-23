.. include:: ../global.inc
.. _decorators.posttask:
.. index::
    pair: @posttask; Syntax

.. seealso::

    * :ref:`@posttask <new_manual.posttask>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

.. |function| replace:: `function`
.. _function: `decorators.posttask.function`_
.. |file_name| replace:: `file_name`
.. _file_name: `decorators.posttask.file_name`_

########################
posttask
########################

*****************************************************************************************************************************************
*@posttask* (|function|_ | :ref:`touch_file<decorators.touch_file>`\ *(*\ |file_name|_\ *)*\)
*****************************************************************************************************************************************
    **Purpose:**
        Calls functions to signal the completion of each task

    **Example**::

        from ruffus import *

        def task_finished():
            print "hooray"

        @posttask(task_finished)
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")

        pipeline_run([create_if_necessary])

    **Parameters:**

.. _decorators.posttask.function:

    * *function*:
        ``function()`` will be called when the ruffus passes through a task.

        This may happen even if all of the jobs are up-to-date:
        when a upstream task is out-of-date, and the execution passes through
        this point in the pipeline

.. _decorators.posttask.file_name:

    * *file_name*
        Files to be ``touch``\ -ed after the task is executed.

        This will change the date/time stamp of the ``file_name`` to the current date/time.
        If the file does not exist, an empty file will be created.

        Requires to be wrapped in a :ref:`touch_file<decorators.touch_file>` indicator object::

            from ruffus import *

            @posttask(touch_file("task_completed.flag"))
            @files(None, "a.1")
            def create_if_necessary(input_file, output_file):
                open(output_file, "w")

            pipeline_run([create_if_necessary])



