.. _Overwiew:

***************
Cheat Sheet
***************

The ``ruffus`` module is a lightweight way to add support 
for running computational pipelines.


Usage
=====

Each stage or **task** in a computational pipeline is represented by a python function
Each python function can be called in parallel to run multiple **jobs**.

1. Annotate functions with python decorators

     +------------------------+-------------------------------------+-----------------------------------------------------------------------------------------------------+
     | Decorator              | Purpose                             |    Example                                                                                          |
     +========================+=====================================+=====================================================================================================+
     |**@follows**            | - Indicate task dependency          | ``@follows(task1, "task2")``                                                                        |
     |                        |                                     |                                                                                                     |
     |                        | - mkdir prerequisite shorthand      | ``@follows(task1, mkdir("my/directory/for/results"))``                                              |
     +------------------------+-------------------------------------+-----------------------------------------------------------------------------------------------------+
     |**@parallel**           | - Parameters for parallel jobs      | ``@parallel(parameter_list)``                                                                       |
     |                        |                                     | ``@parallel(parameter_generating_function)``                                                        |
     +------------------------+-------------------------------------+-----------------------------------------------------------------------------------------------------+
     |**@files**              | - I/O parameters                    | ``@files(parameter_list)``                                                                          |
     |                        |                                     |                                                                                                     |
     |                        | - skips up-to-date jobs             | ``@files(parameter_generating_function)``                                                           |
     |                        |                                     |                                                                                                     |
     |                        |                                     | ``@files(input, output, other_params_for_a_single_job)``                                            |
     +------------------------+-------------------------------------+-----------------------------------------------------------------------------------------------------+
     |**@files_re**           | - I/O file names via regular        | ``@files_re(glob_str, matching_regex, pattern_for_output_filenames)``                               |
     |                        |   expressions                       |                                                                                                     |
     |                        | - start from lists of file names    | ``@files_re(file_names, matching_regex, pattern_for_output_filenames)``                             |
     |                        |   or ``glob`` results               |                                                                                                     |
     |                        | - skips up-to-date jobs             | ``@files_re(glob_str, matching_regex, pattern_for_input_filenames, pattern_for_output_filenames)``  | 
     |                        |                                     |                                                                                                     |
     |                        |                                     | ``@files_re(file_names, matching_regex, pattern_for_input_filenames, pattern_for_output_filenames)``| 
     |                        |                                     |                                                                                                     |
     +------------------------+-------------------------------------+-----------------------------------------------------------------------------------------------------+
     |**@check_if_uptodate**  | - Checks if task needs to be run    | ``@check_if_uptodate(is_task_up_to_date_function)``                                                 |
     +------------------------+-------------------------------------+-----------------------------------------------------------------------------------------------------+
     |**@posttask**           | - Call function after task          | ``@posttask(signal_task_completion_function)``                                                      |
     |                        |                                     |                                                                                                     |
     |                        | - touch file shorthand              | ``@posttask(touch_file("task1.completed")``                                                         |
     +------------------------+-------------------------------------+-----------------------------------------------------------------------------------------------------+

2. Print dependency graph if you necessary

    - For a graphical flowchart in ``jpg``, ``svg``, ``dot``, ``png``, ``ps``, ``gif`` formats::
    
        graph_printout ( open("flowchart.svg", "w"),
                         "svg",
                         list_of_target_tasks)
    
    This requires ``dot`` to be installed
    
    - For a text printout of all jobs ::
    
        pipeline_printout(sys.stdout, list_of_target_tasks)


3. Run the pipeline::

    pipeline_run(list_of_target_tasks, [list_of_tasks_forced_to_rerun, multiprocess = N_PARALLEL_JOBS])


See the :ref:`Tutorial` for a more complete introduction on how to add support
for ruffus.


