import sys 
import os
import math
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
import operator

POS_OBVIOUS_ERRORS = {
    '[': ['NN', 'NNS', 'NNP'],
    ']': ['NN', 'NNS', 'NNP']
}

def my_tokenizer(doc):
    tokenizer = Tokenizer()
    return [t.lower() for t in tokenizer.tokenize(doc)]

def my_tokenizer2(doc):
    tokenizer = Tokenizer()
    return [t.lower() for t in escape_not_abbreviations(tokenizer.tokenize(doc))]

def my_tokenizer3(doc, tokenizer = None):
    return [t.lower() for t in escape_not_abbreviations(tokenizer.tokenize(doc))]

def my_features(doc):
    features = doc.split(" ")
    return features

def my_features_as_string(doc, pos, tokenizer):
    features = " ".join(my_tokenizer3(doc, tokenizer))
    features += " " + " ".join([ "sufix[-3:]=%s " % t[-3:] +   
                                    "sufix[-2:]=%s " % t[-2:] +
                                    "prefix[0:2]=%s " % t[0:2] +
                                    "prefix[0:3]=%s " % t[0:3] +
                                    "isupper=%s " % t.isupper() +
                                    "istitle=%s " % t.istitle() +
                                    "isdigit=%s" % t.isdigit()
                                 for t in doc.split()])
    features += " " + " ".join(["pos=%s" % p for p in pos.split()])
    #print features
    return features

def pos_tagger(doc, tagger, tokenizer):
    return " ".join([t[1] for t in tagger.tag(my_tokenizer3(doc, tokenizer))])


def is_pos_error(token, pos):
    if token in POS_OBVIOUS_ERRORS and pos in POS_OBVIOUS_ERRORS[token]:
        return True
    else:
        return False

def escape_not_abbreviations(tokens):
    new_tokens = []
    length = len(tokens)
    for index, token in enumerate(tokens):
        try:
            if tokens[index][-1] == "." and len(tokens[index]) > 1 and (index + 1) < length and tokens[index + 1][0].isupper():
                new_tokens.append(tokens[index][:-1])
                new_tokens.append(tokens[index][-1])
                #print >> sys.stderr, tokens[index], tokens[index + 1]
            elif len(tokens[index]) > 1 and tokens[index][-1] == "." and index == length - 1:
                new_tokens.append(tokens[index][:-1])
                new_tokens.append(tokens[index][-1])
            else:
                new_tokens.append(tokens[index])
        except:
            print >> sys.stderr, "E) Abbreviation", tokens, index
            new_tokens.append(tokens[index])
    return new_tokens    

def get_pos_tags_by_count(pos_seq_filename, count_limit, debug = False):
    is_posregex = False
    tags_file = open(pos_seq_filename, "r")
    pos_sequences = []
    for ct in tags_file:
        ct_fields = ct.strip().split("\t")
        if not is_posregex and "POSREGEX" == ct_fields[0][:8]:
            is_posregex = True
        if int(ct_fields[1]) < count_limit:
            continue
        if debug:
            print ct_fields
        pos_sequences.append([t for t in ct_fields])
    return pos_sequences, is_posregex

def print_to_ann(output_stream, cur_id, type_indexes, kpstr, pos_str = None, return_string = False):
    if pos_str:
        ann_str = cur_id + "\t" + type_indexes + "\t" + kpstr + "\t" + pos_str
    else:
        ann_str = cur_id + "\t" + type_indexes + "\t" + kpstr
    if not return_string:
        print >> output_stream, ann_str
    else:
        return ann_str

def get_document_content(dirname, filename, extensions = None):
    full_text = []
    if not extensions:
        try:
            path_filename = os.path.join(dirname, filename)
            stream_input = open(path_filename, "r")
            for line in stream_input:
                full_text.append(unicode(line.strip(), encoding="utf-8"))
            stream_input.close()
        except:
            print >> sys.stderr, "E) Single file: ", path_filename, sys.exc_info()            
    else:
        try:
            for ext in extensions:
                path_filename = os.path.join(dirname, filename + ext)
                stream_input = open(path_filename, "r")
                for line in stream_input:
                    full_text.append(unicode(line.strip(), encoding="utf-8"))
                stream_input.close()
        except:
            print >> sys.stderr, "E) Multiple file extensions: ", path_filename, sys.exc_info()
    return full_text

def get_document_content_ann(dirname, filename):
    full_text = []
    try:
        path_filename = os.path.join(dirname, filename)
        stream_input = open(path_filename, "r")
        for line in stream_input:
            if line[0] not in ["R", "*"]:
                full_text.append(unicode(line.strip(), encoding="utf-8").split("\t"))
        stream_input.close()
    except:
        print >> sys.stderr, "E) Single file: ", path_filename, sys.exc_info()            
    return full_text

def tf_normalized(full_texts):
    tokenizer = Tokenizer()
    tf = {}
    max_value = 0
    for text in full_texts:
        text_tokens = tokenizer.tokenize(text)
        text_tokens = escape_not_abbreviations(text_tokens)
        for token in text_tokens:
            token = token.lower()
            tf.setdefault(token, 0.0)
            tf[token] += 1.0
            if tf[token] > max_value:
                max_value = tf[token]
    for t in tf:
        tf[t] = tf[t]/max_value
    return tf

