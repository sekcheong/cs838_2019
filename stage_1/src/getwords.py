#!/usr/bin/env python3
import os
import re
import unicodedata
import glob

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def tokenize(filePath):
    file  = open(filePath, 'r')
    lines =  file.readlines()
    file.close()
    tag = 'name'
    tokens = []
    for l in lines:
        words = re.split('(\\<'+tag+'\\>|\\<\\/'+tag+'\\>|\\W)', l)
        for w in words:
            w = w.strip()
            if len(l)>0:
                tokens.append(w)
    return tokens
        
if __name__ == '__main__':
    files = glob.glob('../data/etc/bbc' + '/**/*.txt', recursive=True)
    files = sorted(files)
    dict = {}
    for file in files:
       tokens = tokenize(file)
       for k in tokens:
           if not k in dict:
               dict[k] = ""

    words = dict.keys()
    words = sorted(words)
    #print(len(words))

    with open('../data/etc/words.txt', 'w') as outFile:
        for w in words:
            outFile.write(w+'\n')