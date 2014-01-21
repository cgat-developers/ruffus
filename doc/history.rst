.. include:: global.inc
########################################
Major Features added to Ruffus
########################################

********************************************************************
version 2.4
********************************************************************

============================================================================================================================================================
Additions to ``ruffus`` namespace
============================================================================================================================================================

    * ``formatter``
    * ``subdivide``
    * ``originate``

============================================================================================================================================================
1) Command Line support
============================================================================================================================================================

    The optional ``Ruffus.cmdline`` module provides support for a set of common command
    line arguments which make writing *Ruffus* pipelines much more pleasant.


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

    The following example uses the standard `argparse  <http://docs.python.org/2.7/library/argparse.html>`__ module
    but the deprecated `optparse  <http://docs.python.org/2.7/library/optparse.html>`__ module works as well.


        .. code-block:: python
            :emphasize-lines: 5,13

            from ruffus import *

            parser = cmdline.get_argparse(description='WHAT DOES THIS PIPELINE DO?')

            #   <<<---- add your own command line options like --input_file here
            #parser.add_argument("--input_file")

            options = parser.parse_args()

            #  logger which can be passed to multiprocessing ruffus tasks
            logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

            #   <<<----  pipelined functions go here

            cmdline.run (options)


    You can exclude any of these common options (not add them to the command line):

        .. code-block:: python
            :emphasize-lines: 4

            parser = cmdline.get_argparse(  description='WHAT DOES THIS PIPELINE DO?',
                                            prog = "my_%(prog)s",

                                            # do not use --log_file and --verbose
                                            ignored_args = ["log_file", "verbose"])


    Note that the version for ``get_argparse`` defaults to ``"%(prog)s 1.0"`` unless specified:

        .. code-block:: python

            parser = cmdline.get_argparse(  description='WHAT DOES THIS PIPELINE DO?',
                                            version = "%(prog)s v. 2.23")








============================================================================================================================================================
2) Task completion monitoring
============================================================================================================================================================

    * Contributed by **Jake Biesinger**
    * Uses a fault resistant sqlite database file to log i/o files, and additional checksums
    * defaults to using checking file timestamps stored in an sqllite database in the current directory (``ruffus_utilility.RUFFUS_HISTORY_FILE = '.ruffus_history.sqlite'``)
    * ``pipeline_run(..., checksum_level = N, ...)``

       * level 0 : Use only file timestamps (no checksum file will be created)
       * level 1 : above, plus timestamp of successful job completion
       * level 2 : above, plus a checksum of the pipeline function body
       * level 3 : above, plus a checksum of the pipeline function default arguments and the additional arguments passed in by task decorators

       * defaults to 1
       * Use ``pipeline_run(..., checksum_level=CHECKSUM_FILE_TIMESTAMPS, ...)`` for "classic" mode


    * Allows Ruffus to avoid adding an extra 1 second pause between tasks to guard against file systems with low timestamp granularity.


____________________________________________________________________________________________________________________
The checksum history_file file name can be changed
____________________________________________________________________________________________________________________


    1) Default is ``.ruffus_history.sqlite`` (i.e. in the current working directory)
    2) Overridden by the environment variable DEFAULT_RUFFUS_HISTORY_FILE
    3) Overridden by parameter to ``pipeline_run``, ``pipeline_printout``, ``pipeline_printout_graph``

            ``pipeline_run(.., history_file = "XXX", ...)``

    The environment variable allows file name expansion for maximum flexibility



    *Example 1*: Same directory, different name

        The job history database for ``run.me.py`` will be ``.run.me.ruffus_history.sqlite``:

        .. code-block:: bash

            export DEFAULT_RUFFUS_HISTORY_FILE=.{basename}.ruffus_history.sqlite

        .. code-block:: bash

            # Ruffus script
            /common/path/for/job_history/scripts/run.me.py
            # checksum file
            /common/path/for/job_history/scripts/.run.me.ruffus_history.sqlite

    *Example 2*: Nested in common directory

        .. code-block:: bash

            export DEFAULT_RUFFUS_HISTORY_FILE=/common/path/for/job_history/{path}/.{basename}.ruffus_history.sqlite

        .. code-block:: bash

            # Ruffus script
            /test/bin/scripts/run.me.py
            # checksum file
            /common/path/for/job_history/test/bin/scripts/.run.me.ruffus_history.sqlite


