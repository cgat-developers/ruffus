.. include:: global.inc

.. _todo:

##########################################
Planned improvements
##########################################

    These are the future enhancements I would like to see in Ruffus:

    * Simpler syntax
        * Extremely pared down syntax where strings are interpreted as commands (like gmake)
          but with full Ruffus support / string interpolation etc.
        * More powerful non-decorator OOP syntax
        * More customisation points for your own syntax / database use

    * Better support for Computational clusters / larger scale pipelines
        * Running jobs out of sequence
        * Long running pipeline where input can be added later
        * Restarting failed jobs robustly
        * Finding out why jobs fail
        * Does Ruffus scale to thousands of parallel jobs. What are the bottlenecks?

    * Better displays of progress
        * Query which tasks / jobs are being run
        * GUI displays

    * Dynamic control during pipeline progress
        * Turn tasks on and off
        * Pause pipelines
        * Pause jobs
        * Change priorities

    * Better handling of data
        * Can we read and write from databases instead of files?
        * Can we cleanup files but preserve history?

===============================================
In up coming release:
===============================================

****************************************************************************************
Todo: Mention python3.2 multiprocessing import and proxies bug in FAQ
****************************************************************************************

****************************************************************************************
Todo: Refactor Error Messages
****************************************************************************************

    When are messages indented?
    When are messages wrapped / extended across new lines

****************************************************************************************
Todo: More documentation for formatter()
****************************************************************************************

    Needs to discuss how to escape. Also in FAQ?

****************************************************************************************
Todo: OOP syntax taking strings
****************************************************************************************

****************************************************************************************
Todo: Extra unit tests
****************************************************************************************
    #. ``@product`` ``set_input`` should take (``input``, ``input2``...)
    #. bioinformatics pipelines (complicated example)
    #. ``output_from`` and Pipeline names

****************************************************************************************
Todo: document ``output_from()``
****************************************************************************************

****************************************************************************************
Todo: document new syntax
****************************************************************************************

****************************************************************************************
Todo: Log the progress through the pipeline in a machine parsable format
****************************************************************************************

    Standard parsable format for reporting the state of the pipeline  enhancement

    * Timestamped text file
    * Timestamped Database

    Unit tests dependeing on topology output:

    * ``Pipeline.clone()``
    * Whether setup occurs ``pipeline_run()`` where ``target_tasks`` and ``forcedtorun_tasks`` are in different linked or unlinked pipelines
    * pipeline in separate module
    * self dependency -> errors


****************************************************************************************
Todo: Check non-reentrant / global variables
****************************************************************************************
    #. update_checksum_level_on_tasks(checksum_level) is non reentrant

****************************************************************************************
Todo: Pipeline runs should have tags / names
****************************************************************************************

****************************************************************************************
Todo: either_or: Prevent failed jobs from propagating further
****************************************************************************************

    Motivating example:

    .. <<Python_

    .. code-block:: python

        @transform(prevtask, suffix(".txt"),  either_or(".failed", ".succeed"))
        def task(input_file, output_files):
            succeed_file_name, failed_file_name = output_files
            if not run_operation(input_file, succeed_file_name):
                # touch failed file
                with open(failed_file_name, "w") as faile_file:
                    pass

    ..
        Python_


.. _todo.inactive_tasks_in_pipeline_printout_graph:

********************************************************************************************************
Todo: (bug fix) pipeline_printout_graph should print inactive tasks
********************************************************************************************************


.. _todo.dynamic_strings:

********************************************************************************************************
Todo: Mark input strings as non-file names, and add support for dynamically returned parameters
********************************************************************************************************

    1. Use indicator object.
    2. What is a good name? ``"output_from()"``, ``"NOT_FILE_NAME"`` :-)
    3. They will still participate in suffix, formatter and regex replacement

    Bernie Pope suggests that we should generalise this:


    If any object in the input parameters is a (non-list/tuple) class instance, check (getattr) whether it has a ``ruffus_params()`` function.
    If it does, call it to obtain a list which is substituted in place.
    If there are string nested within, these will also take part in Ruffus string substitution.
    Objects with ``ruffus_params()`` always "decay" to the results of the function call

    ``output_from`` would be a simple wrapper which returns the internal string via ``ruffus_params()``

    .. code-block:: python

        class output_from (object):
            def __init__(self, str):
                self.str = str
            def ruffus_params(self):
                return [self.str]

    Returning a list should be like wildcards and should not introduce an unnecessary level of indirection for output parameters, i.e. suffix(".txt") or formatter() / "{basename[0]}" should work.

    Check!



