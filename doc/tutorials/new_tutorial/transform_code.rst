.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.transform.code:

##############################################################################################################
|new_manual.introduction.chapter_num|: Python Code for Transforming data in a pipeline with ``@transform``
##############################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`@transform syntax in detail <decorators.transform>`
    * Back to |new_manual.transform.chapter_num|: :ref:`Transforming data in a pipeline with @transform <new_manual.transform>`

*******************************************
Your first Ruffus script
*******************************************

    .. code-block:: python

        #
        #   The starting data files would normally exist beforehand!
        #       We create some empty files for this example
        #
        starting_files = [("a.1.fastq", "a.2.fastq"),
                          ("b.1.fastq", "b.2.fastq"),
                          ("c.1.fastq", "c.2.fastq")]


        for ff_pair in starting_files:
            open(ff_pair[0], "w")
            open(ff_pair[1], "w")


        from ruffus import *

        #
        #   STAGE 1 fasta->sam
        #
        @transform(starting_files,                     # Input = starting files
                   suffix(".1.fastq"),                 #         suffix = .1.fastq
                   ".sam")                             # Output  suffix = .sam
        def map_dna_sequence(input_files,
                            output_file):
            # remember there are two input files now
            ii1 = open(input_files[0])
            ii2 = open(input_files[1])
            oo = open(output_file, "w")

        #
        #   STAGE 2 sam->bam
        #
        @transform(map_dna_sequence,                   # Input = previous stage
                    suffix(".sam"),                    #         suffix = .sam
                    ".bam")                            # Output  suffix = .bam
        def compress_sam_file(input_file,
                              output_file):
            ii = open(input_file)
            oo = open(output_file, "w")

        #
        #   STAGE 3 bam->statistics
        #
        @transform(compress_sam_file,                  # Input = previous stage
                    suffix(".bam"),                    #         suffix = .bam
                    ".statistics",                     # Output  suffix = .statistics
                    "use_linear_model")                # Extra statistics parameter
        def summarise_bam_file(input_file,
                               output_file,
                               extra_stats_parameter):
            """
            Sketch of real analysis function
            """
            ii = open(input_file)
            oo = open(output_file, "w")

        pipeline_run()


************************************
Resulting Output
************************************
    ::

            >>> pipeline_run()
                Job  = [[a.1.fastq, a.2.fastq] -> a.sam] completed
                Job  = [[b.1.fastq, b.2.fastq] -> b.sam] completed
                Job  = [[c.1.fastq, c.2.fastq] -> c.sam] completed
            Completed Task = map_dna_sequence
                Job  = [a.sam -> a.bam] completed
                Job  = [b.sam -> b.bam] completed
                Job  = [c.sam -> c.bam] completed
            Completed Task = compress_sam_file
                Job  = [a.bam -> a.statistics, use_linear_model] completed
                Job  = [b.bam -> b.statistics, use_linear_model] completed
                Job  = [c.bam -> c.statistics, use_linear_model] completed
            Completed Task = summarise_bam_file

