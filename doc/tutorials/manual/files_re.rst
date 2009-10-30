.. _manual_17th_chapter:
.. |task| replace:: **task**
.. _task: ../../glossary.html#term-task
.. |job| replace:: **job**
.. _job: ../../glossary.html#term-job
.. |decorator| replace:: **decorator**
.. _decorator: ../../glossary.html#term-decorator
.. |pipeline_run| replace:: **pipeline_run**
.. _pipeline_run: ../../pipeline_functions.html#pipeline_run

###############################################################################################
Chapter 17: Deprecated: Generating parameters using regular expressions the old fashioned way
###############################################################################################

    .. hlist::

        * :ref:`Manual overview <manual>` 

    
.. index:: 
    single: @files_re; Manual
    
.. _manual.files_re:



***************************************
**@files_re**
***************************************

=======================================
i/o files using regular expressions
=======================================

    It is often not possible to come up with a predetermined list of input
    and output files for a each job in a pipeline task. Instead, you would
    like to apply an operation to whatever files that are present of the right 
    type, however many there are.
    
    Typically, in traditional make files, you would manage this via file extensions.
    For example, compiling all ".c" source files into object files with ".obj"
    extension. Because python has such good regular expression support, it is
    easy to have more sophisticated schemes to organise your files, such as putting
    them into different directories, giving them different names.
    
=======================================
A simple example
=======================================

    ::
    
        from ruffus import *
        #
        #   convert all files ending in ".1" into files ending in ".2"
        #
        @files_re('*.1', '(.*).1', r'\1.2')
        def task_re(infile, outfile):
            open(outfile, "w").write(open(infile).read() + "\nconverted\n")
        
        pipeline_run([task_re])

        
    .. ???

    This pipeline task:

        #. takes each file which has the ``.1`` suffix,
        #. adds the line ``converted`` to its contents, and
        #. outputs a corresponding file with a ``.2`` suffix.
        
    If you ran this, you may be surprised to see that nothing happens. This is because
    there are no ``*.1`` files to begin with.
    
    but if you first created ``a.1`` and ``b.1`` ::
    
        >>> open("a.1", "w")
        <open file 'a.1', mode 'w' at 0x96643e0>
        >>> open("b.1", "w")
        <open file 'b.1', mode 'w' at 0x9664e80>
        >>> pipeline_run([task_re])
    
        
    .. ???

    You would see the creation of two new files::
    
        Task = task_re
            Job = ["a.1" -> "a.2"] completed
            Job = ["b.1" -> "b.2"] completed
    
        
.. ???

    
=======================================
**@files_re** in more detail
=======================================

    Let us look at the ``@files_re`` directive again to see what it does::
    
        @files_re(
                    '*.1',              # 'glob' * .1
                    '(.*).1',           # Regular expression match
                    r'\1.2'             # add the ".2" extension
                  )
    
        
    .. ???

    There are three parameters:
        #. The first is a "glob" pattern, such as you might type in a command prompt to
           find a list of files (``ls *`` or ``dir *.*``)
           
           (See python `glob <http://docs.python.org/library/glob.html>`_ documentation.)
        #. For each file name returned by the "glob",  we make sure it has a ``.1`` extension,
           and save the "root" of each file name.
           
           (See python `regular expression (re) <http://docs.python.org/library/re.html>`_ documentation.)
        #. ``.2`` is appended to the matching file name root to give a new output file.
        
           (See the documentation for `re.sub <http://docs.python.org/library/re.html#re.sub>`_\ .)
           

