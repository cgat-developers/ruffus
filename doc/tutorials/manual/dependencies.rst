.. _manual_3rd_chapter:

###################################################################
Step 3: Running / displaying the pipeline
###################################################################
* :ref:`Up <manual>` 
* :ref:`Prev <manual_2nd_chapter>` 
* :ref:`Next <manual_4th_chapter>` 
* :ref:`pipeline functions <decorators.pipeline_functions>` in detail

***************************************
Automatic dependency checking
***************************************

=============================================
Running all out-of-date tasks and dependents
=============================================

    By default, *ruffus* will 
    
        * build a flow chart,
        * look upstream (among the antecedents) of the specified target(s),
        * find all the most upstream out-of-date tasks,
        * start running from there.
    
        .. _checking-multiple-times:
    
        This means that *ruffus* *may* ask any task if their jobs are out of date more than once:
    
        * once when deciding whether/how to run the pipeline
        * once when actually executing the task.
        
    *Ruffus* tries to be clever / efficient, and does the minimal amount of querying.
    
    
.. _simple-example:
    
    
=======================================
A simple example
=======================================

-------------------------------------
    Python code
-------------------------------------    
    The full code is available :ref:`here <code-for-simpler-example>`.

-------------------------------------
    Four successive tasks to run:
-------------------------------------    
        The pipeline in ``example_scripts/simpler.py`` has four successive tasks::
        
            python simpler.py -F "jpg" -d "../../images/tutorial_four_stage_pipeline.jpg" -t task4  -K -H
        
        .. ???

        producing the following flowchart
        
        .. image:: ../../images/tutorial_four_stage_pipeline.jpg
        
        

        Flow Chart Key:
        
        .. image:: ../../images/tutorial_pipeline_key.jpg
        

        
        
        We can see that all four tasks need to run reach the target task4.
   
.. ???
    

----------------------------------------
    Pipeline tasks are up-to-date:
----------------------------------------


        After the pipeline runs (``python simpler.py -d ""``), all tasks are up to date and the flowchart shows::
        
            python simpler.py -F "jpg" -d ../../images/tutorial_complete.jpg -t task4 -K -H
        
        
        .. ???

        .. image:: ../../images/tutorial_complete.jpg
    
        
.. ???

    

-------------------------------------
    Some tasks out of date:
-------------------------------------

        If we then made task2 and task4 out of date by modifying their input files::
        
            > touch a.1
            > touch a.3
            
        
        .. ???

        the flowchart would show::
        
            python simpler.py -F "jpg" -d ../../images/tutorial_maximal_mode.jpg -t task4  -K -H
        
        
        .. ???

        .. image:: ../../images/tutorial_maximal_mode.jpg
            
        

        Showing that:
        
            #. the pipeline only has to rerun from ``task2``.
            #. ``task1`` is not out of date
            #. ``task3`` will have to be re-run because it follows (depends on) ``task2``.

.. ???

=======================================
Minimal Reruns
=======================================

    In fact, you could point out that ``task3`` is not out of date. And if we were only interested
    in the immediate dependencies of ``task4``, we might not need task2 to rerun at all, only ``task4``.
    
    .. image:: ../../images/tutorial_minimal_mode.jpg
    
        

    
    In which case, we can rerun the pipeline with a different option::
    
        pipeline_run([task4], gnu_make_maximal_rebuild_mode = False)
        
        
    .. ???

    and only ``task4`` will rerun.
    
    This rather dangerous option is useful if you don't want to keep all the intermediate 
    files/results from upstream tasks. The pipeline code will iterate up the flowchart and 
    stop at the first up to date task. 
        

=======================================
Forced Reruns
=======================================
    In any case, you can always force the pipeline to run from one or more tasks, whether they
    are up to date or not. This is particularly useful, for example, if the pipeline code 
    changes (rather than the data).
    ::
    
        pipeline_run([task4], [task1])
        
        
    .. ???

    will run all tasks from ``task1`` to ``task4``
    
    .. image:: ../../images/tutorial_force_from_task1.jpg
    
        

    Both the "target" and the "forced" lists can include as many tasks as you wish. All dependencies
    are still carried out and out-of-date jobs rerun.