____________________________________________________________________________________________________________________
Regenerate checksums
____________________________________________________________________________________________________________________

    Create or update the checkpoint file so that all existing files in completed jobs appear up to date

    .. code-block:: python

        pipeline(touch_files_only = CHECKSUM_REGENERATE, ...)

    will regenerate the checksum history file to reflect the existing i/o files on disk.



============================================================================================================================================================
3) drmaa support and multithreading: ``ruffus.drmaa_wrapper``
============================================================================================================================================================

    Optional helper module allows jobs to dispatch work to a computational cluster and wait for its completion.

    * First set up a shared drmaa session:

        .. code-block:: python

            #
            #   start shared drmaa session for all jobs / tasks in pipeline
            #
            import drmaa
            drmaa_session = drmaa.Session()
            drmaa_session.initialize()


    * ``ruffus.drmaa_wrapper.run_cmd`` dispatches the actual work to a cluster node within a normal Ruffus job

        This is the equivalent of ``os.system`` or ``subprocess.check_output`` but the code will run remotely
        as specified:

        .. code-block:: python
            :emphasize-lines: 16
            :linenos:

            from ruffus.drmaa_wrapper import run_job, error_drmaa_job

            @collate(prev_task,
                formatter(),
                "{basename[1]}",
                logger, logger_mutex)
            def ruffus_task_func(input_file, output_file):
                pass
                pass
                try:
                    stdout_res, stderr_res = "",""
                    job_queue_name, job_other_options = get_a_or_b_queue()


                    #
                    #   ruffus.drmaa_wrapper.run_job
                    #       takes queue parameters but also optionally allows
                    #       1) output file to be "touched" or
                    #       2) jobs to be run locally (normally, not via drmaa) for debugging
                    #
                    stdout_res, stderr_res  = run_job(cmd,
                                                      job_name = job_name,
                                                      logger=logger,
                                                      drmaa_session=drmaa_session,
                                                      run_locally=options.local_run,
                                                      job_queue_name= "my_queue_name",
                                                      job_other_options= job_other_options)

                # relay all the stdout, stderr, drmaa output to diagnose failures
                except error_drmaa_job as err:
                    raise Exception("Failed to run:\n%(cmd)s\n%(err)s\n%(stdout_res)s\n%(stderr_res)s\n" % locals())


    * Use ``multithread`` rather than ``multiprocess``

        * allows the drmaa session to be shared
        * prevents "processing storms" when hundreds or thousands of cluster jobs complete at the same time.

        .. code-block:: python

            pipeline_run (..., multithread = NNN, ...)

        or if you are using ruffus.cmdline:

        .. code-block:: python

            cmdline.run (options, multithread = options.jobs)



============================================================================================================================================================
4) ``@subdivide``
============================================================================================================================================================

    synonym for ``@split(..., regex(), ...)``

    Take a list of input jobs (like ``@transform``) but further splits each into multiple jobs, i.e. it is a many->many more relationship

    Example code in  ``test/test_split_regex_and_collate.py``



============================================================================================================================================================
5) ``@mkdir`` with ``formatter()``, ``suffix()`` and ``regex()``
============================================================================================================================================================

    * allows directories to be created depending on runtime parameters or the output of previous tasks
    * behaves just like ``@transform`` but with its own (internal) function which does the actual work of making a directory
    * ``mkdir`` continues to work seamlessly inside ``@follows``)

    Example (See below for "formatter" syntax):

        .. code-block:: python
           :emphasize-lines: 1,5,15

            # make fixed name directory before job is run
            @mkdir(workdir + "/test1")

            #
            #  makes directory based on output of previous task:
            #      For example:
            #          /prev/task.1.output   ->  make directories /prev/task.1.dir, /prev/task.1.dir2
            #          /prev/task.2.output   ->  make directories /prev/task.2.dir, /prev/task.2.dir2
            #
            @mkdir(prev_task, formatter(),
                        ["{path[0]}/{basename[0]}.dir"
                         "{path[0]}/{basename[0]}.dir2"])

            #
            #  @transform output lives happily inside new directories
            #
            #          /prev/task.1.output   ->  make directories /prev/task.1.dir/task.1.tmp2
            #          /prev/task.2.output   ->  make directories /prev/task.2.dir/task.2.tmp2
            #
            @transform( generate_initial_files1,
                        formatter(),
                        "{path[0]}/{basename[0]}.dir/{basename[0]}.tmp2")
            def curr_task( infiles, outfile):
                pass



