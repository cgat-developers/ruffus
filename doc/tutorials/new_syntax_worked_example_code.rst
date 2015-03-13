.. _new_syntax.worked_example.code:

#################################################################################################################
Python Code for: New Object orientated syntax for Ruffus in Version 2.6
#################################################################################################################

    .. seealso::

        * :ref:`new_syntax.worked_example <new_syntax.worked_example>`

    This code is adapted from ``test/test_subpipeline.py`` in the **Ruffus** distribution


==============================================================================
Output
==============================================================================

    Let us save the script to ``test_subpipeline_cmdline.py``

    #) Try running the script as is:
        .. <<bash

        .. code-block:: bash

            # cleanup before and afterwards
            $ ./test_subpipeline_cmdline.py --cleanup
        ..
            bash

    #) If we printout the pipeline, we can see that, by default,
       the entire pipeline (with all its sub-pipelines) will run.

        .. <<bash

        .. code-block:: bash

            # grep Completed Tasks
            $ ./test_subpipeline_cmdline.py --cleanup --verbose 1 --just_print

            ________________________________________
            Tasks which will be run:

            Task = "pipeline1a::mkdir('tempdir/')   before task_originate "
            Task = "pipeline1a::mkdir('tempdir/testdir',   'tempdir/testdir2') #2   before task_originate "
            Task = 'pipeline1a::task_originate'
            Task = 'pipeline1a::add_input'
            Task = 'pipeline1a::22_to_33'
            Task = 'pipeline1a::33_to_44'
            Task = "pipeline1b::mkdir('tempdir/')   before task_originate "
            Task = "pipeline1b::mkdir('tempdir/testdir',   'tempdir/testdir2') #2   before task_originate "
            Task = 'pipeline1b::task_originate'
            Task = 'pipeline1b::add_input'
            Task = 'pipeline1b::22_to_33'
            Task = 'pipeline1b::33_to_44'
            Task = "pipeline1c::mkdir('tempdir/')   before task_originate "
            Task = "pipeline1c::mkdir('tempdir/testdir',   'tempdir/testdir2') #2   before task_originate "
            Task = 'pipeline1c::task_originate'
            Task = 'pipeline1c::add_input'
            Task = 'pipeline1c::22_to_33'
            Task = 'pipeline1c::33_to_44'
            Task = 'pipeline2::44_to_55'
            Task = 'pipeline2::task_m_to_1'

        ..
            bash

    .. code-block:: bash

    #) Specifying either the main ``pipeline2`` or the last task in ``pipeline2``  produces the same output. All the ancestral tasks in pipelines1a-c will be run automatically.

        .. <<bash

        .. code-block:: bash

            # grep Completed Tasks
            $ ./test_subpipeline_cmdline.py --cleanup --verbose 1 --just_print --target_tasks pipeline2

            $ ./test_subpipeline_cmdline.py --cleanup --verbose 1 --just_print --target_tasks pipeline2::task_m_to_1
        ..
            bash

    #) Specifying only ``pipeline1a`` or any task in ``pipeline1a``  in ``--target_tasks`` will only run the specified tasks in that subpipeline.

        .. <<bash

        .. code-block:: bash

            # grep Completed Tasks
            $ ./test_subpipeline_cmdline.py --cleanup --verbose 1 --just_print --target_tasks pipeline1a
            $ ./test_subpipeline_cmdline.py --cleanup --verbose 1 --just_print --forced_tasks pipeline1a::task_originate

            Task = "pipeline1a::mkdir('tempdir/')   before task_originate "
            Task = "pipeline1a::mkdir('tempdir/testdir',   'tempdir/testdir2') #2   before task_originate "
            Task = 'pipeline1a::task_originate'
            Task = 'pipeline1a::add_input'
            Task = 'pipeline1a::22_to_33'
            Task = 'pipeline1a::33_to_44'

        ..
            bash


