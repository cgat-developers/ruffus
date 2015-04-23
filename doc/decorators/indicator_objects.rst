.. include:: ../global.inc


.. seealso::
    * :ref:`Decorators <decorators>`
    * :ref:`suffix(...) <new_manual.suffix>` in the **Ruffus** Manual
    * :ref:`regex(...) <new_manual.regex>` in the **Ruffus** Manual
    * :ref:`formatter(...) <new_manual.formatter>` in the **Ruffus** Manual

.. index::
    single: Indicator Object (Disambiguating parameters)

.. _decorators.indicator_objects:


########################
Indicator Objects
########################



    How *ruffus* disambiguates certain parameters to decorators.

    They are like `keyword arguments <http://docs.python.org/tutorial/controlflow.html#keyword-arguments>`_ in python, a little more verbose but they make the syntax much simpler.

    Indicator objects are also "self-documenting" so you can see
    exactly what is happening clearly.


.. index::
    pair: formatter; Indicator Object (Disambiguating parameters)

.. _decorators.formatter:


*********************************************
*formatter*
*********************************************

    **formatter([** ``regex | None`` **, regex | None...])**

    * The optional enclosed parameters are a python regular expression strings
    * Each regular expression matches a corresponding *Input* file name string
    * *formatter* parses each file name string into path and regular expression components
    * Parsing fails altogether if the regular expression is not matched

    Path components include:

        * ``basename``: The `base name <http://docs.python.org/2/library/os.path.html#os.path.basename>`__ *excluding* `extension  <http://docs.python.org/2/library/os.path.html#os.path.splitext>`__, ``"file.name"``
        * ``ext``     : The `extension <http://docs.python.org/2/library/os.path.html#os.path.splitext>`__, ``".ext"``
        * ``path``    : The `dirname <http://docs.python.org/2/library/os.path.html#os.path.dirname>`__, ``"/directory/to/a"``
        * ``subdir``  : A list of sub-directories in the ``path`` in reverse order, ``["a", "to", "directory", "/"]``
        * ``subpath`` : A list of descending sub-paths in reverse order, ``["/directory/to/a", "/directory/to", "/directory", "/"]``

    The replacement string refers to these components using python `string.format <http://docs.python.org/2/library/string.html#string-formatting>`__ style curly braces. ``{NAME}``

    We refer to an element from the Nth input string by index, for example:

       * ``"{ext[0]}"``     is the extension of the first input string.
       * ``"{basename[1]}"`` is the basename of the second input string.
       * ``"{basename[1][0:3]}"`` are the first three letters from the basename of the second input string.

    **Used by:**
        * :ref:`@split <decorators.split>`
        * :ref:`@transform <decorators.transform>`
        * :ref:`@merge <decorators.merge>`
        * :ref:`@subdivide <decorators.subdivide>`
        * :ref:`@collate <decorators.collate>`
        * :ref:`@product <decorators.product>`
        * :ref:`@permutations <decorators.permutations>`
        * :ref:`@combinations <decorators.combinations>`
        * :ref:`@combinations_with_replacement <decorators.combinations_with_replacement>`

    **@transform example**:

        .. code-block:: python
            :emphasize-lines: 14, 18,19

            from ruffus import *

            #   create initial file pairs
            @originate([   ['job1.a.start', 'job1.b.start'],
                           ['job2.a.start', 'job2.b.start'],
                           ['job3.a.start', 'job3.c.start']    ])
            def create_initial_file_pairs(output_files):
                for output_file in output_files:
                    with open(output_file, "w") as oo: pass


            #---------------------------------------------------------------
            #
            #   formatter
            #
            @transform(create_initial_file_pairs,                      # Input

                        formatter(".+/job(?P<JOBNUMBER>\d+).a.start",  # Extract job number
                                  ".+/job[123].b.start"),              # Match only "b" files

                        ["{path[0]}/jobs{JOBNUMBER[0]}.output.a.1",    # Replacement list
                         "{path[1]}/jobs{JOBNUMBER[0]}.output.b.1"])
            def first_task(input_files, output_parameters):
                print "input_parameters = ", input_files
                print "output_parameters = ", output_parameters


            #
            #       Run
            #
            pipeline_run(verbose=0)

        This produces:

        .. code-block:: pycon

            input_parameters  =  ['job1.a.start',
                                  'job1.b.start']
            output_parameters =  ['/home/lg/src/temp/jobs1.output.a.1',
                                  '/home/lg/src/temp/jobs1.output.b.1', 45]

            input_parameters  =  ['job2.a.start',
                                  'job2.b.start']
            output_parameters =  ['/home/lg/src/temp/jobs2.output.a.1',
                                  '/home/lg/src/temp/jobs2.output.b.1', 45]

    **@permutations example**:

        Combinatoric decorators such as :ref:`@product <decorators.product>` or
        :ref:`@product <decorators.permutations>` behave much
        like nested for loops in enumerating, combining, and permutating the original sets
        of inputs.

        The replacement strings require an extra level of indirection to refer to
        parsed components:

        .. code-block:: python
            :emphasize-lines: 14,16,23-27

            from ruffus import *
            from ruffus.combinatorics import *

            #   create initial files
            @originate([ 'a.start', 'b.start', 'c.start'])
            def create_initial_files(output_file):
                with open(output_file, "w") as oo: pass


            #---------------------------------------------------------------
            #
            #   formatter
            #
            @permutations(create_initial_files,   # Input

                        formatter("(.start)$"),   # match input file in permutations
                        2,

                        "{path[0][0]}/"
                            "{basename[0][0]}_"
                            "vs_{basename[1][0]}"
                            ".product",           # Output Replacement string
                        "{path[0][0]}",           # path for 1st set of files, 1st file name
                        ["{basename[0][0]}",      # basename for 1st set of files, 1st file name
                         "{basename[1][0]}"])     # basename for 2nd set of files, 1st file name
            def product_task(input_file, output_parameter, shared_path, basenames):
                print "input_parameter  = ", input_file
                print "output_parameter = ", output_parameter
                print "shared_path      = ", shared_path
                print "basenames        = ", basenames


            #
            #       Run
            #
            pipeline_run(verbose=0)

        This produces:

        .. code-block:: pycon

            >>> pipeline_run(verbose=0)
            input_parameter  =  ('a.start', 'b.start')
            output_parameter =  /home/lg/src/oss/ruffus/a_vs_b.product
            shared_path      =  /home/lg/src/oss/ruffus
            basenames        =  ['a', 'b']

            input_parameter  =  ('a.start', 'c.start')
            output_parameter =  /home/lg/src/oss/ruffus/a_vs_c.product
            shared_path      =  /home/lg/src/oss/ruffus
            basenames        =  ['a', 'c']

            input_parameter  =  ('b.start', 'a.start')
            output_parameter =  /home/lg/src/oss/ruffus/b_vs_a.product
            shared_path      =  /home/lg/src/oss/ruffus
            basenames        =  ['b', 'a']

            input_parameter  =  ('b.start', 'c.start')
            output_parameter =  /home/lg/src/oss/ruffus/b_vs_c.product
            shared_path      =  /home/lg/src/oss/ruffus
            basenames        =  ['b', 'c']

            input_parameter  =  ('c.start', 'a.start')
            output_parameter =  /home/lg/src/oss/ruffus/c_vs_a.product
            shared_path      =  /home/lg/src/oss/ruffus
            basenames        =  ['c', 'a']

            input_parameter  =  ('c.start', 'b.start')
            output_parameter =  /home/lg/src/oss/ruffus/c_vs_b.product
            shared_path      =  /home/lg/src/oss/ruffus
            basenames        =  ['c', 'b']