============================================================================================================================================================
6) ``@originate``
============================================================================================================================================================

    * For first step in a pipeline
    * Generates output files without dependencies from scratch  (*ex nihilo*!)
        .. code-block:: python
            :emphasize-lines: 3,5

            @originate([tempdir + d + ".tmp1" for d in 'a', 'b', 'c'])
            def generate_initial_files(outfile):
                pass
    * prints as such:


        .. code-block:: bash

           Task = generate_initial_files
               Job  = [None
                     -> a.tmp1
                     -> b.tmp1]
                 Job needs update: Missing files [a.tmp1, b.tmp1]

    * Task function obviously only takes outputs.
    * synonym for ``@split(None,...)``



============================================================================================================================================================
7) New flexible ``formatter`` alternative to ``regex`` ``suffix``
============================================================================================================================================================

    * Easy manipulation of path subcomponents in the style of `os.path.split()  <http://docs.python.org/2/library/os.path.html#os.path.split>`__

        Regular expressions are no longer necessary for path manipulation

    * Familiar python syntax
    * Optional Regular Expression matches
    * Can refer to any in the list of N nput files (not only the first as for ``regex(...)``)
    * Can even refer to individual letters within a match


____________________________________________________________________________________________________________________
path, extension and basename for pattern substitution
____________________________________________________________________________________________________________________
    ``formatter`` produces matches for both path components and any regular expression.
    Each level of indirection just means another level of nesting.
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


    ``@transform`` example:

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


____________________________________________________________________________________________________________________
``@combinations`` example
____________________________________________________________________________________________________________________

    For the new "combinatorics", (i.e. all versus all etc.) decorators, we have **groups** of inputs for each job.
    This just means an extra level of indirection.

    .. code-block:: python
        :emphasize-lines: 2

        #
        #   Test combinations with k-tuple = 3
        #
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
            pass



____________________________________________________________________________________________________________________
Using regular expressions as a filter
____________________________________________________________________________________________________________________

    * We can use regular expression matches as a filter.

    * Filtering is only applied if the requisited file is referred to in the substitution

    * For example, if a job function receives an inputs of a list of 3:

        .. code-block:: python

            ["prev_task.1.ignore", 17, "prev_task.1.correct"]
            ["prev_task.2.ignore", 19, "prev_task.2.correct"]
            ["prev_task.2.ignore", 19, "prev_task.3.oops"   ]

        When we are refer to the 3rd file name in the list (``"{basename[2]}"``), Ruffus knows that
        the regular expression filter only applies to the third file.

        Ruffus sensibly will not go through your inputs filtering everything blindly (i.e. apply the regular expression to``*.ignore``)


        This works:

        .. code-block:: python
            :emphasize-lines: 3

            @transform( previous_task,
                        formatter(r".correct" ),            # formatter with optional regular expression
                        "{basename[2]}")                    # First file in list
            def test_transform_task(    infiles,
                                        outfile):
                pass


            # non matching input rejected:
            #["prev_task.2.ignore", 19, "prev_task.3.oops"   ]



        This produces no matches:

        .. code-block:: python
            :emphasize-lines: 3

            @transform( previous_task,
                        formatter(r".correct" ),            # formatter with optional regular expression
                        "{basename[0]}")                    # First file in list
            def test_transform_task(    infiles,
                                        outfile):
                pass



