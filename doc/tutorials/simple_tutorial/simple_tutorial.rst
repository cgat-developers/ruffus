.. _Simple_Tutorial:


############################################################
A simple tutorial: 7 steps to *Ruffus*
############################################################

***************************************
Table of Contents
***************************************

============
Features
============

The **Ruffus** provides automatic support for
 
        * Managing dependencies
        * Parallel jobs
        * Re-starting from arbitrary points, especially after errors
        * Display of the pipeline as a flowchart
        * Reporting


    | This tutorial has seven steps which cover all the core functionality of *Ruffus*.
    | Don't worry if steps 1 and 2 seem a bit slow: Once you get used to **Ruffus**
      steps 3-7 will be a breeze.
    
    You can click on "previous" and "next" at the top and bottom of each page to
    navigate through the tutorial.
    
    
============================
The first steps (1-3)
============================

    The first half of the tutorial will show you how to:
        
    .. toctree::
        :maxdepth: 1
    
        1. Chain tasks (functions) together into a pipeline <step1_follows>
        2. Provide parameters to run jobs in parallel <step2_files>
        3. Displaying all the stages of your new pipeline <step3_run_pipeline>
    
============================
A worked example (steps 4-7)
============================

    The second half of the tutorial is a worked example to calculate 
    the sample variance of 10,000 random numbers. This shows you how to:
               
    .. toctree::
        :maxdepth: 1
        
        4. Split up a large problem into smaller chunks<step4_split>
        5. Calculate partial solutions in parallel <step5_transform>
        6. Re-combine the partial solutions into the final result <step6_merge>
        7. Automatically signal the completion of each step of our pipeline <step7_posttask>

        Code for the simple tutorial <simple_tutorial_code>

    This covers the core functionality of *Ruffus*.



            


    






