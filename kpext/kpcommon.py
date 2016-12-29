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
