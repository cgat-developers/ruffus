.. _decorators.merge:

See :ref:`Decorators <decorators>` for more decorators

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.merge.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.merge.extra_parameters`_
.. |output_file| replace:: `output_file`
.. _output_file: `decorators.merge.output_file`_

########################
@merge
########################

************************************************************************************
*@merge* ( |tasks_or_file_names|_, |output_file|_, [|extra_parameters|_,...] )
************************************************************************************
    **Purpose:**
        Merges multiple input files into a single output.
        
        Only out of date tasks (comparing input and output files) will be run

    **Example**::

        @merge(previous_task, 'all.summary')
        def summarize(infiles, summary_file):
            pass
        
    **Parameters:**
                
                
.. _decorators.merge.tasks_or_file_names:

    * *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a glob.
             E.g.:``"a.*" => "a.1", "a.2"``
             
                
.. _decorators.merge.output_file:

    * *output_file*
        Specifies the resulting output file name(s).
                
.. _decorators.merge.extra_parameters:

    * *extra_parameters, ...*
        Any optional extra parameters are passed verbatim to the task function



See :ref:`here <decorators.collate>` for more advanced uses of merging.


