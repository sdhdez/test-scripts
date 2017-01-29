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
        target_type = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != 'debug' else ''

        tokenizer = Tokenizer()
        #pos
        tagger = PerceptronTagger()

        qr = mdbcl.QueryResources()

        extra_features = True
        without_types = True

        train_sents = []
        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-4:]
                if ext == '.ann':
                    file_count += 1
                    if debug and file_count > debug_tests:
                        break
                    
                    file_ann = os.path.join(dirname, f[:-4] + ".clss")
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
                            #pos_tags = [t + (type_indexes[0],)  for t in tagger.tag(tokens)]
                            #if pos_tags:
                            #    pos_tags[0] = pos_tags[0][0:2] + ("B-" + pos_tags[0][2],)
                            #    if debug:
                            #        print >> sys.stderr, pos_tags
                            annotations[" ".join([str(ti) for ti in type_indexes[1:]])] = (ann_text, type_indexes[0])
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

                    train_sent = []
                    prev_token = []
                    next_token = []
                    for indexes in annotations.keys():
                        key_index = indexes.split()
                        start = int(key_index[0])
                        end = int(key_index[1])
                        if debug:
                            print >> sys.stderr, start, end, annotations[indexes]
                   
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

                        annotation_tokens = tokenizer.tokenize(annotations[indexes][0])
                       
                        train_tokens = []
                        train_labels = []
                        last_label = ""
                        if prev_token: 
                            train_tokens.append(prev_token)
                            last_label = "B-None"
                            train_labels.append(last_label)
                        train_tokens.append(annotation_tokens[0])
                       
                        annotation_type = annotations[indexes][1]
                        if without_types and annotation_type != "None":
                            annotation_type = "KeyPhrase" #train for keyphrases (not Process, Task or Material)

                        #If it is not the target class then it is None
                        if (not target_type) or target_type == annotation_type: 
                            curr_label = "B-" + annotation_type
                        else:
                            curr_label = "B-None"

                        if last_label == curr_label:
                            train_labels.append(last_label[2:])
                        else:
                            train_labels.append(curr_label)
                        for antk in  annotation_tokens[1:]:
                            train_tokens.append(antk)
                            train_labels.append(annotation_type)
                        if next_token:
                            train_tokens.append(next_token)
                            if last_label == curr_label:
                                train_labels.append(last_label[2:])
                            else:
                                train_labels.append(last_label)
                        
                        train_pos_tags = tagger.tag(train_tokens)
                        train_sent = [tpt + (train_labels[i],) for i, tpt in enumerate(train_pos_tags)]

                    text_file.close()
                    train_sents.append(train_sent)
        if debug and False:
            if extra_features:
                print >> sys.stderr, kpc.sent2features_extra(train_sents[0], qr)[0]
            else:
                print >> sys.stderr, kpc.sent2features(train_sents[0])[0]

        if extra_features:
            X_train = [kpc.sent2features_extra(s, qr) for s in train_sents]
            y_train = [kpc.sent2labels(s) for s in train_sents]
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
        trainer.train('keyphrase_projection' + ( '.' + target_type if target_type != '' else '' ) + '.crfsuite')
        print trainer.logparser.last_iteration
    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
