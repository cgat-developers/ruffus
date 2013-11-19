##########################################
In progress: Refactoring Ruffus Docs
##########################################

    Remember to cite Jake Biesinger and see if he is interested to be a co-author if we ever resubmit the drastically changed version...

***************************************
Best Practices
***************************************

***************************************
Removing references to "legacy" methods
***************************************

    e.g., @files


***************************************
Reusing pipeline code in modules
***************************************

***************************************
New features
***************************************
==============================================================================
@subdivide / @split(..., regex(), ...)
==============================================================================
    synonym for @split

==============================================================================
formatter
==============================================================================

    with regular expression or not

==============================================================================
@product
==============================================================================

    with formatter()

==============================================================================
@permutations
==============================================================================

    with formatter()

==============================================================================
@combinations
==============================================================================

    with formatter()

==============================================================================
@combinations_with_replacement
==============================================================================

    with formatter()

==============================================================================
@active_if
==============================================================================


==============================================================================
task completion monitoring
==============================================================================

    Jake Biesinger

==============================================================================
command line
==============================================================================

    new minimal code template

==============================================================================
drmaa
==============================================================================

***************************************
git hub docs
***************************************




##########################################
In progress: Refactoring Ruffus
##########################################


***************************************
Custom parameter generator
***************************************

    Leverages built-in Ruffus functionality.
    Don't have to write entire parameter generation from scratch.

    * Gets passed an iterator where you can do a for loop to get input parameters / a flattened list of files
    * Other parameters are forwarded as is
    * The duty of the function is to ``yield`` input, output, extra parameters

***************************************
@mkdir with regex
***************************************


***************************************
Task completion monitoring
***************************************

    * On by default?
    * Can we query the database, get Job history / stats
    * What are the run time performance implications?
    * Can we get rid of the minimum 1 second delay between jobs now? Does the database have finer granularity in timestamps? Can we use the database timestamps provided they are *later* than the filesystem ones. They must be if we are recording them *after* the job succeeds.
    * Can we log this dispatch / completion timestamps to the same database?
    * How easy is it to abstract out the database?
    * How resistant is it to corruption?

************************************************************************************************
@subdivide
************************************************************************************************

    * needs test code
    * needs test scripts



