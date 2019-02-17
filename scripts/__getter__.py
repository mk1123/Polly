import nltk.data
import os


if __name__ == '__main__':
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    fp = open("../data/Marco_Rubio.txt")
    data = fp.read()
    print('\n-----\n'.join(tokenizer.tokenize(data)))





