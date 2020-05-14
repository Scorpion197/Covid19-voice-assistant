#! /usr/bin/python3.6
# -*-coding:utf-8 -* 

import requests
from bs4 import BeautifulSoup
import re 
import pickle
import assistant

URL = 'https://www.worldometers.info/coronavirus/'

class Data:
    """
    A class in which we define methodes to scrape and process the scrapped data 
    """
    def __init__(self, URL):
        self.url = URL 
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.deaths_per_country = {} 
        self.cases_per_country = {} 

    def getData(self):
        return self.soup

    def extract(self):
        """A function to extract the data from the table in the website we used to scrape informations """

        table = self.soup.table
        table_rows = table.find_all('tr')

        for tr in table_rows:
            td = tr.find_all('td')
            data = [item.text for item in td]

            #Extracting each row and save it in a file as an object
            try:
            
                with open('data.txt', 'wb') as file:
                    my_pickler = pickle.Pickler(file)
                    my_pickler.dump(data)

            except Exception as exc:
                print('Error while saving data :', exc)

            #saving data in our dictionaries
            try: 
            
                with open('data.txt', 'rb') as file:
                    my_dipeck = pickle.Unpickler(file)
                    my_data = my_dipeck.load()
                    self.deaths_per_country[my_data[0]] = my_data[3]
                    self.cases_per_country[my_data[0]] = my_data[1]

            except Exception as exc2:
                print('Error while loading data :', exc2)
    
    def process(self):
        """ A function in which we will remove all the ',' and spaces in the values of our dictionnaries in order to convert them to 
            integers """
        
        for key, value in self.deaths_per_country.items():

            if ',' in value:
                new_value = value.replace(',', '')

            elif ' ' in value:
                new_value = value.replace(' ', '')


            if new_value != '':
                self.deaths_per_country[key] = int(new_value)
        
        for key, value in self.cases_per_country.items():

            if ',' in value:
                new_value = value.replace(',', '')

            elif ' ' in value:
                new_value = value.replace(' ', '')

            if new_value != '':       
                self.cases_per_country[key] = int(new_value)


    def getAllDeaths(self):
        """ A function to return the number of deaths in all countries """
        return self.deaths_per_country
    
    def getAllCases(self):
        """ A function to return the number of cases in all countries """
        return self.cases_per_country
    
    def getDeaths(self, country):
        """A function to return the number of deaths in the specified country """
        return self.deaths_per_country[country]
    
    def getCases(self, country):
        """A function to return the number of cases in the specified country """
        return self.cases_per_country[country]
    

data = Data(URL)
data.extract()
data.process()


while True:

    print('Listening....')
    text = assistant.getAudio()
    assistant.parseText(text, data.deaths_per_country, data.cases_per_country)


