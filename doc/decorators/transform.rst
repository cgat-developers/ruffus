.. include:: ../global.inc
.. _decorators.transform:
.. index:: 
    pair: @transform; Syntax

See :ref:`Decorators <decorators>` for more decorators

########################
@transform
########################

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.transform.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.transform.extra_parameters`_
.. |output_pattern| replace:: `output_pattern`
.. _output_pattern: `decorators.transform.output_pattern`_
.. |matching_regex| replace:: `matching_regex`
.. _matching_regex: `decorators.transform.matching_regex`_
.. |suffix_string| replace:: `suffix_string`
.. _suffix_string: `decorators.transform.suffix_string`_

*********************************************************************************************************************************************************************************************************************
*@transform* ( |tasks_or_file_names|_, :ref:`suffix<decorators.suffix>`\ *(*\ |suffix_string|_\ *)*\ | :ref:`regex<decorators.regex`\ *(*\ |matching_regex|_\ *)*\ , |output_pattern|_, [|extra_parameters|_,...] )
*********************************************************************************************************************************************************************************************************************
    **Purpose:**
        Applies the task function to transform data from input to output files.

        Output file names are determined from |tasks_or_file_names|_, i.e. from the output
        of specified tasks, or a list of file names. 

        This can be either via matches to the end of the file name (suffix matches) or, more
        flexibly, using regular expression pattern substitutions.

        Only out of date tasks (comparing input and output files) will be run
        
    **Simple Example**

        Transforms ``*.c`` to ``*.o``::
    
            @transform(["1.c", "2.c"], suffix(".c"), ".o")
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
                
.. _decorators.transform.tasks_or_file_names:

    * *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_.
             E.g.:``"a.*" => "a.1", "a.2"``

.. _decorators.transform.suffix_string:

    * *suffix_string*
       must be wrapped in a :ref:`suffix<decorators.suffix>` indicator object.
       The end of each input file name which matches ``suffix_string`` will be replaced by ``output_pattern``.

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

    * *matching_regex*
       is a python regular expression string, which must be wrapped in
       a :ref:`regex<decorators.regex>`\  indicator object
       See python `regular expression (re) <http://docs.python.org/library/re.html>`_ 
       documentation for details of regular expression syntax
       Each output file name is created using regular expression substitution with ``output_pattern``

.. _decorators.transform.output_pattern:

    * *output_pattern*
       Specifies the resulting output file name(s).
                
.. _decorators.transform.extra_parameters:

    * [*extra_parameters, ...*]
       Any extra parameters are passed to the task function.
       
       If ``regex(matching_regex)`` parameter is used, then regular expression substitution
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
