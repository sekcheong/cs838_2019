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


def load_names(filePath):
    file  = open(filePath, 'r')
    lines =  file.readlines()
    file.close()
    names = {}
    for l in lines:
        p = re.split('\\s', l)
        n = p[0]
        if not n in names:
            names[n] = 0
            # print(p[0])
    return names


def load_first_last_names():
    lastNames = load_names('../data/etc/names/dist.last.txt')
    fnames = load_names('../data/etc/names/dist.female.first.txt')
    mnames = load_names('../data/etc/names/dist.male.first.txt')

    #combine male and female names in on dict
    firstNames = {}
    for n in fnames.keys():
        if not n in firstNames:
            firstNames[n] = 0
    for n in mnames.keys():
        if not n in firstNames:
            firstNames[n] = 0
    return (lastNames, firstNames)


def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).next()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files:                                                                                        
                r.append(subdir + "/" + file)                                                                         
    return r       


def tokenize(filePath):
    file  = open(filePath, 'r')
    lines =  file.readlines()
    file.close()
    tokens = []
    for l in lines:
        words = re.split('(\\W)', l)
        for w in words:
            w = w.strip()
            if len(l)>0:
                tokens.append(w)
    return tokens

def clear_name_count(lastNames, firstNames):
    for w in lastNames:
        lastNames[w] = 0
    for w in firstNames:
        firstNames[w] = 0
    
def get_name_count(filePath, lastNames, firstNames):
    tokens = tokenize(filePath)
    for w in tokens:
        #w = strip_accents(w)
        w = w.upper()
       
        if w in firstNames:
            #print (w)
            firstNames[w] = firstNames[w] + 1
        elif w in lastNames:
            lastNames[w] = lastNames[w] + 1

def get_unique_name_count(lastNames, firstNames):
    last = 0
    first = 0

    for w in lastNames:
        if lastNames[w]>0:
            # print(w)
            last = last + 1

    for w in firstNames:
        if firstNames[w]>0:
            first = first + 1

    return (last, first)
        
if __name__ == '__main__':
    (lastNames, firstNames) = load_first_last_names()
    files = glob.glob('../data/etc/bbc' + '/**/*.txt', recursive=True)
    files = sorted(files)
    # file = '../data/etc/bbc/tech/401.txt'
    # get_name_count(file, lastNames, firstNames)
    # (lcnt, fcnt) = get_unique_name_count(lastNames, firstNames)
    # print(file, lcnt, fcnt)
    for file in files:
        get_name_count(file, lastNames, firstNames)
        (lcnt, fcnt) = get_unique_name_count(lastNames, firstNames)
        clear_name_count(lastNames, firstNames)
        print(file, "," ,lcnt, ",", fcnt)

    #l = list_files('../data/etc/bbc')
    # lastNames = load_names('../data/etc/names/dist.all.last.txt')
    # fnames = load_names('../data/etc/names/dist.female.first.txt')
    # mnames = load_names('../data/etc/names/dist.male.first.txt')

    # #combine male and female names in on dict
    # firstNames = {}
    # for n in fnames.keys():
    #     if not n in firstNames:
    #         firstNames[n] = 0
    # for n in mnames.keys():
    #     if not n in firstNames:
    #         firstNames[n] = 0
    # for x in firstNames:
    #     print (x)



# v = re.split('(\\W)', '\'sfoo/ "bar "" . spam "Hi",   \tSt. Mr. Eggo McEggHead\neggs')
# l = [a.strip() for a in v if not a.isspace()] 
# for x in l:
#     print(len(x))
#     print("|"+x+"|")


