#!/usr/bin/python
import sys 
import time
import getopt
from nltk.tag.perceptron import PerceptronTagger
#from nltk.tokenize import TweetTokenizer as Tokenizer
#from nltk.tokenize import WordPunctTokenizer as Tokenizer 
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
import guess_language #https://bitbucket.org/spirit/guess_language

def get_fields(line):
    fields = line.strip().split("\t")
    return fields[0], fields[1].split("@@@")[0]

def is_english(text):
    lngid_res = guess_language.guess_language(text.decode("utf-8"))
    return lngid_res == 'en'

def pos_titles_from(input_path, output_path = None, options = None):
    finput, foutput = get_streams(input_path, output_path)
    skip, end = get_options(options)
    tokenizer = Tokenizer()
    tagger = PerceptronTagger()
    line_counter = 0
    skipped_lines = 0
    for line in finput:
        log_advance(1000000, line_counter)
        line_counter += 1
        if line_counter <= skip:
            continue
        if end and line_counter > end:
            break
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

def get_options(options):
    skip, take = 0, 0
    for o in options:
        if o[0] == '-s':
            skip = int(o[1])
        if o[0] == '-t':
            take = int(o[1])
    return skip, skip + take

def _command_line():
    options = []
    try:
        options, args = getopt.getopt(sys.argv[1:], 's:t:')
    except:
        pass
    try:
        pos_titles_from(args[0], output_path = None if not args[1:] else args[1], options = options)
    except:
        print >> sys.stderr, "\nTry with:", sys.argv[0], "[-s<integer>] [-t<integer>] <path/to/input> [path/to/output]"
        print >> sys.stderr, sys.exc_info()

if __name__ == "__main__":
    _command_line()
