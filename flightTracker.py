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
    'x-rapidapi-key': "843a92fc7emsh0158a368f38b677p17d9d0jsnb0c2635d1406"
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
                                   "Aircraft Detected",flightInfo["call"],flightLat,flightLong])
            

    for each in currentFlights:            
        for x in range(len(each)):
            if len(each[x]) == 0:
                each[x] = "N/A"


    
    
    tempRegList = []
    for each in currentFlights:
        tempRegList.append([each[0],each[5]])
        

    tempFlightList = []
    newFlight = True
    for each in currentFlights:
        for live in airbornes.airborneFlights:
            if each[5] == live[1] and each[0] == live[0]:
                newFlight = False
                break
        if newFlight:
            tempFlightList.append(each)
        newFlight = True
        
    #print(tempFlightList)

    airbornes.updateAirbornes(tempRegList)

    oldFlights = currentFlights
    currentFlights = []

    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    print("date and time =", dt_string)

    
    aircraftPictureLocated = False
    if len(tempFlightList) != 0:
        for each in tempFlightList:            
            try:
                tweetMessage = "Time: {} EST\n{}\nAircraft ID: {}\nCallsign: {}\nOwner: {}\nCountry: {}\nLat: {}\nLon: {}\n\n#Aviation #AirForce #Europe".format(dt_string,each[4],each[1],each[5],each[3],each[2],each[6][:5],each[7][:5])
                #print(tweetMessage)
                #print(len(tweetMessage))
                #print("\n")
                if firstLoop == True:
                    continue
                for pictures in planePictureList:
                    if each[1] == pictures[0]:
                        #print("Picture Located")
                        api.update_status_with_media(status = tweetMessage, filename = pictures[1])
                        aircraftPictureLocated = True
                        break
                if aircraftPictureLocated == False:
                    print("Picture Missing: {} : {}".format(each[1],each[0]))
                    api.update_status(status = tweetMessage)
            except Exception as e:
                print(e)
            aircraftPictureLocated = False
            #print(tweetMessage)

    tempFlightList = []
    
    airbornes.cleanAirbornes()
    print(len(airbornes.airborneFlights))
    print(airbornes.airborneFlights)
    print("\n")
    firstLoop = False
    time.sleep(420)
