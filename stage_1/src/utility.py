import re
import math
import nltk
import random

TAG = "N"
NUMBIN = 5
ps = nltk.PorterStemmer()

def load_worddir(worddir_path):
	worddir = {}
	with open(worddir_path, 'r') as file:
		lines = file.readlines()
		for i in range(len(lines)):
			worddir[lines[i].strip()] = i
	return worddir

def get_prev(words, pos):
	if pos==0 or '.' in words[pos-1]:
		return None
	pos-=1
	while pos>=0:
		raw_word = get_raw_text(words[pos:pos+1])
		if raw_word[0].isalpha():
			break
		pos-=1
	return words[pos] if pos>=0 else None

def get_next(words, pos):
	if '.' in words[pos]:
		return None
	pos+=1
	while pos<len(words):
		raw_word = get_raw_text(words[pos:pos+1])
		if raw_word[0].isalpha():
			break
		pos+=1
	return words[pos] if pos<len(words) else None

def is_endpoint(word):
	if word:
		return 1
	else:
		return 0

def is_capital(word):
	if not word:
		return 0
	if word.istitle():
		return 1
	return 0

def is_suf_punctutation(word):
	if not word:
		return 0
	punctutation = [',', '.']
	for p in punctutation:
		if p in word:
			return 1
	return 0

def is_suf_who(word):
	if not word:
		return 0
	words = ["who", "whose", "whom"]
	for w in words:
		if ps.stem(w) == ps.stem(word):
			return 1
	return 0

def is_prev_title(word):
	if not word:
		return 0
	# words = ["Mr", "Ms", "Miss", "Dr", "Prof", "Professor", "Lord", "Father",
	# "Fr", "Rabbi", "Cardinal", "Sir", "Chancellor", "President", "CEO",
	# "Minister", "Chef", "solicitor", "MPS"]
	words = ["Boss",
        "Br",
        "Captain",
        "Cardinal",
        "CEO",
        "Chancellor",
        "Chef",
        "Chief",
        "Commander",
        "Dame",
        "Dean",
        "Director",
        "Doctor",
        "Dr",
        "Elder",
        "Father",
        "Fr",
        "Honorable",
		"Imam",
		"Judge",
		"Lady",
		"Lieutenant",
		"Lord",
		"Madam",
		"Master",
		"Minister",
		"Miss",
		"MPS",
		"Mr",
		"Mrs",
		"Ms",
		"Officer"
		"Pastor",
		"Pr",
		"President",
		"Principal",
		"Prof",
		"Professor",
		"Provost",
		"Rabbi",
		"Rector",
		"Regent",
		"Rev",
		"Reverend",
		"Secretary",
		"Sir",
		"Solicitor",
		"Sr",
		"Warden"]
	for w in words:
		if ps.stem(w) == ps.stem(word):
			return 1
	return 0

def is_possessive(word):
	if not word:
		return 0
	if "'" in word:
		return 1
	return 0

def is_prev_pos(word):
	if not word:
		return 0
	words = ["include", "by"]
	for w in words:
		if ps.stem(w) == ps.stem(word):
			return 1
	return 0

def is_next_pos(word):
	if not word:
		return 0
	words = ["said", "told", "will", "has", "is"]
	for w in words:
		if ps.stem(w) == ps.stem(word):
			return 1
	return 0

def is_prev_neg(word):
	if not word:
		return 0
	words = ["the", "a", "an"]
	for w in words:
		if ps.stem(w) == ps.stem(word):
			return 0
	return 1

def get_feature(raw_words, words, prev, next, worddir):
	feature = [0 for _ in range(math.ceil(len(worddir)/NUMBIN))]
	for word in raw_words:
		pos = worddir[ps.stem(word)]
		feature[pos//NUMBIN] = 1
	feature.append(is_endpoint(prev))
	feature.append(is_endpoint(next))
	feature.append(is_suf_punctutation(words[-1]))
	feature.append(is_suf_who(next))
	feature.append(is_prev_title(prev))
	feature.append(is_possessive(words[-1]))
	# feature.append(is_capital(prev))
	# feature.append(is_capital(next))
	feature.append(is_prev_pos(prev))
	# feature.append(is_prev_neg(prev))
	feature.append(is_next_pos(next))
	return feature

def get_label_and_remove_tag(words):
	label = 0
	tag_begin = "<"+TAG+">"
	tag_end = "</"+TAG+">"
	if tag_begin in words[0] or tag_end in words[-1]:
		label = 1
		for i in range(1, len(words)-1):
			if tag_begin in words[i] or tag_end in words[i]:
				label = 0
	remove_tag = []
	for word in words:
		new_word = re.sub(tag_begin+"|"+tag_end, "", word)
		remove_tag.append(new_word)
	return label, remove_tag

def get_raw_text(words):
	new_words = []
	for word in words:
		new_word = re.sub("\'\w+", "", word)
		new_word = re.sub("\.\w+", "", new_word)
		new_word = re.sub("-\w+", "", new_word)
		new_word = re.sub("\W+", "", new_word)
		new_words.append(new_word)
	return new_words

def check_valid(words):
	for word in words:
		if not word.istitle() or not word.isalpha():
			return False
	return True

def sample_data(file, worddir):
	features = []
	labels = []
	lines = None
	with open(file, 'r') as fi:
		lines = fi.readlines()
	for line in lines:
		words = line.strip().split(' ')
		for i in range(len(words)):
			for j in range(i+1, min(len(words), i+3)+1):
				label, sample_words = get_label_and_remove_tag(words[i:j])
				sample_words = get_raw_text(sample_words)
				if check_valid(sample_words):
					if label == 0 and random.random()>0.3:
						continue
					prev = get_prev(words, i)
					next = get_next(words, j-1)
					feature = get_feature(sample_words, words, prev, next, worddir)
					features.append(feature)
					labels.append(label)
	return features, labels