# Tweet Tracker

Track and store realtime tweets.

## Requirements

This is a **Python 3** project that requires **pip** or whatever python package manager you like. To install all modules and dependencies, enter your python virtual environment and run:

`pip install -r requirements.txt`

Since the software consumes Twitter official API to track tweets, you have to register for [Twitter Developer](https://developer.twitter.com/en/apply-for-access) to get your own API keys.

## Settings

Some tracking settings are required to start:

* Words to track in tweets text: words list separated by white spaces
* Tweets languages to filter: language shorthands (en, pt, fr...) list separated by white spaces
* Threshold: number of tweets to track

And Twitter API keys:

* CONSUMER KEY
* CONSUMER SECRET
* ACCESS KEY
* ACCESS TOKEN SECRET

If you intend to run this program multiple times using the same settings, consider creating a file containing settings values, each per line. Below is an example of settings file to track 10000 tweets in english containing words that refer to the COVID-19 pandemic:

```
covid-19 covid covid19 coronavirus pandemic
en
10000
CONSUMER_KEY
CONSUMER_SECRET
ACCESS_KEY
ACCESS_TOKEN_SECRET
```

## Running

This is a CLI Python software, so the command below starts the program. You can pass a optional argument for the settings file or set its values at runtime in default input.

`python app.py [settings_file]`

All set, the program will first try to authenticate your Twitter credentials and it must accomplish this successfully to proceed. Then, the tracking process starts printing each tweet found until reach the threshold or after you manually canceling by pressing `CTRL + C`.

The process splits tweet info into 6 fields: 

* id: tweet original Twitter id
* datetime: whenever the tweet was published
* location: tweet's owner location
* text: tweet content text
* hashtags: hashtags into tweet
* mentions: mentions into tweet

Retweets and text case differences are intentionally ignored.

A log file into *log* folder will be automatically created for each execution.

## Result

All tracked tweets are stored in a CSV file named as **tweets_{date}T{time}.csv** inside *data* folder.
