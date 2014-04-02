##########################################
In progress: Refactoring Ruffus Docs
##########################################

    Remember to cite Jake Biesinger and see if he is interested to be a co-author if we ever resubmit the drastically changed version...


***************************************
New order of Topics in the tutorial
***************************************
    * final_task
    * pipeline_run touch mode


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


