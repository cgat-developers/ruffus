##########################################
New features in the next release
##########################################
***************************************
New features
***************************************

    #. Job completion monitoring: ``pipeline_run(..., checksum_level=CHECKSUM_FILE_TIMESTAMPS, ...)``
    #. ``@originate()``: Make new files (jobs) *ex nihilo*
    #. ``@subdivide`` / ``@split(..., regex(), ...)``
    #. ``formatter`` : with regular expression or not. More flexible replacement for ``regex``
    #. ``@combinatorics.product``
    #. ``@combinatorics.permutations``
    #. ``@combinatorics.combinations``
    #. ``@combinatorics.combinations_with_replacement``
    #. ``@active_if``
    #. ``cmdline`` module to cut down boilerplate code
    #. ``drmaa`` module to help running on a cluster


##########################################
In progress: Refactoring Ruffus Docs
##########################################

    Remember to cite Jake Biesinger and see if he is interested to be a co-author if we ever resubmit the drastically changed version...

    One Table of Contents to rule them all. The current scattered TOCs break rest particularly for pdf builds.

    Tutorial in process at www.well.ox.ac.uk/~lg/oss/ruffus/doc/_build/html/tutorials/new_tutorial/step1.html


***************************************
New order of Topics in the tutorial
***************************************

    1. introduction to decorators, taks and jobs
    2. ``@transform`` as the paradigm for Ruffus
    3. more ``@transform`` (``multiprocess``) and ``@originate`` to start the pipeline
    4. task completion monitoring and exceptions
       Mention the use of file dates and a database. Exceptions
    5. ``pipeline_printout``and ``cmdline``
    6. ``pipeline_printout_graph``
    7. ``suffix`` and ``formatter`` to generate output file names from input file names
    8. A bestiary of the different decorators and how they determine the jobs topology of the pipeline: ``1-to-many``, ``many-to-1`` , ``1-to-1``, ``many-to-many-more``, ``many-to-fewer``, i.e. ``@split``, ``@merge``, ``@transform``, ``@subdivide``, ``@collate``.
    9. ``@split``
    10. ``@merge``
    11. ``@posttask``

***************************************
New order of Topics in the manual
***************************************
    Should not cover the same material as the tutorial. Assumes the reader has read the tutorial first.

    * Tasks as recipes and jobs
    * ``@transform``
    * ``@originate``
    * chaining tasks ``output_from``, Reusing pipeline code in modules
    * ``pipeline_run``, ``pipeline_printout``, ``pipeline_printout_graph`` and ``cmdline``
    * exceptions (``JobSignalledBreak``), early termination and logging ``stderr_logger`` and ``black_hole_logger``
    * Job completion monitoring
    * ``@split``
    * ``@merge``
    * ``@subdivide``
    * ``@collate``
    * ``@posttask``
    * ``@mkdir``
    * Running in parallel: ``@jobs_limit``, ``pipeline_run(..., multi_thread | multi_process,...)`` ``@active_if`` and ``drmaa``
    * ``combinatorics`` module: ``@product``, ``@permutations``, ``@combinations``, ``@combinations_with_replacement``
    * ``add_inputs``, ``inputs``

Esoteric
    * ``@follows`` ``touch_file``
    * ``@parallel``
    * ``@check_if_uptodate``

Legacy and deprecated
   * ``@files``
    * ``@files_re``
    * ``regex``
    * ``@split(...,regex(),...)``


Best Practices
    *

##########################################
In progress: Refactoring Ruffus
##########################################

    All in progress items completed


##########################################
Future / Planned Improvements to  Ruffus
##########################################

****************************************************
Todo: Running python jobs remotely on cluster nodes
****************************************************

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


