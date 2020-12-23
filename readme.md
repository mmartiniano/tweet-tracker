# COVID-19 Tweets Tracker

Track real-time tweets in english about COVID-19.

## Requirements

This is a **Python 3** project that requires **pip** or whatever python package manager you like.

In order to install all **Python** modules and dependencies, run:

`pip install -r requirements.txt`

Since the software consumes Twitter official API to track tweets, you have to register for [Twitter Developer](https://developer.twitter.com/en/apply-for-access) to get your own CONSUMER KEY, CONSUMER SECRET, ACCESS KEY and ACCESS TOKEN SECRET.

## Run

You can run this project by command line setting a optional value for the tweet tracking threshold:

`python app.py [threshold]`

If you do not specify a threshold, the tracking process you continue until 2000 tweets be tracked or after manually canceling by pressing `ctrl + C`.

Then, you have to set values for CONSUMER KEY, CONSUMER SECRET, ACCESS KEY and ACCESS TOKEN SECRET. If Twitter authentication is successfully done, the program will start to track all tweets in english containing the words: "coronavirus", "covid-19". The process splits tweet info into 4 fields: id, datetime, location and text. Id refers to Twitter tweet original id. Datetime stores whenever the tweet was published. Location is set based on tweet's owner location. Text stores the tweet content text. The process ignores retweets and text case.

A log file into *log* folder will be automatically created for each execution.

## Result

All tracked tweets are stored in a CSV file named as **tweets_{date}T{time}.csv** inside *data* folder.
