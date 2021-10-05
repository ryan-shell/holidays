from bs4 import BeautifulSoup
from bs4.element import TemplateString
import requests
from dataclasses import dataclass, field
from datetime import date, datetime
import json

@dataclass
class Holiday:
    name: str
    date : datetime

    def __str__(self):
        return (self.name + " - " + str(self.date))
    def __eq__(self, other):
        return (self.name == other.name)

    def getDate(self):
        return self.date
    
def readFile(holidayList):
    fin = open("holidays.json","r")
    jsonObj = json.load(fin)

    for i in jsonObj["holidays"]:
        holidayList.append(Holiday(i["name"], i["date"]))
        #print(i)
    fin.close()

    return holidayList

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
                #print(row.find_next('a').get_text())
            else:
                break
    return holidayL

def getWeek(year,weekNum):
    weekL = []
    for i in range(1,8):
        weekL.append(str(datetime.fromisocalendar(int(year), int(weekNum), i))[:10])
    return weekL

def getTemps():
    url = "https://api.tomorrow.io/v4/timelines"

    querystring = {
    "location":"33, -84",
    "fields":["temperature", "cloudCover"],
    "units":"imperial",
    "timesteps":"1d",
    "apikey":"xYyT5Ke7qRr3XOn9l7bBItUyprXFJxdq"}

    response = requests.request("GET", url, params=querystring)
    print(response.text)

    t = response.json()['data']['timelines'][0]['intervals'][0]['values']['temperature']
    print("Weather Forecast")
    print("================")

    results = response.json()['data']['timelines'][0]['intervals']

    
    temperatures = []

    for daily_result in results:
        date = daily_result['startTime'][0:10]
        temp = round(daily_result['values']['temperature'])
        temperatures.append({"date" : date, "temperature" : temp})
        print("On",date,"it will be", temp, "F")
    return temperatures

def saveHolidays(holidayList):
    fout = open("holidaysList.json","w")

    tempL = []

    for i in range(0,len(holidayList)):
        tempL.append({"name" : holidayList[i].name, "date" : holidayList[i].date})

    jsonObj = json.dumps(tempL)

    fout.write(jsonObj)

    fout.close()



#main function body.
def main():
    #variable declarations
    holidayList = []
    exitFlag = False
    #import external json file and load it into the list
    holidayList = readFile(holidayList)


    #scrape the web data for the data from 2020-2024
    holidayList = getHolidays(holidayList)

    startupMenu = """Holiday Management\n================\nThere are currently """
    mainMenu = """Main Menu\n============\n1. Add a Holiday\n2. Remove a Holiday
3. Save Holiday List\n4. View Holidays\n5. Exit"""
    print(startupMenu + str(len(holidayList)) + " holidays\nin the system.\n\n")
    
    #loop is needed here to loop through the menu until
    while exitFlag is False:
        userInput = input(mainMenu)



        #Add Holiday
        if(userInput == "1"):
            dFlag = False
            date = ""
            while dFlag == False:
                date = input("Please enter a date in the format yyyy-mm-dd:")
                if(len(date) != 10):
                    print("Please enter a proper date")
                else:
                    dFlag = True
            name = input("Please enter a name: ")
            holidayList.append(Holiday(name, date))
            break



        #Remove Holiday
        elif(userInput == "2"):
            removalList = []
            print("Remove Holiday Selected")
            nameRemoved = input("Please input the name you would like to remove")
            for i in range(0,len(holidayList)):
                if(holidayList[i].name == nameRemoved):
                    removalList.append(i)
            removalList.sort(reverse=True)
            if len(removalList) > 0:
                for i in range(0,len(removalList)):
                    holidayList.pop(removalList[i])


        #Save Holiday
        elif(userInput == "3"):
            #need to save list into a new json file.
            saveHolidays(holidayList)
            print("Save Holiday List Selected")


        #View Holidays
        elif(userInput == "4"):
            inputCorrect = True
            weekHolidayList = []
            print("View Holiday List Selected\n===============\n")
            year = input("Please Enter a Year: ")
            week = input("Please Enter the Week you would like to view 1-52 (leave blank for current week):")
            if(week == ""):
                week = datetime.today().isocalendar()[1]
            dateList = getWeek(year,week)
            print(dateList)
            weekHolidayList = list(filter(lambda x : x.getDate() in dateList, holidayList))
            for i in range(0,len(weekHolidayList)):
                print(weekHolidayList[i].name + " " + str(weekHolidayList[i].date))
            weatherStr = input("Would you like the weather for those days. This will only work within 15 days of todays date. y/n").lower()
            if(weatherStr == "y"):
                temperatureList = getTemps()
                for i in range(0,len(weekHolidayList)):
                    pFlag = False
                    pstring = ""
                    for j in range(0,len(temperatureList)):
                        if((str(temperatureList[j]["date"]) == str(weekHolidayList[i].date)) and pFlag == False):
                            pstring = weekHolidayList[i].name + " " + str(weekHolidayList[i].date) + " The Temperature is " + str(temperatureList[j]["temperature"]) + "F"
                            pFlag = True
                        elif pFlag == False:
                            pstring = weekHolidayList[i].name + " " + str(weekHolidayList[i].date)
                    print(pstring)

        #Exit
        elif(userInput == "5"):
            exitFlag = True
        else:
            print("Please enter a number from 1-5.\n")


main()

