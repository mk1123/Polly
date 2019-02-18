import sentiment_module as s_mod
import pandas as pd
import numpy as np

'''
pos_ex = 'The movie was good. ' \
         'The movie had a happy ending.' \
         'Sound of the movie was perfect.' \
         'Lovely movie, every should go watch it once.' \
         'The acting was great, plot was wonderful, and the casting was splendid.'

neg_ex = 'The movie was horrible. ' \
         'Nothing is good about the moive. ' \
         'This movie is not worth the time to watch. ' \
         'The movie is a waste of time.'

print(s_mod.sentiment(pos_ex))
print(s_mod.sentiment(neg_ex))
'''

elections = ['presidential', 'house', 'senate', 'gov']
coefficient = {'pos': 1, 'neg': -1}


df = pd.read_csv('../data/{}.csv'.format(elections[2]))

positions = []
for comment in df.comment:
    # print(comment)

    pos, conf = s_mod.sentiment(comment)
    # print(pos, conf)

    positions += [coefficient[pos] * conf]

df['position'] = pd.Series(positions)

print(df.head())
df.to_csv('../data/{}_labeled.csv'.format(election), index=False)
df.to_json('../data/{}_labeled.json'.format(election), orient='records')




