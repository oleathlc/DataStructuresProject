from Airports import Airport, airportAtlas
from Aircraft import Aircraft, aircraftAtlas
from Currency import Currency, currencyCreator
import csv
import pandas as pd
import queue
from itertools import permutations

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
    aircraft = aircrafts.getAircraft(craft) #Get the aircraft from the dictionary so the fuel capacity (i.e. range) can be calculated
    flightRange = float(aircraft.getFuel())
    if aircraft.getUnits() == 'imperial': #Convert to km if in miles
        flightRange *= 1.60934
    flightPlan = queue.Queue(maxsize=6) #Queue to store all the airports in order for the chosen itinerary
    flightPlan.put(start)
    destinations = set([A,B,C,D]) #Set containing intermediary airports (unordered)
    plans = getRoutes(destinations) #Get every possible itinerary
    routes = {} #Dictionary to hold all itineraries and their total cost
    for i in range(len(plans)): #Loop through each itinerary to get the cost
        cost = getDistances(start, plans[i], start, flightRange)
        routes[plans[i]] = cost #Append the itinerary as key and cost as value to the routes dictionary
    bestRoute, cost = getShortest(routes) #Get the cheapest itinerary in the routes dictionary
    if bestRoute == '' and cost == 1000000: #Code for when there is no feasible route
        saveToCSV(proposed)
        return "Cannot complete this itinerary with proposed aircraft"
    for i in bestRoute: #Append the airports to the flight plan queue in correct order
        flightPlan.put(i)
    flightPlan.put(start)
    plan = list([]) #List to contain the itinerary to send back to main function
    while not flightPlan.empty(): #Dequeue into the plan list until queue is empty
        plan.append(flightPlan.get())
    plan.append(cost)
    plan.append(craft)
    saveToCSV(plan)
    return plan

def getRoutes(destinations):
    """
    This method reads in a set of destinations, sets up an empty list, and then adds every possible permutation of the
    set into this list, with each permutation representing every possible itinerary route
    """
    routes = list([])
    for each in permutations(destinations):
        routes.append(each)
    return routes

def saveToCSV(route):
    """
    This method takes in two arguments, an array and another variable (the cost). It appends the cost to
    the array and then appends the array to a csv file and returns the array
    """
    with open('../input/bestroute.csv',"a", encoding = "utf8") as f:
        writer = csv.writer(f, delimiter=',', quotechar="-", quoting=csv.QUOTE_ALL)
        writer.writerow(route)
    
def getDistances(startpoint, array, endpoint, limit):
    """
    This method reads in a starting point, an itinerary, end point and limit. It iterates through the itinerary to
    get the distance of each leg of the journey, and then find the distance to the end airport. For each distance
    calculated it checks if it is within the aircrafts range, and returns 'not feasible' if that is the case. Otherwise
    it multiplies the cost of each leg by the currency of the start point of that leg and adds it to the total cost. It
    then returns the total cost of that itinerary
    """
    cost = 0 # Cost inititated as at zero
    for i in array:
        distance = airports.distanceBetweenAirports(startpoint, i)
        if checkDistance(limit,distance)==True:
            cost = "Not feasible"
            return cost
        cost += distance * float(currencyExchange(startpoint))
        startpoint = i
    distance = airports.distanceBetweenAirports(startpoint, endpoint)
    if checkDistance(limit,distance)==True:
            cost = "Not feasible"
            return cost
    cost += distance * float(currencyExchange(startpoint))
    return cost
    
def getShortest(route): 
    """
    This method reads in a dictionary and iterates through it to find the key-value pair with the lowest value in 
    the dictionary. By default the shortest variable is set to 1,000,000 as all possible itinerary legs will be
    less than this. If the value of a key (an itinerary) is a string (i.e. not feasible - from the above 
    function) then it skips to the next key-value pair. It iterates through all key-value pairs, replacing the
    shortkey and shortest variables each time an itinerary is found with a lesser cost/distance. When complete
    it returns the key-value pair of the cheapest itinerary. If all possibilities were not feasible, the default
    values will be returned.
    """
    #print(route)
    shortest = 1000000
    shortkey = ''
    for key,value in route.items():
        if type(value) == str:
            continue 
        elif value < shortest:
            shortest = value
            shortkey = key
    #print(shortkey)        
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
    This method reads in the max range of the aircraft and the distance of the journey leg and check that the aircraft can
    travel that distance. It returns a boolean result, based on the result of this comparison.
    """
    if flightDistance > maxRange:
        #print("Range:", maxRange, "Distance:", flightDistance)
        return True
    else:
        return False

if __name__ == '__main__':
    columns = list(['Start', 'Dest1','Dest2','Dest3','Dest4','End','Cost','Aircraft']) #Set column headings for the csv file
    with open('../input/bestroute.csv',"w", encoding = "utf8") as f:
        writer = csv.writer(f, delimiter=',', quotechar="-", quoting=csv.QUOTE_ALL)
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