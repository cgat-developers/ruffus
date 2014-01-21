.. include:: ../../global.inc
.. _New_Tutorial_2nd_step:

.. index::
    pair: @transform; Tutorial

######################################################################################################################################
New Tutorial in revision Step 2: Transforming data in a pipeline with ``@transform``
######################################################################################################################################

   * :ref:`New tutorial overview <New_Tutorial>`
   * :ref:`@transform syntax in detail <decorators.transform>`

.. note::

    Remember to look at the example code:

    * :ref:`Python Code for step 2 <New_Tutorial_2nd_step_code>`

***************************************
Overview
***************************************
    .. image:: ../../images/theoretical_pipeline_schematic.png
       :scale: 50

    Computational pipelines transform your data in stages until the final result is produced.
    Ruffus automates the plumbing in your pipeline. You supply the python functions which perform the data transformation,
    and tell Ruffus how these pipeline stages or :term:`task` functions are connected together.

    .. note::

        **The best way to design a pipeline is to:**

            * **write down the file names of the data as it flows across your pipeline**
            * **write down the names of functions which transforms the data at each stage of the pipeline.**


    By letting **Ruffus** manage your pipeline parameters, you will get the following features
    for free:

        #. only out-of-date parts of the pipeline will be re-run
        #. multiple jobs can be run in parallel (on different processors if possible)
        #. pipeline stages can be chained together automatically




************************************
@transform
************************************
    Let us start with the simplest pipeline with a single *input* data file **transform**\ed
    into a single *output* file. We will add some arbitrary extra parameters as well.

    The :ref:`@transform <decorators.transform>` decorator tells Ruffus that this
    task function **transforms** each and every piece of input data into a corresponding output.

        In other words, inputs and outputs have a **1 to 1** relationship.


    Let us provide **input**\s and **output**\s to our new pipeline:

        .. code-block:: python
           :emphasize-lines: 7,9,11,12
           :linenos:

            from ruffus import *

            # Start with some initial data file of yours...
            initial_file = "job1.input"
            open(initial_file, "w")

            #Ruffus decorator
            @transform(
                        initial_file,             # input
                        suffix(".input"),
                        ".output1",               # output
                        "an.extra.parameter", 14) # extra parameters
            def first_task(input_file, output_file,
                            extra_str_parameter, extra_int_parameter):
                pass


            pipeline_run([first_task])



        .. :: .. image:: ../../images/simple_tutorial_step2_ex1.png

    The ``@transform`` decorator tells Ruffus to generate appropriate arguments for our python function:

        * The input file name is as given: ``job1.input``
        * The output file name is the input file name with its **suffix** of ``.input`` replaced with ``.output1``
        * There are two extra parameters, a string and a number.

    This is exactly equivalent to the following function call:

        ::

            first_task('job1.input', 'job1.output1', "some_extra.string.for_example", 14)


    Even though this (empty) function doesn't really *do* anything just yet, the output from **Ruffus** ``pipeline_run`` shows at least that this part of the pipeline completed successfully:

        .. code-block:: python

           >>> pipeline_run([first_task])
                Job  = [job1.input -> job1.output1, an.extra.parameter, 14] completed
           Completed Task = first_task


        .. :: .. image:: ../../images/simple_tutorial_step2_ex2.png


