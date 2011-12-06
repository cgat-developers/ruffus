.. include:: ../../global.inc
.. _Simple_Tutorial_1st_step:
    

###################################################################
Step 1: An introduction to Ruffus pipelines
###################################################################

    * :ref:`Simple tutorial overview <Simple_Tutorial>` 


    Computational pipelines often become quite simple
    if we breakdown the process into simple stages.
    
    .. note::
        
        Ruffus refers to each stage of your pipeline as a :term:`task`.

    | Let us start with the usual "Hello World". 
    | We have the following two python functions which
      we would like to turn into an automatic pipeline:
      
    
        .. image:: ../../images/simple_tutorial_hello_world.png

    .. ::
    
        ::
        
            def first_task():
                print "Hello "
        
            def second_task():
                print "world"

    
    The simplest **Ruffus** pipeline would look like this:
    
        .. image:: ../../images/simple_tutorial_intro_follows.png
    
    .. ::
    
        ::
        
            from ruffus import *
            
            def first_task():
                print "Hello "
        
            @follows(first_task)
            def second_task():
                print "world"
    
            pipeline_run([second_task])

    
    The functions which do the actual work of each stage of the pipeline remain unchanged.
    The role of **Ruffus** is to make sure these functions are called in the right order, 
    with the right parameters, running in parallel using multiprocessing if desired.
        
    There are three simple parts to building a **ruffus** pipeline

        #. importing ruffus
        #. "Decorating" functions which are part of the pipeline
        #. Running the pipeline!
    
.. index:: 
    pair: decorators; Tutorial
    

****************************
"Decorating" functions
****************************

    You need to tag or :term:`decorator` existing code to tell **Ruffus** that they are part
    of the pipeline.
    
    .. note::
        
        :term:`decorator`\ s are ways to tag or mark out functions. 

        They start with a ``@`` prefix and take a number of parameters in parenthesis.

        .. image:: ../../images/simple_tutorial_decorator_syntax.png
                
    The **ruffus** decorator :ref:`@follows <decorators.follows>` makes sure that
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

    We run the pipeline by specifying the **last** stage (:term:`task` function) of your pipeline.
    Ruffus will know what other functions this depends on, following the appropriate chain of
    dependencies automatically, making sure that the entire pipeline is up-to-date.

    Because ``second_task`` depends on ``first_task``, both functions are executed in order.

        ::
            
            >>> pipeline_run([second_task], verbose = 1)
        
    Ruffus by default prints out the ``verbose`` progress through the pipelined code, 
    interleaved with the **Hello** printed by ``first_task`` and **World** printed
    by ``second_task``.
    
        .. image:: ../../images/simple_tutorial_hello_world_output.png

    .. ::
    
        ::
            
            >>> pipeline_run([second_task], verbose = 1)
            Start Task = first_task
            Hello
                Job completed
            Completed Task = first_task
            Start Task = second_task
            world
                Job completed
            Completed Task = second_task
    
    
    

