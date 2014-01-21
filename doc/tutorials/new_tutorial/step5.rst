.. include:: ../../global.inc
.. _Simple_Tutorial_5th_step_graphical:



######################################################################################################################################
New Tutorial in revision Step 5: Displaying the pipeline visually
###################################################################

    * :ref:`Simple tutorial overview <Simple_Tutorial>`
    * :ref:`pipeline functions <pipeline_functions>` in detail

.. note::
    Remember to look at the example code:

    * :ref:`Python Code for step 5 <Simple_Tutorial_5th_step_graphical_code>`

.. index::
    pair: pipeline_printout; Tutorial



.. index::
    pair: pipeline_printout_graph; Tutorial

=============================================
Printing out a flowchart of our pipeline
=============================================

    It is all very well being able to trace the data flow through the pipeline.
    Sometimes, however, we need a bit of eye-candy.

    We can see this flowchart of our fledgling pipeline by executing:

        ::

            pipeline_printout_graph (   'flowchart.svg',
                                        'svg',
                                        [second_task],
                                        no_key_legend = False)

        .. image:: ../../images/simple_tutorial_stage5_flowchart.png


    Flowcharts can be printed in a large number of formats including jpg, svg,
    png and pdf provided that the ``dot`` programme from
    `Graphviz <http://www.graphviz.org/>`_ is installed.


    There are 8 standard colour schemes, but you can further customise all the colours to your satisfaction:


        .. image:: ../../images/flowchart_colour_schemes.png

    See :ref:`here <flowchart_colours>` for example code.

================================================================
Command line options made easier with ``ruffus.cmdline``
================================================================


    If you are using ``ruffus.cmdling``, then you can easily ask for a flowchart from the command line:

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


=============================================
Circular dependency errors in pipelines!
=============================================
    Especially, if the pipeline is not set up properly, and vicious circular dependencies
    are present:


        .. image:: ../../images/simple_tutorial_complex_flowchart_error.png
