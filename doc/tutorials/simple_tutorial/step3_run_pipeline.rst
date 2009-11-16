.. _Simple_Tutorial_3rd_step:



###################################################################
Step 3: Displaying the pipeline visually
###################################################################
    * :ref:`Simple tutorial overview <Simple_Tutorial>` 
    * :ref:`pipeline functions <pipeline_functions>` in detail

.. note::
    Remember to look at the example code:

    * :ref:`Python Code for step 3 <Simple_Tutorial_3nd_step_code>` 
    
.. index:: 
    pair: pipeline_printout; Tutorial

=======================================
Printing out which jobs will be run
=======================================

    Sometimes, it is useful to know which tasks are not up-to-date and are 
    scheduled to be re-run, without actually re-running the pipeline.
    
    If any jobs in these tasks are up-to-date, this can be indicated as well:
        ::
    
            pipeline_printout(sys.stdout, [second_task], verbose =2)
            
    will produce the following output:
    
        ::
        
            Task = first_task
                   Job = [None -> job1.stage1]
                   Job = [None -> job2.stage1]
            
            Task = second_task
                   Job = [job1.stage1 -> job1.stage2,     1st_job]
                   Job = [job2.stage1 -> job2.stage2,     2nd_job]
        
    .. ???

.. index:: 
    pair: pipeline_printout_graph; Tutorial

=============================================
Printing out a flowchart of our pipeline
=============================================


    .. csv-table:: 
        :widths: 1,99
        :class: borderless

        ".. image:: ../../images/simple_tutorial_step3.png", "
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

