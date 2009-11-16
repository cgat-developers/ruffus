.. Design:

###############################
Design & Architecture
###############################
    The *ruffus* module has the following design goals:
    
        * Simplicity.
        * Intuitive
        * Lightweight
        * Unintrusive
        * Flexible/Powerful

**************************************************
Task-based rather than file-based work flow
**************************************************

.. design.file_based_pipelines:
.. index:: 
    pair: Design; File-based pipeline management

===============================================
File-based pipeline management
===============================================

    Computational pipelines, especially in science, are best thought of in terms of data
    flowing through successive, dependent stages (**ruffus** calls these :term:`task`\ s).
    Traditionally, files have been used to 
    link pipelined stages together. This means that computational pipelines can be managed 
    using software construction (`build`) systems such as 
    `GNU make <http://www.gnu.org/software/make/>`_ or `scons <http://www.scons.org/>`_ 
    

    These tools infer a static dependency (diacyclic) graph between all the files which 
    are used by a computational pipeline. Inference "rules" can be used to specify the 
    computational recipes used to transform data files of one type to another.
    
    The static dependency tree of data files is used to manage the pipeline:
    
        * File timestamps can indicate whether parts of a pipeline are out-of-date and
          needs to be re-run.
           
        * A stage of the pipeline may involve a number of (conceptually parallel) 
          operations or :term:`job`\s on separate data files. 
          
           | A `Compile` stage may apply a compilation operation to transform all source files to binary
             object files.
           |  A `DNA alignment` stage may apply a DNA comparison operation to
             transform DNA sequences to alignment result files.
           
        * | Where there is a "chain" of successive recipes, only the beginning and the 
            end files of the "chain" need to be retained. 
          | In practice, this is less useful in computational pipelines.
           

.. index:: 
    pair: Design; File-based pipeline management (drawbacks)
    
===============================================
Problems with file-based pipeline management
===============================================
    However, because the dependency trees for data files are inferred *statically*, these
    and similar tools are not ideal matches for scientific computational pipelines:
    
        *  | Though the **stages** of a pipeline (i.e. `compile` or `DNA alignment`) are 
             invariably well-specified in advance, the number of
             operations (**job**\s) involved at each stage may not be.
           |
           
        *  | A common approach is to break up large data sets into manageable chunks which
             can be operated on in parallel in computational clusters or farms 
             (See `embarassingly parallel <http://en.wikipedia.org/wiki/Embarrassingly_parallel>`_).
           | This means that the number of parallel operations or jobs varies with the data,
             and dependency trees cannot be calculated statically beforehand.
           |
           
        *  Pipelines are managed *at one remove*, using only the data files being produced, 
           rather than the computational stages involved. This conceptual mismatch adds
           much unnecessary complexity, as well as development and maintenance cost.
               
    .. csv-table ::
        :widths: 1,1
        :class: borderless
    
        ".. image:: images/design.file_based_workflow.png", ".. image:: images/design.task_based_workflow.png"


.. index:: 
    pair: Design; Task-based pipeline management

===============================================
Managing pipelines stage-by-stage
===============================================
    **Ruffus** reverts to managing pipeline stages directly.
    
        #) | The computational operations for each stage of the pipeline are written by you, in
             separate python functions. 
           | (These correspond to `gmake pattern rules <http://www.gnu.org/software/make/manual/make.html#Pattern-Rules>`_)
           |
           
        #) | The dependencies between pipeline stages (python functions) are specified up-front.
           | These can be displayed as a flow chart (as shown above).
           |
            
        #) **Ruffus** makes sure pipeline stage functions are called in the right order, 
           with the right parameters, running in parallel using multiprocessing if necessary.
    
        #) Data file timestamps can be used to automatically determine if all or any parts
           of the pipeline are out-of-date and need to be rerun.
           
        #) Separate pipeline stages, and operations within each pipeline stage,
           can be run in parallel provided they are not inter-dependent.
           
    Another way of looking at this is that **ruffus** re-constructs datafile dependencies 
    on-the-fly when it gets to each stage of the pipeline, giving much more flexibility.


.. index:: 
    pair: Design; Comparison of Ruffus with alternatives
    
**************************************************
Advantages of **Ruffus** over alternatives
**************************************************

    Tools used to build executables can be used to manage computational pipelines.
    These include
    
            * `GNU make <http://www.gnu.org/software/make/>`_
            * `scons <http://www.scons.org/>`_
            * `ant <http://ant.apache.org/>`_
            
    A comparison of more make-like tools is available from `Ian Holmes' group <http://biowiki.org/MakeComparison>`_.
    
