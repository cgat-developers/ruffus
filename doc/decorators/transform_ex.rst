.. include:: ../global.inc
.. _decorators.transform_ex:
.. index:: 
    pair: @transform, inputs(...); Syntax
    pair: @transform, add_inputs(...); Syntax


See :ref:`Decorators <decorators>` for more decorators

####################################################
@transform  with ``add_inputs`` and ``inputs``
####################################################

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.transform.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.transform.extra_parameters`_
.. |output_pattern| replace:: `output_pattern`
.. _output_pattern: `decorators.transform.output_pattern`_
.. |input_pattern_or_glob| replace:: `input_pattern_or_glob`
.. _input_pattern_or_glob: `decorators.transform.input_pattern_or_glob`_
.. |matching_regex| replace:: `matching_regex`
.. _matching_regex: `decorators.transform.matching_regex`_
.. |suffix_string| replace:: `suffix_string`
.. _suffix_string: `decorators.transform.suffix_string`_





***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
*@transform* ( |tasks_or_file_names|_, :ref:`suffix<decorators.suffix>`\ *(*\ |suffix_string|_\ *)*\ | :ref:`regex<decorators.regex>`\ *(*\ |matching_regex|_\ *)*\ , :ref:`inputs<decorators.inputs>` | :ref:`add_inputs<decorators.add_inputs>`\ *(*\ |input_pattern_or_glob|_\ *)*\ , |output_pattern|_, [|extra_parameters|_,...] )
***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    **Purpose:**
        This variant of ``@transform`` allows additional inputs or dependencies to be added 
        dynamically to the task.

        Output file names are determined from |tasks_or_file_names|_, i.e. from the output
        of up stream tasks, or a list of file names. 

        This variant of ``@transform`` allows input file names to be derived in the same way.
    
        This can be either via matches to the end of the file name (suffix matches) or, using
        more powerful (but more complex) regular expression pattern substitutions.
        
        :ref:`add_inputs<decorators.add_inputs>` nests the the original input parameters in a list before adding additional dependencies.

        :ref:`inputs<decorators.inputs>` replaces the original input parameters wholescale.
        
        Only out of date tasks (comparing input and output files) will be run
        
    **Example of** :ref:`add_inputs<decorators.add_inputs>` 

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

    **Example of** :ref:`inputs<decorators.inputs>` 

        ``inputs(...)`` allows the original input parameters to be replaced wholescale.

        This can be seen in the following example:
            ::

                @transform([    ["1.c", "A.c", 2]
                                ["2.c", "B.c", "C.c", 3]], 
                                suffix(".c"), inputs([r"\1.py", "docs.rst"]),  ".pyc")
                def compile(infile, outfile):
                    pass

        This will result in the following functional calls:
            ::    
            
                compile(["1.py", "docs.rst"], "1.pyc")
                compile(["2.py", "docs.rst"], "2.pyc")



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
       a :ref:`regex<decorators.regex>` indicator object
       See python `regular expression (re) <http://docs.python.org/library/re.html>`_ 
       documentation for details of regular expression syntax
       Each output file name is created using regular expression substitution with ``output_pattern``

.. _decorators.transform.input_pattern_or_glob:

    * *input_pattern*
       Specifies the resulting input(s) to each job. 
       Must be wrapped in an :ref:`inputs<decorators.inputs>` or an :ref:`inputs<decorators.add_inputs>` indicator object.

       Can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            Strings will be subject to (regular expression or suffix) pattern substitution. 
            File names containing ``*[]?`` will be expanded as a |glob|_.
            E.g.:``"a.*" => "a.1", "a.2"``
            
       

.. _decorators.transform.output_pattern:

    * *output_pattern*
       Specifies the resulting output file name(s).
                
.. _decorators.transform.extra_parameters:

    * [*extra_parameters, ...*]
       Any extra parameters are passed to the task function.
       
       If :ref:`regex<decorators.regex>`\ `(matching_regex)` parameter is used, then regular expression substitution
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
