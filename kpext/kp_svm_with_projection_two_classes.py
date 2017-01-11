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

        train_projection_class_process = []
        train_projection_class_task = []
        train_projection_class_material = []
        train_projection_class_none = []
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
                        train_projection = kpc.get_document_content_ann(dirname, current_filename + "clss")
                        for projection in train_projection:
                            projection_type = projection[1].split(" ")[0]
                            if projection_type == "Process":
                                train_projection_class_process.append(projection[2])
                            if projection_type == "Task":
                                train_projection_class_task.append(projection[2])
                            if projection_type == "Material":
                                train_projection_class_material.append(projection[2])
                            if projection_type == "None":
                                train_projection_class_none.append(projection[2])
                    except:
                        print >> sys.stderr, "E) Open files: ", sys.exc_info()
                else:
                    continue
        D = {}
        process_class = "KeyPhrase"
        task_class = "KeyPhrase"
        material_class = "KeyPhrase"
        none_class = "None"
        D[process_class] = kpc.tf_normalized(train_projection_class_process + train_projection_class_task + train_projection_class_material)
        #D[process_class] = kpc.tf_normalized(train_projection_class_process)
        #D[task_class] = kpc.tf_normalized(train_projection_class_task)
        #D[material_class] = kpc.tf_normalized(train_projection_class_material)
        D[none_class] = kpc.tf_normalized(train_projection_class_none)
        V_norm_2 = {}
        V = set()
        for d in D:
            V = V.union(D[d].keys())
            V_norm_2[d] = kpc.norm(D[d])
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
                        _V = V.copy()
                        similarity = {}
                        test_kp = cur_kp[2].split(" ")
                        D["test_kp"] = kpc.tf_normalized(test_kp)
                        _V = _V.union(D["test_kp"].keys()) 
                        t_idf = kpc.idf(_V, D, N)
                        tf_idf = kpc.tf_idf(D, t_idf)
                        Vtest_norm_2 = kpc.norm(tf_idf["test_kp"])
                        print tf_idf["test_kp"]
                        tf_idf_kps[cur_kp[2]] = Vtest_norm_2

                        similarity[process_class] = kpc.v1_dot_v2(tf_idf["test_kp"], tf_idf[process_class])/(Vtest_norm_2*V_norm_2[process_class])
                        #similarity[task_class] = kpc.v1_dot_v2(tf_idf["test_kp"], tf_idf[task_class])/(Vtest_norm_2*V_norm_2[task_class])
                        #similarity[material_class] = kpc.v1_dot_v2(tf_idf["test_kp"], tf_idf[material_class])/(Vtest_norm_2*V_norm_2[material_class])
                        similarity[none_class] = kpc.v1_dot_v2(tf_idf["test_kp"], tf_idf[none_class])/(Vtest_norm_2*V_norm_2[none_class])
                        kp_type = max(similarity.items(), key=operator.itemgetter(1))
                        print cur_kp[2], kp_type, Vtest_norm_2
                        if kp_type[0] != none_class and kp_type[1] > 0.0:
                            #kpe_string = "\t".join( cur_kp[0:1] + [" ".join([kp_type[0]] + cur_kp[1].split(" ")[1:])] + cur_kp[2:])
                            #print >> stream_output, kpe_string.encode("utf-8")
                            keyphrase_extractions.append([cur_kp[0:1] + [" ".join([kp_type[0]] + cur_kp[1].split(" ")[1:])] + cur_kp[2:] , 
                                similarity[none_class], Vtest_norm_2])

                    keyphrase_extractions = sorted(keyphrase_extractions, key = operator.itemgetter(2), reverse=True)
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
