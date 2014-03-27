.. include:: ../global.inc
#######################
Ruffus Decorators
#######################

.. seealso::
    :ref:`Indicator objects <decorators.indicator_objects>`

.. _decorators:

=============================================
*Basic*
=============================================
.. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@follows** (:ref:`Summary <decorators.follows>` / :ref:`Manual <manual.follows>`)

   - Indicates task dependency
   - optional :ref:`mkdir <decorators.follows.directory_name>` prerequisite (:ref:`see Manual <manual.follows.mkdir>`)

   ", "
   * :ref:`@follows <decorators.follows>` ( ``task1``, ``'task2'`` ))
      \
   * :ref:`@follows <decorators.follows>` ( ``task1``,  :ref:`mkdir <decorators.follows.directory_name>`\ ( ``'my/directory/'`` ))
      \

   ", ""

=============================================
*Core*
=============================================
.. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@originate** (:ref:`Summary <decorators.originate>` / :ref:`Manual <new_manual.originate>`)

    - Creates (originates) a set of starting file without dependencies from scratch  (*ex nihilo*!)
    - Only called to create files which do not exist.
    - Invoked onces (a job created) per item in the ``output_files`` list.

   ", "
   * :ref:`@originate <decorators.originate>` ( ``output_files``, [``extra_parameters``,...] )
           \

   ", ""
   "**@split** (:ref:`Summary <decorators.split>` / :ref:`Manual <manual.split>`)

   - Splits a single input into multiple output
   - Globs in ``output`` can specify an indeterminate number of files.

   ", "
   * :ref:`@split <decorators.split>` ( ``tasks_or_file_names``, ``output_files``, [``extra_parameters``,...] )
           \

   ", ""
   "**@transform** (:ref:`Summary <decorators.transform>` / :ref:`Manual <manual.transform>`)

   - Applies the task function to transform input data to output.

   ", "
   * :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`suffix <decorators.transform.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
              \
   * :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`regex <decorators.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""
   "**@merge** (:ref:`Summary <decorators.merge>` / :ref:`Manual <manual.merge>`)

   - Merges multiple input files into a single output.

   ", "
   * :ref:`@merge <decorators.merge>` (``tasks_or_file_names``, ``output``, [``extra_parameters``,...] )
           \

          ", ""
   "**@posttask** (:ref:`Summary <decorators.posttask>` / :ref:`Manual <manual.posttask>`)

   - Calls function after task completes
   - Optional :ref:`touch_file <decorators.posttask.file_name>` indicator (:ref:`Manual <manual.posttask.touch_file>`)

   ", "
   * :ref:`@posttask <decorators.posttask>` ( ``signal_task_completion_function`` )
           \
   * :ref:`@posttask <decorators.posttask>` (:ref:`touch_file <decorators.touch_file>`\ ( ``'task1.completed'`` ))
           \

   ", ""
   "**@active_if** (:ref:`Summary <decorators.active_if>` / :ref:`Manual <manual.active_if>`)

    - Switches tasks on and off at run time depending on its parameters
    - Evaluated each time :ref:`pipeline_run(...) <pipeline_functions.pipeline_run>`, :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>` or :ref:`pipeline_printout_graph(...) <pipeline_functions.pipeline_printout_graph>` is called.
    - Dormant tasks behave as if they are up to date and have no output.

   ", "
   * :ref:`@active_if <decorators.active_if>` ( ``on_or_off1, [on_or_off2, ...]`` )
           \

   ", ""

=============================================
*Combinatorics*
=============================================
.. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@product** (:ref:`Summary <decorators.product>` / :ref:`Manual <new_manual.product>`)

    - Creates (originates) a set of starting file without dependencies from scratch  (*ex nihilo*!)
    - Only called to create files which do not exist.
    - Invoked onces (a job created) per item in the ``output_files`` list.

   ", "
   * :ref:`@product <decorators.product>` ( ``output_files``, [``extra_parameters``,...] )
           \

   ", ""
   "**@permutations** (:ref:`Summary <decorators.permutations>` / :ref:`Manual <new_manual.permutations>`)

    - Creates (originates) a set of starting file without dependencies from scratch  (*ex nihilo*!)
    - Only called to create files which do not exist.
    - Invoked onces (a job created) per item in the ``output_files`` list.

   ", "
   * :ref:`@permutations <decorators.permutations>` ( ``output_files``, [``extra_parameters``,...] )
           \

   ", ""
   "**@combinations** (:ref:`Summary <decorators.combinations>` / :ref:`Manual <new_manual.combinations>`)

    - Creates (originates) a set of starting file without dependencies from scratch  (*ex nihilo*!)
    - Only called to create files which do not exist.
    - Invoked onces (a job created) per item in the ``output_files`` list.

   ", "
   * :ref:`@combinations <decorators.combinations>` ( ``output_files``, [``extra_parameters``,...] )
           \

   ", ""
   "**@combinations_with_replacement** (:ref:`Summary <decorators.combinations_with_replacement>` / :ref:`Manual <new_manual.combinations_with_replacement>`)

    - Creates (originates) a set of starting file without dependencies from scratch  (*ex nihilo*!)
    - Only called to create files which do not exist.
    - Invoked onces (a job created) per item in the ``output_files`` list.

   ", "
   * :ref:`@combinations_with_replacement <decorators.combinations_with_replacement>` ( ``output_files``, [``extra_parameters``,...] )
           \

   ", ""

=============================================
*Advanced*
=============================================
 .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@collate** (:ref:`Summary <decorators.collate>` / :ref:`Manual <manual.collate>`)

   - Groups multiple input files using regular expression matching
   - Input resulting in the same output after substitution will be collated together.

   ", "
   * :ref:`@collate <decorators.collate>` (``tasks_or_file_names``, :ref:`regex <decorators.collate.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \
   * :ref:`@collate <decorators.collate_ex>` (``tasks_or_file_names``, :ref:`regex <decorators.collate_ex.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""
   "**@transform** (:ref:`Summary <decorators.transform_ex>` / :ref:`Manual <manual.transform_ex>`)

   - Infers input as well as output from regular expression substitutions
   - Useful for adding additional file dependencies

   ", "
   * :ref:`@transform <decorators.transform_ex>` ( ``tasks_or_file_names``, :ref:`suffix <decorators.transform.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output_pattern``, [``extra_parameters``,...] )
           \
   * :ref:`@transform <decorators.transform_ex>` ( ``tasks_or_file_names``, :ref:`regex <decorators.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""
   "**@subdivide** (:ref:`Summary <decorators.subdivide>` / :ref:`Manual <manual.subdivide>`)

   - Subdivides a set of *Inputs* each further into multiple *Outputs*.
   - The number of files in each *Output* can be set at runtime by the use of globs.
   - **Many to Even More** operator.
   - The use of **split** is a synonym for subdivide is deprecated.

   ", "
   * :ref:`@subdivide <decorators.subdivide>` ( ``tasks_or_file_names``, :ref:`regex <decorators.subdivide.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ | :ref:`formatter <decorators.subdivide.matching_formatter>`\ *(*\ [``regex_pattern``] *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""
   "**@jobs_limit** (:ref:`Summary <decorators.jobs_limit>` / :ref:`Manual <manual.jobs_limit>`)

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

   "**@files** (:ref:`Summary <decorators.files>` / :ref:`Manual <manual.files>`)

   - I/O parameters
   - skips up-to-date jobs
   - Should use :ref:`@transform <decorators.transform>` etc instead

   ", "
   * :ref:`@files <decorators.files>`\ ( ``parameter_list`` )
           \
   * :ref:`@files <decorators.files>`\ ( ``parameter_generating_function`` )
           \
   * :ref:`@files <decorators.files>` ( ``input_file``, ``output_file``, ``other_params``, ... )
           \

   ", ""
   "**@parallel** (:ref:`Summary <decorators.parallel>` / :ref:`Manual <manual.parallel>`)

   - By default, does not check if jobs are up to date
   - Best used in conjuction with :ref:`@check_if_uptodate <decorators.check_if_uptodate>`

   ", "
   * :ref:`@parallel <decorators.parallel>` ( ``parameter_list`` ) (:ref:`see Manual <manual.parallel>`)
           \
   * :ref:`@parallel <decorators.parallel>` ( ``parameter_generating_function`` ) (:ref:`see Manual <manual.on_the_fly>`)
           \

   ", ""
   "**@check_if_uptodate** (:ref:`Summary <decorators.check_if_uptodate>` / :ref:`Manual <manual.check_if_uptodate>`)

   - Custom function to determine if jobs need to be run

   ", "
   * :ref:`@check_if_uptodate <decorators.check_if_uptodate>` ( ``is_task_up_to_date_function`` )
           \

   ", ""
   ".. tip::
     The use of this overly complicated function is discouraged.
       **@files_re** (:ref:`Summary <decorators.files_re>`)

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

