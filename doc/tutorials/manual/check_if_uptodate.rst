.. _manual.check_if_uptodate:
.. _manual_14th_chapter:

###################################################################################################
**Chapter 14**: `Writing custom functions to decide which jobs are up to date`
###################################################################################################

.. hlist::

    * :ref:`Manual overview <manual>` 
    * :ref:`@check_if_uptodate  syntax in detail<decorators.check_if_uptodate>`

    

.. index:: 
    pair: @check_if_uptodate; Manual
    
******************************************************************************
**@check_if_uptodate** : Manual dependency checking
******************************************************************************
    tasks specified with 
        * :ref:`@files <manual.files>`
        * :ref:`@split <manual.split>` 
        * :ref:`@transform <manual.transform>`
        * :ref:`@merge <manual.merge>`
        * :ref:`@collate <manual.collate>`

    have automatic dependency checking based on file modification times.
    
    Sometimes, you might want to decide have more control over whether to run jobs, especially
    if a task does not rely on or produce files (i.e. with :ref:`@parallel <manual.parallel>`)
    
    You can write your own custom function to decide whether to run a job.
    This takes as many parameters as your task function, and needs to return a
    tuple for whether an update is required, and why (i.e. ``tuple(bool, str)``)
    
    This simple example which creates the file ``"a.1"`` if it does not exist:

        ::
            
            from ruffus import *
            @files(None, "a.1")
            def create_if_necessary(input_file, output_file):
                open(output_file, "w")
                        
            pipeline_run([create_if_necessary])
    

        
    could be rewritten more laboriously as:

        ::
        
            
            from ruffus import *
            import os
            def check_file_exists(input_file, output_file):
                if os.path.exists(output_file):
                    return False, "File already exists"
                return True, "%s is missing" % output_file
            
            @parallel([[None, "a.1"]])
            @check_if_uptodate(check_file_exists)
            def create_if_necessary(input_file, output_file):
                open(output_file, "w")
            
            pipeline_run([create_if_necessary])
            
        

    Both produce the same output:
        ::
        
            Task = create_if_necessary
                Job = [null, "a.1"] completed
        

    
    
.. note::
    
    The function specified by :ref:`@check_if_uptodate <manual.check_if_uptodate>` can be called
    more than once for each job. 

    See the discussion of how **Ruffus** decides which tasks to run in :ref:`Chapter 9 <manual_9th_chapter>`
        

