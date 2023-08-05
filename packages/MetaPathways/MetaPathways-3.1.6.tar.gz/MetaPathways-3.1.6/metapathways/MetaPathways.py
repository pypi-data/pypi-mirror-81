#!/usr/bin/env python
from __future__ import division

__author__ = "Kishori M Konwar"
__copyright__ = "Copyright 2020, MetaPathways"
__credits__ = [""]
__version__ = "3.5.0"
__maintainer__ = "Kishori M Konwar"
__status__ = "Release"


#from  libs.starcluster.test import  teststarcluster as sctest
#import sys

try:
     import sys, traceback, re, inspect, signal, shutil 
     from os import makedirs, sys, listdir, environ, path, _exit
     #from commands import getstatusoutput
     from optparse import OptionParser
     
     from metapathways.utils import metapathways_utils
     from metapathways.utils.utils import *
     from metapathways.utils.metapathways_utils  import  eprintf, halt_process, exit_process, WorkflowLogger, generate_log_fp
     from metapathways.parsers.parse  import parse_metapaths_parameters
     from metapathways.pipeline.execution import print_commands, print_to_stdout, no_status_updates
     from metapathways.utils.sysutil import pathDelim
     from metapathways.pipeline.metapathways import run_metapathways, get_parameter
     from metapathways.annotate import *

     from metapathways.diagnostics.parameters import *
     from metapathways.diagnostics.diagnoze import *
     from metapathways.pipeline.sampledata import *
except:
   print(""" Could not load some user defined  module functions""")
   print(""" Make sure your typed \"source MetaPathwaysrc\" """)
   print(traceback.print_exc(10))
   sys.exit(3)


cmd_folder = path.abspath(path.split(inspect.getfile( inspect.currentframe() ))[0])

PATHDELIM =  str(pathDelim())

#config = load_config()
metapaths_param = """config/template_param.txt""";

script_info={}
script_info['brief_description'] = """A workflow script for making PGDBs from metagenomic sequences"""
script_info['script_description'] = \
    """ This script starts a MetaPathways pipeline run. It requires an input directory of fasta or genbank files
    containing sequences to process, an output directory for results to be placed. It also requires the
    configuration files, template_config.txt and template_param.txt in the config/ directory, to be updated with the
    location of resources on your system.
    """
script_info['script_usage'] = []


usage=  """Metapathways -i input_dir -o output_dir -p parameters.txt
          \t for more options:  ./MetaPathways.py -h"""

parser = None
def createParser():
    global parser
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_fp",
                      help='the input fasta file/input dir [REQUIRED]')
    parser.add_option("-o", "--output_dir", dest="output_dir",
                      help='the input fasta file/input dir [REQUIRED]')
    parser.add_option('-p','--parameter_fp', dest="parameter_fp", 
                       help='path to the parameter file [REQUIRED]')
    parser.add_option("-d", "--dirref", dest="refdb_dir", 
                      help="location of the reference DB [REQUIRED]")
    parser.add_option('-r','--run-type', dest="run_type", default='safe',
                       choices=['safe', 'overlay', 'overwrite','dry-run'], 
                       help= '\n(a) \'overwrite\' -- wipes out the previous runs with the same name\n'+
                             '\n(b)\'overlay\' -- recomputes the steps that are not present \n' +
                             '\n(d)\'safe\' -- safe mode does not run on an existing run folder\n')
    
    #ith out of order completion \ time-stamps in the \'workflow_log.txt\' 
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print lots of information on the stdout [default]")
    
    parser.add_option("--version", action="store_true", dest="version", default=False,
                      help="print MetaPathways version")
    
    parser.add_option("-s", "--samples", dest="sample_subset", action="append", default=[],
                      help="Processes only samples in the list  subset specified [ -s sample1 -s sample2 ]" )
    



def valid_arguments(opts, args):
    """ checks if the supplied arguments are adequate """
    if (opts.input_fp == None and opts.output_dir ==None )  or\
     opts.output_dir == None:
       return True
    else:
       return False

def derive_sample_name(filename):
    basename = path.basename(filename) 
    
    shortname = re.sub('[.]gbk$','',basename, re.IGNORECASE) 
    shortname = re.sub('[.](fasta|fas|fna|faa|fa)$','',shortname, re.IGNORECASE) 
    return shortname
    


