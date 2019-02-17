import codecs
import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from nltk.tokenize import word_tokenize
from statistics import mode


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for clf in self._classifiers:
            vote = clf.classify(features)
            votes.append(vote)

        return mode(votes)

    def confidence(self, features):
        votes = []
        for clf in self._classifiers:
            vote = clf.classify(features)
            votes.append(vote)

        majority = votes.count(mode(votes))
        conf = majority / len(votes)

        return conf


dir = '../pickled_algorithms/'

pos_df = codecs.open('../data/sentiment/positive.txt', 'r', encoding='latin2', errors='ignore').read()
neg_df = codecs.open('../data/sentiment/negative.txt', 'r', encoding='latin2', errors='ignore').read()

documents = []

for l in pos_df.split('\n'):
    documents.append((l, 'pos'))

for l in neg_df.split('\n'):
    documents.append((l, 'neg'))

save_document = open('../data/sentiment/documents.pickle', 'wb')
pickle.dump(documents, save_document)
save_document.close()

all_words = []

pos_words = word_tokenize(pos_df)
neg_words = word_tokenize(neg_df)

for w in (pos_words + neg_words):
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)
# print(all_words.keys())

# print(all_words.most_common(30))
# print(all_words['ridiculous'])1

# Check against the top 5000 words of the document
word_features = list(all_words.keys())[:5000]
save_word_features = open('../data/sentiment/word_features.pickle', 'wb')
pickle.dump(word_features, save_word_features)
save_word_features.close()


# print('Word Features: {}'.format(word_features))


# convert [([w1, w2,..., wn], 'neg'), ([w3, w4,..., wn], 'pos'),...]
# -> {w1 : True, w2 : False, ...}
def find_features(document):
    words = word_tokenize(document)
    # words = set(document)

    features = {}

    for _ in word_features:
        features[_] = (_ in words)

    return features


feature_sets = [(find_features(rev), category) for (rev, category) in documents]
save_feature_sets = open('../data/sentiment/feature_sets.pickle', 'wb')
pickle.dump(feature_sets, save_feature_sets)
save_feature_sets.close()

random.shuffle(feature_sets)

# Positive data example:
train_set = feature_sets[:10000]
test_set = feature_sets[10000:]

# Negative data example:
train_set = feature_sets[600:]
test_set = feature_sets[:600]

'''
Naive Bayes classifier
posterior = prior occurrences * likelihood / evidence
'''
classifier = nltk.NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.accuracy(classifier, test_set)

# Decent range: 65% - 85%
print('Original Naive Bayes Algorithm accuracy percentage: {}%'.format(accuracy * 100))
classifier.show_most_informative_features(15)

save_classifier = open(dir + 'naivebayes_sentence.pickle', 'wb')
pickle.dump(classifier, save_classifier)
save_classifier.close()

# SklearnClassifier(x) is a nltk wrapper for SK-learn x
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(train_set)
print('MNB_classifier accuracy percent: {}%'.format(nltk.classify.accuracy(MNB_classifier, test_set) * 100))

save_classifier = open(dir + 'MNB_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifier)
save_classifier.close()

# GaussianNB_classifier = SklearnClassifier(GaussianNB())
# GaussianNB_classifier.train(train_set)
# print(
#     'GaussianNB_classifier accuracy percent: {}%'.format(nltk.classify.accuracy(GaussianNB_classifier, test_set) * 100))


BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(train_set)
print('BernoulliNB_classifier accuracy percent: {}%'.format(
    nltk.classify.accuracy(BernoulliNB_classifier, test_set) * 100))

save_classifier = open(dir + 'BernoulliNB_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifier)
save_classifier.close()


LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(train_set)
print('LogisticRegression_classifier accuracy percent: {}%'.format(nltk.classify.accuracy(LogisticRegression_classifier,
                                                                                          test_set) * 100))
save_classifier = open(dir + 'LogisticRegression_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifier)
save_classifier.close()


SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(train_set)
print('SGDClassifier_classifier accuracy percent: {}%'.format(nltk.classify.accuracy(SGDClassifier_classifier,
                                                                                     test_set) * 100))
save_classifier = open(dir + 'SGDC_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifier)
save_classifier.close()


SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(train_set)
print('SVC_classifier accuracy percent: {}%'.format(nltk.classify.accuracy(SVC_classifier,
                                                                           test_set) * 100))
save_classifier = open(dir + 'SVC_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifier)
save_classifier.close()


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(train_set)
print('LinearSVC_classifier accuracy percent: {}%'.format(nltk.classify.accuracy(LinearSVC_classifier,
                                                                                 test_set) * 100))
save_classifier = open(dir + 'LinearSVC_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifier)
save_classifier.close()


NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(train_set)
print('NuSVC_classifier accuracy percent: {}'.format(nltk.classify.accuracy(NuSVC_classifier,
                                                                            test_set) * 100))
save_classifier = open(dir + 'NuSVC_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifier)
save_classifier.close()


combined_classifier = VoteClassifier(classifier, MNB_classifier, BernoulliNB_classifier,
                                     LogisticRegression_classifier, SGDClassifier_classifier, LinearSVC_classifier,
                                     NuSVC_classifier)

print('combined_classifier accuracy percent: {}'.format(nltk.classify.accuracy(combined_classifier, test_set) * 100))

i, j = 0, 0
print(test_set[0][0])

while i <= 5:
    print('Classification [{}][{}]: {}'.format(i, j, combined_classifier.classify(test_set[i][j])))
    print('Confidence [{}][{}]: {}'.format(i, j, combined_classifier.confidence(test_set[i][j])))

    i += 1