============================================================================================================================================================
8) Combinatorics (all vs. all decorators)`
============================================================================================================================================================

    * ``@product()``
    * ``@permutations(...)``
    * ``@combinations(...)``
    * ``@combinations_with_replacement(...)``
    * based on `itertools  <http://docs.python.org/2/library/itertools.html>`__
    * in optional ``combinatorics`` module
    * Only ``formatter([OPTIONAl_REGEX])`` provides the necessary flexibility to construct the output so ``suffix`` and ``regex`` are not supported


    * ``@product`` example: Cartesian product of inputs

        .. code-block:: python
            :emphasize-lines: 1,7,11,14

            @product(

                    # first list from wildcard: filter on *.bam
                    "*.a",
                    formatter( ".*/(?P<ID>\w+.bamfile).bam" ),

                    # second list from task "AToB"
                    AToB,
                    formatter(),

                    # output file
                    "{path[0][0]}/{base_name[0][0]}.{base_name[0][0]}.out",

                    # regular expression matches
                    "{path[0][0]}",       # extra: path for 1st input, 1st file
                    "{basename[0][1]}",   # extra: file name for 1st input, 2nd file
                    "{ID[1][2]}",         # extra: regular expression named capture group for 2nd input, 3rd file
                    )
            def product( infiles, outfile,
                        input_1__1st_path,
                        input_1__2nd_file_name,
                        input_2__3rd_file_match
                        ):
                print infiles, outfile


    * ``@permutations`` example

        .. code-block:: python
            :emphasize-lines: 3,7

            @permutations(

                    # Elements in a tuple come from a single list, so we only need one formatter
                    "*.a",
                    formatter( ".*/(?P<ID>\w+.bamfile).bam" ),

                    # k_length_tuples,
                    2,

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
10) ``pipeline_run(...)`` and exceptions
============================================================================================================================================================
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



********************************************************************
version 2.3
********************************************************************
    * ``@active_if`` turns off tasks at runtime
        The Design and initial implementation were contributed by Jacob Biesinger

        Takes one or more parameters which can be either booleans or functions or callable objects which return True / False::

                run_if_true_1 = True
                run_if_true_2 = False

                @active_if(run_if_true, lambda: return run_if_true_2)
                def this_task_might_be_inactive():
                    pass

        The expressions inside @active_if are evaluated each time
        ``pipeline_run``, ``pipeline_printout`` or ``pipeline_printout_graph`` is called.

        Dormant tasks behave as if they are up to date and have no output.

    * Command line parsing
        Supports both argparse (python 2.7) and optparse (python 2.6):
        The following options are defined by default::

                    --verbose
                    --version
                    --log_file

                -t, --target_tasks
                -j, --jobs
                -n, --just_print
                    --flowchart
                    --key_legend_in_graph
                    --draw_graph_horizontally
                    --flowchart_format
                    --forced_tasks

        Usage with argparse (Python > 2.7)::

                from ruffus import *

                parser = cmdline.get_argparse(   description='WHAT DOES THIS PIPELINE DO?')

                # for example...
                parser.add_argument("--input_file")

                options = parser.parse_args()

                #  optional logger which can be passed to ruffus tasks
                logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

                #_____________________________________________________________________________________
                #   pipelined functions go here
                #_____________________________________________________________________________________

                cmdline.run (options)

        Usage with optparse (Python 2.6)::

                from ruffus import *

                parser = cmdline.get_optgparse(version="%prog 1.0", usage = "\n\n    %prog [options]")

                # for example...
                parser.add_option("-c", "--custom", dest="custom", action="count")

                (options, remaining_args) = parser.parse_args()

                #  logger which can be passed to ruffus tasks
                logger, logger_mutex = cmdline.setup_logging ("this_program", options.log_file, options.verbose)

                #_____________________________________________________________________________________
                #   pipelined functions go here
                #_____________________________________________________________________________________

                cmdline.run (options)
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

    * Improved ``pipeline_printout()``

            * `@split` operations now show the 1->many output in pipeline_printout

                This make it clearer that ``@split`` is creating multiple output parameters (rather than a single output parameter consisting of a list)::

                        Task = split_animals
                             Job = [None
                                   -> cows
                                   -> horses
                                   -> pigs
                                    , any_extra_parameters]
            * File date and time are displayed in human readable form and out of date files are flagged with asterisks.



