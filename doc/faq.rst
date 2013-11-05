.. include:: global.inc
******
FAQ
******

^^^^^^^^^^^^^^^^^
Citations
^^^^^^^^^^^^^^^^^

=============================================================
Q. How should *Ruffus* be cited in academic publications?
=============================================================

    The official publication describing the original version of *Ruffus* is:

        `Leo Goodstadt (2010) <http://bioinformatics.oxfordjournals.org/content/early/2010/09/16/bioinformatics.btq524>`_ : **Ruffus: a lightweight Python library for computational pipelines.** *Bioinformatics* 26(21): 2778-2779



^^^^^^^^^^^^^^^^^
General
^^^^^^^^^^^^^^^^^

=========================================================
Q. *Ruffus* won't create dependency graphs
=========================================================

    A. You need to have installed ``dot`` from `Graphviz <http://www.graphviz.org/>`_ to produce
    pretty flowcharts likes this:

            .. image:: images/pretty_flowchart.png







=========================================================
Q. *Ruffus* seems to be hanging in the same place
=========================================================

    A. If *ruffus* is interrupted, for example, by a Ctrl-C,
    you will often find the following lines of code highlighted::

        File "build/bdist.linux-x86_64/egg/ruffus/task.py", line 1904, in pipeline_run
        File "build/bdist.linux-x86_64/egg/ruffus/task.py", line 1380, in run_all_jobs_in_task
        File "/xxxx/python2.6/multiprocessing/pool.py", line 507, in next
          self._cond.wait(timeout)
        File "/xxxxx/python2.6/threading.py", line 237, in wait
          waiter.acquire()

    This is *not* where *ruffus* is hanging but the boundary between the main programme process
    and the sub-processes which run *ruffus* jobs in parallel.

    This is naturally where broken execution threads get washed up onto.




=========================================================
Q. Regular expression substitutions don't work
=========================================================

    A. If you are using the special regular expression forms ``"\1"``, ``"\2"`` etc.
    to refer to matching groups, remember to 'escape' the subsitution pattern string.
    The best option is to use `'raw' python strings <http://docs.python.org/library/re.html>`_.
    For example:

        ::

            r"\1_substitutes\2correctly\3four\4times"

    Ruffus will throw an exception if it sees an unescaped ``"\1"`` or ``"\2"`` in a file name.


======================================================================================
Q. How to use decorated functions in Ruffus
======================================================================================
    A. Place your decorator after *Ruffus* decorators. This ensures that by the time *Ruffus* sees
    your function, it has already been decorated.

        ::

            @transform(["example.abc"], suffix(".abc"), ".xyz")
            @custom_decoration
            def func(input, output):
                pass

    You will also need to use either ``@wraps`` or ``update_wrapper`` from ``functools``
    to write your decorator:

        ::

            def custom(task_func):
                """ Decorate a function to print progress
                """
                @wraps(task_func)
                def wrapper_function(*args, **kwargs):
                    print "Before"
                    task_func(*args, **kwargs)
                    print "After"

                return wrapper_function

    This ensures that the ``__name__`` and ``__module__`` attributes from the task function
    are made available to *Ruffus* via your decorator.


======================================================================================
Q. Can a task function in a *Ruffus* pipeline be called normally outside of Ruffus?
======================================================================================
    A. Yes. Most python decorators wrap themselves around a function. However, *Ruffus* leaves the
    original function untouched and unwrapped. Instead, *Ruffus* adds a ``pipeline_task`` attribute
    to the task function to signal that this is a pipelined function.

    This means the original task function can be called just like any other python function.

======================================================================================
Q. My tasks creates two files but why does only one survive in the *Ruffus* pipeline?
======================================================================================
    ::

        from ruffus import *
        import sys
        @transform("start.input", regex(".+"), ("first_output.txt", "second_output.txt"))
        def task1(i,o):
            pass

        @transform(task1, suffix(".txt"), ".result")
        def task2(i, o):
            pass

        pipeline_printout(sys.stdout, [task2], verbose=3)

    ::

        ________________________________________
        Tasks which will be run:

        Task = task1
               Job = [start.input
                     ->[first_output.txt, second_output.txt]]

        Task = task2
               Job = [[first_output.txt, second_output.txt]
                     ->first_output.result]

        ________________________________________

    A: This code produces a single output of a tuple of 2 files. In fact, you want two
    outputs, each consisting of 1 file.

    You want a single job (single input) to be produce multiple outputs (multiple jobs
    in downstream tasks). This is a one-to-many operation which calls for
    :ref:`@split <decorators.split>`:

        ::

            from ruffus import *
            import sys
            @split("start.input", ("first_output.txt", "second_output.txt"))
            def task1(i,o):
                pass

            @transform(task1, suffix(".txt"), ".result")
            def task2(i, o):
                pass

            pipeline_printout(sys.stdout, [task2], verbose=3)

        ::

            ________________________________________
            Tasks which will be run:

            Task = task1
                   Job = [start.input
                         ->[first_output.txt, second_output.txt]]

            Task = task2
                   Job = [first_output.txt
                         ->first_output.result]
                   Job = [second_output.txt
                         ->second_output.result]

            ________________________________________


