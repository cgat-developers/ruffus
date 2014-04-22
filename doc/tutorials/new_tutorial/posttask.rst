.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: posttask; Tutorial

.. _new_manual.posttask:

####################################################################################################################################################
|new_manual.posttask.chapter_num|: Signal the completion of each stage of our pipeline with :ref:`@posttask <decorators.posttask>`
####################################################################################################################################################


.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@posttask <decorators.posttask>` syntax


***********************
Overview
***********************



    It is often useful to signal the completion of each task by specifying a specific
    action to be taken or function to be called. This can range from
    printing out some message, or  `touching  <http://en.wikipedia.org/wiki/Touch_(Unix)>`__ some sentinel file,
    to emailing the author. This is particular useful if the :term:`task` is a recipe apply to an unspecified number
    of parameters in parallel in different :term:`job`\ s. If the task is never run, or if it
    fails, needless-to-say no task completion action will happen.


    *Ruffus* uses the :ref:`@posttask <decorators.posttask>` decorator for this purpose.


=================
**@posttask**
=================

    We can signal the completion of each task by specifying
    one or more function(s) using :ref:`@posttask <decorators.posttask>` ::

        from ruffus import *

        def task_finished():
            print "hooray"

        @posttask(task_finished)
        @originate("a.1")
        def create_if_necessary(output_file):
            open(output_file, "w")

        pipeline_run([create_if_necessary])


    This is such a short function, we might as well write it in-line:

        ::

            @posttask(lambda: sys.stdout.write("hooray\n"))
            @originate("a.1")
            def create_if_necessary(output_file):
                open(output_file, "w")


.. note::

    The function(s) provided to :ref:`@posttask <decorators.posttask>` will be called if the pipeline passes
    through a task, even if none of its jobs are run because they are up-to-date.
    This happens when a upstream task is out-of-date, and the execution passes through
    this point in the pipeline. See the example in :ref:`new_manual.dependencies`
    of this manual.


.. index::
    single: @posttask; touchfile (Manual)
    single: touchfile ; @posttask (Manual)


.. _new_manual.posttask.touch_file:

============================================
:ref:`touch_file<decorators.touch_file>`
============================================

    One way to note the completion of a task is to create some sort of
    "flag" file. Each stage in a traditional ``make`` pipeline would contain a
    ``touch completed.flag``.

    This is such a useful idiom that *Ruffus* provides the shorthand :ref:`touch_file<decorators.touch_file>`:

        .. code-block:: python

            from ruffus import *

            @posttask(touch_file("task_completed.flag"))
            @files(None, "a.1")
            def create_if_necessary(input_file, output_file):
                open(output_file, "w")

            pipeline_run()

=======================================
Adding several post task actions
=======================================
    You can, of course, add more than one different action to be taken on completion of the
    task, either by stacking up as many :ref:`@posttask<decorators.posttask>` decorators
    as necessary, or by including several functions in the same :ref:`@posttask <decorators.posttask>`:

        .. code-block:: python

            from ruffus import *

            @posttask(print_hooray, print_whoppee)
            @posttask(print_hip_hip, touch_file("sentinel_flag"))
            @originate("a.1")
            def create_if_necessary(output_file):
                open(output_file, "w")

            pipeline_run()

