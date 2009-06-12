************
Fixed Bugs
************

########    
Issue3    
########
    
===============
Manifestation
===============

    Calling::
    
           graph_printout(
           open("flowchart.svg", "w"),
           "svg",
           [final_task]
         )
 
    dies with::
    
        TypeError: "unbound method outward() ..." on call to "graph_printout"
        
===============
Diagnosis
===============
    
        
    `graph_printout` resolves to `graph.graph_printout (...)`
    
    Should be `task.pipeline_printout_graph (...)`
    
    The error is in the documentation but the graph and print_dependencies modules
    should probably not be exported by default.
    
===============
Resolution
===============

    #) Changed documentation
    #) Removed the following code from ``ruffus/__init__.py``::
    
        from graph import *
        from print_dependencies import *

