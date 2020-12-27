import os
import logging
import tweepy

# Logger

# Get Logger instance
__logger__ = logging.getLogger()

# Twitter credentials are required to run this project.
# They should be set at runtime.
def twitter_api() :

	""" This function returns a tweepy.API object by Twitter credentials authentication  """

	print('Set Twitter credentials')

	try :

		# Credentials passed at runtime
		CONSUMER_KEY = input('Consumer key: ')
		CONSUMER_SECRET = input('Consumer secret: ')
		ACCESS_TOKEN = input('Access token: ')
		ACCESS_TOKEN_SECRET = input('Access token secret: ')

	except (ValueError, KeyboardInterrupt) :
		
		# Failed to set credentials

		__logger__.error('Error setting Twitter credentials.')
		exit()


	# Twitter authentication

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	# Create tweepy.API object and notify when rate limit is exceeded.

	api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

	# Validate credentials

	try:

		api.verify_credentials()


	except Exception as e :

		# Authentication fail error

		__logger__.error('Twitter authentication failed. Make sure that credentials are correct and valid.', exc_info = True)
		raise e

	__logger__.info('Successfully authenticated at Twitter.')

	return api