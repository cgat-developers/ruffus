##########################################
In progress: Refactoring Ruffus Docs
##########################################

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
@split
==============================================================================

    with regex

==============================================================================
@active_if
==============================================================================

    with regex

==============================================================================
task completion monitoring
==============================================================================

==============================================================================
command line
==============================================================================

    new minimal code template

***************************************
git hub docs
***************************************




##########################################
In progress: Refactoring Ruffus
##########################################
******************************************************************************
New flexible "format" alternative to regex suffix
******************************************************************************


    ``get_all_paths_components(paths, regex_str)`` in ``ruffus_utility.py``

    If ``regex_str`` is not None, then regular expression match failures will return an empty dictionary.
    The idea is that all file names which throw exceptions will be skipped, and we can continue
    to use regular expression matches as a filter, even if they are not used to construct the result.
    The same is now true for regex matches

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
New decorators
***************************************
==============================================================================
To do:
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


============================================================================================================================================================
@product() / @permutations/ @combinations() / @combinations_with_replacement
============================================================================================================================================================

    Final syntax:

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
    * Put all new generators in an itertools submodule namespace to avoid breaking user code. (They can import if necessary.)
    * The ``itertools.product(repeat)`` parameter doesn't make sense for Ruffus and will not be used
    * The length of combinations and permutations needs to be specified
    * Adds one level of nesting to normal @transform 
    * ``ruffus_uilility.swap_doubly_nested_order()`` makes the syntax / implementation very orthogonal

            
        


    Andreas syntax:

    .. code-block:: python

        @product( "*.a", AToB,
              regex( "(.*).a" ),
              regex( "(.*).b" ),
              "%1_vs_%2.out" )
        def product( infiles, outfile ):
            print infiles, outfile


    Jake syntax:

    .. code-block:: python


        @product( "*.a",
                regex( "(.*).a" ),
                AToB,
                regex( "(.*).b" ),
                ...
                "???,out" )
        def product( infiles, outfile ):
            print infiles, outfile




==============================================================================
@subdivide
==============================================================================

    synonym for @split_ex

==============================================================================
@mkdir with regex
==============================================================================


==============================================================================
@split
==============================================================================

    yielding file names


==============================================================================
@generate
==============================================================================

    @split ex nihilo


==============================================================================
@recombine
==============================================================================

    regroups previously subdivided / split jobs **providing** that the output file names
    were returned from the function

***************************************
Custom parameter generator
***************************************

    * Which leverages some of the current functionality. Don't have to
        write entire parameter generation from scratch?

    * Add customisation point?

***************************************
Task completion monitoring
***************************************

    * Jake has done this already.
    * Fantastic code. Checked in.
    * Get Job history / stats

***************************************
job trickling
***************************************

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



***************************************
drmaa
***************************************

    Implemented in drmaa_wrapper.py

    Alternative, non-drmaa polling code at

    https://github.com/bjpop/rubra/blob/master/rubra/cluster_job.py

    Probably not necessary surely.


***************************************
Running python on nodes
***************************************
    Common "job" interface:

         *  marshalled arguments
         *  marshalled function
         *  timestamp
         *  return
         *  exception

    #) Use libpythongrid
       Too customised?
       https://code.google.com/p/pythongrid/source/browse/#git%2Fpythongrid
    #) file-based invocation
       * needs common directory
    #) Light weight version of python grid needs
       #) "heart beat"
       #) time stamp
       #) process recycling: max number of jobs, min/max time
       #) resubmit
       #) port?


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




