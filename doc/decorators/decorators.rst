.. include:: ../global.inc

.. |br| raw:: html

   <br />

#######################
Ruffus Decorators
#######################

.. seealso::
    :ref:`Indicator objects <decorators.indicator_objects>`

.. _decorators:

.. toctree::
    :maxdepth: 1
    :name: core_toc
    :caption: Core
    :hidden:

    originate.rst
    split.rst
    transform.rst
    merge.rst

.. toctree::
    :maxdepth: 1
    :name: advanced_toc
    :caption: Advanced
    :hidden:

    subdivide.rst
    transform_ex.rst
    collate.rst
    graphviz.rst
    mkdir.rst
    jobs_limit.rst
    posttask.rst
    active_if.rst
    follows.rst



.. toctree::
    :maxdepth: 1
    :name: combinatorics_toc
    :caption: Combinatorics
    :hidden:

    product.rst
    permutations.rst
    combinations.rst
    combinations_with_replacement.rst

.. toctree::
    :maxdepth: 1
    :name: esoteric_toc
    :caption: Esoteric
    :hidden:

    files_ex.rst
    check_if_uptodate.rst
    parallel.rst

.. toctree::
    :maxdepth: 1
    :name: deprecated_toc
    :caption: Deprecated
    :hidden:

    files.rst
    files_re.rst


