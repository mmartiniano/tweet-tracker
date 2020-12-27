import json
import tweepy
import logging
import pandas as pd
from queue import Queue
from threading import Thread
from src.twitter_api import twitter_api

# Default global variables

# Set default keywords to track over tweets
__keywords__ = ['coronavirus', 'covid-19']

# Set default tweet languages stream
__language__ = ['en']

# Set default stream tracking threshold
__threshold__ = 2000

# Logger

# Get Logger instance
__logger__ = logging.getLogger()


class TweetStreamer() :

	""" This class implaments a Tweet Stream by Tweepy Listener """

	def __init__(self, keywords = __keywords__, languages = __language__) :
		self.keywords = keywords
		self.languages = languages

		api = twitter_api()
		
		self.listener = TweetListener(api, self.keywords)

		self.stream = tweepy.Stream(api.auth, self.listener)


	def start(self) :

		""" Recursive function that resarts stream if a exception is raised """

		__logger__.info('Now streaming...')

		try :

			self.stream.filter(track = self.keywords, languages = self.languages)

		except KeyboardInterrupt :

			self.listener.persist()

		except :

			self.stream.disconnect()

			__logger__.info('Stream disconnected. Resuming...')

			self.start()



class TweetListener(tweepy.StreamListener) :

	""" This class retrieves tweeets that match certain criteria  """

	def __init__(self, api, keywords = __keywords__, threshold = __threshold__):
		self.api = api
		self.me = api.me()
		self.keywords = keywords
		self.threshold = threshold
		self.tweet_queue = Queue() # Store tweets from tweepy stream
		self.tweet_list = [] # Store processed tweets
		self.storage = 'output.csv' # Default storage path

		# Create 5 threads to filter tweets
		for i in range(5) :

			filter_tweet_thread = Thread(target = self.filter)
			filter_tweet_thread.daemon = True
			filter_tweet_thread.start()


	def on_status(self, tweet):

		""" Tweepy.StreamListener.on_status override """

		if len(self.tweet_list) < self.threshold : # Stream threshold

			# Add tweet to the queue
			self.tweet_queue.put(tweet)

		else :

			__logger__.info('Stream threshold reached.')

			self.persist()

			return False
		

	def filter(self) :

		""" Filter tweets from Tweepy stream """

		while True :

			# Get a tweet from streaming queue
			tweet = self.tweet_queue.get()

			if not hasattr(tweet, 'retweeted_status') : # Skip RTs

				# Tweets text can be truncated. The full text is required anyway
				text = tweet.extended_tweet['full_text'] if hasattr(tweet, 'extended_tweet') else tweet.text

				# Tweet stream tracks keywords in attributes beyond text.

				if any(keyword in text.lower() for keyword in self.keywords) : # Check if Tweet text contains any keyword

					# Auxiliar variable to select tweet info
					t = [tweet.id, tweet.created_at, tweet.user.location, text]

					# Show tweet info
					print(len(self.tweet_list), t)

					# Store processed tweet
					self.tweet_list.append(t)


			self.tweet_queue.task_done()


	def persist(self) :

		""" Persist tweets data """		

		__logger__.info('Persisting Twitter data...')

		tweets_df = pd.DataFrame(self.tweet_list, columns = ['id', 'datetime', 'location', 'text'])
		tweets_df.to_csv(self.storage, index = False)

		__logger__.info(f'Tweets saved at {self.storage}')


	def on_exception(self, exception) :

		""" Exception handling """

		__logger__.exception(exception)

		self.persist()

		raise exception
