.. _manual_10th_chapter:
.. _manual.on_the_fly:

###################################################################################
**Chapter 10**: `Generating parameters on the fly with` **@files**
###################################################################################
    .. hlist::
    
       * :ref:`Manual overview <manual>` 
       * :ref:`@files on-the-fly syntax in detail <decorators.files_on_the_fly>`

    | Sometimes, it is necessary, or perhaps more convenient, to generate parameters on the fly or
      at runtime. 
    | This  powerful ability to generate the exact parameters you need is 
      sometimes worth the slight increase in complexity.

.. index:: 
    pair: @files; Tutorial on-the-fly parameter generation

    
***********************
**@files**
***********************
    To generate parameters on the fly, pass the decorator **files** with a :term:`generator` function which 
    yields one list / tuple of parameters per job. For example::
    
        from ruffus import *
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
        
        @files(generate_parameters_on_the_fly)
        def pipeline_task(input, output, extra):
            open(output, "w").write(open(input).read())
            sys.stderr.write("%d + %d => %d\n" % (extra[0] , extra[1], extra[0] + extra[1]))
        
        pipeline_run([pipeline_task])
        
        
    .. ???

    Produces::
   
        Task = parallel_task
            1 + 2 = 3
            Job = ["A", 1, 2] completed
            3 + 4 = 7
            Job = ["B", 3, 4] completed
            5 + 6 = 11
            Job = ["C", 5, 6] completed
    
        
    .. note::
    
        Be aware that the parameter generating function may be invoked 
        :ref:`more than once<manual.dependencies.checking_multiple_times>`:
            
            | The first time to check if this part of the pipeline is up-to-date.
            | The second time when the pipeline task function is run.

    The resulting *inputs*, *outputs* and any additional extra parameters per job are
    treated normally for the purposes of checking to see if jobs are up-to-date and
    need to be re-run.
    

**********************************************
 Permutations and Combinations
**********************************************

    The :ref:`accompanying example<manual.on_the_fly_code>` provides a more realistic reason why
    you would want to generate parameters on the fly. It is a fun piece of code, which generates
    N x M combinations from two sets of files as the *inputs* of a pipeline stage.

    The *inputs* / *outputs* filenames are generated as a pair of nested for-loops to produce
    the N (outside loop) x M (inside loop) combinations, with the appropriate parameters
    for each job ``yield``\ed per iteration of the inner loop. The gist of this is:

        ::
        
            #_________________________________________________________________________________________
            #
            #   Step 1:
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


    The :ref:`accompanying code<manual_10th_chapter>` looks slightly more complicated because
    of some extra bookkeeping.
    


