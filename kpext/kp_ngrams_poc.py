#!/usr/bin/python 
import sys
import os
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
import operator
import nltk
import re
import kpcommon as kpc 

if __name__ == "__main__":
    try:
        debug = True if sys.argv[-1] == "debug" else False
        debug_tests = 3
        file_count = 0

        dir_corpus = sys.argv[1]       
        dir_output = sys.argv[2]

        tokenizer = Tokenizer()

        #test_sents = []
        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-4:]
                if ext == '.ann':
                    file_count += 1
                    if debug and file_count > debug_tests:
                        break
                    
                    file_text = os.path.join(dirname, f[:-4] + ".txt")
                    text_file = open(file_text, "r")
                    file_kpe = os.path.join(dir_output, f[:-4] + ".ann")
                    kpe_file = open(file_kpe, "w")

                    raw_text = unicode(text_file.read(), encoding="utf-8")
                    tokens = raw_text.split(' ')

                    kp_index = 0
                    len_tokens = len(tokens)
                    N = 6
                    for ntoken in range(1, N + 1):
                        start = 0
                        for i, token in enumerate(tokens):
                            if i + N < len_tokens:
                                kp_index += 1
                                ngram_str = ' '.join(tokens[i:i + ntoken])
                                end = start + len(ngram_str)
                                term_string = 'T' + str(kp_index) + '\t' + 'None ' + str(start) + ' ' + str(end) + '\t' + raw_text[start:end].strip()
                                term_string = term_string.encode("utf-8")
                                print >> kpe_file, term_string
                                start += len(' '.join(tokens[i:i+1])) + 1
                    text_file.close()
                    kpe_file.close()

    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
