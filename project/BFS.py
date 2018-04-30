from Airports import Airport, airportAtlas
from Aircraft import Aircraft, aircraftAtlas
from Currency import Currency, currencyCreator
import csv
import pandas as pd
import queue

def main(csvFile):
    """
    This is the main method that reads in a csv of test routes. For each route it calls the route planner function
    and prints the results out. If there is any missing data or incorrect data read in, it prints out to say as much
    and then continues on until the file has been read in full.
    """
    filename = csvFile
    with open(filename,"rt", encoding = "utf8") as f:
        reader = csv.reader(f)
        for line in reader:
            start, A, B, C, D, aircraft = line[0],line[1],line[2],line[3],line[4],line[5]
            if start == '' or A == '' or B == '' or C == '' or D == '' or aircraft == '': #Handling empty cells
                print("Proposed journey and aircraft: ", start, A, B, C, D, aircraft)
                print("Proposed route and cost : Itinerary not possible due to missing data")
                print('======================================================================')
            #Elif statement below handles airports in cell that doesn't exist in the airports dictionary (from airport csv file)
            elif start not in airports.airports or A not in airports.airports or B not in airports.airports or C not in airports.airports or D not in airports.airports:
                print("Proposed journey and aircraft: ", start, A, B, C, D, aircraft)
                print("Proposed route and cost : Itinerary not possible due to incorrect data")
                print('======================================================================')
            elif aircraft not in aircrafts.aircrafts: #Handling instants where the aircraft chosen isn't in the aircraft dictionary (from aircraft csv file)
                print("Proposed journey and aircraft: ", start, A, B, C, D, aircraft)
                print("Proposed route and cost : Itinerary not possible due to incorrect data")
                print('======================================================================')
            else: #Call the route planner method to get the best itinerary
                print("Proposed journey and aircraft: ", start, A, B, C, D, aircraft)
                print("Proposed route and cost :", planner(start, A, B, C, D, aircraft))
                print('======================================================================')

def planner(start,A,B,C,D,craft):
    """
    This method reads in the proposed route and aircraft. It creates a set of the possible destinations and tries to determine
    the cheapest route, appending the results to a csv (via saveToCSV method) and then returning them.
    """
    proposed = list([start, A, B, C, D,start,"Not feasible", craft]) #To be printed out if itinerary not feasible
    end=start #Sets end-point to be same as start
    destinations = set([A,B,C,D]) #Set containing intermediary airports (unordered)
    flightplan = queue.Queue(maxsize=6) #Queue to store all the airports in order for the chosen itinerary
    flightplan.put(start)
    cost = 0 #Variable to hold cost of the journey
    aircraft = aircrafts.getAircraft(craft) #Get the aircraft from the dictionary so the fuel capacity (i.e. range) can be calculated
    flightRange = float(aircraft.getFuel())
    if aircraft.getUnits() == 'imperial':#Convert to km if in miles
        flightRange *= 1.60934
    
    while len(destinations) != 0: #While the set isn't empty 
        destination, distance = getDestination(start, destinations,flightRange) #Get airport with shortest distance from the start for this leg
        if destination == 'too' and distance == 4: #Code sent back to say no feasible route for this leg
            saveToCSV(proposed)
            return "Cannot complete this itinerary with proposed aircraft"
        cost += distance
        flightplan.put(destination)
        destinations.remove(destination)
        start = destination
        
    destination, distance = getDestination(start, [end], flightRange)  #Get distance from last airport to home airport for this leg
    if destination == 'too' and distance == 4: #Code sent back to say no feasible route for this leg
        saveToCSV(proposed)
        return "Cannot complete this itinerary with proposed aircraft"
    cost += distance
    flightplan.put(destination)
    plan = list([]) #List to contain the itinerary to send back to main function
    while not flightplan.empty(): #Dequeue into the plan list until queue is empty
        plan.append(flightplan.get())
    plan.append(cost)
    plan.append(craft)
    saveToCSV(plan)
    return plan

