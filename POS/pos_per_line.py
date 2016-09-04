#!/usr/bin/python 
import sys
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
from nltk.tag.perceptron import PerceptronTagger

def pos_per_line(text_file):
    try:
        tokenizer = Tokenizer()
        #pos
        tagger = PerceptronTagger()
        for s in text_file:
            tokens = tokenizer.tokenize(s)
            #print " ".join([" ".join(token)  for token in tagger.tag(tokens)])
            print " ".join([token[1]  for token in tagger.tag(tokens)])
    except:
        print >> sys.stderr, "Error pos_per_line(text_file): ", sys.exc_info()

if __name__ == "__main__":
    try:
        input_path = sys.argv[1]
        text_file = open(input_path, "rU")
        pos_per_line(text_file)

    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<input_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/some/input_file.txt" 