def remove_unspecified_samples(input_output_list, sample_subset,  globalerrorlogger = None):
   """ keep only the samples that are specified  before processing  """

   shortened_names = {}
   input_sample_list = input_output_list.keys()
   for sample_name in input_sample_list:
      short_sample_name = derive_sample_name(sample_name) 
      if len(short_sample_name) > 35:
         eprintf("ERROR\tSample name %s must not be longer than 35 characters!\n",short_sample_name)
         if globalerrorlogger:
             globalerrorlogger.printf("ERROR\tSample name %s must not be longer than 35 characters!\n",short_sample_name)
      if not derive_sample_name(sample_name) in sample_subset and  sample_subset:
         del input_output_list[sample_name]



def check_for_error_in_input_file_name(shortname, globalerrorlogger=None):

    """  creates a list of  input output pairs if input is  an input dir """
    clean = True
    if not re.search(r'^[a-zA-Z]',shortname):
         eprintf("ERROR\tSample name %s must begin with an alphabet!\n",shortname)
         if globalerrorlogger:
            globalerrorlogger.printf("ERROR\tSample name %s must begin with an alphabet!\tConsider prefixing an alphabet to the front\n",shortname)
         clean = False

    if re.search(r'[.]',shortname):
         eprintf("ERROR\tSample name %s contains a '.' in its name!\n",shortname)
         if globalerrorlogger:
            globalerrorlogger.printf("ERROR\tSample name %s contains a '.' in its name!\n",shortname)
         clean = False

    if len(shortname)<2:
         eprintf("ERROR\tSample name %s is too short!\n",shortname)
         if globalerrorlogger:
             globalerrorlogger.printf("ERROR\tSample name %s is too short1\n",shortname)
         clean = False

    if clean:
         return clean

    errmessage = """Sample names before the  suffixes .fasta, .fas, .fna, .faa or .gbk, must  consist only of alphabets, digits and _; and should consist of at least two characters """
    eprintf("ERROR\t%s\n",errmessage)
    if globalerrorlogger:
        globalerrorlogger.printf("ERROR\t%s\n",errmessage)
    #    exit_process(errmessage + "Exiting!" + "\n", logger=globalerrorlogger)
    return False


def create_an_input_output_pair(input_file, output_dir,  globalerrorlogger=None):
    """ creates an input output pair if input is just an input file """
       
    input_output = {}

    if not re.search(r'.(fasta|fas|fna|faa|gbk|gff|fa)$',input_file, re.IGNORECASE):
       return input_output

    shortname = None 
    shortname = re.sub('[.]gbk$','',input_file, re.IGNORECASE) 
    shortname = re.sub('[.](fasta|fas|fna|faa|fa)$','',input_file, re.IGNORECASE) 
    #    shortname = re.sub('[.]gff$','',input_file, re.IGNORECASE) 

    shortname = re.sub(r'.*' + PATHDELIM ,'',shortname) 

    if  check_for_error_in_input_file_name(shortname, globalerrorlogger=globalerrorlogger):
       input_output[input_file] = path.abspath(output_dir) + PATHDELIM + shortname

    return input_output


def create_input_output_pairs(input_dir, output_dir,  globalerrorlogger=None):
    """  creates a list of  input output pairs if input is  an input dir """
    fileslist =  listdir(input_dir)

    gbkPatt = re.compile('[.]gbk$',re.IGNORECASE) 
    fastaPatt = re.compile('[.](fasta|fas|fna|faa|fa)$',re.IGNORECASE) 
    gffPatt = re.compile('[.]gff$',re.IGNORECASE) 

    input_files = {}
    for input_file in fileslist:
       
       shortname = None 
       result = None

       result =  gbkPatt.search(input_file)
       if result:
         shortname = re.sub('[.]gbk$','',input_file, re.IGNORECASE) 

       if result==None:
          result =  fastaPatt.search(input_file)
          if result:
             shortname = re.sub('[.](fasta|fas|fna|faa|fa)$','',input_file, re.IGNORECASE) 

       if shortname == None:
          continue

       if re.search('.(fasta|fas|fna|faa|gff|gbk|fa)$',input_file, re.IGNORECASE):
          if check_for_error_in_input_file_name(shortname, globalerrorlogger=globalerrorlogger):
             input_files[input_file] = shortname

    paired_input = {} 
    for key, value in input_files.items():
       paired_input[input_dir + PATHDELIM + key] = path.abspath(output_dir) + PATHDELIM + value

    return paired_input

def removeSuffix(sample_subset_in):
    sample_subset_out = []
    for sample_name in sample_subset_in:
       mod_name = re.sub('.(fasta|fas|fna|faa|gff|gbk|fa)$','',sample_name)
       sample_subset_out.append(mod_name)

    return sample_subset_out


def openGrades():
    pass

def openRank():
    pass

