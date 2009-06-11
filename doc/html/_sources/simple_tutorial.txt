.. _Simple_Tutorial:

########################
Simple 5 minute Tutorial
########################

***************************************
Overview
***************************************


    The ``ruffus`` module is a lightweight way to add support 
    for running computational pipelines.
    
    Computational pipelines are often conceptually quite simple, especially
    if we breakdown the process into simple stages, or separate **tasks**.
    
    Each **task** is represented by a python function


***************************************
A Simple example
***************************************

**@follows**
************************************

The **@follows(. . .)** python decorator indicates the order in which tasks
should be run::
    
    from ruffus import *
    
    def first_task():
        print "First task"

    @follows(first_task)
    def second_task():
        print "Second task"


the ``@follows`` decorators indicate that the ``first_task`` function precedes ``second_task`` in 
the pipeline.


Running
************************************

    Now we can run the pipeline by::
        
        >>> pipeline_run([second_task])
        
    Which gives::
    
        Task = first_task
        First task
            Job completed
        Task = second_task
        Second task
            Job completed
    
    Because ``second_task`` depends on ``first_task`` , both
    functions will be executed in order.



**@files**
************************************
The **@files(. . .)** decorator provides parameters to a task.
The task function is called in parallel with each set of parameters.

(We describe each task function call as a separate **job**.)



The first two parameters of each job are the input and output files (respectively).
A job will be run only if the file timestamps are out of date.
    
Let us add i/o parameters to the previous python code::
    
    from ruffus import *
    import time
    
    #---------------------------------------------------------------
    #
    #   first task
    #
    task1_param = [
                        [ None, 'a.1'], # 1st job
                        [ None, 'b.1'], # 2nd job
                  ]
                                        
    @files(task1_param)
    def first_task(no_input_file, output_file):
        open(output_file, "w")
    
        # pretend we have worked hard
        time.sleep(1)
    
    
    #---------------------------------------------------------------
    #
    #   second task
    #
    task2_param = [
                        [ 'a.1', "a.2", "    1st_job"], # 1st job
                        [ 'b.1', "b.2", "    2nd_job"], # 2nd job
                  ]
    
    @follows(first_task)
    @files(task2_param)
    def second_task(input_file, output_file, extra_parameter):
        open(output_file, "w")
        print extra_parameter
    
    #---------------------------------------------------------------
    #
    #       Run
    #
    pipeline_run([second_task])
       

Gives::
        
    Task = first_task
        Job = [null -> "a.1"] completed
        Job = [null -> "b.1"] completed
    Task = second_task
        1st_job
        Job = ["a.1" -> "a.2", "1st_job"] completed
        2nd_job
        Job = ["b.1" -> "b.2", "2nd_job"] completed

        

If you ran the same code a second time, nothing would happen because 
``a.2`` is more recent than ``a.1`` and
``b.2`` is more recent than ``b.1`` .
    
However, if you subsequently modified ``a.1`` again::

    >>> open("a.1", "w")
    

You would see the following::

    >>> pipeline_run([second_task])
    Task = second_task
        1st_job
        Job = ["a.1" -> "a.2", "    1st_job"] completed
        Job = ["b.1" -> "b.2", "    2nd_job"] unnecessary: already up to date

    

The 2nd job is up to date and will be skipped.




Displaying
***************

    We can see a flowchart of our fledgling pipeline by executing::
    
        pipeline_printout_graph ( open("flowchart.svg", "w"),
                                 "svg",
                                 [second_task])
    
.. ???

    or in text format with::
    
        pipeline_printout(sys.stdout, [second_task])
    
.. ???



***************************************
More
***************************************

See the :ref:`full tutorial <Tutorial>` for more detail on:

  * :ref:`Ordering tasks <follows>`
  * :ref:`Using files as parameters <files>`
  * :ref:`Generating parameters on the fly <on_the_fly>`
  * :ref:`Multi Processing <multi_processing>`
  * :ref:`Run jobs in parallel <parallel>`
  * :ref:`Handling errors and exceptions <exceptions>`
  * :ref:`Generating parameters using regular expressions <files_re>`
  * :ref:`Manual dependency checking <check_if_uptodate>`
  * :ref:`Signalling the completion of each task <posttask>`
  * :ref:`Logging messages <logging-tasks>`

