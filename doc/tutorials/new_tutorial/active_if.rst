.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: @active_if; Tutorial

.. _new_manual.active_if:

##########################################################################################################################################
|new_manual.active_if.chapter_num|: Turning parts of the pipeline on and off at runtime with :ref:`@active_if <decorators.active_if>`
##########################################################################################################################################


.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@active_if syntax in detail <decorators.active_if>`


***************************************
Overview
***************************************

    It is sometimes useful to be able to switch on and off parts of a pipeline. For example, a pipeline
    might have two difference code paths depending on the type of data it is being asked to analyse.

    One surprisingly easy way to do this is to use a python ``if`` statement around particular task functions:

        .. code-block:: python
           :emphasize-lines: 3,5

            from ruffus import *

            run_task1 = True

            @originate(['a.foo', 'b.foo'])
            def create_files(output_file):
                open(output_file, "w")


            if run_task1:
                # might not run
                @transform(create_files, suffix(".foo"), ".bar")
                def foobar(input_file, output_file):
                    open(output_file, "w")


            @transform(foobar, suffix(".bar"), ".result")
            def wrap_up(input_file, output_file):
                    open(output_file, "w")


            pipeline_run()


    This simple solution has a number of drawbacks:
        #. The on/off decision is a one off event that happens when the script is loaded. Ideally, we
           would like some flexibility, and postpone the decision until ``pipeline_run()`` is invoked.
        #. When ``if`` is false, the entire task function becomes invisible, and if there are any
           downstream tasks, as in the above example, *Ruffus* will complain loudly about
           missing dependencies.


******************************************************************************
:ref:`@active_if <decorators.active_if>`  controls the state of tasks
******************************************************************************


    * Switches tasks on and off at run time depending on its parameters
    * Evaluated each time ``pipeline_run``, ``pipeline_printout`` or ``pipeline_printout_graph`` is called.
    * Dormant tasks behave as if they are up to date and have no output.

    The Design and initial implementation were contributed by Jacob Biesinger

    The following example shows its flexibility and syntax:

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


    The task starts off inactive:


        .. code-block:: pycon
            :emphasize-lines: 1

            >>> # @active_if switches off task "this_task_might_be_inactive" because run_if_true_2 == False
            >>> pipeline_run(verbose = 3)

            Task enters queue = create_files
            create_files
                Job  = [None -> a.foo] Missing file [a.foo]
                Job  = [None -> b.foo] Missing file [b.foo]
                Job  = [None -> a.foo] completed
                Job  = [None -> b.foo] completed
            Completed Task = create_files
            Inactive Task = this_task_might_be_inactive

    Now turn on the task:

        .. code-block:: pycon
            :emphasize-lines: 1

            >>> # @active_if switches on task "this_task_might_be_inactive" because all run_if_true conditions are met
            >>> run_if_true_2 = True
            >>> pipeline_run(verbose = 3)

            Task enters queue = this_task_might_be_inactive

                Job  = [a.foo -> a.bar] Missing file [a.bar]
                Job  = [b.foo -> b.bar] Missing file [b.bar]
                Job  = [a.foo -> a.bar] completed
                Job  = [b.foo -> b.bar] completed
            Completed Task = this_task_might_be_inactive

