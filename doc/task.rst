#####################
ruffus.Task
#####################

.. automodule:: ruffus.task
      :undoc-members:


***************************************
Decorators
***************************************
    Task decorators include:
    
        :ref:`@follows() <task.follows>`      
        
        :ref:`@files() <task.files>`      
        
        :ref:`@files_re() <task.files_re>`      
        
        :ref:`@parallel() <task.parallel>`      
        
        :ref:`@check_if_uptodate() <task.check_if_uptodate>`      

.. _task.follows:

========================
@follows
========================
.. autoclass:: ruffus.task.follows(parent_task1, "module_X.parent_task2")

.. _task.parallel:

========================
@parallel
========================
.. autoclass:: parallel([[job1_params, ...], [job2_params, ...]...])

.. _task.files:

========================
@files
========================
.. autoclass:: files([[input_files, output_files...], ...])

.. _task.files_re:

========================
@files_re
========================
.. autoclass:: files_re(glob/file_list, matching_regex, input_file, output_file, [extra_parameters,...] )

.. _task.check_if_uptodate:

========================
@check_if_uptodate
========================
.. autoclass:: check_if_uptodate(custom_function)

.. _task.posttask:

========================
@posttask
========================
.. autoclass:: posttask(custom_function, [touch_file("a.file")])


.. ???


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
.. autofunction:: file_list_io_param_factory
.. autofunction:: glob_regex_io_param_factory

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





