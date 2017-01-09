#!/usr/bin/python 
import sys
import os
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
from nltk.tag.perceptron import PerceptronTagger
import operator

if __name__ == "__main__":
    try:
        dir_corpus = sys.argv[1]
        dir_output = sys.argv[2]
        
        tokenizer = Tokenizer()
        #pos
        tagger = PerceptronTagger()

        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-3:]
                if ext == 'ann':
                    file_ann = os.path.join(dirname, f[:-3] + "ann")
                    ann_file = open(file_ann, "r")
                    file_ann_ext = os.path.join(dir_output, f[:-3] + "anne")
                    ann_ext_file = open(file_ann_ext, "w")
                    print f[:-4]
                    indexes_kp_tmp = {}
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
                            pos_tags = " ".join([pos[1] for pos in tagger.tag(tokens)])
                            ann_text = ann_text.encode("utf-8")
                            print >> ann_ext_file, " ".join([str(ti) for ti in type_indexes]) + "\t" + ann_text + "\t" + pos_tags
                    ann_file.close()
                    ann_ext_file.close()

                    file_text = os.path.join(dirname, f[:-3] + "txt")
                    text_file = open(file_text, "r")
                    file_nokp = os.path.join(dir_output, f[:-3] + "nann")
                    nokp_file = open(file_nokp, "w")

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

                    i = 0
                    for start, end in indexes_kp:
                        if start == 0:
                            i = end
                            continue
                        not_kp_text = raw_text[i:start]
                        not_kp_tokens = tokenizer.tokenize(not_kp_text)
                        pos_tags = " ".join([pos[1] for pos in tagger.tag(not_kp_tokens)])
                        not_kp_text = not_kp_text.encode("utf-8")
                        print >> nokp_file, i, str(start) + "\t" + not_kp_text + "\t" + pos_tags
                        i = end
                    len_raw_text = len(raw_text)
                    if end < len_raw_text:
                        not_kp_text = raw_text[end:len_raw_text].strip("\n")
                        not_kp_tokens = tokenizer.tokenize(not_kp_text)
                        pos_tags = " ".join([pos[1] for pos in tagger.tag(not_kp_tokens)])
                        not_kp_text = not_kp_text.encode("utf-8")
                        print >> nokp_file, end, str(len_raw_text) + "\t" + not_kp_text + "\t" + pos_tags
                       
                    text_file.close()
                    nokp_file.close()

    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
