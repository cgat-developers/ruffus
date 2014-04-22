#!/usr/bin/env python
"""

    run_dless2_rebecca.py
    [--log_file PATH]
    [--verbose]

"""

################################################################################
#
#   test
#
#
#   Copyright (c) 7/13/2010 Rebecca Chodroff
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

import sys, os, re, shutil

# add self to search path for testing
if __name__ == '__main__':
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__

# Use import path from <<../python_modules>>
if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "python_modules")))
    sys.path.insert(0, "/net/cpp-group/Leo/inprogress/oss_projects/ruffus/installation")




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


if __name__ == '__main__':
    from optparse import OptionParser
    import StringIO

    parser = OptionParser(version="%prog 1.0", usage = "\n\n    %progs [options]")
    parser.add_option("--targets", dest="targets",
                      metavar="INTEGERS",
                      type="string",
                      help="List of comma separated targets.")
    parser.add_option("--working_dir", dest="working_dir",
                      metavar="PATH",
                      type="string",
                      help="Working directory.")
    parser.add_option("--starting_dir", dest="starting_dir",
                      metavar="PATH",
                      type="string",
                      help="Starting directory.")


    #
    #   general options: verbosity / logging
    #
    parser.add_option("-v", "--verbose", dest = "verbose",
                      action="count", default=0,
                      help="Print more verbose messages for each additional verbose level.")
    parser.add_option("-L", "--log_file", dest="log_file",
                      metavar="FILE",
                      type="string",
                      help="Name and path of log file")
    parser.add_option("--skip_parameter_logging", dest="skip_parameter_logging",
                        action="store_true", default=False,
                        help="Do not print program parameters to log.")
    parser.add_option("--debug", dest="debug",
                        action="count", default=0,
                        help="Set default program parameters in debugging mode.")







    #
    #   pipeline
    #
    parser.add_option("-t", "--target_tasks", dest="target_tasks",
                        action="append",
                        default = list(),
                        metavar="JOBNAME",
                        type="string",
                        help="Target task(s) of pipeline.")
    parser.add_option("-j", "--jobs", dest="jobs",
                        default=1,
                        metavar="N",
                        type="int",
                        help="Allow N jobs (commands) to run simultaneously.")
    parser.add_option("-n", "--just_print", dest="just_print",
                        action="store_true", default=False,
                        help="Don't actually run any commands; just print the pipeline.")
    parser.add_option("--flowchart", dest="flowchart",
                        metavar="FILE",
                        type="string",
                        help="Don't actually run any commands; just print the pipeline "
                             "as a flowchart.")
    parser.add_option("--colour_scheme_index", dest="colour_scheme_index",
                        metavar="INTEGER",
                        type="int",
                        help="Index of colour scheme for flow chart.")

    #
    #   Less common pipeline options
    #
    parser.add_option("--key_legend_in_graph", dest="key_legend_in_graph",
                        action="store_true", default=False,
                        help="Print out legend and key for dependency graph.")
    parser.add_option("--forced_tasks", dest="forced_tasks",
                        action="append",
                        default = list(),
                        metavar="JOBNAME",
                        type="string",
                        help="Pipeline task(s) which will be included even if they are up to date.")

    # get help string
    f =StringIO.StringIO()
    parser.print_help(f)
    helpstr = f.getvalue()
    original_args = " ".join(sys.argv)
    (options, remaining_args) = parser.parse_args()


    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    #                                             #
    #   Debug: Change these                       #
    #                                             #
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if options.debug:
        options.log_file                = os.path.join("run_dless2.log")
        if not options.verbose:
            options.verbose             = 1
        if not options.targets:
            options.targets             = "87"
        if not options.working_dir:
            options.working_dir         = "DLESS"
        if not options.starting_dir:
            options.starting_dir         = "DUMMY"
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    #                                             #
    #   Debug: Change these                       #
    #                                             #
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    #
    #   mandatory options
    #
    mandatory_options = ["targets", "starting_dir", "working_dir"]
    def check_mandatory_options (options, mandatory_options, helpstr):
        """
        Check if specified mandatory options have b een defined
        """
        missing_options = []
        for o in mandatory_options:
            if not getattr(options, o):
                missing_options.append("--" + o)

        if not len(missing_options):
            return

        raise Exception("Missing mandatory parameter%s: %s.\n\n%s\n\n" %
                        ("s" if len(missing_options) > 1 else "",
                         ", ".join(missing_options),
                         helpstr))
    check_mandatory_options (options, mandatory_options, helpstr)




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from ruffus import *
from ruffus.ruffus_exceptions import JobSignalledBreak

