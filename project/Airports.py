import csv
from math import pi, sin, cos, acos

class Airport(object):
    """
    Create an airport object
    """
    def __init__(self, airportName,cityName, country, latitude, longitude):
        self.airportName = airportName
        self.cityName = cityName
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        #self.exchange = exchange
    
    def __str__(self):
        return self.airportName, self.cityName, self.country, self.latitude, self.longitude
    
    

class airportAtlas(object):
    '''
    Create and airport atlas
    '''
    def loadData(self, csvFile):
        self.airports = {}
        filename = csvFile
        with open(filename,"rt", encoding = "utf8") as f:
            reader = csv.reader(f)
            for line in reader:
                self.airports[line[4]] = Airport(line[1], line[2],line[3], float(line[6]), float(line[7]))       
        return self.airports
    
    def __init__(self,csvFile):
        '''Constructor'''
        self.csvFile = csvFile
        self.loadData(csvFile)
    
    def getAirport(self,code):
        self.airport = self.airports[code]
        return self.airport 
    
    def greatcircledist(self,lat1,lat2,lon1,lon2):
        '''Calculate distance between airports'''
        earthRad = 6371
        theta1 = lon1 * (2 * pi) / 360
        theta2 = lon2 * (2 * pi) / 360
        phi1 = (90 - lat1) * (2 * pi) / 360
        phi2 = (90 - lat2) * (2 * pi) / 360
        distance = acos(sin(phi1) * sin(phi2) * cos(theta1 - theta2) + cos(phi1) * cos(phi2)) * earthRad
        return distance
    
    def distanceBetweenAirports(self, airp1, airp2):
        airp1 = self.getAirport(airp1)
        airp2 = self.getAirport(airp2)
        lat1 = airp1.latitude
        lat2 = airp2.latitude
        long1 = airp1.longitude
        long2 = airp2.longitude
        distance = self.greatcircledist(lat1, lat2, long1, long2)
        return distance

    
    
    