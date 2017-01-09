import sys 

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

def print_to_ann(output_stream, _id, type_indexes, kpstr, return_string = False):
    ann_str = _id + "\t" + type_indexes + "\t" + kpstr
    if not return_string:
        print >> output_stream, ann_str
    else:
        return ann_str