***************************************
Notes on how to write new decorators
***************************************


    New placeholder class. E.g. for ``@new_deco``

    .. code-block:: python

        class new_deco(task_decorator):
            pass

    Add to list of action names and ids:

    .. code-block:: python

        action_names = ["unspecified",
                        ...
                        "task_new_deco",

        action_task_new_deco     =  15

    Add function:

    .. code-block:: python

        def task_transform (self, orig_args):



***************************************
New decorators
***************************************
==============================================================================
Planned: ``@split`` / ``@subdivide``
==============================================================================

    Return output parameters so that we can stop using wild cards, and the whole
    things become so much cleaner


==============================================================================
Planned: ``@originate``
==============================================================================

    Each (serial) invocation returns lists of output parameters until returns
    None. (Empty list = ``continue``, None = ``break``).



==============================================================================
Planned: ``@recombine``
==============================================================================

    Like ``@collate`` but automatically regroups jobs which were a result of a previous ``@subdivide`` / ``@split`` (even after intervening ``@transform`` )

    This is the only way job trickling can work without stalling the pipeline: We would know
    how many jobs were pending for each ``@recombine`` job and which jobs go together.


********************************************
Planned: Job Trickling brain storming Notes
********************************************

    * allows depth first iteration of tree
    * ``@recombine`` is the necessary step, otherwise all ``@split`` + ``@merge`` / ``@collate`` end in a pipeline stall and we are back to running breadth first rather than depth first. Might as well not bother...
    * Jobs need unique job_id tag
    * Need a way of generating filenames without returning from a function
      indefinitely: i.e. ``@originate`` and ``@split`` should ``yield``
    * Need a way of knowing which files group together (i.e. were split
      from a common job) without using regex (magic ``@split`` and ``@remerge)``
    * ``@split`` needs to be able to specify at run time the number of
      resulting jobs without using wild cards
    * ``@merge`` needs to know when all of a group of files have completed
    * legacy support for wild cards and file names.
    * Possible breaking change: Assumes an explicit ``@follows`` if require
      *all* jobs from the previous task to finish
    * "Push" system of checking in completed jobs into "slots" of waiting
      tasks
    * New jobs dispatched when slots filled adequately
    * Funny "single file" mode for ``@transform,`` ``@files`` needs to be
      regularised so it is a syntactic (front end) convenience (oddity!)
      and not plague the inards of ruffus
    * use named parameters in decorators for clarity?



************************************
Planned: Custom parameter generator
************************************

    Leverages built-in Ruffus functionality.
    Don't have to write entire parameter generation from scratch.

    * Gets passed an iterator where you can do a for loop to get input parameters / a flattened list of files
    * Other parameters are forwarded as is
    * The duty of the function is to ``yield`` input, output, extra parameters


    Simple to do but how do we prevent this from being a job-trickling barrier?

    Postpone until we have an initial design for job-trickling: Ruffus v.4 ;-(



****************************************************************************
Desired!: Ruffus GUI interface.
****************************************************************************

    Desktop (PyQT or web-based solution?)  I'd love to see an svg pipeline picture that I could actually interact with


****************************************************************************
Find contributions for!: Extending graphviz output
****************************************************************************

****************************************
Desired!: Deleting intermediate files
****************************************

****************************************
Desired!: Registering jobs for clean up
****************************************


##########################################
Ruffus documentation Notes
##########################################

***************************************
``pipeline_run(...)`` and exceptions
***************************************
    * Optionally terminate pipeline after first exception
        To have all exceptions interrupt immediately::

                pipeline_run(..., exceptions_terminate_immediately = True)

        By default ruffus accumulates ``NN`` errors before interrupting the pipeline prematurely. ``NN`` is the specified parallelism for ``pipeline_run(..., multiprocess = NN)``.

        Otherwise, a pipeline will only be interrupted immediately if exceptions of type ``ruffus.JobSignalledBreak`` are thrown.

    * Display exceptions without delay

        By default, Ruffus re-throws exceptions in ensemble after pipeline termination.

        To see exceptions as they occur::

                pipeline_run(..., log_exceptions = True)

        ``logger.error(...)`` will be invoked with the string representation of the each exception, and associated stack trace.

        The default logger prints to sys.stderr, but this can be changed to any class from the logging module or compatible object via ``pipeline_run(..., logger = ???)``





##########################################
Updated Ruffus
##########################################

    Unfortunately, some additions to the ruffus namespace were made

        ``formatter``, ``subdivide``, ``originate``


***************************************
Task completion monitoring
***************************************

    * Contributed by **Jake Biesinger**
    * defaults to using checking file timestamps stored in an sqllite database in the current directory (``ruffus_utilility.RUFFUS_HISTORY_FILE = '.ruffus_history.sqlite'``)
    * ``pipeline_run(..., checksum_level = N, ...)``

        where the default is 1:

           level 0 : Use only file timestamps
           level 1 : above, plus timestamp of successful job completion
           level 2 : above, plus a checksum of the pipeline function body
           level 3 : above, plus a checksum of the pipeline function default arguments and the additional arguments passed in by task decorators


======================================================================
What happens when code pickling fails
======================================================================

    People "out there" have a lot of unpicklable stuff in their functions:
    e.g. nested functions, lambdas, dynamic objects, globals

    Added graceful fallback mode so that Ruffus continues to chug along under provocation.
    Don't know how to inform the user when this happens


======================================================================
Job completion should pass ``job_history`` down call chain
======================================================================
    ::

        pipeline_run()
            ->make_job_parameter_generator()

        pipeline_printout()
            ->printout()

        pipeline_printout()
        pipeline_run()
            ->topologically_sorted_nodes()
                ->signal
                    -> needs_update_func()


    ``file_name_parameters.needs_update_check_modify_time (*params, **kwargs)``

        does not necessarily get the extra ``job_history`` (or ``task``) parameters in test code.
        Can we fix this? A hack recreates ``job_history`` if it is missing as a parameter but this hack
        will hide problems later on...

======================================================================
remove job_history updates when ``touching``
======================================================================
    .. code-block:: python

      def job_wrapper_io_files(param, user_defined_work_func, register_cleanup, touch_files_only):
          #
          #   touch files only
          #
          for f in get_strings_in_nested_sequence(o):
              if not os.path.exists(f):
                  open(f, 'w')
                  mtime = os.path.getmtime(f)
              else:
                  os.utime(f, None)
                  mtime = os.path.getmtime(f)
              chksum = JobHistoryChecksum(f, mtime, param[2:], user_defined_work_func.pipeline_task)
              job_history[f] = chksum  # update file times and job details in history


    * How easy is it to abstract out the database?

        * The database is Jacob Sondergaard's ``dbdict`` which is a nosql / key-value store wrapper around sqlite
            .. code-block:: python


======================================================================
Comments on: Job completion monitoring
======================================================================

    * On by default?

            * yes: ``CHECKSUM_HISTORY_TIMESTAMPS``.
            * Use ``pipeline_run(..., checksum_level=CHECKSUM_FILE_TIMESTAMPS, ...)`` for classic mode
            * N.B. Even in classic mode, a ``.ruffus_history.sqlite`` file gets created and updated.
            * Can we have a **nothing** mode using ``dbdict.open(':memory:')``?

    * How resistant is it to corruption?

        Very. Sqlite!

    * Can we query the database, get Job history / stats?

        Yes, if we write a function to read and dump the entire database but this is only useful with timestamps and task names. See below

    * Can we log task names and dispatch / completion timestamps to the same database?

        See ``ruffus_utility.JobHistoryChecksum``

    * What are the run time performance implications?

        * Normally a single instance of dbdict / database connections is created and used inside ``pipeline_run``
        * Each call to ``file_name_parameters.py.needs_update_check_modify_time()`` also opens a connection to the database.
        * We can pass the dbdict connection as an extra parameter to reduce overhead

    * Why is  ``touch``-ing files ( ``pipeline_run(..., touch_files_only = True, ...)`` ) handled directly (and across the multiprocessor boundary) in ``task.job_wrapper_io_files()`` ?

        .. code-block:: python

          def job_wrapper_io_files(param, user_defined_work_func, register_cleanup, touch_files_only):
              #
              #   touch files only
              #
              for f in get_strings_in_nested_sequence(o):
                  if not os.path.exists(f):
                      open(f, 'w')
                      mtime = os.path.getmtime(f)
                  else:
                      os.utime(f, None)
                      mtime = os.path.getmtime(f)
                  chksum = JobHistoryChecksum(f, mtime, param[2:], user_defined_work_func.pipeline_task)
                  job_history[f] = chksum  # update file times and job details in history


        **No longer** (refactored)

    * Can we get rid of the minimum 1 second delay between jobs now? Does the database have finer granularity in timestamps? Can we use the database timestamps provided they are *later* than the filesystem ones?

        * Not at the moment. The database records the file modification time on disk. Is this to be paranoid (careful!)?
        * We can change to a disk-less mode and use the system time, recording output files *after* the job returns.


    * How easy is it to abstract out the database?

        * The database is Jacob Sondergaard's ``dbdict`` which is a nosql / key-value store wrapper around sqlite
            .. code-block:: python

                job_history = dbdict.open(RUFFUS_HISTORY_FILE, picklevalues=True)

        * The key is the output file name, so it is important not to confuse Ruffus by having different tasks generate the same output file!
        * Is it possible to abstract this so that **jobs** get timestamped as well?
        * If we should ever want to abstract out ``dbdict``, we need to have a similar key-value store class,
          and make sure that a single instance of ``dbdict`` is used through ``pipeline_run`` which is passed up
          and down the function call chain. ``dbdict`` would then be drop-in replaceable by our custom (e.g. flat-file-based) dbdict alternative.


============================================================================================================================================================
set history_file  as a parameter to ``pipeline_run``, ``pipeline_printout``, ``pipeline_printout_graph``
============================================================================================================================================================

    * try using ``pipeline_run(.., history_file = "XXX", ...)``
    * If that is missing use default from ``ruffus.ruffus_utility``.

    Default is ``.ruffus_history.sqlite`` (i.e. in the current working directory)
    But can be overridden by the environment variable DEFAULT_RUFFUS_HISTORY_FILE

    There is also path expansion using the main script name.

        So if the environment variable is:

        ::

            export DEFAULT_RUFFUS_HISTORY_FILE=.{basename}.ruffus_history.sqlite

        Then the job history database for ``run.me.py`` will be ``.run.me.ruffus_history.sqlite``

        All the scripts can be set to a single directory by using:

        ::

            export DEFAULT_RUFFUS_HISTORY_FILE=/common/path/for/job_history/.{basename}.ruffus_history.sqlite

        If you are really paranoid about name clashes, you can use:

        ::

            export DEFAULT_RUFFUS_HISTORY_FILE=/common/path/for/job_history/{subdir[0]}/.{basename}.ruffus_history.sqlite

            /test/bin/scripts/run.me.py
                -> /common/path/for/job_history/scripts/.run.me.ruffus_history.sqlite


        or even:

        ::

            export DEFAULT_RUFFUS_HISTORY_FILE=/common/path/for/job_history/{path}/.{basename}.ruffus_history.sqlite

            /test/bin/scripts/run.me.py
                -> /common/path/for/job_history/test/bin/scripts/.run.me.ruffus_history.sqlite


        Just make sure that the requisite destination directories exist...

============================================================================================================================================================
set job_history file name set to "nothing" if checksum_level=CHECKSUM_FILE_TIMESTAMPS
============================================================================================================================================================

    If we aren't using checksums (``pipeline_run(..., checksum_level=CHECKSUM_FILE_TIMESTAMPS, ...) ``,
    and ``history_file`` hasn't been specified, we might be a bit surprised to find Ruffus
    writing to a sqlite db anyway.

    Let us just use an in-memory db which will be thrown away

    Of course, if history_file is specified, we presume you know what you are doing:
    Don't *check* the sqlite db but make sure it is up to date

    This also means to recreate a checksum file, you can just run the pipeline normally in CHECKSUM_FILE_TIMESTAMPS but
    with the history_file specified.


============================================================================================================================================================
regenerate job_history from extant i/o files (from a previous run)
============================================================================================================================================================


   If pipeline(touch_files_only = CHECKSUM_REGENERATE, ...) will regenerate the checksum history file to reflect the existing i/o files on disk.


***************************************
pipeline_run(..., multithread= N, ...)
***************************************

    Use multi_threading rather than multiprocessing

    This is the only safe way to run drmaa.

    Normally this would reduce the amount of parallelism in your code (but reduce the marshalling cost across process boundaries).
    However, if the work load is mostly on another computer with a separate python interpreter, any cost benefit calculations are moot.


***************************************
drmaa
***************************************

    Implemented in drmaa_wrapper.py

    Alternative, non-drmaa polling code at

    https://github.com/bjpop/rubra/blob/master/rubra/cluster_job.py

    Probably not necessary surely.

******************************************************************************
New flexible ``formatter`` alternative to ``regex`` ``suffix``
******************************************************************************

    * Produces (pre-canned) path subcomponents in the style ``os.path.split()``
    * Produces optional [Regular Expression] matches (i.e. optionally filters on a regular expression)
    * Familiar pythonesque syntax
    * Can refer to the Nth-input file and not just the first like ``Suffix()`` and ``Regex()``
    * Can even refer to individual letters within a match


==============================================================================
Building blocks for pattern substitution
==============================================================================
    Formatter produces regular expression matches and path components, adding a level of indirection for each level of nesting.
    In the case of ``@transform`` ``@collate`` we are dealing with a list of input files per job, so typically,
    the components with be, using python format syntax:

        .. code-block:: python

            input_file_names = ['/a/b/c/sample1.bam']
            formatter(r"(.*)(?P<id>\d+)\.(.+)")

            "{0[0]}"            #   '/a/b/c/sample1.bam',           // Entire match captured by index
            "{1[0]}"            #   '/a/b/c/sample',                // captured by index
            "{2[0]}"            #   'bam',                          // captured by index
            "{id[0]}"           #   '1'                             // captured by name
            "{basename[0]}"     #   'sample1',                      // file name
            "{ext[0]}"          #   '.bam',                         // extension
            "{path[0]}"         #   '/a/b/c',                       // full path
            "{subpath[0][1]}"   #   '/a/b'                          // recurse down path 1 level
            "{subdir[0][0]}"    #   'c'                             // 1st level subdirectory


==============================================================================
``@transform`` example
==============================================================================
    .. code-block:: python

        @transform( previous_task,
                    formatter(".*/(?P<FILE_PART>.+).tmp1$" ),   # formatter with optional regular expression
                    "{path[0]}/{FILE_PART[0]}.tmp2",            # output
                    "{basename}",                               # extra: list of all file names
                    "{basename[0]}",                            # extra: first file name
                    "{basename[0][0]}",                         # extra: first letter of first file name
                    "{subpath[0][1]}",                          # extra: 1st file, recurse down path 1 level
                    "{subdir[2][1]}")                           # extra: 3rd file, 1st level sub directory
        def test_transform_task(    infiles,
                                    outfile,
                                    all_file_names_str,
                                    first_file_name,
                                    first_file_name_1st_letter,
                                    first_file_name_first_subpath,
                                    first_file_name_first_subdir):
            """
                Test transform with formatter
            """
            pass

==============================================================================
``@combinations`` example
==============================================================================

    Extra level of indirection because we are dealing with 3 **groups** of input combined

    .. code-block:: python

        @combinations(  previous_task,
                        formatter(".*/(?P<FILE_PART>.+).tmp1$" ),                                   # formatter with optional regular expression
                        3,                                                                          # number of k-mers
                        "{path[0][0]}/{FILE_PART[0][0]}.{basename[1][0]}.{basename[2][0]}.tmp2",    # output file name is a combination of each 3 input files
                        "{basename[0]}{basename[1]}{basename[2]}"                                   # extra: list of 3 sets of file names
                        "{basename[0][0]}{basename[1][0]}{basename[2][0]}",                         # extra: first file names for each of 3 set
                        "{basename[0][0][0]}{basename[1][0][0]}{basename[2][0][0]}",                # extra: first letters of first file name from each of 3 input
                        "{subpath[0][0][1]}",                                                       # extra: 1st input, 1st file, recurse down path 1 level
                        "{subdir[2][3][1]}")                                                        # extra: 3rd input, 4th file, 1st level sub directory
        def test_combinations3_task(nfiles,
                                    outfile,
                                    all_file_names_str,
                                    first_file_names,
                                    first_file_names_1st_letters,
                                    first_file_name_first_subpath,
                                    first_file_name_first_subdir):
            """
                Test combinations with k-tuple = 3
            """
            pass



==============================================================================
Using regular expressions as a filter
==============================================================================

    If ``regex_str`` is specified (``formatter(r".*")`` rather than ``formatter()``),
    then regular expression match failures will return an empty dictionary.

    The idea is we can use regular expression matches as a filter if we refer to that file our specified pattern.

    For example,

    .. code-block:: python

        # filter on ".txt"
        input_filenames = ["a.wrong", "b.txt"]
        formatter(".txt$")

        # OK: regular expression matches the second file name
        "{basename[1]}"

        # Fails: regular expression does not match the second file name. No format substitutions make sense
        "{basename[0]}"


    Note that we are not doing regular expression *substitution* here only matching. Because ``"a.wrong"`` doesn't match
    ``".txt"``, even ``basename[0]`` will fail.

    The regular expression mismatch *taints* all references to that file name in the substitution pattern.

==============================================================================
``regex()`` and ``suffix()``
==============================================================================


    The previous behaviour with regex() where mismatches fail even if no substitution is made is retained by the use of ``re.subn()``.
    This is a corner case but I didn't want user code to break

    .. code-block:: python

        # filter on ".txt"
        input_filenames = ["a.wrong", "b.txt"]
        regex("(.txt)$")

        # fails, no substitution possible
        r"\1"

        # fails anyway even through regular expression matches not referenced...
        r"output.filename"

==============================================================================
implementation
==============================================================================
    ``get_all_paths_components(paths, regex_str)`` in ``ruffus_utility.py``

    Input files names are first squished into a flat list of files.
    ``get_all_paths_components()`` returns both the regular expression matches and the break down of the path.

    In case of name clashes, the classes with higher priority override:

        1) Captures by name
        2) Captures by index
        3) Path components:
            'ext' = extension with dot
            'basename' = file name without extension
            'path' = path before basename, not ending with slash
            'subdir' = list of directories starting with the most nested and ending with the root (if normalised)
            'subpath' = list of 'path' with successive directories removed starting with the most nested and ending with the root (if normalised)

        E.g.  ``name = '/a/b/c/sample1.bam'``, ``formatter=r"(.*)(?P<id>\d+)\.(.+)")`` returns:

        .. code-block:: python

                0:          '/a/b/c/sample1.bam',           // Entire match captured by index
                1:          '/a/b/c/sample',                // captured by index
                2:          'bam',                          // captured by index
                'id':       '1'                             // captured by name
                'ext':      '.bam',
                'subdir':   ['c', 'b', 'a', '/'],
                'subpath':  ['/a/b/c', '/a/b', '/a', '/'],
                'path':     '/a/b/c',
                'basename': 'sample1',


    The code is in ``ruffus_utility.py``:

    .. code-block:: python

        results = get_all_paths_components(paths, regex_str)
        string.format(results[2])


    All the magic is hidden inside black boxes ``filename_transform`` classes:

    .. code-block:: python


        class t_suffix_filename_transform(t_filename_transform):
        class t_regex_filename_transform(t_filename_transform):
        class t_format_filename_transform(t_filename_transform):


