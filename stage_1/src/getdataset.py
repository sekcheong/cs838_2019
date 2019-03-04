#!/usr/bin/env python3
import re
import unicodedata

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def should_include(a):
    return not a.isspace()

def load_names(filePath):
    file  = open(filePath, 'r')
    lines =  file.readlines()
    file.close()
    names = {}
    for l in lines:
        p = re.split('\\s', l)
        names[p[0]]=""
        print(p[0])
    
#def load_last_names():


load_names('../data/etc/names/dist.all.last.txt')


# v = re.split('(\\W)', '\'sfoo/ "bar "" . spam "Hi",   \tSt. Mr. Eggo McEggHead\neggs')
# l = [a.strip() for a in v if not a.isspace()] 
# for x in l:
#     print(len(x))
#     print("|"+x+"|")
