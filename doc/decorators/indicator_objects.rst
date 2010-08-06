.. include:: ../global.inc
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

.. _decorators.add_inputs:
.. index:: 
    pair: add_inputs; Indicator Object (Adding additional input parameters)

***********************************************
*add_inputs(*\ `input_file_pattern`\ *)*
***********************************************
    The enclosed parameter(s) are pattern strings or a nested structure which is added to the
    input for each job. 
    
    **Used by:**
        * :ref:`@transform <decorators.transform_ex>`
          ``regex(...)`` and ``suffix(...)`` only
        * :ref:`@collate <decorators.transform_ex>`
          ``regex(...)`` only 
        * :ref:`@split <decorators.transform_ex>`
          ``regex(...)`` only 
   
    **Example @transform with suffix(...)**

        A common task in compiling C code is to include the corresponding header file for the source.
        To compile ``*.c`` to ``*.o``, adding ``*.h`` and the common header ``universal.h``:

            ::

                @transform(["1.c", "2.c"], suffix(".c"), add_inputs([r"\1.h", "universal.h"]),  ".o")
                def compile(infile, outfile):
                    # do something here
                    pass

        | The starting files names are ``1.c`` and ``2.c``.
        | ``suffix(".c")`` matches ".c" so ``\1`` stands for the unmatched prefices  ``"1"`` and ``"2"``
        This will result in the following functional calls:
            ::    
            
                compile(["1.c", "1.h", "universal.h"], "1.o")
                compile(["2.c", "2.h", "universal.h"], "2.o")


        A string like ``universal.h`` in ``add_inputs`` will added *as is*. 
        ``r"\1.h"``, however, performs suffix substitution, with the special form ``r"\1"`` matching everything up to the suffix.
        Remember to 'escape' ``r"\1"`` otherwise Ruffus will complain and throw an ``Exception`` to remind you.
        The most convenient way is to use a python "raw" string.

    **Example of add_inputs(...) with regex(...)**

        The suffix match (``suffix(...)``) is exactly equivalent to the following code using regular expression (``regex(...)``):
            ::
                
                @transform(["1.c", "2.c"], regex(r"^(.+)\.c$"), add_inputs([r"\1.h", "universal.h"]),  r"\1.o")
                def compile(infile, outfile):
                    # do something here
                    pass

        The ``suffix(..)`` code is much simpler but the regular expression allows more complex substitutions.
                    
    **add_inputs(...) preserves original inputs**

        ``add_inputs`` nests the the original input parameters in a list before adding additional dependencies.
        This can be seen in the following example:
            ::

                @transform([    ["1.c", "A.c", 2]
                                ["2.c", "B.c", "C.c", 3]], 
                                suffix(".c"), add_inputs([r"\1.h", "universal.h"]),  ".o")
                def compile(infile, outfile):
                    # do something here
                    pass

        This will result in the following functional calls:
            ::    
            
                compile([["1.c", "A.c", 2],        "1.h", "universal.h"], "1.o")
                compile([["3.c", "B.c", "C.c", 3], "2.h", "universal.h"], "2.o")


        The original parameters are retained unchanged as the first item in a list

                 
        
            
.. _decorators.inputs:
.. index:: 
    pair: inputs; Indicator Object (Replacing input parameters)

***************************************
*inputs(*\ `input_file_pattern`\ *)*
***************************************
    The enclosed single parameter is a pattern string or a nested structure which is 
    used to construct the input for each job. 
    
    If more than one argument is supplied to inputs, an exception will be raised.
    
    Use a tuple or list (as in the following example) to send multiple input arguments to each job.

    **Used by:**
        * The advanced form of :ref:`@transform <decorators.transform_ex>`
   
    **inputs(...) replaces original inputs**

        ``inputs(...)`` allows the original input parameters to be replaced wholescale.
        This can be seen in the following example:
            ::

                @transform([    ["1.c", "A.c", 2]
                                ["2.c", "B.c", "C.c", 3]], 
                                suffix(".c"), inputs([r"\1.py", "docs.rst"]),  ".pyc")
                def compile(infile, outfile):
                    # do something here
                    pass

        This will result in the following functional calls:
            ::    
            
                compile(["1.py", "docs.rst"], "1.pyc")
                compile(["2.py", "docs.rst"], "2.pyc")

        In this example, the corresponding python files have been sneakily substituted 
        without trace in the place of the C source files.
            
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
    single: @files_re; combine (Deprecated Syntax)
    single: combine; @follows (Deprecated Syntax)
    single: Indicator Object (Disambiguating parameters); combine

******************************************************************************************
*combine(*\ `arguments`\ *)*
******************************************************************************************
    .. note::
        
        This is deprecated syntax.    
    
        Please do not use!
    
        `@merge <decorators.merge>` and :ref:`@collate <decorators.collate>` are more powerful
        and have straightforward syntax.

    Indicates that the *inputs* of :ref:`@files_re <decorators.files_re>` will be collated
    or summarised into *outputs* by category. See the :ref:`Manual <manual.files_re.combine>`  or
    :ref:` @collate <manual.collate>` for examples.
    
    
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
                

        


