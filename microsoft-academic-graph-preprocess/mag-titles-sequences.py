import sys 
from copy import copy as copy_list 

def read_sentence_col_fmt(sentences_col_fmt):
    sentence = []
    for line in sentences_col_fmt:
        line = line.strip().split()
        if not line:
            break
        sentence.append((line[1], line[2]))
    if sentence:
        return sentence
    else:
        return None

def extract_sequences(sentences_col_fmt): 
    while True:
        sentence = None
        try:
            sentence = read_sentence_col_fmt(sentences_col_fmt)
            if sentence != None:
                extracted_sequences = sequences_in(sentence)
                print "\n".join([" ".join(e) for e in extracted_sequences])
                print 
                    
            else:
                break
        except:
            print >> sys.stderr, "Error in sentence:", sentence, sys.exc_info()
            break

def clear_sequence(sequence, sequences):
    if sequence:
        sequences.append(copy_list(sequence))
        del sequence[:]

def sequences_in(sentence):
    sequences = []
    sequence_nominal = []
    sequence_other = []
    pos_tag_prev = " "
    for token in sentence:
        pos_tag = token[1]
        w = token[0]
        w_pos_tag = w + "/" + pos_tag
        if pos_tag[0] not in ["N", "J"]:
            sequence_other.append(w_pos_tag)
            if sequence_nominal:
                clear_sequence(sequence_nominal, sequences)
        else:
            sequence_nominal.append(w_pos_tag)
            if sequence_other:
                clear_sequence(sequence_other, sequences)
        
        pos_tag_prev = pos_tag
    else:
        clear_sequence(sequence_nominal, sequences)
        clear_sequence(sequence_other, sequences)
    return sequences

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
        sentences_col_fmt = open(file_name, "rU")
        extract_sequences(sentences_col_fmt)        
        sentences_col_fmt.close()
    except:
      print >> sys.stderr, "Error:", sys.exc_info()


