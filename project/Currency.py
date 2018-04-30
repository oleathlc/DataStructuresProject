import csv
import pandas as pd

currency = pd.read_csv("../input/countrycurrency.csv",keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
rate = pd.read_csv("../input/currencyrates.csv",header=None, keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
rate.columns = ['name', 'currency_alphabetic_code', 'toEuro', 'fromEuro']
currency = pd.merge(currency, rate, on='currency_alphabetic_code')
currency = currency.drop(['name_fr', 'ISO3166-1-Alpha-2', 'ISO3166-1-Alpha-3', 'currency_minor_unit','currency_country_name','currency_name','name_y','currency_numeric_code','is_independent', 'ISO3166-1-numeric','ITU', 'MARC', 'WMO', 'DS', 'Dial', 'FIFA', 'FIPS', 'GAUL'], axis=1)
currency.to_csv('../input/currencies.csv', index=False)

class Currency(object):
    def __init__(self, country, IOC, code, toEuro, fromEuro):
        self.name = country
        self.IOC = IOC
        self.code = code
        self.toEuro = toEuro
        self.fromEuro = fromEuro
        
    def getName(self):
        return self.name
    
    def getIOC(self):
        return self.IOC
    
    def getToEuro(self):
        return self.toEuro
    
    def getFromEuro(self):
        return self.fromEuro
    
    def getCode(self):
        return self.code
    
    def __str__(self):
        return self.name, self.IOC, self.code, self.toEuro, self.fromEuro

class currencyCreator(object):
    def loadData(self, csvFile):
        self.currencies = {}
        filename = csvFile
        with open(filename,"rt", encoding = "utf8") as f:
            reader = csv.reader(f)
            for line in reader:
                self.currencies[line[0]] = Currency(line[0], line[1], line[2], line[3], line[4])
        return self.currencies
    
    def __init__(self,csvFile):
        '''Constructor'''
        self.csvFile = csvFile
        self.loadData(csvFile)
    
    def getCurrency(self,name):
        Currency = self.currencies[name]
        return Currency 

    