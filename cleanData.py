import os
import json
from datetime import datetime, time, timedelta
from pandas import DataFrame
import re
from dateutil.rrule import *

# Estimates of the Voting Age Population for 2016
# from https://www.federalregister.gov/documents/2017/01/30/2017-01890/estimates-of-the-voting-age-population-for-2016
STATES__VOTING_POPULATION = {
                    "Alabama": 3766477,
                    "Alaska": 554567,
                    "Arizona": 5299579,
                    "Arkansas": 2283195,
                    "California": 30157154,
                    "Colorado": 4279173,
                    "Connecticut": 2823158,
                    "Delaware": 747791,
                    "Florida": 16465727,
                    "Georgia": 7798827,
                    "Hawaii": 1120541,
                    "Idaho": 1245967,
                    "Illinois": 9875430,
                    "Indiana": 5057601,
                    "Iowa": 2403962,
                    "Kansas": 2192338,
                    "Kentucky": 3426345,
                    "Louisiana": 3567717,
                    "Maine": 1076765,
                    "Maryland": 4667719,
                    "Massachusetts": 5433677,
                    "Michigan": 7737243,
                    "Minnesota": 4231619,
                    "Mississippi": 2267438,
                    "Missouri": 4706137,
                    "Montana": 814909,
                    "Nebraska": 1433791,
                    "Nevada": 2262631,
                    "New Hampshire": 1074207,
                    "New Jersey": 6959717,
                    "New Mexico": 1590352,
                    "New York": 15564730,
                    "North Carolina": 7848068,
                    "North Dakota": 581641,
                    "Ohio": 9002201,
                    "Oklahoma": 2961933,
                    "Oregon": 3224738,
                    "Pennsylvania": 10109422,
                    "Rhode Island": 848045,
                    "South Carolina": 3863498,
                    "South Dakota": 652167,
                    "Tennessee": 5149399,
                    "Texas": 20568009,
                    "Utah": 2129444,
                    "Vermont": 506066,
                    "Virginia": 6541685,
                    "Washington": 5658502,
                    "West Virginia": 1456034,
                    "Wisconsin": 4491015,
                    "Wyoming": 446600
                    }
# "Annual Estimates of the Resident Population for the United States, Regions,
#   United States, and Puerto Rico: April 1, 2010 to July 1, 2016" (XLSX).
#   Census Bureau. Retrieved 8 June 2017.
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

## Decided not to work with the nonnormalized tweets
TOPFIVESTATES = []
NORMTOPFIVESTATES = []

files = "data/bigDataDates.csv"
filesNorm = "data/bigDataDatesNormal.csv"

def engageTweets():
    global TOPFIVESTATES, NORMTOPFIVESTATES

    dayTotal = {}
    dayNormTotal = {}

    with open("data/day1Tweets.json") as day1:
        dayNormTL = json.load(day1)
        dayTotal = {key: population * dayNormTL[key] for key, population in STATES_POPULATION.items()}

    with open("data/day2Tweets.json") as day2:
        day2Amounts = json.load(day2)
        nonNormalized2 = {key: day2Amounts[key] *  population for key, population in STATES_POPULATION.items()}
        dayNormTL = {key: day2Amounts[key] +  total for key, total in dayNormTL.items()}
        dayTotal = {key: nonNormalized2[key] +  total for key, total in dayTotal.items()}

    with open("data/day3Tweets.json") as day3:
        day3Amounts = json.load(day3)
        nonNormalized3 = {key: day3Amounts[key] * population for key, population in STATES_POPULATION.items()}
        dayNormTL = {key: day3Amounts[key] +  total for key, total in dayNormTL.items()}
        dayTotal = {key: nonNormalized3[key] +  total for key, total in dayTotal.items()}

    with open("data/day4Tweets.json") as day4:
        day4Amounts = json.load(day4)
        nonNormalized4 = {key: day4Amounts[key] * population for key, population in STATES_POPULATION.items()}
        dayNormTL = {key: day4Amounts[key] +  total for key, total in dayNormTL.items()}
        dayTotal = {key: nonNormalized4[key] +  total for key, total in dayTotal.items()}
        dayNT = sorted(dayNormTL, key=dayNormTL.get, reverse=True)[:5]
        dayT = sorted(dayTotal, key=dayTotal.get, reverse=True)[:5]

        TOPFIVESTATES = dayT
        NORMTOPFIVESTATES = dayNT

