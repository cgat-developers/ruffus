.. include:: global.inc
#####################
ruffus.Task
#####################

.. automodule:: ruffus.task
      :undoc-members:
      :noindex:

***************************************
Decorators
***************************************
    Basic Task decorators are:
    
        :ref:`@follows() <decorators.follows>`      
        
        and
        
        :ref:`@files() <decorators.files>`      
        
    Task decorators include:
    
        :ref:`@split() <decorators.files>`      

        :ref:`@transform() <decorators.files>`      

        :ref:`@merge() <decorators.files>`      

        :ref:`@posttask() <decorators.posttask>`      

    More advanced users may require:
    
        :ref:`@transform() <decorators.transform_ex>`      
        
        :ref:`@collate() <decorators.collate>`      

        :ref:`@parallel() <decorators.parallel>`      
        
        :ref:`@check_if_uptodate() <decorators.check_if_uptodate>`      

        :ref:`@files_re() <decorators.files_re>`      
        

***************************************
Pipeline functions
***************************************
========================
pipeline_run
========================
.. autofunction:: pipeline_run (target_tasks, forcedtorun_tasks=[], multiprocess=1, logger=stderr_logger, gnu_make_maximal_rebuild_mode=True)

========================
pipeline_printout
========================
.. autofunction:: pipeline_printout

========================
pipeline_printout_graph
========================
.. autofunction:: pipeline_printout_graph


.. ???
    

***************************************
Logging
***************************************
.. autoclass:: t_black_hole_logger
.. autoclass:: t_stderr_logger

.. ???


***************************************
Implementation:
***************************************
=================================
Parameter factories:
=================================
.. autofunction:: merge_param_factory
.. autofunction:: collate_param_factory
.. autofunction:: transform_param_factory
.. autofunction:: files_param_factory
.. autofunction:: args_param_factory
.. autofunction:: split_param_factory

.. ???
    
    
=================================
Wrappers around jobs:
=================================
.. autofunction:: job_wrapper_generic
.. autofunction:: job_wrapper_io_files
.. autofunction:: job_wrapper_mkdir

.. ???
    



=================================
Checking if job is update:
=================================
.. autofunction:: needs_update_check_modify_time
.. autofunction:: needs_update_check_directory_missing

.. ???


***************************************
Exceptions and Errors
***************************************
.. autoclass::task_FilesArgumentsError
.. autoclass::task_FilesreArgumentsError
.. autoclass::JobSignalledBreak
.. autoclass::MissingInputFileError
.. autoclass::PostTaskArgumentError
.. autoclass::error_making_directory
.. autoclass::error_duplicate_task_name
.. autoclass::error_decorator_args
.. autoclass::error_task_name_lookup_failed
.. autoclass::error_task_decorator_takes_no_args
.. autoclass::error_function_is_not_a_task
.. autoclass::error_circular_dependencies
.. autoclass::error_not_a_directory
.. autoclass::error_missing_output
.. autoclass::error_job_signalled_interrupt



.. ???





