.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: inputs; Tutorial
    pair: add_inputs; Tutorial
    pair: string substiution for inputs; Tutorial

.. _new_manual.inputs:

###########################################################################################################################################################################################################################################################################################
|new_manual.inputs.chapter_num|: Manipulating task inputs via string substitution using :ref:`inputs() <decorators.inputs>` and  :ref:`add_inputs() <decorators.add_inputs>`
###########################################################################################################################################################################################################################################################################################


.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`inputs() <decorators.inputs>` syntax
    * :ref:`add_inputs() <decorators.add_inputs>` syntax

.. note::

    Remember to look at the example code:

        * :ref:`new_manual.inputs.code`

***********************
Overview
***********************

    The previous chapters have been described how *Ruffus* allows the **Output** names for each job
    to be generated from the *Input* names via string substitution. This is how *Ruffus* can
    automatically chain multiple tasks in a pipeline together seamlessly.

    Sometimes it is useful to be able to modify the **Input**  by string substitution
    as well. There are two situations where this additional flexibility is needed:

        #. You need to add additional prequisites or filenames to the **Input** of every single job
        #. You need to add additional **Input** file names which are some variant of the existing ones.

    Both will be much more obvious with some examples


*******************************************************************************************************************
Adding additional *input* prerequisites per job with :ref:`add_inputs() <decorators.add_inputs>`
*******************************************************************************************************************


===================================================================
1. Example: compiling c++ code
===================================================================

    Let us first compile some c++ (``"*.cpp"``) files using plain :ref:`@transform <decorators.transform>` syntax:

    .. code-block:: python

            # source files exist before our pipeline
            source_files = ["hasty.cpp", "tasty.cpp", "messy.cpp"]
            for source_file in source_files:
                open(source_file, "w")

            from ruffus import *

            @transform(source_files, suffix(".cpp"), ".o")
            def compile(input_filename, output_file):
                open(output_file, "w")

            pipeline_run()


======================================================================================================================================
2. Example: Adding a common header file with :ref:`add_inputs() <decorators.add_inputs>`
======================================================================================================================================

    .. code-block:: python
        :emphasize-lines: 11,17,19

        # source files exist before our pipeline
        source_files = ["hasty.cpp", "tasty.cpp", "messy.cpp"]
        for source_file in source_files:
            open(source_file, "w")

        # common (universal) header exists before our pipeline
        open("universal.h", "w")

        from ruffus import *

        # make header files
        @transform(source_files, suffix(".cpp"), ".h")
        def create_matching_headers(input_file, output_file):
            open(output_file, "w")

        @transform(source_files, suffix(".cpp"),
                                # add header to the input of every job
                    add_inputs("universal.h",
                                # add result of task create_matching_headers to the input of every job
                               create_matching_headers),
                    ".o")
        def compile(input_filename, output_file):
            open(output_file, "w")

        pipeline_run()

            >>> pipeline_run()
                Job  = [hasty.cpp -> hasty.h] completed
                Job  = [messy.cpp -> messy.h] completed
                Job  = [tasty.cpp -> tasty.h] completed
            Completed Task = create_matching_headers
                Job  = [[hasty.cpp, universal.h, hasty.h, messy.h, tasty.h] -> hasty.o] completed
                Job  = [[messy.cpp, universal.h, hasty.h, messy.h, tasty.h] -> messy.o] completed
                Job  = [[tasty.cpp, universal.h, hasty.h, messy.h, tasty.h] -> tasty.o] completed
            Completed Task = compile


=====================================================================
3. Example: Additional *Input* can be tasks
=====================================================================

    We can also add a task name to :ref:`add_inputs() <decorators.add_inputs>`.
    This chains the **Output**, i.e. run time results, of any previous task as
    an additional **Input** to every single job in the task.

        .. code-block:: python
            :emphasize-lines: 1,7,9

            # make header files
            @transform(source_files, suffix(".cpp"), ".h")
            def create_matching_headers(input_file, output_file):
                open(output_file, "w")

            @transform(source_files, suffix(".cpp"),
                                    # add header to the input of every job
                        add_inputs("universal.h",
                                    # add result of task create_matching_headers to the input of every job
                                   create_matching_headers),
                        ".o")
            def compile(input_filenames, output_file):
                open(output_file, "w")

            pipeline_run()


        >>> pipeline_run()
            Job  = [[hasty.cpp, universal.h, hasty.h, messy.h, tasty.h] -> hasty.o] completed
            Job  = [[messy.cpp, universal.h, hasty.h, messy.h, tasty.h] -> messy.o] completed
            Job  = [[tasty.cpp, universal.h, hasty.h, messy.h, tasty.h] -> tasty.o] completed
        Completed Task = compile


