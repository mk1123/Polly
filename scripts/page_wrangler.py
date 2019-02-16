import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import os

lines_seen = set()  # holds lines already seen
outfile = open('../data/ucandidates.txt', "w")

for line in open('../data/candidates.txt', "r"):
    if line not in lines_seen:  # not a duplicate
        outfile.write(line)
        lines_seen.add(line)

outfile.close()

url = open('../data/url_candidates.txt', "w")
for line in open('../data/ucandidates.txt', "r"):
    # print('_'.join(word_tokenize(line)[-2:]))
    url.write('_'.join(word_tokenize(line)[-2:]) + '\n')

