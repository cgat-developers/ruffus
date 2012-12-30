.. include:: ../../global.inc
.. _Simple_Tutorial_2nd_step_code:

###################################################################
Code for Step 2: Passing parameters to the pipeline
###################################################################
* :ref:`Up <Simple_Tutorial>` 
* :ref:`Back <Simple_Tutorial_2nd_step>` 
* :ref:`@transform syntax <decorators.transform>` in detail

************************************
Code
************************************
::

from ruffus import *

#---------------------------------------------------------------
#   Create input files
#
first_task_params = [
                    'job1.input', 
                    'job2.input'
                    ]

for input_file in first_task_params:
    open(input_file, "w")


#---------------------------------------------------------------
#
#   first task
#
@transform(first_task_params, suffix(".input"), ".output1",
                       "some_extra.string.for_example", 14)
def first_task(input_file, output_file,
                extra_parameter_str, extra_parameter_num):
    # make output file
    open(output_file, "w")


#---------------------------------------------------------------
#
#   second task
#
#@follows(first_task)
@transform(first_task, suffix(".output1"), ".output2")
def second_task(input_file, output_file):
    # make output file
    open(output_file, "w")

#---------------------------------------------------------------
#
#       Run
#
pipeline_run([second_task])


************************************
Resulting Output
************************************
    ::

        >>> pipeline_run([second_task])
            Job  = [job1.input -> job1.output1] completed
            Job  = [job2.input -> job2.output1] completed
        Completed Task = first_task

                1st Extra Parameter = some_extra.string.for_example
                2nd Extra Parameter = 14
            Job  = [job1.output1 -> job1.output2, some_extra.string.for_example, 14] completed

                1st Extra Parameter = some_extra.string.for_example
                2nd Extra Parameter = 14
            Job  = [job2.output1 -> job2.output2, some_extra.string.for_example, 14] completed
        Completed Task = second_task




>>> pipeline_run([first_task])
    Job  = [job1.input -> job1.output1] completed
    Job  = [job2.input -> job2.output1] completed
Completed Task = first_task



from ruffus import *

#---------------------------------------------------------------
#   Create input files
#
first_task_params = [   'job1.input', 
                        'job2.input'    ]
for input_file in first_task_params:
    open(input_file, "w")


#---------------------------------------------------------------
#
#   first task
#
@transform(first_task_params, suffix(".input"), ".output1", 
           "some_extra.string.for_example", 14)
def first_task(input_file, output_file):
    # make output file
    open(output_file, "w")


#---------------------------------------------------------------
#
#       Run
#
pipeline_run([second_task])

