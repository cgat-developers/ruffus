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

        .. :: .. image:: ../../images/simple_tutorial_decorator_syntax.png

        .. raw:: html

            <svg version="1.0" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0"
            	 width="249.5" height="67.5" viewBox="0 0 249.5 67.5" enable-background="new 0 0 249.5 67.5" xml:space="preserve">
            <rect x="4.5" y="14.667" fill="#FCF9CE" stroke="#016735" stroke-width="0.25" stroke-miterlimit="10" width="157" height="52.833"/>
            <rect x="3.25" y="14.667" fill="#FCF9CE" width="159.5" height="52.833"/>
            <text transform="matrix(1 0 0 1 14.5 33.6177)"><tspan x="0" y="0" font-family="'Courier'" font-size="12">@follows(first_task)</tspan><tspan x="0" y="14.4" font-family="'CourierNewPSMT'" font-size="12">def second_task():</tspan><tspan x="0" y="28.8" font-family="'CourierNewPSMT'" font-size="12">    &quot;&quot;</tspan><tspan x="0" y="43.2" font-family="'CourierNewPSMT'" font-size="12" letter-spacing="28">	</tspan></text>
            <path fill="none" stroke="#ED1C24" stroke-miterlimit="10" d="M73.25,29.762c0,4.688-3.731,8.488-8.333,8.488H18.083
            	c-4.602,0-8.333-3.8-8.333-8.488l0,0c0-4.688,3.731-8.488,8.333-8.488h46.834C69.519,21.274,73.25,25.075,73.25,29.762L73.25,29.762
            	z"/>
            <g>
            	<g>
            		<line fill="none" stroke="#ED1C24" stroke-miterlimit="10" x1="74.775" y1="20.142" x2="106" y2="7.5"/>
            		<g>
            			<path fill="#ED1C24" d="M71.978,21.274c1.514-0.044,3.484,0.127,4.854,0.6l-1.689-1.881l-0.095-2.526
            				C74.392,18.759,73.097,20.253,71.978,21.274z"/>
            		</g>
            	</g>
            </g>
            <text transform="matrix(1 0 0 1 107.75 11.5)" fill="#ED1C24" font-family="'ArialMT'" font-size="12">Decorator</text>
            <text transform="matrix(1 0 0 1 170.75 50.75)"><tspan x="0" y="0" fill="#2E3192" font-family="'ArialMT'" font-size="12">Normal Python </tspan><tspan x="0" y="14.4" fill="#2E3192" font-family="'ArialMT'" font-size="12">Function</tspan></text>
            <g>
            	<line fill="#2E3192" x1="166.5" y1="46.5" x2="147" y2="46.5"/>
            	<g>
            		<line fill="none" stroke="#2E3192" stroke-miterlimit="10" x1="166.5" y1="46.5" x2="150.018" y2="46.5"/>
            		<g>
            			<path fill="#2E3192" d="M147,46.5c1.42-0.527,3.182-1.426,4.273-2.378l-0.86,2.378l0.86,2.377
            				C150.182,47.925,148.42,47.026,147,46.5z"/>
            		</g>
            	</g>
            </g>
            </svg>


                
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
    
    
    

