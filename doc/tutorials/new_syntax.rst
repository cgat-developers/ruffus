.. include:: ../global.inc

.. role:: raw-html(raw)
   :format: html

:raw-html:`<style> .highlight-blue {color:blue} </style>`

:raw-html:`<style> .highlight-red {color:red} </style>`

.. role:: highlight-red

.. role:: highlight-blue

..   :highlight-red:`Test.`

.. _new_syntax:


################################################################################
New Object Orientated Syntax
################################################################################

    Ruffus Pipelines can now be created and manipulated directly using :highlight-red:`Pipeline` and :highlight-red:`Task` objects instead of via decorators.

.. note::

    You may want to go through the :ref:`worked_example <new_syntax.worked_example>` first.


==============================================================================
Syntax
==============================================================================


    This traditional Ruffus code:

        .. <<python

        .. code-block:: python

            from ruffus import *

            # task function
            starting_files = ["input/a.fasta","input/b.fasta"]
            @transform(input      = starting_files,
                       filter     = suffix('.fasta'),
                       output     = '.sam',
                       output_dir = "output")
            def map_dna_sequence(input_file, output_file) :
                pass

            pipeline_run()


        ..
            python


    Can also be written as:

        .. <<python

        .. code-block:: python
            :emphasize-lines: 9

            from ruffus import *

            # undecorated task function
            def map_dna_sequence(input_file, output_file) :
                pass

            starting_files = ["input/a.fasta","input/b.fasta"]

            #   make ruffus Pipeline() object
            my_pipeline = Pipeline(name = "test")
            my_pipeline.transform(task_func  = map_dna_sequence,
                                  input      = starting_files,
                                  filter     = suffix('.fasta'),
                                  output     = '.sam',
                                  output_dir = "output")

            my_pipeline.run()
        ..
            python

    | The two different syntax are almost identical:
    | The first parameter **task_func=**\ ``your_python_function`` is mandatory.
    | Otherwise, all other parameters are in the same order as before, and can be given by position or as named arguments.

==============================================================================
Advantages
==============================================================================

    These are some of the advantages of the new syntax:

    #) **Pipeline topology is assembled in one place**

       This is a matter of personal preference.

       Nevertheless, using decorators to locally annotate python functions with pipeline parameters arguably
       helps separation of concerns.

    #) **Pipelines can be created** *on the fly*

       For example, using parameters parsed from configuration files.

       Ruffus pipelines no longer have to be defined at global scope.

    #) **Reuse common sub-pipelines**

       Shared sub pipelines can be created from discrete python modules and joined together
       as needed. Bioinformaticists may have "mapping", "aligning", "variant-calling" sub-pipelines etc.

    #) **Multiple Tasks can share the same python function**

       Tasks are normally referred to by their associated functions (as with decoratored Ruffus tasks).
       However, you can also disambiguate Tasks by specifying their name directly.

    #) **Pipeline topology can be specified at run time**

       Some (especially bioinformatics) tasks require binary merging. This can be very inconvenient.

       For example, if we have 8 data files, we need three successive rounds of merging (8->4->2->1)
       or three tasks) to produce the output. But if we are given 10 data files, we now find that
       we needed to have four tasks for four rounds of merging (10->5->3->2->1).

       There was previously no easy way to arrange different Ruffus topologies in response to the
       data. Now we can add as many extra merging tasks to our pipeline (all sharing the same underlying
       python function) as needed.



==============================================================================
Compatability
==============================================================================

    * The changes are fully backwards compatibile. All valid Ruffus code continues to work
    * Decorators and ``Pipeline`` objects can be used interchangeably:

    Decorated functions are automatically part of a default constructed ``Pipeline`` named ``"main"``.
      .. code-block:: python

          main_pipeline = Pipeline.pipelines["main"]

      ..

    In the following example, a pipeline using the
    Ruffus with classes syntax :highlight-red:`(1)` and :highlight-red:`(3)` has a traditionally decorated task function in the middle :highlight-red:`(2)`.


        .. <<python

        .. code-block:: python
            :emphasize-lines: 15, 21, 32

            from ruffus import *

            # get default pipeline
            main_pipeline = Pipeline.pipelines["main"]

            # undecorated task functions
            def compress_sam_to_bam(input_file, output_file) :
                open(output_file, "w").close()

            def create_files(output_file) :
                open(output_file, "w").close()


            #
            #   1. Ruffus with classes
            #
            starting_files = main_pipeline.originate(create_files, ["input/a.fasta","input/b.fasta"])\
                .follows(mkdir("input", "output"))

            #
            #   2. Ruffus with python decorations
            #
            @transform(starting_files,
                       suffix('.fasta'),
                       '.sam',
                       output_dir = "output")
            def map_dna_sequence(input_file, output_file) :
                open(output_file, "w").close()


            #
            #   3. Ruffus with classes
            #
            main_pipeline.transform(task_func   = compress_sam_to_bam,
                                    input       = map_dna_sequence,
                                    filter      = suffix(".sam"),
                                    output      = ".bam")

            # main_pipeline.run()
            #    or
            pipeline_run()


        ..
            python


