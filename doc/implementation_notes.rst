##########################################
Implementation Tips
##########################################

******************************************************************************
Release
******************************************************************************

    * Change ``ruffus_version.py``

    * Rebuild pdf and copy it to ``doc/static_data``

        cd doc
        make latexpdf
        cp _build/latex/ruffus.pdf static_data

    * Rebuild documentation::

        make htmlsync

    * tag git with, for example::

        git tag -a v2.5 -m "Version 2.5"


    * Upload to pypi::

        python setup.py sdist --format=gztar upload

******************************************************************************
dbdict.py
******************************************************************************

    This is an sqlite backed dictionary originally written by Jacob Sondergaard and
    contributed by Jake Biesinger who added automatic pickling of python objects.

    The pickling code was refactored out by Leo Goodstadt into separate functions as
    part of the preparation to make Ruffus python3 ready.

    Python original saved (pickled) objects as 7 bit ASCII strings. Later formats
    (protocol = -1 is the latest format) uses 8 bit strings and are rather more efficient.

    These then need to be saved as BLOBs to sqlite3 rather than normal strings. We
    can signal this by wrapping the pickled string in a object providing a "buffer interface".
    This is ``buffer`` in python2.6/2.7 and ``memoryview`` in python3.

    http://bugs.python.org/issue7723 suggests there is no portable python2/3 way to write
    blobs to Sqlite without these two incompatible wrappers.
    This would require conditional compilation:

    .. code-block:: python

        if sys.hexversion >= 0x03000000:
            value = memoryview(pickle.dumps(value, protocol = -1))
        else:
            value = buffer(pickle.dumps(value, protocol = -1))


    Despite the discussion on the bug report, sqlite3.Binary seems to work.
    We shall see if this is portable to python3.

