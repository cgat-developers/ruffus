.. _task.merge:

See :ref:`Decorators <decorators>` for more decorators

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `task.merge.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `task.merge.extra_parameters`_
.. |output_file| replace:: `output_file`
.. _output_file: `task.merge.output_file`_

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
                
                
.. _task.merge.tasks_or_file_names:

    * *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks (as in the example above).
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a glob.
             E.g.:``"a.*" => "a.1", "a.2"``
             
                
.. _task.merge.output_file:

    * *output_file*
        Specifies the resulting output file name(s).
                
.. _task.merge.extra_parameters:

    * *extra_parameters, ...*
        Any optional extra parameters are passed verbatim to the task function



See :ref:`here <task.collate>` for more advanced uses of merging.


