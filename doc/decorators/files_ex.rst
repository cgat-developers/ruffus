.. include:: ../global.inc
.. _decorators.files_on_the_fly:
.. index::
    pair: @files (on-the-fly parameter generation); Syntax

.. seealso::

    * :ref:`@files <new_manual.on_the_fly>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

.. |custom_function| replace:: `custom_function`
.. _custom_function: `decorators.files.custom_function`_


################################################
Parameters on the fly with @files
################################################

*******************************************************************************************
*@files* (|custom_function|_)
*******************************************************************************************
    **Purpose:**

        Uses a custom function to generate sets of parameters to separate jobs which can run in parallel.

        The first two parameters in each set represent the input and output which are
        used to see if the job is out of date and needs to be (re-)run.

        By default, out of date checking uses input/output file timestamps.
        (On some file systems, timestamps have a resolution in seconds.)
        See :ref:`@check_if_uptodate() <decorators.check_if_uptodate>` for alternatives.

    **Example**:
        ::

            from ruffus import *
            def generate_parameters_on_the_fly():
                parameters = [
                                    ['input_file1', 'output_file1', 1, 2], # 1st job
                                    ['input_file2', 'output_file2', 3, 4], # 2nd job
                                    ['input_file3', 'output_file3', 5, 6], # 3rd job
                             ]
                for job_parameters in parameters:
                    yield job_parameters

            @files(generate_parameters_on_the_fly)
            def parallel_io_task(input_file, output_file, param1, param2):
                pass

            pipeline_run([parallel_task])

    is the equivalent of calling:
        ::

            parallel_io_task('input_file1', 'output_file1', 1, 2)
            parallel_io_task('input_file2', 'output_file2', 3, 4)
            parallel_io_task('input_file3', 'output_file3', 5, 6)


    **Parameters:**


.. _decorators.files.custom_function:

        * *custom_function*:
            Generator function which yields each time a complete set of parameters for one job

    **Checking if jobs are up to date:**
        Strings in ``input`` and ``output`` (including in nested sequences) are interpreted as file names and
        used to check if jobs are up-to-date.

        See :ref:`above <decorators.files.check_up_to_date>` for more details





