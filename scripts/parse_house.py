import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from urllib import request, parse
from bs4 import BeautifulSoup
import pandas as pd
import wikipedia
import os
import re

zipcodes = pd.read_csv('../data/us-zipcode.csv', low_memory=False)
states = zipcodes.State.unique()

# with open('../data/{}/candidates.txt'.format('house'), 'w') as save_file:
#     for state in states:
#         try:
#             with open('../data/{}/{}_{}.txt'.format('house', 'House', state), 'r') as load_file:
#                 word_list = word_tokenize(load_file.read())
#                 for i in range(len(word_list)):
#                     word = word_list[i]
#                     if word == '(':
#                         save_file.write('_'.join(word_list[i-2:i]) + ',{},'.format(state))
#                     elif word == ')':
#                         save_file.write(str(word_list[i+1]) + '\n')
#
#         except Exception as e:
#             print(str(e))

with open('../data/{}/candidates.txt'.format('house'), 'r') as load_file:
    lines = set()
    with open('../data/{}/ucandidates.txt'.format('house'), 'w') as save_file:
        for line in load_file:
            print(line)
            if line[0].isupper() and line not in lines:
                save_file.write(line + '\n')
                lines.add(line)