def timesFix():

    # need to sort the time values into buckets of values by states
    # should resemble
    #
    #           Texas 10PM
    # different time values tweets at times
    #  state by

    tweetsUsed = []
    startTime = 0
    endTime = 0

    with open("data/usefulTweets.json") as tw:
        tweetsUsed = json.load(tw)


    # 3 files (15,30,1 hour)
    #
    masterNorm = []
    masterTotal = []
    tweetsUsed.reverse()

    for tweet in tweetsUsed:
        if tweet["location"] in TOPFIVESTATES:
            time = tweet["created_at"]
            try:
                tweet["created_at"] = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            except TypeError:
                pass
            masterTotal.append(tweet)
        if tweet["location"] in NORMTOPFIVESTATES:
            time = tweet["created_at"]
            try:
                tweet["created_at"] = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            except TypeError:
                pass
            masterNorm.append(tweet)

    masterNormTime = list(map(lambda t: t["created_at"],masterNorm))
    indexBeg = 0
    indexEnd = 0
    for i, time in enumerate(masterNormTime):
        if time.date() == datetime(2018, 2, 27).date() and not indexBeg:
            indexBeg = i
        if time.date() == datetime(2018, 3, 3).date() and not indexEnd:
            indexEnd = i
        else:
            continue

    masterNorm = masterNorm[indexBeg:indexEnd]

    startTime = masterNorm[0]["created_at"].date()
    endTimeTry1 = masterNorm[-1]["created_at"].date()
    endTime = endTimeTry1 + timedelta(days=1)

    loop15Minutes = list(rrule(MINUTELY, interval=15, dtstart=startTime,
                                until=endTime))
    loop30Minutes = list(rrule(MINUTELY, interval=30, dtstart=startTime,
                                until=endTime))
    loopHourly = list(rrule(HOURLY, interval=1, dtstart=startTime,
                                until=endTime))
    indexLoop15 = list(map(lambda t: t.strftime('%Y-%m-%d %H:%M:%S'),
                                        loop15Minutes))
    indexLoop30 = list(map(lambda t: t.strftime('%Y-%m-%d %H:%M:%S'),
                                        loop30Minutes))
    indexLoop60 = list(map(lambda t: t.strftime('%Y-%m-%d %H:%M:%S'),
                                        loopHourly))

    states15N = { key: [0] * len(loop15Minutes) for key in NORMTOPFIVESTATES }
    states30N = { key: [0] * len(loop30Minutes) for key in NORMTOPFIVESTATES }
    states60N = { key: [0] * len(loopHourly) for key in NORMTOPFIVESTATES }

    counter = 0
    index = 0

    for time in loop15Minutes:
        working = True
        while working:
            if not len(masterNorm) == index:
                twTime = masterNorm[index]["created_at"]
                twLocation = masterNorm[index]["location"]
                if twTime >= time and twTime <= loop15Minutes[counter+1]:
                    states15N[twLocation][counter] += 1
                    index +=1
                    pass
                else:
                    working = False
            else:
                working = False

        # for state, items in states15N.items():
        #     items[counter] = (
        #             (items[counter] /
        #                 STATES_POPULATION[state])
        #                 * 1000000
        #                 )
        #     states15N[state] = items
        counter += 1
        continue

    counter = 0
    index = 0

    for time in loop30Minutes:
        working = True
        while working:
            if not len(masterNorm) == index:
                twTime = masterNorm[index]["created_at"]
                twLocation = masterNorm[index]["location"]
                if twTime >= time and twTime <= loop30Minutes[counter+1]:
                    states30N[twLocation][counter] += 1
                    index +=1
                    pass
                else:
                    working = False
            else:
                working = False

        # for state, items in states30N.items():
        #     items[counter] = (
        #             (items[counter] /
        #                 STATES_POPULATION[state])
        #                 * 1000000
        #                 )
        #     states30N[state] = items
        counter += 1
        continue

    counter = 0
    index = 0
    for time in loopHourly:
        working = True
        while working:
            if not len(masterNorm) == index:
                twTime = masterNorm[index]["created_at"]
                twLocation = masterNorm[index]["location"]
                if twTime >= time and twTime <= loopHourly[counter+1]:
                    states60N[twLocation][counter] += 1
                    index +=1
                    pass
                else:
                    working = False
            else:
                working = False

        # for state, items in states60N.items():
        #     items[counter] = (
        #             (items[counter] /
        #                 STATES_POPULATION[state])
        #                 * 1000000
        #                 )
        counter += 1
        continue
    states15N["Times"] = indexLoop15
    states30N["Times"] = indexLoop30
    states60N["Times"] = indexLoop60

    tweets15 = DataFrame(states15N)
    tweets30 = DataFrame(states30N)
    tweets60 = DataFrame(states60N)

    tweets15.to_csv("data/tweets15Days.csv")
    tweets30.to_csv("data/tweets30Days.csv")
    tweets60.to_csv("data/tweets60Days.csv")

