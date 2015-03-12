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
   tutorials/new_syntax.rst
   tutorials/new_syntax_worked_example.rst
   tutorials/new_syntax_worked_example_code.rst
   Future plans <todo>
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
   examples/paired_end_data.py.rst



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


=====================
Indices and tables
=====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
