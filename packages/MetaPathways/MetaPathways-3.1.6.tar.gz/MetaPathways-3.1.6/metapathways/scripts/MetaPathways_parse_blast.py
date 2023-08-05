#!/usr/bin/python
# File created on 27 Jan 2012.
from __future__ import division

__author__ = "Kishori M Konwar"
__copyright__ = "Copyright 2013, MetaPathways"
__credits__ = ["r"]
__version__ = "1.0"
__maintainer__ = "Kishori M Konwar"
__status__ = "Release"

try:
    from os import makedirs, sys, remove, rename
    from sys import path
    import re, math, traceback
    from copy import copy
    from optparse import OptionParser, OptionGroup

    from metapathways.utils.metapathways_utils import (
        parse_command_line_parameters,
        fprintf,
        printf,
        eprintf,
        exit_process,
        ShortenORFId,
    )
    from metapathways.utils.sysutil import getstatusoutput
    from metapathways.utils.errorcodes import (
        error_message,
        get_error_list,
        insert_error,
    )
    from metapathways.utils.errorcodes import *
except:
    print(""" Could not load some user defined  module functions""")
    print(""" Make sure your typed 'source MetaPathwaysrc' """)
    print(""" """)
    sys.exit(3)


usage = (
    sys.argv[0]
    + " -d dbname1 -b blastout_for_database1 -m map_for_database1 [-d dbname2 -b blastout_for_database2 -m map_for_database2 ] "
    ""
)


parser = None
errorcode = 5


