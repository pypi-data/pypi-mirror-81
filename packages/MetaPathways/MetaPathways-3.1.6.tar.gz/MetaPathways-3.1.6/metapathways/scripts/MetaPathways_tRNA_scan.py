#!/usr/bin/python
"""This script run the orf prediction """

__author__ = "Kishori M Konwar"
__copyright__ = "Copyright 2020, MetaPathways"
__version__ = "3.5.0"
__maintainer__ = "Kishori M Konwar"
__status__ = "Release"
try:
    import sys, re, csv, traceback
    from os import path, _exit
    import logging.handlers

    from optparse import OptionParser, OptionGroup

    from metapathways.utils.sysutil import pathDelim
    from metapathways.utils.metapathways_utils import (
        fprintf,
        printf,
        eprintf,
        exit_process,
    )
    from metapathways.utils.sysutil import getstatusoutput

    from metapathways.utils.pathwaytoolsutils import *
    from metapathways.utils.errorcodes import (
        error_message,
        get_error_list,
        insert_error,
    )

except:
    print(""" Could not load some user defined  module functions""")
    sys.exit(3)

PATHDELIM = pathDelim()
errorcode = 7


def fprintf(file, fmt, *args):
    file.write(fmt % args)


def printf(fmt, *args):
    sys.stdout.write(fmt % args)


def files_exist(files, errorlogger=None):
    status = True
    for file in files:
        if not path.exists(file):
            if errorlogger:
                errorlogger.write("ERROR\tCould not find ptools input  file : " + file)
            status = False
    return not status


help = sys.argv[0] + """ -i input -o output [algorithm dependent options]"""

parser = None


def createParser():
    global parser
    epilog = """This script is used for scanning for tRNA,  using tRNA-Scan 1.4, 
              on the set of metagenomics sample sequences """
    epilog = re.sub(r"\s+", " ", epilog)

    parser = OptionParser(usage=help, epilog=epilog)

    # Input options

    parser.add_option(
        "-o",
        dest="trna_o",
        default=None,
        help="Output from the tRNA-Scan 1.4 into <outfile>",
    )

    parser.add_option(
        "-i", dest="trna_i", default=None, help="reads the sequences from <input> file"
    )

    parser.add_option(
        "-T", dest="trna_T", default="6", help="reads the Tsignal from <TPCsignal>"
    )

    parser.add_option(
        "-D", dest="trna_D", default=None, help="reads the Dsignal from <Dsignal>"
    )

    parser.add_option(
        "-F",
        dest="trna_F",
        default=None,
        help="write predicted tRNA genes in fasta format<outfile>",
    )

    parser.add_option(
        "--executable",
        dest="trna_executable",
        default=None,
        help="The tRNA-SCAN 1.4 executable",
    )


def main(argv, errorlogger=None, runcommand=None, runstatslogger=None):
    global parser
    options, args = parser.parse_args(argv)
    return _execute_tRNA_Scan(options)


def _execute_tRNA_Scan(options):
    global errorcode
    args = []

    if options.trna_executable:
        args.append(options.trna_executable)

    if options.trna_i:
        args += ["-i", options.trna_i]

    if options.trna_o:
        args += ["-o", options.trna_o]

    if options.trna_D:
        args += ["-D", options.trna_D]

    if options.trna_T:
        args += ["-T", options.trna_T]

    if options.trna_F:
        args += ["-F", options.trna_F]
    result = getstatusoutput(" ".join(args))

    if result[0] != 0:
        insert_error(errorcode)
    return result


def MetaPathways_tRNA_scan(
    argv, extra_command=None, errorlogger=None, runstatslogger=None
):
    global errorcode
    if errorlogger != None:
        errorlogger.write("#STEP\ttRNA_SCAN\n")
    createParser()
    result = [0, ""]
    try:
        result = main(
            argv,
            errorlogger=errorlogger,
            runcommand=extra_command,
            runstatslogger=runstatslogger,
        )
    except:
        insert_error(errorcode)
        return (res[0], res[1])

    return (result[0], "")


if __name__ == "__main__":
    createParser()
    result = main(sys.argv[1:])
