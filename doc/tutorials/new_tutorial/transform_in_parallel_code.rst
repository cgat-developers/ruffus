.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.transform_in_parallel.code:

######################################################################################################
|new_manual.transform_in_parallel.chapter_num|: Python Code for More on ``@transform``-ing data
######################################################################################################

.. seealso::


    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`@transform syntax in detail <decorators.transform>`
    * Back to |new_manual.transform_in_parallel.chapter_num|: :ref:`More on @transform-ing data and @originate <new_manual.transform_in_parallel>`

*******************************************
Producing several items / files per job
*******************************************

    ::

        from ruffus import *

        #---------------------------------------------------------------
        #   Create pairs of input files
        #
        first_task_params = [
                             ['job1.a.start', 'job1.b.start'],
                             ['job2.a.start', 'job2.b.start'],
                             ['job3.a.start', 'job3.b.start'],
                            ]

        for input_file_pairs in first_task_params:
            for input_file in input_file_pairs:
                open(input_file, "w")


        #---------------------------------------------------------------
        #
        #   first task
        #
        @transform(first_task_params, suffix(".start"),
                                [".output.1",
                                 ".output.extra.1"],
                               "some_extra.string.for_example", 14)
        def first_task(input_files, output_file_pair,
                        extra_parameter_str, extra_parameter_num):
            for output_file in output_file_pair:
                with open(output_file, "w"):
                    pass


        #---------------------------------------------------------------
        #
        #   second task
        #
        @transform(first_task, suffix(".output.1"), ".output2")
        def second_task(input_files, output_file):
            with open(output_file, "w"): pass


        #---------------------------------------------------------------
        #
        #       Run
        #
        pipeline_run([second_task])

=============================
Resulting Output
=============================

        ::

            >>> pipeline_run([second_task])
                Job  = [[job1.a.start, job1.b.start] -> [job1.a.output.1, job1.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job2.a.start, job2.b.start] -> [job2.a.output.1, job2.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job3.a.start, job3.b.start] -> [job3.a.output.1, job3.a.output.extra.1], some_extra.string.for_example, 14] completed
            Completed Task = first_task
                Job  = [[job1.a.output.1, job1.a.output.extra.1] -> job1.a.output2] completed
                Job  = [[job2.a.output.1, job2.a.output.extra.1] -> job2.a.output2] completed
                Job  = [[job3.a.output.1, job3.a.output.extra.1] -> job3.a.output2] completed
            Completed Task = second_task



*******************************************
Defining tasks function out of order
*******************************************

    .. code-block:: python
       :emphasize-lines: 22

        from ruffus import *

        #---------------------------------------------------------------
        #   Create pairs of input files
        #
        first_task_params = [
                             ['job1.a.start', 'job1.b.start'],
                             ['job2.a.start', 'job2.b.start'],
                             ['job3.a.start', 'job3.b.start'],
                            ]

        for input_file_pairs in first_task_params:
            for input_file in input_file_pairs:
                open(input_file, "w")



        #---------------------------------------------------------------
        #
        #   second task defined first
        #
        #   task name string wrapped in output_from(...)
        @transform(output_from("first_task"), suffix(".output.1"), ".output2")
        def second_task(input_files, output_file):
            with open(output_file, "w"): pass


        #---------------------------------------------------------------
        #
        #   first task
        #
        @transform(first_task_params, suffix(".start"),
                                [".output.1",
                                 ".output.extra.1"],
                               "some_extra.string.for_example", 14)
        def first_task(input_files, output_file_pair,
                        extra_parameter_str, extra_parameter_num):
            for output_file in output_file_pair:
                with open(output_file, "w"):
                    pass


        #---------------------------------------------------------------
        #
        #       Run
        #
        pipeline_run([second_task])


