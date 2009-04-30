#!/usr/bin/env python
"""

    intermediate_example.py
    
        This script takes N pairs of input file pairs
                                (with the suffices .gene and .gwas)
                          and runs them against M sets of simulation data
                                (with the suffix .simulation)
        A summary per input file pair is then produced
                    
        
    In pseudo-code:
        
        STEP_1:
        
        for n_file in NNN_pairs_of_input_files:
            for m_file in MMM_simulation_data:

                [n_file.gene,
                 n_file.gwas,
                 m_file.simulation] -> n_file.m_file.simulation_res
                 

        STEP_2:
        
        for n_file in NNN_pairs_of_input_files:
            
            n_file.*.simulation_res -> n_file.mean
            
        

"""

import os, sys
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
from ruffus import *
from time import sleep
import random
from itertools import izip


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
parser = OptionParser(version="%prog 1.0")
parser.add_option("-t", "--target_tasks", dest="target_tasks",
                  action="append",
                  default = ["statistical_summary"],
                  metavar="JOBNAME", 
                  type="string",
                  help="Target task(s) of pipeline.")
parser.add_option("-f", "--forced_tasks", dest="forced_tasks",
                  action="append",
                  default = list(),
                  metavar="JOBNAME", 
                  type="string",
                  help="Pipeline task(s) which will be included even if they are up to date.")
parser.add_option("-j", "--jobs", dest="jobs",
                  default=5,
                  metavar="jobs", 
                  type="int",
                  help="Specifies the number of jobs (commands) to run simultaneously.")

parser.add_option("-g", "--gene_data_dir", dest="gene_data_dir",
                  default="%s/data_for_intermediate_example/genes" % exe_path,
                  metavar="PATH", 
                  type="string",
                  help="Directory with gene data [*.genes / *.gwas].")
parser.add_option("-s", "--simulation_data_dir", dest="simulation_data_dir",
                  default="%s/data_for_intermediate_example/simulation" % exe_path,
                  metavar="PATH", 
                  type="string",
                  help="Directory with simulation data [*.simulation].")
parser.add_option("-w", "--working_dir", dest="working_dir",
                  default="/working_dir",
                  metavar="PATH", 
                  type="string",
                  help="Working directory.")


parser.add_option("-v", "--verbose", dest = "verbose",
                  action="store_true", default=False,
                  help="Do not echo to shell but only print to log.")
parser.add_option("-D", "--dependency", dest="dependency_file",
                  metavar="FILE", 
                  type="string",
                  help="Print a dependency graph of the pipeline that would be executed "
                        "to FILE, but do not execute it.")
parser.add_option("-F", "--dependency_graph_format", dest="dependency_graph_format",
                  metavar="FORMAT", 
                  type="string",
                  default = 'svg',
                  help="format of dependency graph file. Can be 'ps' (PostScript), "+
                  "'svg' 'svgz' (Structured Vector Graphics), " +
                  "'png' 'gif' (bitmap  graphics) etc ")
parser.add_option("-n", "--just_print", dest="just_print",
                    action="store_true", default=False,
                    help="Print a description of the jobs that would be executed, "
                        "but do not execute them.")





#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import StringIO
import re
import operator
import sys
from collections import defaultdict
import glob
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#_________________________________________________________________________________________
#
#   get gene gwas file pairs
#
#_________________________________________________________________________________________
def get_gene_gwas_file_pairs(  ):
    """
    Helper function to get all *.gene, *.gwas from the direction specified
        in --gene_data_dir
        
    Returns 
        file pairs with both .gene and .gwas extensions, 
        corresponding roots (no extension) of each file
    """
    

    gene_files = glob.glob(os.path.join(options.gene_data_dir, "*.gene"))
    gwas_files = glob.glob(os.path.join(options.gene_data_dir, "*.gwas"))
    
    common_roots = set(map(lambda x: os.path.splitext(os.path.split(x)[1])[0], gene_files))
    common_roots &=set(map(lambda x: os.path.splitext(os.path.split(x)[1])[0], gwas_files))
    common_roots = list(common_roots)
        
    p = os.path; g_dir = options.gene_data_dir
    
    file_pairs = [[p.join(g_dir, x + ".gene"), p.join(g_dir, x + ".gwas")] for x in common_roots]
    
    return file_pairs, common_roots

