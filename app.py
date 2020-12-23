import logging
from sys import stdout, argv
from datetime import datetime
from os import mkdir, path
from src.tweet_streamer import TweetStreamer

# Current date and time
__running_at__ =  str(datetime.now()).replace(' ', 'T')

# Create required folders
if not path.exists('data') or not path.exists('log') :
	try :

		mkdir('data')
		mkdir('log')

	except OSError :
		pass

######################
# Logger
######################

# Logger file handler
file_logger = logging.FileHandler(filename = f'log/{__running_at__}.log')

# Logger stdout handler
stdout_logger = logging.StreamHandler(stdout)

# Create a Logger instance to report logs at file an stdout
logging.basicConfig(handlers = [file_logger, stdout_logger], level = logging.INFO)

# Get logger instance
__logger__ = logging.getLogger()

######################

def main() :

	__logger__.info('Starting...')

	# Tweepy stream object
	tweet_streamer = TweetStreamer()

	# Set default tweet listener threshold
	stream_threshold = 2500

	# Check if stream threshold was setted by command line
	if len(argv) == 2 :

		# Threshold non-integer error handling
		try :

			stream_threshold = int(argv[1])

		except :

			__logger__.error('Stream threshold must be integer. Default threshold selected.')

	# Set stream threshold
	tweet_streamer.listener.threshold = stream_threshold

	# Output file
	tweet_streamer.listener.storage = f'data/tweets_{__running_at__ }.csv'

	__logger__.info(f'Traking tweets in {tweet_streamer.languages} containing {tweet_streamer.keywords}')

	# Start stream
	tweet_streamer.start()


if __name__ == '__main__':
	main()