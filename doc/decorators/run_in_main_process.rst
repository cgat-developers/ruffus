.. include:: ../global.inc
.. _decorators.run_in_main_process:

run_in_main_process
===================

``@run_in_main_process()`` executes a task in the process and thread calling
``pipeline_run``, even when other tasks use a multiprocessing pool. Use it for
tasks that create their own multiprocessing children or require the main thread.
Call ``pipeline_run`` from the main thread when the task requires it.

.. code-block:: python

    from multiprocessing import get_context
    from ruffus import originate, pipeline_run, run_in_main_process

    def calculate(value):
        return value * value

    @run_in_main_process()
    @originate("results.txt")
    def calculate_results(outfile):
        with get_context("spawn").Pool(2) as pool:
            results = pool.map(calculate, range(10))
        with open(outfile, "w") as stream:
            stream.write(str(results))

    if __name__ == "__main__":
        pipeline_run([calculate_results], multiprocess=4)

The object-oriented equivalent is:

.. code-block:: python

    pipeline.originate(calculate_results, "results.txt").run_in_main_process()

Other tasks continue to use Ruffus's configured pool. Jobs already submitted to
that pool can run while the main-process task executes. Main-process jobs run one
at a time and count towards Ruffus's concurrency limit. The scheduler cannot
process results or submit newly available jobs until the main-process task
returns. Child processes created by the task are not counted in Ruffus's limit;
the task must manage and clean up its own children.

``jobs_limit`` remains a separate concurrency control. In particular,
``jobs_limit(1)`` alone does not move a task out of the process pool. Named limits
are still shared between main-process and worker tasks.

Main-process tasks use the normal dependency, checkpoint and exception handling.
They share the caller's state, so changes to globals or the working directory
affect the pipeline. Use ``spawn`` for nested multiprocessing rather than forking
a process that already has worker-management threads running. Ordinary Python
multiprocessing requirements for importable child functions and a main guard
still apply.

This option supports the default ``pool_manager="multiprocessing"`` with either
process or thread workers. Parallel runs with the gevent pool manager reject it.
Serial execution is unchanged.