=============================
Resulting Output
=============================

        .. code-block:: pycon

            >>> pipeline_run([second_task])
                Job  = [[job1.a.start, job1.b.start] -> [job1.a.output.1, job1.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job2.a.start, job2.b.start] -> [job2.a.output.1, job2.a.output.extra.1], some_extra.string.for_example, 14] completed
                Job  = [[job3.a.start, job3.b.start] -> [job3.a.output.1, job3.a.output.extra.1], some_extra.string.for_example, 14] completed
            Completed Task = first_task
                Job  = [[job1.a.output.1, job1.a.output.extra.1] -> job1.a.output2] completed
                Job  = [[job2.a.output.1, job2.a.output.extra.1] -> job2.a.output2] completed
                Job  = [[job3.a.output.1, job3.a.output.extra.1] -> job3.a.output2] completed
            Completed Task = second_task

.. _new_manual.transform.multiple_dependencies.code:

*******************************************
Multiple dependencies
*******************************************

    .. code-block:: python
       :emphasize-lines: 58

        from ruffus import *
        import time
        import random

        #---------------------------------------------------------------
        #   Create pairs of input files
        #
        first_task_params = [
                             ['job1.a.start', 'job1.b.start'],
                             ['job2.a.start', 'job2.b.start'],
                             ['job3.a.start', 'job3.b.start'],
                            ]
        second_task_params = [
                             ['job4.a.start', 'job4.b.start'],
                             ['job5.a.start', 'job5.b.start'],
                             ['job6.a.start', 'job6.b.start'],
                            ]

        for input_file_pairs in first_task_params + second_task_params:
            for input_file in input_file_pairs:
                open(input_file, "w")



        #---------------------------------------------------------------
        #
        #   first task
        #
        @transform(first_task_params, suffix(".start"),
                                [".output.1",
                                 ".output.extra.1"],
                               "some_extra.string.for_example", 14)
        def first_task(input_files, output_file_pair,
                        extra_parameter_str, extra_parameter_num):
            for output_file in output_file_pair:
                with open(output_file, "w"):
                    pass
            time.sleep(random.random())



        #---------------------------------------------------------------
        #
        #   second task
        #
        @transform(second_task_params, suffix(".start"),
                                [".output.1",
                                 ".output.extra.1"],
                               "some_extra.string.for_example", 14)
        def second_task(input_files, output_file_pair,
                        extra_parameter_str, extra_parameter_num):
            for output_file in output_file_pair:
                with open(output_file, "w"):
                    pass
            time.sleep(random.random())


        #---------------------------------------------------------------
        #
        #   third task
        #
        #       depends on both first_task() and second_task()
        @transform([first_task, second_task], suffix(".output.1"), ".output2")
        def third_task(input_files, output_file):
            with open(output_file, "w"): pass


        #---------------------------------------------------------------
        #
        #       Run
        #
        pipeline_run([third_task], multiprocess = 6)

=============================
Resulting Output
=============================

    .. code-block:: pycon

        >>> pipeline_run([third_task], multiprocess = 6)
            Job  = [[job3.a.start, job3.b.start] -> [job3.a.output.1, job3.a.output.extra.1], some_extra.string.for_example, 14] completed
            Job  = [[job6.a.start, job6.b.start] -> [job6.a.output.1, job6.a.output.extra.1], some_extra.string.for_example, 14] completed
            Job  = [[job1.a.start, job1.b.start] -> [job1.a.output.1, job1.a.output.extra.1], some_extra.string.for_example, 14] completed
            Job  = [[job4.a.start, job4.b.start] -> [job4.a.output.1, job4.a.output.extra.1], some_extra.string.for_example, 14] completed
            Job  = [[job5.a.start, job5.b.start] -> [job5.a.output.1, job5.a.output.extra.1], some_extra.string.for_example, 14] completed
        Completed Task = second_task
            Job  = [[job2.a.start, job2.b.start] -> [job2.a.output.1, job2.a.output.extra.1], some_extra.string.for_example, 14] completed
        Completed Task = first_task
            Job  = [[job1.a.output.1, job1.a.output.extra.1] -> job1.a.output2] completed
            Job  = [[job2.a.output.1, job2.a.output.extra.1] -> job2.a.output2] completed
            Job  = [[job3.a.output.1, job3.a.output.extra.1] -> job3.a.output2] completed
            Job  = [[job4.a.output.1, job4.a.output.extra.1] -> job4.a.output2] completed
            Job  = [[job5.a.output.1, job5.a.output.extra.1] -> job5.a.output2] completed
            Job  = [[job6.a.output.1, job6.a.output.extra.1] -> job6.a.output2] completed
        Completed Task = third_task


