.. _pipeline_functions:

See :ref:`Decorators <decorators>` for more decorators


.. |pipeline_run| replace:: `pipeline_run`
.. _pipeline_run: `pipeline_functions.pipeline_run`_
.. |target_tasks| replace:: `target_tasks`
.. _target_tasks: `pipeline_functions.pipeline_run.target_tasks`_
.. |forcedtorun_tasks| replace:: `forcedtorun_tasks`
.. _forcedtorun_tasks: `pipeline_functions.pipeline_run.forcedtorun_tasks`_
.. |multiprocess| replace:: `multiprocess`
.. _multiprocess: `pipeline_functions.pipeline_run.multiprocess`_
.. |logger| replace:: `logger`
.. _logger: `pipeline_functions.pipeline_run.logger`_
.. |gnu_make_maximal_rebuild_mode| replace:: `gnu_make_maximal_rebuild_mode`
.. _gnu_make_maximal_rebuild_mode: `pipeline_functions.pipeline_run.gnu_make_maximal_rebuild_mode`_
.. |verbose| replace:: `verbose`
.. _verbose: `pipeline_functions.pipeline_run.verbose`_

.. |output_stream| replace:: `output_stream`
.. _output_stream: `pipeline_functions.pipeline_printout_graph.output_stream`_
.. |target_tasks| replace:: `target_tasks`
.. _target_tasks: `pipeline_functions.pipeline_printout_graph.target_tasks`_
.. |forcedtorun_tasks| replace:: `forcedtorun_tasks`
.. _forcedtorun_tasks: `pipeline_functions.pipeline_printout_graph.forcedtorun_tasks`_
.. |verbose| replace:: `verbose`
.. _verbose: `pipeline_functions.pipeline_printout_graph.verbose`_
.. |indent| replace:: `indent`
.. _indent: `pipeline_functions.pipeline_printout_graph.indent`_
.. |gnu_make_maximal_rebuild_mode| replace:: `gnu_make_maximal_rebuild_mode`
.. _gnu_make_maximal_rebuild_mode: `pipeline_functions.pipeline_printout_graph.gnu_make_maximal_rebuild_mode`_
.. |test_all_task_for_update| replace:: `test_all_task_for_update`
.. _test_all_task_for_update: `pipeline_functions.pipeline_printout_graph.test_all_task_for_update`_

.. |stream| replace:: `stream`
.. _stream: `pipeline_functions.pipeline_printout.stream`_
.. |output_format| replace:: `output_format`
.. _output_format: `pipeline_functions.pipeline_printout.output_format`_
.. |target_tasks| replace:: `target_tasks`
.. _target_tasks: `pipeline_functions.pipeline_printout.target_tasks`_
.. |forcedtorun_tasks| replace:: `forcedtorun_tasks`
.. _forcedtorun_tasks: `pipeline_functions.pipeline_printout.forcedtorun_tasks`_
.. |draw_vertically| replace:: `draw_vertically`
.. _draw_vertically: `pipeline_functions.pipeline_printout.draw_vertically`_
.. |ignore_upstream_of_target| replace:: `ignore_upstream_of_target`
.. _ignore_upstream_of_target: `pipeline_functions.pipeline_printout.ignore_upstream_of_target`_
.. |skip_uptodate_tasks| replace:: `skip_uptodate_tasks`
.. _skip_uptodate_tasks: `pipeline_functions.pipeline_printout.skip_uptodate_tasks`_
.. |gnu_make_maximal_rebuild_mode| replace:: `gnu_make_maximal_rebuild_mode`
.. _gnu_make_maximal_rebuild_mode: `pipeline_functions.pipeline_printout.gnu_make_maximal_rebuild_mode`_
.. |test_all_task_for_update| replace:: `test_all_task_for_update`
.. _test_all_task_for_update: `pipeline_functions.pipeline_printout.test_all_task_for_update`_
.. |no_key_legend| replace:: `no_key_legend`
.. _no_key_legend: `pipeline_functions.pipeline_printout.no_key_legend`_












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
def pipeline_run(
target_tasks = [], 
forcedtorun_tasks = [], 
multiprocess = 1, 
logger = stderr_logger, 
gnu_make_maximal_rebuild_mode  = True, 
verbose = 1):

################################################
Pipeline functions
################################################

    There are only three functions for **Ruffus** pipelines:

        * |pipeline_run|_ executes a pipeline
        * |pipeline_printout|_ prints a list of tasks and jobs which will be run in a pipeline
        * |pipeline_printout_graph|_ prints a schematic flowchart of pipeline tasks in various graphical formats

*******************************************************************************************
*pipeline_run* ( *((* |input|_, |output|_, [|extra_parameters|_,...] *), (...), ...)* )
*******************************************************************************************
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

########################################################################
Passing parameters to @files with a custom function
########################################################################
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
            
            


########################
@files for a single job
########################

*******************************************************************************************
*@files* (|input1|_, |output1|_, [|extra_parameters1|_, ...])
*******************************************************************************************

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