def idf(V, D, N):
    cur_idf = {}
    for t in V:
        for d in D:
            if t in D[d]:
                cur_idf.setdefault(t, 0.0)
                cur_idf[t] += 1.0
    for t in cur_idf:
        cur_idf[t] = math.log(N/(1.0 + cur_idf[t]))
    return cur_idf

def tf_idf(D, t_idf):
    result = {}
    for d in D:
        result.setdefault(d, {})
        for t in D[d]:
            cur_tf = D[d][t]
            cur_idf = t_idf[t]
            result[d][t] = cur_tf * cur_idf
    return result

def norm(V):
    S_x = 0.0
    for x in V:
        S_x += math.pow(V[x], 2)
    return math.sqrt(S_x)

def v1_dot_v2(V1, V2):
    S_v1v2 = 0.0
    for v1 in V1:
        if v1 in V2:
            S_v1v2 += V1[v1]*V2[v1]
    return S_v1v2

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
    ]
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('EOS')
                
    return features

def word2features_extra(sent, i, qr):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
    ]
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]

        ngram_in_msag = qr.is_bigram_in_titles(word1, word)

        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
            '-1:bigram_in_msag=%s' % ngram_in_msag,
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]

        ngram_in_msag = qr.is_bigram_in_titles(word, word1)

        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
            '+1:bigram_in_msag=%s' % ngram_in_msag,
        ])
    else:
        features.append('EOS')
     
    if i > 0 and i < len(sent)-1:
        
        word1, word3 = sent[i-1][0], sent[i+1][0]
        ngram_in_msag = qr.is_trigram_pos_in_titles(word1, word, word3)
        features.extend([
            'trigram_in_msag=%s' % ngram_in_msag,
        ])
        postag1, postag3 = sent[i-1][1], sent[i+1][1]
        ngram_pos_in_msag = qr.is_trigram_pos_in_titles(postag1, postag, postag3)
        features.extend([
            'trigram_pos_in_msag=%s' % ngram_pos_in_msag,
        ])

    #print features                
    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]   

def sent2features_extra(sent, qr):
    return [word2features_extra(sent, i, qr) for i in range(len(sent))]

def shortest_keyphrases_pop(kp_list, index_start = 1, index_end = 2):
    pop_item, last_start, last_end, list_change = -1, -1, -1, True
    while(list_change):
        list_change = False
        for i, kp in enumerate(kp_list):
            start = kp[index_start]
            end = kp[index_end]
            if last_start <= start and last_end >= end:
                 pop_item = i - 1
                 break
            last_start = start
            last_end = end
        if pop_item > -1:
            print "POP:", kp_list.pop(pop_item)
            pop_item, last_start, last_end, list_change = -1, -1, -1, True
    return kp_list
   
def shortest_keyphrases(kp_list, index_start = 1, index_end = 2):
    print "kp_list, len", len(kp_list)
    kp_list = sorted(kp_list, key=operator.itemgetter(2), reverse=True)
    kp_list = shortest_keyphrases_pop(kp_list, index_start = index_start, index_end = index_end)
    kp_list = sorted(kp_list, key=operator.itemgetter(1))
    kp_list = shortest_keyphrases_pop(kp_list, index_start = index_start, index_end = index_end)
    print "kp_list, len", len(kp_list)
    return kp_list

def largest_keyphrases_pop(kp_list, index_start = 1, index_end = 2):
    pop_item, last_start, last_end, list_change = -1, -1, -1, True
    while(list_change):
        list_change = False
        for i, kp in enumerate(kp_list):
            start = kp[index_start]
            end = kp[index_end]
            if last_start <= start and last_end >= end:
                 pop_item = i
                 break
            last_start = start
            last_end = end
        if pop_item > -1:
            print "POP:", kp_list.pop(pop_item)
            pop_item, last_start, last_end, list_change = -1, -1, -1, True
    return kp_list

def largest_keyphrases(kp_list, index_start = 1, index_end = 2):
    print "kp_list, len", len(kp_list)
    kp_list = sorted(kp_list, key=operator.itemgetter(2), reverse=True)
    kp_list = largest_keyphrases_pop(kp_list, index_start = index_start, index_end = index_end)
    kp_list = sorted(kp_list, key=operator.itemgetter(1))
    kp_list = largest_keyphrases_pop(kp_list, index_start = index_start, index_end = index_end)
    print "kp_list, len", len(kp_list)
    return kp_list

def deal_with_overlapping_pop(kp_list, index_start = 1, index_end = 2):
    pop_item, last_start, last_end, list_change = -1, -1, -1, True
    while(list_change):
        list_change = False
        for i, kp in enumerate(kp_list):
            start = kp[index_start]
            end = kp[index_end]
            if last_start <= start and last_end >= end:
                 pop_item = i
                 break
            last_start = start
            last_end = end
        if pop_item > -1:
            print "POP:", kp_list.pop(pop_item)
            pop_item, last_start, last_end, list_change = -1, -1, -1, True
    return kp_list


def deal_with_overlapping(kp_list, index_start = 1, index_end = 2):
    print "kp_list, len", len(kp_list)
    kp_list = sorted(kp_list, key=operator.itemgetter(2), reverse=True)
    kp_list = deal_with_overlapping_pop(kp_list, index_start = index_start, index_end = index_end)
    print "kp_list, len", len(kp_list)
    return kp_list
