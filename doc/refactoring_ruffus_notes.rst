##########################################
In progress: Refactoring Ruffus Docs
##########################################

    Remember to cite Jake Biesinger and see if he is interested to be a co-author if we ever resubmit the drastically changed version...



##########################################
Future / Planned Improvements to  Ruffus
##########################################

********************************************************************************************************
Todo: Bioinformatics example to end all examples
********************************************************************************************************

    Uses
        * @product
        * @subdivide
        * @transform
        * @collate
        * @merge

********************************************************************************************************
Todo: Running python code (task functions) transparently on remote cluster nodes
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


********************************************************************************************************
Mark input strings as non-file names, and add support for dynamically returned parameters
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


********************************************************************************************************
Allow "extra" parameters to be used in output substitution
********************************************************************************************************

    Formatter substitution can refer to the original elements in the input and extra parameters (without converting them to strings either). This refers to the original (nested) data structure.

    This will allow normal python datatypes to be handed down and slipstreamed into a pipeline more easily.

    The syntax would use Ruffus (> version 2.4) formatter:

    ::

        @transform( ..., formatter(), ["{EXTRAS[0][1][3]}", "[INPUTS[1][2]]"],...)

    EXTRA and INPUTS indicate that we are referring to the input and extra parameters.

    These are the full (nested) parameters in all their original form. In the case of the input parameters, this obvious depends on the decorator, so

    ::

        @transform(["a.text", [1, "b.text"]], formatter(), "{INPUTS[0][0]}")

    would give

    ::

        job #1
           input  == "a.text"
           output == "a"

        job #2
           input  == [1, "b.text"]
           output == 1


    The entire string must consist of INPUTS or EXTRAS followed by optionally N levels of square brackets. i.e. They must match "(INPUTS|EXTRAS)(\[\d+\])+"

    No string conversion takes place.


********************************************************************************************************
Refactor verbosity levels
********************************************************************************************************

    Verbosity levels for pipeline_printout and pipeline_run do not seem to be synchronised. It is not clear what exactly increasing verbosity does at each level. What is more, different things seem to happen differently at run time and print_out.

        verbosity=

        1) Out-of-date Tasks
        2) All Tasks
        3) Out-of-date Jobs in Out-of-date Tasks
        4) All Jobs in Out-of-date Tasks
        5) All jobs in All Tasks whether out of date or not

        path_verbosity =

        (default = 2)

        0) the full path
        1-N) N levels of subpath,

            for "what/is/this.txt"
            N = 1 "this.txt"
            N = 2 "is/this.txt"
            N >=3 "what/is/this.txt"

        -N) As above but with the input/output parameter chopped off after 40 letters, and ending in "..."

        Getting the Nth levels of a path use code from ruffus.ruffus_utility

        ::

            from ruffus.ruffus_utility import *
            for aa in range(10):
               print get_nth_nested_level_of_path ("/test/this/now/or/not.txt", aa)

        1) pipeline_printout forwards printing to _task.printout
        2) pipeline_run needs to borrow code from pipeline_printout to print up to date tasks including their jobs
        3) See file_name_parameters.py::get_readable_path_str()



***************************************
New decorators
***************************************
==============================================================================
Planned: ``@split`` / ``@subdivide``
==============================================================================

    Can't see how we can stop using wild cards but at least if we return output strings in the task functions, we
    don't include extraneous files which were not created in the pipeline but which just happened to match the
    wild card in the function.

    We should check whether we have ever run the function before, and if we have to also only check the files
    which we generated last time...


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


