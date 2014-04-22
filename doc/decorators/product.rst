.. include:: ../global.inc
.. _decorators.product:
.. index::
    pair: @product; Syntax

.. seealso::

    * :ref:`Decorators <decorators>` for more decorators

########################
@product
########################

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.product.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.product.extra_parameters`_
.. |output_pattern| replace:: `output_pattern`
.. _output_pattern: `decorators.product.output_pattern`_
.. |matching_formatter| replace:: `matching_formatter`
.. _matching_formatter: `decorators.product.matching_formatter`_



********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
*@product* ( |tasks_or_file_names|_, :ref:`formatter<decorators.formatter>`\ *(*\ |matching_formatter|_\ *)*\, [|tasks_or_file_names|_, :ref:`formatter<decorators.formatter>`\ *(*\ |matching_formatter|_\ *)*\, ... ], |output_pattern|_, [|extra_parameters|_,...] )
********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    **Purpose:**

        Generates the Cartesian **product**, i.e. all vs all comparisons, between sets of input files.

        The effect is analogous to the python `itertools  <http://docs.python.org/2/library/itertools.html#itertools.product>`__
        function of the same name, i.e. a nested for loop.

        .. code-block:: pycon
            :emphasize-lines: 2

            >>> from itertools import product
            >>> # product('ABC', 'XYZ') --> AX AY AZ BX BY BZ CX CY CZ
            >>> [ "".join(a) for a in product('ABC', 'XYZ')]
            ['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']

        Only out of date tasks (comparing input and output files) will be run

        Output file names and strings in the extra parameters
        are determined from |tasks_or_file_names|_, i.e. from the output
        of up stream tasks, or a list of file names, after string replacement via
        :ref:`formatter<decorators.formatter>`.

        The replacement strings require an extra level of indirection to refer to
        parsed components:

            #. The first level refers to which *set* of inputs (e.g. **A,B** or **P,Q** or **X,Y**
               in the following example.)
            #. The second level refers to which input file in any particular *set* of inputs.

        For example, ``'{basename[2][0]}'`` is the `basename  <http://docs.python.org/2/library/os.path.html#os.path.basename>`__ for
            * the third set of inputs (**X,Y**) and
            * the first file name string in each **Input** of that set (``"x.1_start"`` and ``"y.1_start"``)

    **Example**:

        Calculates the **@product** of **A,B** and **P,Q** and **X, Y** files

        .. code-block:: python
            :emphasize-lines: 4,17,19,22,25,27,28,29,30,32,34,35,36

            from ruffus import *
            from ruffus.combinatorics import *

            #   Three sets of initial files
            @originate([ 'a.start', 'b.start'])
            def create_initial_files_ab(output_file):
                with open(output_file, "w") as oo: pass

            @originate([ 'p.start', 'q.start'])
            def create_initial_files_pq(output_file):
                with open(output_file, "w") as oo: pass

            @originate([ ['x.1_start', 'x.2_start'],
                         ['y.1_start', 'y.2_start'] ])
            def create_initial_files_xy(output_file):
                with open(output_file, "w") as oo: pass

            #   @product
            @product(   create_initial_files_ab,        # Input
                        formatter("(.start)$"),         # match input file set # 1

                        create_initial_files_pq,        # Input
                        formatter("(.start)$"),         # match input file set # 2

                        create_initial_files_xy,        # Input
                        formatter("(.start)$"),         # match input file set # 3

                        "{path[0][0]}/"                 # Output Replacement string
                        "{basename[0][0]}_vs_"          #
                        "{basename[1][0]}_vs_"          #
                        "{basename[2][0]}.product",     #

                        "{path[0][0]}",                 # Extra parameter: path for 1st set of files, 1st file name

                        ["{basename[0][0]}",            # Extra parameter: basename for 1st set of files, 1st file name
                         "{basename[1][0]}",            #                               2nd
                         "{basename[2][0]}",            #                               3rd
                         ])
            def product_task(input_file, output_parameter, shared_path, basenames):
                print "# basenames      = ", " ".join(basenames)
                print "input_parameter  = ", input_file
                print "output_parameter = ", output_parameter, "\n"


            #
            #       Run
            #
            pipeline_run(verbose=0)


        This results in:

        .. code-block:: pycon
            :emphasize-lines: 2,6,10,14,18,22,26,30

            >>> pipeline_run(verbose=0)

            # basenames      =  a p x
            input_parameter  =  ('a.start', 'p.start', 'x.start')
            output_parameter =  /home/lg/temp/a_vs_p_vs_x.product

            # basenames      =  a p y
            input_parameter  =  ('a.start', 'p.start', 'y.start')
            output_parameter =  /home/lg/temp/a_vs_p_vs_y.product

            # basenames      =  a q x
            input_parameter  =  ('a.start', 'q.start', 'x.start')
            output_parameter =  /home/lg/temp/a_vs_q_vs_x.product

            # basenames      =  a q y
            input_parameter  =  ('a.start', 'q.start', 'y.start')
            output_parameter =  /home/lg/temp/a_vs_q_vs_y.product

            # basenames      =  b p x
            input_parameter  =  ('b.start', 'p.start', 'x.start')
            output_parameter =  /home/lg/temp/b_vs_p_vs_x.product

            # basenames      =  b p y
            input_parameter  =  ('b.start', 'p.start', 'y.start')
            output_parameter =  /home/lg/temp/b_vs_p_vs_y.product

            # basenames      =  b q x
            input_parameter  =  ('b.start', 'q.start', 'x.start')
            output_parameter =  /home/lg/temp/b_vs_q_vs_x.product

            # basenames      =  b q y
            input_parameter  =  ('b.start', 'q.start', 'y.start')
            output_parameter =  /home/lg/temp/b_vs_q_vs_y.product


    **Parameters:**


.. _decorators.product.tasks_or_file_names:

    * *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_.
             E.g.:``"a.*" => "a.1", "a.2"``


.. _decorators.product.matching_formatter:

    * *matching_formatter*
       a :ref:`formatter<decorators.formatter>` indicator object containing optionally
       a  python `regular expression (re) <http://docs.python.org/library/re.html>`_.


.. _decorators.product.output_pattern:

    * *output_pattern*
        Specifies the resulting output file name(s) after string
        substitution


.. _decorators.product.extra_parameters:

    * *extra_parameters*
        Optional extra parameters are passed to the functions after string
        substitution

