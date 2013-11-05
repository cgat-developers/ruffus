.. include:: global.inc
****************
Glossary
****************
.. _Glossary:

.. _glossary.task:

.. glossary::
    
    
    
    task
        A stage in a computational pipeline.

        Each **task** in *ruffus* is represented by a python function.
    
        For example, a task might be to find the products of a sets of two numbers::

            4 x 5 = 20
            5 x 6 = 30
            2 x 7 = 14   

    job
        Any number of operations which can be run in parallel and make up
        the work in a stage of a computional pipeline.
        
        Each **task** in *ruffus* is a separate call to the **task** function.
        
        For example, if a task is to find products of numbers, each of these will be a separate job.
        
            Job1::
            
                4 x 5 = 20
            
            Job2::
            
                5 x 6 = 30
                    
            Job3::
            
                2 x 7 = 14   
            
        Jobs need not complete in order.
        
    
    decorator
        Ruffus decorators allow functions to be incorporated into a computational
        pipeline, with automatic generation of parameters, dependency checking etc.,
        without modifying any code within the function.
        Quoting from the `python wiki <http://wiki.python.org/moin/PythonDecorators>`_:

            A Python decorator is a specific change to the Python syntax that 
            allows us to more conveniently alter functions and methods.

            Decorators dynamically alter the functionality of a function, method, or 
            class without having to directly use subclasses or change the source code 
            of the function being decorated.
            

    
    generator
        python generators are new to python 2.2 
        (see `Charming Python: Iterators and simple generators <http://www.ibm.com/developerworks/library/l-pycon.html>`_).
        They allow iterable data to be generated on the fly.
        
        Ruffus asks for generators when you want to generate **job** parameters dynamically.
        
        Each set of job parameters is returned by the ``yield`` keyword for 
        greater clarity. For example,::
        
            def generate_job_parameters():
                
                for file_index, file_name in iterate(all_file_names):
                
                    # parameter for each job
                    yield file_index, file_name
    
        Each job takes the parameters ``file_index`` and ``file_name``
    
         
