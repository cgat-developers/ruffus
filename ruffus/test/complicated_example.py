#!/usr/bin/env python
from __future__ import print_function
import glob
from collections import defaultdict
import sys
import operator
import re
from optparse import OptionParser
import random
from time import sleep
from ruffus import *
"""

    complicated_example.py

"""

import os
import sys
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.append(os.path.abspath(os.path.join(exe_path, "..", "..")))

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

parser = OptionParser(version="%prog 1.0")
parser.add_option("-t", "--target_tasks", dest="target_tasks",
                  action="append",
                  default=["summarise_all"],
                  metavar="JOBNAME",
                  type="string",
                  help="Target task(s) of pipeline.")
parser.add_option("-f", "--forced_tasks", dest="forced_tasks",
                  action="append",
                  default=list(),
                  metavar="JOBNAME",
                  type="string",
                  help="Pipeline task(s) which will be included even if they are up to date.")
parser.add_option("-j", "--jobs", dest="jobs",
                  default=5,
                  metavar="jobs",
                  type="int",
                  help="Specifies the number of jobs (commands) to run simultaneously.")

parser.add_option("-d", "--data_dir", dest="data_dir",
                  default="%s/data_for_complicated_example" % exe_path,
                  metavar="PATH",
                  type="string",
                  help="Directory with starting data [*.fa].")
parser.add_option("-w", "--working_dir", dest="working_dir",
                  default="/working_dir",
                  metavar="PATH",
                  type="string",
                  help="Working directory.")


parser.add_option("-v", "--verbose", dest="verbose",
                  action="count", default=0,
                  help="Print more verbose messages for each additional verbose level.")
parser.add_option("-D", "--dependency", dest="dependency_file",
                  metavar="FILE",
                  type="string",
                  help="Print a dependency graph of the pipeline that would be executed "
                        "to FILE, but do not execute it.")
parser.add_option("-F", "--dependency_graph_format", dest="dependency_graph_format",
                  metavar="FORMAT",
                  type="string",
                  default='svg',
                  help="format of dependency graph file. Can be 'ps' (PostScript), " +
                  "'svg' 'svgz' (Structured Vector Graphics), " +
                  "'png' 'gif' (bitmap  graphics) etc ")
parser.add_option("-n", "--just_print", dest="just_print",
                  action="store_true", default=False,
                  help="Print a description of the jobs that would be executed, "
                        "but do not execute them.")


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

try:
    import StringIO as io
except:
    import io as io

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

# _________________________________________________________________________________________
#
#   Helper function:
#
#       split_gene_files
#
# _________________________________________________________________________________________
def split_gene_files(gene_file_name,
                     job_completion_flag_file_name,
                     split_output_dir):
    """
    Helper function to simulate splitting gene files into "chunks" suitable for
        parallel jobs on a computational cluster

    The number of output files is only known at runtime
        because the number of "chunks" depend on the size
        of starting the gene sets

    We simulate this using a random number from 20->50
    """

    #
    #   make output directory
    #
    if not os.path.exists(split_output_dir):
        os.makedirs(split_output_dir)

    # save number of chunks for later tasks
    number_of_output_files = int(random.uniform(20, 50))

    for index in range(number_of_output_files):
        open("%s/%d.fa" % (split_output_dir, index), "w")
    open(job_completion_flag_file_name, "w")


# _________________________________________________________________________________________
#
#   get_unknown_gene_set_names
#   get_species_names
#
#
#   functions for getting unknown gene set names and species names
#
# _________________________________________________________________________________________


def get_chunked_gene_file_names(dir_name):
    """
    Get list of gene file names
    Helper function for getting unknown gene set names, and species names
    """
    regex = re.compile(r".+/(.+).genes.fa")
    gene_set_names = []
    for file_name in glob.glob("%s/%s/*.genes.fa" % (d_dir, dir_name)):
        m = regex.search(file_name)
        gene_set_names.append(m.group(1))
    return gene_set_names


def get_unknown_gene_set_names():
    return get_chunked_gene_file_names("unknown_genes")


def get_species_names():
    return get_chunked_gene_file_names("all_genes_in_each_species")


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# get help string
f = io.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
(options, remaining_args) = parser.parse_args()


d_dir = options.data_dir
w_dir = options.working_dir


# _________________________________________________________________________________________
#
#   Step 1:
#
#       split_unknown_gene_set
#
#           data_dir/unknown_genes/XXX.genes.fa
#               ->working_dir/XXX/split_gene_sets.completed
#               ->working_dir/XXX/NNN.fa
#
# _________________________________________________________________________________________
@follows(mkdir(w_dir))
@files_re("%s/unknown_genes/*.genes.fa" % d_dir,
          r"(.*/)(.*)(\.genes.fa)",
          r"\1\2\3",                                   # unknown_gene_set file name
          r"%s/\2/split_gene_sets.completed" % w_dir,  # job_completion_flag
          r"%s/\2" % w_dir)  # split_output_dir
