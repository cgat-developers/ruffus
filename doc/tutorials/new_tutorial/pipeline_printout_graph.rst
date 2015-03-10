.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: pipeline_printout_graph; Tutorial

.. _new_manual.pipeline_printout_graph:

############################################################################################################################################################################################################
|new_manual.pipeline_printout_graph.chapter_num|: Displaying the pipeline visually with :ref:`pipeline_printout_graph(...) <pipeline_functions.pipeline_printout_graph>`
############################################################################################################################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`pipeline_printout_graph(...) <pipeline_functions.pipeline_printout_graph>` syntax
    * :ref:`@graphviz(...) <decorators.graphviz>` syntax

.. note::

    Remember to look at the example code:

    * :ref:`new_manual.pipeline_printout_graph.code`

=============================================
Printing out a flowchart of our pipeline
=============================================

    It is all very well being able to trace the data flow through the pipeline as text.
    Sometimes, however, we need a bit of eye-candy!

    We can see a flowchart for our fledgling pipeline by executing:

        ::

            pipeline_printout_graph (   'flowchart.svg',
                                        'svg',
                                        [second_task],
                                        no_key_legend = False)

        .. image:: ../../images/simple_tutorial_stage5_flowchart.png
           :scale: 70


    Flowcharts can be printed in a large number of formats including ``jpg``, ``svg``, ``png`` and ``pdf``.


    .. note::

        Flowcharts rely on the ``dot`` programme from `Graphviz <http://www.graphviz.org/>`__.

        Please make sure this is installed.

    There are 8 standard colour schemes, but you can further customise all the colours to your satisfaction:


        .. image:: ../../images/flowchart_colour_schemes.png

    See :ref:`here <new_manual.flowchart_colours>` for example code.

================================================================
Command line options made easier with ``ruffus.cmdline``
================================================================


    If you are using ``ruffus.cmdline``, then you can easily ask for a flowchart from the command line:

        .. code-block:: bash

            your_script.py --flowchart pipeline_flow_chart.png


    The output format is deduced from the extension but can be specified manually:

        .. code-block:: bash

            # specify format. Otherwise, deduced from the extension
            your_script.py --flowchart pipeline_flow_chart.png --flowchart_format png

    Print the flow chart horizontally or vertically...

        .. code-block:: bash

            # flowchart proceeds from left to right , rather than from  top to bottom
            your_script.py --flowchart pipeline_flow_chart.png --draw_graph_horizontally

    ...with or without a key legend

        .. code-block:: bash

            # Draw key legend
            your_script.py --flowchart pipeline_flow_chart.png --key_legend_in_graph


=============================================
Horribly complicated pipelines!
=============================================
    Flowcharts are especially useful if you have really complicated pipelines, such as

        .. image:: ../../images/simple_tutorial_complex_flowchart.png
           :scale: 70


=============================================
Circular dependency errors in pipelines!
=============================================
    Especially, if the pipeline is not set up properly, and vicious circular dependencies
    are present:

        .. image:: ../../images/simple_tutorial_complex_flowchart_error.png
           :scale: 70


.. _new_manual.graphviz:

==========================================================================================
``@graphviz``: Customising the appearance of each task
==========================================================================================

    The graphic for each task can be further customised as you please by adding
    `graphviz attributes  <http://www.graphviz.org/doc/info/attrs.html>`__ such as the URL, shape, colour
    directly to that node using the decorator ```@graphviz``.

    For example, we can customise the graphic for ``myTask()`` to look like:

        .. image:: ../../images/history_html_flowchart.png
           :scale: 30

    by adding the requisite attributes as follows:



    .. code-block:: python


        @graphviz(URL='"http://cnn.com"', fillcolor = '"#FFCCCC"',
                        color = '"#FF0000"', pencolor='"#FF0000"', fontcolor='"#4B6000"',
                        label_suffix = "???", label_prefix = "What is this?<BR/> ",
                        label = "<What <FONT COLOR=\"red\">is</FONT>this>",
                        shape= "component", height = 1.5, peripheries = 5,
                        style="dashed")
        def Up_to_date_task2(infile, outfile):
            pass

        #   Can use dictionary if you wish...
        graphviz_params = {"URL":"http://cnn.com", "fontcolor": '"#FF00FF"'}
        @graphviz(**graphviz_params)
        def myTask(input,output):
            pass

    .. **


    You can even using HTML formatting in task names, including specifying line wraps (as in the above example),
    using the ``label`` parameter. However, HTML labels **must** be enclosed in ``<`` and ``>``.


          .. code-block:: python

            label = "<Line <BR/> wrapped task_name()>"

    Otherwise, you can also opt to keep the task name and wrap it with a prefix and suffix:

          .. code-block:: python

            label_suffix = "??? ", label_prefix = ": What is this?"

    The ``URL`` attribute allows the generation of clickable svg, and also client / server
          side image maps usable in web pages.
          See `Graphviz documentation  <http://www.graphviz.org/content/output-formats#dimap>`__



