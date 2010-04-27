.. include:: ../../global.inc
.. _Simple_Tutorial_4th_step_graphical:



###################################################################
Step 4: Displaying the pipeline visually
###################################################################
    * :ref:`Simple tutorial overview <Simple_Tutorial>` 
    * :ref:`pipeline functions <pipeline_functions>` in detail

.. note::
    Remember to look at the example code:

    * :ref:`Python Code for step 4 <Simple_Tutorial_4th_step_graphical_code>` 
    
.. index:: 
    pair: pipeline_printout; Tutorial



.. index:: 
    pair: pipeline_printout_graph; Tutorial

=============================================
Printing out a flowchart of our pipeline
=============================================

    It is all very well being able to trace the data flow through the pipeline.
    Sometimes, however, we need a bit of eye-candy.

    .. csv-table:: 
        :widths: 1,99
        :class: borderless

        ".. image:: ../../images/simple_tutorial_step4.png", "
            We can see this flowchart of our fledgling pipeline by executing:
                ::
                
                    pipeline_printout_graph (   'flowchart.svg', 
                                                'svg', 
                                                [second_task], 
                                                no_key_legend = False)
            
            Flowcharts can be printed in a large number of formats including jpg, svg, 
            png and pdf provided that the ``dot`` programme from 
            `Graphviz <http://www.graphviz.org/>`_ is installed.

            For this simple case, we have ommitted the legend key which distinguishes between the
            different states of the various tasks. (See below for the legend key.)
            "
            
            

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

