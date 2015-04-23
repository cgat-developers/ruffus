.. include:: ../global.inc
.. _decorators.mkdir:
.. index::
    pair: @mkdir; Syntax

.. seealso::

    * :ref:`@mkdir <new_manual.mkdir>` in the **Ruffus** Manual
    * :ref:`@follows(mkdir("dir")) <decorators.follows>` specifies the creation of a *single* directory as a task pre-requisite.
    * :ref:`Decorators <decorators>` for more decorators

.. |input| replace:: `input`
.. _input: `decorators.mkdir.input`_
.. |output| replace:: `output`
.. _output: `decorators.mkdir.output`_
.. |filter| replace:: `filter`
.. _filter: `decorators.mkdir.filter`_
.. |matching_regex| replace:: `matching_regex`
.. _matching_regex: `decorators.mkdir.matching_regex`_
.. |matching_formatter| replace:: `matching_formatter`
.. _matching_formatter: `decorators.mkdir.matching_formatter`_
.. |suffix_string| replace:: `suffix_string`
.. _suffix_string: `decorators.mkdir.suffix_string`_

########################################################################
mkdir
########################################################################

************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
@mkdir( |input|_, |filter|_, |output|_ )
************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
**Purpose:**

        * Prepares directories to receive *Output* files
        * Used when *Output* path names are generated at runtime from *Inputs*. **mkdir** can make sure these runtime specified paths exist.
        * Directory names are generated from **Input** using string substitution via :ref:`formatter() <decorators.formatter>`,  :ref:`suffix() <decorators.suffix>` or  :ref:`regex() <decorators.regex>`.
        * Behaves essentially like ``@transform`` but with its own (internal) function which does the actual work of making a directory
        * Does *not* invoke the host task function to which it is attached
        * Makes specified directories using `os.makedirs  <http://docs.python.org/2/library/os.html#os.makedirs>`__
        * Multiple directories can be created in a list

        .. note::

            Only missing directories are created.

            In other words, the same directory can be specified multiple times safely without, for example, being recreated repeatedly.

            Sometimes, for pipelines with multiple entry points, this is the only way to make sure that certain working or output
            directories are always created or available *before* the pipeline runs.

    **Simple Example**

        Creates multiple directories per job to hold the results of :ref:`@transform<decorators.transform>`

            .. code-block:: python
                :emphasize-lines: 10,20

                from ruffus import *

                #   initial files
                @originate([ 'A.start',
                             'B.start'])
                def create_initial_files(output_file):
                    with open(output_file, "w") as oo: pass


                # create files without making directories -> ERROR
                @transform( create_initial_files,
                            formatter(),
                            ["{path[0]}/{basename[0]}/processed.txt",
                             "{path[0]}/{basename[0]}.tmp/tmp.processed.txt"])
                def create_files_without_mkdir(input_file, output_files):
                    open(output_files[0], "w")
                    open(output_files[1], "w")


                # create files after making corresponding directories
                @mkdir( create_initial_files,
                        formatter(),
                        ["{path[0]}/{basename[0]}",         # create directory
                         "{path[0]}/{basename[0]}.tmp"])    # create directory.tmp
                @transform( create_initial_files,
                            formatter(),
                            ["{path[0]}/{basename[0]}/processed.txt",
                             "{path[0]}/{basename[0]}.tmp/tmp.processed.txt"])
                def create_files_with_mkdir(input_file, output_files):
                    open(output_files[0], "w")
                    open(output_files[1], "w")

                pipeline_run([create_files_without_mkdir])
                pipeline_run([create_files_with_mkdir])

        Running without making the directories first gives errors:

            .. code-block:: python
                :emphasize-lines: 14-19

                >>> pipeline_run([create_files_without_mkdir])
                    Job  = [None -> A.start] completed
                    Job  = [None -> B.start] completed
                Completed Task = create_initial_files

                    Traceback (most recent call last):
                      File "<stdin>", line 1, in <module>
                      File "/usr/local/lib/python2.7/dist-packages/ruffus/task.py", line 3738, in pipeline_run
                        raise job_errors
                    ruffus.ruffus_exceptions.RethrownJobError:

                    Original exception:

                >>> #    Exception #1
                >>> #      'exceptions.IOError([Errno 2] No such file or directory: 'A/processed.txt')' raised in ...
                >>> #       Task = def create_files_without_mkdir(...):
                >>> #       Job  = [A.start -> [processed.txt, tmp.processed.txt]]


        Running after making the directories first:

            .. code-block:: python
                :emphasize-lines: 15

                >>> pipeline_run([create_files_with_mkdir])
                    Job  = [None -> A.start] completed
                    Job  = [None -> B.start] completed
                Completed Task = create_initial_files
                    Make directories [A, A.tmp] completed
                    Make directories [B, B.tmp] completed
                Completed Task = (mkdir 1) before create_files_with_mkdir
                    Job  = [A.start -> [processed.txt, tmp.processed.txt]] completed
                    Job  = [B.start -> [processed.txt, tmp.processed.txt]] completed
                Completed Task = create_files_with_mkdir

    **Parameters:**

.. _decorators.mkdir.input:

    * **input** = *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the |output|_ of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_.
             E.g.:``"a.*" => "a.1", "a.2"``

.. _decorators.mkdir.filter:

.. _decorators.mkdir.suffix_string:

    * **filter** = *suffix(suffix_string)*
       must be wrapped in a :ref:`suffix<decorators.suffix>` indicator object.
       The end of each |input|_ file name which matches ``suffix_string`` will be replaced by |output|_.

       Input file names which do not match suffix_string will be ignored


       The non-suffix part of the match can be referred to using the ``r"\1"`` pattern. This
       can be useful for putting the output in different directory, for example::


            @mkdir(["1.c", "2.c"], suffix(".c"), r"my_path/\1.o")
            def compile(infile, outfile):
                pass

       This results in the following function calls:

            ::

                # 1.c -> my_path/1.o
                # 2.c -> my_path/2.o
                compile("1.c", "my_path/1.o")
                compile("2.c", "my_path/2.o")

       For convenience and visual clarity, the  ``"\1"`` can be omitted from the output parameter.
       However, the ``"\1"`` is mandatory for string substitutions in additional parameters, ::


            @mkdir(["1.c", "2.c"], suffix(".c"), [r"\1.o", ".o"], "Compiling \1", "verbatim")
            def compile(infile, outfile):
                pass

       Results in the following function calls:

            ::

                compile("1.c", ["1.o", "1.o"], "Compiling 1", "verbatim")
                compile("2.c", ["2.o", "2.o"], "Compiling 2", "verbatim")

       Since r"\1" is optional for the output parameter, ``"\1.o"`` and ``".o"`` are equivalent.
       However, strings in other parameters which do not contain r"\1" will be included verbatim, much
       like the string ``"verbatim"`` in the above example.




.. _decorators.mkdir.matching_regex:

    * **filter** = *regex(matching_regex)*
       is a python regular expression string, which must be wrapped in
       a :ref:`regex<decorators.regex>`\  indicator object
       See python `regular expression (re) <http://docs.python.org/library/re.html>`_
       documentation for details of regular expression syntax
       Each output file name is created using regular expression substitution with ``output``

.. _decorators.mkdir.matching_formatter:

    * **filter** = *formatter(...)*
       a :ref:`formatter<decorators.formatter>` indicator object containing optionally
       a  python `regular expression (re) <http://docs.python.org/library/re.html>`_.

.. _decorators.mkdir.output:

    * **output** = *output*
        Specifies the directories to be created after string substitution

