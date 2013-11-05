.. include:: global.inc
########################################
Major Features added to Ruffus 
########################################

********************************************************************
version 1.0
********************************************************************

    Initial Release in Oxford       

********************************************************************
version 1.0.7
********************************************************************
    Added `proxy_logger` module for accessing a shared log across multiple jobs in different processes.

                                                                                   
********************************************************************
version 1.1.4
********************************************************************
    Tasks can get their input by automatically chaining to the output from one or more parent tasks using :ref:`@files_re <manual.files_re>`

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
version 2.0.2
********************************************************************

    * Much prettier /useful output from :ref:`pipeline_printout <pipeline_functions.pipeline_printout>`
    * New tutorial / manual

********************************************************************
version 2.0.8
********************************************************************

    * File names can be in unicode
    * File systems with 1 second timestamp granularity no longer cause problems.

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




########################################
Fixed Bugs
########################################

    Full list at `"Latest Changes wiki entry" <http://code.google.com/p/ruffus/wiki/LatestChanges>`_
