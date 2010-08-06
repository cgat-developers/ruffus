.. include:: ../../global.inc
.. include:: chapter_numbers.inc

.. _manual.transform_ex:

######################################################################################################################################################
|manual.transform_ex.chapter_num|: **add_inputs()** `and` **inputs()**: `Controlling both input and output files with` **@transform**
######################################################################################################################################################

    .. hlist::

        * :ref:`Manual overview <manual>`
        * :ref:`@transform <decorators.transform>` syntax in detail


    .. index::
        pair: @transform (Advanced Usage); Manual


    The standard :ref:`@transform <manual.transform>` allows you to send a list of data files
    to the same pipelined function and for the resulting *outputs* parameter to be automatically
    inferred from file names in the *inputs*.

    There are two situations where you might desire additional flexibility:
        #. You need to add additional prequisites or filenames to the *inputs* of every single one
           of your jobs
        #. (Less often,) the actual *inputs* file names are some variant of the *outputs* of another
           task.

    Either way, it is occasionally very useful to be able to generate the actual *inputs* as
    well as *outputs* parameters by regular expression substitution. The following examples will show
    you both how and why you would want to do this.

====================================================================
Adding additional *input* prerequisites per job
====================================================================


************************************************************************
1.) Example: compiling c++ code
************************************************************************

    Suppose we wished to compile some c++ (``"*.cpp"``) files:
        .. comment << Pythoncode

        ::

            source_files = "hasty.cpp", "tasty.cpp", "messy.cpp"
            for source_file in source_files:
                open(source_file, "w")

    .. comment
        Pythoncode


    The ruffus code would look like this:
        .. comment << Pythoncode

        ::

            from ruffus import *

            @transform(source_files, suffix(".cpp"), ".o")
            def compile(input_filename, output_file_name):
                open(output_file_name, "w")

    .. comment
        Pythoncode


    This results in the following jobs:
        ::

            >>> pipeline_run([compile], verbose = 2, multiprocess = 3)

                Job = [None -> hasty.cpp] completed
                Job = [None -> tasty.cpp] completed
                Job = [None -> messy.cpp] completed
            Completed Task = prepare_cpp_source

                Job = [hasty.cpp -> hasty.o] completed
                Job = [messy.cpp -> messy.o] completed
                Job = [tasty.cpp -> tasty.o] completed
            Completed Task = compile

************************************************************************
2.) Example: Adding a header file with **add_inputs(..)**
************************************************************************


    All this is plain vanilla **@transform** syntax. But suppose that we need to add a
    common header file ``"universal.h"`` to our compilation.
    The **add_inputs** provides for this with the minimum of fuss:

        .. comment << Pythoncode

        ::

            # create header file
            open("universal.h", "w")

            # compile C++ files with extra header
            @transform(prepare_cpp_source, suffix(".cpp"), add_inputs("universal.h"), ".o")
            def compile(input_filename, output_file_name):
                open(output_file_name, "w")

    .. comment
        Pythoncode

    Now the input file is a python list, with ``"universal.h"`` added to each ``"*.cpp"``

        ::

            >>> pipeline_run([compile], verbose = 2, multiprocess = 3)

                Job = [ [hasty.cpp, universal.h] -> hasty.o] completed
                Job = [ [messy.cpp, universal.h] -> messy.o] completed
                Job = [ [tasty.cpp, universal.h] -> tasty.o] completed
            Completed Task = compile


================================================================================
Additional *input* prerequisites can be globs, tasks or pattern matches
================================================================================

    A common requirement is to include the corresponding header file in compilations.
    It is easy to use **add_inputs** to look up additional files via pattern matches.

