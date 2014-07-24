.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.pipeline_printout.code:

############################################################################################################################################################################################################
|new_manual.pipeline_printout.chapter_num|: Python Code for Understanding how your pipeline works with :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>`
############################################################################################################################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`pipeline_printout(...) <pipeline_functions.pipeline_printout>` syntax
    * Back to |new_manual.pipeline_printout.chapter_num|: :ref:`Understanding how your pipeline works <new_manual.pipeline_printout>`

******************************************
Display the initial state of the pipeline
******************************************
    ::

        from ruffus import *
        import sys

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

        pipeline_printout(sys.stdout, [second_task], verbose = 1)
        pipeline_printout(sys.stdout, [second_task], verbose = 3)

************************************
Normal Output
************************************
    ::

        >>> pipeline_printout(sys.stdout, [second_task], verbose = 1)

        ________________________________________
        Tasks which will be run:

        Task = create_initial_file_pairs
        Task = first_task
        Task = second_task


************************************
High Verbosity Output
************************************

    ::

        >>> pipeline_printout(sys.stdout, [second_task], verbose = 4)

        ________________________________________
        Tasks which will be run:

        Task = create_initial_file_pairs
               Job  = [None
                     -> job1.a.start
                     -> job1.b.start]
                 Job needs update: Missing files [job1.a.start, job1.b.start]
               Job  = [None
                     -> job2.a.start
                     -> job2.b.start]
                 Job needs update: Missing files [job2.a.start, job2.b.start]
               Job  = [None
                     -> job3.a.start
                     -> job3.b.start]
                 Job needs update: Missing files [job3.a.start, job3.b.start]

        Task = first_task
               Job  = [[job1.a.start, job1.b.start]
                     -> job1.a.output.1]
                 Job needs update: Missing files [job1.a.start, job1.b.start, job1.a.output.1]
               Job  = [[job2.a.start, job2.b.start]
                     -> job2.a.output.1]
                 Job needs update: Missing files [job2.a.start, job2.b.start, job2.a.output.1]
               Job  = [[job3.a.start, job3.b.start]
                     -> job3.a.output.1]
                 Job needs update: Missing files [job3.a.start, job3.b.start, job3.a.output.1]

        Task = second_task
               Job  = [job1.a.output.1
                     -> job1.a.output.2]
                 Job needs update: Missing files [job1.a.output.1, job1.a.output.2]
               Job  = [job2.a.output.1
                     -> job2.a.output.2]
                 Job needs update: Missing files [job2.a.output.1, job2.a.output.2]
               Job  = [job3.a.output.1
                     -> job3.a.output.2]
                 Job needs update: Missing files [job3.a.output.1, job3.a.output.2]

        ________________________________________

******************************************
Display the partially up-to-date pipeline
******************************************
    Run the pipeline, modify ``job1.stage`` so that the second task is no longer up-to-date
    and printout the pipeline stage again::

        >>> pipeline_run([second_task], verbose=3)
        Task enters queue = create_initial_file_pairs
            Job  = [None -> [job1.a.start, job1.b.start]]
            Job  = [None -> [job2.a.start, job2.b.start]]
            Job  = [None -> [job3.a.start, job3.b.start]]
            Job  = [None -> [job1.a.start, job1.b.start]] completed
            Job  = [None -> [job2.a.start, job2.b.start]] completed
            Job  = [None -> [job3.a.start, job3.b.start]] completed
        Completed Task = create_initial_file_pairs
        Task enters queue = first_task
            Job  = [[job1.a.start, job1.b.start] -> job1.a.output.1]
            Job  = [[job2.a.start, job2.b.start] -> job2.a.output.1]
            Job  = [[job3.a.start, job3.b.start] -> job3.a.output.1]
            Job  = [[job1.a.start, job1.b.start] -> job1.a.output.1] completed
            Job  = [[job2.a.start, job2.b.start] -> job2.a.output.1] completed
            Job  = [[job3.a.start, job3.b.start] -> job3.a.output.1] completed
        Completed Task = first_task
        Task enters queue = second_task
            Job  = [job1.a.output.1 -> job1.a.output.2]
            Job  = [job2.a.output.1 -> job2.a.output.2]
            Job  = [job3.a.output.1 -> job3.a.output.2]
            Job  = [job1.a.output.1 -> job1.a.output.2] completed
            Job  = [job2.a.output.1 -> job2.a.output.2] completed
            Job  = [job3.a.output.1 -> job3.a.output.2] completed
        Completed Task = second_task


        # modify job1.stage1
        >>> open("job1.a.output.1", "w").close()

    At a verbosity of 6, even jobs which are up-to-date will be displayed::

        >>> pipeline_printout(sys.stdout, [second_task], verbose = 6)

        ________________________________________
        Tasks which are up-to-date:

        Task = create_initial_file_pairs
               Job  = [None
                     -> job1.a.start
                     -> job1.b.start]
               Job  = [None
                     -> job2.a.start
                     -> job2.b.start]
               Job  = [None
                     -> job3.a.start
                     -> job3.b.start]

        Task = first_task
               Job  = [[job1.a.start, job1.b.start]
                     -> job1.a.output.1]
               Job  = [[job2.a.start, job2.b.start]
                     -> job2.a.output.1]
               Job  = [[job3.a.start, job3.b.start]
                     -> job3.a.output.1]

        ________________________________________



        ________________________________________
        Tasks which will be run:

        Task = second_task
               Job  = [job1.a.output.1
                     -> job1.a.output.2]
                 Job needs update:
                 Input files:
                  * 22 Jul 2014 15:29:19.33: job1.a.output.1
                 Output files:
                  * 22 Jul 2014 15:29:07.53: job1.a.output.2

               Job  = [job2.a.output.1
                     -> job2.a.output.2]
               Job  = [job3.a.output.1
                     -> job3.a.output.2]

        ________________________________________



    We can now see that the there is only one job in "second_task" which needs to be re-run
    because 'job1.stage1' has been modified after 'job1.stage2'