******************************************************************************
Refactoring parameter handling
******************************************************************************

    Though the code is still split in a not very sensible way between ``ruffus_utility.py``, ``file_name_parameters.py`` and ``task.py``,
        some rationalisation has taken place, and comments added so further refactoring can be made more easily.

    Common code for::

        file_name_parameters.split_ex_param_factory()
        file_name_parameters.transform_param_factory()
        file_name_parameters.collate_param_factory()

    has been moved to ``file_name_parameters.py.yield_io_params_per_job()``


    unit tests added to ``test_file_name_parameters.py`` and ``test_ruffus_utility.py``


************************************************************************************************************************************************************
Better error messages for ``formatter()``, ``suffix()`` and ``regex()`` for ``pipeline_printout(..., verbose >= 3, ...)``
************************************************************************************************************************************************************

    * Error messages for showing mismatching regular expression and offending file name
    * Wrong capture group names or out of range indices will raise informative Exception
    * ``regex()`` and ``suffix()`` examples in ``test/test_regex_error_messages.py``
    * ``formatter()`` examples in ``test/test_combinatorics.py``



********************************************
``@product()``
********************************************

    * Put all new generators in an ``combinatorics`` submodule namespace to avoid breaking user code. (They can imported if necessary.)
    * Only ``formatter([OPTIONAl_REGEX])`` provides the necessary flexibility to construct the output so we won't bother with ``suffix`` and ``regex``
    * test code in test/test_combinatorics.py

