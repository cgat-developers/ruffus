.. _decorators.split:

See :ref:`Decorators <decorators>` for more decorators


########################
@split
########################

.. |tasks_or_file_names| replace:: `tasks_or_file_names`
.. _tasks_or_file_names: `decorators.split.tasks_or_file_names`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.split.extra_parameters`_
.. |output_files| replace:: `output_files`
.. _output_files: `decorators.split.output_files`_

*****************************************************************************************************************************************
*@split* ( |tasks_or_file_names|_, |output_files|_, [|extra_parameters|_,...]  )
*****************************************************************************************************************************************
    **Purpose:**
        | Splits a single set of input files into multiple output file names, where the number of
          output files may not be known beforehand. 
        | Only out of date tasks (comparing input and output files) will be run
        
    **Example**::

        @split("big_file", '*.little_files')
        def split_big_to_small(input_file, output_files):
            print "input_file = %s" % input_file
            print "output_file = %s" % output_file

    .
    
        will produce::
    
            input_file = big_file
            output_file = *.little_files
        
        
    **Parameters:**
                
.. _decorators.split.tasks_or_file_names:

                
    * *tasks_or_file_names*
       can be a:

       #.  (Nested) list of file name strings (as in the example above).

            | File names containing ``*[]?`` will be expanded as a glob.
            | E.g.:``"a.*" => "a.1", "a.2"``
           
       #.  Task / list of tasks.

            File names are taken from the output of the specified task(s)

                
.. _decorators.split.output_files:

    * *output_files*
       Specifies the resulting output file name(s).

       | These are used **only** to check if the task is up to date.
       | Normally you would use either a glob (e.g. ``*.little_files`` as above) or  a "sentinel file"
         to indicate that the task has completed successfully. 
       | You can of course do both:

        ::
        
            @split("big_file", ["sentinel.file", "*.little_files"])
            def split_big_to_small(input_file, output_files):
                pass    
                
                
.. _decorators.split.extra_parameters:

    * [*extra_parameters, ...*]
        Any extra parameters are passed verbatim to the task function


