.. _code-for-intermediate-pipeline-example:


#######################################################################
:mod:`intermediate_example` -- A real-world example
#######################################################################


See :ref:`here <intermediate-pipelines>` for an overview and explanations for this code.


.. module:: intermediate_example
   :synopsis: A real-world Example.
   :noindex:
.. moduleauthor:: Leo Goodstadt <ruffus@llew.org.uk>



The code for this example is in the test subdirectory of the ``ruffus`` module:

    ``ruffus/test/intermediate_example.py``

The data is at:

    ``ruffus/test/data_for_intermediate_example``

.. program:: intermediate_example.py
    :noindex:

.. index:: 
    single: Example Programme Code; 2. Intermediate

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
           
        * ``gwas_simulation``
        * ``statistical_summary``
        
        For example::
    
            intermediate_example.py -t statistical_summary
        
    .. cmdoption:: --forced_tasks FORCED_TASK, -f FORCED_TASK
        :noindex:
    
        Pipeline task(s) which will be run even if they are up to date.

        For example::
    
            intermediate_example.py -t gwas_simulation
        
    .. cmdoption:: --jobs N, -j N
       :noindex:
        
        N specifies number of concurrent process running jobs in parallel

=================
To specify paths:
=================

    .. cmdoption:: --gene_data_dir PATH, -d PATH
        :noindex:
        
        Directory with input data.

    .. cmdoption:: --simulation_data_dir PATH, -s PATH
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
.. literalinclude:: _static/example_scripts/intermediate_example.py


