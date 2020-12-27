import json
import tweepy
import logging
from src.setup import settings
from src.twitter_api import twitter_api
from src.tweet_listener import TweetListener

# Logger

# Get Logger instance
__logger__ = logging.getLogger()


class TweetStreamer() :

	""" This class implaments a Tweet Stream by Tweepy Listener """

	def __init__(self) :

		api = twitter_api()
		
		self.listener = TweetListener(api)

		self.stream = tweepy.Stream(api.auth, self.listener)


	def start(self) :

		""" Recursive function that resarts stream if a exception is raised """

		__logger__.info('Now streaming...')

		try :

			self.stream.filter(track = settings.keywords, languages = settings.languages)

		except KeyboardInterrupt :

			self.listener.persist()

		except :

			self.stream.disconnect()

			__logger__.info('Stream disconnected. Resuming...')

			self.start()
