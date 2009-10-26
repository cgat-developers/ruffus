.. _code-for-simpler-example:


#######################################################################
:mod:`simpler` -- A simple example
#######################################################################

    See :ref:`here <simple-example>` for a run through of this example.


   
.. moduleauthor:: Leo Goodstadt <ruffus@llew.org.uk>



The code for this example is in the test subdirectory of the ruffus module:

    ``ruffus/test/simpler.py``


.. program:: simpler.py

.. index:: 
    single: Example Programme Code; 1. Simple

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
           
        * ``task1``
        * ``task2``
        * ``task3``
        * ``task4``
        
        For example::
    
            complicated_example.py -t task1 -t task4
        
    .. cmdoption:: --forced_tasks FORCED_TASK, -f FORCED_TASK
        :noindex:
    
        Pipeline task(s) which will be run even if they are up to date.
        
        See above for a list of pipelined tasks
        
    .. cmdoption:: --jobs N, -j N
        :noindex:
        
        N specifies number of concurrent process running jobs in parallel

    .. cmdoption:: --minimal_rebuild_mode, -M
        :noindex:
    
        Rebuild a minimum of tasks necessary for the target. 
        Ignore upstream out of date tasks if intervening tasks are up to date.
        

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

    .. cmdoption:: --no_key_legend_in_graph, -K
        :noindex:
    
        Do not print out legend and key for dependency graph.
        
    .. cmdoption:: --draw_graph_horizontally, -H
        :noindex:
    
        Draw horizontal (left to right) dependency graph.
        


****************************
Code:
****************************
.. literalinclude:: _static/example_scripts/simpler.py

