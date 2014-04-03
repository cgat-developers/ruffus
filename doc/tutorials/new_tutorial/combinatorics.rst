.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: combinatorics; Tutorial

.. _new_manual.combinatorics:

##################################################################################################################################################################################################################################################
|new_manual.combinatorics.chapter_num|: :ref:`@combinations<decorators.combinations>`, :ref:`@permutations<decorators.permutations>` and all versus all :ref:`@product<decorators.product>`
##################################################################################################################################################################################################################################################

.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@combinations_with_replacement <decorators.combinations_with_replacement>`
   * :ref:`@combinations <decorators.combinations>`
   * :ref:`@permutations <decorators.permutations>`
   * :ref:`@product <decorators.product>`
   * :ref:`formatter() <decorators.formatter>`

.. note::

    Remember to look at the example code:

        * :ref:`new_manual.combinatorics.code`


**************************************
Overview
**************************************

    A surprising number of computational problems involve some sort of all versus all calculations.
    Previously, this would have required all the parameters to be supplied using a custom function
    on the fly with :ref:`@files<decorators.files_on_the_fly>`.

    From version 2.4, *Ruffus* supports  :ref:`@combinations_with_replacement <decorators.combinations_with_replacement>`,
    :ref:`@combinations <decorators.combinations>`, :ref:`@permutations <decorators.permutations>`,
    :ref:`@product <decorators.product>`.

    These provide as far as possible all the functionality of the four combinatorics iterators
    from the standard python `itertools  <http://docs.python.org/2/library/itertools.html>`__
    functions of the same name.

***************************************************************************
Generating output with :ref:`formatter()<decorators.formatter>`
***************************************************************************

    String replacement always takes place via :ref:`formatter()<decorators.formatter>`. Unfortunately,
    the other *Ruffus* workhorses of  :ref:`regex()<decorators.regex>` and  :ref:`suffix()<decorators.suffix>`
    do not have sufficient syntactic flexibility.

    Each combinatorics decorator deals with multiple sets of inputs whether this might be:

        * a self-self comparison (such as :ref:`@combinations_with_replacement <decorators.combinations_with_replacement>`,
          :ref:`@combinations <decorators.combinations>`, :ref:`@permutations <decorators.permutations>`) or,
        * a self-other comparison (:ref:`@product <decorators.product>`)

    The replacement strings thus require an extra level of indirection to refer to
    parsed components.

        #. The first level refers to which *set* of inputs.
        #. The second level refers to which input file in any particular *set* of inputs.


    For example, if the *inputs* are  **[A1,A2],[B1,B2],[C1,C2] vs [P1,P2],[Q1,Q2],[R1,R2] vs [X1,X2],[Y1,Y2],[Z1,Z2]**,
    then ``'{basename[2][0]}'`` is the `basename  <http://docs.python.org/2/library/os.path.html#os.path.basename>`__ for

        * the third set of inputs (**X,Y,Z**) and
        * the first file name string in each **Input** of that set (**X1, Y1, Z1**)



.. _new_manual.product:

***************************************************************************
All vs all comparisons with :ref:`@product <decorators.product>`
***************************************************************************

    :ref:`@product <decorators.product>` generates the Cartesian **product** between sets of input files,
    i.e. all vs all comparisons.

    The effect is analogous to a nested for loop.

    :ref:`@product <decorators.product>` can be useful, for example, in bioinformatics for finding
    the corresponding genes (orthologues) for a set of proteins in multiple species.

    .. code-block:: pycon
        :emphasize-lines: 2

        >>> from itertools import product
        >>> # product('ABC', 'XYZ') --> AX AY AZ BX BY BZ CX CY CZ
        >>> [ "".join(a) for a in product('ABC', 'XYZ')]
        ['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']



    This example Calculates the **@product** of **A,B** and **P,Q** and **X,Y** files

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


.. _new_manual.permutations:

******************************************************************************************************************************************************
Permute all k-tuple orderings of inputs without repeats using :ref:`@permutations <decorators.permutations>`
******************************************************************************************************************************************************

    Generates the **permutations** for all the elements of a set of **Input** (e.g. **A B C D**),
        * r-length tuples of *input* elements
        * excluding repeated elements (**A A**)
        * and order of the tuples is significant (both **A B** and  **B A**).

    .. code-block:: pycon
        :emphasize-lines: 2

        >>> from itertools import permutations
        >>> # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
        >>> [ "".join(a) for a in permutations("ABCD", 2)]
        ['AB', 'AC', 'AD', 'BA', 'BC', 'BD', 'CA', 'CB', 'CD', 'DA', 'DB', 'DC']

    This following example calculates the **@permutations** of **A,B,C,D** files

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

.. _new_manual.combinations:

********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
Select unordered k-tuples within inputs excluding repeated elements using :ref:`@combinations <decorators.combinations>`
********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

    Generates the **combinations** for all the elements of a set of **Input** (e.g. **A B C D**),
        * r-length tuples of *input* elements
        * without repeated elements (**A A**)
        * where order of the tuples is irrelevant (either **A B** or  **B A**, not both).

    :ref:`@combinations <decorators.combinations>` can be useful, for example, in calculating a transition probability matrix
    for a set of states. The diagonals are meaningless "self-self" transitions which are excluded.

    .. code-block:: pycon
        :emphasize-lines: 2

        >>> from itertools import combinations
        >>> # combinations('ABCD', 3) --> ABC ABD ACD BCD
        >>> [ "".join(a) for a in combinations("ABCD", 3)]
        ['ABC', 'ABD', 'ACD', 'BCD']

    This example calculates the **@combinations** of **A,B,C,D** files

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

            #   @combinations
            @combinations(create_initial_files_ABCD,      # Input
                          formatter(),                    # match input files

                          # tuple of 3 at a time
                          3,

                          # Output Replacement string
                          "{path[0][0]}/"
                          "{basename[0][1]}_vs_"
                          "{basename[1][1]}_vs_"
                          "{basename[2][1]}.combinations",

                          # Extra parameter: path for 1st set of files, 1st file name
                          "{path[0][0]}",

                          # Extra parameter
                          ["{basename[0][0]}",  # basename for 1st set of files, 1st file name
                           "{basename[1][0]}",  #              2nd
                           "{basename[2][0]}",  #              3rd
                           ])
            def combinations_task(input_file, output_parameter, shared_path, basenames):
                print " - ".join(basenames)


            #
            #       Run
            #
            pipeline_run(verbose=0)


    This results in:

        .. code-block:: pycon

            >>> pipeline_run(verbose=0)
            A - B - C
            A - B - D
            A - C - D
            B - C - D

.. _new_manual.combinations_with_replacement:

********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
Select unordered k-tuples within inputs *including* repeated elements with :ref:`@combinations_with_replacement <decorators.combinations_with_replacement>`
********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

    Generates the **combinations_with_replacement** for all the elements of a set of **Input** (e.g. **A B C D**),
        * r-length tuples of *input* elements
        * including repeated elements (**A A**)
        * where order of the tuples is irrelevant (either **A B** or  **B A**, not both).


    :ref:`@combinations_with_replacement <decorators.combinations_with_replacement>` can be useful,
    for example, in bioinformatics for finding evolutionary relationships between genetic elements such as proteins
    and genes. Self-self comparisons can be used a baseline for scaling similarity scores.

    .. code-block:: pycon
        :emphasize-lines: 2

        >>> from itertools import combinations_with_replacement
        >>> # combinations_with_replacement('ABCD', 2) --> AA AB AC AD BB BC BD CC CD DD
        >>> [ "".join(a) for a in combinations_with_replacement('ABCD', 2)]
        ['AA', 'AB', 'AC', 'AD', 'BB', 'BC', 'BD', 'CC', 'CD', 'DD']

    This example calculates the **@combinations_with_replacement** of **A,B,C,D** files

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