def halt_on_invalid_input(input_output_list, filetypes, sample_subset):

    for samplePath in input_output_list.keys():
       sampleName =  path.basename(input_output_list[samplePath]) 

       if filetypes[samplePath][0]=='UNKNOWN':
          eprintf("ERROR\tIncorrect input sample %s. Check for bad characters or format\n!", samplePath)
          return False

       ''' in the selected list'''
       if not sampleName in sample_subset:
          continue


    return True
          



def report_missing_filenames(input_output_list, sample_subset, logger=None):
    foundFiles = {}
    for samplePath in input_output_list.keys():
       sampleName =  path.basename(input_output_list[samplePath]) 
       foundFiles[sampleName] =True

    for sample_in_subset in sample_subset:
       if not sample_in_subset in foundFiles:
          eprintf("ERROR\tCannot find input file for sample %s\n!", sample_in_subset)
          if logger:
             logger.printf("ERROR\tCannot file input for sample %s!\n", sample_in_subset)


def process(argv):
    global parser

    (opts, args) = parser.parse_args()
    if opts.version:
       print("MetaPathways: Version " + __version__)
       sys.exit(0)

    if valid_arguments(opts, args):
       print(usage)
       sys.exit(0)


    eprintf("%-10s:%s\n" %('COMMAND', sys.argv[0] + ' ' +  ' '.join(argv)) )
    # initialize the input directory or file
    input_fp = opts.input_fp 
    output_dir = path.abspath(opts.output_dir)
    verbose = opts.verbose

    sample_subset = removeSuffix(opts.sample_subset)
    run_type = opts.run_type.strip()
    '''no need to remove the whole directory'''
