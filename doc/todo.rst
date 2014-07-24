.. include:: global.inc

.. _todo:

##########################################
Future Changes to Ruffus
##########################################

    I would appreciated feedback and help on all these issues and where next to take *ruffus*.


    **Future Changes** are features where we more or less know where we are going and how to get there.

    **Planned Improvements** describes features we would like in Ruffus but where the implementation
    or syntax has not yet been (fully) worked out.

    If you have suggestions or contributions, please either write to me ( ruffus_lib at llew.org.uk) or
    send a pull request via the `git site  <https://github.com/bunbun/ruffus>`__.


.. _todo.extending_graph_viz:

********************************************************************************************************
1. Extending graph viz with decorators
********************************************************************************************************

    Contributed by Sean Davis, with suggestions from Jake Biesinger


    In ``task.py``:

    .. code-block:: python

        class graphviz(task_decorator):
            pass


        #_________________________________________________________________________________________

        #   task_graphviz

        #_________________________________________________________________________________________
        def task_graphviz(self, **args):
            self.graphviz_attributes=args


    in print_dependencies.py:

    .. code-block:: python

        for n in all_jobs:
            attributes = dict()
            attributes["shape"]="box3d"
            if(hasattr(n,'graphviz_attributes')):
                for k,v in n.graphviz_attributes.items():
                    attributes[k]=v



    Example:

        .. code-block:: python


            @graphviz(URL='"http://cnn.com"', group='map_reads', foo=bar)
            def myTask(input,output):
                pass

            graphviz_params = {URL='"http://cnn.com"', group='map_reads', foo=bar}
            @graphviz(**graphviz_params)
            def myTask(input,output):
                pass

.. _todo.misfeatures:

********************************************************************************************************
2. (mis) Features
********************************************************************************************************

    * ``Ctrl-C`` should not leave dangling jobs
    * Does killing parallel processes explicitly via kill or qdel cause the job to "fail"
    * What happens with exceptions thrown in the middle of a multiprocessing / multithreading job?
    * Are entries in the queue(s) preventing a clean shutdown?
    * Debug with ``--verbose 10``


.. _todo.inactive_tasks_in_pipeline_printout_graph:

********************************************************************************************************
Todo: pipeline_printout_graph should print inactive tasks
********************************************************************************************************


.. _todo.dynamic_strings:

********************************************************************************************************
Todo: Mark input strings as non-file names, and add support for dynamically returned parameters
********************************************************************************************************

    1. Use indicator object like "ouput_from"
    2. What is a good name?
    3. They will still participate in suffix, formatter and regex replacement

    Bernie Pope suggests that we should generalise this:


    If any object in the input parameters is a (non-list/tuple) class instance, check (getattr) whether it has a "ruffus_params()" function.
    If it does, call it to obtain a list which is substituted in place.
    If there are string nested within, these will take part in Ruffus string substitution.

    "output_from" would be a simple wrapper which returns the internal string via ruffus_params()

    .. code-block:: python

        class output_from (object):
            def __init__(self, str):
                self.str = str
            def ruffus_params(self):
                return [self.str]

    Returning a list should be like wildcards and should not introduce an unnecessary level of indirection for output parameters, i.e. suffix(".txt") or formatter() / "{basename[0]}" should work.

    Check!





.. _todo.extra_parameters:

********************************************************************************************************
Todo: Allow "extra" parameters to be used in output substitution
********************************************************************************************************

    Formatter substitution can refer to the original elements in the input and extra parameters (without converting them to strings either). This refers to the original (nested) data structure.

    This will allow normal python datatypes to be handed down and slipstreamed into a pipeline more easily.

    The syntax would use Ruffus (> version 2.4) formatter:

    .. code-block:: python
        :emphasize-lines: 2,3

        @transform( ..., formatter(), [
                                        "{EXTRAS[0][1][3]}",    # EXTRAS
                                        "[INPUTS[1][2]]"],...)  # INPUTS
        def taskfunc():
            pass

    ``EXTRA`` and ``INPUTS`` indicate that we are referring to the input and extra parameters.

    These are the full (nested) parameters in all their original form. In the case of the input parameters, this obvious depends on the decorator, so

    .. code-block:: python

        @transform(["a.text", [1, "b.text"]], formatter(), "{INPUTS[0][0]}")
        def taskfunc():
            pass

    would give

    ::

        job #1
           input  == "a.text"
           output == "a"

        job #2
           input  == [1, "b.text"]
           output == 1


    The entire string must consist of ``INPUTS`` or ``EXTRAS`` followed by optionally N levels of square brackets. i.e. They must match ``"(INPUTS|EXTRAS)(\[\d+\])+"``

    No string conversion takes place.





