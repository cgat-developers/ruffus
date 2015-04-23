.. include:: ../global.inc
.. _decorators.transform_ex:
.. index::
    pair: @transform, inputs(...); Syntax
    pair: @transform, add_inputs(...); Syntax


.. seealso::

    * :ref:`@transform(.., add_inputs(...)| inputs(...), ...) <new_manual.inputs>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

.. |input| replace:: `input`
.. _input: `decorators.transform_ex.input`_
.. |filter| replace:: `filter`
.. _filter: `decorators.transform_ex.filter`_
.. |extras| replace:: `extras`
.. _extras: `decorators.transform_ex.extras`_
.. |output| replace:: `output`
.. _output: `decorators.transform_ex.output`_
.. |matching_regex| replace:: `matching_regex`
.. _matching_regex: `decorators.transform_ex.matching_regex`_
.. |matching_formatter| replace:: `matching_formatter`
.. _matching_formatter: `decorators.transform_ex.matching_formatter`_
.. |suffix_string| replace:: `suffix_string`
.. _suffix_string: `decorators.transform_ex.suffix_string`_
.. |replace_inputs| replace:: `replace_inputs`
.. _replace_inputs: `decorators.transform_ex.replace_inputs`_
.. |add_inputs| replace:: `add_inputs`
.. _add_inputs: `decorators.transform_ex.add_inputs`_


################################################################################################################################################
transform
################################################################################################################################################
************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
@transform( |input|_, |filter|_, |replace_inputs|_ | |add_inputs|_, |output|_, [|extras|_,...] )
************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

    **Purpose:**
        Applies the task function to transform data from |input|_ to |output|_ files.

        This variant of ``@transform`` allows additional inputs or dependencies to be added
        dynamically to the task.

        Output file names are specified from |input|_, i.e. from the |output|_
        of specified tasks, or a list of file names, or a |glob|_ matching pattern.

        This variant of ``@transform`` allows additional or replacement input file names to be derived in the same way.

        String replacement occurs either through suffix matches via :ref:`suffix<decorators.suffix>` or
        the :ref:`formatter<decorators.formatter>` or :ref:`regex<decorators.regex>` indicators.

        It is a **one to one** operation.

        :ref:`add_inputs(...)<decorators.add_inputs>` nests the the original input parameters in a list before adding additional dependencies.

        :ref:`inputs(...)<decorators.inputs>` replaces the original input parameters wholescale.

        Only out of date tasks (comparing input and output files) will be run

    **Example of** :ref:`add_inputs(...)<decorators.add_inputs>`

        A common task in compiling C code is to include the corresponding header file for the source.

        To compile ``*.c`` to ``*.o``, adding ``*.h`` and the common header ``universal.h``:
            ::

                @transform(["1.c", "2.c"], suffix(".c"), add_inputs([r"\1.h", "universal.h"]),  ".o")
                def compile(infile, outfile):
                    pass

        This will result in the following functional calls:
            ::

                compile(["1.c", "1.h", "universal.h"], "1.o")
                compile(["2.c", "2.h", "universal.h"], "2.o")

    **Example of** :ref:`inputs(...)<decorators.inputs>`

        :ref:`inputs(...)<decorators.inputs>` allows the original input parameters to be replaced wholescale.

        This can be seen in the following example:
            ::

                @transform(input          = [  ["1.c", "A.c", 2]
                                               ["2.c", "B.c", "C.c", 3]],
                           filter         =    suffix(".c"),
                           replace_inputs = inputs([r"\1.py", "docs.rst"]),
                           output         = ".pyc")
                def compile(infile, outfile):
                    pass

        This will result in the following functional calls:
            ::

                compile(["1.py", "docs.rst"], "1.pyc")
                compile(["2.py", "docs.rst"], "2.pyc")



    **Parameters:**

.. _decorators.transform_ex.input:

    * **input** = *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the |output|_ of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_.
             E.g.:``"a.*" => "a.1", "a.2"``

.. _decorators.transform_ex.filter:

.. _decorators.transform_ex.suffix_string:

    * **filter** = *suffix(suffix_string)*
       must be wrapped in a :ref:`suffix<decorators.suffix>` indicator object.
       The end of each |input|_ file name which matches ``suffix_string`` will be replaced by |output|_.
       Thus::

            @transform(input = ["a.c", "b.c"],
                       filter = suffix(".c"),
                       output = ".o")
            def compile(infile, outfile):
                pass

       will result in the following function calls::

           compile("a.c", "a.o")
           compile("b.c", "b.o")

       File names which do not match suffix_string will be ignored

.. _decorators.transform_ex.matching_regex:

    * **filter** = *regex(matching_regex)*
       is a python regular expression string, which must be wrapped in
       a :ref:`regex<decorators.regex>` indicator object
       See python `regular expression (re) <http://docs.python.org/library/re.html>`_
       documentation for details of regular expression syntax
       Each output file name is created using regular expression substitution with ``output``

.. _decorators.transform_ex.matching_formatter:

    * **filter** = *formatter(...)*
       a :ref:`formatter<decorators.formatter>` indicator object containing optionally
       a  python `regular expression (re) <http://docs.python.org/library/re.html>`_.


.. _decorators.transform_ex.add_inputs:

.. _decorators.transform_ex.replace_inputs:

    * **add_inputs** = *add_inputs*\ (...) or **replace_inputs** = *inputs*\ (...)
       Specifies the resulting |input|_\ (s) to each job.

       Positional parameters must be disambiguated by wrapping the values in :ref:`inputs(...)<decorators.inputs>` or an :ref:`add_inputs(...)<decorators.add_inputs>`.

       Named parameters can be passed the values directly.

       Takes:

       #.  Task / list of tasks.
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            Strings will be subject to substitution.
            File names containing ``*[]?`` will be expanded as a |glob|_.
            E.g. ``"a.*" => "a.1", "a.2"``


.. _decorators.transform_ex.output:

    * **output** = *output*
        Specifies the resulting |output|_ file name(s) after string substitution

.. _decorators.transform_ex.extras:

    * **extras** = *extras*
       Any extra parameters are passed verbatim to the task function

       If you are using named parameters, these can be passed as a list, i.e. ``extras= [...]``

       Any extra parameters are consumed by the task function and not forwarded further down the pipeline.

       If the ``regex(...)`` or ``formatter(...)`` parameter is used, then substitution
       is first applied to (even nested) string parameters. Other data types are passed
       verbatim.

       For example::

             @transform(["a.c", "b.c"], regex(r"(.*).c"), inputs(r"\1.c", r"\1.h", "universal.h"),  r"\1.o", r"\1")
             def compile(infiles, outfile, file_name_root):
                 # do something here
                 pass

       will result in the following function calls::

             compile(["1.c", "1.h", "universal.h"], "1.o", "1")
             compile(["2.c", "2.h", "universal.h"], "2.o", "2")


See :ref:`here <decorators.transform>` for more straightforward ways to use transform.
