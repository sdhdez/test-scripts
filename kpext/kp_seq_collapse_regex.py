#!/usr/bin/python 
import sys
import re
import operator 

if __name__ == "__main__":
    try:
        common_tags_filename = sys.argv[1]
        tags_file = open(common_tags_filename, "r")

        try:
            tmp_sequences = {}
            pos_general_regex = re.compile(r"((\w+)\\\+)")
            for ct in tags_file:
                ct_fields = ct.strip().split("\t")
                prev_pos_tag = ""
                pos_tags_string = ""
                pos_tags = ct_fields[2].split()
                for pt in pos_tags:
                    if prev_pos_tag == pt:
                        if pos_tags_string and pos_tags_string[-1] != "+":
                            pos_tags_string += "+"
                    else:
                        pos_tags_string += (" " + pt)
                    prev_pos_tag = pt 
                seq_id = pos_tags_string.replace("+", "")
                tmp_sequences.setdefault(seq_id, [])
                tmp_sequences[seq_id].append(ct_fields[1:] + [pos_tags_string.strip()])
            sequences = {}
            for seq_id, eq_seqs in tmp_sequences.items():
                main_seq = ""
                tmp_sum_seq_ocurrences = 0
                for eq in eq_seqs:
                    if len(eq[2]) > len(main_seq):
                        main_seq = eq[2]
                    tmp_sum_seq_ocurrences += int(eq[0])
                escaped_main_seq = re.escape(main_seq)
                main_seq = re.sub(pos_general_regex, r"(\g<2>)+", escaped_main_seq)
                sequences.setdefault(main_seq, 0)
                sequences[main_seq] += tmp_sum_seq_ocurrences
            print "\n".join(["POSREGEX" + str(i) + "\t" + str(s[1]) + "\t" + s[0] 
                for i, s in enumerate(sorted(sequences.items(), key=operator.itemgetter(1)), start=1)])
        except:
            print >> sys.stderr, "E) Sequences: ", sys.exc_info()

    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<extracted_sequences>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "train_common_pos_tags.dat output.dat" 
        print >> sys.stderr, "Error: ", sys.exc_info()