********************************************************************
version 2.2
********************************************************************
    * Simplifying **@transform** syntax with **suffix(...)**

        Regular expressions within ruffus are very powerful, and can allow files to be moved
        from one directory to another and renamed at will.

        However, using consistent file extensions and
        ``@transform(..., suffix(...))`` makes the code much simpler and easier to read.

        Previously, ``suffix(...)`` did not cooperate well with ``inputs(...)``.
        For example, finding the corresponding header file (".h") for the matching input
        required a complicated ``regex(...)`` regular expression and ``input(...)``. This simple case,
        e.g. matching "something.c" with "something.h", is now much easier in Ruffus.


        For example:
          ::

            source_files = ["something.c", "more_code.c"]
            @transform(source_files, suffix(".c"), add_inputs(r"\1.h", "common.h"), ".o")
            def compile(input_files, output_file):
                ( source_file,
                  header_file,
                  common_header) = input_files
                # call compiler to make object file

          This is equivalent to calling:

            ::

              compile(["something.c", "something.h", "common.h"], "something.o")
              compile(["more_code.c", "more_code.h", "common.h"], "more_code.o")

        The ``\1`` matches everything *but* the suffix and will be applied to both ``glob``\ s and file names.

    For simplicity and compatibility with previous versions, there is always an implied r"\1" before
    the output parameters. I.e. output parameters strings are *always* substituted.


    * Tasks and glob in **inputs(...)** and **add_inputs(...)**

        ``glob``\ s and tasks can be added as the prerequisites / input files using
        ``inputs(...)`` and ``add_inputs(...)``. ``glob`` expansions will take place when the task
        is run.

    * Advanced form of **@split** with **regex**:

        The standard ``@split`` divided one set of inputs into multiple outputs (the number of which
        can be determined at runtime).

        This is a ``one->many`` operation.


        An advanced form of ``@split`` has been added which can split each of several files further.

        In other words, this is a ``many->"many more"`` operation.

        For example, given three starting files:
            ::

                original_files = ["original_0.file",
                                  "original_1.file",
                                  "original_2.file"]
        We can split each into its own set of sub-sections:
            ::

                @split(original_files,
                   regex(r"starting_(\d+).fa"),                         # match starting files
                         r"files.split.\1.*.fa"                         # glob pattern
                         r"\1")                                         # index of original file
                def split_files(input_file, output_files, original_index):
                    """
                        Code to split each input_file
                            "original_0.file" -> "files.split.0.*.fa"
                            "original_1.file" -> "files.split.1.*.fa"
                            "original_2.file" -> "files.split.2.*.fa"
                    """


        This is, conceptually, the reverse of the @collate(...) decorator

    * Ruffus will complain about unescaped regular expression special characters:

        Ruffus uses "\1" and "\2" in regular expression substitutions. Even seasoned python
        users may not remember that these have to be 'escaped' in strings. The best option is
        to use 'raw' python strings e.g.

            ::

                r"\1_substitutes\2correctly\3four\4times"

        Ruffus will throw an exception if it sees an unescaped "\1" or "\2" in a file name,
        which should catch most of these bugs.

    * Prettier output from *pipeline_printout_graph*

        Changed to nicer colours, symbols etc. for a more professional look.
        @split and @merge tasks now look different from @transform.
        Colours, size and resolution are now fully customisable::

            pipeline_printout_graph( #...
                                     user_colour_scheme = {
                                                            "colour_scheme_index":1,
                                                            "Task to run"  : {"fillcolor":"blue"},
                                                             pipeline_name : "My flowchart",
                                                             size          : (11,8),
                                                             dpi           : 120)})

        An SVG bug in firefox has been worked around so that font size are displayed correctly.


********************************************************************
version 2.0.10
********************************************************************
    * **touch_files_only** option for **pipeline_run**

      When the pipeline runs, task functions will not be run. Instead, the output files for
      each job (in each task) will be ``touch``\ -ed if necessary.
      This can be useful for simulating a pipeline run so that all files look as
      if they are up-to-date.

      Caveats:

        * This may not work correctly where output files are only determined at runtime, e.g. with **@split**
        * Only the output from pipelined jobs which are currently out-of-date will be ``touch``\ -ed.
          In other words, the pipeline runs *as normal*, the only difference is that the
          output files are ``touch``\ -ed instead of being created by the python task functions
          which would otherwise have been called.

    * Parameter substitution for **inputs(...)**

      The **inputs(...)** parameter in **@transform**, **@collate** can now take tasks and ``glob`` s,
      and these will be expanded appropriately (after regular expression replacement).

      For example::

          @transform("dir/a.input", regex(r"(.*)\/(.+).input"),
                        inputs((r"\1/\2.other", r"\1/*.more")), r"elsewhere/\2.output")
          def task1(i, o):
            """
            Some pipeline task
            """

      Is equivalent to calling::

            task1(("dir/a.other", "dir/1.more", "dir/2.more"), "elsewhere/a.output")

      \

          Here::

                r"\1/*.more"

          is first converted to::

                r"dir/*.more"

          which matches::

                "dir/1.more"
                "dir/2.more"


