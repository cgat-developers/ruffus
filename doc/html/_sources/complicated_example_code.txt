.. _code-for-complicated-pipeline-example:


#######################################################################
:mod:`complicated_example` -- A more ambitious real-world example
#######################################################################


See :ref:`here <complicated-pipelines>` for an overview and explanations for this code.


.. module:: complicated_example
   :noindex:
   :synopsis: A more ambitious real-world Example.
.. moduleauthor:: Leo Goodstadt <ruffus@llew.org.uk>



The code for this example is in the test subdirectory of the ``ruffus`` module:

    ``ruffus/test/complicated_example.py``

The data is at:

    ``ruffus/test/data_for_complicated_example``

.. program:: complicated_example.py
        :noindex:

.. index:: 
    single: Example Programme Code; 3. Ambitious

****************************
Programme options:
****************************

    .. cmdoption:: --help, -h
        :noindex:
    
        show help message


=================
To specify tasks:
=================

    .. cmdoption:: --target_tasks TARGET_TASK, -t TARGET_TASK
        :noindex:
    
        Target task(s) of pipeline. TARGET_TASK can be
           
        * ``split_unknown_gene_setdef``
        * ``split_per_species_gene_sets``
        * ``all_vs_all_comparisons``
        * ``combine_into_gene_familes``
        * ``split_gene_family_for_evolutionary_analysis``
        * ``evolution_analysis``
        * ``combine_evolution_analysis``
        * ``summarise_evolution_analysis``
        * ``summarise_all``
        
        For example::
    
            complicated_example.py -t evolution_analysis -t summarise_all
        
    .. cmdoption:: --forced_tasks FORCED_TASK, -f FORCED_TASK
        :noindex:
    
        Pipeline task(s) which will be run even if they are up to date.

        See above for a list of pipelined tasks
        
    .. cmdoption:: --jobs N, -j N
        :noindex:
        
        N specifies number of concurrent process running jobs in parallel

=================
To specify paths:
=================

    .. cmdoption:: --data_dir PATH, -d PATH
        :noindex:
        
        Directory with input data.
        
    .. cmdoption:: --working_dir PATH, -d PATH
        :noindex:
    
        Direction in which ruffus will run.


==================================
To print flowchart:
==================================

    .. cmdoption:: --dependency FILE, -d file
        :noindex:
    
        Print a dependency graph of the pipeline that would be
        executed to FILE, but do not execute it.
        
    .. cmdoption:: --dependency_graph_format FORMAT, -F FORMAT
        :noindex:

        Format of dependency graph file. 
    
        Can be::
    
            * 'ps'    
                (PostScript)
                
            * 'svg' 
            
            * 'svgz' 
                (Structured Vector Graphics), 
                
            * 'png' 
            
            * 'gif'
                 (bitmap  graphics)
                 
    .. cmdoption:: --just_print, -n
        :noindex:
    
        Print a description of the jobs that would be
        executed, but do not execute them.

****************************
Code:
****************************
.. literalinclude:: _static/example_scripts/complicated_example.py

