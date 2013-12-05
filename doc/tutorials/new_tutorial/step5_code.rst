.. include:: ../../global.inc
.. _Simple_Tutorial_5th_step_graphical_code:


###################################################################
Code for Step 5: Displaying the pipeline visually
###################################################################
* :ref:`Simple tutorial overview <Simple_Tutorial>`
* :ref:`pipeline functions <pipeline_functions>` in detail
* :ref:`Back to Step 5 <Simple_Tutorial_5th_step_graphical>`

************************************
Code
************************************
    .. code-block:: python
        :emphasize-lines: 28, 51
        :linenos:

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

        #  Print graph before running pipeline

        #---------------------------------------------------------------
        #
        #       Show flow chart and tasks before running the pipeline
        #
        print "Show flow chart and tasks before running the pipeline"
        pipeline_printout_graph ( open("simple_tutorial_stage5_before.png", "w"),
                                 "png",
                                 [second_task],
                                 minimal_key_legend=True)

        #---------------------------------------------------------------
        #
        #       Run
        #
        pipeline_run([second_task])


        # modify job1.stage1
        open("job1.a.output.1", "w").close()


        #  Print graph after everything apart from ``job1.a.output.1`` is update

        #---------------------------------------------------------------
        #
        #       Show flow chart and tasks after running the pipeline
        #
        print "Show flow chart and tasks after running the pipeline"
        pipeline_printout_graph ( open("simple_tutorial_stage5_after.png", "w"),
                                 "png",
                                 [second_task],
                                 no_key_legend=True)


************************************
Resulting Flowcharts
************************************
   +-------------------------------------------------------------+-----------------------------------------------------------------------+
   | .. image:: ../../images/simple_tutorial_stage5_before.png   | .. image::  ../../images/simple_tutorial_stage5_after.png             |
   |           :alt: Before running the pipeline                 |     :alt: After running the pipeline                                  |
   |           :scale: 95                                        |     :scale: 95                                                        |
   |           :align: center                                    |     :align: center                                                    |
   |                                                             |                                                                       |
   | .. centered:: Before                                        | .. centered:: After                                                   |
   |                                                             |                                                                       |
   +-------------------------------------------------------------+-----------------------------------------------------------------------+

   +-------------------------------------------------------------------------------------------------------------------------------------+
   | .. image:: ../../images/tutorial_key.png                                                                                            |
   |           :alt: Legend key                                                                                                          |
   |           :scale: 50                                                                                                                |
   |           :align: center                                                                                                            |
   |                                                                                                                                     |
   | .. centered:: Legend                                                                                                                |
   |                                                                                                                                     |
   +-------------------------------------------------------------------------------------------------------------------------------------+
