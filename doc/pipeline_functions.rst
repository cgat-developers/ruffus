.. _pipeline_functions:

See :ref:`Decorators <decorators>` for more decorators

.. |pipeline_run| replace:: `pipeline_run`
.. _pipeline_run: `pipeline_functions.pipeline_run`_
.. |pr_target_tasks| replace:: `target_tasks`
.. _pr_target_tasks: `pipeline_functions.pipeline_run.target_tasks`_
.. |pr_forcedtorun_tasks| replace:: `forcedtorun_tasks`
.. _pr_forcedtorun_tasks: `pipeline_functions.pipeline_run.forcedtorun_tasks`_
.. |pr_multiprocess| replace:: `multiprocess`
.. _pr_multiprocess: `pipeline_functions.pipeline_run.multiprocess`_
.. |pr_logger| replace:: `logger`
.. _pr_logger: `pipeline_functions.pipeline_run.logger`_
.. |pr_gnu_make_maximal_rebuild_mode| replace:: `gnu_make_maximal_rebuild_mode`
.. _pr_gnu_make_maximal_rebuild_mode: `pipeline_functions.pipeline_run.gnu_make_maximal_rebuild_mode`_
.. |pr_verbose| replace:: `verbose`
.. _pr_verbose: `pipeline_functions.pipeline_run.verbose`_


.. ::
    .. |pp_output_stream| replace:: `output_stream`
    .._pp_output_stream: `pipeline_functions.pipeline_printout_graph.output_stream`_
    .. |pp_target_tasksppg| replace:: `target_tasks`
    .._pp_target_tasksppg: `pipeline_functions.pipeline_printout_graph.target_tasks`_
    .. |pp_forcedtorun_tasksppg| replace:: `forcedtorun_tasks`
    .._pp_forcedtorun_tasksppg: `pipeline_functions.pipeline_printout_graph.forcedtorun_tasks`_
    .. |pp_verbose| replace:: `verbose`
    .._pp_verbose: `pipeline_functions.pipeline_printout_graph.verbose`_
    .. |pp_indent| replace:: `indent`
    .._pp_indent: `pipeline_functions.pipeline_printout_graph.indent`_
    .. |pp_gnu_make_maximal_rebuild_mode| replace:: `gnu_make_maximal_rebuild_mode`
    .._pp_gnu_make_maximal_rebuild_mode: `pipeline_functions.pipeline_printout_graph.gnu_make_maximal_rebuild_mode`_
    .. |pp_test_all_task_for_update| replace:: `test_all_task_for_update`
    .._pp_test_all_task_for_update: `pipeline_functions.pipeline_printout_graph.test_all_task_for_update`_
    
    .. |ppg_stream| replace:: `stream`
    .._ppg_stream: `pipeline_functions.pipeline_printout.stream`_
    .. |ppg_output_format| replace:: `output_format`
    .._ppg_output_format: `pipeline_functions.pipeline_printout.output_format`_
    .. |ppg_target_taskspps| replace:: `target_tasks`
    .._ppg_target_taskspps: `pipeline_functions.pipeline_printout.target_tasks`_
    .. |ppg_forcedtorun_tasks| replace:: `forcedtorun_tasks`
    .._ppg_forcedtorun_tasks: `pipeline_functions.pipeline_printout.forcedtorun_tasks`_
    .. |ppg_draw_vertically| replace:: `draw_vertically`
    .._ppg_draw_vertically: `pipeline_functions.pipeline_printout.draw_vertically`_
    .. |ppg_ignore_upstream_of_target| replace:: `ignore_upstream_of_target`
    .._ppg_ignore_upstream_of_target: `pipeline_functions.pipeline_printout.ignore_upstream_of_target`_
    .. |ppg_skip_uptodate_tasks| replace:: `skip_uptodate_tasks`
    .._ppg_skip_uptodate_tasks: `pipeline_functions.pipeline_printout.skip_uptodate_tasks`_
    .. |ppg_gnu_make_maximal_rebuild_mode| replace:: `gnu_make_maximal_rebuild_mode`
    .._ppg_gnu_make_maximal_rebuild_mode: `pipeline_functions.pipeline_printout.gnu_make_maximal_rebuild_mode`_
    .. |ppg_test_all_task_for_update| replace:: `test_all_task_for_update`
    .._ppg_test_all_task_for_update: `pipeline_functions.pipeline_printout.test_all_task_for_update`_
    .. |ppg_no_key_legend| replace:: `no_key_legend`
    .._ppg_no_key_legend: `pipeline_functions.pipeline_printout.no_key_legend`_
    
    
    def pipeline_printout_graph (stream, 
                                 output_format,
                                 target_tasks, 
                                 forcedtorun_tasks              = [], 
                                 draw_vertically                = True, 
                                 ignore_upstream_of_target      = False,
                                 skip_uptodate_tasks            = False,
                                 gnu_make_maximal_rebuild_mode  = True,
                                 test_all_task_for_update       = True,
                                 no_key_legend                  = False):
    def pipeline_printout(output_stream, target_tasks, forcedtorun_tasks = [], verbose=0, indent = 4,
                                        gnu_make_maximal_rebuild_mode  = True,
                                        test_all_task_for_update        = True):
    

    def pipeline_run(target_tasks = [], forcedtorun_tasks = [], multiprocess = 1, logger = stderr_logger, 
                                    gnu_make_maximal_rebuild_mode  = True, verbose = 1):