def saveToCSV(route):
    """
    This method takes in the itinerary and appends it to a csv file
    """
    with open('../input/bestroute.csv',"a", encoding = "utf8") as f:
        writer = csv.writer(f, delimiter=',', quotechar=" ", quoting=csv.QUOTE_ALL)
        writer.writerow(route)

def getDestination(start,destinations,limit):
    """
    This method takes in a starting point, list of destinations and a limit. It compares the possible distances
    from the start point to each of the other airports and then finds the shortest route. It checks that this distance
    is within the limit. If it is not within the limits, it returns the string 'too' and number 4, which indicate
    that the route is not feasible. Otherwise, it multiplies the distance by the currency of the starting point
    and returns the preferred destination and the distance.
    """
    distances = getDistances(start, destinations)
    destination, distance = getShortest(distances)
    if checkDistance(limit,distance)==True:
        destination,distance = 'too', 4
        return destination, distance
    exchangeRate = float(currencyExchange(start))
    distance *= exchangeRate
    return destination, distance
    
def getDistances(startpoint,array):
    """
    This method reads in a starting point and a set. It creates a dictionary containing each airport in the set
    as a key and the distance between that airport and the starting point as the corresponding value. It then
    returns the dictionary
    """
    routes = {}
    for i in array:
        #print(airports.distanceBetweenAirports(startpoint, i))
        routes[i] = airports.distanceBetweenAirports(startpoint, i)
    return routes
    
def getShortest(route): #Selection sort?
    """
    This method reads in a dictionary and iterates through it to find the key and value pair with the lowest value
    in the dictionary. It assigns the key to the variable 'shortkey' and the value to the 'shortest' variable and
    then returns both variables. (Note: both variables are assigned at the start to values which will be replaced)
    """
    shortest = 1000000
    shortkey = ''
    for key,value in route.items():
        if value < shortest:
            shortest = value
            shortkey = key
    return shortkey, shortest

def currencyExchange(airport):
    """
    This method reads in an airport code as a variable and then creates an airport object using the airportAtlas 'getAirport'
    method. Then it uses the 'getCurrency' method of the currencyCreator to get the currency of the country that airport is in.
    Then it uses the currency 'getToEuro' method to get the exchange rate to Euro and returns it.
    """
    airport = airports.getAirport(airport)
    currency = currencies.getCurrency(airport.country)
    return currency.getToEuro()
     

def checkDistance(maxRange, flightDistance):
    """
    This method reads in the max range of the aircraft and the distance of the journey leg and checks that the aircraft can
    travel that distance. It returns a boolean result, based on the result of this comparison.
    """
    if flightDistance > maxRange:
        return True
    else:
        return False

if __name__ == '__main__':
    columns = list(['Start', 'Dest1','Dest2','Dest3','Dest4','End','Cost','Aircraft']) #Set column headings for the csv file
    with open('../input/bestroute.csv',"w", encoding = "utf8") as f:
        writer = csv.writer(f, delimiter=',', quotechar=" ", quoting=csv.QUOTE_ALL)
        writer.writerow(columns) #write the column headings to the csv file
    #Combine the two currency csv files into one so that currency objects can be created
    currency = pd.read_csv("../input/countrycurrency.csv",keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
    rate = pd.read_csv("../input/currencyrates.csv",header=None, keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
    rate.columns = ['name', 'currency_alphabetic_code', 'toEuro', 'fromEuro']
    currency = pd.merge(currency, rate, on='currency_alphabetic_code')
    currency = currency.drop(['name_fr', 'ISO3166-1-Alpha-2', 'ISO3166-1-Alpha-3', 'currency_minor_unit','currency_country_name','currency_name','name_y','currency_numeric_code','is_independent', 'ISO3166-1-numeric','ITU', 'MARC', 'WMO', 'DS', 'Dial', 'FIFA', 'FIPS', 'GAUL'], axis=1)
    currency.to_csv('../input/currencies.csv', index=False)
    #Create a dictionary of airports, aircrafts and currencies
    aircrafts = aircraftAtlas('../input/aircraft.csv')
    airports = airportAtlas('../input/airport.csv')
    currencies = currencyCreator('../input/currencies.csv')
    main('../input/testroutes.csv')