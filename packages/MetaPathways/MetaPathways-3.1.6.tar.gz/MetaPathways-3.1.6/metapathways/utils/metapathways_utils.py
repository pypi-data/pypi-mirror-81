#!/usr/bin/env python

__author__ = "Kishori M Konwar"
__copyright__ = "Copyright 2020, MetaPathways"
__version__ = "3.5.0"
__maintainer__ = "Kishori M Konwar"
__status__ = "Release"


"""Contains general utility code for the metapaths project"""

from shutil import rmtree
from os import getenv, makedirs, _exit
from operator import itemgetter
from os.path import split, splitext, abspath, exists, dirname, join, isdir
from collections import defaultdict
from optparse import make_option
from datetime import datetime
from optparse import OptionParser
import sys, os, traceback, math, re, time
from metapathways.utils.utils import *
from metapathways.utils.errorcodes import error_message, get_error_list, insert_error


def halt_process(secs=4, verbose=False):
    time.sleep(secs)

    errors = get_error_list()
    if len(errors) > 1:
        insert_error(200)

    if verbose:
        for errorcode in errors.keys():
            eprintf("ERROR:\t%d\t%s\n", errorcode, errors[errorcode])

    if len(errors.keys()) > 1:
        errorcode = 200
        _exit(errorcode)
    elif len(errors.keys()) == 1:
        errorcode = errors.keys()[0]
        _exit(errorcode)

    _exit(0)


def exit_process(message=None, logger=None):
    if message != None:
        eprintf("ERROR\t%s", message + "\n")
        eprintf("ERROR\tExiting the Python code\n")
    if logger:
        logger.printf("ERROR\tExiting the Python code\n")
        logger.printf("ERROR\t" + message + "\n")
    _exit(0)


def exit_step(message=None):
    if message != None:
        eprintf("%s", message + "\n")

    eprintf("INFO: Exiting the Python code\n")
    eprintf("ERROR\t" + str(traceback.format_exc(10)) + "\n")
    time.sleep(4)
    _exit(0)


def getShortORFId(orfname):
    # return orfname
    orfNameRegEx = re.compile(r"(\d+_\d+)$")

    pos = orfNameRegEx.search(orfname)

    shortORFname = ""
    if pos:
        shortORFname = pos.group(1)

    return shortORFname


def getShortContigId(contigname):
    contigNameRegEx = re.compile(r"(\d+)$")
    shortContigname = ""
    pos = contigNameRegEx.search(contigname)
    if pos:
        shortContigname = pos.group(1)

    return shortContigname


def ContigID(contigname):
    contigNameRegEx = re.compile(r"^(\S+_\d+)_\d+$")
    shortContigname = ""
    pos = contigNameRegEx.search(contigname)
    if pos:
        shortContigname = pos.group(1)

    return shortContigname


def getSampleNameFromContig(contigname):
    contigNameRegEx = re.compile(r"(.*)_(\d+)$")
    sampleName = ""
    pos = contigNameRegEx.search(contigname)
    if pos:
        sampleName = pos.group(1)

    return sampleName


def strip_taxonomy(product):
    func = re.sub(r"\[[^\[\]]+\]", "", product)
    return func


def getSamFiles(readdir, sample_name):
    """This function finds the set of fastq files that has the reads"""

    samFiles = []
    _samFiles = glob(readdir + PATHDELIM + sample_name + ".sam")

    if _samFiles:
        samFiles = _samFiles

    return samFiles