.. index::
    pair: suffix; Indicator Object (Disambiguating parameters)

.. _decorators.suffix:


*********************************************
*suffix*
*********************************************

    **suffix(** ``string`` **)**

    The enclosed parameter is a string which must match *exactly* to the end
    of a file name.


    **Used by:**
        * :ref:`@transform <decorators.transform>`

    **Example**:
        ::

            #
            #   Transforms ``*.c`` to ``*.o``::
            #
            @transform(previous_task, suffix(".c"), ".o")
            def compile(infile, outfile):
                pass

.. index::
    pair: regex; Indicator Object (Disambiguating parameters)

.. _decorators.regex:

*********************************************
*regex*
*********************************************

    **regex(** ``regular_expression`` **)**


    The enclosed parameter is a python regular expression string,
    which must be wrapped in a ``regex`` indicator object.

    See python `regular expression (re) <http://docs.python.org/library/re.html>`_
    documentation for details of regular expression syntax


    **Used by:**

        * :ref:`@transform <decorators.transform>`
        * :ref:`@subdivide <decorators.subdivide>`
        * :ref:`@collate <decorators.collate>`
        * The deprecated :ref:`@files_re <decorators.files_re>`

    **Example**:
        ::

            @transform(previous_task, regex(r".c$"), ".o")
            def compile(infile, outfile):
                pass