def createParser():
    global parser

    epilog = """This script parses BLAST/LAST search results of the amino acid sequences against the reference protein databases, in a tabular format. In the context of MetaPathways these files are available in the in the folder blast_results. The tabular results are put in individual files, one for each of the databases and algorithms combinations. This script parses these results  and uses the hits based on the specified cutoffs for the evalue, bit score ratio, etc the parsed results are put in file named according to the format
<samplename><dbname><algorithm>out.parsed.txt. These parsed files are in a tabular format and each row contains information about the hits in terms of start, end, query name, match name, bit score ratio, etc."""

    parser = OptionParser(usage, epilog=epilog)
    parser.add_option(
        "-b",
        "--blastoutput",
        dest="input_blastout",
        action="append",
        default=[],
        help="the input blastout files [at least 1 REQUIRED]",
    )
    parser.add_option(
        "-d",
        "--dbasename",
        dest="database_name",
        action="append",
        default=[],
        help="the database names [at least 1 REQUIRED]",
    )
    parser.add_option(
        "-o",
        "--parsedoutput",
        dest="parsed_output",
        default=None,
        help="the parsed  output file [OPTIONAL]",
    )

    parser.add_option(
        "-r", "--ref_score", dest="refscore_file", help="the refscore  table [REQUIRED]"
    )

    parser.add_option(
        "-m",
        "--map_for_database",
        dest="database_map",
        action="append",
        default=[],
        help="the map file for the database  [at least 1 REQUIRED]",
    )

    parser.add_option(
        "-a",
        "--algorithm",
        dest="algorithm",
        choices=["BLAST", "LAST"],
        default="BLAST",
        help="the algorithm used for computing homology [DEFAULT: BLAST]",
    )

    cutoffs_group = OptionGroup(parser, "Cuttoff Related Options")

    cutoffs_group.add_option(
        "--min_score",
        dest="min_score",
        type="float",
        default=20,
        help="the minimum bit score cutoff [default = 20 ] ",
    )
    cutoffs_group.add_option(
        "--min_query_coverage",
        dest="min_query_coverage",
        type="float",
        default=0,
        help="the minimum bit query_coverage cutoff [default = 0 ] ",
    )
    cutoffs_group.add_option(
        "--max_evalue",
        dest="max_evalue",
        type="float",
        default=1e-6,
        help="the maximum E-value cutoff [ default = 1e-6 ] ",
    )
    cutoffs_group.add_option(
        "--min_length",
        dest="min_length",
        type="float",
        default=30,
        help="the minimum length of query cutoff [default = 30 ] ",
    )
    cutoffs_group.add_option(
        "--max_length",
        dest="max_length",
        type="float",
        default=10000,
        help="the maximum length of query cutoff [default = 10000 ] ",
    )

    cutoffs_group.add_option(
        "--min_identity",
        dest="min_identity",
        type="float",
        default=20,
        help="the minimum identity of query cutoff [default 30 ] ",
    )
    cutoffs_group.add_option(
        "--max_identity",
        dest="max_identity",
        type="float",
        default=100,
        help="the maximum identity of query cutoff [default = 100 ] ",
    )

    cutoffs_group.add_option(
        "--max_gaps",
        dest="max_gaps",
        type="float",
        default=1000,
        help="the maximum gaps of query cutoff [default = 1000] ",
    )
    cutoffs_group.add_option(
        "--limit",
        dest="limit",
        type="float",
        default=5,
        help="max number of hits per query cutoff [default = 5 ] ",
    )

    cutoffs_group.add_option(
        "--min_bsr",
        dest="min_bsr",
        type="float",
        default=0.30,
        help="minimum BIT SCORE RATIO [default = 0.30 ] ",
    )
    parser.add_option_group(cutoffs_group)

    output_options_group = OptionGroup(parser, "Output Options")
    output_options_group.add_option(
        "--tax",
        dest="taxonomy",
        action="store_true",
        default=False,
        help="add the taxonomy info [useful for refseq] ",
    )
    output_options_group.add_option(
        "--remove_tax",
        dest="remove_taxonomy",
        action="store_true",
        default=False,
        help="removes the taxonomy from product [useful for refseq] ",
    )
    output_options_group.add_option(
        "--remove_ec",
        dest="remove_ec",
        action="store_true",
        default=False,
        help="removes the EC number from product [useful for kegg/metacyc] ",
    )

    output_options_group.add_option(
        "--compact_output",
        dest="compact_output",
        action="store_true",
        default=False,
        help="compact output [OPTIONAL]",
    )

    parser.add_option_group(output_options_group)

    bitscore_params = OptionGroup(parser, "Bit Score Parameters")
    bitscore_params.add_option(
        "--lambda",
        dest="Lambda",
        default=None,
        type="float",
        help="lambda parameter to compute bit score [useful for BSR] ",
    )
    bitscore_params.add_option(
        "--k",
        dest="k",
        default=None,
        type="float",
        help="k parameter to compute bit score [useful for BSR] ",
    )
    parser.add_option_group(bitscore_params)


def check_arguments(opts, args):
    if len(opts.input_blastout) == 0:
        print("There sould be at least one blastoutput file")
        return False

    if len(opts.database_name) == 0:
        print("There sould be at least one database name")
        return False

    if len(opts.database_map) == 0:
        print("There sould be at least one database map file name")
        return False

    if len(opts.input_blastout) != len(opts.database_name) or len(
        opts.input_blastout
    ) != len(opts.database_map):
        print(
            "The number of database names, blastoutputs and database map file should be equal"
        )
        return False

    if opts.refscore_file == None:
        print("Must specify the refscore")
        return False

    return True


def create_query_dictionary(
    blastoutputfile, query_dictionary, algorithm, errorlogger=None
):
    seq_beg_pattern = re.compile("^#")

    try:
        blastoutfh = open(blastoutputfile, "r")
    except:
        print(
            "ERROR : cannot open B/LAST output file " + blastoutputfile + " to parse "
        )
        return

    try:
        for line in blastoutfh:
            if not seq_beg_pattern.search(line):
                words = line.rstrip().split("\t")
                if len(words) != 12:
                    continue

                if algorithm == "BLAST":
                    if not words[1] in query_dictionary:
                        query_dictionary[words[1]] = True

                if algorithm == "LAST":
                    if not words[1] in query_dictionary:
                        query_dictionary[words[1]] = True
        blastoutfh.close()
    except:
        eprintf(
            "\nERROR : while reading  B/LAST output file "
            + blastoutputfile
            + " to parse "
            + "        : make sure B/LAST ing was done for the particular database"
        )

        if errorlogger:
            errorlogger.write(
                "\nERROR : while reading  B/LAST output file %s to parse\n"
                % (blastoutputfile)
            )
            errorlogger.write(
                "      : make sure B/LAST ing was done for the particular database\n"
            )
        pass


