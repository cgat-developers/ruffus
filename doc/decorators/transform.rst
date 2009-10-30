.. _decorators.transform:

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
.. |suffix| replace:: *suffix*
.. _suffix: indicator_objects.html#decorators.suffix
.. |regex| replace:: *regex*
.. _regex: indicator_objects.html#decorators.regex

*********************************************************************************************************************************************************************************************************************
*@transform* ( |tasks_or_file_names|_, |suffix|_\ *(*\ |suffix_string|_\ *)*\ | |regex|_\ *(*\ |matching_regex|_\ *)*\ , |output_pattern|_, [|extra_parameters|_,...] )
*********************************************************************************************************************************************************************************************************************
    **Purpose:**
        Applies the task function to transform data from input to output files.

        Output file names are determined from |tasks_or_file_names|_, i.e. from the output
        of specified tasks, or a list of file names. 

        This can be either via matches to the end of the file name (suffix matches) or, more
        flexibly, using regular expression pattern substitutions.

        Only out of date tasks (comparing input and output files) will be run
        
    **Example**

        Transforms ``*.c`` to ``*.o``::
    
            @transform(previous_task, suffix(".c"), ".o")
            def compile(infile, outfile):
                pass
    
        Same example with a regular expression::
            
            @transform(previous_task, regex(r".c$"), ".o")
            def compile(infile, outfile):
                pass

    **Parameters:**
                
.. _decorators.transform.tasks_or_file_names:

    * *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a glob.
             E.g.:``"a.*" => "a.1", "a.2"``

.. _decorators.transform.suffix_string:

    * *suffix_string*
       must be wrapped in a ``suffix`` indicator object.
       The end of each input file name which matches ``suffix_string`` will be replaced by ``output_pattern``.
       Thus::

            @transform(["a.c", "b.c"], suffix(".c"), ".o")
            def compile(infile, outfile):
                pass
                
       will result in the following function calls::         

           compile("a.c", "a.o")
           compile("b.c", "b.o")
             
       input file names which do not match suffix_string will be ignored
    
.. _decorators.transform.matching_regex:

    * *matching_regex*
       is a python regular expression string, which must be wrapped in
       a ``regex`` indicator object
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
       
             @transform(["a.c", "b.c"], regex("r(.*).c"), r"\1.o", r"\1")
             def compile(infile, outfile):
                 pass
                 
       will result in the following function calls::
       
            compile("a.c", "a.o", "a")
            compile("b.c", "b.o", "b")
                   



See :ref:`here <decorators.transform_ex>` for more advanced uses of transform.       