.. index::
    pair: add_inputs; Indicator Object (Adding additional input parameters)

.. _decorators.add_inputs:

***********************************************
*add_inputs*
***********************************************

    **add_inputs(** ``input_file_pattern`` **)**

    The enclosed parameter(s) are pattern strings or a nested structure which is added to the
    input for each job.

    **Used by:**
        * :ref:`@transform <decorators.transform_ex>`
        * :ref:`@collate <decorators.transform_ex>`
        * :ref:`@subdivide <decorators.subdivide>`

    **Example @transform with suffix(...)**

        A common task in compiling C code is to include the corresponding header file for the source.
        To compile ``*.c`` to ``*.o``, adding ``*.h`` and the common header ``universal.h``:

            ::

                @transform(["1.c", "2.c"], suffix(".c"), add_inputs([r"\1.h", "universal.h"]),  ".o")
                def compile(infile, outfile):
                    # do something here
                    pass

        | The starting files names are ``1.c`` and ``2.c``.
        | ``suffix(".c")`` matches ".c" so ``\1`` stands for the unmatched prefices  ``"1"`` and ``"2"``

        This will result in the following functional calls:
            ::

                compile(["1.c", "1.h", "universal.h"], "1.o")
                compile(["2.c", "2.h", "universal.h"], "2.o")


        A string like ``universal.h`` in ``add_inputs`` will added *as is*.
        ``r"\1.h"``, however, performs suffix substitution, with the special form ``r"\1"`` matching everything up to the suffix.
        Remember to 'escape' ``r"\1"`` otherwise Ruffus will complain and throw an ``Exception`` to remind you.
        The most convenient way is to use a python "raw" string.

    **Example of add_inputs(...) with regex(...)**

        The suffix match (``suffix(...)``) is exactly equivalent to the following code using regular expression (``regex(...)``):
            ::

                @transform(["1.c", "2.c"], regex(r"^(.+)\.c$"),
                           add_inputs([r"\1.h", "universal.h"]),  r"\1.o")
                def compile(infile, outfile):
                    # do something here
                    pass

        The ``suffix(..)`` code is much simpler but the regular expression allows more complex substitutions.

    **add_inputs(...) preserves original inputs**

        ``add_inputs`` nests the the original input parameters in a list before adding additional dependencies.

        This can be seen in the following example:
            ::

                @transform([    ["1.c", "A.c", 2]
                                ["2.c", "B.c", "C.c", 3]],
                                suffix(".c"), add_inputs([r"\1.h", "universal.h"]),
                                ".o")
                def compile(infile, outfile):
                    # do something here
                    pass

        This will result in the following functional calls:
            ::

                compile([["1.c", "A.c", 2],        "1.h", "universal.h"], "1.o")
                compile([["3.c", "B.c", "C.c", 3], "2.h", "universal.h"], "2.o")


        The original parameters are retained unchanged as the first item in a list




.. index::
    pair: inputs; Indicator Object (Replacing input parameters)

.. _decorators.inputs:

***************************************
*inputs*
***************************************

    **inputs(** ``input_file_pattern`` **)**

    **Used by:**
        * :ref:`@transform <decorators.transform_ex>`
        * :ref:`@collate <decorators.transform_ex>`
        * :ref:`@subdivide <decorators.subdivide>`

    The enclosed single parameter is a pattern string or a nested structure which is
    used to construct the input for each job.

    If more than one argument is supplied to inputs, an exception will be raised.

    Use a tuple or list (as in the following example) to send multiple input arguments to each job.

    **Used by:**
        * The advanced form of :ref:`@transform <decorators.transform_ex>`

    **inputs(...) replaces original inputs**

        ``inputs(...)`` allows the original input parameters to be replaced wholescale.

        This can be seen in the following example:
            ::

                @transform([    ["1.c", "A.c", 2]
                                ["2.c", "B.c", "C.c", 3]],
                                suffix(".c"), inputs([r"\1.py", "docs.rst"]),  ".pyc")
                def compile(infile, outfile):
                    # do something here
                    pass

        This will result in the following functional calls:
            ::

                compile(["1.py", "docs.rst"], "1.pyc")
                compile(["2.py", "docs.rst"], "2.pyc")

        In this example, the corresponding python files have been sneakily substituted
        without trace in the place of the C source files.