**************************************************
Running python jobs remotely on cluster nodes
**************************************************

    abstract out ``task.run_pooled_job_without_exceptions()`` as a function which can be supplied to
        pipeline_run

    Common "job" interface:

         *  marshalled arguments
         *  marshalled function
         *  submission timestamp

    Returns
         *  completion timestamp
         *  returned values
         *  exception

    #) Full version use libpythongrid
       * Christian Widmer <ckwidmer@gmail.com>
       * Cheng Soon Ong <chengsoon.ong@unimelb.edu.au>
       * https://code.google.com/p/pythongrid/source/browse/#git%2Fpythongrid
       * Probably not good to base Ruffus entirely on libpythongrid to minimise dependencies, their more sophisticated configuration policies etc. and to abstract out commonalities.
    #) Start with light-weight file-based protocol
       * both drmaa and this needs specified local and remote directories
       * use drmaa to start jobs
       * have executable module which knows how to load deserialise (unmarshall) function / parameters from disk
       * time stamp
       * "heart beat"
    #) Next step: pipe-based protocol
       * use specified master port
       * child is handed port in start up code to initiate hand shake or die
       * start remote processes using drmaa
       * process recycling: run successive jobs on the same remote process for reduced overhead, until exceeds max number of jobs on the same process, min/max time on the same process
       * resubmit if die (Don't do sophisticated stuff like libpythongrid).

##########################################
Planned: Refactoring Ruffus
##########################################

***************************************
New decorators
***************************************
==============================================================================
How to:
==============================================================================


    New placeholder class. E.g. for @new_deco

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



==============================================================================
@split / @subdivide
==============================================================================

    yielding file names


==============================================================================
@generate
==============================================================================

    @split ex nihilo


==============================================================================
@recombine
==============================================================================

    regroups previously @subdivide-d jobs **providing** that the output file names
    were returned from the function


***************************************
job trickling
***************************************

    * @recombine is the necessary step, otherwise all @split @merge end in a stall and we might as well not bother...
    * depth first etc iteration of tree
    * Jobs need unique job_id tag
    * Need a way of generating filenames without returning from a function
      indefinitely: i.e. a generator
    * Need a way of knowing which files group together (i.e. were split
      from a common job) without using regex (magic @split and @remerge)
    * @split needs to be able to specify at run time the number of
      resulting jobs without using wild cards
    * @merge needs to know when all of a group of files have completed
    * legacy support for wild cards and file names.
    * Possible breaking change: Assumes an explicit @follows if require
      *all* jobs from the previous task to finish
    * "Push" system of checking in completed jobs into "slots" of waiting
      tasks
    * New jobs dispatched when slots filled adequately
    * Funny "single file" mode for @transform, @files needs to be
      regularised so it is a syntactic (front end) convenience (oddity!)
      and not plague the inards of ruffus
    * use named parameters in decorators for clarity?






******************************************************************************
    Ruffus GUI interface.
******************************************************************************

    Desktop (PyQT or web-based solution?)  I'd love to see an svg pipeline picture that I could actually interact with




******************************************************************************
Extending graphviz output
******************************************************************************



***************************************
Deleting intermediate files
***************************************
==============================================================================
Bernie Pope hack: truncate file to zero, preserving modification times
==============================================================================

    .. code-block:: python

        def zeroFile(file):
            if os.path.exists(file):
                # save the current time of the file
                timeInfo = os.stat(file)
                try:
                    f = open(file,'w')
                except IOError:
                    pass
                else:
                    f.truncate(0)
                    f.close()
                    # change the time of the file back to what it was
                    os.utime(file,(timeInfo.st_atime, timeInfo.st_mtime))


##########################################
Completed: Refactoring Ruffus Docs
##########################################

##########################################
Completed: Refactoring Ruffus
##########################################

***************************************
drmaa
***************************************

    Implemented in drmaa_wrapper.py

    Alternative, non-drmaa polling code at

    https://github.com/bjpop/rubra/blob/master/rubra/cluster_job.py

    Probably not necessary surely.

******************************************************************************
New flexible "format" alternative to regex suffix
******************************************************************************


    ``get_all_paths_components(paths, regex_str)`` in ``ruffus_utility.py``

    If ``regex_str`` is not None, then regular expression match failures will return an empty dictionary.
    The idea is that all file names which throw exceptions will be skipped, and we can continue
    to use regular expression matches as a filter, even if they are not used to construct the result.
    Note that the regular expression is applied to *all* file names in case *any* of them is used in
    format string. So regular expression matches only failures for the file referenced in the format pattern.

    For example,

    .. code-block:: python

        # filter on ".txt"
        input_filenames = ["a.wrong", "b.txt"]
        formatter(".txt$")

        # OK: regular expression matches the second file name
        "{basename[1]}"

        # Failures: regular expression does not match the second file name. No format substitutions make sense
        "{basename[1]}"


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

    .. code-block:: python

        results = get_all_paths_components(paths, regex_str)
        string.format(results[2])


    .. code-block:: python


        class t_suffix_filename_transform(t_filename_transform):
        class t_regex_filename_transform(t_filename_transform):
        class t_format_filename_transform(t_filename_transform):

    ... contains both the regular expression string and the code to make output / extra parameters from
    the input files.
    Suffix and Regex only use the first file name in the input.
    Formatter is more flexible and can use any file names in the input.

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

    Formatter takes these results and adds a level of indirection for each level of nesting.
    In the case of @transform, @collate, we are dealing with a list of input files per job, so typically,
    the components with be, using python format syntax::

        input_file_names = ['/a/b/c/sample1.bam']
        formatter(r"(.*)(?P<id>\d+)\.(.+)")

        "{0[0]}"            #   '/a/b/c/sample1.bam',           // Entire match captured by index
        "{1[0]}"            #   '/a/b/c/sample',                // captured by index
        "{2[0]}"            #   'bam',                          // captured by index
        "{id[0]}"           #   '1'                             // captured by name
        "{ext[0]}"          #   '.bam',
        "{subdir[0][0]}"    #   'c'
        "{subpath[0][1]}"   #   '/a/b'
        "{path[0]}"         #   '/a/b/c',
        "{basename[0]}"     #   'sample1',


    The only trickiness is that string.format() understands all integer number keys to be offsets into lists/ tuples and everything else
    including negative numbers to be dict keys.

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


***************************************
Task completion monitoring
***************************************

    * Jake Biesinger has done this already.
    * Fantastic code. Checked in.


***************************************
@product()
***************************************

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

    Similar to @transform but with extra level of nested-ness

    Retain same code for @product and @transform by adding an additional level of indirection:
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






******************************************************************************
@permutations(...), @combinations(...), @combinations_with_replacement(...)
******************************************************************************

    * Put all new generators in an ``combinatorics`` submodule namespace to avoid breaking user code. (They can import if necessary.)
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

    Similar to @product extra level of nested-ness is self versus self

    Retain same code for @product
        * forward to a sinble ``file_name_parameters.combinatorics_param_factory()``
        * use ``combinatorics_type`` to dispatch to ``combinatorics.permutations``, ``combinatorics.combinations`` and ``combinatorics.combinations_with_replacement``
        * use ``list_input_param_to_file_name_list`` from ``file_name_parameters.product_param_factory()``


******************************************************************************
Better error messages for formatter, suffix and regex
******************************************************************************

    * Error messages for pipeline_printout if verbose >= 3 showing mismatching regular expression and offending file name
    * Wrong capture group names or out of range indices will raise informative Exception
    * regex() and suffix() examples in ``test/test_regex_error_messages.py``
    * formatter() examples in ``test/test_combinatorics.py``
