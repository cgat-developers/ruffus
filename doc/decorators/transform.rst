.. include:: ../global.inc
.. _decorators.transform:
.. index::
    pair: @transform; Syntax

.. seealso::

    * :ref:`@transform <new_manual.transform>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators


.. |input| replace:: `input`
.. _input: `decorators.transform.input`_
.. |extras| replace:: `extras`
.. _extras: `decorators.transform.extras`_
.. |output| replace:: `output`
.. _output: `decorators.transform.output`_
.. |filter| replace:: `filter`
.. _filter: `decorators.transform.filter`_
.. |matching_regex| replace:: `matching_regex`
.. _matching_regex: `decorators.transform.matching_regex`_
.. |matching_formatter| replace:: `matching_formatter`
.. _matching_formatter: `decorators.transform.matching_formatter`_
.. |suffix_string| replace:: `suffix_string`
.. _suffix_string: `decorators.transform.suffix_string`_

########################
transform
########################
************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
@transform( |input|_, |filter|_, |output|_, [|extras|_,...] )
************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

    **Purpose:**
        Applies the task function to transform data from |input|_ to |output|_ files.

        Output file names are specified from |input|_, i.e. from the |output|_
        of specified tasks, or a list of file names, or a |glob|_ matching pattern.

        String replacement occurs either through suffix matches via :ref:`suffix<decorators.suffix>` or
        the :ref:`formatter<decorators.formatter>` or :ref:`regex<decorators.regex>` indicators.

        Only out of date tasks (comparing |input|_ and |output|_ files) will be run

    **Simple Example**

        Transforms ``*.c`` to ``*.o``::

            @transform(input = ["1.c", "2.c"], filter = suffix(".c"), output = ".o")
            def compile(infile, outfile):
                pass

        Same example with a regular expression::

            @transform(["1.c", "2.c"], regex(r".c$"), ".o")
            def compile(infile, outfile):
                pass

        Both result in the following function calls:

            ::

                # 1.c -> 1.o
                # 2.c -> 2.o
                compile("1.c", "1.o")
                compile("2.c", "2.o")


    **Escaping regular expression patterns**

        A string like ``universal.h`` in ``add_inputs`` will added *as is*.
        ``r"\1.h"``, however, performs suffix substitution, with the special form ``r"\1"`` matching everything up to the suffix.
        Remember to 'escape' ``r"\1"`` otherwise Ruffus will complain and throw an Exception to remind you.
        The most convenient way is to use a python "raw" string.

    **Parameters:**

.. _decorators.transform.input:

    * **input** = *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the |output|_ of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_.
             E.g.:``"a.*" => "a.1", "a.2"``


.. _decorators.transform.filter:

.. _decorators.transform.suffix_string:

    * **filter** = *suffix(suffix_string)*
       must be wrapped in a :ref:`suffix<decorators.suffix>` indicator object.
       The end of each |input|_ file name which matches ``suffix_string`` will be replaced by |output|_.

       Input file names which do not match suffix_string will be ignored


       The non-suffix part of the match can be referred to using the ``"\1"`` pattern. This
       can be useful for putting the output in different directory, for example::


            @transform(["1.c", "2.c"], suffix(".c"), r"my_path/\1.o")
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


            @transform(["1.c", "2.c"], suffix(".c"), [r"\1.o", ".o"], "Compiling \1", "verbatim")
            def compile(infile, outfile):
                pass

       Results in the following function calls:

            ::

                compile("1.c", ["1.o", "1.o"], "Compiling 1", "verbatim")
                compile("2.c", ["2.o", "2.o"], "Compiling 2", "verbatim")

       Since r"\1" is optional for the output parameter, ``"\1.o"`` and ``".o"`` are equivalent.
       However, strings in other parameters which do not contain r"\1" will be included verbatim, much
       like the string ``"verbatim"`` in the above example.




.. _decorators.transform.matching_regex:

    * **filter** = *regex(matching_regex)*
       is a python regular expression string, which must be wrapped in
       a :ref:`regex<decorators.regex>`\  indicator object
       See python `regular expression (re) <http://docs.python.org/library/re.html>`_
       documentation for details of regular expression syntax
       Each output file name is created using regular expression substitution with ``output``

.. _decorators.transform.matching_formatter:

    * **filter** = *formatter(...)*
       a :ref:`formatter<decorators.formatter>` indicator object containing optionally
       a python `regular expression (re) <http://docs.python.org/library/re.html>`_.

.. _decorators.transform.output:

    * **output** = *output*
        Specifies the resulting |output|_ file name(s) after string substitution

.. _decorators.transform.extras:

    * **extras** = *extras*
       Any extra parameters are passed verbatim to the task function

       If you are using named parameters, these can be passed as a list, i.e. ``extras= [...]``

       Any extra parameters are consumed by the task function and not forwarded further down the pipeline.

       If ``regex(matching_regex)`` or ``formatter(...)``` is used, then substitution
       is first applied to (even nested) string parameters. Other data types are passed
       verbatim.

       For example::

             @transform(["a.c", "b.c"], regex(r"(.*).c"), r"\1.o", r"\1")
             def compile(infile, outfile):
                 pass

       will result in the following function calls::

            compile("a.c", "a.o", "a")
            compile("b.c", "b.o", "b")




See :ref:`here <decorators.transform_ex>` for more advanced uses of transform.
