#######################
Decorators
#######################

.. seealso::
    :ref:`Indicator objects <indicator_objects>`

        * :ref:`regex <task.regex>`
        * :ref:`suffix <task.suffix>`
        * :ref:`inputs <task.inputs>`
        * :ref:`mkdir <task.mkdir>`
        * :ref:`touch_file <task.touch_file>`


.. _decorators:

=============================================
*Basic*
=============================================
 .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1
   
   "**@follows**

   - Indicates task dependency (:ref:`see tutorial <follows>`)
   - optional :ref:`mkdir <task.follows.directory_name>` prerequisite (:ref:`see tutorial <follow-mkdir>`)
   
   ", "
   * :ref:`@follows <task.follows>` ( ``task1``, ``'task2'`` ))
      \ 
   * :ref:`@follows <task.follows>` ( ``task1``,  :ref:`mkdir <task.follows.directory_name>`\ ( ``'my/directory/'`` ))
      \ 
   
   ", ""
   "**@files** (:ref:`Tutorial <files>`)
   
   - I/O parameters
   - skips up-to-date jobs
   
   ", "
   * :ref:`@files <task.files>`\ ( ``parameter_list`` )
           \ 
   * :ref:`@files <task.files>`\ ( ``parameter_generating_function`` )
           \ 
   * :ref:`@files <task.files>` ( ``input_file``, ``output_file``, ``other_params``, ... )
           \ 
   
   ", ""

=============================================
*Core*
=============================================
 .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@split** (:ref:`Tutorial <tutorial_split>`)   
   
   - Splits a single input into multiple output
   - Globs in ``output`` can specify an indeterminate number of files.
   
   ", "
   * :ref:`@split <task.split>` ( ``tasks_or_file_names``, ``output_files``, [``extra_parameters``,...] )
           \ 

   ", ""
   "**@transform** (:ref:`Tutorial <tutorial_transform>`)   
    
   - Applies the task function to transform input data to output.
    
   ", "
   * :ref:`@transform <task.transform>` ( ``tasks_or_file_names``, :ref:`suffix <task.transform.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
              \ 
   * :ref:`@transform <task.transform>` ( ``tasks_or_file_names``, :ref:`regex <task.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \ 
   
   ", ""
   "**@merge** (:ref:`Tutorial <tutorial_merge>`)   

   - Merges multiple input files into a single output.
   
   ", "
   * :ref:`@merge <task.merge>` (``tasks_or_file_names``, ``output``, [``extra_parameters``,...] )
          ", ""
   "**@posttask**

   - Calls function after task completes (:ref:`see tutorial <posttask>`)
   - Optional :ref:`touch_file <task.posttask.file_name>` indicator (:ref:`see tutorial <posttask-touch-file>`)

   ", "
   * :ref:`@posttask <task.posttask>` ( ``signal_task_completion_function`` )
           \ 
   * :ref:`@posttask <task.posttask>` (:ref:`touch_file <task.touch_file>`\ ( ``'task1.completed'`` ))
           \ 
   
   ", ""

=============================================
*Advanced*
=============================================
 .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@transform** (:ref:`Tutorial <tutorial_transform_ex>`)   

   - Infers input as well as output from regular expression substitutions
   - Useful for adding additional file dependencies
    
   ", "
   * :ref:`@transform <task.transform_ex>` ( ``tasks_or_file_names``, :ref:`suffix <task.transform.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , :ref:`inputs <task.inputs>`\ *(*\ ``input_pattern``\ *)*\ ,  ``output_pattern``, [``extra_parameters``,...] )
           \ 
   * :ref:`@transform <task.transform_ex>` ( ``tasks_or_file_names``, :ref:`regex <task.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , :ref:`inputs <task.inputs>`\ *(*\ ``input_pattern``\ *)*\ ,  ``output_pattern``, [``extra_parameters``,...] )
           \ 
      
   ", ""
   "**@merge** (:ref:`Tutorial <tutorial_merge_ex>`)   

   - Groups multiple input files using regular expression matching
   - Input resulting in the same output after substitution will be collated together.
   
   ", "
   * :ref:`@merge <task.merge_ex>` (``tasks_or_file_names``, :ref:`regex <task.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
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
   - Best used in conjuction with :ref:`@check_if_uptodate <check_if_uptodate>`

   ", "
   * :ref:`@parallel <task.parallel>` ( ``parameter_list`` ) (:ref:`see tutorial <parallel>`)
           \ 
   * :ref:`@parallel <task.parallel>` ( ``parameter_generating_function`` ) (:ref:`see tutorial <on_the_fly>`)
           \ 
   
   ", ""
   "**@check_if_uptodate** (:ref:`Tutorial <check_if_uptodate>`)

   - Custom function to determine if jobs need to be run
   
   ", "
   * :ref:`@check_if_uptodate <task.check_if_uptodate>` ( ``is_task_up_to_date_function`` )
           \ 
   
   ", ""
   ".. tip::
     The use of this overly complicated function is discouraged.
       **@files_re**

       - I/O file names via regular
         expressions
       - start from lists of file names
         or ``glob`` results
       - skips up-to-date jobs
   ", "
   * :ref:`@files_re <files_re>` ( ``tasks_or_file_names``, ``matching_regex``, [``input_pattern``,] ``output_pattern``, ``...`` )
       ``input_pattern``/``output_pattern`` are regex patterns
       used to create input/output file names from the starting
       list of either glob_str or file names
       
   ", ""

