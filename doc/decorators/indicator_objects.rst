.. seealso::
    :ref:`Decorators <decorators>`



########################
Indicator Objects
########################

.. _indicator_objects:


    How *ruffus* disambiguates certain parameters to decorators.
    
    They are like `keyword arguments <http://docs.python.org/tutorial/controlflow.html#keyword-arguments>`_ in python, a little more verbose but they make the syntax much simpler.

    Indicator objects are also "self-documenting" so you can see
    exactly what is happening clearly.
    
.. _task.regex:

*********************************************
*regex(*\ `regular_expression`\ *)*
*********************************************
    The enclosed parameter is a python regular expression string, 
    which must be wrapped in a ``regex`` indicator object.
    
    See python `regular expression (re) <http://docs.python.org/library/re.html>`_ 
    documentation for details of regular expression syntax


    **Used by:**

        * :ref:`@transform <task.transform>`
        * :ref:`@collate <task.collate>`
        * The advanced form of :ref:`@transform <task.transform_ex>`
        * The deprecated :ref:`@files_re <task.files_re>`
   
    **Example**:
        ::
        
            @transform(previous_task, regex(r".c$"), ".o")
            def compile(infile, outfile):
                pass


.. _task.suffix:

*********************************************
*suffix(*\ `string`\ *)*
*********************************************
    The enclosed parameter is a string which must match *exactly* to the end
    of a file name.
    

    **Used by:**
        * :ref:`@transform <task.transform>`
        * The advanced form of :ref:`@transform <task.transform_ex>`
   
    **Example**:
        ::
        
            #
            #   Transforms ``*.c`` to ``*.o``::
            #
            @transform(previous_task, suffix(".c"), ".o")
            def compile(infile, outfile):
                pass

.. _task.inputs:

***************************************
*inputs(*\ `input_file_pattern`\ *)*
***************************************
    The enclosed parameter is a pattern string which is used to construct input file
    names. 

    **Used by:**
        * The advanced form of :ref:`@transform <task.transform_ex>`
   
    **Example**:
        ::
        
             @transform(["x.c", "y.c"], regex(r"(.*).c"), inputs(r"\1.c", r"\1.h"), r"\1.o")
             def compile(infiles, outfile):
                 # do something here
                 pass
                 
        
        | The starting files names are ``x.c`` and ``y.c``.
        | The regular expression is ``r(.*).c`` so the first matching part 
          ``\1`` will be ``x`` and ``y``
        | Because the input file pattern is ``\1.c`` and ``\1.h``, the resulting input files will be:
        
        ::
        
            job1:   "x.c", "x.h"
            job2:   "y.c", "y.h"
            
.. _task.mkdir:

******************************************************************************************
*mkdir(*\ `directory_name1`, [`directory_name2`, ...]\ *)*
******************************************************************************************
    The enclosed parameter is a directory name or a sequence of directory names.
    These directories will be created as part of the prerequisites of running a task.

    **Used by:**
        * :ref:`@follows <task.follows>`
        
    **Example:**
        ::
        
            @follows(mkdir("/output/directory"))
            def task():
                pass


.. _task.touch_file:


******************************************************************************************
*touch_file(*\ `file_name`\ *)*
******************************************************************************************
    The enclosed parameter is a file name. This file will be ``touch``\ -ed after a 
    task is executed.
        
    This will change the date/time stamp of the ``file_name`` to the current date/time. 
    If the file does not exist, an empty file will be created.
        
    
    **Used by:**
        * :ref:`@posttask <task.posttask>`
        
    **Example:**
        ::
        
            @posttask(touch_file("task_completed.flag"))
            @files(None, "a.1")
            def do_task(input_file, output_file):
                pass