def getReadFiles(readdir, sample_name):
    """This function finds the set of fastq files that has the reads"""
    fastqFiles = []
    _fastqfiles = glob(
        readdir + PATHDELIM + sample_name + "*.[fF][aA][Ss][Tt][qQ][gz.]*"
    )

    fastqfiles = []
    for _f in _fastqfiles:
        f = re.sub(r"^.*[//]", "", _f)
        fastqfiles.append(f)

    samPATT = re.compile(sample_name + ".fastq")
    samPATT1 = re.compile(sample_name + "[.]b\d+.fastq")
    samPATT2 = re.compile("(" + sample_name + ")" + "_[1-2].(fastq|fastq[.]gz)")
    samPATT3 = re.compile(sample_name + "_r[1-2].fastq")
    samPATT4 = re.compile(sample_name + "_[1-2][.](b\d+).fastq")

    batch = {}
    for f in fastqfiles:
        res = samPATT.search(f)
        if res:
            readfiles.append([readdir + PATHDELIM + f])
            continue

        res = samPATT1.search(f)
        if res:
            readfiles.append([readdir + PATHDELIM + f])
            continue

        res = samPATT2.search(f)
        if res:
            if not res.group(1) in batch:
                batch[res.group(1)] = []
            batch[res.group(1)].append(readdir + PATHDELIM + f)
            continue

        res = samPATT3.search(f)
        if res:
            if not "r" in batch:
                batch["r"] = []
            batch["r"].append(readdir + PATHDELIM + f)
            continue

        res = samPATT4.search(f)
        if res:
            if not res.group(1) in batch:
                batch[res.group(1)] = []
            batch[res.group(1)].append(readdir + PATHDELIM + f)
            continue

        eprintf(
            'ERROR\tPossible error in read file naming "%s". Ignoring for now!\n', f
        )

    readfiles = []
    for key, values in batch.items():
        readfiles.append(values)

    return readfiles


def deprecated____getReadFiles(readdir, sample_name):
    """This function finds the set of fastq files that has the reads"""

    fastqFiles = []

    _fastqfiles = glob(readdir + PATHDELIM + sample_name + "_[12].[fF][aA][Ss][Tt][qQ]")

    if _fastqfiles:
        fastqFiles = _fastqfiles

    _fastqfiles = glob(readdir + PATHDELIM + sample_name + "_[12].[fF][qQ]")
    if _fastqfiles:
        fastqFiles = _fastqfiles

    _fastqfiles = glob(readdir + PATHDELIM + sample_name + ".[fF][aA][Ss][Tt][qQ]")
    if _fastqfiles:
        fastqFiles = _fastqfiles

    _fastqfiles = glob(readdir + PATHDELIM + sample_name + ".[fF][qQ]")
    if _fastqfiles:
        fastqFiles = _fastqfiles

    return fastqFiles


class GffFileParser(object):
    def __init__(self, gff_filename):
        self.Size = 10000
        self.i = 0
        self.orf_dictionary = {}
        self.gff_beg_pattern = re.compile("^#")
        self.lines = []
        self.size = 0
        try:
            self.gff_file = open(gff_filename, "r")
        except AttributeError:
            print("Cannot read the map file for database :" + dbname)
            sys.exit(0)

    def __iter__(self):
        return self

    def refillBuffer(self):
        self.orf_dictionary = {}
        i = 0
        while i < self.Size:
            line = self.gff_file.readline()
            if not line:
                break
            if self.gff_beg_pattern.search(line):
                continue
            self.insert_orf_into_dict(line, self.orf_dictionary)
            i += 1

        self.orfs = list(self.orf_dictionary.keys())
        self.size = len(self.orfs)
        self.i = 0

    def __next__(self):
        if self.i == self.size:
            self.refillBuffer()

        if self.size == 0:
            self.gff_file.close()
            raise StopIteration()

        if self.i < self.size:
            self.i = self.i + 1
            return self.orfs[self.i - 1]

    def insert_orf_into_dict(self, line, contig_dict):
        rawfields = re.split("\t", line)
        fields = []
        for field in rawfields:
            fields.append(field.strip())

        if len(fields) != 9:
            return

        attributes = {}
        attributes["seqname"] = fields[0]  # this is a bit of a  duplication
        attributes["source"] = fields[1]
        attributes["feature"] = fields[2]
        attributes["start"] = int(fields[3])
        attributes["end"] = int(fields[4])

        try:
            attributes["score"] = float(fields[5])
        except:
            attributes["score"] = fields[5]

        attributes["strand"] = fields[6]
        attributes["frame"] = fields[7]

        self.split_attributes(fields[8], attributes)

        if not fields[0] in contig_dict:
            contig_dict[fields[0]] = []

        contig_dict[fields[0]].append(attributes)

    def insert_attribute(self, attributes, attribStr):
        rawfields = re.split("=", attribStr)
        if len(rawfields) == 2:
            attributes[rawfields[0].strip().lower()] = rawfields[1].strip()

    def split_attributes(self, str, attributes):
        rawattributes = re.split(";", str)
        for attribStr in rawattributes:
            self.insert_attribute(attributes, attribStr)

        return attributes


