.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: check_if_uptodate; Tutorial

.. _new_manual.check_if_uptodate:

########################################################################################################################################################################################################################################################################################################
|new_manual.check_if_uptodate.chapter_num|: Esoteric: Writing custom functions to decide which jobs are up to date with :ref:`@check_if_uptodate<decorators.check_if_uptodate>`
########################################################################################################################################################################################################################################################################################################


.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`@check_if_uptodate  syntax in detail<decorators.check_if_uptodate>`


******************************************************************************
**@check_if_uptodate** : Manual dependency checking
******************************************************************************
    tasks specified with most decorators such as
        * :ref:`@split <decorators.split>`
        * :ref:`@transform <decorators.transform>`
        * :ref:`@merge <decorators.merge>`
        * :ref:`@collate <decorators.collate>`
        * :ref:`@collate <decorators.subdivide>`

    have automatic dependency checking based on file modification times.

    Sometimes, you might want to decide have more control over whether to run jobs, especially
    if a task does not rely on or produce files (i.e. with :ref:`@parallel <decorators.parallel>`)

    You can write your own custom function to decide whether to run a job.
    This takes as many parameters as your task function, and needs to return a
    tuple for whether an update is required, and why (i.e. ``tuple(bool, str)``)

    This simple example which creates the file ``"a.1"`` if it does not exist:

        ::

            from ruffus import *
            @originate("a.1")
            def create_if_necessary(output_file):
                open(output_file, "w")

            pipeline_run([])



    could be rewritten more laboriously as:

        ::


            from ruffus import *
            import os
            def check_file_exists(input_file, output_file):
                if os.path.exists(output_file):
                    return False, "File already exists"
                return True, "%s is missing" % output_file

            @parallel([[None, "a.1"]])
            @check_if_uptodate(check_file_exists)
            def create_if_necessary(input_file, output_file):
                open(output_file, "w")

            pipeline_run([create_if_necessary])



    Both produce the same output:
        ::

            Task = create_if_necessary
                Job = [null, "a.1"] completed




.. note::

    The function specified by :ref:`@check_if_uptodate <decorators.check_if_uptodate>` can be called
    more than once for each job.

    See the :ref:`description here <new_manual.dependencies>` of how *Ruffus* decides which tasks to run.


