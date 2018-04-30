from Airports import *
from Aircraft import *
from Currency import *
from DFS import getRoutes
from BFS import getShortest, checkDistance
import pytest
import csv
import pandas as pd
import queue


def testMakeAirportDict():
    airports = airportAtlas('../input/airport.csv')
    assert airports.airports != None

def testGreatCircledist():
    airports = airportAtlas('../input/airport.csv')
    assert airports.distanceBetweenAirports('DUB', 'LHR') > 445 and airports.distanceBetweenAirports('LHR', 'DUB') <450

def testGetAirport():
    airports = airportAtlas('../input/airport.csv')
    dublin = airports.getAirport('DUB')
    assert dublin.cityName == 'Dublin'
    
def testMakeCurrencyDict():
    currencies = currencyCreator('../input/currencies.csv')
    assert currencies.currencies != None
    
def testGetCurrency():
    currencies = currencyCreator('../input/currencies.csv')
    pounds = currencies.getCurrency('United Kingdom')
    assert pounds.getCode() == 'GBP'
    
def testMakeAircraftDict():
    aircrafts = aircraftAtlas('../input/aircraft.csv')
    assert aircrafts.aircrafts != None
    
def testGetUnits():
    aircrafts = aircraftAtlas('../input/aircraft.csv')
    A319 = aircrafts.getAircraft('A319')
    assert float(A319.getFuel()) == 3750
    
def testGetShortest():
    testDict = {"LHR":500, "SYD":1000}
    airport,distance = getShortest(testDict)
    assert airport == "LHR" and distance == 500

def testCheckDistance():
    assert checkDistance(500,600) == True

def testGetRoutes():
    routes = ['A', 'B']
    assert getRoutes(routes) == [('A', 'B'), ('B', 'A')]
    

if __name__ == '__main__':
    currency = pd.read_csv("../input/countrycurrency.csv",keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
    rate = pd.read_csv("../input/currencyrates.csv",header=None, keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
    rate.columns = ['name', 'currency_alphabetic_code', 'toEuro', 'fromEuro']
    currency = pd.merge(currency, rate, on='currency_alphabetic_code')
    currency = currency.drop(['name_fr', 'ISO3166-1-Alpha-2', 'ISO3166-1-Alpha-3', 'currency_minor_unit','currency_country_name','currency_name','name_y','currency_numeric_code','is_independent', 'ISO3166-1-numeric','ITU', 'MARC', 'WMO', 'DS', 'Dial', 'FIFA', 'FIPS', 'GAUL'], axis=1)
    currency.to_csv('../input/currencies.csv', index=False)
    aircrafts = aircraftAtlas('../input/aircraft.csv')
    airports = airportAtlas('../input/airport.csv')
    currencies = currencyCreator('../input/currencies.csv')