======================================================================================
Q. How can a *Ruffus* task produce output which goes off in different directions?
======================================================================================
    A. As above, anytime there is a situation which requires a one-to-many operation, you should reach
    for :ref:`@split <decorators.split_ex>`. The advanced form takes a regular expression, making
    it easier to produce multiple derivatives of the input file. The following example splits
    *2* jobs each into *3*, so that the subsequence task will run *2* x *3* = *6* jobs.

        ::

            from ruffus import *
            import sys
            @split(["1.input_file",
                    "2.input_file"],
                    regex(r"(.+).input_file"),      # match file prefix
                   [r"\1.file_type1",
                    r"\1.file_type2",
                    r"\1.file_type3"])
            def split_task(input, output):
               pass


            @transform(split_task, regex("(.+)"), r"\1.test")
            def test_split_output(i, o):
               pass

            pipeline_printout(sys.stdout, [test_split_output], verbose = 3)

        Each of the original 2 files have been split in three so that test_split_output will run
        6 jobs simultaneously.

            ::

                ________________________________________
                Tasks which will be run:

                Task = split_task
                       Job = [1.input_file ->[1.file_type1, 1.file_type2, 1.file_type3]]
                       Job = [2.input_file ->[2.file_type1, 2.file_type2, 2.file_type3]]

                Task = test_split_output
                       Job = [1.file_type1 ->1.file_type1.test]
                       Job = [1.file_type2 ->1.file_type2.test]
                       Job = [1.file_type3 ->1.file_type3.test]
                       Job = [2.file_type1 ->2.file_type1.test]
                       Job = [2.file_type2 ->2.file_type2.test]
                       Job = [2.file_type3 ->2.file_type3.test]
                ________________________________________



======================================================================================
Q. Can I call extra code before each job?
======================================================================================
    A. This is easily accomplished by hijacking the process
    for checking if jobs are up to date or not (:ref:`@check_if_uptodate <decorators.check_if_uptodate>`):

        ::

            from ruffus import *
            import sys

            def run_this_before_each_job (*args):
                print "Calling function before each job using these args", args
                # Remember to delegate to the default *Ruffus* code for checking if
                #   jobs need to run.
                return needs_update_check_modify_time(*args)

            @check_if_uptodate(run_this_before_each_job)
            @files([[None, "a.1"], [None, "b.1"]])
            def task_func(input, output):
                pass

            pipeline_printout(sys.stdout, [task_func])

        This results in:
        ::

            ________________________________________
            >>> pipeline_run([task_func])
            Calling function before each job using these args (None, 'a.1')
            Calling function before each job using these args (None, 'a.1')
            Calling function before each job using these args (None, 'b.1')
                Job = [None -> a.1] completed
                Job = [None -> b.1] completed
            Completed Task = task_func

        .. note::

            Because ``run_this_before_each_job(...)`` is called whenever *Ruffus* checks to see if
            a job is up to date or not, the function may be called twice for some jobs
            (e.g. ``(None, 'a.1')`` above).


=========================================================================================================
Q. Does *Ruffus* allow checkpointing: to distinguish interrupted and completed results?
=========================================================================================================

