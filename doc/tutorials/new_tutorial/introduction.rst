.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: overview; Tutorial

.. _new_manual.introduction:

######################################################################################################
|new_manual.introduction.chapter_num|: An introduction to basic Ruffus syntax
######################################################################################################



************************************
Overview
************************************

    .. image:: ../../images/theoretical_pipeline_schematic.png
       :scale: 50

    Computational pipelines transform your data in stages until the final result is produced. One easy way to understand pipelines is by imagining your data flowing across a series of pipes until it reaches its final destination. Even quite complicated processes can be simplified if we broke things down into simple stages. Of course, it helps if we can visualise the whole process.

    Ruffus is a way of automating the plumbing in your pipeline: You supply the python functions which perform the data transformation, and tell Ruffus how these pipeline ``task`` functions are connected up. Ruffus will make sure that the right data flows down your pipeline in the right way at the right time.


    .. note::

        Ruffus refers to each stage of your pipeline as a :term:`task`.

***************************************
A gentle introduction to Ruffus syntax
***************************************

    | Let us start with the usual "Hello World" programme.
    | We have the following two python functions which
      we would like to turn into an automatic pipeline:


        ::

            def first_task():
                print "# Hello "

            def second_task():
                print "# World"


    The simplest **Ruffus** pipeline would look like this:

        .. code-block:: python
           :emphasize-lines: 1,6,10

            from ruffus import *

            def first_task():
                print "# Hello "

            @follows(first_task)
            def second_task():
                print "# World"

            pipeline_run([second_task])


    This is clearer if we annotate the ``Ruffus`` bits:


        .. image:: ../../images/tutorial_step1_follows.png
           :scale: 100



    The functions which do the actual work of each stage of the pipeline remain unchanged.
    The role of **Ruffus** is to make sure these functions are called in the right order,
    with the right parameters, running in parallel using multiprocessing if desired.

    There are three simple parts to building a **ruffus** pipeline

        #. ``import ruffus``
        #. "Decorating" functions which are part of the pipeline
        #. Running the pipeline

.. index::
    pair: decorators; Tutorial


.. _manual.introduction.import:

.. index::
    single: importing ruffus


****************************
Importing ruffus
****************************

    The most convenient way to use ruffus is to import the various names directly:

        ::

            from ruffus import *

    This will allow **ruffus** terms to be used directly in your code. This is also
    the style we have adopted for this manual.

    .. csv-table::
       :header: "Category", "Terms"
       :stub-columns: 1

       "*Pipeline functions*", "
       ::

         pipeline_printout
         pipeline_printout_graph
         pipeline_run"
       "*Decorators*", "
       ::

        @split
        @transform
        @merge
        @subdivide
        @collate
        @follows
        @posttask
        @mkdir
        @jobs_limit
        @parallel
        @check_if_uptodate
        @files
        @files_re"
       "*Loggers*", "
       ::

         stderr_logger
         black_hole_logger"
       "*Parameter disambiguating Indicators*", "
       ::

         suffix
         regex
         formatter
         inputs
         touch_file
         combine
         mkdir
         output_from"

If any of these clash with names in your code, you can use qualified names instead:
        ::

            import ruffus

            ruffus.pipeline_printout("...")

****************************
"Decorators"
****************************

    You need to tag or add a :term:`decorator` to existing code to tell **Ruffus** that they are part
    of the pipeline.

    .. note::

        python :term:`decorator`\ s are ways to tag or mark out functions.

        They start with a ``@`` prefix and take a number of parameters in parenthesis.

        .. image:: ../../images/tutorial_step1_decorator_syntax.png

    For example, the **ruffus** decorator :ref:`@follows <decorators.follows>` makes sure that
    ``second_task`` follows ``first_task``.


    | Multiple :term:`decorator`\ s can be used for each :term:`task` function to add functionality
      to *Ruffus* pipeline functions.
    | However, the decorated python functions can still be
      called normally, outside of *Ruffus*.
    | *Ruffus* :term:`decorator`\ s can be added to (stacked on top of) any function in any order.

    * :ref:`More on @follows in the in the Ruffus `Manual <manual.follows>`
    * :ref:`@follows syntax in detail <decorators.follows>`


.. index::
    pair: pipeline_run; Tutorial

****************************
Running the pipeline
****************************

    When you need to run the pipeline, Ruffus will find the the **last** stage (:term:`task` function) 
    of your pipeline, work out what other functions this depends on, following the appropriate chain of
    dependencies automatically, making sure that the entire pipeline is up-to-date.

    For clarity we will specify the **last** stage, i.e. ``second_task()`` explicitly.
    Because ``second_task`` depends on ``first_task``, both functions are executed in order.

        ::

            >>> pipeline_run([second_task], verbose = 1)

    Ruffus by default prints out the ``verbose`` progress through the pipelined code,
    interleaved with the "**# Hello**" printed by ``first_task`` and "**# World**" printed
    by ``second_task``.



        .. code-block:: python
           :emphasize-lines: 3,7

            >>> pipeline_run([second_task], verbose = 1)
            Start Task = first_task
            # Hello
                Job completed
            Completed Task = first_task
            Start Task = second_task
            # World
                Job completed
            Completed Task = second_task



