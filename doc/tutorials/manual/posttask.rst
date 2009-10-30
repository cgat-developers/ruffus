.. _manual_8th_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run

##################################################################
Chapter 8: Signal the completion of each stage of our pipeline
##################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 
        * :ref:`@posttask <decorators.posttask>` syntax in detail

    It is often useful to signal the completion of each task by specifying a specific
    action to be taken or function to be called. This can range from 
    printing out some message, or ``touching`` some sentinel file,
    to emailing the author.This is particular useful if the |task|_ is a recipe apply to an unspecified number
    of parameters in parallel in different |job|_\ s. If the task is never run, or if it
    fails, needless-to-say no task completion action will happen.


    *Ruffus* uses the :ref:`@posttask <decorators.posttask>` decorator for this purpose.
    
.. index:: 
    single: @posttask; Manual
    
.. _manual.posttask:

=================
**@posttask**
=================
This example is from :ref:`step 7 <Simple_Tutorial_7th_step>` of the simple tutorial.

**************************************************************************************
Remember to look at the example code:
**************************************************************************************
* :ref:`Python Code for step 7 <Simple_Tutorial_7th_step_code>` 


=======================================
Signalling the completion of each task
=======================================
    
    We can signal the completion of each task by specifying
    one or more function(s) using ``@posttask`` ::
    
        from ruffus import *
        
        def task_finished():
            print "hooray"
            
        @posttask(task_finished)
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")
                    
        pipeline_run([create_if_necessary])

        
    
.. note::

    The function(s) provided to ``@posttask`` will be called if the pipeline passes 
    through a task, even if none of its jobs are run because they are up-to-date.
    This happens when a upstream task is out-of-date, and the execution passes through
    this point in the pipeline
    
        
.. index:: 
    pair: @posttask; touch_file

.. _manual.posttask.touch_file:

=======================================
**touch_file**
=======================================

    One common way to note the completion of a task is to create some sort of
    "flag" file. Each stage in a traditional ``make`` pipeline would contain a 
    ``touch completed.flag``.
    
    This is so common that **Ruffus** provides a special shorthand::
    
        from ruffus import *
        
        @posttask(touch_file("task_completed.flag"))
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")
                    
        pipeline_run([create_if_necessary])
