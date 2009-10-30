#######################
List of Decorators
#######################

.. seealso::
    :ref:`Indicator objects <indicator_objects>`

        * :ref:`regex <decorators.regex>`
        * :ref:`suffix <decorators.suffix>`
        * :ref:`inputs <decorators.inputs>`
        * :ref:`mkdir <decorators.mkdir>`
        * :ref:`touch_file <decorators.touch_file>`


.. _decorators:

=============================================
*Basic*
=============================================
 .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1
   
   "**@follows**

   - Indicates task dependency (:ref:`see tutorial <manual.follows>`)
   - optional :ref:`mkdir <decorators.follows.directory_name>` prerequisite (:ref:`see tutorial <manual.follows.mkdir>`)
   
   ", "
   * :ref:`@follows <decorators.follows>` ( ``task1``, ``'task2'`` ))
      \ 
   * :ref:`@follows <decorators.follows>` ( ``task1``,  :ref:`mkdir <decorators.follows.directory_name>`\ ( ``'my/directory/'`` ))
      \ 
   
   ", ""
   "**@files** (:ref:`Tutorial <manual.files>`)
   
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

   "**@split** (:ref:`Tutorial <manual.split>`)   
   
   - Splits a single input into multiple output
   - Globs in ``output`` can specify an indeterminate number of files.
   
   ", "
   * :ref:`@split <decorators.split>` ( ``tasks_or_file_names``, ``output_files``, [``extra_parameters``,...] )
           \ 

   ", ""
   "**@transform** (:ref:`Tutorial <manual.transform>`)   
    
   - Applies the task function to transform input data to output.
    
   ", "
   * :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`suffix <decorators.transform.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
              \ 
   * :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`regex <decorators.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \ 
   
   ", ""
   "**@merge** (:ref:`Tutorial <manual.merge>`)   

   - Merges multiple input files into a single output.
   
   ", "
   * :ref:`@merge <decorators.merge>` (``tasks_or_file_names``, ``output``, [``extra_parameters``,...] )
           \
          ", ""
   "**@posttask**

   - Calls function after task completes (:ref:`see tutorial <manual.posttask>`)
   - Optional :ref:`touch_file <decorators.posttask.file_name>` indicator (:ref:`see tutorial <manual.posttask.touch_file>`)

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

   "**@collate** (:ref:`Tutorial <manual.collate>`)   

   - Groups multiple input files using regular expression matching
   - Input resulting in the same output after substitution will be collated together.
   
   ", "
   * :ref:`@collate <decorators.collate>` (``tasks_or_file_names``, :ref:`regex <decorators.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \ 

   ", ""
   "**@transform** (:ref:`Tutorial <manual.transform_ex>`)   

   - Infers input as well as output from regular expression substitutions
   - Useful for adding additional file dependencies
    
   ", "
   * :ref:`@transform <decorators.transform_ex>` ( ``tasks_or_file_names``, :ref:`suffix <decorators.transform.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , :ref:`inputs <decorators.inputs>`\ *(*\ ``input_pattern``\ *)*\ ,  ``output_pattern``, [``extra_parameters``,...] )
           \ 
   * :ref:`@transform <decorators.transform_ex>` ( ``tasks_or_file_names``, :ref:`regex <decorators.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , :ref:`inputs <decorators.inputs>`\ *(*\ ``input_pattern``\ *)*\ ,  ``output_pattern``, [``extra_parameters``,...] )
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
   * :ref:`@parallel <decorators.parallel>` ( ``parameter_list`` ) (:ref:`see tutorial <manual.parallel>`)
           \ 
   * :ref:`@parallel <decorators.parallel>` ( ``parameter_generating_function`` ) (:ref:`see tutorial <manual.on_the_fly>`)
           \ 
   
   ", ""
   "**@check_if_uptodate** (:ref:`Tutorial <manual.check_if_uptodate>`)

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
         or ``glob`` results
       - skips up-to-date jobs
   ", "
   * :ref:`@files_re <files_re>` ( ``tasks_or_file_names``, ``matching_regex``, [``input_pattern``,] ``output_pattern``, ``...`` )
       ``input_pattern``/``output_pattern`` are regex patterns
       used to create input/output file names from the starting
       list of either glob_str or file names
       
   ", ""

