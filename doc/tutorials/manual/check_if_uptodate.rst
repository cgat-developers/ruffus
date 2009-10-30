.. _manual_14th_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run

###################################################################################
Chapter 14: Writing custom functions to decide which jobs are up to date
###################################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 
        * :ref:`@check_if_uptodate<decorators.check_if_uptodate>` syntax in detail

    
.. index:: 
    single: @check_if_uptodate; Manual
    
.. _manual.check_if_uptodate:


***************************************
**@check_if_uptodate**
***************************************

=======================================
Manual dependency checking
=======================================
    tasks specified with 
        * :ref:`@files <manual.files>`
        * :ref:`@split <manual.split>` 
        * :ref:`@transform <manual.transform>`
        * :ref:`@merge <manual.merge>`
        * :ref:`@collate <manual.collate>`

    have automatic dependency checking based on file modification times.
    
    Sometimes, you might want to decide have more control over whether to run jobs, especially
    if a task does not rely on or produce files (i.e. with :ref:`@parallel <parallel>`)
    
    You can write your own custom function to decide whether to run a job.
    This takes as many parameters as your task function, and needs to return True if an
    update is needed.
    
    This simple example which create ``a.1`` if it does not exist::
        
        from ruffus import *
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")
                    
        pipeline_run([create_if_necessary])


        
    .. ???

    Could be rewritten as::
    
        
        from ruffus import *
        import os
        def check_file_exists(input_file, output_file):
            return not os.path.exists(output_file)
        
        @parallel([[None, "a.1"]])
        @check_if_uptodate(check_file_exists)
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")
        
        pipeline_run([create_if_necessary])
        
        
    .. ???

    Both produce the same output::
    
        Task = create_if_necessary
            Job = [null, "a.1"] completed
        
.. ???

    
    
.. note::
    
    The function specified by :ref:`@check_if_uptodate <check_if_uptodate>` can be called
    more than once for each job. 

    See the discussion of how **Ruffus** decides which tasks to run in :ref:`Chapter 9 <manual_9th_chapter>`
        

