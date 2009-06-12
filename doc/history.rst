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

########    
mkdir
########
    
===============
Manifestation
===============

    Calling::
    
        from ruffus import *
        
        directories = ['a', 'b']    
        @follows(mkdir(directories))
        def task_which_makes_directories ():
            pass
        
    dies with:
        File "build/bdist.linux-i686/egg/ruffus/task.py", line 1604, in task_mkdir
        TypeError: sequence item 0: expected string, list found

    
        
===============
Diagnosis
===============
    
    mkdir should handle cleanly all three cases::
    
        mkdir(['a', 'b'])
        mkdir('a')
        mkdir('a', 'b')
    
    
===============
Resolution
===============

    #) Changes to task.py
    #) Ignores cases (especially race conditions) when the directory already exists
    #) Added test case test/test_follows_mkdir.py