******************************************************************************
how to write new decorators
******************************************************************************


    New placeholder class. E.g. for ``@new_deco``

    .. code-block:: python

        class new_deco(task_decorator):
            pass

    Add to list of action names and ids:

    .. code-block:: python

        action_names = ["unspecified",
                        ...
                        "task_new_deco",

        action_task_new_deco     =  15

    Add function:

    .. code-block:: python

        def task_transform (self, orig_args):


    Add documentation to:

        * decorators/NEW_DECORATOR.rst
        * decorators/decorators.rst
        * _templates/layout.html
        * manual




##########################################
Implementation notes
##########################################

N.B. Remember to cite Jake Biesinger and see if he is interested to be a co-author if we ever resubmit the drastically changed version...
He contributed checkpointing, travis and tox etc.

.. _todo.misfeatures:

********************************************************************************************************
``Ctrl-C`` handling
********************************************************************************************************

    Pressing ``Ctrl-C`` left dangling process in Ruffus 2.4 because ``KeyboardInterrupt`` does not play nice with python ``multiprocessing.Pool``
    See http://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool/1408476#1408476

    http://bryceboe.com/2012/02/14/python-multiprocessing-pool-and-keyboardinterrupt-revisited/ provides a reimplementation of Pool which
    however only works when you have a fixed number of jobs which should then run in parallel to completion. Ruffus is considerably more
    complicated because we have a variable number of jobs completing and being submitted into the job queue at any one time. Think
    of tasks stalling waiting for the dependent tasks to complete and then all the jobs of the task being released onto the queue

    The solution is

        #. Use a ``timeout`` parameter when using ``IMapIterator.next(timeout=None)`` to iterate through ``pool.imap_unordered`` because only timed ``condition`` s can be interruptible by signals...!!
        #. This involves rewriting the ``for`` loop manually as a ``while`` loop
        #. We use a timeout of ``99999999``, i.e. 3 years, which should be enough for any job to complete...
        #. Googling after the fact, it looks like the galaxy guys (cool dudes or what) have written similar `code  <https://galaxy-dist.readthedocs.org/en/latest/_modules/galaxy/objectstore/s3_multipart_upload.html>`__
        #. ``next()`` for normal iterators do not take ``timeout`` as an extra parameter so we have to wrap next in a conditional :-(. The galaxy guys do a `shim  <http://en.wikipedia.org/wiki/Shim_(computing)>`__ around ``next()`` but that is as much obsfucation as a simple if...
        #. After jobs are interrupted by a signal, we rethrow with our own exception because we want something that inherits from ``Exception`` unlike ``KeyboardInterrupt``
        #. When a signal happens, we need to immediately stop ``feed_job_params_to_process_pool()`` from sending more parameters into the job queue (``parameter_q``)
           We use a proxy to a ``multiprocessing.Event`` (via ``syncmanager.Event()``). When ``death_event`` is set, all further processing stops...
        #. We also signal that all jobs should finish by putting ``all_tasks_complete()`` into ``parameter_q`` but only ``death_event`` prevents jobs already in the queue from going through
        #. Ater signalling, some of the child processes appear to be dead by the time we start cleaning up. ``pool.terminate()`` sometimes tries and fails to
           re-connect to the the ``death_event`` proxy via sockets and throws an exception. We should really figure out a better solution but in the meantime
           wrapping it in a ``try / except`` allows a clean exit.
        #. If a vanilla exception is raised without multiprocessing running, we still need to first save the exception in ``job_errors`` (even if it is just one) before
           cleaning up, because the cleaning up process may lead to further (ignored) exceptions which would overwrite the current exception when we need to rethrow it


    Exceptions thrown in the middle of a multiprocessing / multithreading job appear to be handled gracefully.

    For drmaa jobs, ``qdel`` may still be necessary.


******************************************************************************
Python3 compatability
******************************************************************************

    Required extensive changes especially in unit test code.

    Changes:

    1. ``sort`` in python3 does not order mixed types, i.e. ``int()``, ``list()`` and ``str()`` are incommensurate

       * In ``task.get_output_files (...)``, sort after conversion to string

         .. code-block:: python

           sorted(self.output_filenames, key = lambda x: str(x))

       * In ``file_name_parameters.py``: ``collate_param_factory (...)``, ``sort`` after conversion to string, then ``groupby`` without string conversion. This is
         because we can't guarantee that two different objects do not have the same string representation. But ``groupby`` requires that similar things are adjacent...

         In other words, ``groupby`` is a refinement of ``sorted``

         .. code-block:: python

           for output_extra_params, grouped_params in groupby(sorted(io_params_iter, key = get_output_extras_str), key = get_output_extras):
               pass

    2. ``print()`` is a function

       .. code-block:: python

            from __future__ import print_function

    3. ``items()`` only returns a list in python2. Rewrite ``dict.iteritems()`` whenever this might cause a performance bottleneck
    4. ``zip`` and ``map`` return iterators. Conditionally import in python2

       .. code-block:: python

            import sys
            if sys.hexversion < 0x03000000:
                from future_builtins import zip, map

    5. ``cPickle->pickle`` ``CStringIO->io`` need to be conditionally imported

       .. code-block:: python

            try:
                import StringIO as io
            except:
                import io as io


    6. ``map`` code can be changed to list comprehensions. Use ``2to3`` to do heavy lifting

    7. All normal strings are unicode in python3. Have to use ``bytes`` to support 8-bit char arrays.
       Normally, this means that ``str`` "just works". However, to provide special handling of
       both 8-bit and unicode strings in python2, we often need to check for ``isinstance(xxx, basestring)``.

       We need to conditionally define:

       .. code-block:: python

            if sys.hexversion >= 0x03000000:
                # everything is unicode in python3
                path_str_type = str
            else:
                path_str_type = basestring

            # further down...
            if isinstance(compiled_regex, path_str_type):
                pass



******************************************************************************
Refactoring: parameter handling
******************************************************************************

    Though the code is still split in a not very sensible way between ``ruffus_utility.py``, ``file_name_parameters.py`` and ``task.py``,
        some rationalisation has taken place, and comments added so further refactoring can be made more easily.

    Common code for::

        file_name_parameters.split_ex_param_factory()
        file_name_parameters.transform_param_factory()
        file_name_parameters.collate_param_factory()

    has been moved to ``file_name_parameters.py.yield_io_params_per_job()``


    unit tests added to ``test_file_name_parameters.py`` and ``test_ruffus_utility.py``




******************************************************************************
``formatter``
******************************************************************************
    ``get_all_paths_components(paths, regex_str)`` in ``ruffus_utility.py``

    Input files names are first squished into a flat list of files.
    ``get_all_paths_components()`` returns both the regular expression matches and the break down of the path.

    In case of name clashes, the classes with higher priority override:

        1) Captures by name
        2) Captures by index
        3) Path components:
            'ext' = extension with dot
            'basename' = file name without extension
            'path' = path before basename, not ending with slash
            'subdir' = list of directories starting with the most nested and ending with the root (if normalised)
            'subpath' = list of 'path' with successive directories removed starting with the most nested and ending with the root (if normalised)

        E.g.  ``name = '/a/b/c/sample1.bam'``, ``formatter=r"(.*)(?P<id>\d+)\.(.+)")`` returns:

        .. code-block:: python

                0:          '/a/b/c/sample1.bam',           // Entire match captured by index
                1:          '/a/b/c/sample',                // captured by index
                2:          'bam',                          // captured by index
                'id':       '1'                             // captured by name
                'ext':      '.bam',
                'subdir':   ['c', 'b', 'a', '/'],
                'subpath':  ['/a/b/c', '/a/b', '/a', '/'],
                'path':     '/a/b/c',
                'basename': 'sample1',


    The code is in ``ruffus_utility.py``:

    .. code-block:: python

        results = get_all_paths_components(paths, regex_str)
        string.format(results[2])


    All the magic is hidden inside black boxes ``filename_transform`` classes:

    .. code-block:: python


        class t_suffix_filename_transform(t_filename_transform):
        class t_regex_filename_transform(t_filename_transform):
        class t_format_filename_transform(t_filename_transform):

