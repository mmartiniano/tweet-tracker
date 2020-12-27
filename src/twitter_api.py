import os
import logging
import tweepy
from src.setup import settings

# Logger

# Get Logger instance
__logger__ = logging.getLogger()

def twitter_api() :

	""" This function returns a tweepy.API object by Twitter credentials authentication  """

	# Twitter authentication

	auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
	auth.set_access_token(settings.access_token, settings.access_token_secret)

	# Create tweepy.API object and notify when rate limit is exceeded.

	api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

	# Validate credentials

	try:

		api.verify_credentials()

	except tweepy.error.TweepError :

		# Authentication fail error

		__logger__.error('Twitter authentication failed. Make sure that credentials are correct and valid.')
		exit()

	__logger__.info('Successfully authenticated at Twitter.')

	return api