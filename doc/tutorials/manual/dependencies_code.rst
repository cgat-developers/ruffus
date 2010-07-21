.. include:: ../../global.inc
.. _manual.dependencies.code:


########################################################################################
Code for Chapter 9: Checking dependencies to run tasks in order
########################################################################################
    * :ref:`Manual overview <manual>` 
    * :ref:`Back <manual.dependencies.example>` 

    This example shows how dependencies work
              
    
************************************
Code
************************************
    ::

        from ruffus import *
        import json
        
        import time
        def task_helper(infile, outfile):
            """
            cat input file content to output file
                after writing out job parameters
            """
            if infile:
                output_text = "".join(sorted(open(infile).readlines()))
            else:
                output_text = "None"
            output_text += json.dumps(infile) + " -> " + json.dumps(outfile) + "\n"
            open(outfile, "w").write(output_text)



        #
        #    task1
        #
        @files(None, 'a.1')
        def task1(infile, outfile):
            """
            First task
            """
            task_helper(infile, outfile)
        
        
        
        #
        #    task2
        #
        @transform(task1, regex(r'.1'), '.2')
        def task2(infile, outfile):
            """
            Second task
            """
            task_helper(infile, outfile)
        
        
        
        #
        #    task3
        #
        @transform(task2, regex(r'.2'), '.3')
        def task3(infile, outfile):
            """
            Third task
            """
            task_helper(infile, outfile)
        
        
        
        #
        #    task4
        #
        @transform(task3, regex(r'.3'), '.4')
        def task4(infile, outfile):
            """
            Fourth task
            """
            task_helper(infile, outfile)
        
        pipeline_printout_graph ("flowchart.png", "png", [task4], draw_vertically = True, no_key_legend = True)
        pipeline_run([task4])

************************************
Resulting Output
************************************
    ::
    
        >>> pipeline_run([task4], multiprocess = 10, logger = logger_proxy)
            job = [null, "a.1"]
            job = ["a.1", "a.2"]
            job = ["a.2", "a.3"]
            job = ["a.3", "a.4"]