class Performance:
    def __init__(self):
        self.sum = {}
        self.sqsum = {}
        self.num = {}

    def getAverageDelay(self, server=None):
        if server == None:
            avg = 0
            num = 0
            for server in self.sum:
                avg += self.sum[server]
                num += self.num[server]
            if num > 0:
                return avg / num
            else:
                return 0

        if self.num[server] == 0:
            return 0
        avg = self.sum[server] / self.num[server]
        return avg

    def getStdDeviationDelay(self, server=None):
        if server == None:
            avg = 0
            avgsq = 0
            num = 0
            for server in self.sum:
                avg += self.sum[server]
                avgsq += self.sqsum[server]
                num += self.num[server]
            if num == 0:
                return 0

        var = avgsq / num - avg * avg / (num * num)
        std = math.sqrt(var)
        return std

    def addPerformanceData(self, server, data):
        if not server in self.sum:
            self.sum[server] = 0
            self.sqsum[server] = 0
            self.num[server] = 0

        self.sum[server] += data
        self.sqsum[server] += data * data
        self.num[server] += 1
        return True

    def getExpectedDelay(self):
        return 20


class Job:
    def __init__(self, S, d, a, m, server=None):
        self.S = S  # sample
        self.d = d  # database
        self.a = a  # split
        self.m = m  # algorithm
        self.server = None  # server
        return None

    def setValues(self, S, d, a, m, t, server=None):
        self.S = S
        self.d = d
        self.a = a
        self.m = m
        self.submission_time = t
        self.server = server
        return True


def parse_command_line_parameters(script_info, argv):
    opts = []
    return opts


class TreeMissingError(IOError):
    """Exception for missing tree file"""

    pass


class OtuMissingError(IOError):
    """Exception for missing OTU file"""

    pass


class AlignmentMissingError(IOError):
    """Exception for missing alignment file"""

    pass


class MissingFileError(IOError):
    pass


def make_safe_f(f, allowed_params):
    """Make version of f that ignores extra named params."""

    def inner(*args, **kwargs):
        if kwargs:
            new_kwargs = {}
            for k, v in kwargs.items():
                if k in allowed_params:
                    new_kwargs[k] = v
            return f(*args, **new_kwargs)
        return f(*args, **kwargs)

    return inner


class FunctionWithParams(object):
    """A FunctionWithParams is a replacement for the function factory.

    Specifically, the params that will be used in the __call__ method are
    available in a dict so you can keep track of them with the object
    itself.
    """

    Application = None
    Algorithm = None
    Citation = None
    Params = {}
    Name = "FunctionWithParams"  # override in subclasses
    _tracked_properties = []  # properties tracked like params

    def __init__(self, params):
        """Return new FunctionWithParams object with specified params.

        Note: expect params to contain both generic and per-method (e.g. for
        cdhit) params, so leaving it as a dict rather than setting
        attributes.

        Some standard entries in params are:

        [fill in on a per-application basis]
        """
        self.Params.update(params)
        self._tracked_properties.extend(["Application", "Algorithm", "Citation"])

    def __str__(self):
        """Returns formatted key-value pairs from params."""
        res = [self.Name + " parameters:"]
        for t in self._tracked_properties:
            res.append(t + ":" + str(getattr(self, t)))
        for k, v in sorted(self.Params.items()):
            res.append(str(k) + ":" + str(v))
        return "\n".join(res)

    def writeLog(self, log_path):
        """Writes self.Params and other relevant info to supplied path."""
        f = open(log_path, "w")
        f.write(str(self))
        f.close()

    def getResult(self, *args, **kwargs):
        """Gets result in __call__. Override in subclasses."""
        return None

    def formatResult(self, result):
        """Formats result as string (for whatever "result" means)."""
        return str(result)

    def writeResult(self, result_path, result):
        """Writes result to result_path. May need to format in subclasses."""
        f = open(result_path, "w")
        f.write(self.formatResult(result))
        f.close()

    def __call__(self, result_path=None, log_path=None, *args, **kwargs):
        """Returns the result of calling the function using the params dict.

        Parameters:
        [fill in on a per-application basis]
        """
        print("""Function with parameters""")
        result = self.getResult(*args, **kwargs)
        if log_path:
            self.writeLog(log_path)
        if result_path:
            self.writeResult(result_path, result)
        else:
            return result