def create_dictionary(databasemapfile, annot_map, query_dictionary, errorlogger=None):
    if not query_dictionary:
        print("WARNING : empty query dictionary in parse B/LAST")

        if errorlogger:
            errologger.write("WARNING : empty query dictionary in parse B/LAST\n")
        return

    seq_beg_pattern = re.compile(">")
    try:
        dbmapfile = open(databasemapfile, "r")
    except:
        if errorlogger:
            errologger.write(
                "PARSE_BLAST\tERROR\tCannot open database map file %s\t Please check the file manuallyT\n"
                % (databasemapfile)
            )
        exit_process("ERROR: Cannot open database map file %s\n" % (databasemapfile))

    for line in dbmapfile:
        if seq_beg_pattern.search(line):
            words = line.rstrip().split()
            name = words[0].replace(">", "", 1)
            if not name in query_dictionary:
                continue
            words.pop(0)
            if len(words) == 0:
                annotation = "hypothetical protein"
            else:
                annotation = " ".join(words)

            annot_map[name] = annotation
    dbmapfile.close()

    if len(annot_map) == 0:
        if errorlogger:
            errorlogger.write(
                "PARSE_BLAST\tERROR\tFile "
                + databasemapfile
                + " seems to be empty!\tCreate datbasemap file\n"
            )
            errorlogger.write(
                "Try re-running after deleting file : %s\n" % (databasemapfile)
            )
        exit_process("no anntations in file :" + databasemapfile)