.. index::
    single: @follows; mkdir (Syntax)
    single: mkdir; @follows (Syntax)
    single: Indicator Object (Disambiguating parameters); mkdir

.. _decorators.indicator_objects.mkdir:


******************************************************************************************
*mkdir*
******************************************************************************************

    **mkdir(** ``directory_name1`` **, [** ``directory_name2`` **, ...] )**

    The enclosed parameter is a directory name or a sequence of directory names.
    These directories will be created as part of the prerequisites of running a task.

    **Used by:**
        * :ref:`@follows <decorators.follows>`

    **Example:**
        ::

            @follows(mkdir("/output/directory"))
            def task():
                pass


.. index::
    single: @posttask; touch_file (Syntax)
    single: touch_file; @posttask (Syntax)
    single: Indicator Object (Disambiguating parameters); touch_file

.. _decorators.touch_file:


******************************************************************************************
*touch_file*
******************************************************************************************

    **touch_file(** ``file_name`` **)**

    The enclosed parameter is a file name. This file will be ``touch``\ -ed after a
    task is executed.

    This will change the date/time stamp of the ``file_name`` to the current date/time.
    If the file does not exist, an empty file will be created.


    **Used by:**
        * :ref:`@posttask <decorators.posttask>`

    **Example:**
        ::

            @posttask(touch_file("task_completed.flag"))
            @files(None, "a.1")
            def do_task(input_file, output_file):
                pass


.. index::
    pair: output_from; Indicator Object (Disambiguating parameters)

.. _decorators.output_from:

******************************************************************************************
*output_from*
******************************************************************************************

    **output_from (** ``file_name_string1`` **[,** ``file_name_string1`` **, ...] )**

    Indicates that any enclosed strings are not file names but refer to task functions.

    **Used by:**
        * :ref:`@split <decorators.split>`
        * :ref:`@transform <decorators.transform>`
        * :ref:`@merge <decorators.merge>`
        * :ref:`@collate <decorators.collate>`
        * :ref:`@subdivide <decorators.subdivide>`
        * :ref:`@product <decorators.product>`
        * :ref:`@permutations <decorators.permutations>`
        * :ref:`@combinations <decorators.combinations>`
        * :ref:`@combinations_with_replacement <decorators.combinations_with_replacement>`
        * :ref:`@files <decorators.files>`

    **Example:**
        ::

            @split(["a.file", ("b.file", output_from("task1", 76, "task2"))], "*.split")
            def task2(input, output):
                pass


        is equivalent to:

        ::

            @split(["a.file", ("b.file", (task1, 76, task2))], "*.split")
            def task2(input, output):
                pass




.. index::
    single: @files_re; combine (Deprecated Syntax)
    single: combine; @follows (Deprecated Syntax)
    single: Indicator Object (Disambiguating parameters); combine

.. _decorators.combine:

******************************************************************************************
*combine*
******************************************************************************************

    **combine(** ``arguments`` **)**

    .. warning::

        This is deprecated syntax.

        Please do not use!

        :ref:`@merge <decorators.merge>` and :ref:`@collate <decorators.collate>` are more powerful
        and have straightforward syntax.

    Indicates that the *inputs* of :ref:`@files_re <decorators.files_re>` will be collated
    or summarised into *outputs* by category. See the :ref:`Manual <new_manual.files_re.combine>`  or
    :ref:` @collate <new_manual.collate>` for examples.


    **Used by:**
        * :ref:`@files_re <new_manual.files_re.combine>`

    **Example:**
        ::

            @files_re('*.animals',                           # inputs = all *.animal files
                        r'mammals.([^.]+)',                  # regular expression
                        combine(r'\1/animals.in_my_zoo'),    # single output file per species
                        r'\1' )                              # species name
            def capture_mammals(infiles, outfile, species):
                # summarise all animals of this species
                ""