*******************************************
Multiple dependencies after @follows
*******************************************

    .. code-block:: python
        :emphasize-lines: 31

        from ruffus import *
        import time
        import random

        #---------------------------------------------------------------
        #   Create pairs of input files
        #
        first_task_params = [
                             ['job1.a.start', 'job1.b.start'],
                             ['job2.a.start', 'job2.b.start'],
                             ['job3.a.start', 'job3.b.start'],
                            ]
        second_task_params = [
                             ['job4.a.start', 'job4.b.start'],
                             ['job5.a.start', 'job5.b.start'],
                             ['job6.a.start', 'job6.b.start'],
                            ]

        for input_file_pairs in first_task_params + second_task_params:
            for input_file in input_file_pairs:
                open(input_file, "w")



        #---------------------------------------------------------------
        #
        #   first task
        #
        @transform(first_task_params, suffix(".start"),
                                [".output.1",
                                 ".output.extra.1"],
                               "some_extra.string.for_example", 14)
        def first_task(input_files, output_file_pair,
                        extra_parameter_str, extra_parameter_num):
            for output_file in output_file_pair:
                with open(output_file, "w"):
                    pass
            time.sleep(random.random())



        #---------------------------------------------------------------
        #
        #   second task
        #
        @follows("first_task")
        @transform(second_task_params, suffix(".start"),
                                [".output.1",
                                 ".output.extra.1"],
                               "some_extra.string.for_example", 14)
        def second_task(input_files, output_file_pair,
                        extra_parameter_str, extra_parameter_num):
            for output_file in output_file_pair:
                with open(output_file, "w"):
                    pass
            time.sleep(random.random())


        #---------------------------------------------------------------
        #
        #   third task
        #
        #       depends on both first_task() and second_task()
        @transform([first_task, second_task], suffix(".output.1"), ".output2")
        def third_task(input_files, output_file):
            with open(output_file, "w"): pass


        #---------------------------------------------------------------
        #
        #       Run
        #
        pipeline_run([third_task], multiprocess = 6)

=======================================================================================
Resulting Output: ``first_task`` completes before ``second_task``
=======================================================================================

    .. code-block:: pycon

        >>> pipeline_run([third_task], multiprocess = 6)
            Job  = [[job2.a.start, job2.b.start] -> [job2.a.output.1, job2.a.output.extra.1], some_extra.string.for_example, 14] completed
            Job  = [[job3.a.start, job3.b.start] -> [job3.a.output.1, job3.a.output.extra.1], some_extra.string.for_example, 14] completed
            Job  = [[job1.a.start, job1.b.start] -> [job1.a.output.1, job1.a.output.extra.1], some_extra.string.for_example, 14] completed
        Completed Task = first_task
            Job  = [[job4.a.start, job4.b.start] -> [job4.a.output.1, job4.a.output.extra.1], some_extra.string.for_example, 14] completed
            Job  = [[job6.a.start, job6.b.start] -> [job6.a.output.1, job6.a.output.extra.1], some_extra.string.for_example, 14] completed
            Job  = [[job5.a.start, job5.b.start] -> [job5.a.output.1, job5.a.output.extra.1], some_extra.string.for_example, 14] completed
        Completed Task = second_task
            Job  = [[job1.a.output.1, job1.a.output.extra.1] -> job1.a.output2] completed
            Job  = [[job2.a.output.1, job2.a.output.extra.1] -> job2.a.output2] completed
            Job  = [[job3.a.output.1, job3.a.output.extra.1] -> job3.a.output2] completed
            Job  = [[job4.a.output.1, job4.a.output.extra.1] -> job4.a.output2] completed
            Job  = [[job5.a.output.1, job5.a.output.extra.1] -> job5.a.output2] completed
            Job  = [[job6.a.output.1, job6.a.output.extra.1] -> job6.a.output2] completed
