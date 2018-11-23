*************
Release notes
*************

=============
Release 2.8.1
=============

* [#101] compatibility with gevent >= 1.2
* add lookup_pipeline to exported functions
* fix tests (thanks @LocutusOfBorg, @xnox)

=============
Release 2.8.0
=============

* Ctrl-C will kill drmaa jobs, SIGUSR1 will suspend jobs and SIGUSR2
  will resume.
* [#99] use gevent semaphores
* [#87] run everything through autopep8
* [#86] use pytest for testing
* python3.7 compatibility, thanks to @jbarlow83, @QuLogic

