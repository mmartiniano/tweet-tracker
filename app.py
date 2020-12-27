from src.setup import Settings
from src.tweet_streamer import TweetStreamer

# Get logger instance
__logger__ = logging.getLogger()

def main() :

	__logger__.info('Starting...')

	print('Tweet Tracker')

	# Ask for settings

	settings = Settings()
	settings.ask()

	# Tweepy stream object
	tweet_streamer = TweetStreamer()

	# Set tracking config

	tweet_streamer.listener.keywords = settings.keywords
	tweet_streamer.listener.languages = settings.languages
	tweet_streamer.listener.threshold = settings.threshold

	# Output file
	tweet_streamer.listener.storage = f'data/tweets_{settings.running_at}.csv'

	__logger__.info(f'Traking {settings.threshold} tweets in {settings.languages} containing {settings.keywords}')

	# Start stream
	tweet_streamer.start()


if __name__ == '__main__':
	main()