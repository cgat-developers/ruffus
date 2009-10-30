.. _decorators.transform_ex:


See :ref:`Decorators <decorators>` for more decorators

################################################
Advanced usage of @transform:
################################################

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.transform.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.transform.extra_parameters`_
.. |output_pattern| replace:: `output_pattern`
.. _output_pattern: `decorators.transform.output_pattern`_
.. |input_pattern| replace:: `input_pattern`
.. _input_pattern: `decorators.transform.input_pattern`_
.. |matching_regex| replace:: `matching_regex`
.. _matching_regex: `decorators.transform.matching_regex`_
.. |suffix_string| replace:: `suffix_string`
.. _suffix_string: `decorators.transform.suffix_string`_

.. |suffix| replace:: *suffix*
.. _suffix: indicator_objects.html#decorators.suffix
.. |regex| replace:: *regex*
.. _regex: indicator_objects.html#decorators.regex
.. |inputs| replace:: *inputs*
.. _inputs: indicator_objects.html#decorators.inputs




*********************************************************************************************************************************************************************************************************************
*@transform* ( |tasks_or_file_names|_, |suffix|_\ *(*\ |suffix_string|_\ *)*\ | |regex|_\ *(*\ |matching_regex|_\ *)*\ , |inputs|_\ *(*\ |input_pattern|_\ *)*\ , |output_pattern|_, [|extra_parameters|_,...] )
*********************************************************************************************************************************************************************************************************************
    **Purpose:**
        This variant of ``@transform`` provides maximum flexibility to set **input** as well as output file names.
        This is especially useful to **add** an extra dependency to the task.

        Output file names are determined from |tasks_or_file_names|_, i.e. from the output
        of specified tasks, or a list of file names. 

        This can be either via matches to the end of the file name (suffix matches) or, more
        flexibly, using regular expression pattern substitutions.
        
        This variant of ``@transform`` allows input file names to be derived in the same way.
        
        Only out of date tasks (comparing input and output files) will be run
        
    **Example**

        To compile ``*.c`` to ``*.o``, also depending on matching header files ``*.h``::
        
            @transform(previous_task, suffix(".c"), inputs(".c", ".h"),  ".o")
            def compile(infile, outfile):
                # do something here
                pass

        A regular expression gives even more flexibility, allow an additional static dependency to be added,
        compiling ``*.c`` to ``*.o``, depending on header files ``*.h``, and ``universal.h``::
            
            @transform(["1.c", "2.c"], regex(r"(.*).c$"), inputs(r"\1.c", "\1.h", "universal.h"),  "\1.o")
            def compile(infile, outfile):
                # do something here
                pass
                
        This will result in the following functional calls::    
        
            compile(["1.c", "1.h", "universal.h"], "1.o")
            compile(["2.c", "2.h", "universal.h"], "2.o")

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
       The end of each file name which matches suffix_string will be replaced by `output_pattern`.
       Thus::

            @transform(["a.c", "b.c"], suffix(".c"), ".o")
            def compile(infile, outfile):
                pass
                
       will result in the following function calls::         

           compile("a.c", "a.o")
           compile("b.c", "b.o")
             
       File names which do not match suffix_string will be ignored
    
.. _decorators.transform.matching_regex:

    * *matching_regex*
       is a python regular expression string, which must be wrapped in
       a ``regex`` indicator object
       See python `regular expression (re) <http://docs.python.org/library/re.html>`_ 
       documentation for details of regular expression syntax
       Each output file name is created using regular expression substitution with ``output_pattern``

.. _decorators.transform.input_pattern:

    * *input_pattern*
       Specifies the resulting input file name(s).
       
       Must be wrapped in a ``inputs`` indicator object.

.. _decorators.transform.output_pattern:

    * *output_pattern*
       Specifies the resulting output file name(s).
                
.. _decorators.transform.extra_parameters:

    * [*extra_parameters, ...*]
       Any extra parameters are passed to the task function.
       
       If `regex(matching_regex)` parameter is used, then regular expression substitution
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
