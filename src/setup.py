import logging
from sys import stdout, argv
from datetime import datetime
from os import mkdir, path

# Current date and time
__running_at__ =  str(datetime.now()).replace(' ', 'T')

# Create required folders
if not path.exists('data') or not path.exists('log') :
	try :

		mkdir('data')
		mkdir('log')

	except OSError :
		pass

# Logger

# Logger file handler
file_logger = logging.FileHandler(filename = f'log/{__running_at__}.log')

# Logger stdout handler
stdout_logger = logging.StreamHandler(stdout)

# Create a Logger instance to report logs at file an stdout
logging.basicConfig(handlers = [file_logger, stdout_logger], level = logging.INFO)

# Get logger instance
__logger__ = logging.getLogger()


def ask(question) :
	""" Ask user to input requested data """

	answer = input(question)

    if len(answer.strip()) > 0 : 
		return answer
    else :
		return ask(question)

class Settings() :

    def __init__(self,
                running_at = __running_at__,
                keywords = [],
                languages = [],
                threshold = 0,
                consumer_key = '',
                consumer_secret = '',
                access_token = '',
                acces_token_secret = '') :
        
        self.running_at = running_at
        self.keywords = keywords
        self.langauges = languages
        self.threshold = threshold
        self.consumer_key = consumer_key 
		self.consumer_secret = consumer_secret
		self.access_token = access_token
		self.access_token_secret = access_token_secret

    def ask(self) :
        """ Ask for all required settings """

    try :
		self.keywords = ask('Words: ').split(' ')
		self.languages = ask('Languages: ').split(' ')
		self.threshold = int(ask('Threshold: '))

        print('Set Twitter credentials')

		self.consumer_key = ask('Consumer key: ')
		self.consumer_secret = ask('Consumer secret: ')
		self.access_token = ask('Access token: ')
		self.access_token_secret = ask('Access token secret: ')

	except ValueError, TypeError, KeyboardInterrupt :
		__logger__.error('Settings error. Aborted.')