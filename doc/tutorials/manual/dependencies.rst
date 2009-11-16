.. _manual_9th_chapter:

##################################################################################
**Chapter 9**: `Checking dependencies to run tasks in order`
##################################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 

    
.. index:: 
    pair: dependencies; Manual
    
.. _manual.dependencies:


How does **Ruffus** decide how to run your pipeline? 

    * In which order should pipelined functions be called?
    
    * Which parts of the pipeline are up-to-date and do not need to be rerun?


=============================================
Running all out-of-date tasks and dependents
=============================================

    .. image:: ../../images/manual_dependencies_flowchart4.png
    

    By default, *ruffus* will 
    
        * build a flow chart (dependency tree) of pipelined tasks (functions) 
        * start from the most ancestral tasks with the fewest dependencies (``task3`` and ``task1`` in the flowchart above).
        * walk up the tree to find the first incomplete / out-of-date tasks (i.e. ``task6`` and ``task2``. 
          The order by which tasks are asked if they are complete and up-to-date
          is indicated by the red numbers on yellow).
        * start running from there

    All down-stream (dependent) tasks will be re-run anyway, so we don't have to test
          whether they are up-to-date or not.

    .. _checking-multiple-times:
    
    .. note::
    
        This means that **ruffus** *may* ask any task if their jobs are out of date more than once:
    
            * once when deciding which parts of the pipeline have to be run
            * once just before executing the task.
        
    *Ruffus* tries to be clever / efficient, and does the minimal amount of querying.
    
    
.. _manual.dependencies.example:
    
    
=======================================
A simple example
=======================================

-------------------------------------
    Four successive tasks to run:
-------------------------------------    
        .. note::    
            The full code is available :ref:`here <manual.dependencies.code>`.

    
        Suppose we have four successive tasks to run, whose flowchart we can print out
        by running:
        
            ::
            
                pipeline_printout_graph ("flowchart.png", "png", [task4], 
                                            draw_vertically = True)
                
        
        .. image:: ../../images/manual_dependencies_flowchart1.png
        
        We can see that all four tasks need to run reach the target task4.
   
----------------------------------------
    Pipeline tasks are up-to-date:
----------------------------------------


        After the pipeline runs (``python simpler.py -d ""``), all tasks are up to date and the flowchart shows:
        
        .. image:: ../../images/manual_dependencies_flowchart2.png
    
-------------------------------------
    Some tasks out of date:
-------------------------------------

        If we then made task2 and task4 out of date by modifying their *inputs* files:
            ::
        
                open("a.1", "w")
                open("a.3", "w")
                
        
        the flowchart would show:
        
        #. the pipeline only has to rerun from ``task2``.
        #. ``task1`` is complete / up-to-date
        #. ``task3`` will have to be re-run because it follows (depends on) ``task2``.

        .. image:: ../../images/manual_dependencies_flowchart3.png
            
=======================================
Forced Reruns
=======================================
    Even if a pipeline stage appears to be up to date,
    you can always force the pipeline to include from one or more task functions.

    This is particularly useful, for example, if the pipeline data hasn't changed but
    the analysis or computional code has.

        ::
        
            pipeline_run([task4], [task1])
        

        will run all tasks from ``task1`` to ``task4``
        

    Both the "target" and the "forced" lists can include as many tasks as you wish. All dependencies
    are still carried out and out-of-date jobs rerun.
            

=======================================
Esoteric option: Minimal Reruns
=======================================

    In the above example, you could point out that ``task3`` is not out of date. And if we were only interested
    in the immediate dependencies or prerequisites leading up to ``task4``, we might not 
    need task2 to rerun at all, only ``task4``.
    
    This rather dangerous option is useful if you don't want to keep all the intermediate 
    files/results from upstream tasks. The pipeline will only not involve any incomplete
    tasks which precede an up-to-date result. 
    
    This is seldom what you intend, and you should always check that the appropriate stages
    of the pipeline are executed in the flowchart output.
    
    In such cases, we can rerun the pipeline with the following option:

        ::
    
            pipeline_run([task4], gnu_make_maximal_rebuild_mode = False)

    and only ``task4`` will rerun.
    
    
        