class BlastOutputParser(object):
    commentPATTERN = re.compile(r"^#")
    commentLAST_VERSION_PATTERN = re.compile(r"^#.*LAST[\s]+version[\s]+\d+")

    def create_refBitScores(self):
        refscorefile = open(self.refscore_file, "r")
        for line in refscorefile:
            words = [x.strip() for x in line.split("\t")]
            if len(words) == 2:
                orfid = ShortenORFId(words[0])
                try:
                    self.refBitScores[orfid] = int(
                        (self.Lambda * float(words[1]) - self.lnk) / self.ln2
                    )
                except:
                    self.refBitScores[orfid] = int(1)
        refscorefile.close()

    def __init__(
        self,
        dbname,
        blastoutput,
        database_mapfile,
        refscore_file,
        opts,
        errorlogger=None,
    ):
        self.Size = 10000
        self.dbname = dbname
        self.ln2 = 0.69314718055994530941
        self.lnk = math.log(opts.k)
        self.Lambda = opts.Lambda
        self.blastoutput = blastoutput
        self.database_mapfile = database_mapfile
        self.refscore_file = refscore_file
        self.annot_map = {}
        self.i = 0
        self.opts = opts
        self.hits_counts = {}
        self.data = {}
        self.refscores = {}
        self.refBitScores = {}
        self.needToPermute = False

        self.MAX_READ_ERRORS_ALLOWED = 10
        self.ERROR_COUNT = 0
        self.STEP_NAME = "PARSE_BLAST"
        self.error_and_warning_logger = errorlogger

        # print "trying to open blastoutput file " + blastoutput
        query_dictionary = {}

        try:
            create_query_dictionary(
                self.blastoutput,
                query_dictionary,
                self.opts.algorithm,
                errorlogger=errorlogger,
            )
        except:
            insert_error(5)

        try:
            self.blastoutputfile = open(self.blastoutput, "r")
        except:
            eprintf(
                "\nERROR : cannot open B/LAST output file "
                + blastoutput
                + " to parse "
                + '      : make sure "B/LAST"ing was done for the particular database'
            )

            if self.error_and_warning_logger:
                self.error_and_warning_logger.write(
                    "ERROR : cannot open B/LAST output file %s %s to parse \n"
                    + '      : make sure "B/LAST"ing was done for '
                    + "the particular database" % (blastoutput)
                )
            insert_error(5)
            exit_process("Cannot open B/LAST output file " + blastoutput)

        try:
            self.create_refBitScores()
        except:
            print(traceback.print_exc(10))
            exit_process(
                "Error while reading from  B/LAST refscore file " + self.refscore_file
            )
        try:
            create_dictionary(database_mapfile, self.annot_map, query_dictionary)
            query_dictionary = {}
        except AttributeError:
            eprintf("Cannot read the map file for database : %s\n" % (dbname))
            if errorlogger != None:
                errorlogger.write(
                    'PARSE_BLAST\tERROR\tCannot read the map file %s for database : %s\tDelete the formatted files for the database in the "formatted" folder\n'
                    % (database_mapfile, dbname)
                )

            exit_process("Cannot read the map file for database  " + dbname)

    def setMaxErrorsLimit(self, max):
        self.MAX_READ_ERRORS_ALLOWED = max

    def setErrorAndWarningLogger(self, logger):
        self.error_and_warning_logger = logger

    def setSTEP_NAME(self, step_name):
        self.STEP_NAME = step_name

    def incErrorCount(self):
        self.ERROR_COUNT += 1

    def maxErrorsReached(self):
        return self.ERROR_COUNT > self.MAX_READ_ERRORS_ALLOWED

    def __iter__(self):
        return self

    def permuteForLAST(self, words):
        try:
            temp = copy(words)
            words[0] = temp[6]  # query
            words[1] = temp[1]  # target
            words[2] = 100.0  # percent id
            words[3] = temp[3]  # aln length
            words[6] = temp[2]
            words[7] = int(temp[2]) + int(temp[3]) - 1
            words[10] = 0.0  # evalue
            words[11] = temp[0]
        except:
            eprintf("ERROR : Invalid B/LAST output file %s \n" % (self.blastoutput))
            if self.error_and_warning_logger:
                self.error_and_warning_logger.write(
                    "ERROR : Invalid B/LAST output file" % (self.blastoutput)
                )
            exit_process("ERROR : Invalid B/LAST output file %s " % (self.blastoutput))

    def refillBuffer(self):
        i = 0
        self.lines = []
        line = True  # self.blastoutputfile.readline()
        while line and i < self.Size:
            line = self.blastoutputfile.readline()
            if self.commentPATTERN.match(line):
                if self.commentLAST_VERSION_PATTERN.match(line) == False:
                    self.needToPermute = True
                continue
            self.lines.append(line)
            if not line:
                break
            i += 1
        self.size = len(self.lines)

    def __next__(self):
        if self.i % self.Size == 0:
            self.refillBuffer()

        if self.i % self.Size < self.size:
            words = [
                x.strip() for x in self.lines[self.i % self.Size].rstrip().split("\t")
            ]

            if len(words) != 12:
                self.i = self.i + 1
                return None

            """shorten the ORF id"""
            words[0] = ShortenORFId(words[0])
            # if  self.opts.algorithm =='LAST':
            if self.needToPermute:
                self.permuteForLAST(words)

            if not words[0] in self.hits_counts:
                self.hits_counts[words[0]] = 0

            if self.hits_counts[words[0]] >= self.opts.limit:
                self.i = self.i + 1
                return None

            if len(words) != 12 or not self.isWithinCutoffs(
                words, self.data, self.opts, self.annot_map, self.refBitScores
            ):
                self.i = self.i + 1
                return None

            self.hits_counts[words[0]] += 1
            self.i = self.i + 1

            try:
                return self.data
            except:
                return None
        else:
            self.blastoutputfile.close()
            raise StopIteration()

    def isWithinCutoffs(self, words, data, cutoffs, annot_map, refbitscores):

        try:
            orfid = ShortORFId(words[0])
        except:
            orfid = words[0]

        data["query"] = orfid

        try:
            data["target"] = words[1]
        except:
            data["target"] = 0

        try:
            data["q_length"] = int(words[7]) - int(words[6]) + 1
        except:
            data["q_length"] = 0

        try:
            data["bitscore"] = float(words[11])
        except:
            data["bitscore"] = 0

        try:
            data["bsr"] = float(words[11]) / refbitscores[orfid]
        except:
            # print "words 0 " + str(refscores[words[0]])
            # print "words 11 " + str( words[11])
            data["bsr"] = 0

        try:
            data["expect"] = float(words[10])
        except:
            data["expect"] = 0

        try:
            data["aln_length"] = float(words[3])
        except:
            data["aln_length"] = 0

        try:
            data["identity"] = float(words[2])
        except:
            data["identity"] = 0

        try:
            data["product"] = annot_map[words[1]]
        except:
            eprintf(
                'Sequence with name "' + words[1] + '" is not present in map file\n'
            )
            if self.error_and_warning_logger:
                self.error_and_warning_logger.write(
                    "Sequence with name %s is not present in map file " % (words[1])
                )
            self.incErrorCount()
            if self.maxErrorsReached():
                if self.error_and_warning_logger:
                    self.error_and_warning_logger.write(
                        "Number of sequence absent in map file %s exceeds %d"
                        % (self.blastoutput, self.ERROR_COUNT)
                    )
                exit_process(
                    "Number of sequence absent in map file %s exceeds %d"
                    % (self.blastoutput, self.ERROR_COUNT)
                )
            data["product"] = "hypothetical protein"

        try:
            m = re.search(r"(\d+[.]\d+[.]\d+[.]\d+)", data["product"])
            if m != None:
                data["ec"] = m.group(0)
            else:
                data["ec"] = ""
        except:
            data["ec"] = ""

        if cutoffs.taxonomy:
            try:
                m = re.search(r"\[([^\[]+)\]", data["product"])
                if m != None:
                    data["taxonomy"] = m.group(1)
                else:
                    data["taxonomy"] = ""
            except:
                data["taxonomy"] = ""

        if cutoffs.remove_taxonomy:
            try:
                data["product"] = re.sub(r"\[([^\[]+)\]", "", data["product"])
            except:
                data["product"] = ""

        if cutoffs.remove_ec:
            try:
                data["product"] = re.sub(
                    r"\([Ee][Ce][:]\d+[.]\d+[.]\d+[.]\d+\)", "", data["product"]
                )
                data["product"] = re.sub(
                    r"\[[Ee][Ce][:]\d+[.]\d+[.]\d+[.]\d+\]", "", data["product"]
                )
                data["product"] = re.sub(
                    r"\[[Ee][Ce][:]\d+[.]\d+[.]\d+[.-]\]", "", data["product"]
                )
                data["product"] = re.sub(
                    r"\[[Ee][Ce][:]\d+[.]\d+[.-.-]\]", "", data["product"]
                )
                data["product"] = re.sub(
                    r"\[[Ee][Ce][:]\d+[.-.-.-]\]", "", data["product"]
                )
            except:
                data["product"] = ""

        if data["q_length"] < cutoffs.min_length:
            return False

        if data["bitscore"] < cutoffs.min_score:
            return False

        if data["expect"] > cutoffs.max_evalue:
            return False

        if data["identity"] < cutoffs.min_identity:
            return False

        if data["bsr"] < cutoffs.min_bsr:
            return False

        # min_length'
        #'min_score'
        #'max_evalue'
        # 'min_identity'
        #'limit'
        #'max_length'
        #'min_query_coverage'
        #'max_gaps'
        # min_bsr'

        return True