#    if run_type == 'overwrite':
#       force_remove_dir=True
#    else:
#       force_remove_dir=False

    # try to load the parameter file    
    try:
       if opts.parameter_fp:
          parameter_fp= opts.parameter_fp
       else:
          parameter_fp = cmd_folder + PATHDELIM + metapaths_param
    except IOError:
        raise IOError( "Can't open parameters file (%s). Does it exist? Do you have read access?" % opts.parameter_fp )

    
    try:
       if run_type in ['overlay', 'safe'] and not path.exists(output_dir):
             makedirs(output_dir)
    except OSError:
        print("")
        print("ERROR: Cannot create output directory \"" + output_dir + "\"\n"+\
              "       Perhaps directory \"" + output_dir  + "\" already exists.\n" +\
              "       Please choose a different directory, or \n" +\
              "       run with the option \"-r  overwrite\" to force overwrite it." )
        sys.exit(2)

    if verbose:
        status_update_callback = print_to_stdout
    else:
        status_update_callback = no_status_updates
    
    command_line_params={}
    command_line_params['verbose']= opts.verbose

    if not path.exists(parameter_fp):
        eprintf("%-10s: No parameters file %s found!\n" %('WARNING', parameter_fp))
        eprintf("%-10s: Creating a parameters file %s found!\n" %('INFO', parameter_fp))
        create_metapaths_parameters(parameter_fp, cmd_folder)

    params=parse_metapaths_parameters(parameter_fp)

    """ load the sample inputs  it expects either a fasta 
        file or  a directory containing fasta and yaml file pairs
    """

    globalerrorlogger = WorkflowLogger(generate_log_fp(output_dir, basefile_name= 'global_errors_warnings'), open_mode='w') 

    input_output_list = {}
    if path.isfile(input_fp):   
       """ check if it is a file """
       input_output_list = create_an_input_output_pair(input_fp, output_dir,  globalerrorlogger=globalerrorlogger)
    else:
       if path.exists(input_fp):   
          """ check if dir exists """
          input_output_list = create_input_output_pairs(input_fp, output_dir, globalerrorlogger=globalerrorlogger)
       else:   
          """ must be an error """
          eprintf("ERROR\tNo valid input sample file or directory containing samples exists .!")
          eprintf("ERROR\tAs provided as arguments in the -in option.!\n")
          exit_process("ERROR\tAs provided as arguments in the -in option.!\n")
   
    """ these are the subset of sample to process if specified
        in case of an empty subset process all the sample """

    # remove all samples that are not specifed unless sample_subset is empty
    remove_unspecified_samples(input_output_list, sample_subset, globalerrorlogger = globalerrorlogger)

    # add check the config parameters 
    sorted_input_output_list = sorted(input_output_list.keys())

    filetypes = check_file_types(sorted_input_output_list) 

    #stop on in valid samples
    if not halt_on_invalid_input(input_output_list, filetypes, sample_subset):
       globalerrorlogger.printf("ERROR\tInvalid inputs found. Check for file with bad format or characters!\n")

    # make sure the sample files are found
    report_missing_filenames(input_output_list, sample_subset, logger=globalerrorlogger)
    parameter =  Parameters()

    config = someclass()
    config.refdb_dir = opts.refdb_dir
    if not staticDiagnose(params, config,  logger = globalerrorlogger):
        eprintf("ERROR\tFailed to pass the test for required scripts and inputs before run\n")
        globalerrorlogger.printf("ERROR\tFailed to pass the test for required scripts and inputs before run\n")
        return 
    
    samplesData = {}
    # PART1 before the blast

    configs = {
        "PREPROCESS_INPUT"     : "MetaPathways_filter_input",
        "PREPROCESS_AMINOS"    : "MetaPathways_preprocess_amino_input",
        "ORF_PREDICTION"       : "MetaPathways_orf_prediction",
        "ORF_TO_AMINO"         : "MetaPathways_create_amino_sequences",
        "FUNC_SEARCH"          : "MetaPathways_func_search",
        "PARSE_FUNC_SEARCH"    : "MetaPathways_parse_blast",
        "COMPUTE_REFSCORES"    : "python_scripts/MetaPathways_refscore",
        "ANNOTATE_ORFS"        : "MetaPathways_annotate_fast",
        "CREATE_ANNOT_REPORTS" : "MetaPathways_create_reports_fast",
        "GENBANK_FILE"         : "MetaPathways_create_genbank_ptinput_sequin",
        "SCAN_rRNA"            : "MetaPathways_rRNA_stats_calculator",
        "SCAN_tRNA"            : "MetaPathways_tRNA_scan",
        "RPKM_CALCULATION"     : "MetaPathways_rpkm", 
        # executable
        "RESOURCES_DIR"        : "resources",
        "BLASTP_EXECUTABLE"    : 'blastp',
        "BLASTN_EXECUTABLE"    : 'blastn',
        "BWA_EXECUTABLE"       : 'bwa',
        "LASTDB_EXECUTABLE"    : 'lastdb+',
        "LAST_EXECUTABLE"      : 'lastal+',
        "PRODIGAL_EXECUTABLE"  : 'prodigal',
        "SCAN_tRNA_EXECUTABLE" : 'trnascan-1.4',
        "RPKM_EXECUTABLE"      : 'rpkm',
        "NUM_CPUS"             : 4,
        "REFDBS"               : opts.refdb_dir
    }

    block_mode = True

    try:
         # load the sample information 
         print("RUNNING MetaPathways Version " + __version__)
         if len(input_output_list): 
              for input_file in sorted_input_output_list:
                sample_output_dir = input_output_list[input_file]
                algorithm = get_parameter(params, 'annotation', 'algorithm', default='LAST').upper()
   
                s = SampleData() 
                s.setInputOutput(inputFile = input_file, sample_output_dir = sample_output_dir)
                s.setParameter('algorithm', algorithm)
                s.setParameter('FILE_TYPE', filetypes[input_file][0])
                s.setParameter('SEQ_TYPE', filetypes[input_file][1])
                s.clearJobs()
   
                if run_type=='overwrite' and  path.exists(sample_output_dir):
                   shutil.rmtree(sample_output_dir)
                   makedirs(sample_output_dir)
                if not  path.exists(sample_output_dir):
                   makedirs(sample_output_dir)
   
                s.prepareToRun()
                samplesData[input_file] = s
   
              # load the sample information 
              run_metapathways(
                   samplesData,
                   sample_output_dir,
                   output_dir,
                   globallogger = globalerrorlogger,
                   command_line_params = command_line_params,
                   params = params,
                   status_update_callback = status_update_callback,
                   config_settings = configs,
                   run_type = run_type, 
                   block_mode = block_mode
              )
         else: 
              eprintf("ERROR\tNo valid input files/Or no files specified  to process in folder %s!\n",sQuote(input_fp) )
              globalerrorlogger.printf("ERROR\tNo valid input files to process in folder %s!\n",sQuote(input_fp) )
   
    except:
       exit_process(str(traceback.format_exc(10)), logger= globalerrorlogger )


    
    eprintf("            ***********                \n")
    eprintf("INFO : FINISHED PROCESSING THE SAMPLES \n")
    eprintf("             THE END                   \n")
    eprintf("            ***********                \n")
    #halt_process(opts.delay)
    #halt_process(3, verbose=opts.verbose)

def main():
    createParser()
    process(sys.argv[1:])    
    sys.exit(get_recent_error())
    halt_process(1)
    
# the main function of metapaths
if __name__ == "__main__":
    createParser()
    process(sys.argv[1:])    
    sys.exit(get_recent_error())
    halt_process(1)
    

