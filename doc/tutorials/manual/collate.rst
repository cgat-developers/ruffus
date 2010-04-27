.. include:: ../../global.inc
.. include:: chapter_numbers.inc

.. _manual.collate:

######################################################################################################
|manual.collate.chapter_num|: **@collate**\ : `group together disparate input into sets of results`
######################################################################################################

    .. hlist::
    
        * :ref:`Manual overview <manual>` 
        * :ref:`@collate syntax in detail <decorators.collate>`
    
    It is often very useful to group together disparate *inputs* into several categories, each of which
    lead to a separate *output*. In the example shown below, we produce separate summaries of results 
    depending on which species the file belongs to.
    
    **Ruffus** uses the term ``collate`` in a rough analogy to the way printers group together
    copies of documents appropriately.
        
    .. index:: 
        pair: @collate; Manual
        
    



====================================================
Collating many *inputs* each into a single *output*
====================================================

    Our example starts with some files which presumably have been created by some
    earlier stages of our pipeline. We simulate this here with this code:
    
        ::
        
            files_names = [     "mammals.tiger.wild.animals"
                                "mammals.lion.wild.animals"
                                "mammals.lion.handreared.animals"
                                "mammals.dog.tame.animals"
                                "mammals.dog.wild.animals"
                                "mammals.dog.feral.animals"
                                "reptiles.crocodile.wild.animals" ]
            for f in files_names:
                open(f, "w").write(f)

    However, we are only interested in mammals, and we would like the files of each species to
    end up in its own directory, i.e. ``tiger``, ``lion`` and ``dog``:
    
        ::
        
            import os
            os.mkdir("tiger")
            os.mkdir("lion")
            os.mkdir("dog")

    Now we would like to place each file in a different destination, depending on its
    species. The following regular expression marks out the species name ``r'mammals.([^.]+)'``.
    For ``mammals.tiger.wild.animals``, the first matching group (``\1``) == ``"tiger"``
    
    Then, the following::     
    
        from ruffus import *

        @collate('*.animals',                     # inputs = all *.animal files
                    regex(r'mammals.([^.]+)'),    # regular expression
                    r'\1/animals.in_my_zoo',      # single output file per species
                    r'\1' )                       # species name
        def capture_mammals(infiles, outfile, species):
            # summarise all animals of this species
            print "Collating %s" % species
            
            o = open(outfile, "w")
            for i in infiles:
                o.write(open(infile).read() + "\ncaptured\n")
        
        pipeline_run([capture_mammals])
        
    .. ???

    puts each captured mammal in its own directory::

        Task = capture_mammals
            Job = [(mammals.lion.handreared.animals, mammals.lion.wild.animals) -> lion/animals.in_my_zoo] completed
            Job = [(mammals.tiger.wild.animals, ) -> tiger/animals.in_my_zoo] completed
            Job = [(mammals.dog.tame.animals, mammals.dog.wild.animals, mammals.dog.feral.animals) -> dog/animals.in_my_zoo] completed

        
    .. ???

    The crocodile has been discarded because it isn't a mammal and the file name
    doesn't match the ``mammal`` part of the regular expression.


