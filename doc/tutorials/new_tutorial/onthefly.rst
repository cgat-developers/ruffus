.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: on_the_fly; Tutorial

.. _new_manual.on_the_fly:

####################################################################################################################################################
|new_manual.on_the_fly.chapter_num|: Esoteric: Generating parameters on the fly with :ref:`@files<decorators.files_on_the_fly>`
####################################################################################################################################################


.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@files on-the-fly syntax in detail <decorators.files_on_the_fly>`

.. note::

    Remember to look at the example code:

    * :ref:`new_manual.on_the_fly.code`


***********************
Overview
***********************

    The different *Ruffus* :ref:`decorators <decorators>` connect up different tasks and
    generate *Output* (file names) from your *Input* in all sorts of different ways.

    However, sometimes, none of them *quite* do exactly what you need. And it becomes
    necessary to generate your own *Input* and *Output* parameters on the fly.

    Although this additional flexibility comes at the cost of a lot of extra inconvenient
    code, you can continue to leverage the rest of *Ruffus* functionality such as
    checking whether files are up to date or not.

.. index::
    pair: @files; Tutorial on-the-fly parameter generation


*********************************************************************
:ref:`@files <decorators.files_on_the_fly>` syntax
*********************************************************************
    To generate parameters on the fly, use the :ref:`@files <decorators.files_on_the_fly>`
    with a :term:`generator` function which yields one list / tuple of parameters per job.

    For example:

    .. code-block:: python
        :emphasize-lines: 3,16

        from ruffus import *

        # generator function
        def generate_parameters_on_the_fly():
            """
            returns one list of parameters per job
            """
            parameters = [
                                ['A.input', 'A.output', (1, 2)], # 1st job
                                ['B.input', 'B.output', (3, 4)], # 2nd job
                                ['C.input', 'C.output', (5, 6)], # 3rd job
                            ]
            for job_parameters in parameters:
                yield job_parameters

        # tell ruffus that parameters should be generated on the fly
        @files(generate_parameters_on_the_fly)
        def pipeline_task(input, output, extra):
            open(output, "w").write(open(input).read())
            sys.stderr.write("%d + %d => %d\n" % (extra[0] , extra[1], extra[0] + extra[1]))

        pipeline_run()


    Produces:

        .. code-block:: pycon

        Task = parallel_task
            1 + 2 = 3
            Job = ["A", 1, 2] completed
            3 + 4 = 7
            Job = ["B", 3, 4] completed
            5 + 6 = 11
            Job = ["C", 5, 6] completed


    .. note::

        Be aware that the parameter generating function may be invoked
        :ref:`more than once<new_manual.dependencies.checking_multiple_times>`:
        * The first time to check if this part of the pipeline is up-to-date.
        * The second time when the pipeline task function is run.

    The resulting custom *inputs*, *outputs* parameters per job are
    treated normally for the purposes of checking to see if jobs are up-to-date and
    need to be re-run.


**********************************************
 A Cartesian Product, all vs all example
**********************************************

    The :ref:`accompanying example<new_manual.on_the_fly.code>` provides a more realistic reason why
    you would want to generate parameters on the fly. It is a fun piece of code, which generates
    N x M combinations from two sets of files as the *inputs* of a pipeline stage.

    The *inputs* / *outputs* filenames are generated as a pair of nested for-loops to produce
    the N (outside loop) x M (inside loop) combinations, with the appropriate parameters
    for each job ``yield``\ed per iteration of the inner loop. The gist of this is:

        .. code-block:: python
            :emphasize-lines: 3

            #_________________________________________________________________________________________
            #
            #   Generator function
            #
            #        N x M jobs
            #_________________________________________________________________________________________
            def generate_simulation_params ():
                """
                Custom function to generate
                file names for gene/gwas simulation study
                """
                for sim_file in get_simulation_files():
                    for (gene, gwas) in get_gene_gwas_file_pairs():
                        result_file = "%s.%s.results" % (gene, sim_file)
                        yield (gene, gwas, sim_file), result_file



            @files(generate_simulation_params)
            def gwas_simulation(input_files, output_file):
                "..."

        If ``get_gene_gwas_file_pairs()`` produces:
            ::

                ['a.sim', 'b.sim', 'c.sim']

        and ``get_gene_gwas_file_pairs()`` produces:
            ::

                [('1.gene', '1.gwas'), ('2.gene', '2.gwas')]

        then we would end up with ``3`` x ``2`` = ``6`` jobs and the following equivalent function calls:

            ::

                gwas_simulation(('1.gene', '1.gwas', 'a.sim'), "1.gene.a.sim.results")
                gwas_simulation(('2.gene', '2.gwas', 'a.sim'), "2.gene.a.sim.results")
                gwas_simulation(('1.gene', '1.gwas', 'b.sim'), "1.gene.b.sim.results")
                gwas_simulation(('2.gene', '2.gwas', 'b.sim'), "2.gene.b.sim.results")
                gwas_simulation(('1.gene', '1.gwas', 'c.sim'), "1.gene.c.sim.results")
                gwas_simulation(('2.gene', '2.gwas', 'c.sim'), "2.gene.c.sim.results")


    The :ref:`accompanying code<new_manual.on_the_fly.code>` looks slightly more complicated because
    of some extra bookkeeping.



    You can compare this approach with the alternative of using :ref:`@product <decorators.product>`:

        .. code-block:: python
            :emphasize-lines: 3

            #_________________________________________________________________________________________
            #
            #        N x M jobs
            #_________________________________________________________________________________________
            @product(   os.path.join(simulation_data_dir, "*.simulation"),
                        formatter(),

                        os.path.join(gene_data_dir, "*.gene"),
                        formatter(),

                        # add gwas as an input: looks like *.gene but with a differnt extension
                        add_inputs("{path[1][0]/{basename[1][0]}.gwas")

                        "{basename[0][0]}.{basename[1][0]}.results")    # output file
            def gwas_simulation(input_files, output_file):
                "..."