#_________________________________________________________________________________________
#
#   get simulation files
#
#_________________________________________________________________________________________
def get_simulation_files(  ):
    """
    Helper function to get all *.simulation from the direction specified
        in --simulation_data_dir
        Returns 
            file with .simulation extensions, 
            corresponding roots (no extension) of each file
    """
    simulation_files = glob.glob(os.path.join(options.simulation_data_dir, "*.simulation"))
    simulation_roots =map(lambda x: os.path.splitext(os.path.split(x)[1])[0], simulation_files)
    return simulation_files, simulation_roots



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888





# get help string
f =StringIO.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
(options, remaining_args) = parser.parse_args()


working_dir = options.working_dir




#_________________________________________________________________________________________
#
#   Step 1:
#       
#        for n_file in NNN_pairs_of_input_files:
#            for m_file in MMM_simulation_data:
#
#                [n_file.gene,
#                 n_file.gwas,
#                 m_file.simulation] -> working_dir/n_file.m_file.simulation_res
#
#_________________________________________________________________________________________
def generate_simulation_params ():
    """
    Custom function to generate 
    file names for gene/gwas simulation study
    """

    simulation_files, simulation_file_roots    = get_simulation_files()
    gene_gwas_file_pairs, gene_gwas_file_roots =  get_gene_gwas_file_pairs()
    
    for sim_file, sim_file_root in izip(simulation_files, simulation_file_roots):
        for (gene, gwas), gene_file_root in izip(gene_gwas_file_pairs, gene_gwas_file_roots):
            
            result_file = "%s.%s.simulation_res" % (gene_file_root, sim_file_root)
            result_file_path = os.path.join(working_dir, "simulation_results", result_file)
            
            yield [gene, gwas, sim_file], result_file_path, gene_file_root, sim_file_root, result_file

# 
# mkdir: makes sure output directories exist before task    
#
@follows(mkdir(options.working_dir, os.path.join(working_dir, "simulation_results")))
@files(generate_simulation_params)
def gwas_simulation(input_files, result_file_path, gene_file_root, sim_file_root, result_file):
    """
    Dummy calculation of gene gwas vs simulation data
    Normally runs in parallel on a computational cluster       
    """
    (gene_file,
    gwas_file,
    simulation_data_file) = input_files

    simulation_res_file = open(result_file_path, "w")
    simulation_res_file.write("%s + %s -> %s\n" % (gene_file_root, sim_file_root, result_file))


#_________________________________________________________________________________________
#
#   Step 2:
#       
#       Statistical summary per gene/gwas file pair
# 
#        for n_file in NNN_pairs_of_input_files:
#            working_dir/simulation_results/n.*.simulation_res
#               -> working_dir/n.mean
#       
#_________________________________________________________________________________________
def generate_statistical_summary_params():
    """
    Custom function to summarising simulation results files per gene / gwas file pair
    """
    gene_gwas_file_pairs, gene_gwas_file_roots =  get_gene_gwas_file_pairs()

    for (gene, gwas), gene_file_root in izip(gene_gwas_file_pairs, gene_gwas_file_roots):
            result_glob_spec = "%s.*.simulation_res" % (gene_file_root)
            result_files     = glob.glob(os.path.join(working_dir, "simulation_results", result_glob_spec))
            summary_file     = os.path.join(working_dir, gene_file_root + ".mean")
                
            yield result_files, summary_file
                


@follows(gwas_simulation)
@files(generate_statistical_summary_params)
@posttask(lambda : sys.stdout.write("\nAll finished: hooray!!!\n"))
def statistical_summary (result_files, summary_file):
    """
    Simulate statistical summary
    """

    summary_file = open(summary_file, "w")
    for f in result_files:
        summary_file.write(open(f).read())
    sleep(1)
    





    
    
    
    
#888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888    
#
#   print pipeline or run pipeline
# 

if options.just_print:
    pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks, long_winded=True)

elif options.dependency_file:
    graph_printout (     open(options.dependency_file, "w"),
                         options.dependency_graph_format,
                         options.target_tasks, 
                         options.forced_tasks)
else:    
    pipeline_run(options.target_tasks, options.forced_tasks, multiprocess = options.jobs)
    
