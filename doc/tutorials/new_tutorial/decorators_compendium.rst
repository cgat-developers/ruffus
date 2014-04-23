.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: decorators_compendium; Tutorial

.. _new_manual.decorators_compendium:

#####################################################################################################################
|new_manual.decorators_compendium.chapter_num|: Pipeline topologies and a compendium of *Ruffus* decorators
#####################################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`decorators <decorators>`


***************************************
Overview
***************************************

    Computational pipelines transform your data in stages until the final result is produced.

    You can visualise your pipeline data flowing like water down a system of pipes.
    *Ruffus* has many ways of joining up your pipes to create different topologies.

    .. note::

        **The best way to design a pipeline is to:**

            * **Write down the file names of the data as it flows across your pipeline.**
            * **Draw lines between the file names to show how they should be connected together.**


******************************************************************************
:ref:`@transform <decorators.transform>`
******************************************************************************


    So far, our data files have been flowing through our pipelines independently in lockstep.

    .. image:: ../../images/bestiary_transform.png
       :scale: 50

    If we drew a graph of the data files moving through the pipeline, all of our flowcharts would look like something like this.

    The :ref:`@transform <decorators.transform>` decorator connects up your data files in 1 to 1 operations, ensuring that for every **Input**, a corresponding **Output** is
    generated, ready to got into the next pipeline stage. If we start with three sets of starting data, we would end up with three final sets of results.

******************************************************************************
A bestiary of *Ruffus* decorators
******************************************************************************

    Very often, we would like to transform our data in more complex ways, this is where other *Ruffus* decorators come in.

    .. image:: ../../images/bestiary_decorators.png
       :scale: 50

******************************************************************************
:ref:`@originate <decorators.originate>`
******************************************************************************

    * Introduced in |new_manual.transform_in_parallel.chapter_num| :ref:`More on @transform-ing data and @originate <new_manual.transform_in_parallel>`,
      :ref:`@originate <decorators.originate>` generates **Output** files from scratch without the benefits of any **Input** files.

******************************************************************************
:ref:`@merge <decorators.merge>`
******************************************************************************
    * A **many to one** operator.
    * The last decorator at the far right to the figure, :ref:`@merge <decorators.merge>` merges multiple **Input** into one **Output**.

******************************************************************************
:ref:`@split <decorators.split>`
******************************************************************************
    * A  **one to many** operator,
    * :ref:`@split <decorators.split>` is the evil twin of :ref:`@merge <decorators.merge>`. It takes a single set of **Input** and splits them into multiple smaller pieces.
    * The best part of :ref:`@split <decorators.split>` is that we don't necessarily have to decide ahead of time *how many* smaller pieces it should produce. If we have encounter a larger file,
      we might need to split it up into more fragments for greater parallelism.
    * Since :ref:`@split <decorators.split>` is a  **one to many** operator, if you pass it **many** inputs (e.g. via :ref:`@transform <decorators.transform>`, it performs an implicit :ref:`@merge <decorators.merge>` step to make one
      set of **Input** that you can redistribute into a different number of pieces. If you are looking to split *each* **Input** into further smaller fragments, then you
      need :ref:`@subdivide <decorators.subdivide>`

******************************************************************************
:ref:`@subdivide <decorators.subdivide>`
******************************************************************************
    * A **many to even more** operator.
    * It takes each of multiple **Input**, and further subdivides them.
    * Uses :ref:`suffix() <decorators.suffix>`, :ref:`formatter() <decorators.formatter>` or :ref:`regex() <decorators.regex>` to generate **Output** names from its **Input** files but like :ref:`@split <decorators.split>`, we don't have to decide ahead of time
      *how many* smaller pieces each **Input** should be further divided into. For example, a large **Input** files might be subdivided into 7 pieces while the next job might,
      however, split its **Input** into just 4 pieces.

******************************************************************************
:ref:`@collate <decorators.collate>`
******************************************************************************
    * A **many to fewer** operator.
    * :ref:`@collate <decorators.collate>` is the opposite twin of ``subdivide``: it takes multiple **Output** and groups or collates them into bundles of **Output**.
    * :ref:`@collate <decorators.collate>` uses :ref:`formatter() <decorators.formatter>` or :ref:`regex() <decorators.regex>` to generate **Output** names.
    * All **Input** files which map to the same **Output** are grouped together into one job (one task function call) which
      produces one **Output**.

******************************************************************************
Combinatorics
******************************************************************************

    More rarely, we need to generate a set of **Output** based on a combination or permutation or product of the **Input**.

    For example, in bioinformatics, we might need to look for all instances of a set of genes in the genomes of a different number of species.
    In other words, we need to find the :ref:`@product <decorators.product>` of XXX genes x YYY species.

    *Ruffus* provides decorators modelled on the "Combinatoric generators" in the Standard Python `itertools  <http://docs.python.org/2/library/itertools.html>`_ library.

    To use combinatoric decorators, you need to explicitly include them from *Ruffus*:

    .. code-block:: python


        import ruffus
        from ruffus import *
        from ruffus.combinatorics import *

    .. image:: ../../images/bestiary_combinatorics.png
       :scale: 50

******************************************************************************
:ref:`@product <decorators.product>`
******************************************************************************
    * Given several sets of **Input**, it generates all versus all **Output**. For example, if there are four sets of **Input** files, :ref:`@product <decorators.product>` will generate ``WWW x XXX x YYY x ZZZ`` **Output**.
    * Uses :ref:`formatter <decorators.transform>` to generate unique **Output** names from components parsed from *any* parts of *any* specified files in
      all **Input** sets. In the above example, this allows the generation of  ``WWW x XXX x YYY x ZZZ`` unique names.

******************************************************************************
:ref:`@combinations <decorators.combinations>`
******************************************************************************
    * Given one set of **Input**, it generates the combinations of r-length tuples among them.
    * Uses :ref:`formatter <decorators.transform>` to generate unique **Output** names from components parsed from *any* parts of *any* specified files in all **Input** sets.
    * For example, given **Input** called ``A``, ``B`` and ``C``, it will generate: ``A-B``,  ``A-C``,  ``B-C``
    * The order of **Input** items is ignored so either ``A-B`` or ``B-A`` will be included, not both
    * Self-vs-self combinations (``A-A``) are excluded.

************************************************************************************************************************************************************
:ref:`@combinations_with_replacement <decorators.combinations_with_replacement>`
************************************************************************************************************************************************************
    * Given one set of **Input**, it generates the combinations of r-length tuples among them but includes self-vs-self conbinations.
    * Uses :ref:`formatter <decorators.transform>` to generate unique **Output** names from components parsed from *any* parts of *any* specified files in all **Input** sets.
    * For example, given **Input** called ``A``, ``B`` and ``C``, it will generate: ``A-A``, ``A-B``,  ``A-C``, ``B-B``, ``B-C``,  ``C-C``

******************************************************************************
:ref:`@permutations <decorators.permutations>`
******************************************************************************
    * Given one set of **Input**, it generates the permutations of r-length tuples among them. This excludes self-vs-self combinations but includes all orderings (``A-B`` and ``B-A``).
    * Uses :ref:`formatter <decorators.transform>` to generate unique **Output** names from components parsed from *any* parts of *any* specified files in all **Input** sets.
    * For example, given **Input** called ``A``, ``B`` and ``C``, it will generate: ``A-A``, ``A-B``,  ``A-C``, ``B-A``, ``B-C``, ``C-A``,  ``C-B``