============================================================================================================================================================
Final syntax
============================================================================================================================================================

    .. code-block:: python


        @product(
                "*.a",
                formatter( ".*/(?P<ID>\w+.bamfile).bam" ),
                AToB,
                formatter(),
                ...
                "{path[0][0]}/{base_name[0][0]}.{base_name[0][0]}.out",
                "{path[0][0]}",       # extra: path for 1st input, 1st file
                "{path[1][0]}",       # extra: path for 2nd input, 1st file
                "{basename[0][1]}",   # extra: file name for 1st input, 2nd file
                "{ID[1][2]}",         # extra: regular expression named capture group for 2nd input, 3rd file
                )
        def product( infiles, outfile,
                    input_1__path,
                    input_2__path,
                    input_1__2nd_file_name,
                    input_2__3rd_file_match
                    ):
            print infiles, outfile

    * Flexible number of pairs of ``task`` / ``glob`` / file names + ``formatter()``
    * Only ``formatter([OPTIONAl_REGEX])`` provides the necessary flexibility to construct the output so we won't bother with suffix and regex
    * Use all "Combinatoric generators" from itertools. Use the original names for clarity, and the itertools implementation under the hood
    * Put all new generators in an ``combinatorics`` submodule namespace to avoid breaking user code. (They can import if necessary.)
    * The ``itertools.product(repeat)`` parameter doesn't make sense for Ruffus and will not be used


