.. include:: ../global.inc
.. _decorators.subdivide:
.. index::
    pair: @subdivide; Syntax

.. seealso::

    * :ref:`@subdivide <new_manual.subdivide>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

########################
subdivide
########################

.. |input| replace:: `input`
.. _input: `decorators.subdivide.input`_
.. |extras| replace:: `extras`
.. _extras: `decorators.subdivide.extras`_
.. |output| replace:: `output`
.. _output: `decorators.subdivide.output`_
.. |matching_regex| replace:: `matching_regex`
.. _matching_regex: `decorators.subdivide.matching_regex`_
.. |matching_formatter| replace:: `matching_formatter`
.. _matching_formatter: `decorators.subdivide.matching_formatter`_
.. |input_pattern_or_glob| replace:: `input_pattern_or_glob`
.. _input_pattern_or_glob: `decorators.subdivide.input_pattern_or_glob`_


************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
*@subdivide* ( |input|_, :ref:`regex<decorators.regex>`\ *(*\ |matching_regex|_\ *)* |  :ref:`formatter<decorators.formatter>`\ *(*\ |matching_formatter|_\ *)*\, [ :ref:`inputs<decorators.inputs>` *(*\ |input_pattern_or_glob|_\ *)* | :ref:`add_inputs<decorators.add_inputs>` *(*\ |input_pattern_or_glob|_\ *)* ], |output|_, [|extras|_,...]  )
************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    **Purpose:**

        * Subdivides a set of *Inputs* each further into multiple *Outputs*.

        * **Many to Even More** operator

        * The number of files in each *Output* can be set at runtime by the use of globs

        * Output file names are specified using the :ref:`formatter<decorators.formatter>` or :ref:`regex<decorators.regex>` indicators from |input|_, i.e. from the output
          of specified tasks, or a list of file names, or a |glob|_ matching pattern.

        * Additional inputs or dependencies can be added dynamically to the task:
            :ref:`add_inputs<decorators.add_inputs>` nests the the original input parameters in a list before adding additional dependencies.

            :ref:`inputs<decorators.inputs>` replaces the original input parameters wholescale.

        * Only out of date tasks (comparing input and output files) will be run.

        .. note::

            The use of **split** is a synonym for subdivide is deprecated.


    **Example**:

        .. code-block:: python
            :emphasize-lines: 17,19,23

            from ruffus import *
            from random import randint
            from random import os

            @originate(['0.start', '1.start', '2.start'])
            def create_files(output_file):
                with open(output_file, "w"):
                    pass


            #
            #   Subdivide each of 3 start files further into
            #      [NNN1, NNN2, NNN3] number of files
            #      where NNN1, NNN2, NNN3 are determined at run time
            #
            @subdivide(create_files, formatter(),
                        # Output parameter: Glob matches any number of output file names
                        "{path[0]}/{basename[0]}.*.step1",
                        # Extra parameter:  Append to this for output file names
                        "{path[0]}/{basename[0]}")
            def subdivide_files(input_file, output_files, output_file_name_root):
                #
                #   IMPORTANT: cleanup rubbish from previous run first
                #
                for oo in output_files:
                    os.unlink(oo)
                #   The number of output files is decided at run time
                number_of_output_files = randint(2,4)
                for ii in range(number_of_output_files):
                    output_file_name = "{output_file_name_root}.{ii}.step1".format(**locals())
                    with open(output_file_name, "w"):
                        pass


            #
            #   Each output of subdivide_files results in a separate job for downstream tasks
            #
            @transform(subdivide_files, suffix(".step1"), ".step2")
            def analyse_files(input_file, output_file_name):
                with open(output_file_name, "w"):
                    pass

            pipeline_run()

        .. comment **

            The Ruffus printout shows how each of the jobs in ``subdivide_files()`` spawns
            multiple *Output* leading to more jobs in ``analyse_files()``


        .. code-block:: pycon

            >>> pipeline_run()
                Job  = [None -> 0.start] completed
                Job  = [None -> 1.start] completed
                Job  = [None -> 2.start] completed
            Completed Task = create_files
                Job  = [0.start -> 0.*.step1, 0] completed
                Job  = [1.start -> 1.*.step1, 1] completed
                Job  = [2.start -> 2.*.step1, 2] completed
            Completed Task = subdivide_files
                Job  = [0.0.step1 -> 0.0.step2] completed
                Job  = [0.1.step1 -> 0.1.step2] completed
                Job  = [0.2.step1 -> 0.2.step2] completed
                Job  = [1.0.step1 -> 1.0.step2] completed
                Job  = [1.1.step1 -> 1.1.step2] completed
                Job  = [1.2.step1 -> 1.2.step2] completed
                Job  = [1.3.step1 -> 1.3.step2] completed
                Job  = [2.0.step1 -> 2.0.step2] completed
                Job  = [2.1.step1 -> 2.1.step2] completed
                Job  = [2.2.step1 -> 2.2.step2] completed
                Job  = [2.3.step1 -> 2.3.step2] completed
            Completed Task = analyse_files




    **Parameters:**


.. _decorators.subdivide.input:

    * *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_.
             E.g.:``"a.*" => "a.1", "a.2"``


.. _decorators.subdivide.matching_regex:

    * *matching_regex*
       is a python regular expression string, which must be wrapped in
       a :ref:`regex<decorators.regex>` indicator object
       See python `regular expression (re) <http://docs.python.org/library/re.html>`_
       documentation for details of regular expression syntax

.. _decorators.subdivide.matching_formatter:

    * *matching_formatter*
       a :ref:`formatter<decorators.formatter>` indicator object containing optionally
       a  python `regular expression (re) <http://docs.python.org/library/re.html>`_.

.. _decorators.subdivide.output:

    * **output** = *output*
        Specifies the resulting output file name(s) after string substitution

        Can include glob patterns.


.. _decorators.subdivide.input_pattern_or_glob:

    * *input_pattern*
       Specifies the resulting input(s) to each job.
       Must be wrapped in an :ref:`inputs<decorators.inputs>` or an :ref:`inputs<decorators.add_inputs>` indicator object.

       Can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.

       Strings are subject to :ref:`regex<decorators.regex>` or :ref:`formatter<decorators.formatter>` substitution.


.. _decorators.subdivide.extras:

    * **extras** = *extras*
       Any extra parameters are passed verbatim to the task function

       If you are using named parameters, these can be passed as a list, i.e. ``extras= [...]``

       Any extra parameters are consumed by the task function and not forwarded further down the pipeline.

       Strings are subject to :ref:`regex<decorators.regex>` or :ref:`formatter<decorators.formatter>`
       substitution.
