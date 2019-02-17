import pandas as pd
import numpy as np
from sklearn import feature_selection as fs
from sklearn import preprocessing
import multiprocessing
from multiprocessing import Process, Pool
import sys
import logging
import random
import math

import sentiment_module as s_mod
import pandas as pd
import numpy as np


elections = ['presidential', 'house', 'senate', 'gov']
coefficient = {'pos': 1, 'neg': -1}

"""
This is called whenever foo_pool(i) returns a result.
to_be_dropped is modified only by the main process, not the pool workers.
"""


def log_result(result):
    election, df = result
    # print(df.head())

    df.to_csv('../data/{}_labeled.csv'.format(election), index=False)
    df.to_json('../data/{}_labeled.json'.format(election), orient='records')


def analyze_sentiment(election):
    df = pd.read_csv('../data/{}.csv'.format(election))
    positions = []

    for comment in df.comment:
        # print(comment)
        pos, conf = s_mod.sentiment(comment)
        # print(pos, conf)
        positions += [coefficient[pos] * conf]

    df['position'] = pd.Series(positions)

    return election, df


def main():

    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    pool = Pool(processes=50)

    for election in elections:
        pool.apply_async(func=analyze_sentiment,
                         args=(election, ), callback=log_result)

    pool.close()
    pool.join()

    print('main process exiting...')


if __name__ == '__main__':
    main()







