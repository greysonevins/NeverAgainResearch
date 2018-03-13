import os
import json

import json
from datetime import datetime
from dateutil import tz

# "Annual Estimates of the Resident Population for the United States, Regions, States, and Puerto Rico: April 1, 2010 to July 1, 2016" (XLSX). United States Census Bureau. Retrieved 8 June 2017.
STATES_POPULATION = {"Alabama": 4863300,"Alaska": 741894,"Arizona": 6931071,"Arkansas": 2988248,"California": 39250017,"Colorado": 5540545,
  "Connecticut": 3576452,"Delaware": 952065,"Florida": 20612439,"Georgia": 10310371,"Hawaii": 1428557,"Idaho": 1683140,"Illinois": 12801539,
  "Indiana": 6633053,"Iowa": 3134693,"Kansas": 2907289,"Kentucky": 4436974,"Louisiana": 4681666,"Maine": 1331479,"Maryland": 6016447,
  "Massachusetts": 6811779,"Michigan": 9928300,"Minnesota": 5519952,"Mississippi": 2988726,"Missouri": 6093000,"Montana": 1042520,
  "Nebraska": 1907116,"Nevada": 2940058,"New Hampshire": 1334795,"New Jersey": 8944469,"New Mexico": 2081015,"New York": 19745289,
  "North Carolina": 10146788,"North Dakota": 757952,"Ohio": 11614373,"Oklahoma": 3923561,"Oregon": 4093465,"Pennsylvania": 12784227,
  "Rhode Island": 1056426,"South Carolina": 4961119,"South Dakota": 865454,"Tennessee": 6651194,"Texas": 27862596,"Utah": 3051217,
  "Vermont": 624594,"Virginia": 8411808,"Washington": 7288000,"West Virginia": 1831102,"Wisconsin": 5778708,"Wyoming": 585501}

TOPFIVESTATES = {
        "day1": [],
        "day2": [],
        "day3": [],
        "day4": []
}

NORMTOPFIVESTATES = {
        "day1": [],
        "day2": [],
        "day3": [],
        "day4": []
}

DAY1:

files = "data/bigDataDates.csv"
filesNorm = "data/bigDataDatesNormal.csv"

def engageTweets():
    global TOPFIVESTATES, NORMTOPFIVESTATES
    day1 = {}
    day2 = {}
    day3 = {}
    day4 = {}
    day1N = {}
    day2N = {}
    day3N = {}
    day4N = {}

    with open("data/day1Tweets.json") as day1:
        day1Amounts = json.load(day1)
        nonNormalized1 = {key: population * day1Amounts[key] for key, population in STATES_POPULATION.items()}
        day1 = sorted(day1Amounts, key=day1Amounts.get, reverse=True)[:5]
        day1N = sorted(nonNormalized1, key=nonNormalized1.get, reverse=True)[:5]
        TOPFIVESTATES["day1"] = day1N
        NORMTOPFIVESTATES["day1"] = day1


    with open("data/day2Tweets.json") as day2:
        day2Amounts = json.load(day2)
        nonNormalized2 = {key: day2Amounts[key] *  population for key, population in STATES_POPULATION.items()}
        day2 = sorted(day2Amounts, key=day2Amounts.get, reverse=True)[:5]
        day2N = sorted(nonNormalized2, key=nonNormalized2.get, reverse=True)[:5]
        TOPFIVESTATES["day2"] = day2N
        NORMTOPFIVESTATES["day2"] = day2


    with open("data/day3Tweets.json") as day3:
        day3Amounts = json.load(day3)
        nonNormalized3 = {key: day3Amounts[key] * population for key, population in STATES_POPULATION.items()}
        day3 = sorted(day3Amounts, key=day3Amounts.get, reverse=True)[:5]
        day3N = sorted(nonNormalized3, key=nonNormalized3.get, reverse=True)[:5]
        TOPFIVESTATES["day3"] = day3N
        NORMTOPFIVESTATES["day3"] = day3

    with open("data/day4Tweets.json") as day4:
        day4Amounts = json.load(day4)
        nonNormalized4 = {key: day4Amounts[key] * population for key, population in STATES_POPULATION.items()}
        day4 = sorted(day4Amounts, key=day4Amounts.get, reverse=True)[:5]
        day4N = sorted(nonNormalized4, key=nonNormalized4.get, reverse=True)[:5]
        TOPFIVESTATES["day4"] = day4N
        NORMTOPFIVESTATES["day4"] = day4

def timesFix():
    # need to sort the time values into buckets of values by states
    # should resemble
    #
    #           Texas 10PM
    #
    #
def newCSV():
    print(NORMTOPFIVESTATES, TOPFIVESTATES)

    ##Soem CSV
    ##
def main():
    engageTweets()
    newCSV()

main()
