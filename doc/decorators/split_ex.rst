.. include:: ../global.inc

.. _decorators.split_ex:
.. index:: 
    pair: @split (Advanced Usage); Syntax
    pair: @split, inputs; Syntax
    pair: @split, add_inputs; Syntax
    pair: @split, regex; Syntax

See :ref:`Decorators <decorators>` for more decorators
See :ref:`@split <decorators.split>` for basic syntax.


########################################################################
@split with ``regex(...)``, ``add_inputs`` and ``inputs``
########################################################################

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.split_ex.tasks_or_file_names`_
.. |matching_regex| replace:: `matching_regex`
.. _matching_regex: `decorators.split_ex.matching_regex`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.split_ex.extra_parameters`_
.. |output_pattern| replace:: `output_pattern`
.. _output_pattern: `decorators.split_ex.output_pattern`_
.. |input_pattern_or_glob| replace:: `input_pattern_or_glob`
.. _input_pattern_or_glob: `decorators.split_ex.input_pattern_or_glob`_


********************************************************************************************************************************************************************************************************************************************************************
*@split* ( |tasks_or_file_names|_, :ref:`regex<decorators.regex>`\ *(*\ |matching_regex|_\ *)*\, :ref:`inputs<decorators.inputs>` | :ref:`add_inputs<decorators.add_inputs>`\ *(*\ |input_pattern_or_glob|_\ *)*\ , |output_pattern|_, [|extra_parameters|_,...]  )
********************************************************************************************************************************************************************************************************************************************************************
    **Purpose:**
        Splits a set of input files each into multiple output file names, where the number of
        output files may not be known beforehand.     

        This variant of ``@split`` is much like :ref:`@transform <decorators.transform>` in
        that regular expressions are used to generate output file names from each input file.
        However, :ref:`@transform <decorators.transform>` is a one-to-one operation where each
        input produces a single job generating a single output.
        
        ``@split`` is a "``many->many more``" operation, where each input file can generate
        any number of output files whose number may not be known before hand.
                
        Output file names are determined using th regular expression contained in the
        :ref:`regex<decorators.regex>` indicator from |tasks_or_file_names|_, i.e. from the output
        of specified tasks, or a list of file names, or a |glob|_ matching pattern.

        Additional inputs or dependencies can be added dynamically to the task:
            :ref:`add_inputs<decorators.add_inputs>` nests the the original input parameters in a list before adding additional dependencies.

            :ref:`inputs<decorators.inputs>` replaces the original input parameters wholescale.

        Only out of date tasks (comparing input and output files) will be run.

    **Example**::

            @split(["a.big_file","b.big_file"], regex(r"(.+)\.big_file"), r'\1.*.little_files')
            def split_big_to_small(input_file, output_files):
                print "input_file  = %s" % input_file
                print "output_file = %s" % output_file

    
        This results in the following calls::

            split_big_to_small("a.big_file", "a.*.little_files")
            split_big_to_small("b.big_file", "b.*.little_files")
        
    **Example of** :ref:`add_inputs<decorators.add_inputs>` ::

            @split(["a.big_file","b.big_file"], regex(r"(.+)\.big_file"), add_inputs(r"\1.another_big_file"), r'\1.*.little_files')
            def split_big_to_small(input_file, output_files):
                print "input_file  = %s" % input_file
                print "output_file = %s" % output_file

    
        This results in the following calls::

            split_big_to_small(["a.big_file", "a.another_big_file"], "a.*.little_files")
            split_big_to_small(["b.big_file", "b.another_big_file"], "b.*.little_files")

    **Parameters:**
                
.. _decorators.split_ex.tasks_or_file_names:

                
    * *tasks_or_file_names*
       can be a:

       #.  (Nested) list of file name strings (as in the example above).

            | File names containing ``*[]?`` will be expanded as a |glob|_.
            | E.g.:``"a.*" => "a.1", "a.2"``
           
       #.  Task / list of tasks.

            File names are taken from the output of the specified task(s)

.. _decorators.split_ex.matching_regex:

    * *matching_regex*
       is a python regular expression string, which must be wrapped in
       a :ref:`regex<decorators.regex>` indicator object
       See python `regular expression (re) <http://docs.python.org/library/re.html>`_ 
       documentation for details of regular expression syntax
       Each output file name is created using regular expression substitution with ``output_pattern``

                
.. _decorators.split_ex.input_pattern_or_glob:

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
            
       

.. _decorators.split_ex.output_pattern:

    * *output_files*
       Specifies the resulting output file name(s).

       | These are used **only** to check if the task is up to date.
       | Normally you would use either a |glob|_ (e.g. ``*.little_files`` as above) or  a "sentinel file"
         to indicate that the task has completed successfully. 
       | You can of course do both:

        ::
        
            @split(["a.big_file","b.big_file"], regex(r"(.+)\.big_file"), [r'\1.*.little_files', r'\1.finished'])
            def split_big_to_small(input_file, output_files):
                print "input_file   = %s" % input_file
                print "output_files = %s" % output_file

        will result in the following function calls::
       
            split_big_to_small("a.big_file", ["a.*.little_files", "a.finished"])
            split_big_to_small("b.big_file", ["b.*.little_files", "b.finished"])

        and will produce::
    
            input_file   = a.big_file
            output_files = [a.*.little_files, a.finished]
                         
            input_file   = b.big_file
            output_files = [b.*.little_files, b.finished]
        
                
                
.. _decorators.split_ex.extra_parameters:

    * [*extra_parameters, ...*]
       Any extra parameters are passed to the task function after regular expression substitution
       is applied to (even nested) string parameters. Other data types are passed
       verbatim.
       
       For example::
       
            @split(["a.big_file","b.big_file"], regex(r"(.+)\.big_file"), r'\1.*.little_files', r'\1')
            def split_big_to_small(input_file, output_files, file_name_root):
                print "input_file     = %s" % input_file
                print "output_file    = %s" % output_file
                print "file_name_root = %s" % output_file


       will result in the following function calls::
       
            split_big_to_small("a.big_file", "a.*.little_files", "a")
            split_big_to_small("b.big_file", "b.*.little_files", "b")


