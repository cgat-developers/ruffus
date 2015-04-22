.. include:: ../global.inc
.. _decorators.check_if_uptodate:

.. index::
    pair: @check_if_uptodate; Syntax

.. seealso::

    * :ref:`@check_if_uptodate <new_manual.check_if_uptodate>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

.. |dependency_checking_function| replace:: `dependency_checking_function`
.. _dependency_checking_function: `decorators.check_if_uptodate.dependency_checking_function`_

########################
check_if_uptodate
########################

*******************************************************************************************
*@check_if_uptodate* (|dependency_checking_function|_)
*******************************************************************************************

    **Purpose:**
        Checks to see if a job is up to date, and needs to be run.

        Usually used in conjunction with :ref:`@parallel() <decorators.parallel>`

    **Example**::

        from ruffus import *
        import os
        def check_file_exists(input_file, output_file):
            if not os.path.exists(output_file):
                return True, "Missing file %s" % output_file
            else:
                return False, "File %s exists" % output_file

        @parallel([[None, "a.1"]])
        @check_if_uptodate(check_file_exists)
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")

        pipeline_run([create_if_necessary])

    Is equivalent to::

        from ruffus import *
        @files(None, "a.1")
        def create_if_necessary(input_file, output_file):
            open(output_file, "w")

        pipeline_run([create_if_necessary])

    Both produce the same output::

        Task = create_if_necessary
            Job = [null, "a.1"] completed

    **Parameters:**

.. _decorators.check_if_uptodate.dependency_checking_function:

    * *dependency_checking_function*:
            returns two parameters: if job needs to be run, and a message explaining why

            dependency_checking_func() needs to handle the same number of parameters as the
            task function e.g. ``input_file`` and ``output_file`` above.


