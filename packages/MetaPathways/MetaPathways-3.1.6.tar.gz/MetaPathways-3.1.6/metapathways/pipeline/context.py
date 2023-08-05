#!/usr/bin/env python

__author__ = "Kishori M Konwar"
__copyright__ = "Copyright 2013, MetaPathways"
__credits__ = ["r"]
__version__ = "1.0"
__maintainer__ = "Kishori M Konwar"
__status__ = "Release"


"""Contains general utility code for the metapaths project"""

try:
    import os, re
    from shutil import rmtree
    from optparse import make_option
    from os import path, _exit, remove
    from metapathways.utils.utils import *
except:
    print("Cannot load some modules")
    sys.exit(0)

PATHDELIM = pathDelim()


class Context:
    """ This class holds the context of a stage """

    def __init__(self):
        self.outputs = {}
        self.outputs1 = {}
        self.inputs = {}
        self.inputs1 = {}
        self.name = None
        self.status = None
        self.commands = []
        self.message = "Message not set"
        pass

    def isOutputAvailable(self):
        return doFilesExist(self.outputs.values(), gz=True)

    def isInputAvailable(self, errorlogger=None):
        status = True
        for file in self.inputs.values():
            if not doesFileExist(file) and not doesFileExist(file + ".gz"):
                if errorlogger != None:
                    errorlogger.printf("#STEP\t%s\n", self.name)
                    errorlogger.printf("ERROR\tMissing input %s\n", file)
                status = False
        return status

    def getMissingList(self, errorlogger=None):
        missingList = []
        status = True
        for file in self.inputs.values():
            if not doesFileExist(file):
                missingList.append(file)
                if errorlogger != None:
                    errorlogger.printf("ERROR\tMissing input %s\n", file)
                status = False
        return missingList

    def removeOutput(self, errorlogger=None):
        annotationPATT = re.compile(r"annotation_table")
        for item in self.outputs.values():
            if not path.exists(item):
                continue

            if path.isdir(item):
                if annotationPATT.search(item):
                    pass
                else:
                    rmtree(item)
            else:
                remove(item)