=====================================
Obscure and inadequate language
=====================================

    It is often necessary to learn a specialised (domain-specific) language. 
    `GNU make <http://www.gnu.org/software/make/>`_  syntax, for example, is much criticised 
    because of poor support for modern programming languages features like variable scope,
    pattern matching, debugging. Make scripts require large amounts of often obscure shell scripting.
    GNU makefiles can quickly become unmaintainable.
    
    **Ruffus** pipelines are written in normal python, with full access all python features,
    including the standard library modules.
    
=====================================
Declarative file dependencies
=====================================
    Pipeline specifications are usually written in a "declarative" rather than "imperative"
    manner. You write a specification that describes the dependencies, and the tool 
    figures out how to perform the computations in the correct order. However, because
    GNU make and its kin depend entirely on file dependencies, the links between pipeline
    stages can be difficult to trace, and nigh impossible to debug when there are problems.
    
=====================================
Heavyweight pipeline systems 
=====================================
    There are also complete workload managements systems such as Condor. 
    Various bioinformatics pipelines are also available, including that used by the
    leading genome annotation website Ensembl, Pegasys, GPIPE, Taverna, Wildfire, MOWserv,
    Triana, Cyrille2 etc. These all are either hardwired to specific databases, and tasks,
    or have steep learning curves for both the scientist/developer and the IT system
    administrators.
    
    **Ruffus** is designed to be lightweight and unintrusive enough to use for writing pipelines
    with just 10 lines of code.


.. seealso::


   **Bioinformatics pipelines**
   
    Condor:
        http://www.cs.wisc.edu/condor/description.html
    
    Ensembl Analysis pipeline:
        http://www.ncbi.nlm.nih.gov/pubmed/15123589
    
    
    Pegasys:
        http://www.ncbi.nlm.nih.gov/pubmed/15096276
    
    GPIPE:
        http://www.biomedcentral.com/pubmed/15096276
    
    Taverna:
        http://www.ncbi.nlm.nih.gov/pubmed/15201187
    
    Wildfire:
        http://www.biomedcentral.com/pubmed/15788106
    
    MOWserv:
        http://www.biomedcentral.com/pubmed/16257987
    
    Triana:
        http://dx.doi.org/10.1007/s10723-005-9007-3
    
    Cyrille2:
        http://www.biomedcentral.com/1471-2105/9/96
    
    
.. index:: 
    single: Acknowledgements

**************************************************
Acknowledgements
**************************************************
 *  Bruce Eckel's insightful article on 
    `A Decorator Based Build System <http://www.artima.com/weblogs/viewpost.jsp?thread=241209>`_
    was the obvious inspiration for the use of decorators in *Ruffus*. 

    The rest of the *Ruffus* takes uses a different approach. In particular:
        #. *Ruffus* uses task-based not file-based dependencies
        #. *Ruffus* tries to have minimal impact on the functions it decorates.
           
           Bruce Eckel's design wraps functions in "rule" objects. 
           
           *Ruffus* tasks are added as attributes of the functions which can be still be
           called normally. This is how *Ruffus* decorators can be layered in any order 
           onto the same task.

 *  Languages like c++ and Java would probably use a "mixin" approach. 
    Python's easy support for reflection and function references, 
    as well as the necessity of marshalling over process boundaries, dictated the
    internal architecture of *Ruffus*.
 *  The `Boost Graph library <http://www.boost.org>`_ for text book implementations of directed
    graph traversals.
 *  `Graphviz <http://www.graphviz.org/>`_. Just works. Wonderful.

   
.. index:: 
    pair: Ruffus; Etymology
    pair: Ruffus; Name origins
    
**************************************************
Whence the name *Ruffus*?
**************************************************

.. image:: images/wikimedia_cyl_ruffus.jpg

**Cylindrophis ruffus** is the name of the 
`red-tailed pipe snake <http://en.wikipedia.org/wiki/Cylindrophis_ruffus>`_ (bad python-y pun)
which can be found in `Hong Kong <http://www.discoverhongkong.com/eng/index.html>`_ where the original author comes from.
Be careful not to step on one when running down country park lanes at full speed 
in Hong Kong: this snake is a `rare breed <http://www.hkras.org/eng/info/hkspp.htm>`_!

*Ruffus* is a shy creature, and pretends to be a cobra by putting up its red tail and ducking its
head in its coils when startled. It does most of its work at night and sleeps during the day:
typical of many python programmers!

The original image is from `wikimedia <http://upload.wikimedia.org/wikipedia/commons/a/a1/Cyl_ruffus_061212_2025_tdp.jpg>`_

