.. _intermediate-pipelines:

################################################
A real-world example
################################################

.. index:: 
    single: Example Programme; 2. Intermediate

****************************************
Python Code
****************************************
The full code is available :ref:`here <code-for-intermediate-pipeline-example>`.

****************************************************
Running simulation studies with genes and GWAS data
****************************************************

=======================================
Background:
=======================================

    
    `Genome-wide association studies <http://en.wikipedia.org/wiki/Genome-wide_association_study>`_
    allow the underlying genetic factors behind common conditions like schizophrenia, obesity
    and heart disease to be identified.
    
    However, it is very import to make sure that the associations are statistically
    sound. This study uses 100 simulated data per gene / GWAS data to test
    the statistical significance.


=======================================
Aim: 
=======================================
    For each gene / GWAS data pair, we need to

    * run a simulation study 100 times against a reference set of (100) simulated data
    * calculate the mean probability for each gene
     
=======================================
Conceptual Flow chart: 
=======================================

    Our pipeline has just 2 steps:

    1. Simulation.
       In pseudo code::

           for n_file in NNN genes:
                for m_file in MMM simulations:
    
                    [n_file.gene,
                     n_file.gwas,
                     m_file.simulation] -> n_file.m_file.simulation_res

    2. Summarise the simulations as a mean.
       In pseudo code::

        for n_file in NNN genes:
            
            n_file.*.simulation_res -> n_file.mean
            
=======================================
Challenges: 
=======================================

    The first step involves an N x M operation.
    
    These are unnecessary tricky to get right in ``gmake`` and like-minded build tools.
    
    In normal computer languages, this is just a pair of for loops::
        
        for n in NNN:
            for m in MMM:
                do n x m
                
    The *ruffus* code is as simple.

=======================================
1. Simulations per gene 
=======================================

    Notice the nested pair of for loops when generating the simulation parameters::
    
        def generate_simulation_params ():

            for sim_file in get_simulation_files():
                for gene, gwas in get_gene_gwas_file_pairs():
                    
                    result_file = "%s.%s.simulation_res" % (gene, sim_file)
                    yield [gene, gwas, sim_file], result_file
                    
    This has been edited for clarity. The full function is available `here <code-for-intermediate-pipeline-example>`_.


    These parameters are passed to the python function calculating the simulations.
    
    We represent this with the following dummy function::
    
        @follows(mkdir(output_dir))
        @files(generate_simulation_params)
        def gwas_simulation(input_files, result_file):
            """
            Dummy calculation of gene gwas vs simulation data
            Normally runs in parallel on a computational cluster       
            """
            (gene_file,
            gwas_file,
            simulation_data_file) = input_files
        
            simulation_res_file = open(result_file, "w")


    
=============================================
2. Mean simulated probability per gene
=============================================
    Now all we have to do is gather all the simulation results, and caculate a
    mean probability per gene.
    
    .. _intermediate-pipelines-combining_files:
    
    Parameters for this "many -> 1" operation can be generated using a simple call to
    the `glob <docs.python.org/library/glob.html>`_ module::

        def generate_statistical_summary_params():
            for gene, gwas in get_gene_gwas_file_pairs():
                result_files     = glob.glob("%s.*.simulation_res" % (gene))
                summary_file     = gene + ".mean"
                    
                yield result_files, summary_file
                
    The function for calculating means would resemble this::
    
        @follows(gwas_simulation)
        @files(generate_statistical_summary_params)
        def statistical_summary (result_files, summary_file):
            summary_file = open(summary_file, "w")

            # ... more code to parse probabilities from results and calculate their mean

    
===================================================
Conclusions
===================================================

What would be spaghetti in makefile format looks just like normal python code with *ruffus*.


