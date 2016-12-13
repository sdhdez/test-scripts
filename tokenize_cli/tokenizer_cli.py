import sys 
import nltk
from nltk.tokenize import TreebankWordTokenizer as Tokenizer

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
        file_stream = open(file_name, "r")
        tokenizer = Tokenizer()
        for line in file_stream:
            for t in tokenizer.tokenize(line.replace("\xc2\xa0", "")):
                print t
        file_stream.close()
    except:
        print >> sys.stderr, "Error:", sys.exc_info()
