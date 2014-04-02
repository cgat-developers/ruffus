.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.on_the_fly.code:

############################################################################################################################################################################################################
|new_manual.on_the_fly.chapter_num|: Esoteric: Python Code for Generating parameters on the fly with :ref:`@files<decorators.files_on_the_fly>`
############################################################################################################################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`@files on-the-fly syntax in detail <decorators.files_on_the_fly>`
    * Back to |new_manual.on_the_fly.chapter_num|: :ref:`Generating parameters on the fly <new_manual.on_the_fly>`

************************************
Introduction
************************************

    | This script takes N pairs of input file pairs (with the suffices .gene and .gwas)
    | and runs them against M sets of simulation data (with the suffix .simulation)
    | A summary per input file pair is then produced


    In pseudo-code:

        STEP_1:

        ::

            for n_file in NNN_pairs_of_input_files:
                for m_file in MMM_simulation_data:

                    [n_file.gene,
                     n_file.gwas,
                     m_file.simulation] -> n_file.m_file.simulation_res


        STEP_2:

        ::

            for n_file in NNN_pairs_of_input_files:

                n_file.*.simulation_res -> n_file.mean


        | n = CNT_GENE_GWAS_FILES
        | m = CNT_SIMULATION_FILES

************************************
Code
************************************
    ::

        from ruffus import *
        import os

        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

        #   constants

        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        working_dir             = "temp_NxM"
        simulation_data_dir     = os.path.join(working_dir, "simulation")
        gene_data_dir           = os.path.join(working_dir, "gene")
        CNT_GENE_GWAS_FILES     = 2
        CNT_SIMULATION_FILES    = 3



        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

        #   imports

        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        import os, sys
        from itertools import izip
        import glob
        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

        #   Functions


        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

        #_________________________________________________________________________________________
        #
        #   get gene gwas file pairs
        #
        #_________________________________________________________________________________________
        def get_gene_gwas_file_pairs(  ):
            """
            Helper function to get all *.gene, *.gwas from the direction specified
                in --gene_data_dir

            Returns
                file pairs with both .gene and .gwas extensions,
                corresponding roots (no extension) of each file
            """
            gene_files = glob.glob(os.path.join(gene_data_dir, "*.gene"))
            gwas_files = glob.glob(os.path.join(gene_data_dir, "*.gwas"))
            #
            common_roots = set(map(lambda x: os.path.splitext(os.path.split(x)[1])[0], gene_files))
            common_roots &=set(map(lambda x: os.path.splitext(os.path.split(x)[1])[0], gwas_files))
            common_roots = list(common_roots)
            #
            p = os.path; g_dir = gene_data_dir
            file_pairs = [[p.join(g_dir, x + ".gene"), p.join(g_dir, x + ".gwas")] for x in common_roots]
            return file_pairs, common_roots

        #_________________________________________________________________________________________
        #
        #   get simulation files
        #
        #_________________________________________________________________________________________
        def get_simulation_files(  ):
            """
            Helper function to get all *.simulation from the direction specified
                in --simulation_data_dir
                Returns
                    file with .simulation extensions,
                    corresponding roots (no extension) of each file
            """
            simulation_files = glob.glob(os.path.join(simulation_data_dir, "*.simulation"))
            simulation_roots =map(lambda x: os.path.splitext(os.path.split(x)[1])[0], simulation_files)
            return simulation_files, simulation_roots



        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

        #   Main logic


        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888







        #_________________________________________________________________________________________
        #
        #   setup_simulation_data
        #
        #_________________________________________________________________________________________

        #
        # mkdir: makes sure output directories exist before task
        #
        @follows(mkdir(gene_data_dir, simulation_data_dir))
        def setup_simulation_data ():
            """
            create simulation files
            """
            for i in range(CNT_GENE_GWAS_FILES):
                open(os.path.join(gene_data_dir, "%03d.gene" % i), "w")
                open(os.path.join(gene_data_dir, "%03d.gwas" % i), "w")
            #
            # gene files without corresponding gwas and vice versa
            open(os.path.join(gene_data_dir, "orphan1.gene"), "w")
            open(os.path.join(gene_data_dir, "orphan2.gwas"), "w")
            open(os.path.join(gene_data_dir, "orphan3.gwas"), "w")
            #
            for i in range(CNT_SIMULATION_FILES):
                open(os.path.join(simulation_data_dir, "%03d.simulation" % i), "w")




        #_________________________________________________________________________________________
        #
        #   cleanup_simulation_data
        #
        #_________________________________________________________________________________________
        def try_rmdir (d):
            if os.path.exists(d):
                try:
                    os.rmdir(d)
                except OSError:
                    sys.stderr.write("Warning:\t%s is not empty and will not be removed.\n" % d)



        def cleanup_simulation_data ():
            """
            cleanup files
            """
            sys.stderr.write("Cleanup working directory and simulation files.\n")
            #
            #   cleanup gene and gwas files
            #
            for f in glob.glob(os.path.join(gene_data_dir, "*.gene")):
                os.unlink(f)
            for f in glob.glob(os.path.join(gene_data_dir, "*.gwas")):
                os.unlink(f)
            try_rmdir(gene_data_dir)
            #
            #   cleanup simulation
            #
            for f in glob.glob(os.path.join(simulation_data_dir, "*.simulation")):
                os.unlink(f)
            try_rmdir(simulation_data_dir)
            #
            #   cleanup working_dir
            #
            for f in glob.glob(os.path.join(working_dir, "simulation_results", "*.simulation_res")):
                os.unlink(f)
            try_rmdir(os.path.join(working_dir, "simulation_results"))
            #
            for f in glob.glob(os.path.join(working_dir, "*.mean")):
                os.unlink(f)
            try_rmdir(working_dir)


        #_________________________________________________________________________________________
        #
        #   Step 1:
        #
        #        for n_file in NNN_pairs_of_input_files:
        #            for m_file in MMM_simulation_data:
        #
        #                [n_file.gene,
        #                 n_file.gwas,
        #                 m_file.simulation] -> working_dir/n_file.m_file.simulation_res
        #
        #_________________________________________________________________________________________
        def generate_simulation_params ():
            """
            Custom function to generate
            file names for gene/gwas simulation study
            """
            simulation_files, simulation_file_roots    = get_simulation_files()
            gene_gwas_file_pairs, gene_gwas_file_roots =  get_gene_gwas_file_pairs()
            #
            for sim_file, sim_file_root in izip(simulation_files, simulation_file_roots):
                for (gene, gwas), gene_file_root in izip(gene_gwas_file_pairs, gene_gwas_file_roots):
                    #
                    result_file = "%s.%s.simulation_res" % (gene_file_root, sim_file_root)
                    result_file_path = os.path.join(working_dir, "simulation_results", result_file)
                    #
                    yield [gene, gwas, sim_file], result_file_path, gene_file_root, sim_file_root, result_file



        #
        # mkdir: makes sure output directories exist before task
        #
        @follows(mkdir(working_dir, os.path.join(working_dir, "simulation_results")))
        @files(generate_simulation_params)
        def gwas_simulation(input_files, result_file_path, gene_file_root, sim_file_root, result_file):
            """
            Dummy calculation of gene gwas vs simulation data
            Normally runs in parallel on a computational cluster
            """
            (gene_file,
            gwas_file,
            simulation_data_file) = input_files
            #
            simulation_res_file = open(result_file_path, "w")
            simulation_res_file.write("%s + %s -> %s\n" % (gene_file_root, sim_file_root, result_file))


        #_________________________________________________________________________________________
        #
        #   Step 2:
        #
        #       Statistical summary per gene/gwas file pair
        #
        #        for n_file in NNN_pairs_of_input_files:
        #            working_dir/simulation_results/n.*.simulation_res
        #               -> working_dir/n.mean
        #
        #_________________________________________________________________________________________


        @collate(gwas_simulation, regex(r"simulation_results/(\d+).\d+.simulation_res"), r"\1.mean")
        @posttask(lambda : sys.stdout.write("\nOK\n"))
        def statistical_summary (result_files, summary_file):
            """
            Simulate statistical summary
            """
            summary_file = open(summary_file, "w")
            for f in result_files:
                summary_file.write(open(f).read())



        pipeline_run([setup_simulation_data], multiprocess = 5, verbose = 2)
        pipeline_run([statistical_summary], multiprocess = 5, verbose = 2)

        # uncomment to printout flowchar
        #
        # pipeline_printout(sys.stdout, [statistical_summary], verbose=2)
        # graph_printout ("flowchart.jpg", "jpg", [statistical_summary])
        #

        cleanup_simulation_data ()




