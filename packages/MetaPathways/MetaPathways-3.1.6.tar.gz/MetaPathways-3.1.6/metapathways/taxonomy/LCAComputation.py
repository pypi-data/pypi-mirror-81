#!/usr/bin/python
from __future__ import division

try:
    import sys
    import traceback
    import re
    import gzip
    import math

    from metapathways.utils.utils import *
    from metapathways.utils.metapathways_utils import (
        fprintf,
        printf,
        GffFileParser,
        getShortORFId,
    )
except:
    print(""" Could not load some user defined  module functions""")
    print(traceback.print_exc(10))
    sys.exit(3)


def copyList(a, b):
    [b.append(x) for x in a]


class LCAComputation:
    begin_pattern = re.compile("#")

    # initialize with the ncbi tree file
    def __init__(self, filenames, megan_map=None):
         # a readable taxon name to numeric string id map as ncbi
        self.name_to_id = {}
        # a readable taxon ncbi tax id to name map
        self.id_to_name = {}
        # this is the tree structure in a id to parent map, you can traverse it to go to the root
        self.taxid_to_ptaxid = {}
    
        self.lca_min_score = 50  # an LCA parameter for min score for a hit to be considered
        self.lca_top_percent = 10  # an LCA param to confine the hits to within the top hits score upto the top_percent%
        self.lca_min_support = (
            5  # a minimum number of reads in the sample to consider a taxon to be present
        )
        self.results_dictionary = None
        self.tax_dbname = "refseq"
        self.megan_map = {}  # hash between NCBI ID and taxonomic name name
        self.accession_to_taxon_map = {}  # hash between gi and taxon name

  
        for filename in filenames:
            filename_ = correct_filename_extension(filename)
            self.loadtreefile(filename)
        if megan_map:
            self.load_megan_map(megan_map)

    def load_megan_map(self, megan_map_file):
        megan_map_file = correct_filename_extension(megan_map_file) 
        with gzip.open(megan_map_file, 'rt') if megan_map_file.endswith('.gz') \
            else open(megan_map_file, 'r') as meganfin:

            for line in meganfin:
                fields = line.split("\t")
                fields = list(map(str.strip, fields))
                self.megan_map[fields[0]] = fields[1]

    def load_accession_to_taxon_map(self, accession_to_taxon_file):
        accession_to_taxon_file = correct_filename_extension(accession_to_taxon_file)
        with gzip.open(accession_to_taxon_file, 'rt') if accession_to_taxon_file.endswith('.gz') \
                else open(accession_to_taxon_file, 'r') as file:
            for line in file:
                fields = line.split("\t")
                fields = map(str.strip, fields)
                self.accession_to_taxon_map[fields[1]] = fields[0]

    def get_preferred_taxonomy(self, ncbi_id):
        ncbi_id = str(ncbi_id)
        if ncbi_id in self.megan_map:
            exp_lin = self.get_lineage(ncbi_id)
            exp_lin.reverse()
            name = ""
            for lid in exp_lin:
                if lid in self.id_to_name:
                    name += self.id_to_name[lid] + ";"

            # decommison old format
            # return self.megan_map[ncbi_id] + " (" + str(ncbi_id) + ")"

            return name + " (" + str(ncbi_id) + ")"
        # think about this
        return None

    def loadtreefile(self, tree_filename):
        tree_filename = correct_filename_extension(tree_filename) 
        with gzip.open(tree_filename, 'rt') if tree_filename.endswith('.gz') \
            else open(tree_filename, 'r') as taxonomy_file:

            lines = taxonomy_file.readlines()
            for line in lines:
                if self.begin_pattern.search(line):
                    continue
                fields = [x.strip() for x in line.rstrip().split("\t")]
                if len(fields) != 3:
                    continue
                if str(fields[0]) not in self.id_to_name:
                    self.name_to_id[str(fields[0])] = str(fields[1])
                self.id_to_name[str(fields[1])] = str(fields[0])
                # the taxid to ptax map has for each taxid a corresponding 3-tuple
                # the first location is the pid, the second is used as a counter for
                # lca while a search is traversed up the tree and the third is used for
                # the min support
                self.taxid_to_ptaxid[str(fields[1])] = [str(fields[2]), 0, 0]

    def setParameters(self, min_score, top_percent, min_support):
        self.lca_min_score = min_score
        self.lca_top_percent = top_percent
        self.lca_min_support = min_support

    def sizeTaxnames(self):
        return len(self.name_to_id)

    def sizeTaxids(self):
        return len(self.taxid_to_ptaxid)

    def get_a_Valid_ID(self, name_group):
        for name in name_group:
            if name in self.name_to_id:
                return self.name_to_id[name]
        return -1

    # given a taxon name it returns the correcponding unique ncbi tax id
    def translateNameToID(self, name):
        if not name in self.name_to_id:
            return None
        return self.name_to_id[name]

    # given a taxon id to taxon name map
    def translateIdToName(self, id):
        if not id in self.id_to_name:
            return None
        return self.id_to_name[id]

    # given a name it returns the parents name
    def getParentName(self, name):
        if not name in self.name_to_id:
            return None
        id = self.name_to_id[name]
        pid = self.getParentTaxId(id)
        return self.translateIdToName(pid)

    # given a ncbi tax id returns the parents tax id
    def getParentTaxId(self, ID):
        if not ID in self.taxid_to_ptaxid:
            return None
        return self.taxid_to_ptaxid[ID][0]

    # given a set of ids it returns the lowest common ancenstor
    # without caring about min support
    # here LCA for a set of ids are computed as follows
    # first we consider one ID at a time
    #   for each id we traverse up the ncbi tree using the id to parent id map
    #   at the same time increasing the count on the second value of the 3-tuple
    #   note that at the node where all the of the individual ids ( limit in number)
    #   converges the counter matches the limit for the first time, while climbing up.
    #   This also this enables us to  make the selection of id arbitrary
    def get_lca(self, IDs, return_id=False):
        limit = len(IDs)
        for id in IDs:
            tid = id
            while tid in self.taxid_to_ptaxid and tid != "1":
                self.taxid_to_ptaxid[tid][1] += 1
                if self.taxid_to_ptaxid[tid][1] == limit:
                    if return_id:
                        return tid
                    else:
                        return self.id_to_name[tid]
                tid = self.taxid_to_ptaxid[tid][0]
        if return_id:
            return 1
        return "root"

    def update_taxon_support_count(self, taxonomy):
        id = self.get_a_Valid_ID([taxonomy])
        tid = id
        while tid in self.taxid_to_ptaxid and tid != "1":
            self.taxid_to_ptaxid[tid][2] += 1
            tid = self.taxid_to_ptaxid[tid][0]

    def get_supported_taxon(self, taxonomy, return_id=False):
        id = self.get_a_Valid_ID([taxonomy])
        tid = id
        # i =0
        while tid in self.taxid_to_ptaxid and tid != "1":
            # print   str(i) + ' ' + self.translateIdToName(tid)
            if self.lca_min_support > self.taxid_to_ptaxid[tid][2]:
                tid = self.taxid_to_ptaxid[tid][0]
            else:
                if return_id:
                    return tid
                else:
                    return self.translateIdToName(tid)
                # i+=1
        if return_id:
            return tid
        else:
            return self.translateIdToName(tid)

    # need to call this to clear the counts of reads at every node
    def clear_cells(self, IDs):
        limit = len(IDs)
        for id in IDs:
            tid = id
            while tid in self.taxid_to_ptaxid and tid != "1":
                # if self.taxid_to_ptaxid[tid][1]==0:
                #   return  self.id_to_name[tid]
                self.taxid_to_ptaxid[tid][1] = 0
                tid = self.taxid_to_ptaxid[tid][0]
        return ""

    # given a set of sets of names it computes an lca
    # in the format [ [name1, name2], [name3, name4,....namex] ...]
    # here name1 and name2 are synonyms and so are name3 through namex
    def getTaxonomy(self, name_groups, return_id=False):
        IDs = []
        for name_group in name_groups:
            id = self.get_a_Valid_ID(name_group)
            if id != -1:
                IDs.append(id)
        consensus = self.get_lca(IDs, return_id)
        self.clear_cells(IDs)

        return consensus

    # extracts taxon names for a refseq annotation
    def get_species(self, hit):
        accession_PATT = re.compile(r"ref\|(.*)\|")
        if not "product" in hit and not "target" in hit:
            return None

        species = []

        try:
            # extracting taxon names here
            # if 'target' in hit:
            #   gires = accession_PATT.search(hit['target'])
            #   if gires:
            #      gi = gires.group(1)
            #      if gi in self.accession_to_taxon_map:
            #        species.append(self.accession_to_taxon_map[gi])
            # else:
            m = re.findall(r"\[([^\[]+?)\]", hit["product"])
            if m != None:
                copyList(m, species)
                # print hit['product']
                # print species
        except:
            return None

        if species and species != "":
            return species
        else:
            return None

    # used for optimization
    def set_results_dictionary(self, results_dictionary):
        self.results_dictionary = results_dictionary

    # this returns the megan taxonomy, i.e., it computes the lca but at the same time
    # takes into consideration the parameters, min score, min support and top percent
    def getMeganTaxonomy(self, orfid):
        # compute the top hit wrt score
        names = []
        species = []
        if self.tax_dbname in self.results_dictionary:
            if orfid in self.results_dictionary[self.tax_dbname]:

                top_score = 0
                for hit in self.results_dictionary[self.tax_dbname][orfid]:
                    if (
                        hit["bitscore"] >= self.lca_min_score
                        and hit["bitscore"] >= top_score
                    ):
                        top_score = hit["bitscore"]

                for hit in self.results_dictionary[self.tax_dbname][orfid]:
                    if (100 - self.lca_top_percent) * top_score / 100 < hit["bitscore"]:
                        names = self.get_species(hit)
                        if names:
                            species.append(names)

        taxonomy = self.getTaxonomy(species)
        meganTaxonomy = self.get_supported_taxon(taxonomy)
        return meganTaxonomy

    # this is use to compute the min support for each taxon in the tree
    # this is called before the  getMeganTaxonomy
    def compute_min_support_tree(self, annotate_gff_file, pickorfs, dbname="refseq"):
        # print 'dbname' , dbname
        self.tax_dbname = dbname
        gffreader = GffFileParser(annotate_gff_file)
        # print 'done'
        try:
            #   if dbname=='refseq-nr-2014-01-18':
            #       print  'refseq', len(pickorfs)
            for contig in gffreader:
                # if dbname=='refseq-nr-2014-01-18':
                #    print  'refseq',  contig
                for orf in gffreader.orf_dictionary[contig]:
                    shortORFId = getShortORFId(orf["id"])
                    if re.search(r"Xrefseq", dbname):
                        print("refseq", contig, shortORFId, self.tax_dbname)

                    # print shortORFId, orf['id']

                    if not shortORFId in pickorfs:
                        continue
                    #           if dbname=='refseq-nr-2014-01-18':
                    #              print  'refseq',  contig , shortORFId
                    # print ">", shortORFId, orf['id']

                    taxonomy = None
                    species = []

                    if self.tax_dbname in self.results_dictionary:
                        if re.search(r"Xrefseq", dbname):
                            print("hit", len(self.results_dictionary[self.tax_dbname]))
                            print(self.results_dictionary[self.tax_dbname].keys())

                        if shortORFId in self.results_dictionary[self.tax_dbname]:
                            # compute the top hit wrt score
                            top_score = 0
                            for hit in self.results_dictionary[self.tax_dbname][
                                shortORFId
                            ]:
                                # print hit #,hit['bitscore'], self.lca_min_score, top_score

                                if (
                                    hit["bitscore"] >= self.lca_min_score
                                    and hit["bitscore"] >= top_score
                                ):
                                    top_score = hit["bitscore"]
                            #                       if dbname=='refseq-nr-2014-01-18':
                            #                            print  'hit',  hit

                            for hit in self.results_dictionary[self.tax_dbname][
                                shortORFId
                            ]:
                                if (100 - self.lca_top_percent) * top_score / 100 < hit[
                                    "bitscore"
                                ]:
                                    names = self.get_species(hit)
                                    if names:
                                        species.append(names)
                            # print self.results_dictionary[dbname][shortORFId][0]['product']
                            # print  orf['id']
                            # print  orf['id'], species
                            # print  orf['id'], len(self.results_dictionary[dbname][shortORFId]), species
                    taxonomy = self.getTaxonomy(species)
                    # taxonomy_id = self.getTaxonomy(species, return_id=True)
                    # print taxonomy
                    # print taxonomy_id
                    # print taxonomy,  orf['id'], species
                    self.update_taxon_support_count(taxonomy)
                    # preferred_taxonomy = self.get_preferred_taxonomy(taxonomy_id)
                    # print taxonomy
                    # print preferred_taxonomy
                    pickorfs[shortORFId] = taxonomy

        except:
            import traceback

            traceback.print_exc()
            print("ERROR : Cannot read annotated gff file ")

    ## Weighted Taxonomic Distnace (WTD)
    # Implementation of the weighted taxonomic distance as described in
    # Metabolic pathways for the whole community. Hanson et al. (2014)

    # monotonicly decreasing function of depth of divergence d
    def step_cost(self, d):
        return 1 / math.pow(2, d)

    # weighted taxonomic distance between observed and expected taxa
    def wtd(self, exp, obs):
        exp_id = exp
        obs_id = obs
        exp_lin = self.get_lineage(exp_id)
        obs_lin = self.get_lineage(obs_id)
        sign = -1

        # check to see if expected in observed lineage
        # if so distance sign is positive
        if exp_id in obs_lin:
            sign = 1
        large = None
        if len(obs_lin) <= len(exp_lin):
            # expected longer than observed
            large = exp_lin
            small = obs_lin
        else:
            large = obs_lin
            small = exp_lin

        # calculate cost
        a_cost = 0
        b_cost = 0
        for i in range(len(large)):
            if i > 0:
                a_cost += self.step_cost(len(large) - i - 1)
            b_cost = 0
            for j in range(len(small)):
                if j > 0:
                    b_cost += self.step_cost(len(small) - j - 1)
                if large[i] == small[j]:
                    return (a_cost + b_cost) * sign
        return None  # did not find lineages

    # given an ID gets the lineage
    def get_lineage(self, id):
        tid = str(id)
        lineage = []
        lineage.append(tid)
        while tid in self.taxid_to_ptaxid and tid != "1":
            lineage.append(self.taxid_to_ptaxid[tid][0])
            tid = self.taxid_to_ptaxid[tid][0]
        return lineage
