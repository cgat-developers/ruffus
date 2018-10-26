#! /usr/bin/env python

from __future__ import print_function
import unittest
import glob
from ruffus import pipeline_run, Pipeline, follows, posttask, collate, mkdir, regex, files
import os
import sys
if sys.hexversion < 0x03000000:
    from future_builtins import zip
"""

    test_N_x_M_and_collate.py


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


        n = CNT_GENE_GWAS_FILES
        m = CNT_SIMULATION_FILES



"""

CNT_GENE_GWAS_FILES = 2
CNT_SIMULATION_FILES = 3


# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0]))
gene_data_dir = "%s/temp_gene_data_for_intermediate_example" % tempdir
simulation_data_dir = "%s/temp_simulation_data_for_intermediate_example" % tempdir
working_dir = "%s/working_dir_for_intermediate_example" % tempdir


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
#   get gene gwas file pairs
#
# _________________________________________________________________________________________
def get_gene_gwas_file_pairs():
    """
    Helper function to get all *.gene, *.gwas from the direction specified
        in --gene_data_dir

    Returns
        file pairs with both .gene and .gwas extensions,
        corresponding roots (no extension) of each file
    """

    gene_files = glob.glob(os.path.join(gene_data_dir, "*.gene"))
    gwas_files = glob.glob(os.path.join(gene_data_dir, "*.gwas"))

    common_roots = set([os.path.splitext(os.path.split(x)[1])[0]
                        for x in gene_files])
    common_roots &= set([os.path.splitext(os.path.split(x)[1])[0]
                         for x in gwas_files])
    common_roots = list(common_roots)

    p = os.path
    g_dir = gene_data_dir

    file_pairs = [[p.join(g_dir, x + ".gene"), p.join(g_dir, x + ".gwas")]
                  for x in common_roots]

    return file_pairs, common_roots

# _________________________________________________________________________________________
#
#   get simulation files
#
# _________________________________________________________________________________________


def get_simulation_files():
    """
    Helper function to get all *.simulation from the direction specified
        in --simulation_data_dir
        Returns
            file with .simulation extensions,
            corresponding roots (no extension) of each file
    """
    simulation_files = glob.glob(os.path.join(
        simulation_data_dir, "*.simulation"))
    simulation_roots = [os.path.splitext(os.path.split(x)[1])[
        0] for x in simulation_files]
    return simulation_files, simulation_roots


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


# _________________________________________________________________________________________
#
#   setup_simulation_data
#
# _________________________________________________________________________________________

#
# mkdir: makes sure output directories exist before task
#
@follows(mkdir(gene_data_dir, simulation_data_dir))
def setup_simulation_data():
    """
    create simulation files
    """
    for i in range(CNT_GENE_GWAS_FILES):
        open(os.path.join(gene_data_dir, "%03d.gene" % i), "w").close()
        open(os.path.join(gene_data_dir, "%03d.gwas" % i), "w").close()

    # gene files without corresponding gwas and vice versa
    open(os.path.join(gene_data_dir, "orphan1.gene"), "w").close()
    open(os.path.join(gene_data_dir, "orphan2.gwas"), "w").close()
    open(os.path.join(gene_data_dir, "orphan3.gwas"), "w").close()

    for i in range(CNT_SIMULATION_FILES):
        open(os.path.join(simulation_data_dir, "%03d.simulation" % i), "w").close()


# _________________________________________________________________________________________
#
#   cleanup_simulation_data
#
# _________________________________________________________________________________________
def try_rmdir(d):
    if os.path.exists(d):
        try:
            os.rmdir(d)
        except OSError:
            sys.stderr.write(
                "Warning:\t%s is not empty and will not be removed.\n" % d)


