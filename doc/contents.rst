.. include:: global.inc
***************************
**Ruffus** documentation
***************************
==========================================
Start Here:
==========================================
.. toctree::
   :maxdepth: 2

   installation.rst
   tutorials/new_tutorial/manual_contents.rst
   tutorials/new_tutorial/introduction.rst
   tutorials/new_tutorial/transform.rst
   tutorials/new_tutorial/transform_in_parallel.rst
   tutorials/new_tutorial/originate.rst
   tutorials/new_tutorial/pipeline_printout.rst
   tutorials/new_tutorial/command_line.rst
   tutorials/new_tutorial/pipeline_printout_graph.rst
   tutorials/new_tutorial/output_file_names.rst
   tutorials/new_tutorial/mkdir.rst
   tutorials/new_tutorial/checkpointing.rst
   tutorials/new_tutorial/decorators_compendium.rst
   tutorials/new_tutorial/split.rst
   tutorials/new_tutorial/merge.rst
   tutorials/new_tutorial/multiprocessing.rst
   tutorials/new_tutorial/logging.rst
   tutorials/new_tutorial/subdivide_collate.rst
   tutorials/new_tutorial/combinatorics.rst
   tutorials/new_tutorial/active_if.rst
   tutorials/new_tutorial/posttask.rst
   tutorials/new_tutorial/inputs.rst
   tutorials/new_tutorial/onthefly.rst
   tutorials/new_tutorial/parallel.rst
   tutorials/new_tutorial/check_if_uptodate.rst
   tutorials/new_tutorial/flowchart_colours.rst
   tutorials/new_tutorial/dependencies.rst
   tutorials/new_tutorial/exceptions.rst
   tutorials/new_tutorial/list_of_ruffus_names.rst
   tutorials/new_tutorial/deprecated_files.rst
   tutorials/new_tutorial/deprecated_files_re.rst


Example code for:

.. toctree::
   :maxdepth: 1

   tutorials/new_tutorial/introduction_code.rst
   tutorials/new_tutorial/transform_code.rst
   tutorials/new_tutorial/transform_in_parallel_code.rst
   tutorials/new_tutorial/originate_code.rst
   tutorials/new_tutorial/pipeline_printout_code.rst
   tutorials/new_tutorial/pipeline_printout_graph_code.rst
   tutorials/new_tutorial/output_file_names_code.rst
   tutorials/new_tutorial/mkdir_code.rst
   tutorials/new_tutorial/checkpointing_code.rst
   tutorials/new_tutorial/split_code.rst
   tutorials/new_tutorial/merge_code.rst
   tutorials/new_tutorial/multiprocessing_code.rst
   tutorials/new_tutorial/logging_code.rst
   tutorials/new_tutorial/subdivide_collate_code.rst
   tutorials/new_tutorial/combinatorics_code.rst
   tutorials/new_tutorial/inputs_code.rst
   tutorials/new_tutorial/onthefly_code.rst
   tutorials/new_tutorial/flowchart_colours_code.rst



=====================
Overview:
=====================
.. toctree::
   :maxdepth: 2

   cheatsheet.rst
   pipeline_functions.rst
   drmaa_wrapper_functions.rst
   installation.rst
   design.rst
   Bugs and Updates <history>
   Future plans <todo>
   Pending changes <refactoring_ruffus_notes>
   Implementation_notes <implementation_notes.rst>
   faq.rst
   glossary.rst
   gallery.rst
   why_ruffus.rst

=====================
Examples
=====================
.. toctree::
   :maxdepth: 2

   examples/bioinformatics/index.rst
   examples/bioinformatics/part2.rst
   examples/bioinformatics/part1_code.rst
   examples/bioinformatics/part2_code.rst
   tutorials/manual/manual_code.rst
   tutorials/simple_tutorial/simple_tutorial_code.rst



=====================
Reference:
=====================
######################
Decorators
######################
.. toctree::
    :maxdepth: 1

    decorators/decorators.rst
    decorators/indicator_objects.rst


