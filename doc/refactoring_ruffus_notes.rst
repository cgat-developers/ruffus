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
file_name_parameters.py
******************************************************************************

    t_params_tasks_globs_run_time_data.regex_replaced()
        only does a regex replacement of the globs and raw strings, not tasks
    Used in:

    @split_ex
        extra_input, then file_names_from_tasks_globs()
        output_param, file_names_from_tasks_globs , unexpanded_globs()
    @transform
        extra_input, then file_names_from_tasks_globs()
    @collate
        extra_input, then file_names_from_tasks_globs()



******************************************************************************
New flexible "format" alternative to regex suffix
******************************************************************************

    ``get_all_paths_components(paths, regex_str)`` in ``ruffus_utility.py``

    If ``regex_str`` is not None, then regular expression match failures will return an empty dictionary.

    .. code-block:: python

        results = get_all_paths_components(paths, regex_str)
        string.format(results[2])

    will fail (raise and Exception)

    The idea is that all file names which throw exceptions will be skipped, and we can continue
    to use regular expression matches as a filter, even if they are not used to construct the result.


    .. code-block:: python


        class t_suffix_filename_transform(t_filename_transform):
        class t_regex_filename_transform(t_filename_transform):
        class t_format_filename_transform(t_filename_transform):

        contains both the regular expression string and the code to construct




***************************************
New decorators
***************************************
==============================================================================
@split
==============================================================================

    returning files

==============================================================================
@generate
==============================================================================

    @split ex nihilo

==============================================================================
@product
==============================================================================

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
@permute @combination
==============================================================================

==============================================================================
@stagger
==============================================================================

    Prevent jobs all launching at the same time?

==============================================================================
@mkdir with regex
==============================================================================

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




