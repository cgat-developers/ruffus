.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: @parallel; Tutorial

.. _new_manual.deprecated_parallel:

####################################################################################################################################################
|new_manual.parallel.chapter_num|: Esoteric: Running jobs in parallel without files using :ref:`@parallel<decorators.parallel>`
####################################################################################################################################################


.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@parallel<decorators.parallel>` syntax in detail


.. _new_manual.parallel:

***************************************
**@parallel**
***************************************

    **@parallel** supplies parameters for multiple **jobs** exactly like :ref:`@files<new_manual.deprecated_files>` except that:

        #. The first two parameters are not treated like *inputs* and *ouputs* parameters,
           and strings are not assumed to be file names
        #. Thus no checking of whether each job is up-to-date is made using *inputs* and *outputs* files
        #. No expansions of |glob|_ patterns or *output* from previous tasks is carried out.

    This syntax is most useful when a pipeline stage does not involve creating or consuming any files, and
    you wish to forego the conveniences of :ref:`@files<new_manual.deprecated_files>`, :ref:`@transform<new_manual.transform>` etc.

    The following code performs some arithmetic in parallel:

        ::

            import sys
            from ruffus import *
            parameters = [
                             ['A', 1, 2], # 1st job
                             ['B', 3, 4], # 2nd job
                             ['C', 5, 6], # 3rd job
                         ]
            @parallel(parameters)
            def parallel_task(name, param1, param2):
                sys.stderr.write("    Parallel task %s: " % name)
                sys.stderr.write("%d + %d = %d\n" % (param1, param2, param1 + param2))

            pipeline_run([parallel_task])

        produces the following::

            Task = parallel_task
                Parallel task A: 1 + 2 = 3
                Job = ["A", 1, 2] completed
                Parallel task B: 3 + 4 = 7
                Job = ["B", 3, 4] completed
                Parallel task C: 5 + 6 = 11
                Job = ["C", 5, 6] completed