=============================================
*Core*
=============================================
.. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@originate** (:ref:`Summary <decorators.originate>` / :ref:`Manual <new_manual.originate>`)

    - Creates (originates) a set of starting file from scratch  (*ex nihilo*!)
    - Only called to create files which do not exist.
    - Each item in ``output`` is created by a separate job.

   ", "
   * :ref:`@originate <decorators.originate>` ( ``output``, [``extras``,...] )
           \

   ", ""
   "**@split** (:ref:`Summary <decorators.split>` / :ref:`Manual <new_manual.split>`)

   - Splits a single input into multiple output
   - Globs in ``output`` can specify an indeterminate number of files.

   ", "
   * :ref:`@split <decorators.split>` ( ``input``, ``output``, [``extras``,...] )
           \

   ", ""
   "**@transform** (:ref:`Summary <decorators.transform>` / :ref:`Manual <new_manual.transform>`)

   - | Applies the task function to
     | transform input data to output.

   ", "
   * :ref:`@transform <decorators.transform>` ( ``input``, :ref:`suffix <decorators.transform.suffix_string>`\ () , ``output``, [``extras``,...] )
              \
   * :ref:`@transform <decorators.transform>` ( ``input``, :ref:`regex <decorators.transform.matching_regex>`\ () , ``output``, [``extras``,...] )
           \
   * :ref:`@transform <decorators.transform>` ( ``input``, :ref:`formatter <decorators.transform.matching_formatter>`\ () , ``output``, [``extras``,...] )
           \

   ", ""
   "**@merge** (:ref:`Summary <decorators.merge>` / :ref:`Manual <new_manual.merge>`)

   - Merges multiple input files into a single output.

   ", "
   * :ref:`@merge <decorators.merge>` (``input``, ``output``, [``extras``,...] )
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

    - Generates the **product** between sets of input, i.e. all vs all comparisons.
   ", "
   * :ref:`@product <decorators.product>` ( ``input``, :ref:`formatter <decorators.product.matching_formatter>`\ () ,*[* ``input``, :ref:`formatter <decorators.product.matching_formatter>`\ (), ``output``, [``extras``,...] )
           \

   ", ""
   "**@permutations** (:ref:`Summary <decorators.permutations>` / :ref:`Manual <new_manual.permutations>`)

    - Generates the **permutations**, between all elements of a set of **Input**
    - Analogous to the python `itertools.permutations <http://docs.python.org/2/library/itertools.html#itertools.permutations>`__
    - permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC

   ", "
   * :ref:`@permutations <decorators.permutations>` ( ``input``, :ref:`formatter <decorators.product.matching_formatter>`\ (), ``tuple_size``, ``output``, [``extras``,...] )
           \
   ", ""
   "**@combinations** (:ref:`Summary <decorators.combinations>` / :ref:`Manual <new_manual.combinations>`)

    - Generates the **permutations**, between all elements of a set of **Input**
    - Analogous to the python `itertools.combinations <http://docs.python.org/2/library/itertools.html#itertools.permutations>`__
    - combinations('ABCD', 3) --> ABC ABD ACD BCD
    - Generates the **combinations**, between all the elements of a set of **Input**:
      i.e. r-length tuples of *input* elements with no repeated elements (**A A**)
      and where order of the tuples is irrelevant
      (either **A B** or  **B A**, not both).

   ", "
   * :ref:`@combinations <decorators.permutations>` ( ``input``, :ref:`formatter <decorators.product.matching_formatter>`\ (), ``tuple_size``, ``output``, [``extras``,...] )
           \

   ", ""
   "**@combinations_with_replacement** (:ref:`Summary <decorators.combinations_with_replacement>` / :ref:`Manual <new_manual.combinations_with_replacement>`)

    - Generates the **permutations**, between all the elements of a set of **Input**
    - Analogous to the python `itertools.permutations <http://docs.python.org/2/library/itertools.html#itertools.permutations>`__
    - combinations('ABCD', 3) --> ABC ABD ACD BCD
    - Generates the **combinations_with_replacement**,
      between all the elements of a set of **Input**:
      i.e. r-length tuples of *input* elements with no repeated elements (**A A**)
      and where order of the tuples is irrelevant
      (either **A B** or  **B A**, not both).

   ", "
   * :ref:`@combinations_with_replacement <decorators.permutations>` ( ``input``, :ref:`formatter <decorators.product.matching_formatter>`\ (), ``tuple_size``, ``output``, [``extras``,...] )
           \

   ", ""

=============================================
*Advanced*
=============================================
 .. csv-table::
   :header: "Decorator", "Examples"
   :widths: 400, 600,1

   "**@subdivide** (:ref:`Summary <decorators.subdivide>` / :ref:`Manual <new_manual.subdivide>`)

   - Subdivides each *input* into multiple *Outputs*.
   - The number of *output* can be determined at runtime using globs.
   - **Many to Even More** operator.
   - Do not use **split** as a synonym for **subdivide**.

   ", "
   * :ref:`@subdivide <decorators.subdivide>` ( ``input``, :ref:`regex <decorators.subdivide.matching_regex>`\ () , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output``, [``extras``,...] )
           \
   * :ref:`@subdivide <decorators.subdivide>` ( ``input``, :ref:`formatter <decorators.subdivide.matching_formatter>`\ *(*\ [] *)*\ , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output``, [``extras``,...] )
           \

   ", ""
   "**@transform** (:ref:`Summary <decorators.transform_ex>` / :ref:`Manual <new_manual.inputs>`)

   - Generates both **input** & **output** from regular expressions
   - Useful for adding additional file dependencies

   ", "
   * :ref:`@transform <decorators.transform_ex>` ( ``input``, :ref:`regex <decorators.transform.matching_regex>`\ () , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output``, [``extras``,...] )
           \
   * :ref:`@transform <decorators.transform_ex>` ( ``input``, :ref:`formatter <decorators.transform.matching_formatter>`\ () , [ :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ] ``output``, [``extras``,...] )
           \

   ", ""
   "**@collate** (:ref:`Summary <decorators.collate>` / :ref:`Manual <new_manual.collate>`)

   - Groups multiple input using regular expression matching.
   - Multiple input generating identical output are collated together.

   ", "
   * :ref:`@collate <decorators.collate>` (``input``, :ref:`regex <decorators.collate.matching_regex>`\ () , ``output``, [``extras``,...] )
           \
   * :ref:`@collate <decorators.collate_ex>` (``input``, :ref:`regex <decorators.collate_ex.matching_regex>`\ () , :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ``output``, [``extras``,...] )
           \
   * :ref:`@collate <decorators.collate>` (``input``, :ref:`formatter <decorators.collate.matching_formatter>`\ () , ``output``, [``extras``,...] )
           \
   * :ref:`@collate <decorators.collate_ex>` (``input``, :ref:`formatter <decorators.collate_ex.matching_formatter>`\ () , :ref:`inputs <decorators.inputs>` | :ref:`add_inputs <decorators.add_inputs>`\ *(*\ ``input_pattern``\ *)*\ , ``output``, [``extras``,...] )
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
   * :ref:`@posttask <decorators.posttask>` ( ``completion_signal_func`` )
           \
   * :ref:`@posttask <decorators.posttask>` (:ref:`touch_file <decorators.touch_file>`\ ( ``'task1.done'`` ))
           \

   ", ""
   "**@active_if** (:ref:`Summary <decorators.active_if>` / :ref:`Manual <new_manual.active_if>`)

    - Switches tasks on and off at run time
    - Evaluated each time you call
        * :ref:`pipeline_run(...) <pipeline_functions.pipeline_run>`,
        * :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>` or
        * :ref:`pipeline_printout_graph(...) <pipeline_functions.pipeline_printout_graph>`
    - Dormant tasks behave as if they are :
        * up to date and
        * have no output.

   ", "
   * :ref:`@active_if <decorators.active_if>` ( ``on_or_off1``, ``[on_or_off2, ...]`` )
           \

   ", ""
   "**@jobs_limit** (:ref:`Summary <decorators.jobs_limit>` / :ref:`Manual <new_manual.jobs_limit>`)

   - Limits the amount of multiprocessing for the specified task
   - Ensures that fewer than N jobs are run in parallel for this task
   - Overrides ``multiprocess`` parameter in :ref:`pipeline_run(...) <pipeline_functions.pipeline_run>`
   ", "
   * :ref:`@jobs_limit <decorators.jobs_limit>` ( ``NUMBER_OF_JOBS_RUNNING_CONCURRENTLY`` )
           \

   ", ""
   "**@mkdir** (:ref:`Summary <decorators.mkdir>` / :ref:`Manual <new_manual.mkdir>`)

   - Generates paths for `os.makedirs  <http://docs.python.org/2/library/os.html#os.makedirs>`__

   ", "
   * :ref:`@mkdir <decorators.mkdir>` ( ``input``, :ref:`suffix <decorators.mkdir.suffix_string>`\ () , ``output`` )
              \
   * :ref:`@mkdir <decorators.mkdir>` ( ``input``, :ref:`regex <decorators.mkdir.matching_regex>`\ () , ``output`` )
           \
   * :ref:`@mkdir <decorators.mkdir>` ( ``input``, :ref:`formatter <decorators.mkdir.matching_formatter>`\ () , ``output``)
           \

   ", ""
   "**@graphviz** (:ref:`Summary <decorators.graphviz>` / :ref:`Manual <new_manual.pipeline_printout_graph>`)

   - Customise the task graphics in
     flowcharts from :ref:`pipeline_printout_graph(...) <pipeline_functions.pipeline_printout_graph>`

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
   * :ref:`@parallel <decorators.parallel>` ( ``parameter_list`` )
           \
   * :ref:`@parallel <decorators.parallel>` ( ``parameter_generating_function`` )
           \

   ", ""
   "**@check_if_uptodate** (:ref:`Summary <decorators.check_if_uptodate>` / :ref:`Manual <new_manual.check_if_uptodate>`)

   - Custom function to determine if jobs need to be run

   ", "
   * :ref:`@check_if_uptodate <decorators.check_if_uptodate>` ( ``is_task_up_to_date_function`` )
           \

   ", ""
   ".. tip::
     The use of this is discouraged.
       **@files_re** (:ref:`Summary <decorators.files_re>`)

       - I/O file names via regular
         expressions
       - start from lists of file names
         or |glob|_ results
       - skips up-to-date jobs
   ", "
   * :ref:`@files_re <decorators.files_re>` ( ``input``, ``matching_regex``, [``input_pattern``,] ``output``, ``...`` )

   ", ""

