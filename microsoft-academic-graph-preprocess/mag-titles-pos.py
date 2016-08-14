#!/usr/bin/python
import sys 
import time
from nltk.tag.perceptron import PerceptronTagger
#from nltk.tokenize import TweetTokenizer as Tokenizer
#from nltk.tokenize import WordPunctTokenizer as Tokenizer 
from nltk.tokenize import TreebankWordTokenizer as Tokenizer

def pos_titles_from(input_path, output_path = ""):
  finput = open(input_path, "r")
  if output_path:
    foutput = open(output_path, "w")
  else:
    foutput = sys.stdout

  tokenizer = Tokenizer()
  tagger = PerceptronTagger()

  line_number = 0
  for line in finput:
    if line_number % 100000 == 0:
      print >> sys.stderr, "Status:", time.strftime("%d/%m/%Y %H:%M:%S"), "Count:", line_number
    line_number += 1
    try:
      fields = line.strip().split("\t")
      paper_id = fields[0]
      title = fields[1]
      print >> foutput, paper_id
      tokens = tokenizer.tokenize(title)
      for token in tagger.tag(tokens):
        print >> foutput, token[0], token[1]
      print >> foutput
    except:
      print >> sys.stderr, "Error:", line, sys.exc_info()

if __name__ == "__main__":
  if sys.argv[2:]:
    pos_titles_from(sys.argv[1], sys.argv[2])
  else:
    pos_titles_from(sys.argv[1])