def get_qiime_project_dir():
    """Returns the top-level QIIME directory"""
    # Get the full path of util.py
    current_file_path = abspath(__file__)
    # Get the directory containing util.py
    current_dir_path = dirname(current_file_path)
    # Return the directory containing the directory containing util.py
    return dirname(current_dir_path)


def get_qiime_scripts_dir():
    """Returns the QIIME scripts directory

    This value must be stored in qiime_config if the user
    has installed qiime using setup.py. If it is not in
    qiime_config, it is inferred from the qiime_project_dir.

    """
    qiime_config = load_qiime_config()
    qiime_config_value = qiime_config["qiime_scripts_dir"]
    if qiime_config_value != None:
        result = qiime_config_value
    else:
        result = join(get_qiime_project_dir(), "scripts")

    # assert exists(result),\
    # "qiime_scripts_dir does not exist: %s." % result +\
    # " Have you defined it correctly in your qiime_config?"

    return result


def load_qiime_config():
    """Return default parameters read in from file"""

    qiime_config_filepaths = []
    qiime_project_dir = get_qiime_project_dir()
    qiime_config_filepaths.append(
        qiime_project_dir + "/qiime/support_files/qiime_config"
    )

    qiime_config_env_filepath = getenv("QIIME_CONFIG_FP")
    if qiime_config_env_filepath:
        qiime_config_filepaths.append(qiime_config_env_filepath)

    home_dir = getenv("HOME")
    if home_dir:
        qiime_config_home_filepath = home_dir + "/.qiime_config"
        qiime_config_filepaths.append(qiime_config_home_filepath)

    qiime_config_files = []
    for qiime_config_filepath in qiime_config_filepaths:
        if exists(qiime_config_filepath):
            qiime_config_files.append(open(qiime_config_filepath))

    return parse_qiime_config_files(qiime_config_files)


# The qiime_blast_seqs function should evetually move to PyCogent,
# but I want to test that it works for all of the QIIME functionality that
# I need first. -Greg


def extract_seqs_by_sample_id(seqs, sample_ids, negate=False):
    """ Returns (seq id, seq) pairs if sample_id is in sample_ids """
    sample_ids = {}.fromkeys(sample_ids)

    if not negate:

        def f(s):
            return s in sample_ids

    else:

        def f(s):
            return s not in sample_ids

    for seq_id, seq in seqs:
        sample_id = seq_id.split("_")[0]
        if f(sample_id):
            yield seq_id, seq


def split_fasta_on_sample_ids(seqs):
    """yields (sample_id, seq_id, seq) for each entry in seqs

    seqs: (seq_id,seq) pairs, as generated by MinimalFastaParser

    """
    for seq_id, seq in seqs:
        yield (seq_id.split()[0].rsplit("_", 1)[0], seq_id, seq)
    return


