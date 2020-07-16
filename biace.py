import os
import tweepy
import time
import datetime
from os import environ

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
foi = False

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global foi
        if status.user.screen_name == "BiaceLucas" and not "RT" in status.text:
            try:
                if not foi:
                    api.update_status("Concordo @BiaceLucas", in_reply_to_status=status.id, auto_populate_metadata=True)                
                else:
                    api.update_status("Sempre cirúrgico @BiaceLucas", in_reply_to_status=status.id)
                foi = not foi    
                api.create_favorite(status.id)
                api.retweet(status.id)
            except tweepy.TweepError as e:
                print(e.reason)    

                                                 
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(follow=["1252818979992727552"])
