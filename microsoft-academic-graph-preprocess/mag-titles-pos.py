#!/usr/bin/python
import sys 
import time
from nltk.tag.perceptron import PerceptronTagger
#from nltk.tokenize import TweetTokenizer as Tokenizer
#from nltk.tokenize import WordPunctTokenizer as Tokenizer 
from nltk.tokenize import TreebankWordTokenizer as Tokenizer

def pos_titles_from(input_path):
  line_number = 0
  finput = open(input_path, "r")
  tokenizer = Tokenizer()
  tagger = PerceptronTagger()
  for line in finput:
    if line_number % 100000 == 0:
      print >> sys.stderr, "Status:", time.strftime("%d/%m/%Y %H:%M:%S"), "Count:", line_number
    line_number += 1
    try:
      paper_id, title = line.split("\t")
      tokens = tokenizer.tokenize(title.strip())
      for token in tagger.tag(tokens):
        print paper_id, token[0], token[1], token[0].lower()
      print 
    except:
      print >> sys.stderr, "Error:", line, sys.exc_info()

if __name__ == "__main__":
  pos_titles_from(sys.argv[1])
