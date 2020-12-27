import logging
from src.setup import settings
from src.tweet_streamer import TweetStreamer

# Get logger instance
__logger__ = logging.getLogger()

def main() :

	print('Tweet Tracker')

	# Ask for filling settings
	settings.fill()

	# Tweepy stream object
	tweet_streamer = TweetStreamer()

	__logger__.info(f'Traking {settings.threshold} tweets in {settings.languages} containing {settings.keywords}')

	# Start stream
	tweet_streamer.start()


if __name__ == '__main__':
	main()