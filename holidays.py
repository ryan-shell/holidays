from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Holiday:
    name: str
    date : datetime
    
def getHTML(url):
    response = requests.get(url)
    return response.text


response = requests.get("https://www.timeanddate.com/holidays/us/")

html = getHTML("https://www.timeanddate.com/holidays/us/")

holidayParse = BeautifulSoup(html,'html.parser')

table = holidayParse.find('table',attrs = {'id':'holidays-table'})

holidayList = []

for row in table.find_all_next('tr'):
    if(row.find_next('th') is not None) and (row.find_next('a') is not None):
        holidayList.append(Holiday(row.find_next('th').get_text(), row.find_next('a').get_text()))
    else:
        break




print(holidayList[4].name)
print(len(holidayList))

#This function returns a date from year, weekNum, day of week.
print (datetime.fromisocalendar(2011, 22, 7))