def split_unknown_gene_set(starting_gene_set,
                           job_completion_flag,
                           split_output_dir):
    """
    Simulate splitting gene files for unknown gene set into "chunks" suitable for
        parallel jobs on a computational cluster
    """
    split_gene_files(starting_gene_set,
                     job_completion_flag,
                     split_output_dir)


# _________________________________________________________________________________________
#
#   Step 2:
#
#       split_per_species_gene_sets

#           data_dir/all_genes_in_each_species/YYY.genes.fa
#               ->working_dir/species_YYY/split_gene_sets.completed
#               ->working_dir/species_YYY/MMM.fa
#
# _________________________________________________________________________________________
@follows(mkdir(w_dir))
@files_re("%s/all_genes_in_each_species/*.genes.fa" % d_dir,
          r"(.*/)(.*)(\.genes.fa)",
          r"\1\2\3",                                           # all_genes_in_species
          r"%s/species_\2/split_gene_sets.completed" % w_dir,  # job_completion_flag
          r"%s/species_\2" % w_dir)  # split_output_dir
def split_per_species_gene_sets(all_genes_in_species,
                                job_completion_flag,
                                split_output_dir):
    """
    Simulate splitting gene files for each species into "chunks" suitable for
        parallel jobs on a computational cluster
    """
    split_gene_files(all_genes_in_species,
                     job_completion_flag,
                     split_output_dir)


# _________________________________________________________________________________________
#
#   Step 3:
#
#       all_vs_all_comparisons
#                 working_dir/species_YYY/MMM.fa
#                 working_dir/XXX/NNN.fa
#                                 -> compare/x/y.n.m.comparison_res
#                                 -> compare/x/y.n.m.complete
#
# _________________________________________________________________________________________
#
#           function for generating custom parameters
#
def generate_all_vs_all_params():
    """
    Custom function to generate
    all vs. all file names for the various "chunks"
    """

    chunk_index_regex = re.compile(r".+/(.+).fa")

    def parse_index_from_chunk_filename(chunk_filename):
        match = chunk_index_regex.search(chunk_filename)
        return int(match.group(1))

    species_names = get_species_names()
    gene_set_names = get_unknown_gene_set_names()
    for x in gene_set_names:
        for y in species_names:
            y = "species_" + y

            m_files = glob.glob("%s/%s/*.fa" % (w_dir, x))
            n_files = glob.glob("%s/%s/*.fa" % (w_dir, y))

            #
            #    for each species chunk vs for each unknown chunk
            #
            for m_file in m_files:
                for n_file in n_files:
                    input_files = [m_file, n_file]
                    output_dir = "%s/compare/%s" % (w_dir, x)

                    m = parse_index_from_chunk_filename(m_file)
                    n = parse_index_from_chunk_filename(n_file)

                    job_completion_flag = output_dir + \
                        "/%s.%d.%d.complete" % (y, m, n)
                    result_file = output_dir + \
                        "/%s.%d.%d.comparison_res" % (y, m, n)
                    name = "%s -> %d vs %d\n" % (y, m, n)
                    yield input_files, job_completion_flag, output_dir, result_file, name


@follows(split_unknown_gene_set, split_per_species_gene_sets)
@files(generate_all_vs_all_params)
def all_vs_all_comparisons(file_chunks,
                           job_completion_flag,
                           output_dir,
                           result_file,
                           name):
    """
    Simulate comparison of gene chunks against each  other
    Normally runs in parallel on a computational cluster
    """

    #
    #   make output directory
    #
    try:
        os.makedirs(output_dir)
    except OSError:
        pass

    open(job_completion_flag, "w")
    open(result_file, "w").write(name)


# _________________________________________________________________________________________
#
#   Step 4:
#
#       Recombine: alignment results to make gene families
#            compare/x/*.comparison_res
#               -> multiple_alignment/x/x.gene_families
#
# _________________________________________________________________________________________

#
#   generate_params_for_making_gene_families
#
#           function for generating custom parameters
#
def generate_params_for_making_gene_families():
    """
    Custom function to combining comparison files into gene families
    """
    gene_set_names = get_unknown_gene_set_names()
    for x in gene_set_names:
        results_files = glob.glob(
            "%s/compare/%s/*.comparison_res" % (w_dir, x))
        output_dir = "%s/multiple_alignment/%s" % (w_dir, x)
        family_file = "%s/gene.families" % output_dir
        yield results_files, family_file, output_dir


@follows(all_vs_all_comparisons)
@files(generate_params_for_making_gene_families)
def combine_into_gene_familes(results_files, family_file_name, output_dir):
    """
    Simulate making gene families by concatenating comparison results :-)
    """
    #
    #   make output directory
    #
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    family_file = open(family_file_name, "w")
    for f in results_files:
        family_file.write(open(f).read())

