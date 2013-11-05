.. include:: ../../global.inc
.. _manual.transform_code:

########################################################################################
Code for Chapter 6: Applying the same recipe to create many different files
########################################################################################
    * :ref:`Manual overview <manual>` 
    * :ref:`@transform syntax in detail <decorators.transform>`
    * :ref:`Back <manual.transform>` 


    | Our example starts off with data file for different zoo animals.
    | We are only interested in mammals, and we would like the files of each species to 
    | end up in its own directory after processing.                                     
              
    
************************************
Code
************************************
    ::

        # 
        #   Start with species files
        #
        open("mammals.tiger.wild.animals"     , "w")
        open("mammals.lion.wild.animals"      , "w")
        open("mammals.lion.handreared.animals", "w")
        open("mammals.dog.tame.animals"       , "w")
        open("mammals.dog.wild.animals"       , "w")
        open("reptiles.crocodile.wild.animals", "w")
        
        # 
        #   create destinations for each species
        #
        import os
        for s in ("tiger", "lion", "dog"):
            if not os.path.exists(s):
                os.mkdir(s)                 
    
    
        #
        #   Now summarise files in directories organised by species
        #        
        from ruffus import *
        @transform('*.animals', 
                    regex(r'mammals\.(.+)\.(.+)\.animals'), # save species and wild/tame
                    r'\1/\1.\2.in_my_zoo',                  # same species go together
                    r'\1')                                  # extra species name
        def capture_mammals(infile, outfile, species):
            open(outfile, "w").write(open(infile).read() + "\ncaptured %s\n" % species)
        
        pipeline_run([capture_mammals])

            

************************************
Resulting Output
************************************
    ::
        
        >>> pipeline_run([capture_mammals])
            Job = [mammals.dog.tame.animals        -> dog/dog.tame.in_my_zoo, dog] completed
            Job = [mammals.dog.wild.animals        -> dog/dog.wild.in_my_zoo, dog] completed
            Job = [mammals.lion.handreared.animals -> lion/lion.handreared.in_my_zoo, lion] completed
            Job = [mammals.lion.wild.animals       -> lion/lion.wild.in_my_zoo, lion] completed
            Job = [mammals.tiger.wild.animals      -> tiger/tiger.wild.in_my_zoo, tiger] completed
        Completed Task = capture_mammals

