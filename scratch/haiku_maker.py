import numpy as np
from nltk.corpus import cmudict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stopWords = set(stopwords.words('english'))


d = cmudict.dict()
def nsyl(word):
	"""Count syllables, or -1 if not found"""
	try:
		return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
	except:
		return -1

def text_to_word_list(text):
	"""Given text, clean it and format it into a word list"""
	text = text.lower()
	text = text.strip()
	for i in ',.?!:;*-"(){}[]@$%\n':
		text = text.replace(i, ' ')

	text = text.replace("' ", ' ')
	text = text.replace(" '", ' ')
	words = text.split()

	filtered_words = []
	for i in words:
		if len(i) == 1 and not i in ('a', 'i'):
			continue
		filtered_words.append(i)
	return filtered_words

def lazy_haiku_maker(words):
	"""
	Given a list of words, return a haiku as a string
	Returns None if fails
	"""
	syllables = [nsyl(x) for x in words]
	state = 0
	count = 0
	haiku = [[],[],[]]
	for i, j in zip(words, syllables):
		if j == -1:
			continue
		if j + count > 5:
			continue
		haiku[state].append(i)
		count += j
		if count == 5:
			if state == 0:
				state = 1
				count = -2
			elif state == 1:
				state = 2
				count = 0
			elif state == 2:
				return haiku
	return None

def bagging_haiku_maker(words, keep_chance=0.75, iterations=2000):
	"""
	Given a list of words, generate a haiku by randomly dropping words
	Returns None if fails
	"""
	for i in range(iterations):
		new_words = [x for x in words if np.random.rand() < keep_chance]
		if not new_words or len(new_words) <= 1:
			continue
		new_words = new_words[np.random.randint(len(new_words) - 1):]
		haiku = lazy_haiku_maker(new_words)
		if not haiku:
			continue
		if haiku[0][-1] in stopWords:
			continue
		if haiku[1][-1] in stopWords:
			continue
		if haiku[2][-1] in stopWords:
			continue
		if np.sum([1 for x in sum(haiku, []) if x in stopWords]) > 3:
			continue
		return "\n".join(list(map(lambda x : " ".join(x), haiku)))
	return None

def text2haiku(text, keep_chance=0.75, iterations=2000):
	"""
	Given a string of text, try to make a haiku
	returns a haiku as a string or None if it fails
	"""
	word_list = text_to_word_list(text)
	haiku = bagging_haiku_maker(word_list, keep_chance=keep_chance, iterations=iterations)
	return haiku


if __name__ == '__main__':
	import sys
	infile = sys.argv[1]
	with open(infile, 'r') as f:
		for i in f:
			haiku = text2haiku(i, keep_chance=0.75)
			if haiku:
				print("*************************")
				print(i)
				print("_________________________")
				print(haiku)
				print("*************************\n")
				input()
