.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: Up to date; Tutorial
    pair: Task completion; Tutorial
    pair: Exceptions; Tutorial
    pair: Interrupted Pipeline; Tutorial

.. _new_manual.checkpointing:

######################################################################################################
|new_manual.checkpointing.chapter_num|: Checkpointing: Interrupted Pipelines and Exceptions
######################################################################################################


.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`

.. note::

    Remember to look at the example code:

    * :ref:`new_manual.checkpointing.code`



***************************************
Overview
***************************************
    .. image:: ../../images/theoretical_pipeline_schematic.png
       :scale: 50

    Computational pipelines transform your data in stages until the final result is produced.

    By default, *Ruffus* uses file modification times for the **input** and **output** to determine
    whether each stage of a pipeline is up-to-date or not. But what happens when the task
    function is interrupted, whether from the command line or by error, half way through writing the output?

    In this case, the half-formed, truncated and corrupt **Output** file will look newer than its **Input** and hence up-to-date.


.. index::
    pair: Tutorial; interrupting tasks

.. _new_manual.interrupting_tasks:

***************************************
Interrupting tasks
***************************************
    Let us try with an example:

        .. code-block:: python
            :emphasize-lines: 20

            from ruffus import *
            import sys, time

            #   create initial files
            @originate(['job1.start'])
            def create_initial_files(output_file):
                with open(output_file, "w") as oo: pass


            #---------------------------------------------------------------
            #
            #   long task to interrupt
            #
            @transform(create_initial_files, suffix(".start"), ".output")
            def long_task(input_files, output_file):
                with open(output_file, "w") as ff:
                    ff.write("Unfinished...")
                    # sleep for 2 seconds here so you can interrupt me
                    sys.stderr.write("Job started. Press ^C to interrupt me now...\n")
                    time.sleep(2)
                    ff.write("\nFinished")
                    sys.stderr.write("Job completed.\n")


            #       Run
            pipeline_run([long_task])


    When this script runs, it pauses in the middle with this message::

        Job started. Press ^C to interrupt me now...

    If you interrupted the script by pressing Control-C at this point, you will see that ``job1.output`` contains only ``Unfinished...``.
    However, if you should rerun the interrupted pipeline again, Ruffus ignores the corrupt, incomplete file:

        .. code-block:: pycon

            >>> pipeline_run([long_task])
            Job started. Press ^C to interrupt me now...
            Job completed

    And if you had run ``pipeline_printout``:

        .. code-block:: pycon
            :emphasize-lines: 8

            >>> pipeline_printout(sys.stdout, [long_task], verbose=3)
            ________________________________________
            Tasks which will be run:

            Task = long_task
                   Job  = [job1.start
                         -> job1.output]
                     # Job needs update: Previous incomplete run leftover: [job1.output]


    We can see that *Ruffus* magically knows that the previous run was incomplete, and that ``job1.output`` is detritus that needs to be discarded.


.. _new_manual.logging_completed_jobs:

******************************************
Checkpointing: only log completed jobs
******************************************

    All is revealed if you were to look in the working directory. *Ruffus* has created a file called ``.ruffus_history.sqlite``.
    In this `SQLite  <https://sqlite.org/>`_ database, *Ruffus* logs only those files which are the result of a completed job,
    all other files are suspect.
    This file checkpoint database is a fail-safe, not a substitute for checking file modification times. If the **Input** or **Output** files are
    modified, the pipeline will rerun.

    By default, *Ruffus* saves only file timestamps to the SQLite database but you can also add a checksum of the pipeline task function body or parameters.
    This behaviour can be controlled by setting the ``checksum_level`` parameter
    in ``pipeline_run()``. For example, if you do not want to save any timestamps or checksums:

        .. code-block:: python

            pipeline_run(checksum_level = 0)

            CHECKSUM_FILE_TIMESTAMPS      = 0     # only rerun when the file timestamps are out of date (classic mode)
            CHECKSUM_HISTORY_TIMESTAMPS   = 1     # Default: also rerun when the history shows a job as being out of date
            CHECKSUM_FUNCTIONS            = 2     # also rerun when function body has changed
            CHECKSUM_FUNCTIONS_AND_PARAMS = 3     # also rerun when function parameters or function body change


    .. note::

        Checksums are calculated from the `pickled  <http://docs.python.org/2/library/pickle.html>`_ string for the function code and parameters.
        If pickling fails, Ruffus will degrade gracefully to saving just the timestamp in the SQLite database.