============================================================================================================================================================
Initial proposed syntax
============================================================================================================================================================

    Andreas Heger:

    .. code-block:: python

        @product( "*.a", AToB,
              regex( "(.*).a" ),
              regex( "(.*).b" ),
              "%1_vs_%2.out" )
        def product( infiles, outfile ):
            print infiles, outfile


    Jake Biesinger:

    .. code-block:: python


        @product( "*.a",
                regex( "(.*).a" ),
                AToB,
                regex( "(.*).b" ),
                ...
                "???,out" )
        def product( infiles, outfile ):
            print infiles, outfile

============================================================================================================================================================
Implementation
============================================================================================================================================================

    Similar to ``@transform`` but with extra level of nested-ness

    Retain same code for ``@product`` and ``@transform`` by adding an additional level of indirection:
        * generator wrap around ``get_strings_in_nested_sequence`` to convert nested input parameters either to a single flat list of file names or to nested lists of file names

          .. code-block:: python

              file_name_parameters.input_param_to_file_name_list (input_params)
              file_name_parameters.list_input_param_to_file_name_list (input_params)

        * ``t_file_names_transform`` class which stores a list of regular expressions, one for each ``formatter()`` object corresponding to a single set of input parameters

          .. code-block:: python

            t_formatter_file_names_transform
            t_nested_formatter_file_names_transform

        * string substitution functions which will apply a list of ``formatter`` changes

          .. code-block:: python

                ruffus.utility.t_formatter_replace()
                ruffus.utility.t_nested_formatter_replace()

        * ``ruffus_uilility.swap_doubly_nested_order()`` makes the syntax / implementation very orthogonal