===================================================
``formatter()``: ``regex()`` and ``suffix()``
===================================================


    The previous behaviour with regex() where mismatches fail even if no substitution is made is retained by the use of ``re.subn()``.
    This is a corner case but I didn't want user code to break

    .. code-block:: python

        # filter on ".txt"
        input_filenames = ["a.wrong", "b.txt"]
        regex("(.txt)$")

        # fails, no substitution possible
        r"\1"

        # fails anyway even through regular expression matches not referenced...
        r"output.filename"


************************************************************************************************************************************************************
@product()
************************************************************************************************************************************************************

    * Use combinatoric generators from itertools and keep that naming scheme
    * Put all new generators in an ``combinatorics`` submodule namespace to avoid breaking user code. (They can imported if necessary.)
    * test code in test/test_combinatorics.py
    * The ``itertools.product(repeat)`` parameter doesn't make sense for Ruffus and will not be used
    * Flexible number of pairs of ``task`` / ``glob`` / file names + ``formatter()``
    * Only ``formatter([OPTIONAl_REGEX])`` provides the necessary flexibility to construct the output so we won't bother with suffix and regex

    * Similar to ``@transform`` but with extra level of nested-ness

    Retain same code for ``@product`` and ``@transform`` by adding an additional level of indirection:
        * generator wrap around ``get_strings_in_nested_sequence`` to convert nested input parameters either to a single flat list of file names or to nested lists of file names

          .. code-block:: python

              file_name_parameters.input_param_to_file_name_list (input_params)
              file_name_parameters.list_input_param_to_file_name_list (input_params)

        * ``t_file_names_transform`` class which stores a list of regular expressions, one for each ``formatter()`` object corresponding to a single set of input parameters

          .. code-block:: python

            t_formatter_file_names_transform
            t_nested_formatter_file_names_transform

        * string substitution functions which will apply a list of ``formatter`` changes

          .. code-block:: python

                ruffus.utility.t_formatter_replace()
                ruffus.utility.t_nested_formatter_replace()

        * ``ruffus_uilility.swap_doubly_nested_order()`` makes the syntax / implementation very orthogonal

************************************************************************************************************************************************************
``@permutations(...),`` ``@combinations(...),`` ``@combinations_with_replacement(...)``
************************************************************************************************************************************************************

    Similar to ``@product`` extra level of nested-ness is self versus self

    Retain same code for ``@product``
        * forward to a sinble ``file_name_parameters.combinatorics_param_factory()``
        * use ``combinatorics_type`` to dispatch to ``combinatorics.permutations``, ``combinatorics.combinations`` and ``combinatorics.combinations_with_replacement``
        * use ``list_input_param_to_file_name_list`` from ``file_name_parameters.product_param_factory()``



************************************************************************************************************************************************************
drmaa alternatives
************************************************************************************************************************************************************

    Alternative, non-drmaa polling code at

    https://github.com/bjpop/rubra/blob/master/rubra/cluster_job.py



************************************************************************************************************************************************************
Task completion monitoring
************************************************************************************************************************************************************

===================================================
 How easy is it to abstract out the database?
===================================================

    * The database is Jacob Sondergaard's ``dbdict`` which is a nosql / key-value store wrapper around sqlite
        .. code-block:: python

            job_history = dbdict.open(RUFFUS_HISTORY_FILE, picklevalues=True)

    * The key is the output file name, so it is important not to confuse Ruffus by having different tasks generate the same output file!
    * Is it possible to abstract this so that **jobs** get timestamped as well?
    * If we should ever want to abstract out ``dbdict``, we need to have a similar key-value store class,
      and make sure that a single instance of ``dbdict`` is used through ``pipeline_run`` which is passed up
      and down the function call chain. ``dbdict`` would then be drop-in replaceable by our custom (e.g. flat-file-based) dbdict alternative.


    To peek into the database:

        .. code-block:: bash

            $ sqlite3 .ruffus_history.sqlite
            sqlite> .tables
            data
            sqlite> .schema data
            CREATE TABLE data (key PRIMARY KEY,value);
            sqlite> select key from data order by key;

======================================================================================================
 Can we query the database, get Job history / stats?
======================================================================================================

        Yes, if we write a function to read and dump the entire database but this is only useful with timestamps and task names. See below

======================================================================================================
  What are the run time performance implications?
======================================================================================================

  Should be fast: a single db connection is created and used inside ``pipeline_run``,  ``pipeline_printout``,  ``pipeline_printout_graph``



===================================================
  Avoid pauses between tasks
===================================================

    Allows Ruffus to avoid adding an extra 1 second pause between tasks to guard against file systems with low timestamp granularity.

        * If the local file time looks to be in sync with the underlying file system, saved system time is used instead of file timestamps




******************************************************************************************
``@mkdir(...),``
******************************************************************************************

    * ``mkdir`` continues to work seamlessly inside ``@follows``) but also as its own decorator ``@mkdir`` due to the original happy orthogonal design
    * fixed bug in checking so that Ruffus does't blow up if non strings are in the output (number...)
    * note: adding the decorator to a previously undecorated function might have unintended consequences. The undecorated function turns into a zombie.
    * fixed ugly bug in ``pipeline_printout`` for printing single line output
    * fixed description and printout indent


