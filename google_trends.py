#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import datetime
import requests
from bs4 import BeautifulSoup

__author__ = 'HK Dambanemuya'
__version__ = 'Python2'

'''
    Google Trends:
        Code to collect Top 20 Google Daily Search Trends
'''

class Google():
    def __init__(self):
        self.trends = list() 
        # Get Top 20 Google Daily Search Trends as HTML request
        self.google_trends = requests.get("https://trends.google.com/trends/hottrends/atom/feed")
        # Parse HTML response using BeautifulSoup
        self.soup = BeautifulSoup(self.google_trends.content,'html.parser')

    # Method to pre-process BeautifulSoup object
    def get_daily_trends(self):
        for item in self.soup.find_all('item'):
            self.trends.append(item.title.text.strip().encode('utf-8'))

    # Method to save pre-processes search trends
    def save_daily_trends(self):
        with open(str('Data/Trends/trends_' + datetime.datetime.now().strftime('%m_%d_%y') + '.csv'), 'wb') as f:
            wr = csv.writer(f, delimiter="\n")
            wr.writerow(self.trends)

def main():
    g = Google()
    g.get_daily_trends()
    g.save_daily_trends()

if __name__ in "__main__":
    main()
 