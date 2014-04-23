.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: Checking dependencies; Tutorial

.. _new_manual.dependencies:

##################################################################################
|new_manual.dependencies.chapter_num|: How dependency is checked
##################################################################################

.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`


**************************************
Overview
**************************************

    How does *Ruffus* decide how to run your pipeline?

        * In which order should pipelined functions be called?

        * Which parts of the pipeline are up-to-date and do not need to be rerun?


=============================================
Running all out-of-date tasks and dependents
=============================================

    .. image:: ../../images/manual_dependencies_flowchart_intro.png
       :scale: 50


    By default, *Ruffus* will

        * build a flow chart (dependency tree) of pipelined tasks (functions)
        * start from the most ancestral tasks with the fewest dependencies (``task1`` and ``task4`` in the flowchart above).
        * walk up the tree to find the first incomplete / out-of-date tasks (i.e. ``task3`` and ``task5``.
        * start running from there

    All down-stream (dependent) tasks will be re-run anyway, so we don't have to test
          whether they are up-to-date or not.

    .. _new_manual.dependencies.checking_multiple_times:

    .. note::

        This means that *Ruffus* *may* ask any task if their jobs are out of date more than once:

            * once when deciding which parts of the pipeline have to be run
            * once just before executing the task.

    *Ruffus* tries to be clever / efficient, and does the minimal amount of querying.


.. _new_manual.dependencies.forced_reruns:

=======================================
Forced Reruns
=======================================
    Even if a pipeline stage appears to be up to date,
    you can always force the pipeline to include from one or more task functions.

    This is particularly useful, for example, if the pipeline data hasn't changed but
    the analysis or computional code has.

        ::

            pipeline_run(forcedtorun_tasks = [up_to_date_task1])


        will run all tasks from ``up_to_date_task1`` to ``final_task``


    Both the "target" and the "forced" lists can include as many tasks as you wish. All dependencies
    are still carried out and out-of-date jobs rerun.

.. _new_manual.dependencies.minimal_reruns:

=======================================
Esoteric option: Minimal Reruns
=======================================

    In the above example, if we were to delete the results of ``up_to_date_task1``, *Ruffus*
    would rerun ``up_to_date_task1``, ``up_to_date_task2`` and ``task3``.

    However, you might argue that so long as ``up_to_date_task2`` is up-to-date, and it
    is the only necessary prerequisite for ``task3``, we should not be concerned about
    ``up_to_date_task1``.

    This is enabled with:

        .. code-block:: python

            pipeline_run([task6], gnu_make_maximal_rebuild_mode = False)

    This option walks down the dependency tree and proceeds no further when it encounters
    an up-to-date task (``up_to_date_task2``) whatever the state of what lies beyond it.

    This rather dangerous option is useful if you don't want to keep all the intermediate
    files/results from upstream tasks. The pipeline will only not involve any incomplete
    tasks which precede an up-to-date result.

    This is seldom what you intend, and you should always check that the appropriate stages
    of the pipeline are executed in the flowchart output.


