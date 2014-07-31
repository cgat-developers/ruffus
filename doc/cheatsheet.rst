.. include:: global.inc
.. _cheat_sheet:


#####################
Cheat Sheet
#####################

The ``ruffus`` module is a lightweight way to add support
for running computational pipelines.

| Each stage or **task** in a computational pipeline is represented by a python function
| Each python function can be called in parallel to run multiple **jobs**.

================================================
1. Annotate functions with **Ruffus** decorators
================================================


******
Core
******
.. csv-table::
   :header: "Decorator", "Syntax"
   :widths: 100, 600,1

   "@originate (:ref:`Manual <new_manual.originate>`)
   ", "
   :ref:`@originate <decorators.originate>` ( ``output_files``, [``extra_parameters``,...] )
   ", ""
   "@split (:ref:`Manual <new_manual.split>`)
   ", "
   :ref:`@split <decorators.split>` ( ``tasks_or_file_names``, ``output_files``, [``extra_parameters``,...] )
   ", ""
   "@transform (:ref:`Manual <new_manual.transform>`)
   ", "
   | :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`suffix <decorators.transform.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
   | :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`regex <decorators.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )

   ", ""
   "@merge (:ref:`Manual <new_manual.merge>`)
   ", "
   :ref:`@merge <decorators.merge>` (``tasks_or_file_names``, ``output``, [``extra_parameters``,...] )
   ", ""
   "@posttask (:ref:`Manual <new_manual.posttask>`)
   ", "
   | :ref:`@posttask <decorators.posttask>` ( ``signal_task_completion_function`` )
   | :ref:`@posttask <decorators.posttask>` (:ref:`touch_file <decorators.touch_file>`\ ( ``'task1.completed'`` ))

   ", ""

************************************************************************************************
See :ref:`Decorators <decorators>` for a complete list of decorators
************************************************************************************************



================================================
2. Print dependency graph if necessary
================================================

- For a graphical flowchart in ``jpg``, ``svg``, ``dot``, ``png``, ``ps``, ``gif`` formats::

        pipeline_printout_graph ( "flowchart.svg")

.. comment

        This requires the `dot programme <http://www.graphviz.org/>`_ to be installed

- For a text printout of all jobs ::

        pipeline_printout()


================================================
3. Run the pipeline
================================================

::

    pipeline_run(multiprocess = N_PARALLEL_JOBS)




