.. include:: ../global.inc
.. _decorators.graphviz:
.. index::
    pair: @graphviz; Syntax

.. seealso::

    * :ref:`@graphviz <new_manual.graphviz>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

########################
graphviz
########################

.. |graphviz_parameters| replace:: `graphviz_parameters`
.. _graphviz_parameters: `decorators.graphviz.graphviz_parameters`_


********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
*@graphviz* ( |graphviz_parameters|_,...] )
********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    *Contributed by Sean Davis, with improved syntax via Jake Biesinger*

    **Purpose:**
        Customise the graphic for each task in printed flowcharts by adding
        `graphviz attributes  <http://www.graphviz.org/doc/info/attrs.html>`__,
        (URL, shape, colour) to that node.

        * This allows HTML formatting in the task names (using the ``label`` parameter as in the following example).
          HTML labels **must** be enclosed in ``<`` and ``>``. E.g.

          .. code-block:: python

            label = "<Line <BR/> wrapped task_name()>"

        * You can also opt to keep the task name and wrap it with a prefix and suffix:

          .. code-block:: python

            label_suffix = "??? ", label_prefix = ": What is this?"

        * The ``URL`` attribute allows the generation of clickable svg, and also client / server
          side image maps usable in web pages.
          See `Graphviz documentation  <http://www.graphviz.org/content/output-formats#dimap>`__


    **Example**:
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

        .. image:: ../images/history_html_flowchart.png
           :scale: 30

    **Parameters:**


.. _decorators.graphviz.graphviz_parameters:

    * named *graphviz_parameters*

        Including among others:

            * URL (e.g. ``"www.ruffus.org.uk"``)
            * fillcolor
            * color
            * pencolor
            * fontcolor
            * label_suffix (appended to task name)
            * label_prefix (precedes task name)
            * label (replaces task name)
            * shape (e.g. ``"component", "box", "diamond", "doubleoctagon"`` etc., see `graphviz <http://www.graphviz.org/doc/info/shapes.html>`__ )
            * height
            * peripheries (Number of borders)
            * style (e.g. ``"solid", "wedged", "dashed"``  etc., see `graphviz <http://www.graphviz.org/doc/info/attrs.html#k:style>`__ )

        Colours may specified as ``'"#FFCCCC"', 'red', 'red:blue', '/bugn9/7'`` etc. see  `color names <http://www.graphviz.org/doc/info/attrs.html#k:color>`__ and `colour schemes <http://www.graphviz.org/doc/info/colors.html>`__
