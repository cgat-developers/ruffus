.. include:: ../global.inc
.. _decorators.split:
.. index::
    pair: @split; Syntax

.. role:: raw-html(raw)
   :format: html

:raw-html:`<style> .red {color:red} </style>`

.. role:: red



.. seealso::

    * :ref:`@split <new_manual.split>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

########################################################################
split
########################################################################
************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
@split ( |input|_, |output|_, [|extras|_,...]  )
************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

.. |input| replace:: `input`
.. _input: `decorators.split.input`_
.. |extras| replace:: `extras`
.. _extras: `decorators.split.extras`_
.. |output| replace:: `output`
.. _output: `decorators.split.output`_

    **Purpose:**
        | Splits a single set of |input|_ into multiple |output|_, where the number of
          |output|_ may not be known beforehand.
        | Only out of date tasks (comparing |input|_ and |output|_ files) will be run

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

.. _decorators.split.input:


    * **input** = *tasks_or_file_names*
       can be a:

       #.  (Nested) list of file name strings (as in the example above).

            | File names containing ``*[]?`` will be expanded as a |glob|_.
            | E.g.:``"a.*" => "a.1", "a.2"``

       #.  Task / list of tasks.

            File names are taken from the output of the specified task(s)


.. _decorators.split.output:

    * **output** = *output*
       Specifies the resulting output file name(s) after string substitution

       Can include glob patterns (e.g. ``"*.txt"``)

       | These are used **only** to check if the task is up to date.
       | Normally you would use either a |glob|_ (e.g. ``*.little_files`` as above) or  a "sentinel file"
         to indicate that the task has completed successfully.
       | You can of course do both:

        ::

            @split("big_file", ["sentinel.file", "*.little_files"])
            def split_big_to_small(input_file, output_files):
                pass


.. _decorators.split.extras:

    * **extras** = *extras*
       Any extra parameters are passed verbatim to the task function

       If you are using named parameters, these can be passed as a list, i.e. ``extras= [...]``

       Any extra parameters are consumed by the task function and not forwarded further down the pipeline.



.. warning::

    Deprecated since Ruffus v 2.5

    :red:`@split( input, output, filter =` ``regex(...)``, ``add_inputs(...)`` | ``inputs(...)``, :red:`[|extras|_,...]  )` is a synonym for :ref:`@subdivide <decorators.subdivide>`.