.. _new_manual.history_files_cannot_be_shared:

****************************************************************************
Do not share the same checkpoint file across for multiple pipelines!
****************************************************************************

    The name of the Ruffus python script is not saved in the checkpoint file along side timestamps and checksums.
    That means that you can rename your pipeline source code file without having to rerun the pipeline!
    The tradeoff is that if multiple pipelines are run from the same directory, and save their histories to the
    same SQlite database file, and if their file names overlap (all of these are bad ideas anyway!), this is
    bound to be a source of confusion.

    Luckily, the name and path of the checkpoint file can be also changed for each pipeline

.. _new_manual.changing_history_file_name:

****************************************************************************
Setting checkpoint file names
****************************************************************************

    .. warning::

        Some file systems do not appear to support SQLite at all:

        There are reports that SQLite databases have `file locking problems  <http://beets.radbox.org/blog/sqlite-nightmare.html>`_ on Lustre.

        The best solution would be to keep the SQLite database on an alternate compatible file system away from the working directory if possible.

============================================================================================================================================================
environment variable ``DEFAULT_RUFFUS_HISTORY_FILE``
============================================================================================================================================================

    The name of the checkpoint file is the value of the environment variable ``DEFAULT_RUFFUS_HISTORY_FILE``.

        export DEFAULT_RUFFUS_HISTORY_FILE=/some/where/.ruffus_history.sqlite

    This gives considerable flexibility, and allows a system-wide policy to be set so that all Ruffus checkpoint files are set logically to particular paths.

    .. note::

        It is your responsibility to make sure that the requisite destination directories for the checkpoint files exist beforehand!


    Where this is missing, the checkpoint file defaults to ``.ruffus_history.sqlite`` in your working directory


============================================================================================================================================================
Setting the checkpoint file name manually
============================================================================================================================================================

    This checkpoint file name can always be overridden as a parameter to Ruffus functions:

        .. code-block:: python

            pipeline_run(history_file = "XXX")
            pipeline_printout(history_file = "XXX")
            pipeline_printout_graph(history_file = "XXX")


    There is also built in support in ``Ruffus.cmdline``. So if you use this module, you can simply add to your command line:

        .. code-block:: bash

            # use a custom checkpoint file
            myscript --checksum_file_name .myscript.ruffus_history.sqlite

    This takes precedence over everything else.



****************************************************************************
Useful checkpoint file name policies ``DEFAULT_RUFFUS_HISTORY_FILE``
****************************************************************************

    If the pipeline script is called ``test/bin/scripts/run.me.py``, then these are the resulting checkpoint files locations:

============================================================================================================================================================
Example 1: same directory, different name
============================================================================================================================================================
    If the environment variable is:

    .. code-block:: bash

        export DEFAULT_RUFFUS_HISTORY_FILE=.{basename}.ruffus_history.sqlite

    Then the job checkpoint database for ``run.me.py`` will be ``.run.me.ruffus_history.sqlite``

    .. code-block:: bash

        /test/bin/scripts/run.me.py
        /common/path/for/job_history/scripts/.run.me.ruffus_history.sqlite

============================================================================================================================================================
Example 2: Different directory, same name
============================================================================================================================================================

    .. code-block:: bash

        export DEFAULT_RUFFUS_HISTORY_FILE=/common/path/for/job_history/.{basename}.ruffus_history.sqlite

    .. code-block:: bash

        /common/path/for/job_history/.run.me.ruffus_history.sqlite


============================================================================================================================================================
Example 2: Different directory, same name but keep one level of subdirectory to disambiguate
============================================================================================================================================================

    .. code-block:: bash

        export DEFAULT_RUFFUS_HISTORY_FILE=/common/path/for/job_history/{subdir[0]}/.{basename}.ruffus_history.sqlite


    .. code-block:: bash

        /common/path/for/job_history/scripts/.run.me.ruffus_history.sqlite



