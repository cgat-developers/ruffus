.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: transform; Tutorial

.. _new_manual.transform:

######################################################################################################
|new_manual.transform.chapter_num|: Transforming data in a pipeline with ``@transform``
######################################################################################################


.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@transform syntax in detail <decorators.transform>`

.. note::

    Remember to look at the example code:

    * :ref:`new_manual.transform.code`


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




************************************************************************
:ref:`@transform <decorators.transform>`
************************************************************************
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
Chaining multiple steps together
************************************

    Best of all, it is easy to add a third stage to our two step pipeline.

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


    The full source code can be found :ref:`here <new_manual.transform.code>`

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



************************************
**Input** and **Output** parameters
************************************

    **Ruffus** is able to chain together different tasks by taking the **Output** from one job
    and plugging it automatically as the **Input** of the next.

    The first two parameters of each job are the **Input** and **Output** parameters respectively.

    In the above example, we thus have:

        .. table:: Parameters for ``second_task()``

           ================   ====================  =============================================
             **Inputs**           **Outputs**             **Extra**
           ================   ====================  =============================================
           ``"job1.input"``    ``"job1.output1"``    ``"some_extra.string.for_example", 14``
           ``"job2.input"``    ``"job2.output1"``    ``"some_extra.string.for_example", 14``
           ``"job3.input"``    ``"job3.output1"``    ``"some_extra.string.for_example", 14``
           ================   ====================  =============================================



    **Extra** parameters are consumed by the task python function and not passed further on.

    If the **Input** and **Output** parameter contains strings, these will be interpreted as file names
    required by and produced by that job. As we shall see, the modification times of these file names
    indicate whether that part of the pipeline is up to date or needs to be rerun.

    Apart from this, **Ruffus** imposes no other restrictions on the parameters for jobs, which
    are passed verbatim to task functions.