************************************
Task functions as recipes
************************************
    This may seem like a lot of effort and complication for something so simple: a normal python function call.
    However, now that we have annotated a task, we can start using it as part of our computational pipeline:


    Each :term:`task` function of the pipeline is a recipe or
    `rule <http://www.gnu.org/software/make/manual/make.html#Rule-Introduction>`_
    which can be applied repeatedly to our data.

    For example, one can have

        * a ``compile()`` *task* which will compile any number of source code files, or
        * a ``count_lines()`` *task* which will count the number of lines in any file or
        * an ``align_dna()`` *task* which will align the DNA of many chromosomes.

    .. note ::

        **Key Ruffus Terminology**:

        A  :term:`task` is an annotated python function which represents a recipe or stage of your pipeline.

        A  :term:`job` is each time your recipe is applied to a piece of data, i.e. each time Ruffus calls your function.

        Each **task** or pipeline recipe can thus have many **jobs** each of which can work in parallel on different data.

    In the original example, we have made a single output file by supplying a single input parameter.
    We shall use much the same syntax to apply the same recipe to *multiple* input files.
    Instead of providing a single *input*, and a single *output*, we are going to specify
    the parameters for *three* jobs at once:

        .. code-block:: python
           :emphasize-lines: 3

            # original example code
            # first_task_params = 'job1.input'

            # three files at once
            first_task_params = [
                                'job1.input',
                                'job2.input'
                                'job3.input'
                                ]

            # make sure the input files are there
            open('job1.input', "w")
            open('job2.input', "w")
            open('job3.input', "w")

            pipeline_run([first_task])


    .. :: .. image:: ../../images/simple_tutorial_files3.png



    Just by changing the inputs from a single file to a list of three files, we now have a pipeline which runs independently on three pieces of data.
    The results should look familiar:

        ::

            >>> pipeline_run([first_task])
                Job  = [job1.input -> job1.output1,
                        some_extra.string.for_example, 14] completed
                Job  = [job2.input -> job2.output1,
                        some_extra.string.for_example, 14] completed
                Job  = [job3.input -> job3.output1,
                        some_extra.string.for_example, 14] completed
            Completed Task = first_task


************************************
Multiple steps
************************************

    Best of all, it is easy to add another step to our initial pipeline.

    We have to

        * add another ``@transform`` decorated function (``second_task()``),
        * specify ``first_task()`` as the source:
        * use a ``suffix`` which matches the output from ``first_task()``


        ::

            @transform(first_task, suffix(".output1"), ".output2")
            def second_task(input_file, output_file):
                # make output file
                open(output_file, "w")

        * call ``pipeline_run()`` with the correct final task (``second_task()``)


    The full source code can be found :ref:`here <New_Tutorial_2nd_step_code>`

    With very little effort, we now have three independent pieces of information coursing through our pipeline.
    Because ``second_task()`` *transforms* the output from ``first_task()``, it magically knows its dependencies and
    that it too has to work on three jobs.


        ::

            >>> pipeline_run([second_task])
                Job  = [job1.input -> job1.output1, some_extra.string.for_example, 14] completed
                Job  = [job2.input -> job2.output1, some_extra.string.for_example, 14] completed
                Job  = [job3.input -> job3.output1, some_extra.string.for_example, 14] completed
            Completed Task = first_task
                Job  = [job1.output1 -> job1.output2] completed
                Job  = [job2.output1 -> job2.output2] completed
                Job  = [job3.output1 -> job3.output2] completed
            Completed Task = second_task




.. index::
    pair: input / output parameters; Tutorial

***************************************
@transform is a 1 to 1 operation
***************************************


    ``@transform`` is a 1:1 operation because for each input, it generates one output.

    This is obvious when you count the number of jobs at each step. In our example pipeline, there are always
    three jobs at each step (task).

    Each input or output is not limited, however, to a single filename. Each job can accept, for example,
    a pair of files as its input, or generate more than one file or a dictionary or numbers as its output.

    When each job outputs a pair of files, this does not generate two jobs downstream. It just means that the successive
    task in the pipeline will receive a list or tuple of files as its input parameter.

    .. note::

        The different sort of decorators in Ruffus determine the *topology* of your pipeline, i.e. how the jobs from different tasks are linked together seamlessly.

        In the later parts of the tutorial, we will encounter more decorators which can *split up*, or *join together* or *group* inputs.

            In other words, inputs and output can have **many to one**, **many to many** etc. relationships.


*******************************************
Producing several items / files per job
*******************************************

    Let us demonstrate this by modifying our previous example:
        * ``first_task_params`` is changed to 3 *pairs* of file names
        * ``@transform`` for ``first_task`` is modified to produce *pairs* of file names
            * ``.output.1``
            * ``.output.extra.1``


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

        This gives the following results:

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



        We see that apart from having a file pair where previously there was a single file,
        little else has changed. We still have three pieces of data going through the
        pipeline in three parallel jobs.
