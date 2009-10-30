.. _manual_10th_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run


###################################################################
Chapter 10: Generating parameters on the fly
###################################################################
    .. hlist::
    
       * :ref:`Manual overview <manual>` 
       * :ref:`@files syntax in detail <decorators.files>`

    Sometimes, it is necessary, or perhaps more convenient, to generate parameters on the fly or
    at runtime. This provides the maximum flexibility
    
    All this requires is a function which generate one list (or any sequence) of
    parameters per job. For example::
    
        from ruffus import *
        def generate_parameters_on_the_fly():
            """
            returns one list of parameters per job
            """
            parameters = [
                                ['A', 1, 2], # 1st job
                                ['B', 3, 4], # 2nd job
                                ['C', 5, 6], # 3rd job
                            ]
            for job_parameters in parameters:
                yield job_parameters
        
        @parallel(generate_parameters_on_the_fly)
        def parallel_task(name, param1, param2):
            sys.stderr.write("    Parallel task %s: " % name)
            sys.stderr.write("%d + %d = %d\n" % (param1, param2, param1 + param2))
        
        pipeline_run([parallel_task])
        
        
    .. ???

    Similarly produces::
   
        Task = parallel_task
            Parallel task A: 1 + 2 = 3
            Job = ["A", 1, 2] completed
            Parallel task B: 3 + 4 = 7
            Job = ["B", 3, 4] completed
            Parallel task C: 5 + 6 = 11
            Job = ["C", 5, 6] completed
    
        
    .. ???

    
    The parameters often need to be generated more than once (see 
    :ref:`below <checking-multiple-times>`).


**********************************************
 Permutations and Combinations
**********************************************
 N x M


                                                     

    
