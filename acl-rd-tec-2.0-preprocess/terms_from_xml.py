#!/usr/bin/python 
import sys
import os.path
from xml.dom import minidom

try:
    xml_file = sys.argv[1]
except:
    xml_file = sys.stdout

if os.path.isfile(xml_file):
    try:
        xmldoc = minidom.parse(xml_file)
        elements_list = xmldoc.getElementsByTagName("term")
        text_list = [e[0].nodeValue for e in [element.childNodes for element in elements_list] if e[0].nodeType == e[0].TEXT_NODE] 
        for t in text_list:
            print t
    except:
        print >> sys.stderr, "xml_file:", xml_file, sys.exc_info()[0]

