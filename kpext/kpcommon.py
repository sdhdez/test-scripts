import sys 
import os
import math
from nltk.tokenize import TreebankWordTokenizer as Tokenizer

POS_OBVIOUS_ERRORS = {
    '[': ['NN', 'NNS', 'NNP'],
    ']': ['NN', 'NNS', 'NNP']
}

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

def print_to_ann(output_stream, cur_id, type_indexes, kpstr, return_string = False):
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
