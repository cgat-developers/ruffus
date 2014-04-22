.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.inputs.code:

############################################################################################################################################################################################################
|new_manual.inputs.chapter_num|: Python Code for Manipulating task inputs via string substitution using :ref:`inputs() <decorators.inputs>`  and  :ref:`add_inputs() <decorators.add_inputs>`
############################################################################################################################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`inputs() <decorators.inputs>` syntax
    * :ref:`add_inputs() <decorators.add_inputs>` syntax
    * Back to |new_manual.inputs.chapter_num|: :ref:`Manipulating task inputs via string substitution <new_manual.inputs>`

******************************************************************************************************************************************************
Example code for adding additional *input* prerequisites per job with :ref:`add_inputs() <decorators.add_inputs>`
******************************************************************************************************************************************************

.. _new_manual.inputs.example1:

===================================================================
1. Example: compiling c++ code
===================================================================

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


    Giving:

        .. code-block:: pycon

            >>> pipeline_run()
                Job  = [hasty.cpp -> hasty.o] completed
                Job  = [messy.cpp -> messy.o] completed
                Job  = [tasty.cpp -> tasty.o] completed
            Completed Task = compile

.. _new_manual.inputs.example2:

======================================================================================================================================
2. Example: Adding a common header file with :ref:`add_inputs() <decorators.add_inputs>`
======================================================================================================================================


    .. code-block:: python
        :emphasize-lines: 12

        # source files exist before our pipeline
        source_files = ["hasty.cpp", "tasty.cpp", "messy.cpp"]
        for source_file in source_files:
            open(source_file, "w")

        # common (universal) header exists before our pipeline
        open("universal.h", "w")

        from ruffus import *

        @transform( source_files, suffix(".cpp"),
                    # add header to the input of every job
                    add_inputs("universal.h"),
                    ".o")
        def compile(input_filename, output_file):
            open(output_file, "w")

        pipeline_run()

    Giving:

        .. code-block:: pycon

            >>> pipeline_run()
                Job  = [[hasty.cpp, universal.h] -> hasty.o] completed
                Job  = [[messy.cpp, universal.h] -> messy.o] completed
                Job  = [[tasty.cpp, universal.h] -> tasty.o] completed
            Completed Task = compile

.. _new_manual.inputs.example3:

=====================================================================
3. Example: Additional *Input* can be tasks
=====================================================================

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

    Giving:

        .. code-block:: pycon


            >>> pipeline_run()
                Job  = [hasty.cpp -> hasty.h] completed
                Job  = [messy.cpp -> messy.h] completed
                Job  = [tasty.cpp -> tasty.h] completed
            Completed Task = create_matching_headers
                Job  = [[hasty.cpp, universal.h, hasty.h, messy.h, tasty.h] -> hasty.o] completed
                Job  = [[messy.cpp, universal.h, hasty.h, messy.h, tasty.h] -> messy.o] completed
                Job  = [[tasty.cpp, universal.h, hasty.h, messy.h, tasty.h] -> tasty.o] completed
            Completed Task = compile

.. _new_manual.inputs.example4:

================================================================================================================================================================================================================================================
4. Example: Add corresponding files using :ref:`add_inputs() <decorators.add_inputs>` with :ref:`formatter <decorators.formatter>` or :ref:`regex <decorators.regex>`
================================================================================================================================================================================================================================================

    .. code-block:: python
        :emphasize-lines: 11,17,19

        # source files exist before our pipeline
        source_files = ["hasty.cpp", "tasty.cpp", "messy.cpp"]
        header_files = ["hasty.h", "tasty.h", "messy.h"]
        for source_file in source_files + header_files:
            open(source_file, "w")

        # common (universal) header exists before our pipeline
        open("universal.h", "w")

        from ruffus import *

        @transform( source_files,
                    formatter(".cpp$"),
                                # corresponding header for each source file
                    add_inputs("{basename[0]}.h",
                               # add header to the input of every job
                               "universal.h"),
                    "{basename[0]}.o")
        def compile(input_filename, output_file):
            open(output_file, "w")

        pipeline_run()

    Giving:

        .. code-block:: pycon

            >>> pipeline_run()
                Job  = [[hasty.cpp, hasty.h, universal.h] -> hasty.o] completed
                Job  = [[messy.cpp, messy.h, universal.h] -> messy.o] completed
                Job  = [[tasty.cpp, tasty.h, universal.h] -> tasty.o] completed
            Completed Task = compile

*********************************************************************************************
Example code for replacing all input parameters with :ref:`inputs() <decorators.inputs>`
*********************************************************************************************

.. _new_manual.inputs.example5:

================================================================================================================================================================================================================================================
5. Example: Running matching python scripts using :ref:`inputs() <decorators.inputs>`
================================================================================================================================================================================================================================================

    .. code-block:: python
        :emphasize-lines: 11,17,19

        # source files exist before our pipeline
        source_files = ["hasty.cpp", "tasty.cpp", "messy.cpp"]
        python_files = ["hasty.py", "tasty.py", "messy.py"]
        for source_file in source_files + python_files:
            open(source_file, "w")

        # common (universal) header exists before our pipeline
        open("universal.h", "w")

        from ruffus import *

        @transform( source_files,
                    formatter(".cpp$"),
                    # corresponding python file for each source file
                    inputs("{basename[0]}.py"),

                    "{basename[0]}.results")
        def run_corresponding_python(input_filenames, output_file):
            open(output_file, "w")


        pipeline_run()

    Giving:

        .. code-block:: pycon

            >>> pipeline_run()
                Job  = [hasty.py -> hasty.results] completed
                Job  = [messy.py -> messy.results] completed
                Job  = [tasty.py -> tasty.results] completed
            Completed Task = run_corresponding_python

