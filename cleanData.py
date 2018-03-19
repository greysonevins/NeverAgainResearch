import os
import json

import json
from datetime import datetime
from dateutil import tz
from pandas import DataFrame

# "Annual Estimates of the Resident Population for the United States, Regions, States, and Puerto Rico: April 1, 2010 to July 1, 2016" (XLSX). United States Census Bureau. Retrieved 8 June 2017.
STATES_POPULATION = {
                    "Alabama": 4863300,
                    "Alaska": 741894,
                    "Arizona": 6931071,
                    "Arkansas": 2988248,
                    "California": 39250017,
                    "Colorado": 5540545,
                    "Connecticut": 3576452,
                    "Delaware": 952065,
                    "Florida": 20612439,
                    "Georgia": 10310371,
                    "Hawaii": 1428557,
                    "Idaho": 1683140,
                    "Illinois": 12801539,
                    "Indiana": 6633053,
                    "Iowa": 3134693,
                    "Kansas": 2907289,
                    "Kentucky": 4436974,
                    "Louisiana": 4681666,
                    "Maine": 1331479,
                    "Maryland": 6016447,
                    "Massachusetts": 6811779,
                    "Michigan": 9928300,
                    "Minnesota": 5519952,
                    "Mississippi": 2988726,
                    "Missouri": 6093000,
                    "Montana": 1042520,
                    "Nebraska": 1907116,
                    "Nevada": 2940058,
                    "New Hampshire": 1334795,
                    "New Jersey": 8944469,
                    "New Mexico": 2081015,
                    "New York": 19745289,
                    "North Carolina": 10146788,
                    "North Dakota": 757952,
                    "Ohio": 11614373,
                    "Oklahoma": 3923561,
                    "Oregon": 4093465,
                    "Pennsylvania": 12784227,
                    "Rhode Island": 1056426,
                    "South Carolina": 4961119,
                    "South Dakota": 865454,
                    "Tennessee": 6651194,
                    "Texas": 27862596,
                    "Utah": 3051217,
                    "Vermont": 624594,
                    "Virginia": 8411808,
                    "Washington": 7288000,
                    "West Virginia": 1831102,
                    "Wisconsin": 5778708,
                    "Wyoming": 585501}

# Election Results
# Trump vs. Clinton
# Levaing out Third Party Canidates and Write-Ins
# Votes + or - // The number is irrelevant could be inversed and mean the same
#    Essentially
# https://transition.fec.gov/pubrec/fe2016/2016presgeresults.pdf

STATES_VOTER_RECORDS = {
                    "Alabama":{ "Trump": 1318255, "Clinton":729547},
                    "Alaska":{ "Trump": 163387, "Clinton":116454},
                    "Arizona":{ "Trump": 1252401, "Clinton": 1161167},
                    "Arkansas":{ "Trump": 684872, "Clinton": 380494},
                    "California":{ "Trump": 4483810, "Clinton": 8753788},
                    "Colorado":{ "Trump": 1202484, "Clinton": 1338870},
                    "Connecticut":{ "Trump": 673215, "Clinton": 897572},
                    "Delaware":{ "Trump": 185127, "Clinton": 235603},
                    "Florida":{ "Trump": 4617886, "Clinton": 4504975},
                    "Georgia":{ "Trump": 2089104, "Clinton": 1877963},
                    "Hawaii":{ "Trump": 128847, "Clinton": 266891},
                    "Idaho":{ "Trump": 409055, "Clinton": 189765},
                    "Illinois":{ "Trump": 2146015, "Clinton": 3090729},
                    "Indiana":{ "Trump": 1557286, "Clinton": 1033126},
                    "Iowa":{ "Trump": 800983, "Clinton": 653669},
                    "Kansas":{ "Trump": 671018, "Clinton": 427005},
                    "Kentucky":{ "Trump": 1202971, "Clinton": 628854},
                    "Louisiana":{ "Trump": 1178638, "Clinton": 780154},
                    "Maine":{ "Trump": 335593, "Clinton": 357735},
                    "Maryland":{ "Trump": 943169, "Clinton": 1677928},
                    "Massachusetts":{ "Trump": 1090893, "Clinton": 1995196},
                    "Michigan":{ "Trump": 2279543, "Clinton": 2268839},
                    "Minnesota":{ "Trump": 1322951, "Clinton": 1367716},
                    "Mississippi":{ "Trump": 700714, "Clinton": 485131},
                    "Missouri":{ "Trump": 1594511, "Clinton": 1071068},
                    "Montana":{ "Trump": 279240, "Clinton": 177709},
                    "Nebraska":{ "Trump": 495961, "Clinton": 284494},
                    "Nevada":{ "Trump": 512058 , "Clinton": 539260},
                    "New Hampshire":{ "Trump": 345790, "Clinton": 348526},
                    "New Jersey":{ "Trump": 1601933, "Clinton": 2148278},
                    "New Mexico":{ "Trump": 319667, "Clinton": 385234},
                    "New York":{ "Trump": 2819534, "Clinton": 4556124},
                    "North Carolina":{ "Trump": 2362631, "Clinton": 2189316},
                    "North Dakota":{ "Trump": 216794, "Clinton": 93758},
                    "Ohio":{ "Trump": 2841005, "Clinton": 2394164},
                    "Oklahoma":{ "Trump": 949136, "Clinton": 420375},
                    "Oregon":{ "Trump": 782403, "Clinton": 1002106},
                    "Pennsylvania":{ "Trump": 2970733, "Clinton": 2926441},
                    "Rhode Island":{ "Trump": 180543, "Clinton": 252525},
                    "South Carolina":{ "Trump": 1155389, "Clinton": 855373},
                    "South Dakota":{ "Trump": 227721, "Clinton": 117458},
                    "Tennessee":{ "Trump": 1522925, "Clinton": 870695},
                    "Texas":{ "Trump": 4685047, "Clinton": 3877868},
                    "Utah":{ "Trump": 515231, "Clinton": 310676},
                    "Vermont":{ "Trump": 95369, "Clinton": 178573},
                    "Virginia":{ "Trump": 1769443, "Clinton": 1981473},
                    "Washington":{ "Trump": 1221747, "Clinton": 1742718},
                    "West Virginia":{ "Trump": 489371, "Clinton": 188794},
                    "Wisconsin":{ "Trump": 1405284, "Clinton": 1382536},
                    "Wyoming":{ "Trump": 174419, "Clinton": 55973}
                    }


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

# def timesFix():
#
#     # need to sort the time values into buckets of values by states
#     # should resemble
#     #
#     #           Texas 10PM
#     # different time values tweets at times
#     #  state by
#     #
# def lengthOfTweets():
#     #Lengths of every tweet over the 5 day
#     # then distribute it in R
#     #

def votingRecords():
    # 2016 election results vs. frequency of tweets
    #
    global STATES_VOTER_RECORDS
    changedRecord = {}
    for key, item in STATES_POPULATION.items():
        trumpV = STATES_VOTER_RECORDS[key]["Trump"]
        clintonV = STATES_VOTER_RECORDS[key]["Clinton"]

        normVTrump = trumpV / (item)
        normVClinton = clintonV / (item)

        # positive if more trump // could be anything

        trumpOrClintonState = normVTrump - normVClinton
        changedRecord[key] = trumpOrClintonState

    STATES_VOTER_RECORDS = changedRecord



def newCSV():
    print(NORMTOPFIVESTATES, TOPFIVESTATES)

    ##Soem CSV
    ##
def main():
    # engageTweets()
    # newCSV()
    votingRecords()
    print(STATES_VOTER_RECORDS)

main()