********************************************************************
version 2.1.1
********************************************************************
    * **@transform(.., add_inputs(...))**
        ``add_inputs(...)`` allows the addition of extra input dependencies / parameters for each job.

        Unlike ``inputs(...)``, the original input parameter is retained:
            ::

                from ruffus import *
                @transform(["a.input", "b.input"], suffix(".input"), add_inputs("just.1.more","just.2.more"), ".output")
                def task(i, o):
                ""

        Produces:
            ::

                Job = [[a.input, just.1.more, just.2.more] ->a.output]
                Job = [[b.input, just.1.more, just.2.more] ->b.output]


        Like ``inputs``, ``add_inputs`` accepts strings, tasks and ``glob`` s
        This minor syntactic change promises add much clarity to Ruffus code.
        ``add_inputs()`` is available for ``@transform``, ``@collate`` and ``@split``


********************************************************************
version 2.1.0
********************************************************************
    * **@jobs_limit**
      Some tasks are resource intensive and too many jobs should not be run at the
      same time. Examples include disk intensive operations such as unzipping, or
      downloading from FTP sites.

      Adding::

          @jobs_limit(4)
          @transform(new_data_list, suffix(".big_data.gz"), ".big_data")
          def unzip(i, o):
            "unzip code goes here"

      would limit the unzip operation to 4 jobs at a time, even if the rest of the
      pipeline runs highly in parallel.

      (Thanks to R. Young for suggesting this.)



********************************************************************
version 2.0.9
********************************************************************

    * Better display of logging output
    * Advanced form of **@split**
      This is an experimental feature.

      Hitherto, **@split** only takes 1 set of input (tasks/files/``glob`` s) and split these
      into an indeterminate number of output.

          This is a one->many operation.

      Sometimes it is desirable to take multiple input files, and split each of them further.

          This is a many->many (more) operation.

      It is possible to hack something together using **@transform** but downstream tasks would not
      aware that each job in **@transform** produces multiple outputs (rather than one input,
      one output per job).

      The syntax looks like::

           @split(get_files, regex(r"(.+).original"), r"\1.*.split")
           def split_files(i, o):
                pass

      If ``get_files()`` returned ``A.original``, ``B.original`` and ``C.original``,
      ``split_files()`` might lead to the following operations::

            A.original
                    -> A.1.original
                    -> A.2.original
                    -> A.3.original
            B.original
                    -> B.1.original
                    -> B.2.original
            C.original
                    -> C.1.original
                    -> C.2.original
                    -> C.3.original
                    -> C.4.original
                    -> C.5.original

      Note that each input (``A/B/C.original``) can produce a number of output, the exact
      number of which does not have to be pre-determined.
      This is similar to **@split**

      Tasks following ``split_files`` will have ten inputs corresponding to each of the
      output from ``split_files``.

      If **@transform** was used instead of **@split**, then tasks following ``split_files``
      would only have 3 inputs.

********************************************************************
version 2.0.8
********************************************************************

    * File names can be in unicode
    * File systems with 1 second timestamp granularity no longer cause problems.

********************************************************************
version 2.0.2
********************************************************************

    * Much prettier /useful output from :ref:`pipeline_printout <pipeline_functions.pipeline_printout>`
    * New tutorial / manual



********************************************************************
version 2.0
********************************************************************
    * Revamped documentation:

        * Rewritten tutorial
        * Comprehensive manual
        * New syntax help

    * Major redesign. New decorators include

        * :ref:`@split <manual.split>`
        * :ref:`@transform <manual.transform>`
        * :ref:`@merge <manual.merge>`
        * :ref:`@collate <manual.collate>`

    * Major redesign. Decorator *inputs* can mix

        * Output from previous tasks
        * |glob|_ patterns e.g. ``*.txt``
        * Files names
        * Any other data type

********************************************************************
version 1.1.4
********************************************************************
    Tasks can get their input by automatically chaining to the output from one or more parent tasks using :ref:`@files_re <manual.files_re>`

********************************************************************
version 1.0.7
********************************************************************
    Added `proxy_logger` module for accessing a shared log across multiple jobs in different processes.

********************************************************************
version 1.0
********************************************************************

    Initial Release in Oxford

########################################
Fixed Bugs
########################################

    Full list at `"Latest Changes wiki entry" <http://code.google.com/p/ruffus/wiki/LatestChanges>`_
