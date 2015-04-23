.. include:: ../global.inc
.. _decorators.active_if:
.. index::
    pair: @active_if; Syntax

.. seealso::

    * :ref:`@active_if <new_manual.active_if>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators


############
active_if
############

.. Comment. These are parameter names

.. |on_or_off| replace:: `on_or_off`
.. _on_or_off: `decorators.active_if.on_or_off`_

***************************************************************************************************************************************************
*@active_if*\ (on_or_off1, [on_or_off2,...])
***************************************************************************************************************************************************
    **Purpose:**

        * Switches tasks on and off at run time depending on its parameters
        * Evaluated each time ``pipeline_run``, ``pipeline_printout`` or ``pipeline_printout_graph`` is called.
        * The Design and initial implementation were contributed by Jacob Biesinger
        * Dormant tasks behave as if they are up to date and have no output.

    **Example**:

        .. code-block:: python
            :emphasize-lines: 20

            from ruffus import *
            run_if_true_1 = True
            run_if_true_2 = False
            run_if_true_3 = True


            #
            #    task1
            #
            @originate(['a.foo', 'b.foo'])
            def create_files(outfile):
                """
                create_files
                """
                open(outfile, "w").write(outfile + "\n")

            #
            #   Only runs if all three run_if_true conditions are met
            #
            #   @active_if determines if task is active
            @active_if(run_if_true_1, lambda: run_if_true_2)
            @active_if(run_if_true_3)
            @transform(create_files, suffix(".foo"), ".bar")
            def this_task_might_be_inactive(infile, outfile):
                open(outfile, "w").write("%s -> %s\n" % (infile, outfile))


            # @active_if switches off task because run_if_true_2 == False
            pipeline_run(verbose = 3)

            # @active_if switches on task because all run_if_true conditions are met
            run_if_true_2 = True
            pipeline_run(verbose = 3)


        Produces the following output:

            .. code-block:: pycon
                :emphasize-lines: 1,2,14,15

                >>> # @active_if switches off task "this_task_might_be_inactive"
                >>> # because run_if_true_2 == False
                >>> pipeline_run(verbose = 3)

                Task enters queue = create_files
                create_files
                    Job  = [None -> a.foo] Missing file [a.foo]
                    Job  = [None -> b.foo] Missing file [b.foo]
                    Job  = [None -> a.foo] completed
                    Job  = [None -> b.foo] completed
                Completed Task = create_files
                Inactive Task = this_task_might_be_inactive

                >>> # @active_if switches on task "this_task_might_be_inactive"
                >>> # because all run_if_true conditions are met
                >>> run_if_true_2 = True
                >>> pipeline_run(verbose = 3)

                Task enters queue = this_task_might_be_inactive

                    Job  = [a.foo -> a.bar] Missing file [a.bar]
                    Job  = [b.foo -> b.bar] Missing file [b.bar]
                    Job  = [a.foo -> a.bar] completed
                    Job  = [b.foo -> b.bar] completed
                Completed Task = this_task_might_be_inactive


    **Parameters:**

.. _decorators.active_if.on_or_off:

    * *on_or_off*:
        A comma separated list of boolean conditions. These can be values, functions or callable objects which return True / False

        Multiple ``@active_if`` decorators can be stacked for clarity as in the example


