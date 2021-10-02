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

def getJSON(holidayL):
    return

def getHolidays(holidayL):
    #loop that gets the years of 2020-2024 data. The weather data only needs to work for the current year
    for i in range(0,5):
        html = getHTML("https://www.timeanddate.com/holidays/us/202" + str(i))

        holidayParse = BeautifulSoup(html,'html.parser')

        table = holidayParse.find('table',attrs = {'id':'holidays-table'})

        for row in table.find_all_next('tr')[1:]:
            if (row.find_next('th') is not None) and (row.find_next('a') is not None):
                #print(row.find_next('th').get_text() + " 202" + str(i))
                holidayL.append(Holiday(row.find_next('a').get_text(), datetime.strptime(row.find_next('th').get_text() + " 202" + str(i), "%b %d %Y").strftime('%Y-%m-%d')))
                print(row.find_next('a').get_text())
            else:
                break
    return holidayL

#main function body.
def main():
    #variable declarations
    holidayList = []
    #import external json file and load it into the list

    #scrape the web data for the data from 2020-2024
    holidayList = getHolidays(holidayList)

    startupMenu = """Holiday Management\n================\nThere are currently """
    mainMenu = """Main Menu\n============\n1. Add a Holiday\n2. Remove a Holiday
3. Save Holiday List\n4. View Holidays\n5. Exit"""
    print(startupMenu + str(len(holidayList)) + " holidays\nin the system.\n\n")
    print(mainMenu)


    
    
    
    
    print(holidayList[4])
    print(len(holidayList))
    #This function returns a date from year, weekNum, day of week.
    print (datetime.fromisocalendar(2011, 22, 7))


main()