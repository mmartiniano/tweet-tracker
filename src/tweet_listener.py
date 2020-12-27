import logging
import pandas as pd
from queue import Queue
from threading import Thread
from tweepy import StreamListener
from src.setup import settings

# Logger

# Get Logger instance
__logger__ = logging.getLogger()

class TweetListener(StreamListener) :

	""" This class retrieves tweeets that match certain criteria  """

	def __init__(self, api):
		self.api = api
		self.me = api.me()
		self.tweet_queue = Queue() # Store tweets from tweepy stream
		self.tweet_list = [] # Store processed tweets

		# Create 5 threads to filter tweets
		for i in range(5) :

			filter_tweet_thread = Thread(target = self.filter)
			filter_tweet_thread.daemon = True
			filter_tweet_thread.start()


	def on_status(self, tweet):

		""" Tweepy.StreamListener.on_status override """

		if len(self.tweet_list) < settings.threshold : # Stream threshold

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

				if any(keyword in text.lower() for keyword in settings.keywords) : # Check if Tweet text contains any keyword

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

		storage = f'data/tweets_{settings.running_at}.csv'

		tweets_df.to_csv(storage, index = False)

		__logger__.info(f'Tweets saved at {storage}')


	def on_exception(self, exception) :

		""" Exception handling """

		__logger__.exception(exception)

		self.persist()

		raise exception
