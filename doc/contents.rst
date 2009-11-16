***************************
**Ruffus** documentation
***************************

=====================
Start Here:
=====================

.. toctree::
   :maxdepth: 1

   installation.rst
   tutorials/simple_tutorial/simple_tutorial.rst
   Manual <tutorials/manual/manual_contents.rst>


=====================
Overview:
=====================
.. toctree::
   :maxdepth: 2

   cheatsheet.rst
   pipeline_functions.rst
   installation.rst   
   design.rst
   Bugs and Updates <history>
   Future plans <todo>
   faq.rst
   glossary.rst





=====================
Reference:
=====================
######################
Decorators
######################
.. toctree::
    :maxdepth: 1

    decorators/decorators.rst
    decorators/indicator_objects.rst


.. topic::
    Basic

    .. toctree::
        :maxdepth: 1
    
        decorators/follows.rst
        decorators/files.rst

.. topic::
    Core

    .. toctree::
        :maxdepth: 1
    
        decorators/split.rst
        decorators/transform.rst
        decorators/merge.rst
        decorators/posttask.rst
    
.. topic::
    For advanced users

    .. toctree::
        :maxdepth: 1
    
        decorators/transform_ex.rst
        decorators/collate.rst

.. topic::
    Esoteric

    .. toctree::
        :maxdepth: 1
        
        decorators/files_ex.rst
        decorators/parallel.rst
        decorators/check_if_uptodate.rst
        decorators/files_re.rst

   
   
######################
Example code:
######################

.. toctree::
   :maxdepth: 1
   
   examples/simpler.rst
   examples/intermediate_example.rst
   examples/intermediate_example_code.rst
   examples/complicated_example.rst
   examples/complicated_example_code.rst
   examples/sharing_data_across_jobs_example.rst
   examples/sharing_data_across_jobs_example_code.rst
    
######################
Modules:
######################
   
.. toctree::
   :maxdepth: 2

   task.rst
   proxy_logger.rst
   
.. comment
   graph.rst
   print_dependencies.rst
   adjacent_pairs_iterate.rst


=====================
Indices and tables
=====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

