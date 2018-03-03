import json
from datetime import datetime
from dateutil import tz

# from https://python-forum.io/Thread-list-of-US-states
STATES = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

# edited from because it included DC from https://gist.github.com/JeffPaine/3083347
STATES_CODES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def cleanTweets():
    tweets = []

    with open("cleanTweets.json", "r") as data:
        tweets = json.load(data)

    usefulTweets = []

    for tweet in tweets:
        locationValue = tweet["location"]
        locationSplit = locationValue.split(",")
        possibleLocal = []
        for local in locationSplit:
            if not local:
                continue
            elif local[0] == " ":
                local = local[1:]
            possibleLocal.append(local)
        locationRelevant = ""
        for localTest in possibleLocal:
            if localTest in STATES:
                locationRelevant = localTest
                break
            elif localTest in STATES_CODES:
                stateIndex = STATES_CODES.index(localTest)
                localTest = STATES[stateIndex]
                locationRelevant = localTest
                break
            else:
                continue
        if locationRelevant:
            tweet["location"] = locationRelevant
            time = tweet["created_at"]
            tweet["created_at"] = UTCFixTime(time)
            usefulTweets.append(tweet)

    with open("usefulTweets.json", "w") as tw:
        json.dump(usefulTweets, tw)


def UTCFixTime(time):
    #from help https://stackoverflow.com/questions/4770297/python-convert-utc-datetime-string-to-local-datetime
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    easternTime = utc.astimezone(to_zone)
    return easternTime.strftime("%Y-%m-%d %H:%M:%S")




def statesAmounts():

    tweetsUsed = []

    with open("usefulTweets.json", "r") as tw:
        tweetsUsed = json.load(tw)

    State_Tweets_day1 = {"Alabama": 0,"Alaska": 0,"Arizona": 0,"Arkansas": 0,"California": 0,"Colorado": 0,
      "Connecticut": 0,"Delaware": 0,"Florida": 0,"Georgia": 0,"Hawaii": 0,"Idaho": 0,"Illinois": 0,
      "Indiana": 0,"Iowa": 0,"Kansas": 0,"Kentucky": 0,"Louisiana": 0,"Maine": 0,"Maryland": 0,
      "Massachusetts": 0,"Michigan": 0,"Minnesota": 0,"Mississippi": 0,"Missouri": 0,"Montana": 0,
      "Nebraska": 0,"Nevada": 0,"New Hampshire": 0,"New Jersey": 0,"New Mexico": 0,"New York": 0,
      "North Carolina": 0,"North Dakota": 0,"Ohio": 0,"Oklahoma": 0,"Oregon": 0,"Pennsylvania": 0,
      "Rhode Island": 0,"South Carolina": 0,"South Dakota": 0,"Tennessee": 0,"Texas": 0,"Utah": 0,
      "Vermont": 0,"Virginia": 0,"Washington": 0,"West Virginia": 0,"Wisconsin": 0,"Wyoming":0}

    State_Tweets_day2 = {"Alabama": 0,"Alaska": 0,"Arizona": 0,"Arkansas": 0,"California": 0,"Colorado": 0,
      "Connecticut": 0,"Delaware": 0,"Florida": 0,"Georgia": 0,"Hawaii": 0,"Idaho": 0,"Illinois": 0,
      "Indiana": 0,"Iowa": 0,"Kansas": 0,"Kentucky": 0,"Louisiana": 0,"Maine": 0,"Maryland": 0,
      "Massachusetts": 0,"Michigan": 0,"Minnesota": 0,"Mississippi": 0,"Missouri": 0,"Montana": 0,
      "Nebraska": 0,"Nevada": 0,"New Hampshire": 0,"New Jersey": 0,"New Mexico": 0,"New York": 0,
      "North Carolina": 0,"North Dakota": 0,"Ohio": 0,"Oklahoma": 0,"Oregon": 0,"Pennsylvania": 0,
      "Rhode Island": 0,"South Carolina": 0,"South Dakota": 0,"Tennessee": 0,"Texas": 0,"Utah": 0,
      "Vermont": 0,"Virginia": 0,"Washington": 0,"West Virginia": 0,"Wisconsin": 0,"Wyoming":0}

    State_Tweets_day3 = {"Alabama": 0,"Alaska": 0,"Arizona": 0,"Arkansas": 0,"California": 0,"Colorado": 0,
      "Connecticut": 0,"Delaware": 0,"Florida": 0,"Georgia": 0,"Hawaii": 0,"Idaho": 0,"Illinois": 0,
      "Indiana": 0,"Iowa": 0,"Kansas": 0,"Kentucky": 0,"Louisiana": 0,"Maine": 0,"Maryland": 0,
      "Massachusetts": 0,"Michigan": 0,"Minnesota": 0,"Mississippi": 0,"Missouri": 0,"Montana": 0,
      "Nebraska": 0,"Nevada": 0,"New Hampshire": 0,"New Jersey": 0,"New Mexico": 0,"New York": 0,
      "North Carolina": 0,"North Dakota": 0,"Ohio": 0,"Oklahoma": 0,"Oregon": 0,"Pennsylvania": 0,
      "Rhode Island": 0,"South Carolina": 0,"South Dakota": 0,"Tennessee": 0,"Texas": 0,"Utah": 0,
      "Vermont": 0,"Virginia": 0,"Washington": 0,"West Virginia": 0,"Wisconsin": 0,"Wyoming":0}

    days = ['2018-02-28','2018-03-01','2018-03-02']
    dayCount = 1

    for tweet in tweetsUsed:
        createdDate = tweet["created_at"][:10]
        locationUsed = tweet["location"]
        if createdDate in days:
            dayTweeted = days.index(createdDate)
            if dayTweeted == 0:
                valuePast = State_Tweets_day1[locationUsed]
                valuePast += 1
                State_Tweets_day1[locationUsed] = valuePast

            elif dayTweeted == 1:
                valuePast = State_Tweets_day2[locationUsed]
                valuePast += 1
                State_Tweets_day2[locationUsed] = valuePast

            elif dayTweeted == 2:
                valuePast = State_Tweets_day3[locationUsed]
                valuePast += 1
                State_Tweets_day3[locationUsed]  = valuePast
    with open("day1Tweets.json", "w") as total:
        json.dump(State_Tweets_day1)

    with open("day2Tweets.json", "w") as total:
        json.dump(State_Tweets_day2)

    with open("day3Tweets.json", "w") as total:
        json.dump(State_Tweets_day3)


cleanTweets()
