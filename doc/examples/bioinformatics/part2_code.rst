.. include:: ../../global.inc
.. _examples_bioinformatics_part2_code:


###################################################################
Ruffus code
###################################################################

::
    
    #!/usr/bin/env python
    """
    
        run_parallel_blast.py
        [--log_file PATH]
        [--quiet]
    
    """
    
    ################################################################################
    #
    #   run_parallel_blast
    #
    #
    #   Copyright (c) 4/21/2010 Leo Goodstadt
    #   
    #   Permission is hereby granted, free of charge, to any person obtaining a copy
    #   of this software and associated documentation files (the "Software"), to deal
    #   in the Software without restriction, including without limitation the rights
    #   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    #   copies of the Software, and to permit persons to whom the Software is
    #   furnished to do so, subject to the following conditions:
    #   
    #   The above copyright notice and this permission notice shall be included in
    #   all copies or substantial portions of the Software.
    #   
    #   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    #   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    #   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    #   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    #   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    #   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    #   THE SOFTWARE.
    #################################################################################
    import os, sys
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    #   options        
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    from optparse import OptionParser
    import sys, os
    
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    
    
    parser = OptionParser(version="%prog 1.0", usage = "\n\n    %prog --input_file QUERY_FASTA --database_file FASTA_DATABASE [more_options]")
    parser.add_option("-i", "--input_file", dest="input_file",
                      metavar="FILE", 
                      type="string",
                      help="Name and path of query sequence file in FASTA format. ")
    parser.add_option("-d", "--database_file", dest="database_file",
                      metavar="FILE", 
                      type="string",
                      help="Name and path of FASTA database to search. ")
    parser.add_option("--result_file", dest="result_file",
                      metavar="FILE", 
                      type="string",
                      default="final.blast_results",
                      help="Name and path of where the files should end up. ")
    parser.add_option("-t", "--temp_directory", dest="temp_directory",
                      metavar="PATH", 
                      type="string",
                      default="tmp",
                      help="Name and path of temporary directory where calculations "
                                "should take place. ")
    
    #
    #   general options: verbosity / logging
    # 
    parser.add_option("-v", "--verbose", dest = "verbose",
                      action="count", default=0,
                      help="Print more detailed messages for each additional verbose level."
                           " E.g. run_parallel_blast --verbose --verbose --verbose ... (or -vvv)")
    
    #
    #   pipeline
    # 
    parser.add_option("-j", "--jobs", dest="jobs",
                      default=1,
                      metavar="jobs", 
                      type="int",
                      help="Specifies the number of jobs (operations) to run in parallel.")
    parser.add_option("--flowchart", dest="flowchart",
                      metavar="FILE", 
                      type="string",
                      help="Print flowchart of the pipeline to FILE. Flowchart format "
                           "depends on extension. Alternatives include ('.dot', '.jpg', "
                           "'*.svg', '*.png' etc). Formats other than '.dot' require "
                           "the dot program to be installed (http://www.graphviz.org/).")
    parser.add_option("-n", "--just_print", dest="just_print",
                        action="store_true", default=False,
                        help="Only print a trace (description) of the pipeline. "
                             " The level of detail is set by --verbose.")
    
    (options, remaining_args) = parser.parse_args()
    
    
    if not options.flowchart:
        if not options.database_file:
            parser.error("\n\n\tMissing parameter --database_file FILE\n\n")
        if not options.input_file:
            parser.error("\n\n\tMissing parameter --input_file FILE\n\n")
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    #   imports        
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    from ruffus import * 
    import subprocess
    
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    #   Functions        
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    def run_cmd(cmd_str):
        """
        Throw exception if run command fails
        """
        process = subprocess.Popen(cmd_str, stdout = subprocess.PIPE, 
                                    stderr = subprocess.PIPE, shell = True)
        stdout_str, stderr_str = process.communicate()
        if process.returncode != 0:
            raise Exception("Failed to run '%s'\n%s%sNon-zero exit status %s" %
                                (cmd_str, stdout_str, stderr_str, process.returncode))
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    #   Logger
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    import logging
    logger = logging.getLogger("run_parallel_blast")
    # 
    # We are interesting in all messages
    # 
    if options.verbose:
        logger.setLevel(logging.DEBUG)
        stderrhandler = logging.StreamHandler(sys.stderr)
        stderrhandler.setFormatter(logging.Formatter("    %(message)s"))
        stderrhandler.setLevel(logging.DEBUG)
        logger.addHandler(stderrhandler)
    
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    #   Pipeline tasks
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    original_fasta = options.input_file
    database_file  = options.database_file
    temp_directory = options.temp_directory
    result_file    = options.result_file
    
    @follows(mkdir(temp_directory))
    
    @split(original_fasta, os.path.join(temp_directory, "*.segment"))
    def splitFasta (seqFile, segments):
        """Split sequence file into 
           as many fragments as appropriate
           depending on the size of original_fasta"""
        # 
        #   Clean up any segment files from previous runs before creating new one
        #
        for i in segments:
            os.unlink(i)
        #
        current_file_index = 0
        for line in open(original_fasta):
            # 
            # start a new file for each accession line
            # 
            if line[0] == '>':
                current_file_index += 1
                file_name = "%d.segment" % current_file_index
                file_path = os.path.join(temp_directory, file_name)
                current_file = open(file_path, "w")
            current_file.write(line)
    
    
    @transform(splitFasta, suffix(".segment"), [".blastResult", ".blastSuccess"])
    def runBlast(seqFile,  output_files):
        #
        blastResultFile, flag_file = output_files
        #
        run_cmd("blastall -p blastp -d human.protein.faa -i %s > %s" % (seqFile, blastResultFile))
        #
        #   "touch" flag file to indicate success
        #
        open(flag_file, "w")            
    
    
    @merge(runBlast, result_file)
    def combineBlastResults (blastResult_and_flag_Files, combinedBlastResultFile):
        """Combine blast results"""
        #
        output_file = open(combinedBlastResultFile,  "w")
        for blastResult_file, flag_file in blastResult_and_flag_Files:
            output_file.write(open(blastResult_file).read())
    
    
    
    
    
    
    
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    #   Print list of tasks
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    if options.just_print:
        pipeline_printout(sys.stdout, [combineBlastResults], verbose=options.verbose)
    
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    #   Print flowchart
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    elif options.flowchart:
        # use file extension for output format
        output_format = os.path.splitext(options.flowchart)[1][1:]
        pipeline_printout_graph (open(options.flowchart, "w"),
                                 output_format,
                                 [combineBlastResults],
                                 no_key_legend = True)
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    
    #   Run Pipeline
    
    #88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    else:
        pipeline_run([combineBlastResults],  multiprocess = options.jobs,
                            logger = logger, verbose=options.verbose)
    

