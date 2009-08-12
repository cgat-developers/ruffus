.. Design:

****************************
Design & Architecture
****************************
    The *ruffus* module has the following design goals:
    
        * Simplicity. Can be picked up in 10 minutes
        * Elegance
        * Lightweight
        * Unintrusive
        * Flexible/Powerful

Task-based rather than file-based work flow
================================================

    Computational pipelines, especially in science are best thought of as successively 
    dependent stages (we call them **task**\ s: See the :ref:`Glossary <Glossary>` ).
    
    Traditionally, especially in Unix, pipelined stages have been linked together using files.
    
    Tools like `GNU make <http://www.gnu.org/software/make/>`_ or `scons <http://www.scons.org/>`_ 
    create a static dependency graph between all the files which are produced by the pipe line. 
    Inference "rules" specifying how files of one type are converted into another add 
    additional conciseness to such systems.
    
    However, the use of files to link pipeline stages makes these tools a poor match
    for scientific computational pipelines:
    
        #) Though the stages of a pipeline will be specified up-front, the number of 
           (conceptually parallel) operations (**job**\ s) involved in each stage may not be.
           If the data sets are large, this may be broken up into larger number of smaller pieces.
        
        #) Some stages can depend on databases or data in other formats. It seems clumsy to
           always shoehorn everything into a "file" paradigm
           
        #) Static File dependencies graphs are very difficult to debug.
    
    This is how *ruffus* runs its pipelines:
    
        #) Dependencies between **task**\ s are specified up front. 
           These can be displayed as a flow chart.
        #) Out-of-date pipeline stages are identified by asking each task if it has *any* out-of-date operations. 
    
           This is a short-circuiting operation, and *ruffus* tries to do the minimal amount of
           querying
           
        #) All out-of-date **task**\ s and subsequent stages in the pipeline will be re-run
        #) When each **task** is run, it is asked (again) which operations are out-of-date and 
           those **job**\ s will be executed
           
    In practice, this means that *ruffus* re-constructs its dependencies on-the-fly when it
    gets to each stage, giving much more flexibility.




Alternatives
============
    Tools used to build executables can be used to manage computational pipelines.
    These include
    
            * `GNU make <http://www.gnu.org/software/make/>`_
            * `scons <http://www.scons.org/>`_
            * `ant <http://ant.apache.org/>`_
            
    A comparison of more make-like tools is available from `Ian Holmes' group <http://biowiki.org/MakeComparison>`_.
    
    It is often necessary to learn a specialised (domain-specific) language. 
    GNU make syntax, for example, is much criticised because of limited support for
    abstraction compared with modern programming languages like 
    C, Perl, python etc. GNU makefiles can quickly become unmaintainable.
    
    Pipeline specifications are usually written in a "declarative" rather than "imperative"
    manner. You write a specification that describes the dependencies, and the tool 
    figures out how to perform the computations in the correct order. However, because
    GNU make and its kin depend entirely on file dependencies, the links between pipeline
    stages can be difficult to trace, and nigh impossible to debug when there are problems.
    
    There are also complete workload managements systems such as Condor. 
    Various bioinformatics pipelines are also available, including that used by the
    leading genome annotation website Ensembl, Pegasys, GPIPE, Taverna, Wildfire, MOWserv,
    Triana, Cyrille2 etc. These all are either hardwired to specific databases, and tasks,
    or have steep learning curves for both the scientist/developer and the IT system
    administrators 


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
    
    

Acknowledgements
=================
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

   
    
    
    
    

