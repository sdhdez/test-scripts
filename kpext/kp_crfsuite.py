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

        tokenizer = Tokenizer()
        #pos
        tagger = PerceptronTagger()

        crftagger = pycrfsuite.Tagger()
        crftagger.open('keyphrase-0.crfsuite')

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
                    file_kpe = os.path.join(dir_output, f[:-4] + ".ann")
                    kpe_file = open(file_kpe, "w")

                    raw_text = unicode(text_file.read(), encoding="utf-8")
                    tokens = tokenizer.tokenize(raw_text)
                    tagged_text = [t + ("None",)  for t in tagger.tag(tokens)]
                    text_file.close()
                    #test_sents.append(tagged_text)
                    if debug:
                        print >> sys.stderr, raw_text

                    X_test = kpc.sent2features(tagged_text)
                    is_none = "None"
                    last_label = is_none
                    new_kp = []
                    kp_list = []
                    for kp in zip(crftagger.tag(X_test), [tt[0] for tt in tagged_text]):
                        if debug:
                            print >> sys.stderr, "    ---- ", kp
                        if kp[0] != is_none:
                            if kp[0] == last_label:
                                new_kp.append(kp[1])
                            else:
                                if new_kp:
                                    if debug:
                                        print >> sys.stderr, (last_label, new_kp)
                                    kp_list.append((last_label, [nkp for nkp in new_kp]))
                                new_kp = []
                                new_kp.append(kp[1])
                                last_label = kp[0]
                        elif new_kp:
                            if debug:
                                print >> sys.stderr, (last_label, new_kp)
                            kp_list.append((last_label, " ".join(new_kp)))
                            new_kp = []
                            last_label = is_none
                    if new_kp:
                        if debug:
                            print >> sys.stderr, (last_label, new_kp)
                        kp_list.append((last_label, " ".join(new_kp)))
                        new_kp = []
                        last_label = is_none
                   
                    if debug:
                        print >> sys.stderr, raw_text
                    kp_index = 0
                    for kp in kp_list:
                        kp_iter_counter = 0
                        for m in re.finditer("\W?(" + re.escape(kp[1]) + ")\W", raw_text):
                            kp_iter_counter += 1
                            kp_index += 1
                            #print kp_iter_counter, m.groups()
                            start = m.start(1)
                            end = m.end(1)
                            term_string = "T" + str(kp_index) + "\t" + kp[0] + " " + str(start) + " " + str(end) + "\t" + raw_text[start:end]
                            term_string = term_string.encode("utf-8")
                            print >> kpe_file, term_string
                            #tmp_kps_candidates.append((start, end, m.span(1), kp, raw_text[start:end]))

                        if debug and kp_iter_counter == 0:  
                            """
                                There is an error here and in the projections.
                                The match is made by tokens.
                                When some of semi-colon, comma or ( ) there is an extra espace. 
                            """
                            print >> sys.stderr, raw_text
                            print >> sys.stderr, kp_iter_counter, ": ", kp[1].encode("utf-8")

                    kpe_file.close()

    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
