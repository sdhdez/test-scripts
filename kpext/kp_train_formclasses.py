#!/usr/bin/python 
import sys
import os
import mdb_common_lib as mdbcl
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
from nltk.tag.perceptron import PerceptronTagger
import nltk.data
import re
import kpcommon

from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

if __name__ == "__main__":
    try:
        debug = True if sys.argv[-1] == "debug" else False
        debug_tests = 1
        file_count = 0

        try:
            dir_corpus = sys.argv[1]
            dir_projection = sys.argv[2]
            dir_output = sys.argv[3]
        except:
            print >> sys.stderr, "E) Directories: ", sys.exc_info()
       
        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-3:]
                if ext == 'ann':
                    file_count += 1 #debug
                    if debug and file_count > debug_tests: #debug
                        break #debug
                    print file_count, f[:-4]
                    try:
                        filename_ann = os.path.join(dirname, f[:-3] + "ann")
                        ann_file = open(filename_ann, "r")
                        filename_proj = os.path.join(dir_projection, f[:-3] + "ann")
                        proj_file = open(filename_proj, "r")
                        filename_output_clss = os.path.join(dir_output, f[:-3] + "clss")
                        clss_file = open(filename_output_clss, "w")
                    except:
                        print >> sys.stderr, "E) Open files: ", sys.exc_info()
                    annotanted_keyphrases = {}
                    for ann in ann_file:
                        ann = unicode(ann, encoding="utf-8")
                        if ann[0] not in ["R", "*"]:
                            ann_items = ann.strip().split("\t")
                            if ann_items[1].find(";") >= 0:
                                type_indexes_tmp = ann_items[1].split(" ")
                                type_indexes = type_indexes_tmp[0:2] + type_indexes_tmp[3:]
                            else:
                                type_indexes = ann_items[1].split(" ")
                            start_ann = int(type_indexes[1])
                            end_ann = int(type_indexes[2])
                            annotanted_keyphrases.setdefault(start_ann, {})
                            annotanted_keyphrases[start_ann].setdefault(end_ann, [])
                            annotanted_keyphrases[start_ann][end_ann].append(ann_items)
                    ann_file.close()
                    projected_keyphrases = {}
                    for ann in proj_file:
                        ann = unicode(ann, encoding="utf-8")
                        if ann[0] not in ["R", "*"]:
                            ann_items = ann.strip().split("\t")
                            if ann_items[1].find(";") >= 0:
                                type_indexes_tmp = ann_items[1].split(" ")
                                type_indexes = type_indexes_tmp[0:2] + type_indexes_tmp[3:]
                            else:
                                type_indexes = ann_items[1].split(" ")
                            start_ann = int(type_indexes[1])
                            end_ann = int(type_indexes[2])
                            projected_keyphrases.setdefault(start_ann, {})
                            projected_keyphrases[start_ann].setdefault(end_ann, [])
                            projected_keyphrases[start_ann][end_ann].append(ann_items)
                    proj_file.close()

                    kp_count = 0
                    kp_labeled = []
                    for prj_start in projected_keyphrases:
                        for prj_end in projected_keyphrases[prj_start]:
                            for prj_kp in projected_keyphrases[prj_start][prj_end]:
                                if prj_start in annotanted_keyphrases:
                                    if prj_end in annotanted_keyphrases[prj_start]:
                                        for ann_kp in annotanted_keyphrases[prj_start][prj_end]:
                                            prj_kp[1] = ann_kp[1]
                                            kp_count += 1
                                            kpcommon.print_to_ann(clss_file, (u"T" + str(kp_count)).encode("utf-8"), prj_kp[1].encode("utf-8"), prj_kp[2].encode("utf-8"))
                                    else:
                                        kp_count += 1
                                        kpcommon.print_to_ann(clss_file, (u"T" + str(kp_count)).encode("utf-8"), prj_kp[1].encode("utf-8"), prj_kp[2].encode("utf-8"))
                else:
                    continue
    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
