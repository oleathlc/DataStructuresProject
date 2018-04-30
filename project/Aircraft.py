import csv

class Aircraft(object):
    '''
    Aircraft class: An Airplane has to be filled before it can take off
    '''

    def __init__(self, code, units, fuel):
        self.code = code
        self.fuel = fuel
        self.units = units
        
    def getFuel(self):
        return self.fuel
    
    def getUnits(self):
        return self.units
        
    
class aircraftAtlas(object):
    '''
    classdocs
    '''
    def loadData(self, csvFile):
        self.aircrafts = {}
        filename = csvFile
        with open(filename,"rt", encoding = "utf8") as f:
            reader = csv.reader(f)
            for line in reader:
                self.aircrafts[line[0]] = Aircraft(line[0], line[3], line[4])       
        return self.aircrafts
    
    def __init__(self,csvFile):
        '''Constructor'''
        self.csvFile = csvFile
        self.loadData(csvFile)
    
    def getAircraft(self,code):
        self.aircraft = self.aircrafts[code]
        return self.aircraft

            
            
            
            
            