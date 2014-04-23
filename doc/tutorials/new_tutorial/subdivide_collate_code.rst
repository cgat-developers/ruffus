.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.subdivide_collate.code:

#############################################################################################################################################################################################################################################################################################################################
|new_manual.subdivide_collate.chapter_num|: Python Code for :ref:`@subdivide <decorators.subdivide>` tasks to run efficiently and regroup with :ref:`@collate <decorators.collate>`
#############################################################################################################################################################################################################################################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`@jobs_limit <decorators.jobs_limit>` syntax
    * :ref:`pipeline_run() <pipeline_functions.pipeline_run>` syntax
    * :ref:`drmaa_wrapper.run_job() <drmaa_wrapper.run_job>` syntax
    * Back to |new_manual.subdivide_collate.chapter_num|: :ref:`:ref:`@subdivide tasks to run efficiently and regroup with @collate <new_manual.subdivide_collate>`

*****************************************************************************************************************************
:ref:`@subdivide <decorators.subdivide>` and regroup with :ref:`@collate <decorators.collate>` example
*****************************************************************************************************************************

    .. code-block:: python
        :emphasize-lines: 17

        from ruffus import *
        import os, random, sys

        # Create files a random number of lines
        @originate(["a.start",
                    "b.start",
                    "c.start"])
        def create_test_files(output_file):
            cnt_lines = random.randint(1,3) * 2
            with open(output_file, "w") as oo:
                for ii in range(cnt_lines):
                    oo.write("data item = %d\n" % ii)
                print "        %s has %d lines" % (output_file, cnt_lines)


        #
        #   subdivide the input files into NNN fragment files of 2 lines each
        #
        @subdivide( create_test_files,
                    formatter(),
                    "{path[0]}/{basename[0]}.*.fragment",
                    "{path[0]}/{basename[0]}")
        def subdivide_files(input_file, output_files, output_file_name_stem):
            #
            #   cleanup any previous results
            #
            for oo in output_files:
                os.unlink(oo)
            #
            #   Output files contain two lines each
            #       (new output files every even line)
            #
            cnt_output_files = 0
            for ii, line in enumerate(open(input_file)):
                if ii % 2 == 0:
                    cnt_output_files += 1
                    output_file_name = "%s.%d.fragment" % (output_file_name_stem, cnt_output_files)
                    output_file = open(output_file_name, "w")
                    print "        Subdivide %s -> %s" % (input_file, output_file_name)
                output_file.write(line)


        #
        #   Analyse each fragment independently
        #
        @transform(subdivide_files, suffix(".fragment"), ".analysed")
        def analyse_fragments(input_file, output_file):
            print "        Analysing %s -> %s" % (input_file, output_file)
            with open(output_file, "w") as oo:
                for line in open(input_file):
                    oo.write("analysed " + line)


        #
        #   Group results using original names
        #
        @collate(   analyse_fragments,

                    # split file name into [abc].NUMBER.analysed
                    formatter("/(?P<NAME>[abc]+)\.\d+\.analysed$"),

                    "{path[0]}/{NAME[0]}.final_result")
        def recombine_analyses(input_file_names, output_file):
            with open(output_file, "w") as oo:
                for input_file in input_file_names:
                    print "        Recombine %s -> %s" % (input_file, output_file)
                    for line in open(input_file):
                        oo.write(line)




        #pipeline_printout(sys.stdout, verbose = 3)


        pipeline_run(verbose = 1)

    Results in

    .. code-block:: pycon

        >>> pipeline_run(verbose = 1)

                a.start has 2 lines
            Job  = [None -> a.start] completed
                b.start has 6 lines
            Job  = [None -> b.start] completed
                c.start has 6 lines
            Job  = [None -> c.start] completed
        Completed Task = create_test_files

                Subdivide a.start -> /home/lg/temp/a.1.fragment
            Job  = [a.start -> a.*.fragment, a] completed
                Subdivide b.start -> /home/lg/temp/b.1.fragment
                Subdivide b.start -> /home/lg/temp/b.2.fragment
                Subdivide b.start -> /home/lg/temp/b.3.fragment
            Job  = [b.start -> b.*.fragment, b] completed
                Subdivide c.start -> /home/lg/temp/c.1.fragment
                Subdivide c.start -> /home/lg/temp/c.2.fragment
                Subdivide c.start -> /home/lg/temp/c.3.fragment
            Job  = [c.start -> c.*.fragment, c] completed
        Completed Task = subdivide_files

                Analysing /home/lg/temp/a.1.fragment -> /home/lg/temp/a.1.analysed
            Job  = [a.1.fragment -> a.1.analysed] completed
                Analysing /home/lg/temp/b.1.fragment -> /home/lg/temp/b.1.analysed
            Job  = [b.1.fragment -> b.1.analysed] completed
                Analysing /home/lg/temp/b.2.fragment -> /home/lg/temp/b.2.analysed
            Job  = [b.2.fragment -> b.2.analysed] completed
                Analysing /home/lg/temp/b.3.fragment -> /home/lg/temp/b.3.analysed
            Job  = [b.3.fragment -> b.3.analysed] completed
                Analysing /home/lg/temp/c.1.fragment -> /home/lg/temp/c.1.analysed
            Job  = [c.1.fragment -> c.1.analysed] completed
                Analysing /home/lg/temp/c.2.fragment -> /home/lg/temp/c.2.analysed
            Job  = [c.2.fragment -> c.2.analysed] completed
                Analysing /home/lg/temp/c.3.fragment -> /home/lg/temp/c.3.analysed
            Job  = [c.3.fragment -> c.3.analysed] completed
        Completed Task = analyse_fragments

                Recombine /home/lg/temp/a.1.analysed -> /home/lg/temp/a.final_result
            Job  = [[a.1.analysed] -> a.final_result] completed
                Recombine /home/lg/temp/b.1.analysed -> /home/lg/temp/b.final_result
                Recombine /home/lg/temp/b.2.analysed -> /home/lg/temp/b.final_result
                Recombine /home/lg/temp/b.3.analysed -> /home/lg/temp/b.final_result
            Job  = [[b.1.analysed, b.2.analysed, b.3.analysed] -> b.final_result] completed
                Recombine /home/lg/temp/c.1.analysed -> /home/lg/temp/c.final_result
                Recombine /home/lg/temp/c.2.analysed -> /home/lg/temp/c.final_result
                Recombine /home/lg/temp/c.3.analysed -> /home/lg/temp/c.final_result
            Job  = [[c.1.analysed, c.2.analysed, c.3.analysed] -> c.final_result] completed
        Completed Task = recombine_analyses

