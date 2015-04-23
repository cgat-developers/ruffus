.. include:: ../global.inc
.. _decorators.jobs_limit:
.. index::
    pair: @jobs_limit; Syntax

.. seealso::

    * :ref:`@jobs_limit <new_manual.jobs_limit>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

########################
jobs_limit
########################

.. |maximum_num_of_jobs| replace:: `maximum_num_of_jobs`
.. _maximum_num_of_jobs: `decorators.jobs_limit.maximum_num_of_jobs`_
.. |name| replace:: `name`
.. _name: `decorators.jobs_limit.name`_

*****************************************************************************************************************************************
*@jobs_limit* ( |maximum_num_of_jobs|_, [ |name|_ ])
*****************************************************************************************************************************************
    **Purpose:**
        | Manages the resources available for a task.
        | Limits the number of concurrent jobs which can be run in parallel for this task
        | Overrides the value for ``multiprocess`` in :ref:`pipeline_run <pipeline_functions.pipeline_run>`
        | If an optional ``name`` is given, the same limit is shared across all tasks with the same @job_limit name.


    **Parameters:**

.. _decorators.jobs_limit.maximum_num_of_jobs:


    * *maximum_num_of_jobs*
       The maximum number of concurrent jobs for this task. Must be an integer number
       greater than or equal to 1.

.. _decorators.jobs_limit.name:

    * *name*
       Optional name for the limit. All tasks with the same name share the same limit if they
       are running concurrently.

    **Example**
        ::

            from ruffus import *

            # make list of 10 files
            @split(None, "*.stage1")
            def make_files(input_file, output_files):
                for i in range(10):
                    open("%d.stage1" % i, "w")

            @jobs_limit(2)
            @transform(make_files, suffix(".stage1"), ".stage2")
            def stage1(input_file, output_file):
                open(output_file, "w")

            @transform(stage1, suffix(".stage2"), ".stage3")
            def stage2(input_file, output_file):
                open(output_file, "w")

            pipeline_run([stage2], multiprocess = 5)

        will run the 10 jobs of ``stage1`` 2 at a time, while `` stage2`` will
        run 5 at a time (from ``multiprocess = 5``):

        .. image:: ../images/jobs_limit.png