============================================================================================================================================================
Example 2: nested in common directory
============================================================================================================================================================

    .. code-block:: bash

        export DEFAULT_RUFFUS_HISTORY_FILE=/common/path/for/job_history/{path}/.{basename}.ruffus_history.sqlite

    .. code-block:: bash

        /common/path/for/job_history/test/bin/scripts/.run.me.ruffus_history.sqlite




.. index::
    pair: Tutorial; Regenerating the checkpoint file

.. _new_manual.regenerating_history_file:

******************************************************************************
Regenerating the checkpoint file
******************************************************************************

    Occasionally you may need to re-generate the checkpoint file.

    This could be necessary:

        * because you are upgrading from a previous version of Ruffus without checkpoint file support
        * on the rare occasions when the SQLite file becomes corrupted and has to deleted
        * if you wish to circumvent the file checking of Ruffus after making some manual changes!

    To do this, it is only necessary to call ``pipeline_run`` appropriately:

        .. code-block:: python

            CHECKSUM_REGENERATE = 2
            pipeline(touch_files_only = CHECKSUM_REGENERATE)


    Similarly, if you are using ``Ruffus.cmdline``, you can call:

        .. code-block:: bash

            myscript --recreate_database


    Note that this regenerates the checkpoint file to reflect the existing *Input*, *Output* files on disk.
    In other words, the onus is on you to make sure there are no half-formed, corrupt files. On the other hand,
    the pipeline does not need to have been previously run successfully for this to work. Essentially, Ruffus,
    pretends to run the pipeline, while logging all the files with consistent file modication times, stopping
    at the first tasks which appear out of date or incomplete.


.. index::
    pair: rules; for rerunning jobs

.. _new_manual.skip_up_to_date.rules:

******************************************************************************
Rules for determining if files are up to date
******************************************************************************
    The following simple rules are used by *Ruffus*.

    #. The pipeline stage will be rerun if:

        * If any of the **Input** files are new (newer than the **Output** files)
        * If any of the **Output** files are missing

    #. In addition, it is possible to run jobs which create files from scratch.

        * If no **Input** file names are supplied, the job will only run if any *output* file is missing.

    #. Finally, if no **Output** file names are supplied, the job will always run.



.. index::
    pair: Exception; Missing input files

******************************************************************************
Missing files generate exceptions
******************************************************************************

    If the *inputs* files for a job are missing, the task function will have no way
    to produce its *output*. In this case, a ``MissingInputFileError`` exception will be raised
    automatically. For example,

        ::

            task.MissingInputFileError: No way to run job: Input file ['a.1'] does not exist
            for Job = ["a.1" -> "a.2", "A file"]

.. index::
    pair: Manual; Timestamp resolution

******************************************************************************
Caveats: Coarse Timestamp resolution
******************************************************************************

    Note that modification times have precision to the nearest second under some older file systems
    (ext2/ext3?). This may be also be true for networked file systems.

    *Ruffus* supplements the file system time resolution by independently recording the timestamp at
    full OS resolution (usually to at least the millisecond) at job completion, when presumably the **Output**
    files will have been created.

    However, *Ruffus* only does this if the discrepancy between file time and system time is less than a second
    (due to poor file system timestamp resolution). If there are large mismatches between the two, due for example
    to network time slippage, misconfiguration etc, *Ruffus* reverts to using the file system time and adds a one second
    delay between jobs (via ``time.sleep()``) to make sure input and output file stamps are different.

    If you know that your filesystem has coarse-grained timestamp resolution, you can always revert to this very conservative behaviour,
    at the prices of some annoying 1s pauses, by setting :ref:`pipeline_run(one_second_per_job = True) <pipeline_functions.pipeline_run>`



.. index::
    pair: Manual; flag files

******************************************************************************
Flag files: Checkpointing for the paranoid
******************************************************************************

    One other way of checkpointing your pipelines is to create an extra "flag" file as an additional
    **Output** file name. The flag file is only created or updated when everything else in the
    job has completed successifully and written to disk. A missing or out of date flag file then
    would be a sign for Ruffus that the task never completed properly in the first place.

    This used to be much the best way of performing checkpointing in Ruffus and is still
    the most bulletproof way of proceeding. For example, even the loss or corruption
    of the checkpoint file, would not affect things greatly.

    Nevertheless flag files are largely superfluous in modern *Ruffus*.
