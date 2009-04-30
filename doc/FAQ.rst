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

