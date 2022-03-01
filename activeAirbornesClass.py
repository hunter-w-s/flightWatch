import config

class activeAirbornes:
    def __init__(self):
        self.airborneFlights = []
        
    def updateAirbornes(self,currentList):
        regList = []
        notPresent = True
        counterReset = False
        callList = []
        for each in currentList:                
            regList.append(each[0])
            callList.append(each[1])
            
        for each in self.airborneFlights:
            for x in range(len(callList)):
                if each[0] == regList[x] and each[1] == callList[x]:
                    each[2] == 0
                    counterReset = True
                    break
            if counterReset != True:
                each[2] += 1
            counterReset = False

        for x in range(len(callList)):
            for each in self.airborneFlights:
                if each[0] == regList[x] and each[1] == callList[x]:
                    notPresent = False
                    break
            if notPresent:
                self.airborneFlights.append([regList[x],callList[x],0])                

    def cleanAirbornes(self):
        for each in self.airborneFlights:
            if each[2] >= config.reseter:
                self.airborneFlights.remove(each)

    def getAirbornes(self):
        return self.airborneFlights