#from json import dumps
#from collections import defaultdict


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Constants


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#from read_project_parameter_file import get_keys
#parameters =  get_keys('PARAMETERS')
#
#reference_species = parameters['REFERENCE_SPECIES']
#species = parameters['SPECIES']
#working_dir = parameters['WORKING_DIR_ROOT']
#tree = parameters['TREE']
#ref_sequences = parameters['REFERENCE_SEQUENCES']
#working_dir= parameters['WORKING_DIR_ROOT']
#tba_alignments = parameters['TBA_ALIGNMENTS_DIR']
#tba_projected_alignments = parameters['TBA_PROJECTED_ALIGNMENTS_DIR']
#fasta_alignments = parameters['FASTA_ALIGNMENTS_DIR']
#repeats_dir = parameters['REPEATS_DIR']
#neutral_mods_dir = parameters['NEUTRAL_MODELS_DIR']
#indel_hist_dir = parameters['INDEL_HISTORY_DIR']
#indel_mods_dir = parameters['INDEL_MODELS_DIR']
#
#python_code = parameters['PYTHON_CODE_DIR']
#find_ars = parameters['FIND_ARS']
#maf_project = parameters['MAF_PROJECT_BIN']
#phylo_fit = parameters['PHYLOFIT_BINARY']
#msa_view = parameters['MSA_VIEW_BINARY']
#indel_history = parameters['INDEL_HISTORY_BINARY']
#tree_doctor = parameters['TREE_DOCTOR_BINARY']
#indel_fit = parameters['INDEL_FIT_BINARY']
#dless = parameters['DLESS_BINARY']


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#def get_all_alignment_file_names():
#    alignment_file_names = os.listdir(tba_alignments)
#    return alignment_file_names
#
#def get_all_targets():
#    alignment_file_names = get_all_alignment_file_names()
#    targets = []
#    for alignment_file_name in alignment_file_names:
#        targets.append(alignment_file_name.split('.')[0])
#    return targets
#
#
#def find_ARs(target):
#    coor_file = os.path.join(ref_sequences, target + '_' + reference_species)
#    coor = open(coor_file, 'r').readline()
#    species, chr, start, strand, other = coor.split(':',4)
#    RM_out = os.path.join(repeats_dir, target + '_' + reference_species + '.out')
#    out_file = os.path.join(repeats_dir, target + '_' + reference_species + '.ar')
#    os.system('perl ' + find_ars + ' ' + RM_out + ' >' + out_file)
#    return chr, start, strand, out_file
#
#def write_gff(target):
#    chr, start, strand, out_file = find_ARs(target)
#    file = open(out_file, 'r')
#    line = file.readline()
#    lines = file.readlines()
#    repeats_file = os.path.join(repeats_dir, target + '_' + reference_species + '.gff')
#    repeats = open(repeats_file, 'w')
#    for line in lines:
#        line = line.strip()
#        beg, end, feature = line.split()
#        b = str(int(beg) + int(start))
#        e = str(int(end) + int(start))
#        entry = '\t'.join([chr, 'RepeatMasker', 'AR', b, e,'.', '.','.',feature])
#        repeats.write(entry + '\n')
#    repeats.close()
#    return repeats_file




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Logger


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

if __name__ == '__main__':
    import logging
    import logging.handlers

    MESSAGE = 15
    logging.addLevelName(MESSAGE, "MESSAGE")

    def setup_std_logging (logger, log_file, verbose):
        """
        set up logging using programme options
        """
        class debug_filter(logging.Filter):
            """
            Ignore INFO messages
            """
            def filter(self, record):
                return logging.INFO != record.levelno

        class NullHandler(logging.Handler):
            """
            for when there is no logging
            """
            def emit(self, record):
                pass

        # We are interesting in all messages
        logger.setLevel(logging.DEBUG)
        has_handler = False

        # log to file if that is specified
        if log_file:
            handler = logging.FileHandler(log_file, delay=False)
            handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)6s - %(message)s"))
            handler.setLevel(MESSAGE)
            logger.addHandler(handler)
            has_handler = True

        # log to stderr if verbose
        if verbose:
            stderrhandler = logging.StreamHandler(sys.stderr)
            stderrhandler.setFormatter(logging.Formatter("    %(message)s"))
            stderrhandler.setLevel(logging.DEBUG)
            if log_file:
                stderrhandler.addFilter(debug_filter())
            logger.addHandler(stderrhandler)
            has_handler = True

        # no logging
        if not has_handler:
            logger.addHandler(NullHandler())


    #
    #   set up log
    #
    logger = logging.getLogger(module_name)
    setup_std_logging(logger, options.log_file, options.verbose)

    #
    #   Allow logging across Ruffus pipeline
    #
    def get_logger (logger_name, args):
        return logger

    from ruffus.proxy_logger import *
    (logger_proxy,
     logging_mutex) = make_shared_logger_and_proxy (get_logger,
                                                    module_name,
                                                    {})

    #
    #   log programme parameters
    #
    if not options.skip_parameter_logging:
        programme_name = os.path.split(sys.argv[0])[1]
        logger.info("%s %s" % (programme_name, original_args))


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Pipeline


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
#   convert targets into individual strings
#       and identify files in staring_dir
#
options.targets = re.split(", *", options.targets)
if not len(options.targets):
    raise Exception ("Please specify the targets as a common separated list for --targets")
