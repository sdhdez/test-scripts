#!/usr/bin/python 
import sys
import os
import mdb_common_lib as mdbcl
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
from nltk.tag.perceptron import PerceptronTagger
import nltk.data
import re
import kpcommon

from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

if __name__ == "__main__":
    try:
        debug = True if sys.argv[-1] == "debug" else False
        debug_tests = 1
        file_count = 0

        try:
            dir_corpus = sys.argv[1]
            dir_output = sys.argv[2]
        except:
            print >> sys.stderr, "E) Directories: ", sys.exc_info()

        try:
            pos_sequences_filename = sys.argv[3]
            count_limit = int(sys.argv[4])
            pos_sequences, is_posregex = kpcommon.get_pos_tags_by_count(pos_sequences_filename, count_limit)
        except:
            print >> sys.stderr, "E) Common tags: ", sys.exc_info()

        qr = mdbcl.QueryResources()
        tokenizer = Tokenizer()
        tagger = PerceptronTagger()
        lemmatizer = WordNetLemmatizer()
        stemmer = LancasterStemmer()
        
        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-4:]
                if ext == '.txt':
                    file_count += 1 #debug
                    if debug and file_count > debug_tests: #debug
                        break #debug
                    print file_count, f[:-4]
                    try:
                        file_text = os.path.join(dirname, f[:-4] + ".txt")
                        text_file = open(file_text, "r")
                        raw_text = unicode(text_file.read(), encoding="utf-8")
                        file_kpe = os.path.join(dir_output, f[:-4] + ".ann")
                        kpe_file = open(file_kpe, "w")
                    except:
                        print >> sys.stderr, "E) Open files: ", sys.exc_info()

                    text_tokens = tokenizer.tokenize(raw_text)
                    text_tokens = kpcommon.escape_not_abbreviations(text_tokens)
                    #if debug:
                    #    print text_tokens, len(text_tokens)

                    pos_tags = tagger.tag(text_tokens)
                    pos_tags_string = " ".join([pt[1] for pt in pos_tags])
                    #print "\n".join([str(ptstr) for ptstr in pos_tags])
                    kps_candidates = {}
                    test_match = 0
                    for ct in pos_sequences:
                        if is_posregex:
                            pos_regex = re.compile("\s?(" + ct[2] + ")\s")
                        else:
                            pos_regex = re.compile("\s?(" + re.escape(ct[2]) + ")\s")
                        for pos_match in re.finditer(pos_regex, pos_tags_string):
                            pos_match_string = pos_match.group(1)
                            pos_seq_start = pos_match.start(1)
                            pos_seq_end = pos_match.end(1)
                            token_index_start = len(pos_tags_string[:pos_seq_start].split())
                            token_offset = len(pos_tags_string[pos_seq_start:pos_seq_end].split())
                            token_index_end = token_index_start + token_offset
                            real_pos_seq =  " ".join([pos_i for tok_i, pos_i in pos_tags[token_index_start:token_index_end]])
                            real_token_seq =  " ".join([tok_i for tok_i, pos_i in pos_tags[token_index_start:token_index_end]])
                            if debug:
                                pass
                                #print pos_seq_start, pos_seq_end, token_index_start, token_offset, 
                                #print pos_tags[token_index_start:token_index_end]
                                #print pos_match_string == pos_tags_string[pos_seq_start:pos_seq_end], 
                                #print pos_match_string == real_pos_seq, real_pos_seq, 
                                #print real_token_seq
                            if pos_match_string == real_pos_seq:
                                is_pos_valid = True
                                for pt in pos_tags[token_index_start:token_index_end]:
                                    if kpcommon.is_pos_error(pt[0], pt[1]):
                                        is_pos_valid = False
                                        break
                                if is_pos_valid:
                                    test_match += 1
                                    kps_candidates.setdefault(real_token_seq, [0, set()])
                                    kps_candidates[real_token_seq][0] += 1 
                                    kps_candidates[real_token_seq][1].add(str(ct))
                    #if debug:
                        #print >> sys.stderr, "-- Match:", test_match

                    #print kps_candidates, len(kps_candidates)
                    #if debug:
                    #    print "\n".join([str(c) for c in kps_candidates.items()]), len(kps_candidates)
                    i = 0
                    tmp_kps_candidates = []
                    for kp in kps_candidates.keys():
                        """
                        kp_tokens = [t for t in tokenizer.tokenize(kp) if t not in stopwords.words('english')]
                        lemma_keywords_str = " ".join([lemmatizer.lemmatize(kp_token) for kp_token in kp_tokens])
                        stem_keywords_str = " ".join([stemmer.stem(kp_token) for kp_token in kp_tokens])
                        query_r = qr.is_keyword(stem_keywords_str, exact = True, not_by_keyword = 'stem')
                        if not query_r:
                            continue
                        """
                        """
                        query_r = qr.is_keyword(kp, exact = True)
                        if not query_r:
                            continue
                        """
                        """
                        query_r = qr.is_keyword(kp, exact = True, of_interest = False)
                        if query_r:
                            continue
                        """
                        for m in re.finditer("\W?(" + re.escape(kp) + ")\W", raw_text):
                            #m = re.search(re.escape(term[2]), text)
                            start = m.start(1)
                            end = m.end(1)
                            i += 1
                            pos_seq_str = eval(list(kps_candidates[kp][1])[0])[2]
                            term_string = "T" + str(i) + "\tNone " + str(start) + " " + str(end) + "\t" + raw_text[start:end] + "\t" + pos_seq_str
                            term_string = term_string.encode("utf-8")
                            print >> kpe_file, term_string
                            tmp_kps_candidates.append((start, end, m.span(1), kp, raw_text[start:end]))
                    kps_candidates = sorted(tmp_kps_candidates, key=lambda tup: tup[0])
                    if debug:
                        pass
                        #print "\n".join([str(c) for c in kps_candidates])
                        #print "Candidates:", len(kps_candidates)
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
