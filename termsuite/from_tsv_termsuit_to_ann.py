import sys 
import os
import re

if __name__ == "__main__":
    try:
        dir_termsuit_result = sys.argv[1]
        dir_texts = sys.argv[2]
        dir_ann = sys.argv[3]
        set_wrlog = float(sys.argv[4])
        delimiters = [" ", ",", ".", ":", "(", ")", "-"]
        for (dirname, _, filenames) in os.walk(dir_termsuit_result):
            for f in filenames:
                ext = f[-3:]
                if ext == 'tsv':
                    file_terms = os.path.join(dirname, f)
                    file_text = os.path.join(dir_texts, f[:-14] + ".txt" )
                    file_ann = os.path.join(dir_ann, f[:-14] + ".ann" )
                    file_stream = open(file_terms, 'r')
                    file_stream_txt = open(file_text, 'r')
                    file_output_ann = open(file_ann, 'w')
                    text = file_stream_txt.read()
                    #print file_text, len(text)
                    text = unicode(text, encoding="utf-8")
                    i = 0
                    for line in file_stream:
                        term = line.strip("\n").split("\t")
                        #if term[1] != "type": #incuding V
                        if term[1] == "T": #only T 
                            wrlog = float(term[3].replace(",", "."))
                            if wrlog < set_wrlog:
                                continue
                            #print term 
                            for m in re.finditer(re.escape(term[2]), text):
                                #m = re.search(re.escape(term[2]), text)
                                start = m.start()
                                end = m.end()
                                if text[start - 1] in delimiters and text[end] in delimiters:
                                    i += 1
                                    print >> file_output_ann, u"T" + str(i) + "\tProcess", str(start), str(end) + "\t" + term[2]
                                    #print "T" + str(i) + "\tProcess", str(start), str(end) + "\t" + term[2]
                    file_stream.close()
                    file_stream_txt.close()
                    file_output_ann.close()
    except:
        print >> sys.stderr, "Error:", sys.exc_info()
