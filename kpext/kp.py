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

        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-3:]
                if ext == 'txt':
                    file_text = os.path.join(dirname, f)
                    text_file = open(file_text, "rU")
                    tagged_text = pos_text(text_file.read())

                    file_ann = os.path.join(dirname, f[:-3] + "ann")
                    ann_file = open(file_ann, "rU")
                    for ann in ann_file:
                        if ann[0] not in ["R", "*"]:
                            ann_items = ann.strip().split("\t")
                            if ann_items[1].find(";") >= 0:
                                type_indexes_tmp = ann_items[1].split(" ")
                                type_indexes = type_indexes_tmp[0:2] + type_indexes_tmp[3:]
                            else:
                                type_indexes = ann_items[1].split(" ")
                            type_indexes[1] = int(type_indexes[1])
                            type_indexes[2] = int(type_indexes[2])
                            ann_text = ann_items[2]

                            for tt in tagged_text: 
                                if tt[0] >= type_indexes[1] and tt[1] <= type_indexes[2]:
                                    print tt
                                if tt[1] > type_indexes[2]:
                                    break
                                else: 
                                    continue
                            print type_indexes, ann_text

    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
