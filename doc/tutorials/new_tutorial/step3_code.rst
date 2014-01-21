.. include:: ../../global.inc
.. _New_Tutorial_3nd_step_code:

######################################################################################################################################
New Tutorial in revision Code for Step 3: More on ``@transform``-ing data
######################################################################################################################################

* :ref:`New tutorial overview <New_Tutorial>`
* :ref:`Back to Step 3 <New_Tutorial_3rd_step>`

**********************************************
Using ``@originate``
**********************************************
    ::

        from ruffus import *

        #---------------------------------------------------------------
        #   create initial files
        #
        @originate([   ['job1.a.start', 'job1.b.start'],
                       ['job2.a.start', 'job2.b.start'],
                       ['job3.a.start', 'job3.b.start']    ])
        def create_initial_file_pairs(output_files):
            # create both files as necessary
            for output_file in output_files:
                with open(output_file, "w") as oo: pass

        #---------------------------------------------------------------
        #   first task
        @transform(create_initial_file_pairs, suffix(".start"), ".output.1")
        def first_task(input_files, output_file):
            with open(output_file, "w"): pass


        #---------------------------------------------------------------
        #   second task
        @transform(first_task, suffix(".output.1"), ".output.2")
        def second_task(input_files, output_file):
            with open(output_file, "w"): pass

        #
        #       Run
        #
        pipeline_run([second_task])


************************************
Resulting Output
************************************

    ::

            Job  = [None -> [job1.a.start, job1.b.start]] completed
            Job  = [None -> [job2.a.start, job2.b.start]] completed
            Job  = [None -> [job3.a.start, job3.b.start]] completed
        Completed Task = create_initial_file_pairs
            Job  = [[job1.a.start, job1.b.start] -> job1.a.output.1] completed
            Job  = [[job2.a.start, job2.b.start] -> job2.a.output.1] completed
            Job  = [[job3.a.start, job3.b.start] -> job3.a.output.1] completed
        Completed Task = first_task
            Job  = [job1.a.output.1 -> job1.a.output.2] completed
            Job  = [job2.a.output.1 -> job2.a.output.2] completed
            Job  = [job3.a.output.1 -> job3.a.output.2] completed
        Completed Task = second_task

