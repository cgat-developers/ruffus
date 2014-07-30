.. include:: ../global.inc
#######################
Ruffus Decorators
#######################

.. seealso::
    :ref:`Indicator objects <decorators.indicator_objects>`

.. _decorators:


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
   "**@split** (:ref:`Summary <decorators.split>` / :ref:`Manual <new_manual.split>`)

   - Splits a single input into multiple output
   - Globs in ``output`` can specify an indeterminate number of files.

   ", "
   * :ref:`@split <decorators.split>` ( ``tasks_or_file_names``, ``output_files``, [``extra_parameters``,...] )
           \

   ", ""
   "**@transform** (:ref:`Summary <decorators.transform>` / :ref:`Manual <new_manual.transform>`)

   - Applies the task function to transform input data to output.

   ", "
   * :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`suffix <decorators.transform.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
              \
   * :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`regex <decorators.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \
   * :ref:`@transform <decorators.transform>` ( ``tasks_or_file_names``, :ref:`formatter <decorators.transform.matching_formatter>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""
   "**@merge** (:ref:`Summary <decorators.merge>` / :ref:`Manual <new_manual.merge>`)

   - Merges multiple input files into a single output.

   ", "
   * :ref:`@merge <decorators.merge>` (``tasks_or_file_names``, ``output``, [``extra_parameters``,...] )
           \

          ", ""

.. _decorators.combinatorics:

=============================================
*Combinatorics*
=============================================
.. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@product** (:ref:`Summary <decorators.product>` / :ref:`Manual <new_manual.product>`)

    - Generates the **product**, i.e. all vs all comparisons, between sets of input files.
   ", "
   * :ref:`@product <decorators.product>` ( ``tasks_or_file_names``, :ref:`formatter <decorators.product.matching_formatter>` *([* ``regex_pattern`` *])* ,*[* ``tasks_or_file_names``, :ref:`formatter <decorators.product.matching_formatter>` *([* ``regex_pattern`` *]), ]*, ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""
   "**@permutations** (:ref:`Summary <decorators.permutations>` / :ref:`Manual <new_manual.permutations>`)

    - Generates the **permutations**, between all the elements of a set of **Input**
    - Analogous to the python `itertools.permutations <http://docs.python.org/2/library/itertools.html#itertools.permutations>`__
    - permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC

   ", "
   * :ref:`@permutations <decorators.permutations>` ( ``tasks_or_file_names``, :ref:`formatter <decorators.product.matching_formatter>` *([* ``regex_pattern`` *])*, ``tuple_size``, ``output_pattern``, [``extra_parameters``,...] )
           \
   ", ""
   "**@combinations** (:ref:`Summary <decorators.combinations>` / :ref:`Manual <new_manual.combinations>`)

    - Generates the **permutations**, between all the elements of a set of **Input**
    - Analogous to the python `itertools.combinations <http://docs.python.org/2/library/itertools.html#itertools.permutations>`__
    - combinations('ABCD', 3) --> ABC ABD ACD BCD
    - Generates the **combinations**, between all the elements of a set of **Input**:
      i.e. r-length tuples of *input* elements with no repeated elements (**A A**)
      and where order of the tuples is irrelevant (either **A B** or  **B A**, not both).

   ", "
   * :ref:`@combinations <decorators.permutations>` ( ``tasks_or_file_names``, :ref:`formatter <decorators.product.matching_formatter>` *([* ``regex_pattern`` *])*, ``tuple_size``, ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""
   "**@combinations_with_replacement** (:ref:`Summary <decorators.combinations_with_replacement>` / :ref:`Manual <new_manual.combinations_with_replacement>`)

    - Generates the **permutations**, between all the elements of a set of **Input**
    - Analogous to the python `itertools.permutations <http://docs.python.org/2/library/itertools.html#itertools.permutations>`__
    - combinations('ABCD', 3) --> ABC ABD ACD BCD
    - Generates the **combinations_with_replacement**, between all the elements of a set of **Input**:
      i.e. r-length tuples of *input* elements with no repeated elements (**A A**)
      and where order of the tuples is irrelevant (either **A B** or  **B A**, not both).

   ", "
   * :ref:`@combinations_with_replacement <decorators.permutations>` ( ``tasks_or_file_names``, :ref:`formatter <decorators.product.matching_formatter>` *([* ``regex_pattern`` *])*, ``tuple_size``, ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""

=============================================
*Advanced*
=============================================
 .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@subdivide** (:ref:`Summary <decorators.subdivide>` / :ref:`Manual <new_manual.subdivide>`)
   - Subdivides a set of *Inputs* each further into multiple *Outputs*.
   - The number of files in each *Output* can be set at runtime by the use of globs.
   - **Many to Even More** operator.
   - The use of **split** is a synonym for subdivide is deprecated.

   ", "
   * :ref:`@subdivide <decorators.subdivide>` ( ``tasks_or_file_names``, :ref:`regex <decorators.subdivide.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output_pattern``, [``extra_parameters``,...] )
           \
   * :ref:`@subdivide <decorators.subdivide>` ( ``tasks_or_file_names``, :ref:`formatter <decorators.subdivide.matching_formatter>`\ *(*\ [``regex_pattern``] *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""
   "**@transform** (:ref:`Summary <decorators.transform_ex>` / :ref:`Manual <new_manual.inputs>`)

   - Infers input as well as output from regular expression substitutions
   - Useful for adding additional file dependencies

   ", "
   * :ref:`@transform <decorators.transform_ex>` ( ``tasks_or_file_names``, :ref:`regex <decorators.transform.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output_pattern``, [``extra_parameters``,...] )
           \
   * :ref:`@transform <decorators.transform_ex>` ( ``tasks_or_file_names``, :ref:`formatter <decorators.transform.matching_formatter>`\ *(*\ ``regex_pattern``\ *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""
   "**@collate** (:ref:`Summary <decorators.collate>` / :ref:`Manual <new_manual.collate>`)

   - Groups multiple input files using regular expression matching
   - Input resulting in the same output after substitution will be collated together.

   ", "
   * :ref:`@collate <decorators.collate>` (``tasks_or_file_names``, :ref:`regex <decorators.collate.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \
   * :ref:`@collate <decorators.collate_ex>` (``tasks_or_file_names``, :ref:`regex <decorators.collate_ex.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \
   * :ref:`@collate <decorators.collate>` (``tasks_or_file_names``, :ref:`formatter <decorators.collate.matching_formatter>`\ *(*\ ``formatter_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \
   * :ref:`@collate <decorators.collate_ex>` (``tasks_or_file_names``, :ref:`formatter <decorators.collate_ex.matching_formatter>`\ *(*\ ``formatter_pattern``\ *)*\ , :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ``output_pattern``, [``extra_parameters``,...] )
           \

   ", ""
   "**@follows** (:ref:`Summary <decorators.follows>` / :ref:`Manual <new_manual.follows>`)

   - Indicates task dependency
   - optional :ref:`mkdir <decorators.follows.directory_name>` prerequisite (:ref:`see Manual <new_manual.follows.mkdir>`)

   ", "
   * :ref:`@follows <decorators.follows>` ( ``task1``, ``'task2'`` ))
      \
   * :ref:`@follows <decorators.follows>` ( ``task1``,  :ref:`mkdir <decorators.follows.directory_name>`\ ( ``'my/directory/'`` ))
      \

   ", ""
   "**@posttask** (:ref:`Summary <decorators.posttask>` / :ref:`Manual <new_manual.posttask>`)

   - Calls function after task completes
   - Optional :ref:`touch_file <decorators.posttask.file_name>` indicator (:ref:`Manual <new_manual.posttask.touch_file>`)

   ", "
   * :ref:`@posttask <decorators.posttask>` ( ``signal_task_completion_function`` )
           \
   * :ref:`@posttask <decorators.posttask>` (:ref:`touch_file <decorators.touch_file>`\ ( ``'task1.completed'`` ))
           \

   ", ""
   "**@active_if** (:ref:`Summary <decorators.active_if>` / :ref:`Manual <new_manual.active_if>`)

    - Switches tasks on and off at run time depending on its parameters
    - Evaluated each time :ref:`pipeline_run(...) <pipeline_functions.pipeline_run>`, :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>` or :ref:`pipeline_printout_graph(...) <pipeline_functions.pipeline_printout_graph>` is called.
    - Dormant tasks behave as if they are up to date and have no output.

   ", "
   * :ref:`@active_if <decorators.active_if>` ( ``on_or_off1, [on_or_off2, ...]`` )
           \

   ", ""
   "**@jobs_limit** (:ref:`Summary <decorators.jobs_limit>` / :ref:`Manual <new_manual.jobs_limit>`)

   - Limits the amount of multiprocessing for the specified task
   - Ensures that fewer than N jobs for this task are run in parallel
   - Overrides ``multiprocess`` parameter in :ref:`pipeline_run(...) <pipeline_functions.pipeline_run>`
   ", "
   * :ref:`@jobs_limit <decorators.jobs_limit>` ( ``NUMBER_OF_JOBS_RUNNING_CONCURRENTLY`` )
           \

   ", ""
   "**@mkdir** (:ref:`Summary <decorators.mkdir>` / :ref:`Manual <new_manual.mkdir>`)

   - Generates paths for `os.makedirs  <http://docs.python.org/2/library/os.html#os.makedirs>`__

   ", "
   * :ref:`@mkdir <decorators.mkdir>` ( ``tasks_or_file_names``, :ref:`suffix <decorators.mkdir.suffix_string>`\ *(*\ ``suffix_string``\ *)*\ , ``output_pattern`` )
              \
   * :ref:`@mkdir <decorators.mkdir>` ( ``tasks_or_file_names``, :ref:`regex <decorators.mkdir.matching_regex>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern`` )
           \
   * :ref:`@mkdir <decorators.mkdir>` ( ``tasks_or_file_names``, :ref:`formatter <decorators.mkdir.matching_formatter>`\ *(*\ ``regex_pattern``\ *)*\ , ``output_pattern``)
           \

   ", ""
   "**@graphviz** (:ref:`Summary <decorators.graphviz>` / :ref:`Manual <new_manual.pipeline_printout_graph>`)

   - Customise the graphic for each task in printed flowcharts

   ", "
   * :ref:`@graphviz <decorators.graphviz>` ( ``graphviz_parameter = XXX``, ``[graphviz_parameter2 = YYY ...]``)
           \

   ", ""



=============================================
*Esoteric!*
=============================================
 .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@files** (:ref:`Summary <decorators.files>` / :ref:`Manual <new_manual.deprecated_files>`)

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
   "**@parallel** (:ref:`Summary <decorators.parallel>` / :ref:`Manual <new_manual.deprecated_parallel>`)

   - By default, does not check if jobs are up to date
   - Best used in conjuction with :ref:`@check_if_uptodate <decorators.check_if_uptodate>`

   ", "
   * :ref:`@parallel <decorators.parallel>` ( ``parameter_list`` ) (:ref:`see Manual <new_manual.deprecated_parallel>`)
           \
   * :ref:`@parallel <decorators.parallel>` ( ``parameter_generating_function`` ) (:ref:`see Manual <new_manual.on_the_fly>`)
           \

   ", ""
   "**@check_if_uptodate** (:ref:`Summary <decorators.check_if_uptodate>` / :ref:`Manual <new_manual.check_if_uptodate>`)

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

