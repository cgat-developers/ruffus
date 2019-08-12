*************
Release notes
*************

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
