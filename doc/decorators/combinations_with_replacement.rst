.. include:: ../global.inc
.. _decorators.combinations_with_replacement:
.. index::
    pair: @combinations_with_replacement; Syntax

.. seealso::

    * :ref:`Decorators <decorators>` for more decorators

################################################
@combinations_with_replacement
################################################

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.combinations_with_replacement.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.combinations_with_replacement.extra_parameters`_
.. |output_pattern| replace:: `output_pattern`
.. _output_pattern: `decorators.combinations_with_replacement.output_pattern`_
.. |matching_formatter| replace:: `matching_formatter`
.. _matching_formatter: `decorators.combinations_with_replacement.matching_formatter`_



********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
*@combinations_with_replacement* ( |tasks_or_file_names|_, :ref:`formatter<decorators.formatter>`\ *(*\ |matching_formatter|_\ *)*\, |output_pattern|_, [|extra_parameters|_,...] )
********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    **Purpose:**

        Generates the **combinations_with_replacement**, between all the elements of a set of **Input** (e.g. **A B C D**),
        i.e. r-length tuples of *input* elements included repeated elements (**A A**)
        and where order of the tuples is irrelevant (either **A B** or  **B A**, not both).

        The effect is analogous to the python `itertools  <http://docs.python.org/2/library/itertools.html#itertools.combinations_with_replacement>`__
        function of the same name:

        .. code-block:: pycon
            :emphasize-lines: 2

            >>> from itertools import combinations_with_replacement
            >>> # combinations_with_replacement('ABCD', 2) --> AA AB AC AD BB BC BD CC CD DD
            >>> [ "".join(a) for a in combinations_with_replacement('ABCD', 2)]
            ['AA', 'AB', 'AC', 'AD', 'BB', 'BC', 'BD', 'CC', 'CD', 'DD']

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

        Calculates the **@combinations_with_replacement** of **A,B,C,D** files

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

            #   @combinations_with_replacement
            @combinations_with_replacement(create_initial_files_ABCD,   # Input
                          formatter(),                                  # match input files

                          # tuple of 2 at a time
                          2,

                          # Output Replacement string
                          "{path[0][0]}/"
                          "{basename[0][1]}_vs_"
                          "{basename[1][1]}.combinations_with_replacement",

                          # Extra parameter: path for 1st set of files, 1st file name
                          "{path[0][0]}",

                          # Extra parameter
                          ["{basename[0][0]}",  # basename for 1st set of files, 1st file name
                           "{basename[1][0]}",  #              2rd
                           ])
            def combinations_with_replacement_task(input_file, output_parameter, shared_path, basenames):
                print " - ".join(basenames)


            #
            #       Run
            #
            pipeline_run(verbose=0)


        This results in:

        .. code-block:: pycon

            >>> pipeline_run(verbose=0)
            A - A
            A - B
            A - C
            A - D
            B - B
            B - C
            B - D
            C - C
            C - D
            D - D


    **Parameters:**


.. _decorators.combinations_with_replacement.tasks_or_file_names:

    * *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_.
             E.g.:``"a.*" => "a.1", "a.2"``


.. _decorators.combinations_with_replacement.matching_formatter:

    * *matching_formatter*
       a :ref:`formatter<decorators.formatter>` indicator object containing optionally
       a  python `regular expression (re) <http://docs.python.org/library/re.html>`_.


.. _decorators.combinations_with_replacement.output_pattern:

    * *output_pattern*
        Specifies the resulting output file name(s) after string
        substitution


.. _decorators.combinations_with_replacement.extra_parameters:

    * *extra_parameters*
        Optional extra parameters are passed to the functions after string
        substitution

