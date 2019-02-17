import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        mode_votes = mode(votes)
        # print('{}: {}'.format(mode_votes, features))
        return mode_votes

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            # print(v, features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


dir = '../pickled_algorithms/'

word_features_file = open('../data/sentiment/word_features.pickle', 'rb')
word_features = pickle.load(word_features_file)
word_features_file.close()


# convert [([w1, w2,..., wn], 'neg'), ([w3, w4,..., wn], 'pos'),...]
# -> {w1 : True, w2 : False, ...}
def find_features(document):
    words = word_tokenize(document)
    features = {}

    for _ in word_features:
        features[_] = (_ in words)

    return features


open_file = open(dir + 'naivebayes_sentence.pickle', 'rb')
classifier = pickle.load(open_file)
open_file.close()

open_file = open(dir + 'MNB_classifier.pickle', 'rb')
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open(dir + 'BernoulliNB_classifier.pickle', 'rb')
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open(dir + 'LogisticRegression_classifier.pickle', 'rb')
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open(dir + 'SGDC_classifier.pickle', 'rb')
SGDC_classifier = pickle.load(open_file)
open_file.close()

open_file = open(dir + 'LinearSVC_classifier.pickle', 'rb')
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open(dir + 'NuSVC_classifier.pickle', 'rb')
NuSVC_classifier = pickle.load(open_file)
open_file.close()

voted_classifier = VoteClassifier(
    classifier,
    MNB_classifier,
    BernoulliNB_classifier,
    LogisticRegression_classifier,
    SGDC_classifier,
    LinearSVC_classifier,
    NuSVC_classifier)


def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)




