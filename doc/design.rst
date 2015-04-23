.. Design:

.. include:: global.inc

.. index::
    pair: Design; Ruffus

###############################
Design & Architecture
###############################

    The *ruffus* module has the following design goals:

        * Simplicity.
        * Intuitive
        * Lightweight
        * Unintrusive
        * Flexible/Powerful


    Computational pipelines, especially in science, are best thought of in terms of data
    flowing through successive, dependent stages (**ruffus** calls these :term:`task`\ s).
    Traditionally, files have been used to
    link pipelined stages together. This means that computational pipelines can be managed
    using traditional software construction (`build`) systems.

=================================================
`GNU Make`
=================================================
    The grand-daddy of these is UNIX `make <http://en.wikipedia.org/wiki/Make_(software)>`_.
    `GNU make <http://www.gnu.org/software/make/>`_ is ubiquitous in the linux world for
    installing and compiling software.
    It has been widely used to build computational pipelines because it supports:

    * Stopping and restarting computational processes
    * Running multiple, even thousands of jobs in parallel

.. _design.make_syntax_ugly:

******************************************************
Deficiencies of `make` / `gmake`
******************************************************

    However, make and `GNU make <http://www.gnu.org/software/make/>`_ use a much criticised
    specialised (domain-specific) language. The make language has poor support for modern
    programming languages features such as variable scope, pattern matching, debugging.
    Make scripts require large amounts of often obscure shell scripting
    and makefiles can quickly become unmaintainable.

.. _design.scons_and_rake:

=================================================
`Scons`, `Rake` and other `Make` alternatives
=================================================

    Many attempts have been made to produce a more modern version of make, with less of its
    historical baggage. These include the Java-based `Apache ant <http://ant.apache.org/>`_ which is specified in xml.

    More interesting are a new breed of build systems whose scripts are written in modern programming
    languages, rather than a specially-invented "build" specification syntax.
    These include the Python `scons <http://www.scons.org/>`_, Ruby `rake <http://rake.rubyforge.org/>`_ and
    its python port `Smithy <http://packages.python.org/Smithy/>`_.

    The great advantages are that computation pipelines do not need to be artificially divided
    between (the often second-class) workflow management code, and the logic of real calculations and work
    in the pipeline. It also means that workflow management can use all the standard language and library
    features, for example, to read directories and match file names using regular expressions.

    **Ruffus** is much like scons in that the modern dynamic programming language python is used seamlessly
    throughout its pipeline scripts.

.. _design.implicit_dependencies:

**************************************************************************
Implicit dependencies: disadvantages of `make` / `scons` / `rake`
**************************************************************************

    Although Python `scons <http://www.scons.org/>`_ and Ruby `rake <http://rake.rubyforge.org/>`_
    are in many ways more powerful and easier to use for building software, they are still an
    imperfect fit to the world of computational pipelines.

    This is a result of the way dependencies are specified, an essential part of their design inherited
    from `GNU make <http://www.gnu.org/software/make/>`_.

    The order of operations in all of these tools is specified in a *declarative* rather than
    *imperative* manner. This means that the sequence of steps that a build should take are
    not spelled out explicity and directly. Instead recipes are provided for turning input files
    of each type to another.

    So, for example, knowing that ``a->b``, ``b->c``, ``c->d``, the build
    system can infer how to get from ``a`` to ``d`` by performing the necessary operations in the correct order.

    This is immensely powerful for three reasons:
     #) The plumbing, such as dependency checking, passing output
        from one stage to another, are handled automatically by the build system. (This is the whole point!)
     #) The same *recipe* can be re-used at different points in the build.
     #) Intermediate files do not need to be retained.

        Given the automatic inference that ``a->b->c->d``,
        we don't need to keep ``b`` and ``c`` files around once ``d`` has been produced.



    The disadvantage is that because stages are specified only indirectly, in terms of
    file name matches, the flow through a complex build or a pipeline can be difficult to trace, and nigh
    impossible to debug when there are problems.


.. _design.explicit_dependencies_in_ruffus:

**************************************************************************
Explicit dependencies in `Ruffus`
**************************************************************************

    **Ruffus** takes a different approach. The order of operations is specified explicitly rather than inferred
    indirectly from the input and output types. So, for example, we would explicitly specify three successive and
    linked operations ``a->b``, ``b->c``, ``c->d``. The build system knows that the operations always proceed in
    this order.

    Looking at a **Ruffus** script, it is always clear immediately what is the succession of computational steps
    which will be taken.

    **Ruffus** values clarity over syntactic cleverness.

.. _design.static_dependencies:

**************************************************************************
Static dependencies: What `make` / `scons` / `rake` can't do (easily)
**************************************************************************

    `GNU make <http://www.gnu.org/software/make/>`_, `scons <http://www.scons.org/>`_ and `rake <http://rake.rubyforge.org/>`_
    work by infer a static dependency (diacyclic) graph between all the files which
    are used by a computational pipeline. These tools locate the target that they are supposed
    to build and work backward through the dependency graph from that target,
    rebuilding anything that is out of date.This is perfect for building software,
    where the list of files data files can be computed **statically** at the beginning of the build.

    This is not ideal matches for scientific computational pipelines because:

        *  | Though the *stages* of a pipeline (i.e. `compile` or `DNA alignment`) are
             invariably well-specified in advance, the number of
             operations (*job*\s) involved at each stage may not be.
           |

        *  | A common approach is to break up large data sets into manageable chunks which
             can be operated on in parallel in computational clusters or farms
             (See `embarassingly parallel problems <http://en.wikipedia.org/wiki/Embarrassingly_parallel>`_).
           | This means that the number of parallel operations or jobs varies with the data (the number of manageable chunks),
             and dependency trees cannot be calculated statically beforehand.
           |

    Computational pipelines require **dynamic** dependencies which are not calculated up-front, but
    at each stage of the pipeline

    This is a *known* issue with traditional build systems each of which has partial strategies to work around
    this problem:

        * gmake always builds the dependencies when first invoked, so dynamic dependencies require (complex!) recursive calls to gmake
        * `Rake dependencies unknown prior to running tasks <http://objectmix.com/ruby/759716-rake-dependencies-unknown-prior-running-tasks-2.html>`_.
        * `Scons: Using a Source Generator to Add Targets Dynamically <http://www.scons.org/wiki/DynamicSourceGenerator>`_


    **Ruffus** explicitly and straightforwardly handles tasks which produce an indeterminate (i.e. runtime dependent)
    number of output, using a **split** / **transform** / **merge** idiom.

=============================================================================
Managing pipelines stage-by-stage using **Ruffus**
=============================================================================
    **Ruffus** manages pipeline stages directly.

        #) | The computational operations for each stage of the pipeline are written by you, in
             separate python functions.
           | (These correspond to `gmake pattern rules <http://www.gnu.org/software/make/manual/make.html#Pattern-Rules>`_)
           |

        #) | The dependencies between pipeline stages (python functions) are specified up-front.
           | These can be displayed as a flow chart.

           .. image:: images/front_page_flowchart.png

        #) **Ruffus** makes sure pipeline stage functions are called in the right order,
           with the right parameters, running in parallel using multiprocessing if necessary.

        #) Checkpointing automatically determines if all or any parts
           of the pipeline are out-of-date and need to be rerun.

        #) Separate pipeline stages, and operations within each pipeline stage,
           can be run in parallel provided they are not inter-dependent.

    Another way of looking at this is that **ruffus** re-constructs datafile dependencies dynamically
    on-the-fly when it gets to each stage of the pipeline, giving much more flexibility.

**************************************************************************
Disadvantages of the Ruffus design
**************************************************************************
    Are there any disadvantages to this trade-off for additional clarity?

        #) Each pipeline stage needs to take the right input and output. For example if we specified the
           steps in the wrong order: ``a->b``, ``c->d``, ``b->c``, then no useful output would be produced.
        #) We cannot re-use the same recipes in different parts of the pipeline
        #) Intermediate files need to be retained.


    In our experience, it is always obvious when pipeline operations are in the wrong order, precisely because the
    order of computation is the very essense of the design of each pipeline. Ruffus produces extra diagnostics when
    no output is created in a pipeline stage (usually happens for incorrectly specified regular expressions.)

    Re-use of recipes is as simple as an extra call to common function code.

    Finally, some users have proposed future enhancements to **Ruffus** to handle unnecessary temporary / intermediate files.


.. index::
    pair: Design; Comparison of Ruffus with alternatives

=================================================
Alternatives to **Ruffus**
=================================================

    A comparison of more make-like tools is available from `Ian Holmes' group <http://biowiki.org/MakeComparison>`_.

    Build systems include:

            * `GNU make <http://www.gnu.org/software/make/>`_
            * `scons <http://www.scons.org/>`_
            * `ant <http://ant.apache.org/>`_
            * `rake <http://rake.rubyforge.org/>`_

    There are also complete workload managements systems such as Condor.
    Various bioinformatics pipelines are also available, including that used by the
    leading genome annotation website Ensembl, Pegasys, GPIPE, Taverna, Wildfire, MOWserv,
    Triana, Cyrille2 etc. These all are either hardwired to specific databases, and tasks,
    or have steep learning curves for both the scientist/developer and the IT system
    administrators.

    **Ruffus** is designed to be lightweight and unintrusive enough to use for writing pipelines
    with just 10 lines of code.


.. seealso::


   **Bioinformatics workload managements systems**

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
 *  Andreas Heger, Christoffer Nellåker and Grant Belgard for driving Ruffus towards
    ever simpler syntax.



