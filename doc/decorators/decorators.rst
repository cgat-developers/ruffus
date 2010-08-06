.. include:: ../global.inc
#######################
Ruffus Decorators
#######################


.. Note::
    See also:

    .. toctree::
        :maxdepth: 1
    
        indicator_objects.rst
    
.. _decorators:

=============================================
*Basic*
=============================================
.. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1
   
   "**@follows**

   - Indicates task dependency (:ref:`see Manual <manual.follows>`)
   - optional :ref:`mkdir <decorators.follows.directory_name>` prerequisite (:ref:`see Manual <manual.follows.mkdir>`)
   
   ", "
   * :ref:`@follows <decorators.follows>` ( ``task1``, ``'task2'`` ))
      \ 
   * :ref:`@follows <decorators.follows>` ( ``task1``,  :ref:`mkdir <decorators.follows.directory_name>`\ ( ``'my/directory/'`` ))
      \ 
   
   ", ""
   "**@files** (:ref:`see Manual <manual.files>`)
   
   - I/O parameters
   - skips up-to-date jobs
   
   ", "
   * :ref:`@files <decorators.files>`\ ( ``parameter_list`` )
           \ 
   * :ref:`@files <decorators.files>`\ ( ``parameter_generating_function`` )
           \ 
   * :ref:`@files <decorators.files>` ( ``input_file``, ``output_file``, ``other_params``, ... )
           \ 
   
   ", ""

=============================================
*Core*
=============================================
.. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@split** (:ref:`see Manual <manual.split>`)   
   
   - Splits a single input into multiple output
   - Globs in ``output`` can specify an indeterminate number of files.
   
   ", "
   * :ref:`@split <decorators.split>` ( ``tasks_or_file_names``, ``output_files``, [``extra_parameters``,...] )
           \ 

   ", ""
   "**@transform** (:ref:`see Manual <manual.transform>`)   
    
   - Applies the task function to transform input data to output.
    
   ", "
   * :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`suffix <decorators.transform.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
              \ 
   * :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`regex <decorators.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \ 
   
   ", ""
   "**@merge** (:ref:`see Manual <manual.merge>`)   

   - Merges multiple input files into a single output.
   
   ", "
   * :ref:`@merge <decorators.merge>` (``tasks_or_file_names``, ``output``, [``extra_parameters``,...] )
           \

          ", ""
   "**@posttask**

   - Calls function after task completes (:ref:`see Manual <manual.posttask>`)
   - Optional :ref:`touch_file <decorators.posttask.file_name>` indicator (:ref:`see Manual <manual.posttask.touch_file>`)

   ", "
   * :ref:`@posttask <decorators.posttask>` ( ``signal_task_completion_function`` )
           \ 
   * :ref:`@posttask <decorators.posttask>` (:ref:`touch_file <decorators.touch_file>`\ ( ``'task1.completed'`` ))
           \ 
   
   ", ""

=============================================
*Advanced*
=============================================
 .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@collate** (See Manual :ref:`here <manual.collate>` and :ref:`here <manual.collate>`)   

   - Groups multiple input files using regular expression matching
   - Input resulting in the same output after substitution will be collated together.
   
   ", "
   * :ref:`@collate <decorators.collate>` (``tasks_or_file_names``, :ref:`regex <decorators.collate.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \ 
   * :ref:`@collate <decorators.collate_ex>` (``tasks_or_file_names``, :ref:`regex <decorators.collate_ex.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \ 

   ", ""
   "**@transform** (:ref:`Manual <manual.transform_ex>`)   

   - Infers input as well as output from regular expression substitutions
   - Useful for adding additional file dependencies
    
   ", "
   * :ref:`@transform <decorators.transform_ex>` ( ``tasks_or_file_names``, :ref:`suffix <decorators.transform.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output_pattern``, [``extra_parameters``,...] )
           \ 
   * :ref:`@transform <decorators.transform_ex>` ( ``tasks_or_file_names``, :ref:`regex <decorators.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output_pattern``, [``extra_parameters``,...] )
           \ 

   ", ""
   "**@split** (:ref:`see Manual <manual.split_ex>`)   

   - Splits multiple input each further into many more output
   - Globs in ``output`` can specify an indeterminate number of files.
    
   ", "
   * :ref:`@split <decorators.split_ex>` ( ``tasks_or_file_names``, :ref:`regex <decorators.split_ex.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output_pattern``, [``extra_parameters``,...] )
           \ 
      
   ", ""
   "**@jobs_limit** (:ref:`see Manual <manual.jobs_limit>`)   

   - Limits the amount of multiprocessing for the specified task
   - Ensures that fewer than N jobs for this task are run in parallel
   - Overrides ``multiprocess`` parameter in :ref:`pipeline_run(...) <pipeline_functions.pipeline_run>`
   ", "
   * :ref:`@jobs_limit <decorators.jobs_limit>` ( ``NUMBER_OF_JOBS_RUNNING_CONCURRENTLY`` )
           \ 
   
   ", ""



=============================================
*Esoteric!*
=============================================
 .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@parallel**

   - By default, does not check if jobs are up to date
   - Best used in conjuction with :ref:`@check_if_uptodate <decorators.check_if_uptodate>`

   ", "
   * :ref:`@parallel <decorators.parallel>` ( ``parameter_list`` ) (:ref:`see Manual <manual.parallel>`)
           \ 
   * :ref:`@parallel <decorators.parallel>` ( ``parameter_generating_function`` ) (:ref:`see Manual <manual.on_the_fly>`)
           \ 
   
   ", ""
   "**@check_if_uptodate** (:ref:`see Manual <manual.check_if_uptodate>`)

   - Custom function to determine if jobs need to be run
   
   ", "
   * :ref:`@check_if_uptodate <decorators.check_if_uptodate>` ( ``is_task_up_to_date_function`` )
           \ 
   
   ", ""
   ".. tip::
     The use of this overly complicated function is discouraged.
       **@files_re**

       - I/O file names via regular
         expressions
       - start from lists of file names
         or |glob|_ results
       - skips up-to-date jobs
   ", "
   * :ref:`@files_re <decorators.files_re>` ( ``tasks_or_file_names``, ``matching_regex``, [``input_pattern``,] ``output_pattern``, ``...`` )
       ``input_pattern``/``output_pattern`` are regex patterns
       used to create input/output file names from the starting
       list of either glob_str or file names
       
   ", ""

