#!/usr/bin/python 
import sys
import os
import operator
import mdb_common_lib as mdbcl
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
from nltk.tag.perceptron import PerceptronTagger
import nltk.data
import re
import math
import kpcommon as kpc 

from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

if __name__ == "__main__":
    try:
        debug = True if sys.argv[-1] == "debug" else False
        debug_tests = 3
        file_count = 0
        try:
            dir_corpus = sys.argv[1]
            dir_test = sys.argv[2]
            dir_output = sys.argv[3]
        except:
            print >> sys.stderr, "E) Directories: ", sys.exc_info()

        D = {}
        V = {}
        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-3:]
                current_filename = f[:-3]
                if ext == 'ann':
                    file_count += 1 #debug
                    if debug and file_count > debug_tests: #debug
                        break #debug
                    print >> sys.stderr, file_count, f[:-4]
                    try:
                        dfull_content = kpc.get_document_content(dirname, current_filename, extensions = ["fll.abs", "fll.ttl", "fll.text"])
                    except:
                        print >> sys.stderr, "E) Open files: ", sys.exc_info()
                    D[current_filename] = kpc.tf_normalized(dfull_content)
                    V.update(D[current_filename])
                else:
                    continue

        """
        N = file_count
        tf_idf_0, t_idf = kpc.idf(V, D, N)
        tf_idf = kpc.tf_idf(D, t_idf)
        if debug:
            for d in tf_idf:
                print "---", d
                for t in sorted(tf_idf[d].items(), key=operator.itemgetter(1)):
                    print "   +++", t
        """

        N = file_count + 1 # includes the keyphrase to test
        file_count = 0

        for (dirname, _, filenames) in os.walk(dir_test):
            for f in filenames:
                ext = f[-3:]
                current_filename = f
                if ext == 'ann':
                    file_count += 1 #debug
                    if debug and file_count > debug_tests: #debug
                        break #debug
                    print >> sys.stderr, "Test: ", file_count, f[:-4]
                    ann_content = kpc.get_document_content_ann(dirname, current_filename)
                    keyphrase_extractions = []
                    tf_idf_kps = {}
                    for cur_kp in ann_content:
                        if cur_kp[2] in tf_idf_kps:
                            norm_2 = tf_idf_kps[cur_kp[2]]
                        else:
                            D["cur_kp"] = kpc.tf_normalized(cur_kp[2].split(" "))
                            _V = V.copy()
                            for Dckp in D["cur_kp"]:
                                _V[Dckp] = 1.0
                            tf_idf_0, t_idf = kpc.idf(_V, D, N)
                            tf_idf = kpc.tf_idf(D, t_idf)
                            sum_tf_idf = 0.0
                            for term_kp in tf_idf["cur_kp"]:
                                sum_tf_idf += math.pow(tf_idf["cur_kp"][term_kp], 2)
                            norm_2 = math.sqrt(sum_tf_idf)
                            tf_idf_kps[cur_kp[2]] = norm_2
                        keyphrase_extractions.append([cur_kp, norm_2])

                    keyphrase_extractions = sorted(keyphrase_extractions, key = operator.itemgetter(1), reverse = True)
                    file_output = os.path.join(dir_output, current_filename)
                    stream_output = open(file_output, "w")
                    kp_count = 0
                    for kpe in keyphrase_extractions:
                        if kpe[1] > 0:
                            kp_count += 1
                            kpe_string = "\t".join(["T" + str(kp_count)] + kpe[0][1:])
                            print >> stream_output, kpe_string.encode("utf-8")
                    stream_output.close()
                else:
                    continue

    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
