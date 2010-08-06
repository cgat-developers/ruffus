.. include:: ../global.inc
.. _decorators.collate_ex:
.. index:: 
    pair: @collate (Advanced Usage); Syntax
    pair: @collate, inputs(...); Syntax
    pair: @collate, add_inputs(...); Syntax

See :ref:`Decorators <decorators>` for more decorators

####################################################
@collate  with ``add_inputs`` and ``inputs``
####################################################

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.collate_ex.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.collate_ex.extra_parameters`_
.. |output_pattern| replace:: `output_pattern`
.. _output_pattern: `decorators.collate_ex.output_pattern`_
.. |input_pattern_or_glob| replace:: `input_pattern_or_glob`
.. _input_pattern_or_glob: `decorators.collate_ex.input_pattern_or_glob`_
.. |matching_regex| replace:: `matching_regex`
.. _matching_regex: `decorators.collate_ex.matching_regex`_


**********************************************************************************************************************************************************************************************************************************************************************************************************************
*@collate* ( |tasks_or_file_names|_, :ref:`regex<decorators.regex>`\ *(*\ |matching_regex|_\ *)*\ , [:ref:`inputs<decorators.inputs>`\ *(*\ |input_pattern_or_glob|_\ *)* | :ref:`add_inputs<decorators.add_inputs>`\ *(*\ |input_pattern_or_glob|_\ *)*\] , |output_pattern|_, [|extra_parameters|_,...] )
**********************************************************************************************************************************************************************************************************************************************************************************************************************
    **Purpose:**
        Groups / collates sets of input files, each into a separate summary. 
        
        This variant of ``@collate`` allows additional inputs or dependencies to be added 
        dynamically to the task.

        Output file names are determined from |tasks_or_file_names|_, i.e. from the output
        of up stream tasks, or a list of file names. 

        This variant of ``@collate`` allows input file names to be derived in the same way.
    
        :ref:`add_inputs<decorators.add_inputs>` nests the the original input parameters in a list before adding additional dependencies.

        :ref:`inputs<decorators.inputs>` replaces the original input parameters wholescale.

        Only out of date tasks (comparing input and output files) will be run
        
    **Example of** :ref:`add_inputs<decorators.add_inputs>` 

        ``regex(r".*(\..+)"), "\1.summary"`` creates a separate summary file for each suffix.
        But we also add date of birth data for each species::

            animal_files = "tuna.fish", "shark.fish", "dog.mammals", "cat.mammals"
            # summarise by file suffix:
            @collate(animal_files, regex(r".+\.(.+)$"),  add_inputs(r"\1.date_of_birth"), r'\1.summary')
            def summarize(infiles, summary_file):
                pass

        This results in the following equivalent function calls::

            summarize([ ["shark.fish",  "fish.date_of_birth"   ], 
                        ["tuna.fish",   "fish.date_of_birth"   ] ], "fish.summary")
            summarize([ ["cat.mammals", "mammals.date_of_birth"], 
                        ["dog.mammals", "mammals.date_of_birth"] ], "mammals.summary")
    
    **Example of** :ref:`add_inputs<decorators.inputs>` 

        using ``inputs(...)`` will summarise only the dates of births for each species group::

            animal_files = "tuna.fish", "shark.fish", "dog.mammals", "cat.mammals"
            # summarise by file suffix:
            @collate(animal_files, regex(r".+\.(.+)$"),  inputs(r"\1.date_of_birth"), r'\1.summary')
            def summarize(infiles, summary_file):
                pass

        This results in the following equivalent function calls::

            summarize(["fish.date_of_birth"   ], "fish.summary")
            summarize(["mammals.date_of_birth"], "mammals.summary")

    **Parameters:**
                
                
.. _decorators.collate_ex.tasks_or_file_names:

    * *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_.
             E.g.:``"a.*" => "a.1", "a.2"``
           
                
.. _decorators.collate_ex.matching_regex:

    * *matching_regex*
       is a python regular expression string, which must be wrapped in
       a :ref:`regex<decorators.regex>` indicator object
       See python `regular expression (re) <http://docs.python.org/library/re.html>`_ 
       documentation for details of regular expression syntax
                
.. _decorators.collate_ex.input_pattern_or_glob:

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
            
       

.. _decorators.collate_ex.output_pattern:

    * *output_pattern*
        Specifies the resulting output file name(s).
                
.. _decorators.collate_ex.extra_parameters:

    * *extra_parameters*
        Any extra parameters are passed verbatim to the task function

    #. *outputs* and optional extra parameters are passed to the functions after regular expression
       substitution in any strings. Non-string values are passed through unchanged.
    #. Each collate job consists of input files which are aggregated by regular expression substitution
       to a single set of output / extra parameter matches


See :ref:`@collate <decorators.collate>` for more straightforward ways to use collate.       