******************************************************************************************
``@permutations(...),`` ``@combinations(...),`` ``@combinations_with_replacement(...)``
******************************************************************************************

    * Put all new generators in an ``combinatorics`` submodule namespace to avoid breaking user code. (They can imported if necessary.)
    * Only ``formatter([OPTIONAl_REGEX])`` provides the necessary flexibility to construct the output so we won't bother with suffix and regex
    * test code in test/test_combinatorics.py

    Use combinatoric generators from itertools and keep that naming scheme

    Final syntax:




    .. code-block:: python




        @permutations(
                "*.a",
                formatter( ".*/(?P<ID>\w+.bamfile).bam" ),     # Elements in a tuple come from a single list, so we only need one formatter
                2,                                             # k_length_tuples,
                "{path[0][0]}/{base_name[0][0]}.{base_name[1][0]}.out",
                "{path[0][0]}",                                # extra: path for 1st input, 1st file
                "{path[1][0]}",                                # extra: path for 2nd input, 1st file
                "{basename[0][1]}",                            # extra: file name for 1st input, 2nd file
                "{ID[1][2]}",                                  # extra: regular expression named capture group for 2nd input, 3rd file
                )
        def task1( infiles, outfile,
                    input_1__path,
                    input_2__path,
                    input_1__2nd_file_name,
                    input_2__3rd_file_match
                    ):
            print infiles, outfile


