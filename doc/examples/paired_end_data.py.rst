.. _faq.paired_files.code:

############################################################################################################################################################################################################
Example code for :ref:`FAQ Good practices: "What is the best way of handling data in file pairs (or triplets etc.)?" <faq.paired_files>`
############################################################################################################################################################################################################

    .. seealso::

        * :ref:`@collate <new_manual.collate>`


    .. code-block:: python
        :emphasize-lines: 10-21,29-31,40-43,70-74

        #!/usr/bin/env python
        import sys, os

        from ruffus import *
        import ruffus.cmdline as cmdline
        from subprocess import check_call

        parser = cmdline.get_argparse(description="Parimala's pipeline?")

        #                                                                                 .
        #   Very flexible handling of input files                                         .
        #                                                                                 .
        #      input files can be specified flexibly as:                                  .
        #                 --input a.fastq b.fastq                                         .
        #                 --input a.fastq --input b.fastq                                 .
        #                 --input *.fastq --input other/*.fastq                           .
        #                 --input "*.fastq"                                               .
        #                                                                                 .
        #       The last form is expanded in the script and avoids limitations on command .
        #           line lengths                                                          .
        #                                                                                 .
        parser.add_argument('-i', '--input', nargs='+', metavar="FILE", action="append", help = "Fastq files")

        options = parser.parse_args()

        #  standard python logger which can be synchronised across concurrent Ruffus tasks
        logger, logger_mutex = cmdline.setup_logging ("PARIMALA", options.log_file, options.verbose)

        #                                                                                .
        #   Useful code to turn input files into a flat list                             .
        #                                                                                .
        from glob import glob
        original_data_files = [fn for grouped in options.input for glob_spec in grouped for fn in glob(glob_spec)] if options.input else []
        if not original_data_files:
            original_data_files = [["C1W1_R1.fastq.gz", "C1W1_R2.fastq.gz"]]
            #raise Exception ("No matching files specified with --input.")

        #   <<<----  pipelined functions go here

        #_________________________________________________________________________________
        #                                                                                .
        #   Group together file pairs                                                    .
        #_________________________________________________________________________________
        @collate(original_data_files,
                    # match file name up to the "R1.fastq.gz"
                    formatter("([^/]+)R[12].fastq.gz$"),
                    # Create output parameter supplied to next task
                    ["{path[0]}/{1[0]}paired.R1.fastq.gz",  # paired file 1
                     "{path[0]}/{1[0]}paired.R2.fastq.gz"], # paired file 2
                    # Extra parameters for our own convenience and use
                    ["{path[0]}/{1[0]}unpaired.R1.fastq.gz",  # unpaired file 1
                     "{path[0]}/{1[0]}unpaired.R2.fastq.gz"], # unpaired file 2
                    logger, logger_mutex)
        def trim_fastq(input_files, output_paired_files, discarded_unpaired_files, logger, logger_mutex):
            if len(input_files) != 2:
                raise Exception("One of read pairs %s missing" % (input_files,))
            cmd = ("java -jar ~/SPRING-SUMMER_2014/Softwares/Trimmomatic/Trimmomatic-0.32/trimmomatic-0.32.jar "
                   " PE -phred33  "
                   " {input_files[0]} {input_files[1]} "
                   " {output_paired_files[0]} {output_paired_files[1]} "
                   " {discarded_unpaired_files[0]} {discarded_unpaired_files[1]} "
                   " LEADING:30 TRAILING:30 SLIDINGWINDOW:4:15 MINLEN:50 "
                )

            check_call(cmd.format(**locals()))

            with logger_mutex:
                    logger.debug("Hooray trim_fastq worked")

        #_________________________________________________________________________________
        #                                                                                .
        #   Each file pair now makes its way down the rest of the pipeline as            .
        #       a couple                                                                 .
        #_________________________________________________________________________________
        @transform(trim_fastq,
                    # regular expression match on first of pe files
                    formatter("([^/]+)paired.R1.fastq.gz$"),
                    # Output parameter supplied to next task
                    "{path[0]}/{1[0]}.sam"

                   # Extra parameters for our own convenience and use
                    "{path[0]}/{1[0]}.pe_soap_pe",        # soap intermediate file
                    "{path[0]}/{1[0]}.pe_soap_se",        # soap intermediate file
                    logger, logger_mutex)
        def align_seq(input_files, output_file, soap_pe_output_file, soap_se_output_file, logger, logger_mutex):
            if len(input_files) != 2:
                raise Exception("One of read pairs %s missing" % (input_files,))
            cmd = ("~/SPRING-SUMMER_2014/Softwares/soap2.21release/soap "
                    " -a {input_files[0]} "
                    " -b {input_files[1]} "
                    " -D Y55_genome.fa.index* "
                    " -o {soap_pe_output_file} -2 {soap_se_output_file} -m 400 -x 600")

            check_call(cmd.format(**locals()))


            #Soap_to_sam
            cmd = " perl ~/SPRING-SUMMER_2014/Softwares/soap2sam.pl -p {soap_pe_output_file} > {output_file}"

            check_call(cmd.format(**locals()))


            with logger_mutex:
                    logger.debug("Hooray align_seq worked")


        cmdline.run (options)

