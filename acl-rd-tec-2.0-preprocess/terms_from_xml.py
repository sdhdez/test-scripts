#!/usr/bin/python 
import sys
import os.path
from xml.dom import minidom

element_to_extract = sys.argv[1]
xml_file = sys.argv[2]

text_extracted = {}
if os.path.isfile(xml_file):
    try:
        xmldoc = minidom.parse(xml_file)
        elements_list = xmldoc.getElementsByTagName(element_to_extract)
        text_list = [e[0].nodeValue for e in [element.childNodes for element in elements_list] if e[0].nodeType == e[0].TEXT_NODE] 
        for t in text_list:
            text_extracted.setdefault(t, 0)
            text_extracted[t] += 1
    except:
        print >> sys.stderr, "xml_file:", xml_file, sys.exc_info()[0]

print text_extracted
