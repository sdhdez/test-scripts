#!/usr/bin/python
import sys 
import time
from nltk.tag.perceptron import PerceptronTagger
#from nltk.tokenize import TweetTokenizer as Tokenizer
#from nltk.tokenize import WordPunctTokenizer as Tokenizer 
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
import guess_language #https://bitbucket.org/spirit/guess_language

def log_advance(step, line_counter):
    if line_counter % step == 0:
        print >> sys.stderr, "Status:", time.strftime("%d/%m/%Y %H:%M:%S"), "Count:", line_counter

def log_nlines(total, skipped):
    print >> sys.stderr, "Status:", time.strftime("%d/%m/%Y %H:%M:%S"), "Final:", total, skipped

def get_streams(input_path, output_path):
    finput = open(input_path, "r")
    if output_path:
        foutput = open(output_path, "w")
    else:
        foutput = sys.stdout
    return finput, foutput

def get_fields(line):
    fields = line.strip().split("\t")
    return fields[0], fields[1].split("@@@")[0]

def is_english(text):
    lngid_res = guess_language.guess_language(text.decode("utf-8"))
    return lngid_res == 'en'

def pos_titles_from(input_path, output_path = ""):
    finput, foutput = get_streams(input_path, output_path)
    tokenizer = Tokenizer()
    tagger = PerceptronTagger()
    line_counter = 0
    skipped_lines = 0
    for line in finput:
        log_advance(1000000, line_counter)
        line_counter += 1
        try:
            paper_id, title = get_fields(line)
            if is_english(title):
                print >> foutput, paper_id
                tokens = tokenizer.tokenize(title)
                for token in tagger.tag(tokens):
                    print >> foutput, token[0], token[1]
                print >> foutput
            else:
                skipped_lines += 1
        except:
            print >> sys.stderr, "Error:", line, sys.exc_info()
    log_nlines(line_counter, skipped_lines)

if __name__ == "__main__":
    if sys.argv[2:]:
        pos_titles_from(sys.argv[1], sys.argv[2])
    else:
        pos_titles_from(sys.argv[1])