============================================================================================================================================================
Implementation
============================================================================================================================================================

    Similar to ``@product`` extra level of nested-ness is self versus self

    Retain same code for ``@product``
        * forward to a sinble ``file_name_parameters.combinatorics_param_factory()``
        * use ``combinatorics_type`` to dispatch to ``combinatorics.permutations``, ``combinatorics.combinations`` and ``combinatorics.combinations_with_replacement``
        * use ``list_input_param_to_file_name_list`` from ``file_name_parameters.product_param_factory()``


******************************************************************************
``@mkdir`` with ``formatter()``, ``suffix()`` and ``regex()``
******************************************************************************

    * essentially behaves just like ``@transform`` but with its own (internal) function which does the actual work of making a directory
    * ``mkdir`` continues to work seamlessly inside ``@follows``) but also as its own decorator ``@mkdir`` due to the original happy orthogonal design
    * fixed bug in checking so that Ruffus does't blow up if non strings are in the output (number...)
    * fixed ugly bug in ``pipeline_printout`` for printing single line output
    * fixed description and printout indent
    * note: adding the decorator to a previously undecorated function might have unintended consequences. The undecorated function
      turns into a zombie.

************************************************************************************************
``@originate``
************************************************************************************************

    * generates output *ex nihilo*, i.e. not from previous dependencies
    * useful at top of pipeline
    * Can use file lists or wildcards (please don't! :-) )
    * Planned future support for ``yield`` to get rid of wild cards
    * synonym for ``@split(None,...)``
    * prints as such:

        .. code-block:: bash

           Task = generate_initial_files
               Job  = [None
                     -> a.tmp1
                     -> b.tmp1]
                 Job needs update: Missing files [a.tmp1, b.tmp1]

    * N.B. Task function obviously only takes outputs (and extras)

************************************************************************************************
cmdline: 5 lines of boilerplate
************************************************************************************************

============================================================================================================================================================
argparse
============================================================================================================================================================


        .. code-block:: python

            from ruffus import *

            parser = cmdline.get_argparse(description='WHAT DOES THIS PIPELINE DO?')

            #   <<<---- add your own command line options like --input_file here
            #parser.add_argument("--input_file")

            options = parser.parse_args()

            #  logger which can be passed to multiprocessing ruffus tasks
            logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

            #   <<<----  pipelined functions go here

            cmdline.run (options)


    Provides these predefined options:

        .. code-block:: bash

            -v, --verbose
                --version
            -L, --log_file

            -T, --target_tasks
            -j, --jobs
                --use_threads
            -n, --just_print
                --flowchart
                --key_legend_in_graph
                --draw_graph_horizontally
                --flowchart_format
                --forced_tasks
                --touch_files_only
                --checksum_file_name
                --recreate_database

    Note that particular options can be skipped (not added to the command line:

        .. code-block:: python

            parser = cmdline.get_argparse(  description='WHAT DOES THIS PIPELINE DO?',
                                            prog = "my_%(prog)s",
                                            ignored_args = ["log_file", "key_legend_in_graph"])


    Note that the version for ``get_argparse`` defaults to ``"%(prog)s 1.0"`` unless specified:

        .. code-block:: python

            parser = cmdline.get_argparse(  description='WHAT DOES THIS PIPELINE DO?',
                                            version = "my_programme.py v. 2.23")





============================================================================================================================================================
optparse (deprecated)
============================================================================================================================================================

    ``optparse`` deprecated since python 2.7

        .. code-block:: python

            #
            #   Using optparse (new in python v 2.6)
            #
            from ruffus import *

            parser = cmdline.get_optgparse(version="%prog 1.0", usage = "\n\n    %prog [options]")

            parser.add_option("-i", "--input_file", dest="input_file", help="Input file")

            (options, remaining_args) = parser.parse_args()

            #  logger which can be passed to ruffus tasks
            logger, logger_mutex = cmdline.setup_logging ("this_program", options.log_file, options.verbose)

            #_____________________________________________________________________________________

            #   pipelined functions go here

            #_____________________________________________________________________________________

            cmdline.run (options)





************************************************************************************************
``@subdivide``
************************************************************************************************

    synonym for ``@split(..., regex(), ...)``

    Take a list of input jobs (like ``@transform``) but further splits each into multiple jobs, i.e. it is a many->many more relationship

    Example code in  ``test/test_split_regex_and_collate.py``



