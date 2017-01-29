#!/usr/bin/python 
import sys
import os
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
from nltk.tag.perceptron import PerceptronTagger
import operator
import pycrfsuite
import kpcommon as kpc
import mdb_common_lib as mdbcl

if __name__ == "__main__":
    try:
        debug = True if sys.argv[-1] == "debug" else False
        debug_tests = 3
        file_count = 0

        dir_corpus = sys.argv[1]
       
        extra_features = True
        qr = mdbcl.QueryResources()

        without_types = False

        tokenizer = Tokenizer()
        #pos
        tagger = PerceptronTagger()

        train_sents = []

        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-4:]
                if ext == '.ann':
                    file_count += 1
                    if debug and file_count > debug_tests:
                        break
                    
                    file_ann = os.path.join(dirname, f[:-4] + ".ann")
                    ann_file = open(file_ann, "r")
                    #file_ann_ext = os.path.join(dir_output, f[:-4] + ".anne")
                    #ann_ext_file = open(file_ann_ext, "w")
                    print f[:-4]
                    indexes_kp_tmp = {}
                    annotations = {}
                    for ann in ann_file:
                        ann = unicode(ann, encoding="utf-8")
                        if ann[0] not in ["R", "*"]:
                            ann_items = ann.strip().split("\t")
                            if ann_items[1].find(";") >= 0:
                                type_indexes_tmp = ann_items[1].split(" ")
                                type_indexes = type_indexes_tmp[0:2] + type_indexes_tmp[3:]
                            else:
                                type_indexes = ann_items[1].split(" ")
                            type_indexes[1] = int(type_indexes[1])
                            type_indexes[2] = int(type_indexes[2])
                            indexes_kp_tmp.setdefault(type_indexes[1], -1)
                            if indexes_kp_tmp[type_indexes[1]] < type_indexes[2]:
                                indexes_kp_tmp[type_indexes[1]] = type_indexes[2]
                            ann_text = ann_items[2]
                            tokens = tokenizer.tokenize(ann_text)
                            if without_types:
                                annotation_type = 'KeyPhrase'
                            else:
                                annotation_type = type_indexes[0]
                            pos_tags = [t + (annotation_type,)  for t in tagger.tag(tokens)]
                            if pos_tags:
                                pos_tags[0] = pos_tags[0][0:2] + ("B-" + pos_tags[0][2],)
                                if debug:
                                    print >> sys.stderr, pos_tags
                            annotations[" ".join([str(ti) for ti in type_indexes[1:]])] = pos_tags
                            #print >> ann_ext_file, " ".join([str(ti) for ti in type_indexes]) + "\t" + ann_text + "\t" + pos_tags
                    ann_file.close()
                    #ann_ext_file.close()

                    if debug:
                        pass
                        #print indexes_kp_tmp
                        #print annotations

                    file_text = os.path.join(dirname, f[:-4] + ".txt")
                    text_file = open(file_text, "r")
                    #file_nokp = os.path.join(dir_output, f[:-4] + ".nann")
                    #nokp_file = open(file_nokp, "w")

                    raw_text = unicode(text_file.read(), encoding="utf-8")

                    indexes_kp_tmp = sorted(indexes_kp_tmp.items(), key=operator.itemgetter(0,1))
                    indexes_kp = []
                    ikp_tmp = (-1, -1)
                    for ikp in indexes_kp_tmp:
                        if ikp_tmp[1] >= ikp[0]:
                            ikp_tmp = (ikp_tmp[0], max([ikp_tmp[1], ikp[1]]))
                            print "Overlap --- ", ikp_tmp
                        indexes_kp.append(ikp_tmp)
                        ikp_tmp = ikp

                    if ikp_tmp[0] > indexes_kp[len(indexes_kp) - 1][1]:
                        indexes_kp.append(ikp_tmp)
                    else:
                        print "Overlap at the end --- ", ikp_tmp
                    indexes_kp.pop(0) #removes (-1, -1)

    
                    train_sent = []
                    i = 0
                    for start, end in indexes_kp:
                        key_index = str(start) + " " + str(end)
                        if start == 0:
                            if key_index in annotations:
                                print "annotations[key_index] ... ", annotations[key_index]
                                train_sent += annotations[key_index]
                            i = end
                            continue
                        not_kp_text = raw_text[i:start]
                        tokens = tokenizer.tokenize(not_kp_text)
                        pos_tags = [t + ("None",)  for t in tagger.tag(tokens)]
                        if pos_tags:
                            pos_tags[0] = pos_tags[0][0:2] + ("B-" + pos_tags[0][2],)
                            if debug:
                                print >> sys.stderr, pos_tags

                        train_sent += pos_tags

                        if key_index in annotations:
                            train_sent += annotations[key_index]
                        #print >> nokp_file, i, str(start) + "\t" + not_kp_text + "\t" + pos_tags
                        i = end
                    len_raw_text = len(raw_text)
                    if end < len_raw_text:
                        not_kp_text = raw_text[end:len_raw_text].strip("\n")
                        tokens = tokenizer.tokenize(not_kp_text)
                        pos_tags = [t + ("None",)  for t in tagger.tag(tokens)]
                        if pos_tags:
                            pos_tags[0] = pos_tags[0][0:2] + ("B-" + pos_tags[0][2],)
                        train_sent += pos_tags
                        #print >> nokp_file, end, str(len_raw_text) + "\t" + not_kp_text + "\t" + pos_tags
                    if debug:
                        #print " ".join([str(ts[0].encode("utf-8")) for ts in train_sent])
                        #print raw_text
                        #print train_sent
                        pass
                    text_file.close()

                    train_sents.append(train_sent)

        if debug and False:
            print >> sys.stderr, kpc.sent2features(train_sents[0])[0]

        if extra_features:
            X_train = [kpc.sent2features_extra(s, qr) for s in train_sents]
        else:
            X_train = [kpc.sent2features(s) for s in train_sents]

        y_train = [kpc.sent2labels(s) for s in train_sents]
        
        trainer = pycrfsuite.Trainer(verbose=False)
        for xseq, yseq in zip(X_train, y_train):
            trainer.append(xseq, yseq)
        trainer.set_params({
                'c1': 1.0,   # coefficient for L1 penalty
                'c2': 1e-3,  # coefficient for L2 penalty
                'max_iterations': 50,  # stop earlier
                # include transitions that are possible, but not observed
                'feature.possible_transitions': True
        })
        trainer.params()
        trainer.train('keyphrase_crf_extra_features.crfsuite')
        print trainer.logparser.last_iteration
    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
