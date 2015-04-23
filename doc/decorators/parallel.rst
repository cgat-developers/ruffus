.. include:: ../global.inc
.. _decorators.parallel:
.. index::
    pair: @parallel; Syntax

.. seealso::

    * :ref:`@parallel <new_manual.parallel>` in the **Ruffus** Manual
    * :ref:`Decorators <decorators>` for more decorators

########################
parallel
########################

.. |job_params| replace:: `job_params`
.. _job_params: `decorators.parallel.job_params`_
.. |parameter_generating_function| replace:: `parameter_generating_function`
.. _parameter_generating_function: `decorators.parallel.parameter_generating_function`_


*****************************************************************************************************************************************
*@parallel* ( [ [|job_params|_, ...], [|job_params|_, ...]...] | |parameter_generating_function|_)
*****************************************************************************************************************************************
    **Purpose:**
        To apply the (task) function to a set of parameters in parallel without file dependency checking.

        Most useful allied to :ref:`@check_if_uptodate() <decorators.check_if_uptodate>`

    **Example**::

        from ruffus import *
        parameters = [
                         ['A', 1, 2], # 1st job
                         ['B', 3, 4], # 2nd job
                         ['C', 5, 6], # 3rd job
                     ]
        @parallel(parameters)
        def parallel_task(name, param1, param2):
            sys.stderr.write("    Parallel task %s: " % name)
            sys.stderr.write("%d + %d = %d\\n" % (param1, param2, param1 + param2))

        pipeline_run([parallel_task])

    **Parameters:**


.. _decorators.parallel.job_params:

    * *job_params*:
        Requires a sequence of parameters, one set for each job.

        Each set of parameters can be one or more items in a sequence which will be passed to
        the decorated task function iteratively (or in parallel)

        For example::

            parameters = [
                             ['A', 1, 2], # 1st job
                             ['B', 3, 4], # 2nd job
                             ['C', 5, 6], # 3rd job
                         ]
            @parallel(parameters)
            def parallel_task(name, param1, param2):
                pass

        Will result in the following function calls::

            parallel_task('A', 1, 2)
            parallel_task('B', 3, 4)
            parallel_task('C', 5, 6)



.. _decorators.parallel.parameter_generating_function:

    * *parameter_generating_function*
        #. A generator yielding  set of parameters (as above) in turn and on the fly
        #. A function returning a sequence of parameter sets, as above