************************************
Resulting Output
************************************
    ::

        >>> pipeline_run([setup_simulation_data], multiprocess = 5, verbose = 2)
            Make directories [temp_NxM/gene, temp_NxM/simulation] completed
        Completed Task = setup_simulation_data_mkdir_1
            Job completed
        Completed Task = setup_simulation_data


        >>> pipeline_run([statistical_summary], multiprocess = 5, verbose = 2)
            Make directories [temp_NxM, temp_NxM/simulation_results] completed
        Completed Task = gwas_simulation_mkdir_1
            Job = [[temp_NxM/gene/001.gene, temp_NxM/gene/001.gwas, temp_NxM/simulation/000.simulation] -> temp_NxM/simulation_results/001.000.simulation_res, 001, 000, 001.000.simulation_res] completed
            Job = [[temp_NxM/gene/000.gene, temp_NxM/gene/000.gwas, temp_NxM/simulation/000.simulation] -> temp_NxM/simulation_results/000.000.simulation_res, 000, 000, 000.000.simulation_res] completed
            Job = [[temp_NxM/gene/001.gene, temp_NxM/gene/001.gwas, temp_NxM/simulation/001.simulation] -> temp_NxM/simulation_results/001.001.simulation_res, 001, 001, 001.001.simulation_res] completed
            Job = [[temp_NxM/gene/000.gene, temp_NxM/gene/000.gwas, temp_NxM/simulation/001.simulation] -> temp_NxM/simulation_results/000.001.simulation_res, 000, 001, 000.001.simulation_res] completed
            Job = [[temp_NxM/gene/000.gene, temp_NxM/gene/000.gwas, temp_NxM/simulation/002.simulation] -> temp_NxM/simulation_results/000.002.simulation_res, 000, 002, 000.002.simulation_res] completed
            Job = [[temp_NxM/gene/001.gene, temp_NxM/gene/001.gwas, temp_NxM/simulation/002.simulation] -> temp_NxM/simulation_results/001.002.simulation_res, 001, 002, 001.002.simulation_res] completed
        Completed Task = gwas_simulation
            Job = [[temp_NxM/simulation_results/000.000.simulation_res, temp_NxM/simulation_results/000.001.simulation_res, temp_NxM/simulation_results/000.002.simulation_res] -> temp_NxM/000.mean] completed
            Job = [[temp_NxM/simulation_results/001.000.simulation_res, temp_NxM/simulation_results/001.001.simulation_res, temp_NxM/simulation_results/001.002.simulation_res] -> temp_NxM/001.mean] completed
