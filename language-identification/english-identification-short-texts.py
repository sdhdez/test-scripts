import sys
import langid #https://github.com/saffsd/langid.py
import langdetect #https://github.com/Mimino666/langdetect
from nltk.classify import TextCat #http://www.nltk.org/api/nltk.classify.html
import guess_language #https://bitbucket.org/spirit/guess_language

def checking_answer(methodid, relevant_lang, text_lang, result_lang, results):
    results.setdefault(methodid, {})
    results[methodid].setdefault('tp', 0)
    results[methodid].setdefault('fn', 0)
    results[methodid].setdefault('fp', 0)
    results[methodid].setdefault('tn', 0)

    if relevant_lang == text_lang:
        if text_lang == result_lang:
            results[methodid]['tp'] += 1
        else:
            results[methodid]['fn'] += 1
    else:
        if relevant_lang == result_lang:
            results[methodid]['fp'] += 1
        else:
            results[methodid]['tn'] += 1

def evaluate(results):
    for method in results.items():
        tp = method[1]['tp']
        tn = method[1]['tn']
        fp = method[1]['fp']
        fn = method[1]['fn']
        accuracy = (tp + tn)/float(tp + tn + fp + fn)
        precision = tp/float(tp + fp)
        recall = tp/float(tp + fn)
        f1 = 2 * (precision*recall)/(precision + recall)
        print "Method name:\t", method[0]
        print "Accuracy:   \t{0:.4f}".format(accuracy)
        print "Precision:  \t{0:.4f}".format(precision)
        print "Recall:     \t{0:.4f}".format(recall)
        print "f1:         \t{0:.4f}".format(f1)
        print 

def compare_english_identification(corpus):
    relevant_language = "en"
    results = {}
    for line in corpus:
        try:
            text_lang, text = line.strip().split("\t")
            text_split = text.split("@@@") #Microsoft Academic Graph - Titles with translation
            text = text_split[0] #Choose only first text
            text_decode = text.decode("utf-8")
            checking_answer("langdetect", relevant_language, text_lang, with_langdetect(text_decode), results)
            checking_answer("guess_language", relevant_language, text_lang, with_guess_language(text_decode), results)
            checking_answer("langid", relevant_language, text_lang, with_langid(text), results)
            checking_answer("textcat", relevant_language, text_lang, with_textcat(text_decode), results) 
        except UnicodeDecodeError as e:
            print >> sys.stderr, "UnicodeDecodeError ({0}): {1}".format(e.errno, e.strerror)
            return 
        except:
            print >> sys.stderr, "Unexpected error:", sys.exc_info()
            return
    evaluate(results)
    corpus.close()
    
def with_langid(text):
    langid_result = langid.classify(text)
    return langid_result[0]

def with_langdetect(text):
    langdetect_result = langdetect.detect(text) 
    return langdetect_result

def with_textcat(text):
    tc = TextCat()
    textcat_result = tc.guess_language(text)
    return textcat_result[0:2]

def with_guess_language(text):
    guess_language_result = guess_language.guess_language(text)
    return guess_language_result

if __name__ == "__main__":
    try:
        file_input = open(sys.argv[1], "rU")
        compare_english_identification(file_input)
    except IOError, e:
        print >> sys.stderr, "Try with:", sys.argv[0], "<path/to/file_name>"
    
