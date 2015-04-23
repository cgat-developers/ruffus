.. include:: ../global.inc
.. _decorators.files:
.. index::
    pair: @files; Syntax

.. seealso::

    * :ref:`@files (deprecated) <new_manual.deprecated_files>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

.. |input| replace:: `input`
.. _input: `decorators.files.input`_
.. |input1| replace:: `input1`
.. _input1: `decorators.files.input1`_
.. |output| replace:: `output`
.. _output: `decorators.files.output`_
.. |output1| replace:: `output1`
.. _output1: `decorators.files.output1`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.files.extra_parameters`_
.. |extra_parameters1| replace:: `extra_parameters1`
.. _extra_parameters1: `decorators.files.extra_parameters1`_


########################
files
########################

*******************************************************************************************
*@files* (|input1|_, |output1|_, [|extra_parameters1|_, ...])
*******************************************************************************************
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@files for single jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Purpose:**
        Provides parameters to run a task.

        The first two parameters in each set represent the input and output which are
        used to see if the job is out of date and needs to be (re-)run.

        By default, out of date checking uses input/output file timestamps.
        (On some file systems, timestamps have a resolution in seconds.)
        See :ref:`@check_if_uptodate() <decorators.check_if_uptodate>` for alternatives.


    **Example**:
        ::

            from ruffus import *
            @files('a.1', 'a.2', 'A file')
            def transform_files(infile, outfile, text):
                pass
            pipeline_run([transform_files])

    If ``a.2`` is missing or was created before ``a.1``, then the following will be called:
        ::

            transform_files('a.1', 'a.2', 'A file')

    **Parameters:**

.. _decorators.files.input1:

    * *input*
        Input file names


.. _decorators.files.output1:

    * *output*
        Output file names


.. _decorators.files.extra_parameters1:

    * *extra_parameters*
        optional ``extra_parameters`` are passed verbatim to each job.


    **Checking if jobs are up to date:**
        Strings in ``input`` and ``output`` (including in nested sequences) are interpreted as file names and
        used to check if jobs are up-to-date.

        See :ref:`above <decorators.files.check_up_to_date>` for more details


*******************************************************************************************
*@files* ( *((* |input|_, |output|_, [|extra_parameters|_,...] *), (...), ...)* )
*******************************************************************************************
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@files in parallel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    **Purpose:**

        Passes each set of parameters to separate jobs which can run in parallel

        The first two parameters in each set represent the input and output which are
        used to see if the job is out of date and needs to be (re-)run.

        By default, out of date checking uses input/output file timestamps.
        (On some file systems, timestamps have a resolution in seconds.)
        See :ref:`@check_if_uptodate() <decorators.check_if_uptodate>` for alternatives.

    **Example**:
        ::

            from ruffus import *
            parameters = [
                                [ 'a.1', 'a.2', 'A file'], # 1st job
                                [ 'b.1', 'b.2', 'B file'], # 2nd job
                          ]

            @files(parameters)
            def parallel_io_task(infile, outfile, text):
                pass
            pipeline_run([parallel_io_task])

    is the equivalent of calling:
        ::

            parallel_io_task('a.1', 'a.2', 'A file')
            parallel_io_task('b.1', 'b.2', 'B file')

    **Parameters:**

.. _decorators.files.input:

    * *input*
        Input file names


.. _decorators.files.output:

    * *output*
        Output file names


.. _decorators.files.extra_parameters:

    * *extra_parameters*
        optional ``extra_parameters`` are passed verbatim to each job.

.. _decorators.files.check_up_to_date:

    **Checking if jobs are up to date:**
        #. Strings in ``input`` and ``output`` (including in nested sequences) are interpreted as file names and
           used to check if jobs are up-to-date.
        #. In the absence of input files (e.g. ``input is None``), the job will run if any output file is missing.
        #. In the absence of output files (e.g. ``output is None``), the job will always run.
        #. If any of the output files is missing, the job will run.
        #. If any of the input files is missing when the job is run, a
           ``MissingInputFileError`` exception will be raised.


