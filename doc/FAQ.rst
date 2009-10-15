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
        
        .. image:: images/tutorial_four_stage_pipeline.jpg
        

        (Flow Chart Key):
        
        .. image:: images/tutorial_key.jpg


=========================================================
Q. Some jobs re-run even when they seem up-to-date
=========================================================

A. You might have fallen foul of coarse timestamp precision in some
operating systems.

If you are using ``@files`` or ``@files_re``, *ruffus* uses
file modification times to see if input files were created before
output files.

Unfortunately, some file systems in some versions of 
Windows, Unix, linux or NFS do not record file times with
sub-second precision.

In the worse case, you might try adding some ``time.sleep(1)`` judiciously.


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
`Sun Grid Engine <http://gridengine.sunsource.net/>`_ 
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