================================================================================================================================================================================================================================================
4. Example: Add corresponding files using :ref:`add_inputs() <decorators.add_inputs>` with :ref:`formatter <decorators.formatter>` or :ref:`regex <decorators.regex>`
================================================================================================================================================================================================================================================
    The previous example created headers corresponding to our source files and added them
    as the **Input** to the compilation. That is generally not what you want. Instead,
    what is generally need is a way to

        1) Look up the exact corresponding header for the *specific* job, and not add all
           possible files to all jobs in a task. When compiling ``hasty.cpp``, we just need
           to add ``hasty.h`` (and ``universal.h``).
        2) Add a pre-existing file name (``hasty.h`` already exists. Don't create it via
           another task.)

    This is a surprisingly common requirement: In bioinformatics sometimes DNA or RNA
    sequence files come singly in  `*.fastq  <http://en.wikipedia.org/wiki/FASTQ_format>`__
    and sometimes in `matching pairs  <http://en.wikipedia.org/wiki/DNA_sequencing_theory#Pairwise_end-sequencing>`__:
    ``*1.fastq, *2.fastq`` etc. In the latter case, we often need to make sure that both
    sequence files are being processed in tandem. One way is to take one file name (``*1.fastq``)
    and look up the other.

     :ref:`add_inputs() <decorators.add_inputs>` uses standard *Ruffus* string substitution
     via :ref:`formatter <decorators.formatter>` and :ref:`regex <decorators.regex>` to lookup (generate) **Input** file names.
     (As a rule :ref:`suffix <decorators.suffix>` only substitutes **Output** file names.)

    .. code-block:: python
        :emphasize-lines: 3,5

        @transform( source_files,
                    formatter(".cpp$"),
                                # corresponding header for each source file
                    add_inputs("{basename[0]}.h",
                               # add header to the input of every job
                               "universal.h"),
                    "{basename[0]}.o")
        def compile(input_filenames, output_file):
            open(output_file, "w")

    This script gives the following output

        .. code-block:: pycon

            >>> pipeline_run()
                Job  = [[hasty.cpp, hasty.h, universal.h] -> hasty.o] completed
                Job  = [[messy.cpp, messy.h, universal.h] -> messy.o] completed
                Job  = [[tasty.cpp, tasty.h, universal.h] -> tasty.o] completed
            Completed Task = compile


********************************************************************************
Replacing all input parameters with :ref:`inputs() <decorators.inputs>`
********************************************************************************

    The previous examples all *added* to the set of **Input** file names.
    Sometimes it is necessary to replace all the **Input** parameters altogether.

================================================================================================================================================================================================================================================
5. Example: Running matching python scripts using :ref:`inputs() <decorators.inputs>`
================================================================================================================================================================================================================================================

    Here is a contrived example: we wish to find all cython/python files which have been
    compiled into corresponding c++ source files.
    Instead of compiling the c++, we shall invoke the corresponding python scripts.

    Given three c++ files and their corresponding python scripts:

        .. code-block:: python
            :emphasize-lines: 4

            @transform( source_files,
                        formatter(".cpp$"),

                        # corresponding python file for each source file
                        inputs("{basename[0]}.py"),

                        "{basename[0]}.results")
            def run_corresponding_python(input_filenames, output_file):
                open(output_file, "w")


    The *Ruffus* code will call each python script corresponding to their c++ counterpart:

        .. code-block:: pycon

            >>> pipeline_run()
                Job  = [hasty.py -> hasty.results] completed
                Job  = [messy.py -> messy.results] completed
                Job  = [tasty.py -> tasty.results] completed
            Completed Task = run_corresponding_python

