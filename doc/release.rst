*************
Release notes
*************

=============
Release 3.0.0
=============

Compatibility changes
---------------------

* Python 3.11 or later is required. Linux CI tests Python 3.11 through 3.14.
* History paths are now relative to the history database directory, allowing
  runs from different working directories when the same database and files are
  used. Moving a project together with its database preserves checkpoints if
  their relative layout is unchanged.
* Old histories do not record their original working directory. Their records
  are preserved in the ``ruffus_legacy_history`` SQLite table, and active
  checkpoints are rebuilt on the next history-based run. Expect a one-time
  rerun of affected jobs. Do not share upgraded databases with older Ruffus.
* Keyword-only defaults now contribute to function checksums. Tasks with these
  defaults may rerun once at checksum levels 2 and 3 after upgrading.

Features and fixes
------------------

* Add ``@run_in_main_process()`` and ``Task.run_in_main_process()`` for tasks
  that need to create their own multiprocessing children or run in the pipeline
  caller's thread. Other tasks retain pool execution. ``jobs_limit(1)`` remains
  a concurrency limit and does not opt into this behaviour. See
  :ref:`run_in_main_process <decorators.run_in_main_process>` for limitations.
* Stop resubmitting successful DRMAA jobs when retries are enabled and the
  scheduler provides no job information. Communication-error retry limitations
  remain; this change does not make resubmission safe after a lost response.
* Fix keyword-only and mixed arguments in ``@split``, and correct argument
  forwarding for the legacy regex form.
* Modernize the test runner and add Linux GitHub Actions coverage.
* Remove obsolete hosting references from the documentation.
* Add a ``pyproject.toml`` build configuration using setuptools.

=============
Release 2.8.3
=============

* add missing import

=============
Release 2.8.2
=============

* implement retry behaviour for input file check.

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


=============
Release 2.6.3
=============

* @transform works even when the ouput has more than one file.
* @subdivide works in exactly the same way as @transform.
* ruffus.drmaa_wrapper.run_job() works with python3 `(github) Fixed issue with byte and text streams.
* ruffus.drmaa.wrapper.run_job() allows env (environment) to be set for jobs run locally as well as those on the cluster.
* New object-orientated style syntax works seamlessly with Ruffus command line support. 

=============
Release 2.6.2
=============

* pipeline_printout_graph()` incompatibility with python3 fixed.
* checkpointing did not work correctly with @split and @subdivide.
* @transoform has easier to understand syntax and takes care of most common use cases of ruffus (Thanks Milan Simonovic).
* @transform takes an optional output_dir. 
* Decorators can take named parameters.