_____________________________________________________
A. Use a flag file
_____________________________________________________

    (Thanks to Bernie Pope for sorting this out.)

    A. When gmake is interrupted, it will delete the target file it is updating so that the target is
    remade from scratch when make is next run.

    There is no direct support for this in *ruffus* **yet**. In any case, the partial / incomplete
    file may be usefully if only to reveal, for example, what might have caused an interrupting error
    or exception.

    A common *Ruffus* convention is create an empty checkpoint or "flag" file whose sole purpose
    is to record a modification-time and the successful completion of a job.

    This would be task with a completion flag:

    ::

        #
        #   Assuming a pipelined task function named "stage1"
        #
        @transform(stage1, suffix(".stage1"), [".stage2", ".stage2_finished"] )
        def stage2 (input_files, output_files):
            task_output_file, flag_file = output_files
            cmd = ("do_something2 %(input_file)s >| %(task_output_file)s ")
            cmd = cmd % {
                            "input_file":               input_files[0],
                            "task_output_file":         task_output_file
                        }
            if not os.system( cmd ):
                #88888888888888888888888888888888888888888888888888888888888888888888888888888
                #
                #   It worked: Create completion flag_file
                #
                open(flag_file, "w")
                #
                #88888888888888888888888888888888888888888888888888888888888888888888888888888


    The flag_files ``xxx.stage2_finished`` indicate that each job is finished. If this is missing,
    ``xxx.stage2`` is only a partial, interrupted result.


    The only thing to be aware of is that the flag file will appear in the list of inputs of the
    downstream task, which should accordingly look like this:


    ::

        @transform(stage2, suffix(".stage2"), [".stage3", ".stage3_finished"] )
        def stage3 (input_files, output_files):

            #888888888888888888888888888888888888888888888888888888888888888888888888888888888
            #
            #   Note that the first parameter is a LIST of input files, the last of which
            #       is the flag file from the previous task which we can ignore
            #
            input_file, previous_flag_file  = input_files
            #
            #888888888888888888888888888888888888888888888888888888888888888888888888888888888
            task_output_file, flag_file     = output_files
            cmd = ("do_something3 %(input_file)s >| %(task_output_file)s ")
            cmd = cmd % {
                            "input_file":               input_file,
                            "task_output_file":         task_output_file
                        }
            # completion flag file for this task
            if not os.system( cmd ):
                open(flag_file, "w")


    The :ref:`Bioinformatics example<examples_bioinformatics_part2.step2>` contains :ref:`code <examples_bioinformatics_part2_code>` for checkpointing.


_____________________________________________________
A. Use a temp file
_____________________________________________________

    (Thanks to Martin Goodson for suggesting this and providing an example.)

    I normally use a decorator to create a temporary file which is only renamed after the task has completed without any problems. This seems a more elegant solution to the problem:


        .. code-block:: python

            def usetemp(task_func):
                """ Decorate a function to write to a tmp file and then rename it. So half finished tasks cannot create up to date targets.
                """
                @wraps(task_func)
                def wrapper_function(*args, **kwargs):
                    args=list(args)
                    outnames=args[1]
                    if not isinstance(outnames, basestring) and  hasattr(outnames, '__getitem__'):
                        tmpnames=[str(x)+".tmp" for x in outnames]
                        args[1]=tmpnames
                        task_func(*args, **kwargs)
                        try:
                            for tmp, name in zip(tmpnames, outnames):
                                if os.path.exists(tmp):
                                    os.rename(tmp, str(name))
                        except BaseException as e:
                            for name in outnames:
                                if os.path.exists(name):
                                    os.remove(name)
                            raise (e)
                    else:
                        tmp=str(outnames)+'.tmp'
                        args[1]=tmp
                        task_func(*args, **kwargs)
                        os.rename(tmp, str(outnames))
            return wrapper_function


    Use like this:

        .. code-block:: python

            @files(None, 'client1.price')
            @usetemp
            def getusers(inputfile, outputname):
                #**************************************************
                # code goes here
                # outputname now refers to temporary file
                pass





^^^^^^^^^^^^^^^
Windows
^^^^^^^^^^^^^^^

=========================================================
Q. Windows seems to spawn *ruffus* processes recursively
=========================================================

    A. It is necessary to protect the "entry point" of the program under windows.
    Otherwise, a new process will be started each time the main module is imported
    by a new Python interpreter as an unintended side effects. Causing a cascade
    of new processes.

    See: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming

    This code works::

        if __name__ == '__main__':
            try:
                pipeline_run([parallel_task], multiprocess = 5)
        except Exception, e:
            print e.args



^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Sun Grid Engine / PBS etc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

