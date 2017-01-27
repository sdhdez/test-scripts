#!/usr/bin/python 
import sys
import os
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
from nltk.tag.perceptron import PerceptronTagger
import operator
from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite
import re
import kpcommon as kpc 

if __name__ == "__main__":
    try:
        debug = True if sys.argv[-1] == "debug" else False
        debug_tests = 3
        file_count = 0

        dir_corpus = sys.argv[1]       
        dir_output = sys.argv[2]
        try:
            training_crfsuite = sys.argv[3]
        except:
            training_crfsuite = 'keyphrase_projection'

        tokenizer = Tokenizer()
        #pos
        tagger = PerceptronTagger()

        crfsuite_training_types = []
        for ctc in ['Process', 'Task', 'Material']:
            crfsuite_training_types.append('keyphrase_projection.' + ctc + '.crfsuite')

        crftagger0 = pycrfsuite.Tagger()
        crftagger0.open(crfsuite_training_types[0])

        crftagger1 = pycrfsuite.Tagger()
        crftagger1.open(crfsuite_training_types[1])

        crftagger2 = pycrfsuite.Tagger()
        crftagger2.open(crfsuite_training_types[2])


        #test_sents = []
        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-4:]
                if ext == '.ann':
                    file_count += 1
                    if debug and file_count > debug_tests:
                        break
                    
                    file_text = os.path.join(dirname, f[:-4] + ".txt")
                    text_file = open(file_text, "r")
                    raw_text = unicode(text_file.read(), encoding="utf-8")

                    file_kpe = os.path.join(dir_output, f[:-4] + ".ann")
                    kpe_file = open(file_kpe, "w")

                    kp_list = []
                    projections_list = kpc.get_document_content_ann(dirname, f[:-4] + ".ann")
                    for projection in projections_list:

                        index_list = projection[1].split()
                        start = int(index_list[1])
                        end = int(index_list[2])
                        prev_token = False

                        if start > 0:
                            prev_text = raw_text[0:start]
                            prev_text_tokens = tokenizer.tokenize(prev_text)
                            if prev_text_tokens:
                                prev_token = prev_text_tokens[-1]
                            else:
                                prev_token = False

                        next_text = raw_text[end:]
                        next_text_tokens = tokenizer.tokenize(next_text)
                        if next_text_tokens:
                            next_token = next_text_tokens[0]
                        else:
                            next_token = False

                        projection_tokens = tokenizer.tokenize(projection[2])

                        test_tokens = []
                        test_labels = []
                        dummy_label = "Dummy"
                        last_label = ""
                        if prev_token: 
                            test_tokens.append(prev_token)
                            last_label = dummy_label
                            test_labels.append(last_label)
                        for pjtk in  projection_tokens:
                            test_tokens.append(pjtk)
                            test_labels.append("None")
                        if next_token:
                            test_tokens.append(next_token)
                            test_labels.append(dummy_label)

                        test_pos_tags = tagger.tag(test_tokens)
                        tagged_text = [tpt + (test_labels[i],) for i, tpt in enumerate(test_pos_tags)]
                        if debug and False:
                            print >> std.stderr, "Tagged projection", tagged_text

                        X_test = kpc.sent2features(tagged_text)

                        is_not_kp = "None"
                        tmp_label = is_not_kp
                        new_kp = []


                        X_labeled_0 = crftagger0.tag(X_test)
                        X_labeled_1 = crftagger1.tag(X_test)
                        X_labeled_2 = crftagger2.tag(X_test)

                        #if debug and False:
                        #    print >> std.stderr, X_labeled, tagged_text, X_test
                        
                        if tagged_text:
                            if tagged_text[0][2] == dummy_label:
                                X_labeled_0.pop(0)
                                X_labeled_1.pop(0)
                                X_labeled_2.pop(0)
                                tagged_text.pop(0)
                            if tagged_text[-1][2] == dummy_label:
                                X_labeled_0.pop(-1)
                                X_labeled_1.pop(-1)
                                X_labeled_2.pop(-1)
                                tagged_text.pop(-1)
                        
                        is_not_kp = "None"
                        tmp_label = is_not_kp
                        new_kp = []


                        if X_labeled_0[0][0:2] == "B-" and not("B-None" in X_labeled_0) and not ("None" in X_labeled_0):
                            for kp in zip(X_labeled_0, [tt[0] for tt in tagged_text]):
                                if debug and False:
                                    print >> sys.stderr, "    ---- ", kp
                                if kp[0][0:2] == "B-":
                                    if new_kp and tmp_label != is_not_kp:
                                        kp_list.append((tmp_label, start, end))
                                    tmp_label = kp[0][2:]
                                    new_kp = []
                                new_kp.append(kp[1])
                            if new_kp:
                                kp_list.append((tmp_label, start, end))

                        is_not_kp = "None"
                        tmp_label = is_not_kp
                        new_kp = []


                        if X_labeled_1[0][0:2] == "B-" and not("B-None" in X_labeled_1) and not ("None" in X_labeled_1):
                            for kp in zip(X_labeled_1, [tt[0] for tt in tagged_text]):
                                if debug and False:
                                    print >> sys.stderr, "    ---- ", kp
                                if kp[0][0:2] == "B-":
                                    if new_kp and tmp_label != is_not_kp:
                                        kp_list.append((tmp_label, start, end))
                                    tmp_label = kp[0][2:]
                                    new_kp = []
                                new_kp.append(kp[1])
                            if new_kp:
                                kp_list.append((tmp_label, start, end))

                        is_not_kp = "None"
                        tmp_label = is_not_kp
                        new_kp = []


                        if X_labeled_2[0][0:2] == "B-" and not("B-None" in X_labeled_2) and not ("None" in X_labeled_2):
                            for kp in zip(X_labeled_2, [tt[0] for tt in tagged_text]):
                                if debug and False:
                                    print >> sys.stderr, "    ---- ", kp
                                if kp[0][0:2] == "B-":
                                    if new_kp and tmp_label != is_not_kp:
                                        kp_list.append((tmp_label, start, end))
                                    tmp_label = kp[0][2:]
                                    new_kp = []
                                new_kp.append(kp[1])
                            if new_kp:
                                kp_list.append((tmp_label, start, end))

                    print >> sys.stderr, file_count, training_crfsuite

                    #kp_list = kpc.shortest_keyphrases(kp_list)
                    kp_list = kpc.largest_keyphrases(kp_list) 
 
                    kp_index = 0
                    for kp in kp_list:
                        kp_index += 1 
                        start = kp[1]
                        end = kp[2]
                        print kp, raw_text[start:end]
                        term_string = "T" + str(kp_index) + "\t" + kp[0] + " " + str(start) + " " + str(end) + "\t" + raw_text[start:end]
                        term_string = term_string.encode("utf-8")
                        print >> kpe_file, term_string
                        #tmp_kps_candidates.append((start, end, m.span(1), kp, raw_text[start:end]))
                        if debug and kp_iter_counter == 0:  
                            #print >> sys.stderr, raw_text
                            print >> sys.stderr, kp_iter_counter, ": ", kp[1].encode("utf-8")
                    print >> sys.stderr, "File:", file_count, "KeyPhrases:", len(kp_list)
                    kpe_file.close()
    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/"
        print >> sys.stderr, "Error: ", sys.exc_info()
