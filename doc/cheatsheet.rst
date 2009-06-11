.. _Overwiew:

***************
Cheat Sheet
***************

The ``ruffus`` module is a lightweight way to add support 
for running computational pipelines.

======
Usage
======

Each stage or **task** in a computational pipeline is represented by a python function
Each python function can be called in parallel to run multiple **jobs**.

1. Annotate functions with python decorators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 40, 60
   
   "**@follows**

   - Indicate task dependency          
   - `mkdir` prerequisite shorthand
   ", "
   :ref:`@follows <follows>` ( ``task1``, ``'task2'`` ))                                
                                                                              
   :ref:`@follows <follows-out-of-order>` ( ``task1``,  :ref:`mkdir <follow-mkdir>`\ ( ``'my/directory/for/results'`` )) 
   "
   "**@parallel**                            
   
   - Parameters for parallel jobs
   ", "   
   :ref:`@parallel <parallel>` ( ``parameter_list`` )                                
                                                                           
   :ref:`@parallel <on_the_fly>` ( ``parameter_generating_function`` ) 
   "
   "**@files**
   
   - I/O parameters         
   - skips up-to-date jobs
   ", "
   :ref:`@files <files>`\ ( ``parameter_list`` )                                

   :ref:`@files <files>`\ ( ``parameter_generating_function`` )                                

   *Simplified syntax for tasks with a single job:*
   
   :ref:`@files <files>` ( ``input_file``, ``output_file``, ``other_params``, ``...`` )                                
   "
   "**@files_re**

   - I/O file names via regular     
     expressions                    
   - start from lists of file names 
     or ``glob`` results            
   - skips up-to-date jobs          
   ", "
   :ref:`@files_re <files_re>` ( ``glob_str``, ``matching_regex``, ``output_pattern``, ``...`` )
                                 
   :ref:`@files_re <files_re>` ( ``file_names``, ``matching_regex``, ``input_pattern``, ``output_pattern``, ``...`` )
                                 
   :ref:`@files_re <files_re>` ( ``glob_str``, ``matching_regex``, ``output_pattern``, ``...`` )
                                 
   :ref:`@files_re <files_re>` ( ``file_names``, ``matching_regex``, ``input_pattern``, ``output_pattern``, ``...`` )                                
                                                                               
   ``input_pattern``/``output_pattern`` are regex patterns                 
   used to create input/output file names from the starting                
   list of either glob_str or file names                                   
   "
   "**@check_if_uptodate**

   - Checks if task needs to be run
   ", "
   :ref:`@check_if_uptodate <check_if_uptodate>` ( ``is_task_up_to_date_function`` )
   "
   "**@posttask**

   - Calls function after task completes
   - *touch_file* shorthand
   ", "
   :ref:`@posttask <posttask>` ( ``signal_task_completion_function`` )

   :ref:`@posttask <posttask>` (:ref:`@touch_file <posttask-touch-file>`\ ( ``'task1.completed'`` ))
   "  


2. Print dependency graph if you necessary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - For a graphical flowchart in ``jpg``, ``svg``, ``dot``, ``png``, ``ps``, ``gif`` formats::
    
        pipeline_printout_graph ( open("flowchart.svg", "w"),
                                 "svg",
                                 list_of_target_tasks)
    
    This requires `dot <http://www.graphviz.org/>`_ to be installed
    
    - For a text printout of all jobs ::
    
        pipeline_printout(sys.stdout, list_of_target_tasks)


3. Run the pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    pipeline_run(list_of_target_tasks, [list_of_tasks_forced_to_rerun, multiprocess = N_PARALLEL_JOBS])


See the :ref:`Tutorial` for a more complete introduction on how to add support
for ruffus.