==============================================================================
Code
==============================================================================
    .. <<python

    .. code-block:: python
        :emphasize-lines: 70,76-79,86,87,94,95,101,106-107,109,112-114,118,119,125,130,132,150,154,157,158,162

        #!/usr/bin/env python
        from __future__ import print_function
        """


                Demonstrates the new Ruffus syntax in version 2.6
        """

        import os
        import sys

        # add grandparent to search path for testing
        grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        sys.path.insert(0, grandparent_dir)

        import ruffus
        from ruffus import add_inputs, suffix, mkdir, regex, Pipeline, output_from, touch_file
        print("\tRuffus Version = ", ruffus.__version__)

        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

        #   imports


        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        import shutil


        def touch (outfile):
            with open(outfile, "w"):
                pass


        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

        #   Tasks


        #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
        tempdir = "tempdir/"
        def task_originate(o):
            """
            Makes new files
            """
            touch(o)

        def task_m_to_1(i, o):
            """
            Merges files together
            """
            with open(o, "w") as o_file:
                for f in sorted(i):
                    with open(f) as ii:
                        o_file.write(f +"=" + ii.read() + "; ")

        def task_1_to_1(i, o):
            """
            1 to 1 for transform
            """
            with open(o, "w") as o_file:
                with open(i) as ii:
                    o_file.write(i +"+" + ii.read())

        DEBUG_do_not_define_tail_task = False
        DEBUG_do_not_define_head_task = False

        import unittest

        #
        #   Returns a fully formed sub pipeline useable as a building block
        #
        def make_pipeline1(pipeline_name,   # Pipelines need to have a unique name
                           starting_file_names):
            test_pipeline = Pipeline(pipeline_name)

            #   We can change the starting files later using
            #          set_input() for transform etc.
            #       or set_output() for originate
            #   But it can be more convenient to just pass this to the function making the pipeline
            #
            test_pipeline.originate(task_originate, starting_file_names)\
                .follows(mkdir(tempdir), mkdir(tempdir + "testdir", tempdir + "testdir2"))\
                .posttask(touch_file(tempdir + "testdir/whatever.txt"))
            test_pipeline.transform(task_func   = task_m_to_1,
                                    name        = "add_input",
                                    # Lookup Task from function name task_originate()
                                    #   So long as this is unique in the pipeline
                                    input       = task_originate,
                                    filter      = regex(r"(.*)"),
                                    add_inputs  = add_inputs(tempdir + "testdir/whatever.txt"),
                                    output      = r"\1.22")
            test_pipeline.transform(task_func   = task_1_to_1,
                                    name        = "22_to_33",
                                    # Lookup Task from Task name
                                    #   Function name is not unique in the pipeline
                                    input       = output_from("add_input"),
                                    filter      = suffix(".22"),
                                    output      = ".33")
            tail_task = test_pipeline.transform(task_func   = task_1_to_1,
                                                name        = "33_to_44",
                                                # Ask Pipeline to lookup Task from Task name
                                                input       = test_pipeline["22_to_33"],
                                                filter      = suffix(".33"),
                                                output      = ".44")

            #   Set the tail task so that users of my sub pipeline can use it as a dependency
            #       without knowing the details of task names
            #
            #   Use Task() object directly without having to lookup
            test_pipeline.set_tail_tasks([tail_task])

            #   If we try to connect a Pipeline without tail tasks defined, we have to
            #       specify the exact task within the Pipeline.
            #   Otherwise Ruffus will not know which task we mean and throw an exception
            if DEBUG_do_not_define_tail_task:
                test_pipeline.set_tail_tasks([])

            # Set the head task so that users of my sub pipeline send input into it
            #   without knowing the details of task names
            test_pipeline.set_head_tasks([test_pipeline[task_originate]])

            return test_pipeline

        #
        #   Returns a fully formed sub pipeline useable as a building block
        #
        def make_pipeline2( pipeline_name = "pipeline2"):
            test_pipeline2 = Pipeline(pipeline_name)
            test_pipeline2.transform(task_func   = task_1_to_1,
                                     # task name
                                    name        = "44_to_55",
                                     # placeholder: will be replaced later with set_input()
                                    input       = None,
                                    filter      = suffix(".44"),
                                    output      = ".55")
            test_pipeline2.merge(   task_func   = task_m_to_1,
                                    input       = test_pipeline2["44_to_55"],
                                    output      = tempdir + "final.output",)

            # Set head and tail
            test_pipeline2.set_tail_tasks([test_pipeline2[task_m_to_1]])
            if not DEBUG_do_not_define_head_task:
                test_pipeline2.set_head_tasks([test_pipeline2["44_to_55"]])

            return test_pipeline2




        #   First two pipelines are created as separate instances by the make_pipeline1 function
        pipeline1a = make_pipeline1(pipeline_name = "pipeline1a", starting_file_names = [tempdir + ss for ss in ("a.1", "b.1")])
        pipeline1b = make_pipeline1(pipeline_name = "pipeline1b", starting_file_names = [tempdir + ss for ss in ("c.1", "d.1")])

        #   The Third pipeline is a clone of pipeline1b
        pipeline1c = pipeline1b.clone(new_name = "pipeline1c")

        #   Set the "originate" files for pipeline1c to ("e.1" and "f.1")
        #       Otherwise they would use the original ("c.1", "d.1")
        pipeline1c.set_output(output = [])
        pipeline1c.set_output(output = [tempdir + ss for ss in ("e.1", "f.1")])

        #   Join all pipeline1a-c to pipeline2
        pipeline2 = make_pipeline2()
        pipeline2.set_input(input = [pipeline1a, pipeline1b, pipeline1c])


        import ruffus.cmdline as cmdline
        parser = cmdline.get_argparse(description='Demonstrates the new Ruffus syntax in version 2.6')

        parser.add_argument('--cleanup', "-C",
                            action="store_true",
                            help="Cleanup before and after.")


        options = parser.parse_args()



        #  standard python logger which can be synchronised across concurrent Ruffus tasks
        logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)


        # if we are printing only
        if  not options.just_print and \
            not options.flowchart and \
            not options.touch_files_only:
            cmdline.run (options)
            sys.exit()

        #
        #   Cleanup beforehand
        #
        if options.cleanup:
            try:
                shutil.rmtree(tempdir)
            except:
                pass

        #
        #   Run
        #
        cmdline.run (options)

        #
        #   Cleanup Afterwards
        #
        if options.cleanup:
            try:
                shutil.rmtree(tempdir)
            except:
                pass





    ..
        python
