******
FAQ
******


=========================================================
Q. Some jobs rerun even when they seem up-to-date
=========================================================

A. You might have fallen foul of coarse timestamp precision in some
operating systems.

If you are using ``@files`` or ``files_re``, ruffus uses
file modification times to see if input files were created before
output files.

Unfortunately, some file systems for some versions of 
Windows, Unix, linux or NFS do not record file times with
sub-second precision.

In the worse case, you might try adding some ``time.sleep(1)`` judiciously.


=========================================================
Q. Ruffus seems to be hanging in the same place
=========================================================

A. If ruffus is interrupted, for example, by a Ctrl-C,
you will find the following lines of code highlighted::

    File "build/bdist.linux-x86_64/egg/ruffus/task.py", line 1904, in pipeline_run
    File "build/bdist.linux-x86_64/egg/ruffus/task.py", line 1380, in run_all_jobs_in_task
    File "/xxxx/python2.6/multiprocessing/pool.py", line 507, in next
      self._cond.wait(timeout)
    File "/xxxxx/python2.6/threading.py", line 237, in wait
      waiter.acquire() 
      
This is *not* where ruffus is hanging but the boundary between the main programme process
and the sub-processes which run ruffus jobs in parallel.

This is naturally where broken execution threads get washed up onto.


=========================================================
Q. *qrsh* eats up all my processor time under ruffus
=========================================================
`Sun Grid Engine <http://gridengine.sunsource.net/>`_ provides the 
`qrsh <http://gridengine.sunsource.net/nonav/source/browse/~checkout~/gridengine/doc/htmlman/manuals.html?content-type=text/html>`_
command to run an interactive rsh session. ``qrsh`` can
be used to run commands/scripts in a compute farm or grid cluster. 

However, when run within ruffus, ``qrsh`` seems to spin idly, polling for input, consuming
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

                                      
