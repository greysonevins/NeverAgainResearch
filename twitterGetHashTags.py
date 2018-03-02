import os
import tweepy
import threading
import json

consumer_key = os.environ["NA_CONSUMER_KEY"]
consumer_secret = os.environ["NA_CONSUMER_SECRET"]
access_token = os.environ["NA_ACCESS_TOKEN"]
access_token_secret = os.environ["NA_ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


t = None


def cleanData(data):
    if (not data.retweeted and data.user.location):
        twitterDict = {
            "created_at"    : data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "text"          : data.text,
            "id"            : data.id,
            "location"      : data.user.location,
            "coordinates"   : data.coordinates,
            "retweet_count" : data.retweet_count,
            "favorite_count": data.favorite_count
        }
        return twitterDict
    else:
        return

def getTwitterData():
    global t
    last_used_file = open("lastused.txt", "r")
    discoveredTweets = []
    with open('tweetsNAHash.json', 'r') as tweet_json:
        discoveredTweets = json.load(tweet_json)


    lastused = last_used_file.read()
    last_used_file.close()
    params = {"q": "#neveragain since:2018-02-18", "result_type": "recent", "max_id": lastused, "count": "100"}
    tweets = api.search(**params)
    newData = list(map(lambda t: cleanData(t), tweets))
    finalData = [t for t in newData if t is not None]
    list(map(lambda t: discoveredTweets.append(t), finalData))
    with open('tweetsNAHash.json', 'w') as outfile:
        json.dump(discoveredTweets, outfile)

    newLast = tweets[-1].id - 1
    last_used_file = open("lastused.txt", "w")
    last_used_file.write(str(newLast))
    last_used_file.close()
    print(tweets[-1].created_at)
    t = threading.Timer(5, getTwitterData)
    print("starting next")
    t.start()

getTwitterData()