==============================================================================
Class methods
==============================================================================

    The **ruffus.Pipeline** class has the following self-explanatory methods:

        .. <<python

        .. code-block:: python

            Pipeline.run(...)
            Pipeline.printout(...)
            Pipeline.printout_graph(...)

        ..
            python


    These methods return a **ruffus.Task** object

        .. <<python


        .. code-block:: python

            Pipeline.originate(...)
            Pipeline.transform(...)
            Pipeline.split(...)
            Pipeline.merge(...)
            Pipeline.mkdir(...)

            Pipeline.collate(...)
            Pipeline.subdivide(...)

            Pipeline.combinations(...)
            Pipeline.combinations_with_replacement(...)
            Pipeline.product(...)
            Pipeline.permutations(...)

            Pipeline.follows(...)
            Pipeline.check_if_uptodate(...)
            Pipeline.graphviz(...)

            Pipeline.files(...)
            Pipeline.parallel(...)

        ..
            python


    A Ruffus **Task** can be modified with the following methods

        .. <<python

        .. code-block:: python

            Task.active_if(...)
            Task.check_if_uptodate(...)
            Task.follows(...)
            Task.graphviz(...)
            Task.jobs_limit(...)
            Task.mkdir(...)
            Task.posttask(...)

        ..
            python

==============================================================================
Call chaining
==============================================================================

    The syntax is designed to allow call chaining:

        .. <<python

        .. code-block:: python

            Pipeline.transform(...)\
                .mkdir(follows(...))\
                .active_if(...)\
                .graphviz(...)

        ..
            python


==============================================================================
Referring to Tasks
==============================================================================

    Ruffus pipelines are chained together or specified by referring to each stage or Task.

    :highlight-red:`(1)` and :highlight-red:`(2)` are ways to referring to tasks that Ruffus has always supported.

    :highlight-red:`(3)` - :highlight-red:`(6)` are new to Ruffus v 2.6 but apply
    to both using decorators or the new Ruffus with classes syntax.

______________________________________________________________________________
1) Python function
______________________________________________________________________________

       .. <<python

       .. code-block:: python

        @transform(prev_task, ...)
        def next_task():
            pass

        pipeline.transform(input = next_task, ...)

       ..
           python

______________________________________________________________________________
2) Python function name (using *output_from*)
______________________________________________________________________________


       .. <<python

       .. code-block:: python

        pipeline.transform(input = output_from("prev_task"), ...)

       ..
           python

.. note::

   The above :highlight-red:`(1) and (2) only work if the Python function specifies the task unambiguously in a pipeline.`
   If you reuse the same Python function for multiple tasks, use the following methods.

   Ruffus will complain with Exceptions if your code is ambiguous.


______________________________________________________________________________
3) Task object
______________________________________________________________________________


       .. <<python

       .. code-block:: python
           :emphasize-lines: 3

            prev_task = pipeline.transform(...)

            # prev_task is a Task object
            next_task = pipeline.transform(input = prev_task, ....)

       ..
           python

______________________________________________________________________________
4) Task name (using *output_from*)
______________________________________________________________________________


       .. <<python

       .. code-block:: python
           :emphasize-lines: 1

           # name this task "prev_task"
           pipeline.transform(name = "prev_task",...)

           pipeline.transform(input = output_from("prev_task"), ....)

       ..
           python

       .. note::

           Tasks from other pipelines can be referred to using full qualified names in the **pipeline**::*task* format

           .. <<python

           .. code-block:: python

               pipeline.transform(input = output_from("other_pipeline::prev_task"), ....)

           ..
               python


______________________________________________________________________________
5) Pipeline
______________________________________________________________________________


    When we are assembling our pipeline from sub-pipelines (especially those in other modules which other people might have written)
    it is inconvenient to break encapsulation to find out the component **Task** of the subpipeline.

    In which case, the sub-pipeline author can assign particular tasks to the **head** and **tail** of the pipeline.
    The pipeline will be an alias for these:

    .. <<python

    .. code-block:: python
         :emphasize-lines: 5,8

         # Note: these functions take lists
         sub_pipeline.set_head_tasks([first_task])
         sub_pipeline.set_tail_tasks([last_task])

         # first_task.set_input(...)
         sub_pipeline.set_input(input = "*.txt")

         # (input = last_task,...)
         main_pipeline.transform(input = sub_pipeline, ....)

    ..
           python


    If you don't have access to a pipeline object, you can look it up via the Pipeline object

         .. code-block:: python
              :emphasize-lines: 1

              # This is the default "main" pipeline which holds decorated task functions
              main_pipeline = Pipeline.pipelines["main"]

              my_pipeline = Pipeline("test")

              alias_to_my_pipeline = Pipeline.pipelines["test"]

         ..
                python



______________________________________________________________________________
6) Lookup Task via the Pipeline
______________________________________________________________________________

        We can ask a Pipeline to lookup task names, functions and function names for us.

        .. <<python

        .. code-block:: python
            :emphasize-lines: 1,4,7

            # Lookup task name
            pipeline.transform(input = pipeline["prev_task"], ....)

            # Lookup via python function
            pipeline.transform(input = pipeline[python_function], ....)

            # Lookup via python function name
            pipeline.transform(input = pipeline["python_function_name"], ....)

        ..
           python

        This is straightforward if the lookup is unambiguous for the pipeline.

        If the names are not found in the pipeline, Ruffus will look across all pipelines.

        Any ambiguities will result in an immediate error.

        *In extremis*, you can use pipeline qualified names


        .. <<python

        .. code-block:: python
            :emphasize-lines: 1

            # Pipeline qualified task name
            pipeline.transform(input = pipeline["other_pipeline::prev_task"], ....)

        ..
           python



.. note::

    All this will be much clearer going through the :ref:`worked_example <new_syntax.worked_example>`.

.. toctree::
   :maxdepth: 2
   :hidden:

   new_syntax_worked_example.rst
   new_syntax_worked_example_code.rst