.. _todo.pre_post_job:

********************************************************************************************************
Todo: Extra signalling before and after each task and job
********************************************************************************************************

    .. code-block:: python

        @prejob(custom_func)
        @postjob(custom_func)
        def task():
            pass

    ``@prejob`` / ``@postjob`` would be run in the child processes.


.. _todo.new_decorators:

******************************************************************************
Todo: ``@split`` / ``@subdivide`` returns the actual output created
******************************************************************************

    * **overrides** (not replaces) wild cards.
    * Returns a list, each with output and extra paramters.
    * Won't include extraneous files which were not created in the pipeline but which just happened to match the wild card
    * We should have ``ruffus_output_params``, ``ruffus_extra_params`` wrappers for clarity:

      .. code-block:: python

        @split("a.file", "*.txt")
        def split_into_txt_files(input_file, output_files):
            output_files = ["a.txt", "b.txt", "c.txt"]
            for output_file_name in output_files:
                with open(output_file_name, "w") as oo:
                    pass
            return [
                    ruffus_output("a.file"),
                    [ruffus_output(["b.file", "c.file"]), ruffus_extras(13, 14)],
                    ]


    * Consider yielding?

==========================================================================================
Checkpointing
==========================================================================================

    * If checkpoint file is used, the actual files are saved and checked the next time
    * If no files are generated, no files are checked the next time...
    * The output files do not have to match the wildcard though we can output a warning message if that happens...
      This is obviously dangerous because the behavior will change if the pipeline is rerun without using the checkpoint file
    * What happens if the task function changes?

***************************************
Todo: New decorators
***************************************

==============================================================================
Todo: ``@originate``
==============================================================================

    Each (serial) invocation returns lists of output parameters until returns
    None. (Empty list = ``continue``, None = ``break``).



==============================================================================
Todo: ``@recombine``
==============================================================================

    Like ``@collate`` but automatically regroups jobs which were a result of a previous ``@subdivide`` / ``@split`` (even after intervening ``@transform`` )

    This is the only way job trickling can work without stalling the pipeline: We would know
    how many jobs were pending for each ``@recombine`` job and which jobs go together.

****************************************************************************************
Todo: Named parameters in decorators for clarity
****************************************************************************************

.. _todo.bioinformatics_example:

********************************************************************************************************
Todo: Bioinformatics example to end all examples
********************************************************************************************************

    Uses
        * ``@product``
        * ``@subdivide``
        * ``@transform``
        * ``@collate``
        * ``@merge``

****************************************************************************************
Todo: Allow the next task to start before all jobs in the previous task have finished
****************************************************************************************

    Jake (Biesinger) calls this **Job Trickling**!

    * A single long running job no longer will hold up the entire pipeline
    * Calculates dependencies dynamically at the job level.
    * Goal is to have a long running (months) pipeline to which we can keep adding input...
    * We can choose between prioritising completion of the entire pipeline for some jobs
      (depth first) or trying to complete as many tasks as possible (breadth first)

==============================================================================
Converting to per-job rather than per task dependencies
==============================================================================
    Some decorators prevent per job (rather than per task) dependency calculations, and
    will call a pipeline stall until the dependent tasks are completed (the current situation):

        * Some types of jobs unavoidably depend on an entire previous task completing:
             * ``add_inputs()``, ``inputs()``
             * ``@merge``
             * ``@split`` (implicit ``@merge``)
        * ``@split``, ``@originate`` produce variable amount of output at runtime and must be completed before the next task can be run.
             * Should ``yield`` instead of return?
        * ``@collate`` needs to pattern match all the inputs of a previous task
             * Replace ``@collate`` with ``@recombine`` which "remembers" and reverses the results of a previous
               ``@subdivide`` or ``@split``
             * Jobs need unique job_id tag
             * Jobs are assigned (nested) grouping id which accompany them down the
               pipeline after ``@subdivide`` / ``@split`` and are removed after ``@recombine``
             * Should have a count of jobs so we always know *when* an "input slot" is full
        * Funny "single file" mode for ``@transform,`` ``@files`` needs to be
          regularised so it is a syntactic (front end) convenience (oddity!)
          and not plague the inards of ruffus


    Breaking change: to force the entirety of the previous task to complete before the next one, use ``@follows``

