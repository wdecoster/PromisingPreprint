# PromisingPreprint
A python twitter bot tweeting about bioRxiv preprints reaching an interesting altmetric score.

## Introduction
The script is designed to run as a cron job:
- getPreprintsAndSave.py hourly
- checkScoreAndTweet.py once daily
In my case I use a raspberry pi for this.

In case you want to use this code for a similar project it is highly encouraged to reach out to [Altmetric](https://api.altmetric.com/) to get an API key. For enabling the tweeting you need to setup a Twitter application on an existing account, see for [example this blog post](https://www.digitalocean.com/community/tutorials/how-to-create-a-twitterbot-with-python-3-and-the-tweepy-library).

## Scripts and modules
### preprint.py
This module contains the Preprint Class, of which instances are defined based on a digital object identifier (doi), url, title, date and status. The status attribute contains information if this article has been tweeted by the bot or not (yet). The class has three methods: querying the altmetric score of an article, tweeting it, or just printing to the terminal in a "dry" run without tweeting. Furthermore, functions to load and save the preprint database in Pickle format are included in this module file.

### getPreprintsAndSave.py
This script will check for new entries in an RSS feed specified by an URL in check_RSS(). This URL can freely be adapted to follow other RSS feeds. Found entries are saved to the preprint database as Preprint class instances, unless those were already found earlier.

### checkScoreAndTweet.py
This script will query the altmetric data for all saved articles in the preprint database. In the current implementation the altmetric score percentage for this journal gets queried, essentially, the attention this particular publication received compared to all other from the same source. If the score is above a certain cutoff, by default 90%, the article will get tweeted once. Note that it is also possible to change the Altmetric feature to filter on, or the required cutoff before tweeting. Finally, the database is cleared by removing all preprints which are older than a user-specified number of days, by default 31 days.

### utils.py
A function for setting up the rotating logs is included in this module, which would be the most logical place to place further util functions.

### Not included: secrets.py
Not included in this repo is the secrets.py file, in which all passwords and credentials are stored, using the following structure (order not important):
```python
consumer_key = ''  # twitter app credentials
consumer_secret = ''  # twitter app credentials
access_token = ''  # twitter app credentials
access_secret = ''  # twitter app credentials
altmetric_key = ''  # altmetric API key
```
