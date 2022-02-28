from FlightRadar24.api import FlightRadar24API
import time
import tweepy
from datetime import datetime

#Creates the Tweepy API Auth
auth = tweepy.OAuthHandler("1Ae6znw6op7ZbfPc8f0wXXDMt", 
    "zM7Aw2dNEeBHgpAUW0zqvOnSRTkjeBwKdrtP1PUXnOzRgBuOIT")

auth.set_access_token("1497239674049511428-IV39RuVHFwFgBO4JlYLWU1ku4OKWe1", 
    "2C2oKZKjXNfDhH70UGSX5aeke3ik4Tv33AcZGWqKsuqfg")

api = tweepy.API(auth, wait_on_rate_limit=True)

#api.update_status(status = "Hello Twitter")

#Gets Flight Data
fr_api = FlightRadar24API()

airbaseInfo = {
    "IATA_KEY":{
    "MHZ" : {"IATA":"MHZ",
             "ICAO":"EGUN",
             "Name":"RAF Mildenhall"
             },
    "RMS" : {"IATA":"RMS",
             "ICAO":"ETAR",
             "Name":"Ramstein Air Base"
             },
    "AVB" : {"IATA":"AVB",
             "ICAO":"LIPA",
             "Name":"Aviano Air Base"
             },
    "UAB" : {"IATA":"UAB",
             "ICAO":"LTAG",
             "Name":"Incirlik Air Base"
             },
    "OZP" : {"IATA":"OZP",
             "ICAO":"LEMO",
             "Name":"Moron Air Base"
             },
    "GKE" : {"IATA":"GKE",
             "ICAO":"ETNG",
             "Name":"NATO Air Base Geilenkirchen"
             },
    "AYH" : {"IATA":"AYH",
             "ICAO":"EGWZ",
             "Name":"RAF Alconbury"
             },
    "FFD" : {"IATA":"FFD",
             "ICAO":"EGVA",
             "Name":"RAF Fairford"
             },
    "LKZ" : {"IATA":"LKZ",
             "ICAO":"EGUL",
             "Name":"RAF Lakenheath"
             },
    "SPM" : {"IATA":"SPM",
             "ICAO":"ETAD",
             "Name":"Spangdahlem Air Base"
             },
    "UDE" : {"IATA":"UDE",
             "ICAO":"EHVL",
             "Name":"Vokel Air Base"
             },
    "N/A" : {"IATA":"N/A",
             "ICAO":"N/A",
             "Name":"Unlisted Origin"
             }
    },
    "ICAO_KEY":{
    "ETSB" : {"IATA": None,
             "ICAO":"ETSB",
             "Name":"Büchel Air Base"
             },
    "EBCV" : {"IATA": None,
             "ICAO":"EBCV",
             "Name":"Chièvres Air Base"
             },
    "LHPA" : {"IATA": None,
             "ICAO":"LHPA",
             "Name":"Pápa Air Base"
             },
    "EBBL" : {"IATA": None,
             "ICAO":"EBBL",
             "Name":"Kleine Brogel Air Base"
             },
    "EGUN" : {"IATA":"MHZ",
             "ICAO":"EGUN",
             "Name":"RAF Mildenhall"
             },
    "ETAR" : {"IATA":"RMS",
             "ICAO":"ETAR",
             "Name":"Ramstein Air Base"
             },
    "LIPA" : {"IATA":"AVB",
             "ICAO":"LIPA",
             "Name":"Aviano Air Base"
             },
    "LTAG" : {"IATA":"UAB",
             "ICAO":"LTAG",
             "Name":"Incirlik Air Base"
             },
    "LPLA" : {"IATA":"TER",
             "ICAO":"LPLA",
             "Name":"Lajes Field"
             },
    "LEMO" : {"IATA":"OZP",
             "ICAO":"LEMO",
             "Name":"Moron Air Base"
             },
    "ETNG" : {"IATA":"GKE",
             "ICAO":"ETNG",
             "Name":"NATO Air Base Geilenkirchen"
             },
    "EGWZ" : {"IATA":"AYH",
             "ICAO":"EGWZ",
             "Name":"RAF Alconbury"
             },
    "EGVA" : {"IATA":"FFD",
             "ICAO":"EGVA",
             "Name":"RAF Fairford"
             },
    "EGUL" : {"IATA":"LKZ",
             "ICAO":"EGUL",
             "Name":"RAF Lakenheath"
             },
    "ETAD" : {"IATA":"SPM",
             "ICAO":"ETAD",
             "Name":"Spangdahlem Air Base"
             },
    "EHVL" : {"IATA":"UDE",
             "ICAO":"EHVL",
             "Name":"Vokel Air Base"
             }
    }
    }

