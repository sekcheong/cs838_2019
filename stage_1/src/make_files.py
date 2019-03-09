#!/usr/bin/env python3
import os
import glob
import random
from shutil import copyfile

def split_list(dataset, ratio):
    random.shuffle(dataset)
    s = int(len(dataset) * ratio)
    test = []
    train = []
    for i in range(0, s):
        #print (i)
        test.append(dataset[i])

    for i in range(s, len(dataset)):
        #print (i)
        train.append(dataset[i])
    return train, test

files = glob.glob('../data/txt' + '/**/*.txt', recursive=True)
random.seed(838)
train, test = split_list(files, 0.3333)

print(len(train))
print(len(test))
counter = 1 

with open('../data/train.txt', 'w') as outFile:
    for f in train:
        fname = format(counter, "03d") + ".txt"
        copyfile(f, '../data/I/'+fname)
        counter = counter + 1
        outFile.write('/I/' + fname +'\n')

with open('../data/test.txt', 'w') as outFile:
    for f in test:
        fname = format(counter, "03d") + ".txt"
        copyfile(f, '../data/J/'+fname)
        counter = counter + 1
        outFile.write('/J/' + fname +'\n')