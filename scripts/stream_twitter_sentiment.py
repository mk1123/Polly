import sys
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
# from twitter_api import *
import sentiment_module as s_mod
import pickle

# consumer key, consumer secret, access token, access secret.
# ckey = ""
# csecret = ""
# atoken = ""
# asecret = ""

sys.path.append('/Users/jasonchang/Desktop/PrivateRepo')
dir = '/Users/jasonchang/Desktop/PycharmProjects/natural-language-processing/'


def load_keys():
    global ckey, csecret, atoken, asecret
    load_file = open('../keys/ckey.pickle', 'rb')
    ckey = pickle.load(load_file)
    load_file.close()

    load_file = open('../keys/csecret.pickle', 'rb')
    csecret = pickle.load(load_file)
    load_file.close()

    load_file = open('../keys/atoken.pickle', 'rb')
    atoken = pickle.load(load_file)
    load_file.close()

    load_file = open('../keys/asecret.pickle', 'rb')
    asecret = pickle.load(load_file)
    load_file.close()


class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"]
        sentiment_val, confidence = s_mod.sentiment(tweet)

        print('Tweet: {} \n Sentiment: {} \n Confidence: {}'.format(tweet, sentiment_val, confidence))

        if confidence*100 >= 80:
            out = open(dir + 'twitter_output.txt', 'a')
            out.write(sentiment_val)
            out.write('\n')
            out.close()

        return True

    def on_error(self, status):
        print(status)


load_keys()
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["politics"])