===============================================
Future Changes to Ruffus
===============================================

    I would appreciated feedback and help on all these issues and where next to take *ruffus*.


    **Future Changes** are features where we more or less know where we are going and how to get there.

    **Planned Improvements** describes features we would like in Ruffus but where the implementation
    or syntax has not yet been (fully) worked out.

    If you have suggestions or contributions, please either write to me ( ruffus_lib at llew.org.uk) or
    send a pull request via the `git site  <https://github.com/bunbun/ruffus>`__.



****************************************************************************************
Todo: Replacements for formatter(), suffix(), regex()
****************************************************************************************

    formatter etc. should be self contained objects derived from a single base class
    with behaviour rather than empty tags used for dispatching to functions

    The design is better fit by and should be switched over to an inheritance scheme


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

    For ``INPUTS`` or ``EXTRAS`` which have objects with a ``ruffus_params()`` function (see Todo item above),
    the original object rather than the result of ``ruffus_params()`` is forwarded.



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

_________________________________________________________
Checkpointing
_________________________________________________________

    * If checkpoint file is used, the actual files are saved and checked the next time
    * If no files are generated, no files are checked the next time...
    * The output files do not have to match the wildcard though we can output a warning message if that happens...
      This is obviously dangerous because the behavior will change if the pipeline is rerun without using the checkpoint file
    * What happens if the task function changes?

***************************************
Todo: New decorators
***************************************

_________________________________________________________
Todo: ``@originate``
_________________________________________________________

    Each (serial) invocation returns lists of output parameters until returns
    None. (Empty list = ``continue``, None = ``break``).



_________________________________________________________
Todo: ``@recombine``
_________________________________________________________

    Like ``@collate`` but automatically regroups jobs which were a result of a previous ``@subdivide`` / ``@split`` (even after intervening ``@transform`` )

    This is the only way job trickling can work without stalling the pipeline: We would know
    how many jobs were pending for each ``@recombine`` job and which jobs go together.

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

_________________________________________________________
Converting to per-job rather than per task dependencies
_________________________________________________________
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

_________________________________________________________
Implementation
_________________________________________________________

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

.. _todo.move_checkpoint_files:

********************************************************************************************************
Todo: Allow checkpoint files to be moved
********************************************************************************************************

    Allow checkpoint files to be "rebased" so that moving the working directory of the pipeline does not
    invalidate all the files.

    We need some sort of path search and replace mechanism which handles conflicts, and probably versioning?



.. _todo.intermediate_files:

********************************************************************************************************
Todo: Remove intermediate files
********************************************************************************************************

    Often large intermediate files are produced in the middle of a pipeline which could be
    removed. However, their absence would cause the pipeline to appear out of date. What is
    the best way to solve this?

    In gmake, all intermediate files which are not marked ``.PRECIOUS`` are deleted.

    We can similar mark out all tasks producing intermediate files so that all their output file can be deleted using an ``@intermediate/provisional/transient/temporary/interim/ephemeral`` decorator.

    The tricky part of the design is how to delete files without disrupting our ability to build the original file dependency DAG, and hence
    check which tasks have up-to-date output when the pipeline is run again.

    1. We can just work back from upstream/downstream files and ignore the intermediate files as gmake does. However,
       the increased power of Ruffus makes this very fragile: In gmake, the DAG is entirely specified by the specified destination files.
       In Ruffus, the number of task files is indeterminate, and can be changed at run time (see @split and @subdivide)
    2. We can save the filenames into the checksum file before deleting them
    3. We can leave the files in place files but zero out their contents. It is probably best
       to write a small magic text value to the file, e.g. "RUFFUS_ZEROED_FILE", so that we are
       not confused by real files of zero size.

    In practice (2) and (3) should be combined for safety.

    1. pipeline_cleaunup() will print out a list of files to be zeroed, or a list of commands to zero files or just do it for you
    2. When rerunning, we can force files to be recreated using ``pipeline_run(..., forcedtorun_tasks,...)``, and Ruffus will track back
       through lists of dependencies and recreate all "zeroed" files.



===============================================
Planned Improvements to Ruffus
===============================================

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
       * http://zguide.zeromq.org/page:all
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