# compute the refscores
def process_blastoutput(
    dbname, blastoutput, mapfile, refscore_file, opts, errorlogger=None
):

    blastparser = BlastOutputParser(
        dbname, blastoutput, mapfile, refscore_file, opts, errorlogger=errorlogger
    )

    blastparser.setMaxErrorsLimit(100)
    blastparser.setErrorAndWarningLogger(errorlogger)
    blastparser.setSTEP_NAME("PARSE BLAST")

    fields = [
        "target",
        "q_length",
        "bitscore",
        "bsr",
        "expect",
        "aln_length",
        "identity",
        "ec",
    ]
    if opts.taxonomy:
        fields.append("taxonomy")
    fields.append("product")

    output_blastoutput_parsed = opts.parsed_output

    # temporary file is used to deal with incomplete processing of the file
    output_blastoutput_parsed_tmp = output_blastoutput_parsed + ".tmp"
    try:
        outputfile = open(output_blastoutput_parsed_tmp, "w")
    except:
        if errorlogger:
            errorlogger.write(
                "PARSE_BLAST\tERROR\tCannot open temp file %s to sort\tfor reference db\n"
                % (soutput_blastoutput_parsed_tmp, dbname)
            )
        exit_process(
            "PARSE_BLAST\tERROR\tCannot open temp file %s to sort\tfor reference db\n"
            % (soutput_blastoutput_parsed_tmp, dbname)
        )

    # write the headers out
    fprintf(outputfile, "#%s", "query")
    for field in fields:
        fprintf(outputfile, "\t%s", field)
    fprintf(outputfile, "\n")

    pattern = re.compile(r"" + "(\d+_\d+)$")

    count = 0
    uniques = {}
    for data in blastparser:
        if not data:
            continue
        try:
            fprintf(outputfile, "%s", data["query"])

            result = pattern.search(data["query"])
            if result:
                name = result.group(1)
                uniques[name] = True
        except:
            print("data is : ", data, "\n")
            return count, len(uniques)

        for field in fields:
            fprintf(outputfile, "\t%s", data[field])
        fprintf(outputfile, "\n")
        count += 1

    outputfile.close()
    rename(output_blastoutput_parsed_tmp, output_blastoutput_parsed)

    return count, len(uniques)


