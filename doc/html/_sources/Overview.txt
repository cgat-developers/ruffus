.. _Overwiew:

********
Overview
********

The :mod:`task` module is a lightweight way to add support 
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

.. _Background:

Background
==========

The purpose of a pipeline is to determine automatically which parts of a multistage 
process needs to be run and in what order in order to reach an objective ("targets")

Computational pipelines, especially for analysing large scientific datasets are
in widespread use. 
However, even a conceptually simple series of steps can be difficult to set up and
to maintain, perhaps because the right tools are not available.
 
Design
======
The ruffus module has the following design goals:

    * Simplicity. Can be picked up in 10 minutes
    * Elegance
    * Lightweight
    * Unintrusive
    * Flexible/Powerful

Features
============

Automatic support for
 
        * Managing dependencies
        * Parallel jobs
        * Re-starting from arbitrary points, especially after errors
        * Display of the pipeline as a flowchart
        * Reporting

Alternatives
============
Often, tools used to build executables can be used to manage computational pipelines.
These include

        * GNU make
        * scons
        * ant

It is often necessary to learn a specialised (domain-specific) language. 
GNU make syntax, for example, is much critised because of limited support for
abstraction compared with modern programming languages like 
C, Perl, python etc. GNU makefiles can quickly become unmaintainable

Pipeline specifications are usually written in a "declarative" rather than "imperative"
manner. You write a specification that describes the dependencies, and the tool 
figures out how to perform the computations in the correct order. However, because
GNU make and its kin depend entirely on file dependencies, the links between pipeline
stages can be difficult to trace, and nigh impossible to debug when there are problems.

There are also complete workload managements systems such as Condor. 
Various bioinformatics pipelines are also available, including that used by the
leading genome annotation website Ensembl, Pegasys, GPIPE, Taverna, Wildfire, MOWserv,
Triana, Cyrille2 etc. These all are either hardwired to specific databases, and tasks,
or have steep learning curves for both the scientist/developer and the IT system
administrators 


.. seealso::



   **Make like tools**

   GNU Make:
      http://www.gnu.org/software/make/

   SCONS:
      http://www.scons.org/
      
   Apache Ant:
      http://ant.apache.org/
      
\ 
\ 

.. seealso::
   **Bioinformatics pipelines**
   
    Condor:
        http://www.cs.wisc.edu/condor/description.html
    
    Ensembl Analysis pipeline:
        http://www.ncbi.nlm.nih.gov/pubmed/15123589
    
    
    Pegasys:
        http://www.ncbi.nlm.nih.gov/pubmed/15096276
    
    GPIPE:
        http://www.biomedcentral.com/pubmed/15096276
    
    Taverna:
        http://www.ncbi.nlm.nih.gov/pubmed/15201187
    
    Wildfire:
        http://www.biomedcentral.com/pubmed/15788106
    
    MOWserv:
        http://www.biomedcentral.com/pubmed/16257987
    
    Triana:
        http://dx.doi.org/10.1007/s10723-005-9007-3
    
    Cyrille2:
        http://www.biomedcentral.com/1471-2105/9/96
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