### Issue with numbers coming up the same....
    ### Need to fix this

def lengthOfTweets():
    #Lengths of every tweet over the 5 day
    # then distribute it in R
    tweetsUsed = {}

    with open("data/usefulTweets.json") as tw:
        tweetsUsed = json.load(tw)

    tweetData = {"textLength": [], "location": [], "time": []}
    for tweet in tweetsUsed:
        textUsed = tweet["text"]
        tweetTime = tweet["created_at"]
        state = tweet["location"]

        wordRe = re.compile('[A-Za-z]+')
        wordsTry = wordRe.findall(textUsed)
        chopNumber = 0

        for word in wordsTry:
            try:
                chopNumber = word.index("http")
            except ValueError:
                continue

            try:
                chopNumber = word.index("https")
            except ValueError:
                continue
        wordCount = 0
        if chopNumber:
            wordCount = len(wordsTry[0:chopNumber])
        else:
            wordCount = len(wordsTry)

        tweetData["textLength"].append(wordCount)
        tweetData["location"].append(state)
        tweetData["time"].append(tweetTime)

    tweetLengthDF = DataFrame(tweetData)

    tweetLengthDF.to_csv("data/lengthOfTweets.csv", index=False)

def votingRecords():
    # 2016 election results vs. frequency of tweets
    global STATES_VOTER_RECORDS

    changedRecord = {}
    totals = []
    states = []
    for key, item in STATES__VOTING_POPULATION.items():
        trumpV = STATES_VOTER_RECORDS[key]["Trump"]
        clintonV = STATES_VOTER_RECORDS[key]["Clinton"]

        normVTrump = trumpV / (item)
        normVClinton = clintonV / (item)

        # positive if more Clinton // could be anything
        # assumption is that more Clinton means more engagement
        # turn to CSV

        trumpOrClintonState = normVClinton - normVTrump

        changedRecord[key] = trumpOrClintonState
        totals.append(trumpOrClintonState)
        states.append(key)

    STATES_VOTER_RECORDS = changedRecord
    dayList = ["1", "2", "3", "4"]
    totalsData = {"votingRecord": totals,
    "day1": [],
    "day2": [],
    "day3": [],
    "day4": []
    }
    totalTweetsVPolitics = {"t"}
    for day in dayList:
        dayFile = "data/day"+day+"Tweets.json"
        dayName = "day"+day
        jsonDay = {}
        with open(dayFile) as fle:
            jsonDay = json.load(fle)
        for key, stTotal in jsonDay.items():
            totalsData[dayName].append(stTotal)

    tweetDaysPolitics = DataFrame(totalsData, index=states)

    tweetDaysPolitics.to_csv("data/politicsOfTweets.csv")




    # with open("")


# def newCSV():
#     print(NORMTOPFIVESTATES, TOPFIVESTATES)
#
#     ##Soem CSV
    ##
def main():
    engageTweets()
    votingRecords()
    timesFix()
    # lengthOfTweets()

main()
