from FlightRadar24.api import FlightRadar24API
import time
import tweepy
from datetime import datetime
import config, apiKeys, airInfo, activeAirbornesClass, requests, json


#Creates the Tweepy API Auth
auth = tweepy.OAuthHandler(apiKeys.tweepyConsumeKey, 
    apiKeys.tweepyConsumeSecret)

auth.set_access_token(apiKeys.tweepyAccessKey, 
    apiKeys.tweepyAccessSecret)

api = tweepy.API(auth, wait_on_rate_limit=True)

#api.update_status(status = "Hello Twitter")

#Gets Flight Data
fr_api = FlightRadar24API()

url = "https://adsbexchange-com1.p.rapidapi.com/mil/"

headers = {
    'x-rapidapi-host': "adsbexchange-com1.p.rapidapi.com",
    'x-rapidapi-key': config.rapidAPIKey
    }

upperLat = float(config.upperLat)
lowerLat = float(config.lowerLat)
upperLong = float(config.upperLong)
lowerLong = float(config.lowerLong)
firstLoop = config.firstLoop
reseter = config.reseter
planePictureList = airInfo.planePictureListing
airbaseInfo = airInfo.airbaseInfo
airbornes = activeAirbornesClass.activeAirbornes
callsignList = airInfo.callsignPrefix

airborneFlights = []
oldFlights = []
currentFlights = []
tempFlightList = []


class NestEscape(Exception): pass

airbornes = activeAirbornesClass.activeAirbornes()

while True:
    while True:
        try:
            response = requests.request("GET", url, headers=headers)
            break
        except Exception as e:
            print(e)
            time.sleep(420)
    response = json.loads(response.text)
    for each in response["ac"]:
        
        flightInfo = each
        flightLat = (flightInfo["lat"])
        flightLong = (flightInfo["lon"])
        flightAlt = (flightInfo["alt"])

        if flightLat == "" or flightLong == "":
            continue

        if flightInfo["reg"] == "" and flightInfo["call"] == "" or flightInfo["type"] == "" or flightInfo["type"] == "TEST":
            continue

        if "GROUND" in flightAlt.upper() or flightAlt == "":
            continue

        try:
            flightAlt = int(flightAlt)
        except:
            continue
                          
        if (flightAlt >= 2000 and float(flightLat) <= upperLat and float(flightLat) >= lowerLat and float(flightLong) <= upperLong and float(flightLong) >= lowerLong):
            currentFlights.append([flightInfo["reg"],flightInfo["type"],flightInfo["cou"],flightInfo["opicao"],
                                   "Aircraft Detected",flightInfo["call"],flightLat,flightLong,flightInfo["icao"]])
            

    for each in currentFlights:            
        for x in range(len(each)):
            if len(each[x]) == 0:
                each[x] = "N/A"


    
    
    tempRegList = []
    for each in currentFlights:
        tempRegList.append(each[8])

    tempFlightList = []
    newFlight = True
    for each in currentFlights:
        for live in airbornes.airborneFlights:
            if each[8] == live[0]:
                newFlight = False
                break
        if newFlight:
            tempFlightList.append(each)
        newFlight = True

    airbornes.updateAirbornes(tempRegList)
    
    currentFlights = []

    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M")


    if len(tempFlightList) != 0:
        if firstLoop == True:
            continue

        postPicsExist = []
        postPictures = []
        postMediaIDs = []
        postText = []
        infoCounter = 0
        for x in range(len(tempFlightList)):
            
            postText.append("Aircraft: {}\nCallsign: {}\nLat: {}\nLon: {}\n\n".format(tempFlightList[x][1],tempFlightList[x][5],tempFlightList[x][6][:4],tempFlightList[x][7][:4]))
            for pictures in planePictureList:
                    if tempFlightList[x][1] == pictures[0]:
                        #print("Picture Located")
                        postPicsExist.append(pictures[1])
                        break
                    
            infoCounter += 1
            if infoCounter == 4 or x+1 == len(tempFlightList):
                tweetMessage = "Time: {} EST\n\n".format(dt_string)
                for each in postText:
                    tweetMessage += each

                for each in postPicsExist:
                    if each not in postPictures:
                        postPictures.append(each)

                for each in postPictures:
                    res = api.media_upload(config.picPath + each)
                    postMediaIDs.append(res.media_id)

                tweetMessage += "#Aviation #Europe"
                print(tweetMessage)
                print(len(tweetMessage))

                infoCounter = 0

                if len(postMediaIDs) > 0:
                    api.update_status(status = tweetMessage, media_ids = postMediaIDs)
                else:
                    api.update_status(status = tweetMessage)

                postPicsExist = []
                postPictures = []
                postMediaIDs = []
                postText = []

    tempFlightList = []
    
    airbornes.cleanAirbornes()
    print(len(airbornes.airborneFlights))
    print(airbornes.airborneFlights)
    print("\n")
    firstLoop = False
    time.sleep(420)