************************************************************************
3.) Example: Adding matching header file
************************************************************************

    To make this example more fun, we shall also:
        #) Give each source code file its own ordinal
        #) Use ``add_inputs`` to add files produced by another task function

    .. comment << Pythoncode

    ::

        # each source file has its own index
        source_names = [("hasty.cpp", 1),
                        ("tasty.cpp", 2),
                        ("messy.cpp", 3), ]
        header_names = [sn.replace(".cpp", ".h") for (sn, i) in source_names]
        header_names.append("universal.h")

        #
        #   create header and source files
        #
        for source, source_index in source_names:
            open(source, "w")

        for header in header_names:
            open(header, "w")



        from ruffus import *

        #
        #   lookup embedded strings in each source files
        #
        @transform(source_names, suffix(".cpp"), ".embedded")
        def get_embedded_strings(input_filename, output_file_name):
            open(output_file_name, "w")



        # compile C++ files with extra header
        @transform(source_names, suffix(".cpp"),
                   add_inputs(  "universal.h",
                                r"\1.h",
                                get_embedded_strings     ), ".o")
        def compile(input_params, output_file_name):
            open(output_file_name, "w")


        pipeline_run([compile], verbose = 2, multiprocess = 3)

    .. comment
        Pythoncode

    This script gives the following output

        ::

                >>> pipeline_run([compile], verbose = 2, multiprocess = 3)

                    Job = [[hasty.cpp,  1] -> hasty.embedded] completed
                    Job = [[messy.cpp,  3] -> messy.embedded] completed
                    Job = [[tasty.cpp,  2] -> tasty.embedded] completed
                Completed Task = get_embedded_strings

                    Job = [[[hasty.cpp,  1],                                            # inputs
                            universal.h,                                                # common header
                            hasty.h,                                                    # corresponding header
                            hasty.embedded, messy.embedded, tasty.embedded]             # output of get_embedded_strings()
                           -> hasty.o] completed
                    Job = [[[messy.cpp, 3],                                             # inputs
                            universal.h,                                                # common header
                            messy.h,                                                    # corresponding header
                            hasty.embedded, messy.embedded, tasty.embedded]             # output of get_embedded_strings()
                           -> messy.o] completed
                    Job = [[[tasty.cpp, 2],                                             # inputs
                            universal.h,                                                # common header
                            tasty.h,                                                    # corresponding header
                            hasty.embedded, messy.embedded, tasty.embedded]             # output of get_embedded_strings()
                           -> tasty.o] completed
                Completed Task = compile

    We can see that the ``compile(...)`` task now has four sets of *inputs*:
        1) The original inputs (e.g. ``[hasty.cpp,  1]``)

    And three additional added by **add_inputs(...)**
        2) A header file (``universal.h``) common to all jobs
        3) The matching header (e.g. ``hasty.h``)
        4) The output from another task ``get_embedded_strings()`` (e.g. ``hasty.embedded, messy.embedded, tasty.embedded``)

    .. note::
        For input parameters with nested structures (lists or sets), the pattern matching is
        on the first filename string Ruffus comes across (DFS).

        So for ``["hasty.c", 0]``, the pattern matches ``"hasty.c"``.

        If in doubt, use :ref:`pipeline_printout <manual.tracing_pipeline_parameters>` to
        check what parameters Ruffus is using.


************************************************************************
4.) Example: Using **regex(..)** instead of **suffix(..)**
************************************************************************
    Suffix pattern matching is much simpler and hence is usually preferable to the more
    powerful regular expressions. We can rewrite the above example to use **regex** as well
    to give exactly the same output.

    .. comment << Pythoncode

    ::

        # compile C++ files with extra header
        @transform(source_names, regex(r"(.+)\.cpp"),
                   add_inputs(  "universal.h",
                                r"\1.h",
                                get_embedded_strings     ), r"\1.o")
        def compile(input_params, output_file_name):
            open(output_file_name, "w")

    .. comment
        Pythoncode

    .. note::
        The backreference ``\g<0>`` usefully substitutes the entire substring matched by
        the regular expression.



====================================================================
Replacing all input parameters with **inputs(...)**
====================================================================

    More rarely, it is necessary to replace all the input parameters wholescale.

************************************************************************
4.) Example: Running matching python scripts
************************************************************************
    In the following example, we are not compiling C++ source files but invoking
    corresponding python scripts which have the same name.

    Given three c++ files and their corresponding python scripts:

        .. comment << Pythoncode

        ::

            # each source file has its own index
            source_names = [("hasty.cpp", 1),
                            ("tasty.cpp", 2),
                            ("messy.cpp", 3), ]

            #
            #   create c++ source files and corresponding python files
            #
            for source, source_index in source_names:
                open(source, "w")
                open(source.replace(".cpp", ".py"), "w")

        .. comment
            Pythoncode

    The Ruffus code will call each python script corresponding to their c++ counterpart:

        .. comment << Pythoncode

        ::

            from ruffus import *


            # run corresponding python files
            @transform(source_names, suffix(".cpp"), inputs(  r"\1.py"), ".results")
            def run_python_file(input_params, output_file_name):
                open(output_file_name, "w")


            pipeline_run([run_python_file], verbose = 2, multiprocess = 3)

        .. comment
            Pythoncode

    Resulting in this output:
        ::

            >>> pipeline_run([run_python_file], verbose = 2, multiprocess = 3)
                Job = [hasty.py -> hasty.results] completed
                Job = [messy.py -> messy.results] completed
                Job = [tasty.py -> tasty.results] completed
            Completed Task = run_python_file


************************************************************************
5.) Example: Using **regex** instead of **suffix**
************************************************************************

    Again, the same code can be written (less clearly) using the more powerful
    **regex** and python regular expressions:

        .. comment << Pythoncode

        ::

            from ruffus import *


            # run corresponding python files
            @transform(source_names, regex(r"(.+)\.cpp"), inputs(  r"\1.py"), r\"1.results")
            def run_python_file(input_params, output_file_name):
                open(output_file_name, "w")


            pipeline_run([run_python_file], verbose = 2, multiprocess = 3)

        .. comment
            Pythoncode


    This is about as sophisticated as **@transform** ever gets!