upperLat = 75
lowerLat = 35
upperLong = 40
lowerLong = -15
firstLoop = True


airborneFlights = []
oldFlights = []
currentFlights = []
tempFlightList = []
reseter = 30

planePictureList = [["DC10","kc10.jpg"],["K35R","kc135.jpg"],["C17","c17.jpg"],["CL60","cl60.jpg"],["Q4","q4.jpg"],["A332","a332.jpg"],["R135","r135.jpg"],["H60","uh60.jpg"]]

def updateAirbornes(currentList):
    existsInList = False
    for each in airborneFlights:
        if each[0] in currentList:
            each[1] = 0
        else:
            each[1] += 1

    for each in currentList:
        for listed in airborneFlights:
            if each == listed[0]:
                existsInList = True
                break
        if existsInList != True:
            airborneFlights.append([each,0])
        existsInList = False
                

def addToAirbornes(reg):
    airborneFlights.append([reg,0])

def cleanAirbornes():
    for each in airborneFlights:
        if each[1] >= reseter:
            airborneFlights.remove(each)

class NestEscape(Exception): pass


callsignList = ["FORTE","LAGR","KAYAK","NCHO","HOLD","JAKE","HOMER","PYTHON56","RCH","CNV","086205","095713","VIPER41","NATO","COBRA","REDEYE6","SVF622","RSD","RA","RFF6118","RF82040","RF82013"
                "RF82013","CTA","KK","RRR","RFR","CTM","GAF","CL60","DUKE","BRK","PLF","RMAF","TUAF","IAM","MMF","SPTYT","CFC","HAF"]


while True:
    while True:
        try:
            flights = fr_api.get_flights()
            break
        except Exception as e:
            print(e)
            time.sleep(60)
    
    for each in flights:
        try:
            for callS in callsignList:
                if callS == each.callsign[:len(callS)] and each.aircraft_code != "GRND" and int(each.latitude) > lowerLat and int(each.latitude) < upperLat and int(each.longitude) > lowerLong and int(each.longitude) < upperLong:
                    currentFlights.append([each.registration,each.aircraft_code,each.origin_airport_iata,"Aircraft Detected",each.callsign,each.latitude,each.longitude])
                    print("New Method")
                    raise NestEscape()
        except NestEscape:
            continue
                
        if each.origin_airport_iata in airbaseInfo["IATA_KEY"] and each.origin_airport_iata != "N/A":
            currentFlights.append([each.registration,each.aircraft_code,each.origin_airport_iata,"Likely Departure",each.callsign,each.latitude,each.longitude])
            continue
        if int(each.altitude ) >= 50000 and int(each.latitude) > lowerLat and int(each.latitude) < upperLat and int(each.longitude) > lowerLong and int(each.longitude) < upperLong:
            currentFlights.append([each.registration,each.aircraft_code,each.origin_airport_iata,"Aircraft Detected Above FL500",each.callsign,each.latitude,each.longitude])
            continue

    
    tempRegList = []
    for each in currentFlights:
        tempRegList.append(each[4])

    tempFlightList = []
    newFlight = True
    for each in currentFlights:
        for live in airborneFlights:
            if each[4] == live[0]:
                newFlight = False
                break
        if newFlight:
            tempFlightList.append(each)
        newFlight = True
    print(tempFlightList)

    updateAirbornes(tempRegList)



    
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
                tweetMessage = "Time: {}\n{}\nAircraft ID: {}\nCallsign: {}\nOrigin Airport: {}\nLat: {}\nLong: {}\n\n#Aviation #AirForce #Europe".format(dt_string,each[3],each[1],each[4],airbaseInfo["IATA_KEY"][each[2]]["Name"],each[5],each[6])
                print(tweetMessage)
                print(len(tweetMessage))
                print("\n")
                if firstLoop == True:
                    continue
                for pictures in planePictureList:
                    print(each[1] == pictures[0])
                    print(each[1])
                    print(pictures[0])
                    if each[1] == pictures[0]:
                        print("Picture Located")
                        
                        api.update_status_with_media(status = tweetMessage, filename = pictures[1])
                        aircraftPictureLocated = True
                        break
                if aircraftPictureLocated == False:
                    api.update_status(status = tweetMessage)
                break
            except Exception as e:
                print(e)
            #print(tweetMessage)
            
    tempFlightList = []    
    cleanAirbornes()
    print(airborneFlights)
    print("\n")
    firstLoop = False
    time.sleep(120)
