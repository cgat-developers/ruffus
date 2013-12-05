.. include:: ../../global.inc
.. _Simple_Tutorial_2nd_step_code:


###################################################################
Code for Step 2: Transforming data in a pipeline with ``@transform``
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>`
* :ref:`Back to Step 2 <Simple_Tutorial_2nd_step>`

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
            def first_task(input_files, output_file_pairs,
                            extra_parameter_str, extra_parameter_num):
                with open(output_file, "w"): pass


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




************************************
Resulting Output
************************************
    ::

            >>> pipeline_run([second_task])
                Job  = [[job1.a.start, job1.b.start] -> job1.a.output.1] completed
                Job  = [[job2.a.start, job2.b.start] -> job2.a.output.1] completed
                Job  = [[job3.a.start, job3.b.start] -> job3.a.output.1] completed
            Completed Task = first_task

                Job  = [job1.a.output.1 -> job1.a.output.2] completed
                Job  = [job2.a.output.1 -> job2.a.output.2] completed
                Job  = [job3.a.output.1 -> job3.a.output.2] completed
            Completed Task = second_task
