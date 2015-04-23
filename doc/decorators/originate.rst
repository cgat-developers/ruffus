.. include:: ../global.inc
.. _decorators.originate:
.. index::
    pair: @originate; Syntax

.. seealso::

    * :ref:`@originate <new_manual.originate>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

################################################
originate
################################################

************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
*@originate* ( |output|_, [|extras|_,...] )
************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

.. |output| replace:: `output`
.. _output: `decorators.originate.output`_
.. |extras| replace:: `extras`
.. _extras: `decorators.originate.extras`_


    **Purpose:**
        * Creates (originates) a set of starting file without dependencies from scratch  (*ex nihilo*!)
        * Only called to create files which do not exist.
        * Invoked onces (a job created) per item in the |output|_ list.

        .. note::

            The first argument for the task function is the |output|_. There is by definition no
            *input* for ``@originate``

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


.. _decorators.originate.output:

    * **output** = *output*
       * Can be a single file name or a list of files
       * Each item in the list is treated as the |output|_ of a separate job


.. _decorators.originate.extras:

    * **extras** = *extras*
       Any extra parameters are passed verbatim to the task function

       If you are using named parameters, these can be passed as a list, i.e. ``extras= [...]``

       Any extra parameters are consumed by the task function and not forwarded further down the pipeline.

