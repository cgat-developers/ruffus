.. include:: ../global.inc
.. _decorators.files_re:

.. index::
    pair: @files_re; Syntax

.. seealso::

    * :ref:`Decorators <decorators>` for more decorators


########################
@files_re
########################
.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.files_re.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.files_re.extra_parameters`_
.. |output_pattern| replace:: `output_pattern`
.. _output_pattern: `decorators.files_re.output_pattern`_
.. |input_pattern| replace:: `input_pattern`
.. _input_pattern: `decorators.files_re.input_pattern`_
.. |matching_regex| replace:: `matching_regex`
.. _matching_regex: `decorators.files_re.matching_regex`_

*****************************************************************************************************************************************
*@files_re* (|tasks_or_file_names|_, |matching_regex|_, [|input_pattern|_], |output_pattern|_, [|extra_parameters|_,...])
*****************************************************************************************************************************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Legacy design now deprecated. We suggest using :ref:`@transform() <decorators.transform>` instead
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Purpose:**

        All singing, all dancing decorator which can do everything that :ref:`@merge() <decorators.merge>` and
        :ref:`@transform() <decorators.transform>` can do.

        Applies the task function to transform data from input to output files.

        Output file names are determined from |tasks_or_file_names|_, i.e. from the output
        of specified tasks, or a list of file names, using regular expression pattern substitutions.

        Only out of date tasks (comparing input and output files) will be run.

    **Example**:
        ::

            from ruffus import *
            #
            #   convert all files ending in ".1" into files ending in ".2"
            #
            @files_re('*.1', '(.*).1', r'\1.2')
            def transform_func(infile, outfile):
                open(outfile, "w").write(open(infile).read() + "\nconverted\n")

            pipeline_run([task_re])

    If the following files are present ``a.1``, ``b.1``, ``c.1``, this will result in the following function calls:
        ::

            transform_func("a.1", "a.2")
            transform_func("b.1", "b.2")
            transform_func("c.1", "c.2")

    **Parameters:**

.. _decorators.files_re.tasks_or_file_names:

    * *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_ .
             E.g.:``"a.*" => "a.1", "a.2"``

.. _decorators.files_re.matching_regex:

    * *matching_regex*
       a python regular expression string.

       | See python `regular expression (re) <http://docs.python.org/library/re.html>`_ documentation for details of regular expression syntax
       | Each output file name is created using regular expression substitution with |output_pattern|_

.. _decorators.files_re.input_pattern:

    * *input_pattern*
       Optionally specifies the resulting input file name(s).

.. _decorators.files_re.output_pattern:

    * *output_pattern*
       Specifies the resulting output file name(s).

.. _decorators.files_re.extra_parameters:

    * [*extra_parameters, ...*]
       Any extra parameters are passed to the task function.

       | Regular expression substitution is first applied to (even nested) string parameters.
       | Other data types are passed verbatim.

       For example:
        ::

            from ruffus import *
            #
            #   convert all files ending in ".1" into files ending in ".2"
            #
            @files_re('*.1', '(.*).1', r'\1.2', [r'\1', 55], 17)
            def transform_func(infile, outfile, extras, extra3):
                extra1, extra2 = extras
                open(outfile, "w").write(open(infile).read() + "\nconverted%s\n" % (extra1, extra2, extra3))

            pipeline_run([transform_func])

       If the following files are present ``a.1``, ``b.1``, ``c.1``, this will result in the following function calls:
        ::

            transform_func("a.1", "a.2", ["a", 55], 17)
            transform_func("b.1", "b.2", ["b", 55], 17)
            transform_func("c.1", "c.2", ["c", 55], 17)






