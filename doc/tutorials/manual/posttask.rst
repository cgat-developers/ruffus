.. _manual_7th_chapter:

###################################################################
Step 7: Signal the completion of each stage of our pipeline
###################################################################
* :ref:`Up <manual>` 
* :ref:`Prev <manual_6th_chapter>` 
* :ref:`Next <manual_8th_chapter>` 
* :ref:`@posttask<decorators.posttask>` syntax in detail


***************************************
**@posttask**
***************************************

=======================================
Signalling the completion of each task
=======================================
    
    It is often useful to signal the completion of each task by specifying
    one or more function(s) using ``@posttask`` ::
    
        from ruffus import *
        
        def task_finished():
            print "hooray"
            
        @posttask(task_finished)
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")
                    
        pipeline_run([create_if_necessary])

        
.. ???

    
.. note::

    The function(s) provided to ``@posttask`` will be called if the pipeline passes 
    through a task, even if none of its jobs are run because they are up-to-date.
    This happens when a upstream task is out-of-date, and the execution passes through
    this point in the pipeline
    
        
.. ???

.. index:: 
    pair: @posttask; touch_file

.. ???
.. _posttask-touch-file:

=======================================
touch_file
=======================================

    One common way to note the completion of a task is to create some sort of
    "flag" file. Each stage in a traditional ``make`` pipeline would contain a 
    ``touch completed.flag``.
    
    This is such a common use that there is a special shortcut for posttask::
    
        from ruffus import *
        
        @posttask(touch_file("task_completed.flag"))
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")
                    
        pipeline_run([create_if_necessary])
        
.. ???

