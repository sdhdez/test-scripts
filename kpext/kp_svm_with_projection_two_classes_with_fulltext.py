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
import numpy as np

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

        keyphrase_class = "KeyPhrase"
        none_class = "None"
        train_projection_classes = {}
        train_projection_classes[keyphrase_class] = {}
        train_projection_classes[none_class] = {}
        train_max_anntoken_occurrence = 0
        corpus = []
        Dnames = []
        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-3:]
                current_filename = f[:-4]
                if ext == 'ann':
                    file_count += 1 #debug
                    if debug and file_count > debug_tests: #debug
                        break #debug
                    print >> sys.stderr, file_count, f[:-4]
                    try:
                        train_doc = kpc.get_document_content(dirname, current_filename, extensions = [".fll.abs", ".fll.ttl", ".fll.text"])
                        corpus.append(" ".join(train_doc))
                        Dnames.append(current_filename)
                        train_projection = kpc.get_document_content_ann(dirname, current_filename + ".clss")
                    except:
                        print >> sys.stderr, "E) Open training files: ", sys.exc_info()
                        print len(train_doc), len(train_projection)

                    try:
                        for projection in train_projection:
                            projection_type = projection[1].split(" ")[0]
                            projection_tokens = kpc.my_tokenizer2(projection[2])
                            for pt in projection_tokens:
                                if projection_type == none_class:
                                    train_projection_classes[none_class].setdefault(pt, 0.0)
                                    train_projection_classes[none_class][pt] += 1.0
                                    if train_max_anntoken_occurrence < train_projection_classes[none_class][pt]:
                                        train_max_anntoken_occurrence = train_projection_classes[none_class][pt]
                                else:
                                    train_projection_classes[keyphrase_class].setdefault(pt, 0.0)
                                    train_projection_classes[keyphrase_class][pt] += 1
                                    if train_max_anntoken_occurrence < train_projection_classes[keyphrase_class][pt]:
                                        train_max_anntoken_occurrence = train_projection_classes[keyphrase_class][pt]
                    except:
                        print >> sys.stderr, "E) Forming classes: ", sys.exc_info()


                else:
                    continue
        Dcount = len(Dnames)
        file_count = 0
        for (dirname, _, filenames) in os.walk(dir_test):
            for f in filenames:
                ext = f[-3:]
                current_filename = f[:-4]
                if ext == 'ann':
                    file_count += 1 #debug
                    if debug and file_count > debug_tests: #debug
                        break #debug
                    print >> sys.stderr, "Test: ", file_count, f[:-4], min_similarity
                    shorttext_content = kpc.get_document_content(dirname, current_filename + ".txt")
                    tmp_corpus = copy.copy(corpus)
                    tmp_corpus += shorttext_content
                    if debug:
                        for i, cor in enumerate(tmp_corpus):
                            print cor[0:10] + "..."
                    vectorizer = TfidfVectorizer(min_df=0, analyzer=kpc.my_tokenizer2)
                    tfidf = vectorizer.fit_transform(tmp_corpus)
                    vocabulary_len = len(vectorizer.vocabulary_)
                    print "tf-idf ...", tfidf.shape

                    V_centroid = scipy.sparse.dok_matrix((1, vocabulary_len), dtype=np.float128)
                    for d in tfidf:
                        V_centroid += d
                    V_centroid /= (Dcount + 1)
                    print "Centroid ...", V_centroid.shape
                    try:
                        class_vectors = {}
                        for class_name in train_projection_classes:
                            class_vectors[class_name] = scipy.sparse.dok_matrix((1, vocabulary_len), dtype=np.float128)
                            #print " Class", class_name
                            for term_in_class in train_projection_classes[class_name]:
                                term_occurrences = train_projection_classes[class_name][term_in_class]
                                term_id = vectorizer.vocabulary_.get(term_in_class)
                                if term_id:
                                    #print V_centroid[0, term_id]*(term_occurrences/train_max_anntoken_occurrence)
                                    class_vectors[class_name][0, term_id] = V_centroid[0, term_id]*(term_occurrences/train_max_anntoken_occurrence)
                    except:
                        print >> sys.stderr, "E) Getting class features: ", sys.exc_info(), vocabulary_len, term_in_class, term_occurrences, term_id
                        sys.exit(1)

                    keyphrase_extractions = []
                    ann_content = kpc.get_document_content_ann(dirname, current_filename + ".ann")
                    ann_count = 0
                    for annotation in ann_content:
                        if debug and ann_count > debug_tests: #debug
                            break #debug
                        ann_count += 1
                        ann_tokens = kpc.my_tokenizer2(annotation[2])
                        ann_vector = scipy.sparse.dok_matrix((1, vocabulary_len), dtype=np.float128)
                        for token in ann_tokens:
                            term_id = vectorizer.vocabulary_.get(token)
                            if term_id:
                                ann_vector[0, term_id] = V_centroid[0, term_id]
                        similarity = dict(zip(  [none_class, keyphrase_class],  
                                                [cosine_similarity(ann_vector, class_vectors[none_class])[0][0], 
                                                    cosine_similarity(ann_vector, class_vectors[keyphrase_class])[0][0] ]))
                        #print "Similarity", similarity
                        kp_type = max(similarity.items(), key=operator.itemgetter(1))
                        #if similarity[none_class] > 0.0:
                        #    print "None:", ann_tokens, similarity
                        #    continue 
                        #elif kp_type[0] != none_class or kp_type[1] == min_similarity:
                        print "KP:", ann_tokens, similarity
                        if kp_type[0] != none_class and kp_type[1] > min_similarity:
                            keyphrase_extractions.append(
                                        [annotation[0:1] + [" ".join([kp_type[0]] + annotation[1].split(" ")[1:])] + annotation[2:] , 
                                        similarity[none_class]]
                                    )
                    
                    keyphrase_extractions = sorted(keyphrase_extractions, key = operator.itemgetter(1))
                    file_output = os.path.join(dir_output, current_filename + ".ann")
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
