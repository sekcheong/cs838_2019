import re
import nltk

TAG = "N"
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
	words = ["Mr", "Ms", "Miss", "Dr", "Prof", "Professor", "Lord", "Father",
	"Fr", "Rabbi", "Cardinal", "Sir", "Chancellor", "President", "CEO",
	"Minister", "Chef", "solicitor", "MPS"]
	for w in words:
		if ps.stem(w) == ps.stem(word):
			return 1
	return 0

def is_prev_pos(word):
	if not word:
		return 0
	words = ["include"]
	for w in words:
		if ps.stem(w) == ps.stem(word):
			return 1
	return 0

def is_next_pos(word):
	if not word:
		return 0
	words = ["said"]
	for w in words:
		if ps.stem(w) == ps.stem(word):
			return 1
	return 0

def get_feature(raw_words, words, prev, next, worddir):
	feature = [0 for _ in range(len(worddir))]
	for word in raw_words:
		pos = worddir[ps.stem(word)]
		#print(pos)
		feature[pos] = 1
	feature.append(is_endpoint(prev))
	feature.append(is_endpoint(next))
	feature.append(is_suf_punctutation(words[-1]))
	feature.append(is_suf_who(next))
	feature.append(is_prev_title(prev))
	feature.append(is_prev_pos(prev))
	feature.append(is_next_pos(next))
	#print(len(feature))
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
		words = lines[4].strip().split(' ')
		for i in range(len(words)):
			for j in range(i+1, min(len(words), i+3)+1):
				label, sample_words = get_label_and_remove_tag(words[i:j])
				sample_words = get_raw_text(sample_words)
				if check_valid(sample_words):
					#print(label, sample_words)
					prev = get_prev(words, i)
					next = get_next(words, j-1)
					#print(prev, next)
					feature = get_feature(sample_words, words, prev, next, worddir)
					features.append(feature)
					labels.append(label)
	return features, labels