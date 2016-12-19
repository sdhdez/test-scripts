#!/usr/bin/python 
import sys
import os
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
from nltk.tag.perceptron import PerceptronTagger

def pos_text(text):
    try:
        tokenizer = Tokenizer()
        #pos
        tagger = PerceptronTagger()
        tokens = tokenizer.tokenize(text)
        tagged_tokens = [(token[0], token[1]) for token in tagger.tag(tokens)]
        #span 
        offset = 0
        tagged_tokens_index = []
        for tt in tagged_tokens:
            start = offset + text[offset:].find(tt[0])
            end_token = start + len(tt[0])
            if text[start:end_token] != tt[0]:
                print >> sys.stderr, "Different."
                raise 
            tagged_tokens_index.append((start, end_token, tt[0], tt[1]))
            offset = end_token
        return tagged_tokens_index 
    except:
        print >> sys.stderr, "Error: ", sys.exc_info()

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

                    print "Starting ..."
                    print f[:-4]
                    indexes_kp = []
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
                            indexes_kp.append((type_indexes[1], type_indexes[2]))
                            ann_text = ann_items[2]
                            tokens = tokenizer.tokenize(ann_text)
                            pos_tags = " ".join([pos[1] for pos in tagger.tag(tokens)])
                            ann_text = ann_text.encode("utf-8")
                            print ann_text, pos_tags
                            print >> ann_ext_file, " ".join([str(ti) for ti in type_indexes]) + "\t" + ann_text + "\t" + pos_tags
                    ann_file.close()
                    ann_ext_file.close()

                    file_text = os.path.join(dirname, f[:-3] + "txt")
                    text_file = open(file_text, "r")
                    file_nokp = os.path.join(dir_output, f[:-3] + "nann")
                    nokp_file = open(file_nokp, "w")

                    raw_text = unicode(text_file.read(), encoding="utf-8")
                    print raw_text
                    i = 0
                    for start, end in indexes_kp:
                        not_kp_text = raw_text[i:start]
                        not_kp_tokens = tokenizer.tokenize(not_kp_text)
                        pos_tags = " ".join([pos[1] for pos in tagger.tag(not_kp_tokens)])
                        not_kp_text = not_kp_text.encode("utf-8")
                        print >> nokp_file, i, str(start) + "\t" + not_kp_text + "\t" + pos_tags
                        i = end + 1 
                    text_file.close()
                    nokp_file.close()

    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
