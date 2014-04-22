.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: @subdivide; Tutorial
    pair: @collate; Tutorial

.. _new_manual.subdivide_collate:

############################################################################################################################################################################
|new_manual.subdivide_collate.chapter_num|: :ref:`@subdivide <decorators.subdivide>` tasks to run efficiently and regroup with :ref:`@collate <decorators.collate>`
############################################################################################################################################################################


.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@subdivide <decorators.subdivide>` syntax
   * :ref:`@collate <decorators.collate>` syntax


***********************
Overview
***********************

    In |new_manual.split.chapter_num| and |new_manual.merge.chapter_num|, we saw how a large
    task can be :ref:`@split <new_manual.split>` into small jobs to be analysed efficiently
    in parallel. Ruffus can then :ref:`@merge <new_manual.split>` these back together
    to give a single, unified result.

    This assumes that your pipeline is processing one item at a time. Usually, however, we
    will have, for example, 10 large pieces of data in play, each of which has to be
    subdivided into smaller pieces for analysis before being put back together.

    This is the role of :ref:`@subdivide <decorators.subdivide>` and  :ref:`@subdivide <decorators.collate>`.

    Like :ref:`@split <decorators.split>`,  the number of output files
    :ref:`@subdivide <decorators.subdivide>` produces for *each* **Input** is not predetermined.

    On the other hand, these output files should be named in such a way that they can
    later be grouped back together later using :ref:`@subdivide <decorators.collate>`.

    This will be clearer with some worked examples.


.. _new_manual.subdivide:

*********************************************************************
:ref:`@subdivide <decorators.subdivide>` in parallel
*********************************************************************

    Let us start from 3 files with varying number of lines. We wish to process these two
    lines at a time but we do not know ahead of time how long each file is:

    .. code-block:: python
        :emphasize-lines: 3,5

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


    This produces the following output:

    .. code-block:: pycon
        :emphasize-lines: 8,20,36

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

            [ ...SEE EXAMPLE CODE FOR MORE LINES ...]

        Completed Task = analyse_fragments


    ``a.start`` has two lines and results in a single ``.fragment`` file,
    while there are 3 ``b.*.fragment`` files because it has 6 lines.
    Whatever their origin, all of the different fragment files are treated equally
    in ``analyse_fragments()`` and processed (in parallel) in the same way.



.. _new_manual.collate:

*********************************************************************
Grouping using :ref:`@collate <decorators.collate>`
*********************************************************************

    All that is left in our example is to reassemble the analysed fragments back together into
    3 sets of results corresponding to the original 3 pieces of starting data.

    This is straightforward by eye: the file names all have the same pattern: ``[abc].*.analysed``:

        ::

            a.1.analysed    ->   a.final_result
            b.1.analysed    ->   b.final_result
            b.2.analysed    ->   ..
            b.3.analysed    ->   ..
            c.1.analysed    ->   c.final_result
            c.2.analysed    ->   ..

    :ref:`@collate <decorators.collate>` does something similar:

        #. Specify a string substitution e.g. ``c.??.analysed  -> c.final_result`` and
        #. Ask *ruffus* to group together any **Input** (e.g. ``c.1.analysed``, ``c.2.analysed``)
           that will result in the same **Output** (e.g. ``c.final_result``)


        .. code-block:: python
            :emphasize-lines: 3,5

            #
            #   ``XXX.??.analysed  -> XXX.final_result``
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

        This produces the following output:

        .. code-block:: pycon
            :emphasize-lines: 11

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


    .. warning::

        * **Input** file names are grouped together not in a guaranteed order.

              For example, the fragment files may not be sent to ``recombine_analyses(input_file_names, ...)``
              in alphabetically or any other useful order.

              You may want to sort **Input** before concatenation.

        * All **Input** are grouped together if they have both the same **Output** *and* **Extra**
          parameters. If any string substitution is specified in any of the other **Extra** parameters
          to :ref:`@subdivide <decorators.subdivide>`, they must give the same answers for **Input**
          in the same group.