=======================================
More ambitious **@files_re** 
=======================================

    Because @files_re uses regular expressions, you organise your files for each job with
    greater power and flexibility. Let us try putting files in different subdirectories.
    
    First create some files for different animals::
        
        > touch mammals.tiger.wild.animals
        > touch mammals.lion.wild.animals
        > touch mammals.lion.handreared.animals
        > touch mammals.dog.tame.animals
        > touch mammals.dog.wild.animals
        > touch reptiles.crocodile.wild.animals
    
        
    .. ???

    We are only interested in mammals, and we would like the files of each species to
    end up in its own directory after we have processed it. 

    Let us also prepare the directories. (We could also use :ref:`@follows(mk_dir(xxx)) <follow-mkdir>`  
    to do this but let us keep this example simple.)::
        
        > mkdir -p tiger lion dog
     
        
    .. ???

    Then, the following::     
    
        from ruffus import *
        @files_re('*.animals', 
                    r'mammals\.(.+)\.(.+)\.animals',    # save species and 'wild'/'tame'
                    r'\1/\1.\2.in_my_zoo')
        def capture_mammals(infile, outfile):
            open(outfile, "w").write(open(infile).read() + "\ncaptured\n")
        
        pipeline_run([capture_mammals])
    
        
    .. ???

    Will put each captured mammal in its own directory::

        Task = capture_mammals
            Job = ["mammals.dog.tame.animals" -> "dog/dog.tame.in_my_zoo"] completed
            Job = ["mammals.dog.wild.animals" -> "dog/dog.wild.in_my_zoo"] completed
            Job = ["mammals.lion.handreared.animals" -> "lion/lion.handreared.in_my_zoo"] completed
            Job = ["mammals.lion.wild.animals" -> "lion/lion.wild.in_my_zoo"] completed
            Job = ["mammals.tiger.wild.animals" -> "tiger/tiger.wild.in_my_zoo"] completed

        
    .. ???

    Note that we have ignored the crocodile file because it doesn't match the ``mammal`` part
    of the regular expression.

=======================================
Multiple parameters with **@files_re** 
=======================================

    So far, even with the complicated example above, we are only generating one input file name,
    and one output file name per job. Sometimes this is not sufficient. By analogy with 
    ``@files``, we can use regular expressions to create any number of parameters for each
    job, so long as 

        #. The first parameter are input file(s)
        #. The second parameter are output file(s)
        
    Regular expression substitution is carried out on all strings, or on list of strings

    `None` and all other types of objects are passed through unchanged.
    
    Let us see how this works in practice. Building on the previous example::

        > touch mammals.tiger.wild.animals
        > touch mammals.lion.wild.animals mammals.lion.handreared.animals
        > touch mammals.dog.tame.animals  mammals.dog.wild.animals
        > touch reptiles.crocodile.wild.animals
        > mkdir -p tiger lion dog

        
    .. ???

     
    Then, the following::     

        from ruffus import *
        @files_re('*.animals', r'mammals\.(.+)\.(.+)\.animals',      # save species and 'wild'/'tame'
                               r'\g<0>',                             # input:  entire match unchanged
                               [r'\1/\1.\2.in_my_zoo',               # output file names
                                r'all_species/\1.\2.in_my_zoo'],
                                r'\1' )                              # species name
        def capture_mammals(infile, outfiles, species):
            for f in outfiles:
                open(f, "w").write(open(infile).read() + "\nCaptured %s\n" % species)
        
        pipeline_run([capture_mammals])
    
        
    .. ???

    Will put each captured mammal in the ``all_species`` directory as well as its own::
    
        Task = capture_mammals
            Job = ["mammals.dog.tame.animals" -> ["dog/dog.tame.in_my_zoo", "all_species/dog.tame.in_my_zoo"], "dog"] completed
            Job = ["mammals.dog.wild.animals" -> ["dog/dog.wild.in_my_zoo", "all_species/dog.wild.in_my_zoo"], "dog"] completed
            Job = ["mammals.lion.handreared.animals" -> ["lion/lion.handreared.in_my_zoo", "all_species/lion.handreared.in_my_zoo"], "lion"] completed
            Job = ["mammals.lion.wild.animals" -> ["lion/lion.wild.in_my_zoo", "all_species/lion.wild.in_my_zoo"], "lion"] completed
            Job = ["mammals.tiger.wild.animals" -> ["tiger/tiger.wild.in_my_zoo", "all_species/tiger.wild.in_my_zoo"], "tiger"] completed

        
    .. ???

    Note the third ``species`` parameter for ``capture_mammals(...)``.