.. _pipeline_functions.pipeline_printout_graph.output_stream:
.. _pipeline_functions.pipeline_printout_graph.target_tasks:
.. _pipeline_functions.pipeline_printout_graph.forcedtorun_tasks:
.. _pipeline_functions.pipeline_printout_graph.verbose:
.. _pipeline_functions.pipeline_printout_graph.indent:
.. _pipeline_functions.pipeline_printout_graph.gnu_make_maximal_rebuild_mode:
.. _pipeline_functions.pipeline_printout_graph.test_all_task_for_update:

.. _pipeline_functions.pipeline_printout.stream:
.. _pipeline_functions.pipeline_printout.output_format:
.. _pipeline_functions.pipeline_printout.target_tasks:
.. _pipeline_functions.pipeline_printout.forcedtorun_tasks:
.. _pipeline_functions.pipeline_printout.draw_vertically:
.. _pipeline_functions.pipeline_printout.ignore_upstream_of_target:
.. _pipeline_functions.pipeline_printout.skip_uptodate_tasks:
.. _pipeline_functions.pipeline_printout.gnu_make_maximal_rebuild_mode:
.. _pipeline_functions.pipeline_printout.test_all_task_for_update:
.. _pipeline_functions.pipeline_printout.no_key_legend:




.. _pipeline_functions.pipeline_run.target_tasks:
.. _pipeline_functions.pipeline_run.forcedtorun_tasks:
.. _pipeline_functions.pipeline_run.multiprocess:
.. _pipeline_functions.pipeline_run.logger:
.. _pipeline_functions.pipeline_run.gnu_make_maximal_rebuild_mode:
.. _pipeline_functions.pipeline_run.verbose:



################################################
Pipeline functions
################################################

    There are only three functions for **Ruffus** pipelines:

        * |pipeline_run|_ executes a pipeline
        * |pipeline_printout|_ prints a list of tasks and jobs which will be run in a pipeline
        * |pipeline_printout_graph|_ prints a schematic flowchart of pipeline tasks in various graphical formats

.. _pipeline_functions.pipeline_run:



**************************************************************************************************************************************************************************************
*pipeline_run* ( |pr_target_tasks|_, [ |pr_forcedtorun_tasks|_ = [], |pr_multiprocess|_, |pr_logger|_, |pr_gnu_make_maximal_rebuild_mode|_, |pr_verbose|_ ])
**************************************************************************************************************************************************************************************
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
        #. In the absence of input files (e.g. ``input == None``), the job will run if any output file is missing.
        #. In the absence of output files (e.g. ``output == None``), the job will always run.
        #. If any of the output files is missing, the job will run.
        #. If any of the input files is missing when the job is run, a
           ``MissingInputFileError`` exception will be raised.