starting_files = [os.path.join(options.starting_dir, t + ".maf") for t in options.targets]
repeats_files = [os.path.join(options.starting_dir, t + ".repeats") for t in options.targets]

#
# regex to split path out and substitute working directory
#
@follows(mkdir(options.working_dir, "test"))
@transform(starting_files, regex(r"(.+/)([^/]+\.maf)"), os.path.join(options.working_dir, r"\2"))
def copy_maf_into_working_directory(input_file, output_file):
    """
    Make copy in working directory
    """
    shutil.copyfile(input_file, output_file)

@follows(mkdir(options.working_dir))
@transform(repeats_files, regex(r"(.+/)([^/]+\.repeats)"), os.path.join(options.working_dir, r"\2"))
def copy_repeats_into_working_directory(input_file, output_file):
    """
    Make copy in working directory
    """
    shutil.copyfile(input_file, output_file)


#
#   pipes in output from copy_maf_into_working_directory
#
#      working_dir/target.maf ->   working_dir/target.projected_maf
#
@transform(copy_maf_into_working_directory, suffix(".maf"), ".projected_maf")
def project_maf_alignments(input_file, output_file):
    #os.system(maf_project + ' ' + input_file + ' ' + reference_species + ' > ' + output_file)
    open(output_file, "w")

@transform(project_maf_alignments, suffix(".projected_maf"), add_inputs(r"\1.repeats"), r".neutral_model")
@follows(copy_repeats_into_working_directory)
def generate_neutral_model(input_files, output_file):
    maf_file, repeats_file = input_files
    #cmd_str = (phylo_fit + ' --tree ' + tree
    #              + ' --features ' + repeats_file
    #              + ' --do-cats AR --out-root '
    #              + output_file + ' --msa-format MAF '
    #              + maf_file)
    #os.system(cmd_str)
    #run_cmd(cmd_str, "generate neutral model")
    #queue_cmd_prefix    = "qrsh -now n -cwd -p -6 -v BASH_ENV=~/.bashrc -q medium_jobs.q"
    #target_name            = os.path.splitext("maf_file")[0]
    #run_cmd(cmd_str, "generate neutral model", queue_cmd_prefix = queue_cmd_prefix, job_name = target_name)
    open(output_file, "w")


#must convert maf to fasta for indel history program
@transform(project_maf_alignments, suffix(".projected_maf"), ".fa")
def convert_maf2fasta(input_file, output_file):
    #species = (open(species, 'r')).readline()
    #os.system(msa_view + ' ' + input_file\
    #          + ' --soft-masked --seqs '\
    #          + species + ' --in-format MAF > ' + output_file)
    open(output_file, "w")


@follows(generate_neutral_model)
@transform(convert_maf2fasta, regex("(.+).fa"), add_inputs(r"\1.neutral_model"), r"\1.indel_history")
def generate_indel_history(input_files, output_file):
    fasta_file, neutral_model = input_files
    #os.system(indel_history + ' ' + fasta_file + ' ' + neutral_model + ' > ' + output_file)
    open(output_file, "w")

def parameters_for_dless(indel_history_file, neutral_model):
    os.system(tree_doctor + ' -t ' + neutral_model + ' > ' + tree_file)
    cmd = indel_fit + ' ' + indel_history_file + ' ' + tree_file
    fin,fout=os.popen4(cmd)
    indel_mod = fout.read()
    indelmod=[]
    for n in [2,5,8]:
        indelmod.append(indel_mod.split()[n].strip(','))
    return indelmod


@follows(generate_neutral_model)
@follows(convert_maf2fasta)
@transform(generate_indel_history,
            suffix(".indel_history"),
           add_inputs(r"\1.neutral_model", r"\1.fa"),
           ".dless.out")
def run_dless(input_files, output_file):
    indel_history_file, neutral_model, fasta_file = input_files
    #indelmod = parameters_for_dless(indel_history_file, neutral_model)
    #cmd = ' '.join([dless,'-I',','.join(indel_params), '-H', indel_history_file,
    #                alignment, neutral_mod, '>', output_file])
    #os.system(cmd)
    open(output_file, "w")











#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
if __name__ == '__main__':
    if options.just_print:
        pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks,
                            verbose=options.verbose)

    elif options.flowchart:
        pipeline_printout_graph (   open(options.flowchart, "w"),
                                    os.path.splitext(options.flowchart)[1][1:],
                                    options.target_tasks,
                                    options.forced_tasks,
                                    no_key_legend   = not options.key_legend_in_graph,
                                    minimal_key_legend             = True,
                                    user_colour_scheme = {"colour_scheme_index": options.colour_scheme_index},
                                    pipeline_name = "dless2")
        #graph_colour_demo_printout (open(options.flowchart, "w"),
    #                                os.path.splitext(options.flowchart)[1][1:])
    else:
        pipeline_run(options.target_tasks, options.forced_tasks,
                            multiprocess    = options.jobs,
                            logger          = stderr_logger,
                            verbose         = options.verbose)








