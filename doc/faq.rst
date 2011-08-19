.. include:: global.inc
******
FAQ
******

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
A. Place your decorator after Ruffus decorators. This ensures that by the time Ruffus sees
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
are made available to Ruffus via your decorator.


======================================================================================
Q. Can a task function in a Ruffus pipeline be called normally outside of Ruffus?
======================================================================================
A. Yes. Most python decorators wrap themselves around a function. However, Ruffus leaves the
original function untouched and unwrapped. Instead, Ruffus adds a ``pipeline_task`` attribute
to the task function to signal that this is a pipelined function.

This means the original task function can be called just like any other python function.

======================================================================================
Q. My tasks creates two files but why does only one survive in the ruffus pipeline?
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
Q. How can a Ruffus task produce output which goes off in different directions?
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
            # Remember to delegate to the default Ruffus code for checking if
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

        Because ``run_this_before_each_job(...)`` is called whenever Ruffus checks to see if
        a job is up to date or not, the function may be called twice for some jobs
        (e.g. ``(None, 'a.1')`` above).


=========================================================================================================
Q. Does *Ruffus* allow checkpointing: to distinguish interrupted and completed results?
=========================================================================================================

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
Sun Grid Engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


=========================================================
Q. *qrsh* eats up all my processor time under *ruffus*
=========================================================
A. `Sun Grid Engine <http://gridengine.sunsource.net/>`_ provides the 
`qrsh <http://gridengine.sunsource.net/nonav/source/browse/~checkout~/gridengine/doc/htmlman/manuals.html?content-type=text/html>`_
command to run an interactive rsh session. ``qrsh`` can
be used to run commands/scripts in a compute farm or grid cluster. 

However, when run within *ruffus*, ``qrsh`` seems to spin idly, polling for input, consuming
all the CPU resources in that process.

An interim solution is to close the ``STDIN`` for the ``qrsh`` invocation::

    from subprocess import Popen, PIPE
    qrsh_cmd = ["qrsh", 
                "-now", "n", 
                "-cwd", 
                "-p", "-%d" % priority, 
                "-q",  queue_name, 
                "little_script.py"]
    p = Popen(qrsh_cmd, stdin = PIPE)
    p.stdin.close()
    sts = os.waitpid(p.pid, 0)

=====================================================================
Q. When I submit lots of jobs at the same time, SGE freezes and dies
=====================================================================
A. This seems to be dependent on your setup. One workaround may be to
introduce a random time delay at the beginining of your jobs::

    import time, random
    @parallel(param_func)
    def task_in_parallel(input_file, output_file):
        """
        Works starts after a random delay so that SGE has a chance to manage the queue
        """
        time.sleep(random.random() / 2.0)
    
        # Wake up and do work



