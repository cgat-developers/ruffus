.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.combinatorics.code:

############################################################################################################################################################################################################
|new_manual.combinatorics.chapter_num|: Python Code for :ref:`@combinations<decorators.combinations>`, :ref:`@permutations<decorators.permutations>` and all versus all :ref:`@product<decorators.product>`
############################################################################################################################################################################################################

.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@combinations_with_replacement <decorators.combinations_with_replacement>`
   * :ref:`@combinations <decorators.combinations>`
   * :ref:`@permutations <decorators.permutations>`
   * :ref:`@product <decorators.product>`
   * Back to |new_manual.combinatorics.chapter_num|: :ref:`Preparing directories for output with @combinatorics() <new_manual.combinatorics>`

***************************************************************************
Example code for :ref:`@product <decorators.product>`
***************************************************************************

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

******************************************************************************************************************************************************
Example code for :ref:`@permutations <decorators.permutations>`
******************************************************************************************************************************************************


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


********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
Example code for :ref:`@combinations <decorators.combinations>`
********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

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


********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
Example code for :ref:`@combinations_with_replacement <decorators.combinations_with_replacement>`
********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

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

