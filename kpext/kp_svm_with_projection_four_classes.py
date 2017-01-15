#!/usr/bin/python 
import sys
import os
import re
import copy
import operator
import math
import kpcommon as kpc 
import mdb_common_lib as mdbcl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse
import numpy

if __name__ == "__main__":
    try:
        debug = True if sys.argv[-1] == "debug" else False
        debug_tests = 3
        file_count = 0
        try:
            dir_corpus = sys.argv[1]
            dir_test = sys.argv[2]
            dir_output = sys.argv[3]
            min_similarity = float(sys.argv[4])
        except:
            print >> sys.stderr, "E) Directories: ", sys.exc_info()

        process_class = "Process"
        task_class = "Task"
        material_class = "Material"
        none_class = "None"
        train_projection_classes = {}
        train_projection_classes[process_class] = []
        train_projection_classes[task_class] = []
        train_projection_classes[material_class] = []
        train_projection_classes[none_class] = []
        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-4:]
                current_filename = f[:-4]
                if ext == '.ann':
                    file_count += 1 #debug
                    if debug and file_count > debug_tests: #debug
                        break #debug
                    print >> sys.stderr, file_count, f[:-4]
                    try:
                        train_projection = kpc.get_document_content_ann(dirname, current_filename + ".clss")
                        for projection in train_projection:
                            projection_type = projection[1].split(" ")[0]
                            tokenized_projection = " ".join(kpc.my_tokenizer2(projection[2]))
                            if projection_type == process_class:
                                train_projection_classes[process_class].append(tokenized_projection)
                            if projection_type == task_class:
                                train_projection_classes[task_class].append(tokenized_projection)
                            if projection_type == material_class:
                                train_projection_classes[material_class].append(tokenized_projection)
                            if projection_type == none_class:
                                train_projection_classes[none_class].append(tokenized_projection)

                    except:
                        print >> sys.stderr, "E) Open files: ", sys.exc_info()
                else:
                    continue
        corpus = []
        Dnames = []
        for tpc in train_projection_classes:
            Dnames.append(tpc)
            corpus.append(" ".join(train_projection_classes[tpc]))

        file_count = 0
        for (dirname, _, filenames) in os.walk(dir_test):
            for f in filenames:
                ext = f[-4:]
                current_filename = f
                if ext == '.ann':
                    file_count += 1 #debug
                    if debug and file_count > debug_tests: #debug
                        break #debug
                    print >> sys.stderr, "Test: ", file_count, f[:-4], min_similarity
                    ann_content = kpc.get_document_content_ann(dirname, current_filename)
                    #print ann_content
                    keyphrase_extractions = []
                    for annotation in ann_content:
                        tmp_corpus = copy.copy(corpus)
                        tmp_corpus.append(" ".join(kpc.my_tokenizer2(annotation[2])))
                        vectorizer = TfidfVectorizer(min_df=0, analyzer=kpc.my_features)
                        tfidf = vectorizer.fit_transform(tmp_corpus)
                        tfidf_test = tfidf[-1:]
                        similarity = dict(zip(Dnames, cosine_similarity(tfidf_test, tfidf[:-1]).flatten()))
                        kp_type = max(similarity.items(), key=operator.itemgetter(1))
                        #print annotation[2], kp_type
                        if kp_type[0] != none_class and kp_type[1] > min_similarity:
                            keyphrase_extractions.append([annotation[0:1] + [" ".join([kp_type[0]] + annotation[1].split(" ")[1:])] + annotation[2:] , 
                                similarity[none_class]])

                    keyphrase_extractions = sorted(keyphrase_extractions, key = operator.itemgetter(1))
                    file_output = os.path.join(dir_output, current_filename)
                    stream_output = open(file_output, "w")
                    kp_count = 0
                    for kpe in keyphrase_extractions:
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
