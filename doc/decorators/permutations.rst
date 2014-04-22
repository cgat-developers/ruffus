.. include:: ../global.inc
.. _decorators.permutations:
.. index::
    pair: @permutations; Syntax

.. seealso::

    * :ref:`Decorators <decorators>` for more decorators

########################
@permutations
########################

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.permutations.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.permutations.extra_parameters`_
.. |output_pattern| replace:: `output_pattern`
.. _output_pattern: `decorators.permutations.output_pattern`_
.. |matching_formatter| replace:: `matching_formatter`
.. _matching_formatter: `decorators.permutations.matching_formatter`_



********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
*@permutations* ( |tasks_or_file_names|_, :ref:`formatter<decorators.formatter>`\ *(*\ |matching_formatter|_\ *)*\, |output_pattern|_, [|extra_parameters|_,...] )
********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    **Purpose:**

        Generates the **permutations**, between all the elements of a set of **Input**

        The effect is analogous to the python `itertools  <http://docs.python.org/2/library/itertools.html#itertools.permutations>`__
        function of the same name:

        .. code-block:: pycon
            :emphasize-lines: 2

            >>> from itertools import permutations
            >>> # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
            >>> [ "".join(a) for a in permutations("ABCD", 2)]
            ['AB', 'AC', 'AD', 'BA', 'BC', 'BD', 'CA', 'CB', 'CD', 'DA', 'DB', 'DC']

        Only out of date tasks (comparing input and output files) will be run

        Output file names and strings in the extra parameters
        are determined from |tasks_or_file_names|_, i.e. from the output
        of up stream tasks, or a list of file names, after string replacement via
        :ref:`formatter<decorators.formatter>`.

        The replacement strings require an extra level of indirection to refer to
        parsed components:

            #. The first level refers to which *set* in each tuple of inputs.
            #. The second level refers to which input file in any particular *set* of inputs.

    **Example**:

        Calculates the **@permutations** of **A,B,C,D** files

        .. code-block:: python
            :emphasize-lines: 13,17,20,25,28-30

            from ruffus import *
            from ruffus.combinatorics import *

            #   initial file pairs
            @originate([ ['A.1_start', 'A.2_start'],
                         ['B.1_start', 'B.2_start'],
                         ['C.1_start', 'C.2_start'],
                         ['D.1_start', 'D.2_start']])
            def create_initial_files_ABCD(output_files):
                for output_file in output_files:
                    with open(output_file, "w") as oo: pass

            #   @permutations
            @permutations(create_initial_files_ABCD,      # Input
                          formatter(),                    # match input files

                          # tuple of 2 at a time
                          2,

                          # Output Replacement string
                          "{path[0][0]}/"
                          "{basename[0][1]}_vs_"
                          "{basename[1][1]}.permutations",

                          # Extra parameter: path for 1st set of files, 1st file name
                          "{path[0][0]}",

                          # Extra parameter
                          ["{basename[0][0]}",  # basename for 1st set of files, 1st file name
                           "{basename[1][0]}",  #                                2nd
                           ])
            def permutations_task(input_file, output_parameter, shared_path, basenames):
                print " - ".join(basenames)


            #
            #       Run
            #
            pipeline_run(verbose=0)


        This results in:

        .. code-block:: pycon

            >>> pipeline_run(verbose=0)

            A - B
            A - C
            A - D
            B - A
            B - C
            B - D
            C - A
            C - B
            C - D
            D - A
            D - B
            D - C


    **Parameters:**


.. _decorators.permutations.tasks_or_file_names:

    * *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_.
             E.g.:``"a.*" => "a.1", "a.2"``


.. _decorators.permutations.matching_formatter:

    * *matching_formatter*
       a :ref:`formatter<decorators.formatter>` indicator object containing optionally
       a  python `regular expression (re) <http://docs.python.org/library/re.html>`_.


.. _decorators.permutations.output_pattern:

    * *output_pattern*
        Specifies the resulting output file name(s) after string
        substitution


.. _decorators.permutations.extra_parameters:

    * *extra_parameters*
        Optional extra parameters are passed to the functions after string
        substitution