.. topic::
    Core

    .. toctree::
        :maxdepth: 1

        decorators/originate.rst
        decorators/split.rst
        decorators/transform.rst
        decorators/merge.rst

.. topic::
    For advanced users

    .. toctree::
        :maxdepth: 1

        decorators/subdivide.rst
        decorators/transform_ex.rst
        decorators/collate.rst
        decorators/collate_ex.rst
        decorators/graphviz.rst
        decorators/mkdir.rst
        decorators/jobs_limit.rst
        decorators/posttask.rst
        decorators/active_if.rst
        decorators/follows.rst

.. topic::
    Combinatorics

    .. toctree::
        :maxdepth: 1

        decorators/product.rst
        decorators/permutations.rst
        decorators/combinations.rst
        decorators/combinations_with_replacement.rst

.. topic::
    Esoteric

    .. toctree::
        :maxdepth: 1

        decorators/files_ex.rst
        decorators/check_if_uptodate.rst
        decorators/parallel.rst

.. topic::
    Deprecated

    .. toctree::
        :maxdepth: 1

        decorators/files.rst
        decorators/files_re.rst


######################
Modules:
######################

.. toctree::
   :maxdepth: 2

   task.rst
   proxy_logger.rst

.. comment
   graph.rst
   print_dependencies.rst
   adjacent_pairs_iterate.rst


==========================================
Old Manual: / tutorial
==========================================

.. toctree::
   :maxdepth: 1

   tutorials/manual/manual_contents.rst
   tutorials/manual/manual_introduction.rst
   tutorials/manual/follows.rst
   tutorials/manual/tasks_as_recipes.rst
   tutorials/manual/files.rst
   tutorials/manual/tasks_and_globs_in_inputs.rst
   tutorials/manual/tracing_pipeline_parameters.rst
   tutorials/manual/parallel_processing.rst
   tutorials/manual/split.rst
   tutorials/manual/transform.rst
   tutorials/manual/merge.rst
   tutorials/manual/posttask.rst
   tutorials/manual/jobs_limit.rst
   tutorials/manual/dependencies.rst
   tutorials/manual/onthefly.rst
   tutorials/manual/collate.rst
   tutorials/manual/advanced_transform.rst
   tutorials/manual/parallel.rst
   tutorials/manual/check_if_uptodate.rst
   tutorials/manual/exceptions.rst
   tutorials/manual/logging.rst
   tutorials/manual/files_re.rst
   recipes.rst

.. toctree::
   :maxdepth: 1

   tutorials/simple_tutorial/simple_tutorial.rst
   1. Chain tasks (functions) together into a pipeline <tutorials/simple_tutorial/step1_follows>
   2. Provide parameters to run jobs in parallel <tutorials/simple_tutorial/step2>
   3. Tracing through your new pipeline <tutorials/simple_tutorial/step3_run_pipeline>
   4. Using flowcharts  <tutorials/simple_tutorial/step4_run_pipeline_graphically>
   5. Split up a large problem into smaller chunks <tutorials/simple_tutorial/step5_split>
   6. Calculate partial solutions in parallel <tutorials/simple_tutorial/step6_transform>
   7. Re-combine the partial solutions into the final result <tutorials/simple_tutorial/step7_merge>
   8. Automatically signal the completion of each step of our pipeline <tutorials/simple_tutorial/step8_posttask>


Old Manual Code:

.. toctree::
    :maxdepth: 1

    tutorials/manual/dependencies_code.rst
    tutorials/manual/logging_code.rst
    tutorials/manual/onthefly_code.rst
    tutorials/manual/transform_code.rst

Old Tutorial Code:

.. toctree::
    :maxdepth: 1

    tutorials/simple_tutorial/step2_code.rst
    tutorials/simple_tutorial/step3_run_pipeline_code.rst
    tutorials/simple_tutorial/step4_run_pipeline_graphically_code.rst
    tutorials/simple_tutorial/step5_split_code.rst
    tutorials/simple_tutorial/step6_transform_code.rst
    tutorials/simple_tutorial/step7_merge_code.rst
    tutorials/simple_tutorial/step8_posttask_code.rst


=====================
Indices and tables
=====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
