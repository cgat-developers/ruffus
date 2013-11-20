.. include:: global.inc
***************************
**Ruffus** documentation
***************************

=====================
Start Here:
=====================

.. toctree::
   :maxdepth: 1

   installation.rst
   tutorials/simple_tutorial/simple_tutorial.rst
   1. Chain tasks (functions) together into a pipeline <tutorials/simple_tutorial/step1_follows>
   2. Provide parameters to run jobs in parallel <tutorials/simple_tutorial/step2>
   3. Tracing through your new pipeline <tutorials/simple_tutorial/step3_run_pipeline>
   4. Using flowcharts  <tutorials/simple_tutorial/step4_run_pipeline_graphically>
   5. Split up a large problem into smaller chunks <tutorials/simple_tutorial/step5_split>
   6. Calculate partial solutions in parallel <tutorials/simple_tutorial/step6_transform>
   7. Re-combine the partial solutions into the final result <tutorials/simple_tutorial/step7_merge>
   8. Automatically signal the completion of each step of our pipeline <tutorials/simple_tutorial/step8_posttask>


=====================
Manual:
=====================

.. toctree::
   :maxdepth: 2

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


=====================
Overview:
=====================
.. toctree::
   :maxdepth: 2

   cheatsheet.rst
   pipeline_functions.rst
   installation.rst
   design.rst
   Bugs and Updates <history>
   Future plans <todo>
   Pending changes <refactoring_ruffus_notes>
   faq.rst
   glossary.rst
   gallery.rst
   examples/code_template/code_template.rst
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
   examples/colour_schemes/flowchart_colours.rst
   examples/colour_schemes/flowchart_colours_code.rst
   examples/code_template/code_template_code.rst
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
    Basic

    .. toctree::
        :maxdepth: 1

        decorators/follows.rst
        decorators/files.rst

.. topic::
    Core

    .. toctree::
        :maxdepth: 1

        decorators/split.rst
        decorators/transform.rst
        decorators/merge.rst
        decorators/posttask.rst

.. topic::
    For advanced users

    .. toctree::
        :maxdepth: 1

        decorators/jobs_limit.rst
        decorators/split_ex.rst
        decorators/transform_ex.rst
        decorators/collate.rst
        decorators/collate_ex.rst

.. topic::
    Esoteric

    .. toctree::
        :maxdepth: 1

        decorators/files_ex.rst
        decorators/parallel.rst
        decorators/check_if_uptodate.rst
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


=====================
Indices and tables
=====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

