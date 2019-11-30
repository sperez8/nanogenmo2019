import sys
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import string
from collections import Counter
import re

text_for_testing = '''
# Suddenly, Alice devoured the apple with green leaves.
# The cat devoured the leaves.
# Alice's eyes widened. 
# Cat!, yelled Alice.
# The cat ran away down the corridor.
# '''

f1 = open('A tale of two cities.txt','r')
text1 = '\n'.join([line.decode('utf-8').strip() for line in f1.readlines()])
f1.close()

def get_nouns(text):
	#get all words
	tokens = word_tokenize(text)
	# convert to lower case
	tokens = [w.lower() for w in tokens]
	# remove punctuation from each word
	exclude = set(string.punctuation)
	stripped = [''.join([ch for ch in w if ch not in exclude]) for w in tokens]
	# remove remaining tokens that are not alphabetic
	words = [word for word in stripped if word.isalpha()]
	# filter out stop words
	from nltk.corpus import stopwords
	stop_words = set(stopwords.words('english'))
	words = [w for w in words if not w in stop_words]

	tags = nltk.pos_tag(words)
	nouns = [word for word,pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
	return nouns


nouns1 = get_nouns(text1)
N = len(nouns1)
topN = zip(*Counter(nouns1).most_common(N))[0]
leastN = zip(*Counter(nouns1).most_common()[:-N-1:-1])[0]

convert = {t:l for t,l in zip(topN,leastN)}
convert.update({t.capitalize():l.capitalize() for t,l in zip(topN,leastN)})
# for t,l in zip(topN,leastN):
# 	print t,l

f_out = open('mashup.txt','w')

#we use word boundaries (\b), otherwise the characters 'air' in 'despair' gets replaced
rep = dict(('\\b'+k+'\\b', v) for k, v in convert.iteritems()) 
pattern = re.compile("|".join(rep.keys()))
mashed_text = pattern.sub(lambda m: rep['\\b'+m.group(0)+'\\b'], text1)
f_out.write(mashed_text.encode('utf8'))
f_out.close()
