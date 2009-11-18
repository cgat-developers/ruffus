.. seealso::
    :ref:`Decorators <decorators>`

.. index:: 
    single: Indicator Object (Disambiguating parameters)
.. _indicator_objects:


########################
Indicator Objects
########################



    How *ruffus* disambiguates certain parameters to decorators.
    
    They are like `keyword arguments <http://docs.python.org/tutorial/controlflow.html#keyword-arguments>`_ in python, a little more verbose but they make the syntax much simpler.

    Indicator objects are also "self-documenting" so you can see
    exactly what is happening clearly.
    
.. _decorators.regex:
.. index:: 
    pair: regex; Indicator Object (Disambiguating parameters)

*********************************************
*regex(*\ `regular_expression`\ *)*
*********************************************
    The enclosed parameter is a python regular expression string, 
    which must be wrapped in a ``regex`` indicator object.
    
    See python `regular expression (re) <http://docs.python.org/library/re.html>`_ 
    documentation for details of regular expression syntax


    **Used by:**

        * :ref:`@transform <decorators.transform>`
        * :ref:`@collate <decorators.collate>`
        * The advanced form of :ref:`@transform <decorators.transform_ex>`
        * The deprecated :ref:`@files_re <decorators.files_re>`
   
    **Example**:
        ::
        
            @transform(previous_task, regex(r".c$"), ".o")
            def compile(infile, outfile):
                pass


.. _decorators.suffix:
.. index:: 
    pair: suffix; Indicator Object (Disambiguating parameters)

*********************************************
*suffix(*\ `string`\ *)*
*********************************************
    The enclosed parameter is a string which must match *exactly* to the end
    of a file name.
    

    **Used by:**
        * :ref:`@transform <decorators.transform>`
        * The advanced form of :ref:`@transform <decorators.transform_ex>`
   
    **Example**:
        ::
        
            #
            #   Transforms ``*.c`` to ``*.o``::
            #
            @transform(previous_task, suffix(".c"), ".o")
            def compile(infile, outfile):
                pass

.. _decorators.inputs:
.. index:: 
    pair: inputs; Indicator Object (Disambiguating parameters)

***************************************
*inputs(*\ `input_file_pattern`\ *)*
***************************************
    The enclosed parameter is a pattern string which is used to construct input file
    names. 

    **Used by:**
        * The advanced form of :ref:`@transform <decorators.transform_ex>`
   
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
            
.. _decorators.mkdir:


.. index:: 
    single: @follows; mkdir (Syntax)
    single: mkdir; @follows (Syntax)
    single: Indicator Object (Disambiguating parameters); mkdir

******************************************************************************************
*mkdir(*\ `directory_name1`, [`directory_name2`, ...]\ *)*
******************************************************************************************
    The enclosed parameter is a directory name or a sequence of directory names.
    These directories will be created as part of the prerequisites of running a task.

    **Used by:**
        * :ref:`@follows <decorators.follows>`
        
    **Example:**
        ::
        
            @follows(mkdir("/output/directory"))
            def task():
                pass


.. _decorators.touch_file:

.. index:: 
    single: @posttask; touch_file (Syntax)
    single: touch_file; @posttask (Syntax)
    single: Indicator Object (Disambiguating parameters); touch_file


******************************************************************************************
*touch_file(*\ `file_name`\ *)*
******************************************************************************************
    The enclosed parameter is a file name. This file will be ``touch``\ -ed after a 
    task is executed.
        
    This will change the date/time stamp of the ``file_name`` to the current date/time. 
    If the file does not exist, an empty file will be created.
        
    
    **Used by:**
        * :ref:`@posttask <decorators.posttask>`
        
    **Example:**
        ::
        
            @posttask(touch_file("task_completed.flag"))
            @files(None, "a.1")
            def do_task(input_file, output_file):
                pass


.. _decorators.combine:
.. index:: 
    single: @files_re; combine (Syntax)
    single: combine; @follows (Syntax)
    single: Indicator Object (Disambiguating parameters); combine

******************************************************************************************
*combine(*\ `arguments`\ *)*
******************************************************************************************
    Indicates that the *inputs* of :ref:`@files_re <decorators.files_re>` will be collated
    or summarised into *outputs* by category. See the :ref:`Manual <manual.files_re.combine>`  or
    :ref:` @collate <manual.collate>` for examples.
    
    This is deprecated syntax.    
    
    **Used by:**
        * :ref:`@files_re <manual.files_re.combine>`
        
    **Example:**
        ::
        
            @files_re('*.animals',                           # inputs = all *.animal files
                        r'mammals.([^.]+)',                  # regular expression
                        combine(r'\1/animals.in_my_zoo'),    # single output file per species
                        r'\1' )                              # species name
            def capture_mammals(infiles, outfile, species):
                # summarise all animals of this species
                ""

.. _decorators.output_from:
.. index:: 
    pair: output_from; Indicator Object (Disambiguating parameters)

******************************************************************************************
*output_from(*\ `file_name_string1`\ *[,*\ `file_name_string1` , ... *]* *)*
******************************************************************************************
    Indicates that any enclosed strings are not file names but refer to task functions.    
    
    **Used by:**
        * :ref:`@files <decorators.files>`
        * :ref:`@split <decorators.split>`
        * :ref:`@transform <decorators.transform>`
        * :ref:`@merge <decorators.merge>`
        * :ref:`@collate <decorators.collate>`
        
    **Example:**
        ::
        
            @split(["a.file", ("b.file", output_from("task1", 76, "task2"))], "*.split")
            def task2(input, output):
                pass


        is equivalent to:
    
        ::
        
            @split(["a.file", ("b.file", (task1, 76, task2))], "*.split")
            def task2(input, output):
                pass
                

        