==============================================================================
Implementation
==============================================================================

    * "Push" model. Completing jobs "check in" their outputs to "input slots" for all the sucessor jobs.
    * When "input slots" are full for any job, it is put on the dispatch queue to be run.
    * The priority (depth first or breadth first) can be set here.
    * ``pipeline_run`` / ``Pipeline_printout`` create a task dependency tree structure (from decorator dependencies) (a runtime pipeline object)
    * Each task in the pipeline object knows which other tasks wait on it.
    * When output is created by a job, it sends messages to (i.e. function calls) all dependent tasks in the pipeline object with the new output
    * Sets of output such as from ``@split`` and ``@subdivide`` and ``@originate`` have a
      terminating condition and/or a associated count (# of output)
    * Tasks in the pipeline object forward incoming inputs to task input slots (for slots common to all jobs in a
      task: ``@inputs``, ``@add_inputs``) or to slots in new jobs in the pipeline object
    * When all slots are full in each job, this triggers putting the job parameters onto the job submission queue
    * The pipeline object should allow Ruffus to be reentrant?



##########################################
Planned Improvements to Ruffus
##########################################

.. _todo.run_on_cluster:



    * ``@split`` needs to be able to specify at run time the number of
      resulting jobs without using wild cards
    * legacy support for wild cards and file names.


********************************************************************************************************
Planned: Running python code (task functions) transparently on remote cluster nodes
********************************************************************************************************

    Wait until next release.

    Will bump Ruffus to v.3.0 if can run python jobs transparently on a cluster!

    abstract out ``task.run_pooled_job_without_exceptions()`` as a function which can be supplied to ``pipeline_run``

    Common "job" interface:

         *  marshalled arguments
         *  marshalled function
         *  submission timestamp

    Returns
         *  completion timestamp
         *  returned values
         *  exception

    #) Full version use libpythongrid?
       * Christian Widmer <ckwidmer@gmail.com>
       * Cheng Soon Ong <chengsoon.ong@unimelb.edu.au>
       * https://code.google.com/p/pythongrid/source/browse/#git%2Fpythongrid
       * Probably not good to base Ruffus entirely on libpythongrid to minimise dependencies, the use of sophisticated configuration policies etc.
    #) Start with light-weight file-based protocol
       * specify where the scripts should live
       * use drmaa to start jobs
       * have executable ruffus module which knows how to load deserialise (unmarshall) function / parameters from disk. This would be what drmaa starts up, given the marshalled data as an argument
       * time stamp
       * "heart beat" to check that the job is still running
    #) Next step: socket-based protocol
       * use specified master port in ruffus script
       * start remote processes using drmaa
       * child receives marshalled data and the address::port in the ruffus script (head node) to initiate hand shake or die
       * process recycling: run successive jobs on the same remote process for reduced overhead, until exceeds max number of jobs on the same process, min/max time on the same process
       * resubmit if die (Don't do sophisticated stuff like libpythongrid).

.. _todo.job_trickling:



.. _todo.custom_parameters:

************************************
Planned: Custom parameter generator
************************************

    Request on mailing list

         I've often wished that I could use an arbitrary function to process the input filepath instead of just a regex.

        .. code-block:: python

           def f(inputs, outputs, extra_param1, extra_param2):
                # do something to generate parameters
                return new_output_param, new_extra_param1, new_extra_param2

        now f() can be used inside a Ruffus decorator to generate the outputs from inputs, instead of being forced to use a regex for the job.

        Cheers,
        Bernie.

    Leverages built-in Ruffus functionality.
    Don't have to write entire parameter generation from scratch.

    * Gets passed an iterator where you can do a for loop to get input parameters / a flattened list of files
    * Other parameters are forwarded as is
    * The duty of the function is to ``yield`` input, output, extra parameters


    Simple to do but how do we prevent this from being a job-trickling barrier?

    Postpone until we have an initial design for job-trickling: Ruffus v.4 ;-(


.. _todo.gui:

****************************************************************************
Planned: Ruffus GUI interface.
****************************************************************************

    Desktop (PyQT or web-based solution?)  I'd love to see an svg pipeline picture that I could actually interact with


********************************************************************************************************
Planned: Non-decorator / Function interface to Ruffus
********************************************************************************************************


.. _todo.intermediate_files:

********************************************************************************************************
Planned: Remove intermediate files
********************************************************************************************************

    Often large intermediate files are produced in the middle of a pipeline which could be
    removed. However, their absence would cause the pipeline to appear out of date. What is
    the best way to solve this?

    In gmake, all intermediate files which are not marked ``.PRECIOUS`` are deleted.

    We do not want to manually mark intermediate files for several reasons:
        * The syntax would be horrible and clunky
        * The gmake distinction between ``implicit`` and ``explicit`` rules is not one we
          would like to impose on Ruffus
        * Gmake uses statically determined (DAG) dependency trees so it is quite natural and
          easy to prune intermediate paths

    Our preferred solution should impose little to no semantic load on Ruffus, i.e. it should
    not make it more complex / difficult to use. There are several alternatives we are
    considering:

        #) Have an **update** mode in which pipeline_run would ignore missing files and only run tasks with existing, out-of-date files.
        #) Optionally ignore all out-of-date dependencies beyond a specified point in the pipeline
        #) Add a decorator to flag sections of the pipeline where intermediate files can be removed


    Option (1) is rather unnerving because it makes inadvertent errors difficult to detect.

    Option (2) involves relying on the user of a script to remember the corect chain of dependencies in
    often complicated pipelines. It would be advised to keep a flowchart to hand. Again,
    the chances of error are much greater.

    Option (3) springs from the observation by Andreas Heger that parts of a pipeline with
    disposable intermediate files can usually be encapsulated as an autonomous section.
    Within this subpipeline, all is well provided that the outputs of the last task are complete
    and up-to-date with reference to the inputs of the first task. Intermediate files
    could be removed with impunity.

    The suggestion is that these autonomous subpipelines could be marked out using the Ruffus
    decorator syntax::

        #
        #   First task in autonomous subpipeline
        #
        @files("who.isit", "its.me")
        def first_task(*args):
            pass

        #
        #   Several intermediate tasks
        #
        @transform(subpipeline_task1, suffix(".me"), ".her")
        def task2_etc(*args):
           pass

        #
        #   Final task
        #
        @sub_pipeline(subpipeline_task1)
        @transform(subpipeline_task1, suffix(".her"), ".you")
        def final_task(*args):
           pass

    **@sub_pipeline** marks out all tasks between ``first_task`` and ``final_task`` and
    intermediate files such as ``"its.me"``, ``"its.her`` can be deleted. The pipeline will
    only run if ``"its.you"`` is missing or out-of-date compared with ``"who.isit"``.

    Over the next few Ruffus releases we will see if this is a good design, and whether
    better keyword can be found than **@sub_pipeline** (candidates include **@shortcut**
    and **@intermediate**)


.. _todo.retry:

********************************************************************************************************
Planned: @retry_on_error(NUM_OF_RETRIES)
********************************************************************************************************

.. _todo.cleanup:

********************************************************************************************************
Planned: Clean up
********************************************************************************************************

    The plan is to store the files and directories created via
    a standard interface.

    The placeholders for this are a function call ``register_cleanup``.

    Jobs can specify the files they created and which need to be
    deleted by returning a list of file names from the job function.

    So::

        raise Exception = Error

        return False = halt pipeline now

        return string / list of strings = cleanup files/directories later

        return anything else = ignored


    The cleanup file/directory store interface can be connected to
    a text file or a database.

    The cleanup function would look like this::

        pipeline_cleanup(cleanup_log("../cleanup.log"), [instance ="october19th" ])
        pipeline_cleanup(cleanup_msql_db("user", "password", "hash_record_table"))

    The parameters for where and how to store the list of created files could be
    similarly passed to pipeline_run as an extra parameter::

        pipeline_run(cleanup_log("../cleanup.log"), [instance ="october19th" ])
        pipeline_run(cleanup_msql_db("user", "password", "hash_record_table"))

    where `cleanup_log` and `cleanup_msql_db` are classes which have functions for

        #) storing file
        #) retrieving file
        #) clearing entries


    * Files would be deleted in reverse order, and directories after files.
    * By default, only empty directories would be removed.

      But this could be changed with a ``--forced_remove_dir`` option

    * An ``--remove_empty_parent_directories`` option would be
      supported by `os.removedirs(path) <http://docs.python.org/library/os.html#os.removedirs>`_.

