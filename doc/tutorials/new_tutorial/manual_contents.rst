.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.table_of_contents:


==========================================
Manual
==========================================
.. toctree::
   :maxdepth: 1
   :caption: Manual / Tutorial
   :name: manual_toc
   :hidden:

   introduction.rst
   transform.rst
   transform_in_parallel.rst
   originate.rst
   pipeline_printout.rst
   command_line.rst
   pipeline_printout_graph.rst
   output_file_names.rst
   mkdir.rst
   checkpointing.rst
   decorators_compendium.rst
   split.rst
   merge.rst
   multiprocessing.rst
   logging.rst
   subdivide_collate.rst
   combinatorics.rst
   active_if.rst
   posttask.rst
   inputs.rst
   onthefly.rst
   parallel.rst
   check_if_uptodate.rst
   flowchart_colours.rst
   dependencies.rst
   exceptions.rst
   list_of_ruffus_names.rst
   deprecated_files.rst
   deprecated_files_re.rst

####################################################################
**Ruffus** Manual Table of Contents
####################################################################

    Download as :download:`pdf <../../static_data/ruffus.pdf>`.

    * |new_manual.introduction.chapter_num|: :ref:`An introduction to basic Ruffus syntax <new_manual.introduction>`
    * |new_manual.transform.chapter_num|: :ref:`Transforming data in a pipeline with @transform <new_manual.transform>`
    * |new_manual.transform_in_parallel.chapter_num|: :ref:`More on @transform-ing data <new_manual.transform_in_parallel>`
    * |new_manual.originate.chapter_num|: :ref:`Creating files with @originate <new_manual.originate>`
    * |new_manual.pipeline_printout.chapter_num|: :ref:`Understanding how your pipeline works with pipeline_printout() <new_manual.pipeline_printout>`
    * |new_manual.cmdline.chapter_num|: :ref:`Running Ruffus from the command line with ruffus.cmdline <new_manual.cmdline>`
    * |new_manual.pipeline_printout_graph.chapter_num|: :ref:`Displaying the pipeline visually with pipeline_printout_graph() <new_manual.pipeline_printout_graph>`
    * |new_manual.output_file_names.chapter_num|: :ref:`Specifying output file names with formatter() and regex() <new_manual.output_file_names>`
    * |new_manual.mkdir.chapter_num|: :ref:`Preparing directories for output with @mkdir <new_manual.mkdir>`
    * |new_manual.checkpointing.chapter_num|: :ref:`Checkpointing: Interrupted Pipelines and Exceptions <new_manual.checkpointing>`
    * |new_manual.decorators_compendium.chapter_num|: :ref:`Pipeline topologies and a compendium of Ruffus decorators <new_manual.decorators_compendium>`
    * |new_manual.split.chapter_num|: :ref:`Splitting up large tasks / files with @split <new_manual.split>`
    * |new_manual.merge.chapter_num|: :ref:`@merge multiple input into a single result <new_manual.merge>`
    * |new_manual.logging.chapter_num|: :ref:`Logging progress through a pipeline <new_manual.logging>`
    * |new_manual.multiprocessing.chapter_num|: :ref:`Multiprocessing, drmaa and Computation Clusters <new_manual.multiprocessing>`
    * |new_manual.subdivide_collate.chapter_num|: :ref:`@subdivide tasks to run efficiently and regroup with @collate <new_manual.subdivide_collate>`
    * |new_manual.combinatorics.chapter_num|: :ref:`@combinations, @permutations and all versus all @product <new_manual.combinatorics>`
    * |new_manual.active_if.chapter_num|: :ref:`Turning parts of the pipeline on and off at runtime with @active_if <new_manual.active_if>`
    * |new_manual.inputs.chapter_num|: :ref:`Manipulating task inputs via string substitution with inputs() and add_inputs() <new_manual.inputs>`
    * |new_manual.posttask.chapter_num|: :ref:`Signal the completion of each stage of our pipeline with @posttask <new_manual.posttask>`
    * |new_manual.on_the_fly.chapter_num|: :ref:`Esoteric: Generating parameters on the fly with @files <new_manual.on_the_fly>`
    * |new_manual.parallel.chapter_num|: :ref:`Esoteric: Running jobs in parallel without files using @parallel <new_manual.deprecated_parallel>`
    * |new_manual.check_if_uptodate.chapter_num|: :ref:`Esoteric: Writing custom functions to decide which jobs are up to date with @check_if_uptodate <new_manual.check_if_uptodate>`
    * |new_manual.flowchart_colours.chapter_num| :ref:`Flow Chart Colours with pipeline_printout_graph <new_manual.flowchart_colours>`
    * |new_manual.dependencies.chapter_num| :ref:`Under the hood: How dependency works <new_manual.dependencies>`
    * |new_manual.exceptions.chapter_num| :ref:`Exceptions thrown inside pipelines <new_manual.exceptions>`
    * |new_manual.ruffus_names.chapter_num| :ref:`Names (keywords) exported from Ruffus <new_manual.ruffus_names>`
    * |new_manual.deprecated_files.chapter_num|: :ref:`Legacy and deprecated syntax @files <new_manual.deprecated_files>`
    * |new_manual.deprecated_files_re.chapter_num|: :ref:`Legacy and deprecated syntax @files_re <new_manual.deprecated_files_re>`



**Ruffus** Manual: List of Example Code for Each Chapter:

    * :ref:`new_manual.introduction.code`
    * :ref:`new_manual.transform.code`
    * :ref:`new_manual.transform_in_parallel.code`
    * :ref:`new_manual.originate.code`
    * :ref:`new_manual.pipeline_printout.code`
    * :ref:`new_manual.pipeline_printout_graph.code`
    * :ref:`new_manual.output_file_names.code`
    * :ref:`new_manual.mkdir.code`
    * :ref:`new_manual.checkpointing.code`
    * :ref:`new_manual.split.code`
    * :ref:`new_manual.merge.code`
    * :ref:`new_manual.multiprocessing.code`
    * :ref:`new_manual.logging.code`
    * :ref:`new_manual.subdivide_collate.code`
    * :ref:`new_manual.combinatorics.code`
    * :ref:`new_manual.inputs.code`
    * :ref:`new_manual.on_the_fly.code`

.. toctree::
   :caption: Example code
   :name: example_code_toc
   :hidden:
   :maxdepth: 1

   introduction_code.rst
   transform_code.rst
   transform_in_parallel_code.rst
   originate_code.rst
   pipeline_printout_code.rst
   pipeline_printout_graph_code.rst
   output_file_names_code.rst
   mkdir_code.rst
   checkpointing_code.rst
   split_code.rst
   merge_code.rst
   multiprocessing_code.rst
   logging_code.rst
   subdivide_collate_code.rst
   combinatorics_code.rst
   inputs_code.rst
   onthefly_code.rst
   flowchart_colours_code.rst

.. toctree::
   :maxdepth: 2
   :hidden:

   ../../examples/bioinformatics/index.rst
   ../../examples/bioinformatics/part2.rst
   ../../examples/bioinformatics/part1_code.rst
   ../../examples/bioinformatics/part2_code.rst
   ../../examples/paired_end_data.py.rst