def split_fasta_on_sample_ids_to_dict(seqs):
    """return split_fasta_on_sample_ids as {sample_id: [(seq_id, seq), ], }

    seqs: (seq_id,seq) pairs, as generated by MinimalFastaParser

    """
    result = {}
    for sample_id, seq_id, seq in split_fasta_on_sample_ids(seqs):
        try:
            result[sample_id].append((seq_id, seq))
        except KeyError:
            result[sample_id] = [(seq_id, seq)]
    return result


def split_fasta_on_sample_ids_to_files(seqs, output_dir):
    """output of split_fasta_on_sample_ids to fasta in specified output_dir

    seqs: (seq_id,seq) pairs, as generated by MinimalFastaParser
    output_dir: string defining directory where output should be
     written, will be created if it doesn't exist

    """
    create_dir(output_dir)
    file_lookup = {}
    for sample_id, seq_id, seq in split_fasta_on_sample_ids(seqs):
        try:
            file_lookup[sample_id].write(">%s\n%s\n" % (seq_id, seq))
        except KeyError:
            file_lookup[sample_id] = open("%s/%s.fasta" % (output_dir, sample_id), "w")
            file_lookup[sample_id].write(">%s\n%s\n" % (seq_id, seq))
    for file_handle in file_lookup.values():
        file_handle.close()
    return None


def isarray(a):
    """
    This function tests whether an object is an array
    """
    try:
        validity = isinstance(a, ndarray)
    except:
        validity = False

    return validity


def degap_fasta_aln(seqs):
    """degap a Fasta aligment.

    seqs: list of label,seq pairs
    """

    for (label, seq) in seqs:
        degapped_seq = Sequence(moltype=DNA_with_more_gaps, seq=seq, name=label).degap()
        degapped_seq.Name = label
        yield degapped_seq


def write_degapped_fasta_to_file(seqs, tmp_dir="/tmp/"):
    """ write degapped seqs to temp fasta file."""

    tmp_filename = get_tmp_filename(
        tmp_dir=tmp_dir, prefix="degapped_", suffix=".fasta"
    )
    fh = open(tmp_filename, "w")

    for seq in degap_fasta_aln(seqs):
        fh.write(seq.toFasta() + "\n")
    fh.close()
    return tmp_filename


# remove the string "/pathway-tools" to infer the pathway tools dir
def create_pathway_tools_dir_path_From_executable(pathway_tools_executable):
    return pathway_tools_executable.replace(
        "pathway-tools/pathway-tools", "pathway-tools"
    )


# removes an existing pgdb from the  ptools-local/pgdbs/user directory under the
# pathway tools directory
def remove_existing_pgdb(sample_name, pathway_tools_exec):
    suffix_to_remove = ""
    # crete the pathway tools dir
    pathway_tools_dir = create_pathway_tools_dir_path_From_executable(
        pathway_tools_exec
    )

    sample_pgdb_dir = (
        pathway_tools_dir + "/" + "ptools-local/pgdbs/user/" + sample_name + "cyc"
    )
    if os.path.exists(sample_pgdb_dir):
        return rmtree(sample_pgdb_dir)


def generate_log_fp(output_dir, basefile_name="", suffix="txt", timestamp_pattern=""):
    filename = "%s.%s" % (basefile_name, suffix)
    return join(output_dir, filename)


class WorkflowError(Exception):
    pass


def contract_key_value_file(fileName):

    file = open(fileName, "r")
    lines = file.readlines()
    if len(lines) < 20:
        file.close()
        return

    keyValuePairs = {}

    for line in lines:
        fields = [x.strip() for x in line.split("\t")]
        if len(fields) == 2:
            keyValuePairs[fields[0]] = fields[1]
    file.close()

    file = open(fileName, "w")
    for key, value in keyValuePairs.items():
        fprintf(file, "%s\t%s\n", key, value)
    file.close()


class FastaRecord(object):
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence


#    return FastaRecord(title, sequence)


