.. include:: ../global.inc
.. _decorators.originate:
.. index::
    pair: @originate; Syntax

.. seealso::

    * :ref:`Decorators <decorators>` for more decorators

########################
@originate
########################

.. |output_files| replace:: `output_files`
.. _output_files: `decorators.originate.output_files`_
.. |extra_parameters| replace:: `extra_parameters`
.. _extra_parameters: `decorators.originate.extra_parameters`_


***********************************************************************************************************************************************************
*@originate* ( |output_files|_, [|extra_parameters|_,...] )
***********************************************************************************************************************************************************
    **Purpose:**
        * Creates (originates) a set of starting file without dependencies from scratch  (*ex nihilo*!)
        * Only called to create files which do not exist.
        * Invoked onces (a job created) per item in the ``output_files`` list.

        .. note::

            The first argument for the task function is the *Output*. There is by definition no
            *Input* for ``@originate``

    **Example**:

        .. code-block:: python

            from ruffus import *
            @originate(["a", "b", "c", "d"], "extra")
            def test(output_file, extra):
                open(output_file, "w")

            pipeline_run()

        .. code-block:: pycon
            :emphasize-lines: 8,11

            >>> pipeline_run()
                Job  = [None -> a, extra] completed
                Job  = [None -> b, extra] completed
                Job  = [None -> c, extra] completed
                Job  = [None -> d, extra] completed
            Completed Task = test

            >>> # all files exist: nothing to do
            >>> pipeline_run()

            >>> # delete 'a' so that it is missing
            >>> import os
            >>> os.unlink("a")

            >>> pipeline_run()
                Job  = [None -> a, extra] completed
            Completed Task = test

    **Parameters:**


.. _decorators.originate.output_files:

    * *output_files*
       * Can be a single file name or a list of files
       * Each item in the list is treated as the *Output* of a separate job


.. _decorators.originate.extra_parameters:

    * *extra_parameters*
        Any extra parameters are passed verbatim to the task function

