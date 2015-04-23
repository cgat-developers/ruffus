.. include:: ../global.inc
.. _decorators.merge:
.. index::
    pair: @merge; Syntax

.. seealso::

    * :ref:`@merge <new_manual.merge>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

.. |input| replace:: `input`
.. _input: `decorators.merge.input`_
.. |extras| replace:: `extras`
.. _extras: `decorators.merge.extras`_
.. |output| replace:: `output`
.. _output: `decorators.merge.output`_

########################################################################
merge
########################################################################

************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
@merge ( |input|_, |output|_, [|extras|_,...] )
************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

    **Purpose:**
        Merges multiple |input|_ into a single |output|_.

        Only out of date tasks (comparing |input|_ and |output|_ files) will be run

    **Example**::

        @merge(previous_task, 'all.summary')
        def summarize(infiles, summary_file):
            pass

    **Parameters:**


.. _decorators.merge.input:

    * **input** = *tasks_or_file_names*
       can be a:

       #.  Task / list of tasks.
            File names are taken from the output of the specified task(s)
       #.  (Nested) list of file name strings.
            File names containing ``*[]?`` will be expanded as a |glob|_.
             E.g.:``"a.*" => "a.1", "a.2"``


.. _decorators.merge.output:

    * **output** = *output*
        Specifies the resulting output file name(s).

.. _decorators.merge.extras:

    * **extras** = *extras*
       Any extra parameters are passed verbatim to the task function

       If you are using named parameters, these can be passed as a list, i.e. ``extras= [...]``

       Any extra parameters are consumed by the task function and not forwarded further down the pipeline.



See :ref:`here <decorators.collate>` for more advanced uses of merging.


