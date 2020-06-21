import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import tokenize
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from lexical_diversity import lex_div as ld
from nltk.util import ngrams
import gensim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import os
import codecs
import re
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter
from collections import OrderedDict
# import nlp
import spacy
from textstat.textstat import textstatistics, legacy_round
from sklearn.preprocessing import StandardScaler
#Using Min Max scaler for NAive bayes so as to bound the values between 0 and 1
#Negative values won't work for probability computations
from sklearn.preprocessing import MinMaxScaler
#GridSearch for hyperparams tuning and classification_report for generating report after param tuning
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

import en_core_web_sm
from sklearn import svm
#Naive Bayes from SKLearn
from sklearn.naive_bayes import MultinomialNB
nlp = en_core_web_sm.load()

#Supress warning in console
import warnings
warnings.filterwarnings("ignore")

#For giving relative path
from pathlib import Path
base_path = Path(__file__).parent
file_path = (base_path / "../final_features_without_null_values.csv").resolve()

data = pd.read_csv(file_path,encoding="ISO-8859-1")

#data = pd.read_csv("final_features_without_null_values.csv",encoding="ISO-8859-1")

# Split Train and Test Data
y_true = data['class'].values
x_train, test_df, y_train, y_test = train_test_split(data, y_true, stratify = y_true, test_size = 0.2)
# train_df, cv_df, y_train, y_cv = train_test_split(x_train, y_train, stratify = y_train, test_size = 0.2)

print("Number of samples in training data :", x_train.shape[0])
# print("Number of samples in validation data :", cv_df.shape[0])
print("Number of samples in test data :", test_df.shape[0])

train_class_distribution = x_train['class'].value_counts().sort_index()
# cv_class_distribution = cv_df['class'].value_counts().sort_index()
test_class_distribution = test_df['class'].value_counts().sort_index()

print("\ntraining distribution:\n\n", train_class_distribution)
# print("\ncv distribution: \n\n", cv_class_distribution)
print("\ntest distribution: \n\n", test_class_distribution)

scaler = MinMaxScaler()
train_df = scaler.fit_transform(x_train)
test_df = scaler.fit_transform(test_df)

#Tune Hyperparams
# Set the parameters by cross-validation
tuned_parameters = [{'alpha': [0.40,0.25,0.45,0.55]}]
scores = ['precision', 'recall','f1']

for score in scores:
	print("# Tuning hyper-parameters for %s" % score)
	clf = GridSearchCV(MultinomialNB(), tuned_parameters, scoring='%s_macro' % score)
	clf.fit(train_df, y_train)

	print("Best parameters set found on development set:")
	print(clf.best_params_)
	print("Grid scores on development set:")
	means = clf.cv_results_['mean_test_score']
	stds = clf.cv_results_['std_test_score']
	for mean, std, params in zip(means, stds, clf.cv_results_['params']):
		print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
	print("Detailed classification report:")
	print("The model is trained on the full development set.")
	print("The scores are computed on the full evaluation set.")
	y_true, y_pred = y_test, clf.predict(test_df)

print(classification_report(y_true, y_pred))

# Alpha=Smoothening parameter(0 for no smoothening)
# Other hyperparams for naive bayes fit_prior & class prior
# If we know class prior set fit prior to yes and define class prior, Now since we don't know we are going with uniform prior for classes
# clf = MultinomialNB(alpha=.45)
# clf.fit(train_df, y_train)
# pred = clf.predict(test_df)

# print('*******************F1 Score and Accuracy*****************************')
# print('F1 Score: ', metrics.f1_score(y_test, pred, average='macro'))
# print('Accuracy: ', metrics.accuracy_score(y_test, pred))