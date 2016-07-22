#!/usr/bin/python 
import sys
from os import walk
from os import mkdir
from os import path
from xml.dom import minidom
from nltk import word_tokenize 
from nltk.tag.perceptron import PerceptronTagger

def strip_end_slash(str_path):
    if str_path.endswith('/'):
        str_path = str_path[:-1]
    return str_path

def change_file_extention(str_path, ext, new_ext):
    return str_path[::-1].replace(ext[::-1], new_ext[::-1], 1)[::-1]

def save_to_file(output_file, data):
    print output_file
    foutput = open(output_file, "w")
    for e in data:
        print >> foutput, e
        print >> foutput
    foutput.close()

def get_list_files(path):
    walking = walk(path)
    directory_content = []
    for step in walking:
        directory_content.append(step)
    return directory_content

def new_paths(directory_content, input_path, output_path):
    paired_paths = []
    try:
        input_path = strip_end_slash(input_path)
        mkdir(output_path)
        for cur_content in directory_content:
            cur_path = strip_end_slash(cur_content[0])
            for list_content in cur_content[1:]:
                if list_content:
                    for resource in list_content:
                        resource_path = cur_path + "/" + resource
                        resource_new_path = resource_path.replace(input_path, output_path, 1)
                        if path.isdir(resource_path):
                            mkdir(resource_new_path)
                        elif  path.isfile(resource_path):
                            paired_paths.append((resource_path, resource_new_path))
    except:
        print >> sys.stderr, "Error:", sys.exc_info()
        print >> sys.stderr
        print >> sys.stderr, "Make sure that", output_path, "doesn't exists."
    return paired_paths

def pos_title_abstract(resource):
    xml_file = resource[0]
    pos_data = []
    try:
        xmldoc = minidom.parse(xml_file)
        elements_title = xmldoc.getElementsByTagName("Title")
        title =  elements_title.item(0).childNodes[0].nodeValue
        elements_list = xmldoc.getElementsByTagName("S")
        sentences = [e[0].nodeValue for e in [element.childNodes for element in elements_list] if e[0].nodeType == e[0].TEXT_NODE]
        sentences.insert(0, title)
        #raw text 
        txt_file = change_file_extention(resource[1], "xml", "txt")
        save_to_file(txt_file, sentences)
        #pos
        tagger = PerceptronTagger()
        for s in sentences:
            tokens = word_tokenize(s)
            pos_data.append(tagger.tag(tokens))
        pos_file = change_file_extention(resource[1], "xml", "pos")
        save_to_file(pos_file, pos_data)
    except:
        print >> sys.stderr, "Error pos_title_abstract:", resource, sys.exc_info()

    return pos_data 

if __name__ == "__main__":
    try:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        resources = new_paths(get_list_files(input_path), input_path, output_path)

        for resource in resources:
            pos_title_abstract(resource)

    except:
        print >> sys.stderr, "Error:", sys.exc_info()
        print >> sys.stderr
        print >> sys.stderr, "usage: python", sys.argv[0], "<directory> <output directory>"
        print >> sys.stderr, "example:"
        print >> sys.stderr, "    python", sys.argv[0], "acl-rd-tec-2.0/distribution/raw_abstract_txt/ titles_and_abstracts" 
