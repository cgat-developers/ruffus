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


    * Check passes Travis

    * tag git with, for example::

        git tag -a v2.6.3 -m "Version 2.6.3"


    * Upload to pypi::

        python setup.py sdist --format=gztar upload

    * Upload to repository::

        git push googlecode
        git push

******************************************************************************
blogger
******************************************************************************

    ::


        .article-content h2 {color: #ad3a2b}
        .article-content h3 {color: #0100b4}
            #header .header-bar .title h1
            {
            background-image: url('http://www.ruffus.org.uk/_static/small_logo.png');
            background-repeat: no-repeat;
            background-position: left;
            }


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

    * ``mkdir`` continues to work seamlessly inside ``@follows`` but also as its own decorator ``@mkdir`` due to the original happy orthogonal design
    * fixed bug in checking so that Ruffus does't blow up if non strings are in the output (number...)
    * note: adding the decorator to a previously undecorated function might have unintended consequences. The undecorated function turns into a zombie.
    * fixed ugly bug in ``pipeline_printout`` for printing single line output
    * fixed description and printout indent



******************************************************************************
Parameter handling
******************************************************************************

======================================================================================================
 Current design
======================================================================================================

    Parameters in Ruffus v 2.x are obtained using a "pull" model.

    Each task has its self.param_generator_func()
    This is an iterator function which yields ``param`` and ``descriptive_param`` per iteration:

    .. code-block:: python

        for param, descriptive_param in self.param_generator_func(runtime_data):
            pass


     ``param`` and ``descriptive_param`` are basically the same except that globs are not expanded in ``descriptive_param`` because
     they are used for display.


    The iterator functions have all the state they need to generate their input, output and extra parameters
    (only ``runtime_data``) is added at run time.
    These closures are generated as nested functions inside "factory" functions defined in ``file_name_parameters.py``

    Each task type has its own factory function. For example:

        .. code-block:: python

            args_param_factory (orig_args)
            files_param_factory (input_files_task_globs, flatten_input, do_not_expand_single_job_tasks, output_extras)
            split_param_factory (input_files_task_globs, output_files_task_globs, *extra_params)
            merge_param_factory (input_files_task_globs, output_param, *extra_params)
            originate_param_factory (list_output_files_task_globs, extras)


    The following factory files delegate most of their work to ``yield_io_params_per_job``:

        to support:

            * ``inputs()``, ``add_inputs()`` input parameter supplementing
            * extra inputs, outputs, extra parameter replacement with ``suffix()``, ``regex()`` and ``formatter``

        .. code-block:: python

            collate_param_factory       (input_files_task_globs,      flatten_input,                              file_names_transform, extra_input_files_task_globs, replace_inputs, output_pattern,          *extra_specs)
            transform_param_factory     (input_files_task_globs,      flatten_input,                              file_names_transform, extra_input_files_task_globs, replace_inputs, output_pattern,          *extra_specs)
            combinatorics_param_factory (input_files_task_globs,      flatten_input, combinatorics_type, k_tuple, file_names_transform, extra_input_files_task_globs, replace_inputs, output_pattern,          *extra_specs)
            subdivide_param_factory     (input_files_task_globs,      flatten_input,                              file_names_transform, extra_input_files_task_globs, replace_inputs, output_files_task_globs, *extra_specs)
            product_param_factory       (list_input_files_task_globs, flatten_input,                              file_names_transform, extra_input_files_task_globs, replace_inputs, output_pattern,          *extra_specs)


            yield_io_params_per_job (input_params, file_names_transform, extra_input_files_task_globs, replace_inputs, output_pattern, extra_specs, runtime_data, iterator, expand_globs_in_output = False):


        #. The first thing they do is to get a list of input parameters, either directly, or by expanding globs or by query upstream tasks:

            .. code-block:: python

                file_names_from_tasks_globs(files_task_globs, runtime_data, do_not_expand_single_job_tasks = True_if_split_or_merge)

            .. note ::

                ``True_if_split_or_merge`` is a wierd parameter which directly queries the upstream dependency for its output files if it is a single task...

                This is legacy code. Probably should be refactored out of existence...


        #. They then convert the input parameters to a flattened list of file names (passing through unchanged the original input parameters structure)

            .. code-block:: python

                input_param_to_file_name_list()
                # combinatorics and product call:
                list_input_param_to_file_name_list()

            This is done at the iterator level because the combinatorics decorators do not have just a
            list of input parameters (They have combinations, permutations, products of
            input parameters etc) but a list of lists of input parameters.

            transform, collate, subdivide => list of strings.
            combinatorics / product       => list of lists of strings

        #. ``yield_io_params_per_job`` yields pairs of param sets by

            * Replacing or supplementing input parameters for the indicator objects ``inputs()`` and ``add_inputs()``
            * Expanding extra parameters
            * Expanding output parameters (with or without expanding globs)

            In each case:
                * If these contains objects which look like strings, we do regular expression / file component substitution
                * If they contain tasks, these are queries for output files


            .. note ::

                This should be changed:

                If the flattened list of input file names is empty, ie. if the input parameters
                contain just other stuff, then the entire parameter is ignored.

======================================================================================================
 Handling file names
======================================================================================================

    All strings in input (or output parameters) are treated as file names unless they are wrapped
    with ``output_from`` in which case they are ``Task``, ``Pipeline`` or function names.

    A list of strings for ready for substitution to output parameters is obtained from the
    ``ruffus_utility.get_strings_in_flattened_sequence()``

    This is called from:

        file_name_parameters

            (1) Either to check that input files exist:
                ``check_input_files_exist()``
                ``needs_update_check_directory_missing()``
                ``needs_update_check_exist()``
                ``needs_update_check_modify_time()``

            (2) Or to generate parameters from the various param factories

                ``product_param_factory()``
                ``transform_param_factory()``
                ``collate_param_factory()``
                ``combinatorics_param_factory()``
                ``subdivide_param_factory()``

            These first call ``file_names_from_tasks_globs()`` to get the input parameters,
            then pass a flattened list of strings to ``yield_io_params_per_job()``

                -> ``file_names_from_tasks_globs()``
                -> ``yield_io_params_per_job(`` ``input_param_to_file_name_list()`` / ``list_input_param_to_file_name_list()`` ``)``


        task

            (3) to obtain a list of file names to ``touch``

                ``job_wrapper_io_files``

            (4) to make directories

                ``job_wrapper_mkdir``

            (5) update / remove files in ``job_history`` if job succeeded or failed

                ``pipeline_run``


======================================================================================================
 Refactor to handle input parameter objects with ruffus_params() functions
======================================================================================================

    We want to expand objects with ruffus_params *only* when doing output parameter
    substitution, i.e. Case (2) above. They are not file names: cases (1), (3), (4), (5).

    Therefore: Expand in ``file_names_from_tasks_globs()`` which also handles
    ``inputs()`` and ``add_inputs`` and ``@split`` outputs.

======================================================================================================
 Refactor to handle formatter() replacement with "{EXTRAS[0][1][3]}" and "[INPUTS[1][2]]"
======================================================================================================

    Non-recursive Substitution in all:

        construct new list where each item is replaced referring to the original and then assign

        extra_inputs()      "[INPUTS[1][2]]" refers to the original input
        output / extras     "[INPUTS[1][2]]" refers to substituted input


    In addition to the flattened input paramters, we need to pass in the unflattened input and extra parameters

    In ``file_name_parameters.py.``: ``yield_io_params_per_job``

        From:
        .. code-block:: python

            extra_inputs = extra_input_files_task_globs.file_names_transformed (filenames, file_names_transform)
            extra_params = tuple( file_names_transform.substitute(filenames, p) for p in extra_specs)
            output_pattern_transformed = output_pattern.file_names_transformed (filenames, file_names_transform)
            output_param = file_names_transform.substitute_output_files(filenames, output_pattern)

        To:
        .. code-block:: python

            extra_inputs = extra_input_files_task_globs.file_names_transformed (orig_input_param, extra_specs, filenames, file_names_transform)
            extra_params = tuple( file_names_transform.substitute(input_param, extra_specs, filenames, p) for p in extra_specs)
            output_pattern_transformed = output_pattern.file_names_transformed (input_param, extra_specs, filenames, file_names_transform)
            output_param = file_names_transform.substitute_output_files(input_param, extra_specs, filenames, output_pattern)

    In other words, we need two extra parameters for inputs and extras

        .. code-block:: python

            class t_file_names_transform(object):
                def substitute (self, input_param, extra_param, starting_file_names, pattern):
                    pass
                def substitute_output_files (self, input_param, extra_param, starting_file_names, pattern):
                    pass


            class t_params_tasks_globs_run_time_data(object):
                def file_names_transformed (self, input_param, extra_param, filenames, file_names_transform):
                    pass


======================================================================================================
 Refactor to handle alternative outputs with either_or(...,...)
======================================================================================================

    * what happens to get_outputs or checkpointing when the job completes but the output files are not made?
    * either_or matches

        * the only alternative to have all files existing
        * the alternative with the most recent file

    * either_or behaves as ``list()`` in ``file_name_parameters.py.`` : ``file_names_from_tasks_globs``



    * Handled to check that input files exist:

            ``check_input_files_exist()``
            ``needs_update_check_directory_missing()``
            ``needs_update_check_exist()``
            ``needs_update_check_modify_time()``

    * Handled to update / remove files in ``job_history`` if job succeeded or failed

    * Only first either_or is used to obtain list of file names to ``touch``

        ``task.job_wrapper_io_files``

    * Only first either_or is used to obtain list of file names to make directories

        ``job_wrapper_mkdir``

    * What happens in ``task.get_output_files()``?


******************************************************************************
 Add Object Orientated interface
******************************************************************************


======================================================================================================
Passed Unit tests
======================================================================================================
    #. Refactored to remove unused "flattened" code paths / parameters
    #. Prefix all attributes for Task into underscore so that help(Task) is not overloaded with details
    #. Named parameters
        * parse named parameters in order filling in from unnamed
        * save parameters in ``dict``  ``Task.parsed_args``
        * call ``setup_task_func()`` afterwards which knows how to setup:
            * poor man's OOP but
            * allows type to be changed after constructor:
              Because can't guarantee that ``@transform`` ``@merge`` is the first Ruffus decorator to be encountered.
        * ``setup_task_func()`` is called for every task before pipeline_xxx()
    #. Much more informative messages for errors when parsing decorator arguments
    #. Pipeline decorator methods renamed to decorator_xxx as in ``decorator_follows``
    #. ``Task.get_task_name()``
       * rename to ``Task.get_display_name()``
       * distinguish between decorator and OO interface
    #. Rename ``_task`` to ``Task``
    #. Identifying tasks from t_job_result:
        * job results do not contain references to ``Task`` so that it can be marshalled more easily
        * we need to look up task at job completion
        * use  ``_node_index`` from ``graph.py`` so we have always a unique identifier for each ``Task``
    #. Parse arguments using ruffus_utility.parse_task_arguments
        * Reveals full hackiness and inconsistency between ``add_inputs`` and ``inputs``. The latter only takes a single argument. Each of the elements of the former gets added along side the existing inputs.
    #. Add ``Pipeline`` class
       * Create global called ``"main"`` (accessed by Pipeline.pipelines["main"])
    #. Task name lookup
        * Task names are unique (Otherwise Ruffus will complain at Task creation)
        * Can also lookup by fully qualified or unqualified function name but these can be ambiguous
        * Ambiguous lookups give a list of tasks only so we can have nice diagnostic messages ... UI trumps clean design
    #. Look up strings across pipelines
       #. Is pipeline name qualified? Check that
       #. Check default (current) pipeline
       #. Check if pipeline name. In which case returns all tail functions
       #. Check all pipelines

       * Will blow up at any instance of ambiguity in any particular pipeline
       * Will blow up at any instance of ambiguity across pipelines
       * Note that mis-spellings will cause problems but if this were c++, I would enforce stricter checking
    #. Look up functions across pipelines
       * Try current pipeline first, then all pipelines
       * Will blow up at any instance of ambiguity in any particular pipeline
       * Will blow up at any instance of ambiguity across pipelines (if not in current pipeline)
    #. @mkdir, @follows(mkdir)
    #. ``Pipeline.get_head_tasks(self)`` (including tasks with mkdir())
    #. ``Pipeline.get_tail_tasks(self)``
    #. ``Pipeline._complete_task_setup()`` which follows chain of dependencies for each task in a pipeline


======================================================================================================
Pipeline and Task creation
======================================================================================================

    * Share code as far as possible between decorator and OOP syntax
    * Cannot use textbook OOP inheritance hierarchy easily because @decorators are not necessarily
      given in order.


      .. <<python

      .. code-block:: python

        Pipeline.transform
            _do_create_task_by_OOP()

        @transform
            Pipeline._create_task()
            task._decorator_transform

                task._prepare_transform()
                    self.setup_task_func = self._transform_setup
                    parse_task_arguments


        Pipeline.run
            pipeline._complete_task_setup()
                # walk up ancestors of all task and call setup_task_func
                unprocessed_tasks = Pipeline.tasks
                while len(unprocessed_tasks):
                    ancestral_tasks = setup_task_func()
                    if not already processed:
                        unprocessed_tasks.append(ancestral_tasks)

                Call _complete_task_setup() for all the pipelines of each task

      ..
        python


======================================================================================================
Connecting Task into a DAG
======================================================================================================

    .. <<python

    ::

        task._complete_setup()
            task._remove_all_parents()
            task._deferred_connect_parents()
            task._setup_task_func()
                task._handle_tasks_globs_in_inputs()
                    task._connect_parents()
                        # re-lookup task from names in current pipeline so that pipeline.clone() works

    ..
        python

    * Task dependencies are normally deferred and saved to ``Task.deferred_follow_params``
    * If Task dependencies call for a new Task (``follows``/``follows(mkdir)``), this takes place
      immediately
    * The parameters in ``Task.deferred_follow_params`` are updated with the created ``Task`` when
      this happens
    * ``Task._prepare_preceding_mkdir()`` has a ``defer`` flag to prevent it from updating
      ``Task.deferred_follow_params`` when it is called to resolve deferred dependencies from
      ``Task._connect_parents()``. Otherwise we will have two copies of each deferred dependency...
    * ``Task.deferred_follow_params`` must be deep-copied otherwise cloned pipelines will interfere
      with each other when dependencies are resolved...









