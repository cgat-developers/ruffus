.. _Simple_Tutorial_3rd_step:

###################################################################
Step 3: Displaying the pipeline visually
###################################################################
    * :ref:`Simple tutorial overview <Simple_Tutorial>` 
    * :ref:`pipeline functions <decorators.pipeline_functions>` in detail

=============================================
Remember to look at the example code:
=============================================
    * :ref:`Python Code for step 3 <Simple_Tutorial_3nd_step_code>` 
=============================================
Printing out a flowchart of our pipeline
=============================================


    We can see a flowchart of our fledgling pipeline by executing:
        ::
        
            pipeline_printout_graph ( open("flowchart.svg", "w"),
                                     "svg",
                                     [second_task])
        
    .. ???
    
    producing the following flowchart
    
    .. image:: ../../images/simple_tutorial_step3.png
        :scale: 50



=======================================
Printing out which jobs will be run
=======================================

    If you want a list of task which need to be re-run in the pipeline, you can
    do so as well.
    
    If any jobs in these tasks are up-to-date, this will be indicated as well:
        ::
    
            pipeline_printout(sys.stdout, [second_task])
            
    which will produce a list of all jobs which will be run per task:
    
        ::
        
            Task = first_task
                   Job = [None -> job1.stage1]
                   Job = [None -> job2.stage1]
            
            Task = second_task
                   Job = [job1.stage1 -> job1.stage2,     1st_job]
                   Job = [job2.stage1 -> job2.stage2,     2nd_job]
        
    .. ???

