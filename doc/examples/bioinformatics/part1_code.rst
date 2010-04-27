.. include:: ../../global.inc
.. _examples_bioinformatics_part1_code:


###################################################################
Ruffus code
###################################################################

::
    
    import os, sys
    
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..","..")))
    
    from ruffus import *
    
    
    original_fasta = "original.fa"
    database_file  = "human.protein.faa"
    
    @split(original_fasta, "*.segment")
    def splitFasta (seqFile, segments):
        """Split sequence file into 
           as many fragments as appropriate
           depending on the size of original_fasta"""
        current_file_index = 0
        for line in open(original_fasta):
            # 
            # start a new file for each accession line
            # 
            if line[0] == '>':
                current_file_index += 1
                current_file = open("%d.segment" % current_file_index, "w")
            current_file.write(line)
    
    
    
    @transform(splitFasta, suffix(".segment"), ".blastResult")
    def runBlast(seqFile,  blastResultFile):
        """Run blast"""
        os.system("blastall -p blastp -d %s -i %s > %s" %
                    (database_file, seqFile, blastResultFile))
    
    
    @merge(runBlast, "final.blast_results")
    def combineBlastResults (blastResultFiles, combinedBlastResultFile):
        """Combine blast results"""
        output_file = open(combinedBlastResultFile,  "w")
        for i in blastResultFiles:
            output_file.write(open(i).read())
    
    
    pipeline_run([combineBlastResults], verbose = 2, multiprocess = 4)
    

    #
    #   Simulate interuption of the pipeline by 
    #        deleting the output of one of the BLAST jobs
    #
    os.unlink("4.blastResult")

    pipeline_printout(sys.stdout, [combineBlastResults], verbose = 4) 
    

    #
    #   Re-running the pipeline
    #
    pipeline_run([combineBlastResults], verbose = 2, multiprocess = 4)

