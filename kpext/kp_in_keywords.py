#!/usr/bin/python 
import sys
import os
import mdb_common_lib as mdbcl

if __name__ == "__main__":
    try:
        dir_corpus = sys.argv[1]
        dir_output = sys.argv[2]
        qr = mdbcl.QueryResources()
        for (dirname, _, filenames) in os.walk(dir_corpus):
            for f in filenames:
                ext = f[-3:]
                if ext == 'ann':
                    file_ann = os.path.join(dirname, f[:-3] + "ann")
                    ann_file = open(file_ann, "r")
                    file_kpe = os.path.join(dir_output, f[:-3] + "ann")
                    kpe_file = open(file_kpe, "w")

                    print f[:-4]
                    for ann in ann_file:
                        if ann[0] not in ["R", "*"]:
                            ann_items = ann.strip().split("\t")
                            ann_text = unicode(ann_items[2], encoding="utf-8")
                            #search kp
                            query_r = qr.is_keyword(ann_text, exact = True)
                            if query_r:
                                print >> kpe_file, ann,
                    ann_file.close()
                    kpe_file.close()
    except:
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<corpus_dir_path> <output_dir_path>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "some/path/to/corpus/ some/path/to/output/" 
        print >> sys.stderr, "Error: ", sys.exc_info()