def cleanup_simulation_data():
    """
    cleanup files
    """

    #
    #   cleanup gene and gwas files
    #
    for f in glob.glob(os.path.join(gene_data_dir, "*.gene")):
        os.unlink(f)
    for f in glob.glob(os.path.join(gene_data_dir, "*.gwas")):
        os.unlink(f)
    try_rmdir(gene_data_dir)

    #
    #   cleanup simulation
    #
    for f in glob.glob(os.path.join(simulation_data_dir, "*.simulation")):
        os.unlink(f)
    try_rmdir(simulation_data_dir)

    #
    #   cleanup working_dir
    #
    for f in glob.glob(os.path.join(working_dir, "simulation_results", "*.simulation_res")):
        os.unlink(f)
    try_rmdir(os.path.join(working_dir, "simulation_results"))

    for f in glob.glob(os.path.join(working_dir, "*.mean")):
        os.unlink(f)
    try_rmdir(working_dir)

    try_rmdir(tempdir)


# _________________________________________________________________________________________
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
# _________________________________________________________________________________________
def generate_simulation_params():
    """
    Custom function to generate
    file names for gene/gwas simulation study
    """

    simulation_files, simulation_file_roots = get_simulation_files()
    gene_gwas_file_pairs, gene_gwas_file_roots = get_gene_gwas_file_pairs()

    for sim_file, sim_file_root in zip(simulation_files, simulation_file_roots):
        for (gene, gwas), gene_file_root in zip(gene_gwas_file_pairs, gene_gwas_file_roots):

            result_file = "%s.%s.simulation_res" % (
                gene_file_root, sim_file_root)
            result_file_path = os.path.join(
                working_dir, "simulation_results", result_file)

            yield [gene, gwas, sim_file], result_file_path, gene_file_root, sim_file_root, result_file

#
# mkdir: makes sure output directories exist before task
#


@follows(setup_simulation_data)
@follows(mkdir(working_dir, os.path.join(working_dir, "simulation_results")))
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
    simulation_res_file.write("%s + %s -> %s\n" %
                              (gene_file_root, sim_file_root, result_file))
    simulation_res_file.close()


# _________________________________________________________________________________________
#
#   Step 2:
#
#       Statistical summary per gene/gwas file pair
#
#        for n_file in NNN_pairs_of_input_files:
#            working_dir/simulation_results/n.*.simulation_res
#               -> working_dir/n.mean
#
# _________________________________________________________________________________________


@collate(gwas_simulation, regex(r"simulation_results/(\d+).\d+.simulation_res"), r"\1.mean")
@posttask(lambda: sys.stdout.write("\nOK\n"))
def statistical_summary(result_files, summary_file):
    """
    Simulate statistical summary
    """

    summary_file = open(summary_file, "w")
    for f in result_files:
        with open(f) as ii:
            summary_file.write(ii.read())
    summary_file.close()


try:
    from StringIO import StringIO
except:
    from io import StringIO


class Test_ruffus(unittest.TestCase):

    def tearDown(self):
        try:
            cleanup_simulation_data()
            pass
        except:
            pass

    def test_ruffus(self):
        pipeline_run(multiprocess=50, verbose=0, pipeline="main")
        for oo in "000.mean", "001.mean":
            results_file_name = os.path.join(working_dir, oo)
            if not os.path.exists(results_file_name):
                raise Exception("Missing %s" % results_file_name)

    def test_newstyle_ruffus(self):

        test_pipeline = Pipeline("test")

        test_pipeline.follows(setup_simulation_data, mkdir(
            gene_data_dir, simulation_data_dir))

        test_pipeline.files(gwas_simulation, generate_simulation_params)\
            .follows(setup_simulation_data)\
            .follows(mkdir(working_dir, os.path.join(working_dir, "simulation_results")))

        test_pipeline.collate(statistical_summary, gwas_simulation, regex(r"simulation_results/(\d+).\d+.simulation_res"), r"\1.mean")\
            .posttask(lambda: sys.stdout.write("\nOK\n"))

        test_pipeline.run(multiprocess=50, verbose=0)
        for oo in "000.mean", "001.mean":
            results_file_name = os.path.join(working_dir, oo)
            if not os.path.exists(results_file_name):
                raise Exception("Missing %s" % results_file_name)


if __name__ == '__main__':
    unittest.main()