==========================================================================================================================================
Q. Can Ruffus be used to manage a cluster or grid based pipeline?
==========================================================================================================================================
    A. Some minimum modifications have to be made to your *Ruffus* script to allow it to submit jobs to a cluster

        Thanks to Andreas Heger and others at CGAT for contributing ideas and code.

    1) You need to have the `python drmaa <https://code.google.com/p/drmaa-python/wiki/Tutorial>`_ module installed:

        .. code-block:: bash

            easy_install -U drmaa

        `DRMAA <http://www.drmaa.org/>`_ is the standard way to talk to grid/cluster systems. It has been, for example, built into the Sun / Oracle Grid Engine (SGE) for some time.

        .. note:: You may need to tell the python drmaa module where the (correct) drmaa API files live on your system, e.g.

            .. code-block:: bash

                export DRMAA_LIBRARY_PATH=/some/path/on/your/system/libdrmaa.so


    2) You need to switch *Ruffus* into multi-threading rather than multi-processing mode.


        .. code-block:: python
           :emphasize-lines: 4

           pipeline_run(target_tasks,
                        multiprocess = 230,
                        logger = stderr_logger,
                        use_multi_threading = True)


        .. note:: Embarrassingly, the degree of pipeline parallelism is specified via `multiprocess = NNN`, even in multi threading mode!!

        This is necessary for two reasons:

        A) To allow drmaa sessions to be shared

            Each drmaa session opens up a channel of communication with the cluster / grid management sofware. Especially for older versions of SGE (<6.2?), each persistent connection with
            the grid management system consumes a precious file descriptor.


        B) To prevent the cluster / grid submission node from being overwhelmed

            Most calculations will be carried out on cluster nodes, but even with the best designed pipelines, there will still be some *Ruffus* bookkeeping which will take place on the
            submisison node where *Ruffus* is running. In the overall scheme, this may be insignificant, but if thousands of cluster nodes return at the same time, and thousand of *Ruffus* jobs
            perform their bookkeeping at the same time, this could cause a "processor storm" and overwhelm or even kill the grid submission node. This will have a decided effect on your popularity.

            Normally, multi-processing is the preferable way to run code in parallel in python because of the python `Global Interpreter Lock (GIL) <https://wiki.python.org/moin/GlobalInterpreterLock>`_ .
            Multiple native *threads* cannot execute python byte codes at the same time. Obviously that would severely cut down on parallelism in your *Ruffus* scripts.

            For grid pipelines, this is an advantage: the Global Interpreter Lock (GIL) keeps all your python code serialised rather than swamping the cluster submission node.

            If your *Ruffus* script is just forwarding calls to run on the cluster, the reduction in parallelism on the head node is no big deal, so long as all the parallelism occurs on the cluster.
            Each *Ruffus* job on the submission node is mostly quiescent, forwarding all the hard work to separate grid or cluster nodes.


    3) Run code on the cluster using drmaa

        The *Ruffus* `drmaa_wrapper` module provides a convenience function which can be used as a drop in replacement for `os.system()` or `subprocess.check_output()` to run commands directly on the cluster.

        .. code-block:: python

            import ruffus
            from ruffus.drmaa_wrapper import run_job

            stdout_lines, stderr_lines = run_job("ls", "short_queue")

        (You can of course continue to use `qrsh` or `qsub` to run commands on the cluster.)


        `run_job` allows the
            * queue name
            * job name
            * priority
            * other custom drmaa options to be specified

        * If a drmaa_session is not provided, it will create a shared session for you.
        * Error messages are optionally sent to a supplied object with `python logging <http://docs.python.org/2/library/logging.html>`_ semantics, much like in the rest of Ruffus.
        * For testing and developing, `run_locally` and `touch_only` flags allow the specified command to be run locally (without forwarding to the grid via drmaa), or for specified output files to be created (`touch`) with running any code at all.

        The full signature is:

        .. code-block:: python

            def run_job(cmd_str, job_queue_name = None, job_queue_priority = None, job_name = None, job_other_options = None, logger = None, drmaa_session = None, run_locally = False, output_files = None, touch_only = False):
                ""



==========================================================================================================================================
Q. When I submit lots of jobs via Sun Grid Engine (SGE), the head node occassionally freezes and dies
==========================================================================================================================================

    A. See Running *Ruffus* on a cluster head node with drmaa



=====================================================================
Q. Keeping Large intermediate files
=====================================================================

    Sometimes pipelines create a large number of intermediate files which might not be needed later.

    Unfortunately, the current design of *Ruffus* requires these files to hang around otherwise the pipeline
    will not know that it ran successfully.

    We have some tentative plans to get around this but in the meantime, Bernie Pope suggests
    truncating intermediate files in place, preserving timestamps::


        # truncate a file to zero bytes, and preserve its original modification time
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