def read_fasta_records(input_file):
    records = []
    sequence = ""
    while 1:
        line = input_file.readline()
        if line == "":
            if sequence != "" and name != "":
                records.append(FastaRecord(name, sequence))
            return records

        if line == "\n":
            continue

        line = line.rstrip()
        if line.startswith(">"):
            if sequence != "" and name != "":
                records.append(FastaRecord(name, sequence))

            name = line.rstrip()
            sequence = ""
        else:
            sequence = sequence + line.rstrip()
    return records


class WorkflowLogger(object):
    def __init__(self, log_fp=None, params=None, metapaths_config=None, open_mode="w"):
        if log_fp:
            self._filename = log_fp
            # contract the file if we have to
            if open_mode == "c":
                try:
                    contract_key_value_file(log_fp)
                except:
                    pass
                open_mode = "a"
            self._f = open(self._filename, open_mode)
            self._f.close()
        else:
            self._f = None

        # start_time = datetime.now().strftime('%H:%M:%S on %d %b %Y')
        self.writemetapathsConfig(metapaths_config)
        self.writeParams(params)

    def get_log_filename(self):
        return self._filename

    def printf(self, fmt, *args):
        self._f = open(self._filename, "a")
        if self._f:
            self._f.write(fmt % args)
            self._f.flush()
        else:
            pass
        self._f.close()

    def write(self, s):
        self._f = open(self._filename, "a")
        if self._f:
            self._f.write(s)
            # Flush here so users can see what step they're
            # on after each write, since some steps can take
            # a long time, and a relatively small amount of
            # data is being written to the log files.
            self._f.flush()
        else:
            pass
        self._f.close()

    def writemetapathsConfig(self, metapaths_config):
        if metapaths_config == None:
            # self.write('#No metapaths config provided.\n')
            pass
        else:
            self.write("#metapaths_config values:\n")
            for k, v in metapaths_config.items():
                if v:
                    self.write("%s\t%s\n" % (k, v))
            self.write("\n")

    def writeParams(self, params):
        if params == None:
            # self.write('#No params provided.\n')
            pass
        else:
            self.write("#parameter file values:\n")
            for k, v in params.items():
                for inner_k, inner_v in v.items():
                    val = inner_v or "True"
                    self.write("%s:%s\t%s\n" % (k, inner_k, val))
            self.write("\n")

    def close(self):
        end_time = datetime.now().strftime("%H:%M:%S on %d %b %Y")
        self.write("\nLogging stopped at %s\n" % end_time)
        if self._f:
            self._f.close()
        else:
            pass


def ShortenORFId(_orfname, RNA=False):

    ORFIdPATT = re.compile("(\\d+_\\d+)$")
    RNAPATT = re.compile("(\\d+_\\d+_[tr]RNA)$")

    if RNA:
        result = RNAPATT.search(_orfname)
    else:
        result = ORFIdPATT.search(_orfname)

    if result:
        shortORFname = result.group(1)
    else:
        return ""
    return shortORFname


def ShortentRNAId(_orfname):
    ORFIdPATT = re.compile("(\\d+_\\d+_tRNA)$")

    result = ORFIdPATT.search(_orfname)

    if result:
        shortORFname = result.group(1)

    else:
        return ""
    return shortORFname


def ShortenrRNAId(_orfname):
    ORFIdPATT = re.compile("(\\d+_\\d+_rRNA)$")

    result = ORFIdPATT.search(_orfname)
    if result:
        shortORFname = result.group(1)
    else:
        return ""
    return shortORFname


def ShortenContigId(_contigname):
    ContigIdPATT = re.compile("(\\d+)$")

    result = ContigIdPATT.search(_contigname)

    if result:
        shortContigname = result.group(1)
    else:
        return ""

    return shortContigname


def create_metapaths_parameters(filename, folder):
    """ creates a parameters file from the default """
    default_filename = (
        folder + PATHDELIM + "resources" + PATHDELIM + "template_param.txt"
    )

    with open(default_filename, "r") as filep, open(filename, "w") as newfile:
        for line in filep.readlines():
            fprintf(newfile, "%s", line)

    return True


def touch(fname, times=None):
    with open(fname, "a"):
        os.utime(fname, times)

