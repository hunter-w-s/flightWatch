import config

class activeAirbornes():
    def __init__(self):
        self.airborneFlights = []
        
    def updateAirbornes(self,currentList):
        existsInList = False
        for each in self.airborneFlights:
            if each[0] in currentList:
                each[1] = 0
            else:
                each[1] += 1

        for each in currentList:
            for listed in self.airborneFlights:
                if each == listed[0]:
                    existsInList = True
                    break
            if existsInList != True:
                self.airborneFlights.append([each,0])
            existsInList = False
                

    def addToAirbornes(self,reg):
        self.airborneFlights.append([reg,0])

    def cleanAirbornes(self):
        for each in self.airborneFlights:
            if each[1] >= config.reseter:
                self.airborneFlights.remove(each)
