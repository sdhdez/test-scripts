#!/usr/bin/python 
import sys
import os
import mdb_common_lib as mdbcl
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
from nltk.tag.perceptron import PerceptronTagger
import nltk.data
import re
import kpcommon

def reset_kp_search():
    return [], 0, False 

if __name__ == "__main__":
    try:
        debug = True if sys.argv[-1] == "debug" else False
        debug_tests = 1
        file_count = 0

        dir_corpus = sys.argv[1]
        dir_output = sys.argv[2]

        try:
            common_tags = sys.argv[3]
            count_limit = int(sys.argv[4])
            tags_file = open(common_tags, "r")
            common_tags = []
            for ct in tags_file:
                ct_fields = ct.strip().split("\t")
                if int(ct_fields[1]) < count_limit:
                    continue
                if debug:
                    print ct_fields
                common_tags.append([t for t in ct_fields])
        except:
            print >> sys.stderr, "E) Common tags: ", sys.exc_info()

        qr = mdbcl.QueryResources()
        tokenizer = Tokenizer()
        tagger = PerceptronTagger()

        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-3:]
                if ext == 'txt':

                    file_count += 1 #debug
                    if debug and file_count > debug_tests: #debug
                        break #debug

                    print file_count, f[:-4]
                    try:
                        file_text = os.path.join(dirname, f[:-3] + "txt")
                        text_file = open(file_text, "r")
                        raw_text = unicode(text_file.read(), encoding="utf-8")

                        file_kpe = os.path.join(dir_output, f[:-3] + "ann")
                        kpe_file = open(file_kpe, "w")
                    except:
                        print >> sys.stderr, "E) Open files: ", sys.exc_info()

                    text_tokens = tokenizer.tokenize(raw_text)
                    text_tokens = kpcommon.escape_not_abbreviations(text_tokens)
                    if debug:
                        print text_tokens

                    pos_tags = tagger.tag(text_tokens)
                    pos_tags_string = " ".join([pt[1] for pt in pos_tags])
                    #print "\n".join([str(ptstr) for ptstr in pos_tags])
                    kps_candidates = {}
                    for ct in common_tags:
                        if ct[2] in pos_tags_string:
                            tags = ct[2].split(" ")
                            t_index = 0
                            n_tags = len(tags)
                            start = False
                            keyphrase = []
                            for pt in pos_tags:
                                if kpcommon.is_pos_error(pt[0], pt[1]):
                                    keyphrase, t_index, start = reset_kp_search()
                                    continue
                                if n_tags > t_index:
                                    if pt[1] == tags[t_index] and not start:
                                        start = True
                                        t_index += 1
                                        keyphrase.append(pt[0])
                                        #print start, pt, t_index, n_tags, tags
                                        continue 
                                    if start and pt[1] == tags[t_index]:
                                        keyphrase.append(pt[0])
                                        t_index += 1
                                    elif start and pt[1] != tags[t_index]:
                                        keyphrase, t_index, start = reset_kp_search()
                                    continue 
                                if start:
                                    final_kp = " ".join(keyphrase)
                                    kps_candidates.setdefault(final_kp, [0, set()])
                                    kps_candidates[final_kp][0] += 1 
                                    kps_candidates[final_kp][1].add(str(ct))
                                    keyphrase, t_index, start = reset_kp_search()
                    #print kps_candidates, len(kps_candidates)
                    if debug:
                        print "\n".join([str(c) for c in kps_candidates.items()]), len(kps_candidates)
                    i = 0
                    tmp_kps_candidates = []
                    for kp in kps_candidates.keys():
                        """
                        query_r = qr.is_keyword(kp, exact = False)
                        if not query_r:
                            continue
                        """
                        for m in re.finditer("\W?(" + re.escape(kp) + ")\W", raw_text):
                            #m = re.search(re.escape(term[2]), text)
                            start = m.start(1)
                            end = m.end(1)
                            i += 1
                            term_string = "T" + str(i) + "\tNone " + str(start) + " " + str(end) + "\t" + raw_text[start:end]
                            term_string = term_string.encode("utf-8")
                            print >> kpe_file, term_string
                            tmp_kps_candidates.append((start, end, m.span(1), kp, raw_text[start:end]))
                    kps_candidates = sorted(tmp_kps_candidates, key=lambda tup: tup[0])
                    if debug:
                        print "\n".join([str(c) for c in kps_candidates]), len(kps_candidates)
                    text_file.close()
                    kpe_file.close()
                else:
                    continue
    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
