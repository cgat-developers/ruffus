########################################
Major Features added to Ruffus 
########################################

********************************************************************
version 1.0
********************************************************************

    Initial Release in Oxford       

********************************************************************
version 1.0.7
********************************************************************
    Added `proxy_logger` module for accessing a shared log across multiple jobs in different processes.

                                                                                   
********************************************************************
version 1.1.4
********************************************************************
    Tasks can get their input by automatically chaining to the output from one or more parent tasks using :ref:`@files_re <manual.files_re>`

********************************************************************
version 2.0
********************************************************************
    * Revamped documentation:
    
        * Rewritten tutorial
        * Comprehensive manual
        * New syntax help
        
    * Major redesign. New decorators include
    
        * :ref:`@split <manual.split>`
        * :ref:`@transform <manual.transform>`
        * :ref:`@merge <manual.merge>`
        * :ref:`@collate <manual.collate>`
    
    * Major redesign. Decorator *inputs* can mix

        * Output from previous tasks
        * `"glob" <http://docs.python.org/library/glob.html>`_ patterns e.g. ``*.txt``
        * Files names
        * Any other data type

********************************************************************
version 2.0.2
********************************************************************

    * Much prettier /useful output from :ref:`pipeline_printout <pipeline_functions.pipeline_printout>`
    * New tutorial / manual

********************************************************************
version 2.0.8
********************************************************************

    * File names can be in unicode
    * File systems with 1 second timestamp granularity no longer cause problems.

********************************************************************
version 2.0.9
********************************************************************

    * Better display of logging output
    * Advanced form of **@split**
      This is an experimental feature.
      
      Hitherto, **@split** only takes 1 set of input (tasks/files/globs) and split these
      into an indeterminate number of output.
      
          This is a one->many operation.
      
      Sometimes it is desirable to take multiple input files, and split each of them further.
      
          This is a many->many (more) operation.
      
      It is possible to hack something together using **@transform** but downstream tasks would not
      aware that each job in **@transform** produces multiple outputs (rather than one input,
      one output per job).
      
      The syntax looks like::

           @split(get_files, regex(r"(.+).original"), r"\1.*.split")
           def split_files(i, o): 
                pass
                
      If ``get_files()`` returned ``A.original``, ``B.original`` and ``C.original``,
      ``split_files()`` might lead to the following operations::
            
            A.original
                    -> A.1.original
                    -> A.2.original
                    -> A.3.original
            B.original
                    -> B.1.original
                    -> B.2.original
            C.original
                    -> C.1.original
                    -> C.2.original
                    -> C.3.original
                    -> C.4.original
                    -> C.5.original
                    
      Note that each input (``A/B/C.original``) can produce a number of output, the exact
      number of which does not have to be pre-determined. 
      This is similar to **@split**
      
      Tasks following ``split_files`` will have ten inputs corresponding to each of the
      output from ``split_files``.
      
      If **@transform** was used instead of **@split**, then tasks following ``split_files`` 
      would only have 3 inputs.

********************************************************************
version 2.0.10
********************************************************************
    * **touch_files_only** option for **pipeline_run**
    
      When the pipeline runs, task functions will not be run. Instead, the output files for
      each job (in each task) will be ``touch``\ -ed if necessary.
      This can be useful for simulating a pipeline run so that all files look as
      if they are up-to-date.

      Caveats:
      
        * This may not work correctly where output files are only determined at runtime, e.g. with **@split**
        * Only the output from pipelined jobs which are currently out-of-date will be ``touch``\ -ed.
          In other words, the pipeline runs *as normal*, the only difference is that the
          output files are ``touch``\ -ed instead of being created by the python task functions
          which would otherwise have been called.

    * Parameter substitution for **inputs(...)**
    
      The **inputs(...)** parameter in **@transform**, **@collate** can now take tasks and globs,
      and these will be expanded appropriately (after regular expression replacement).
      
      For example::
      
          @transform("dir/a.input", regex(r"(.*)\/(.+).input"), 
                        inputs((r"\1/\2.other", r"\1/*.more")), r"elsewhere/\2.output")
          def task1(i, o):
            """
            Some pipeline task
            """
            
      Is equivalent to calling::
            
            task1(("dir/a.other", "dir/1.more", "dir/2.more"), "elsewhere/a.output")
            
      \ 
            
          Here::
            
                r"\1/*.more"
              
          is first converted to::
          
                r"dir/*.more"
                
          which matches::
          
                "dir/1.more" 
                "dir/2.more"
      
                    


########################################
Fixed Bugs
########################################

********************************************************************    
Issue3    
********************************************************************
    
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

********************************************************************    
mkdir
********************************************************************
    
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


