from sklearn.feature_extraction.text import TfidfTransformer
from random import shuffle
from math import floor
from pathlib import Path
import nltk
nltk.download('wordnet')
import os


tfidfconverter = TfidfTransformer()


def get_flist(d):
	if Path(d).exists():
		all_files = os.listdir(os.path.abspath(d))
		data_files = list(filter(lambda file: file.endswith('.txt'), all_files))
		return shuffle(data_files)
	else:
		print('[!] Path {0} does not exist'.format(d))
		return False


def get_training_testing(fl):
	split = 0.7
	split_index = floor(len(fl) * split)
	training = fl[:split_index]
	testing = fl[split_index:]
	return training, testing


def prep_training(X):
	documents = []
	for sen in range(0, len(X)):
		document = re.sub(r'\W', ' ', str(X[sen]))
		document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
		document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)
		document = re.sub(r'\s+', ' ', document, flags=re.I)
		document = re.sub(r'^b\s+', '', document)
		document = document.lower()
		document = document.split()
		document = [stemmer.lemmatize(word) for word in document]
		document = ' '.join(document)
		documents.append(document)


def get_features(documents):
	vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
	X = vectorizer.fit_transform(documents).toarray()
	return tfidfconverter.fit_transform(X).toarray()
	# returns 'X' in terms of training X, and test y data.



"""
may be able to directly convert text to TFIDF features without first needing to convert text to numbers \
with the bag to words features. using the following:

tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X = tfidfconverter.fit_transform(documents).toarray()
"""

