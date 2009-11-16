.. _manual_12th_chapter:

##############################################################################################################
**Chapter 12**: `Advanced usage of` **@transform**: `controlling both input and output files`
##############################################################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 
        * :ref:`@transform <decorators.transform>` syntax in detail

    
.. index:: 
    pair: @transform (Advanced Usage); Manual

.. _manual.transform_ex:

    The standard :ref:`@transform <manual.transform>` allows you to send a list of data files
    to the same pipelined function and for the resulting *outputs* parameter to be automatically
    inferred from file names in the *inputs*.
    
    There are two situations where you might desire additional flexibility:
    
        #. You need to add additional prequisites or filenames to the *inputs* of every single one
           of your jobs
           
        #. (Less often,) the actual *inputs* file names are some variant of the *outputs* of another
           task. 
           
    Either way, it is occasionally very useful to be able to generate the actual *inputs* as 
    well as *outputs* parameters by regular expression substitution. The following examples will show
    you both how and why you would want to do this.

====================================================================
Adding additional *input* prerequisites per job
====================================================================

    Suppose we had two pipelined tasks which create, respectively, one file called ``important.file``,
    and three little ``.chunks`` files (``0.chunks``, ``1.chunks``, ``2.chunks``):

        ::

            from ruffus import *

            @files(None, 'important.file')
            def make_important_file(no_input_filename, output_file_name):
                open(output_file_name, "w")
                
            @split(None, '*.chunks')
            def split_up_problem(input_filename, output_file_names):
                for i in range(3):
                    open("%d.chunks" % i, "w")
                    

    The problem is that our ``analysis()`` function requires both ``important.file`` and one of the ``.chunks`` files
    at a time. There is no way that we can use vanilla **@transform** to do this. Do we have
    to fall back on :ref:`generating parameters on the fly <manual.on_the_fly>`?
    

    Instead, let us just add the extra ``important.file`` to the *inputs* of each job like so:
    
        ::  
          
            @follows(make_important_file)
            @transform(split_up_problem,                # starting set of *inputs*
                        regex(r"(.*).chunks"),          # regular expression
                        inputs([r"\g<0>",               # xx.chunks
                                "important.file"]),     # important.file
                         r"\1.results"                  # xx.results
                          )
            def analyse(input_filenames, output_file_name):
                "Do analysis here"
    
    This results in the following equivalent calls to the pipelined function:
    
        ::
        
            analyse(["0.chunks", "important.file"], "0.results")
            analyse(["1.chunks", "important.file"], "1.results")
            analyse(["2.chunks", "important.file"], "2.results")
            
            
    This is exactly what ``analyse()`` needs, giving the following output:
    
        ::
        
            >>> pipeline_run([analyse])
                Job = [big.file -> *.chunks] completed
            Completed Task = split_up_problem
                Job = [[0.chunks, important.file] -> 0.results] completed
                Job = [[1.chunks, important.file] -> 1.results] completed
                Job = [[2.chunks, important.file] -> 2.results] completed
            Completed Task = analyse

    
    .. note::
    
        The backreference ``\g<0>`` usefully substitutes the entire substring matched by 
        the regular expression.
        
    .. note::
        One side effect of regular expression substitution on the *inputs* parameter is 
        that if the *inputs* parameter contains other (nested) data types, all but the 
        first string encountered will be ignored. 

        If the *inputs* parameter for one job is :
            ::

                [3, ["0.chunks", "1.funfair", 7.4]]
                
        **Ruffus** will treat this as if the *inputs* parameter was just:
            ::
            
                "0.chunks" 
                
        which was the first string encountered.





====================================================================
Generating additional **variable** *input* prerequisites per job
====================================================================

    Continuing our previous example, suppose that our pipeline contained another function
    which generated ``.red_indian`` files:
    
        ::
        
            @split(None, '*.red_indian')
            def make_red_indians(no_input_filename, output_file_names):
                for i in range(10):
                    open("%d.red_indian" % i, "w")
                    

    How could we organise the pipeline so that ``analyse()`` gets corresponding pairs
    of ``xx.chunks`` and ``xx.red_indian`` files?

    It turns out that this is just a minor variant on the above code, with a slightly
    different regular expression:
    
        ::    
            
            @follows(make_red_indians)
            @transform(split_up_problem,                # starting set of *inputs*
                        regex(r"(.*).chunks"),          # regular expression
                        inputs([r"\g<0>",               # xx.chunks
                                r"\1.red_indian"]),     # important.file
                         r"\1.results"                  # xx.results
                          )
            def analyse(input_filenames, output_file_name):
                "Do analysis here"
    
    This results in the following equivalent calls to the pipelined function:
    
        ::
        
            analyse(["0.chunks", "0.red_indian"], "0.results")
            analyse(["1.chunks", "1.red_indian"], "1.results")
            analyse(["2.chunks", "2.red_indian"], "2.results")
            
    and the following results:
    
        ::
        
            >>> pipeline_run([analyse])
                Job = [None -> *.red_indian] completed
            Completed Task = make_red_indians
                Job = [big.file -> *.chunks] completed
            Completed Task = split_up_problem
                Job = [[0.chunks, 0.red_indian] -> 0.results] completed
                Job = [[1.chunks, 1.red_indian] -> 1.results] completed
                Job = [[2.chunks, 2.red_indian] -> 2.results] completed
            Completed Task = analyse
            

    This is about as sophisticated as **@transform** ever gets!
    