# _________________________________________________________________________________________
#
#   Step 5:
#
#       split_gene_family_for_evolutionary_analysis
#           multiple_alignment/x/x.gene_families
#               -> multiple_alignment/x/NNN.aln
#               -> multiple_alignment/x/split.completed
#
# _________________________________________________________________________________________


@follows(combine_into_gene_familes)
@files_re("%s/multiple_alignment/*/gene.families" % w_dir,
          r"(.+)/(gene.families)",
          r"\1/\2",
          r"\1/split.completed",
          r"\1")
def split_gene_family_for_evolutionary_analysis(family_file,
                                                job_completion_flag_file, split_output_dir):
    """
    Simulate splitting family of genes into "chunks" suitable for
        parallel jobs on a computational cluster
    """

    # save number of chunks for later tasks
    number_of_output_files = int(random.uniform(20, 50))

    for index in range(number_of_output_files):
        open("%s/%d.aln" % (split_output_dir, index),
             "w").write("chunk %d" % index)
    open(job_completion_flag_file, "w")


# _________________________________________________________________________________________
#
#   Step 6:
#
#       evolution_analysis
#           multiple_alignment/x/NNN.aln
#               -> multiple_alignment/x/NNN.evo_res
#
# _________________________________________________________________________________________
@follows(split_gene_family_for_evolutionary_analysis)
@files_re("%s/multiple_alignment/*/*.aln" % w_dir,
          r"(.+).aln",
          r"\1.evo_res")
def evolution_analysis(family_file, result_file_name):
    """
    Simulate evolutionary analysis
    """

    result_file = open(result_file_name, "w")
    result_file.write(family_file + "\n")


# _________________________________________________________________________________________
#
#   Step 7:
#
#       combine_evolution_analysis
#           multiple_alignment/x/NNN.evo_res
#               -> evolutionary_analysis/x.results
#
# _________________________________________________________________________________________

#
#   generate_params_for_combining_evolutionary_analyses
#
#           function for generating custom parameters
#
def generate_params_for_combining_evolutionary_analyses():
    """
    Custom function to combining evolutionary analyses per unknown gene set
    """
    gene_set_names = get_unknown_gene_set_names()
    for x in gene_set_names:
        results_files = glob.glob(
            "%s/multiple_alignment/%s/*.evo_res" % (w_dir, x))
        combined_file = "%s/evolutionary_analysis/%s.results" % (w_dir, x)
        yield results_files, combined_file


@follows(evolution_analysis, mkdir("%s/evolutionary_analysis" % w_dir))
@files(generate_params_for_combining_evolutionary_analyses)
def combine_evolution_analysis(results_files, combined_file_name):
    """
    Simular combining evolutionary analyses
    """
    combined_file = open(combined_file_name, "w")
    for f in results_files:
        combined_file.write(open(f).read())


# _________________________________________________________________________________________
#
#   Step 8:
#
#       summarise_evolution_analysis
#           evolutionary_analysis/x.results
#                -> evolutionary_analysis/x.summary
#
# _________________________________________________________________________________________
@follows(combine_evolution_analysis)
@files_re("%s/evolutionary_analysis/*.results" % w_dir,
          r"(.+).results",
          r"\1.summary")
def summarise_evolution_analysis(results_file, summary_file_name):
    """
    Simulate summary of evolutionary analysis
    """
    summary_file = open(summary_file_name, "w")
    summary_file.write("summary of " + open(results_file).read())


# _________________________________________________________________________________________
#
#   Step 9:
#
#       summarise_all
#       evolutionary_analysis/x.summary
#           -> all.total_summary
#
# _________________________________________________________________________________________
summary_file_names = ["%s/evolutionary_analysis/%s.summary" % (w_dir, n)
                      for n in get_unknown_gene_set_names()]
total_summary_file_name = "%s/all.total_summary" % w_dir


@follows(summarise_evolution_analysis)
@files(summary_file_names, total_summary_file_name)
def summarise_all(summary_files, total_summary_file_name):
    """
    Simulate summarize all
    """
    total_summary_file = open(total_summary_file_name, "w")
    total_summary_file.write("Over all Summary:\n")
    for f in summary_files:
        total_summary_file.write(open(f).read())


# 888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#   print pipeline or run pipeline
#
#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
    try:
        if options.just_print:
            pipeline_printout(sys.stdout, options.target_tasks,
                              options.forced_tasks, verbose=1, pipeline="main")

        elif options.dependency_file:
            graph_printout(open(options.dependency_file, "w"),
                           options.dependency_graph_format,
                           options.target_tasks,
                           options.forced_tasks)
        else:
            pipeline_run(options.target_tasks, options.forced_tasks,
                         multiprocess=options.jobs, pipeline="main")
    except Exception as e:
        print(e.args)