# the main function
def main(argv, errorlogger=None, runstatslogger=None):
    global parser
    (opts, args) = parser.parse_args(argv)
    if not check_arguments(opts, args):
        print(sage)
        sys.exit(0)

    if errorlogger:
        errorlogger.write("#STEP\tPARSE_BLAST\n")

    if opts.Lambda == None or opts.k == None:
        if opts.algorithm == "LAST":
            opts.Lambda = 0.300471
            opts.k = 0.103946

        if opts.algorithm == "BLAST":
            opts.Lambda = 0.267
            opts.k = 0.0410

    dictionary = {}
    priority = 5000
    priority1 = 5500
    for dbname, blastoutput, mapfile in zip(
        opts.database_name, opts.input_blastout, opts.database_map
    ):
        temp_refscore = ""
        temp_refscore = opts.refscore_file
        if opts.parsed_output == None:
            opts.parsed_output = blastoutput + ".parsed.txt"

        count, unique_count = process_blastoutput(
            dbname, blastoutput, mapfile, temp_refscore, opts, errorlogger=errorlogger
        )
        if runstatslogger:
            runstatslogger.write(
                "%s\tTotal Protein Annotations %s (%s)\t%s\n"
                % (str(priority), dbname, opts.algorithm, str(count))
            )
            runstatslogger.write(
                "%s\tNumber of ORFs with hits in %s (%s)\t%s\n"
                % (str(priority1), dbname, opts.algorithm, str(unique_count))
            )


def MetaPathways_parse_blast(argv, errorlogger=None, runstatslogger=None):
    createParser()
    try:
        main(argv, errorlogger=errorlogger, runstatslogger=runstatslogger)
    except:
        insert_error(5)
        return (0, "")

    return (0, "")


# the main function of metapaths
if __name__ == "__main__":
    createParser()
    main(sys.argv[1:])
