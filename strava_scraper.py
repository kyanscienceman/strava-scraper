'''
~~~3+1~~~
This file contains all relevant code for scraping data from Strava
'''
import sys
import bs4
import re
import urlutil
import csv
import time
from itertools import cycle 
from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.strava.com"
MARATHON_IDS = {
    'CH14': ('2014-10-12', 'Chicago'),
    'CH15': ('2015-10-11', 'Chicago'),
    'CH16': ('2016-10-09', 'Chicago'),
    'CH17': ('2017-10-08', 'Chicago'),
    'CH18': ('2018-10-07', 'Chicago'),
    'CH19': ('2019-10-13', 'Chicago'), 
    'NY14': ("2019-11-02", "New York"),
    "NY15": ("2015-11-01", "New York"),
    "NY16": ("2016-11-06", "New York"),
    'NY17': ("2017-11-05", "New York"),
    "NY18": ("2018-11-04", "New York"),
    "NY19": ("2019-11-03", "New York")
}
MARATHON_PAGES = {
    'CH14': 'https://www.strava.com/running_races/2014-chicago-marathon/results?page={}',
    'CH15': 'https://www.strava.com/running_races/2015-chicago-marathon/results?page={}',
    'CH16': 'https://www.strava.com/running_races/2016-chicago-marathon/results?page={}',
    'CH17': 'https://www.strava.com/running_races/2017-chicago-marathon/results?page={}',
    'CH18': 'https://www.strava.com/running_races/2153/results?page={}',
    'CH19': 'https://www.strava.com/running_races/2782/results?page={}',
    'NY14': 'https://www.strava.com/running_races/32/results?page={}',
    'NY15': 'https://www.strava.com/running_races/302/results?page={}',
    'NY16': 'https://www.strava.com/running_races/659/results?page={}' ,
    'NY17': 'https://www.strava.com/running_races/878/results?page={}',
    'NY18': 'https://www.strava.com/running_races/2132/results?page={}',
    'NY19': 'https://www.strava.com/running_races/2904/results?page={}'
}
LOGIN_URL = BASE_URL + "/login"
#LOGIN_EMAIL = "stravascraper123@mail.com"
LOGIN_PASSWORD = "2hourmarathon"
L_STR = 'uchistrava{}@gmail.com'
LOGIN_EMAILS = [L_STR.format('+'+str(i)) for i in range(1, 31)]
FIELDNAMES = ["RaceID", "Name", "Gender", "Age", "Time1", "Time2", "Shoes"]


CHROME_PATH = '/usr/bin/google-chrome'
# CHROMEDRIVER_PATH = '~/three-plus-one/chromedriver'
WINDOW_SIZE = "1920,1080"
CHROME_OPTIONS = Options()  
CHROME_OPTIONS.add_argument("--headless")  
CHROME_OPTIONS.add_argument("--window-size=%s" % WINDOW_SIZE)
CHROME_OPTIONS.binary_location = CHROME_PATH


def strava_scrape(filename, race_id, start_page_num):
    '''
    Function that scrapes all marathons in MARATHON_PAGES
    and writes the information to a CSV file

    Inputs:
        filename (string): name of file
        marathon_page (string): url of race result page
        start_page_num (int): the page number in the result page that we start from

    Returns: None, but writes a new CSV file
    '''
    #Prepare csv file for results
    with open(filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES, delimiter='|')
        if start_page_num == 1:
            writer.writeheader()
        
    email_pool = cycle(LOGIN_EMAILS)

    page_num = start_page_num
    last_page_num = sys.maxsize
    counter = 1

    while page_num <= last_page_num:
        #Log in to Strava
        try: 
            driver
        except NameError:
            driver = None 
        if page_num % 3 == 1 or driver is None: 
            driver = webdriver.Chrome(options=CHROME_OPTIONS)
            driver.get(LOGIN_URL)
            elem = driver.find_element_by_id("email")
            elem.send_keys(next(email_pool))
            elem = driver.find_element_by_id("password")
            elem.send_keys(LOGIN_PASSWORD)
            elem.submit()
            time.sleep(1) #To make sure server catches up

        #Navigate to the marathon results page
        marathon_page = MARATHON_PAGES[race_id]
        driver.get(marathon_page.format(page_num))
        soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

        #If this is the first page we have scraped, find what the last page number is
        if page_num == start_page_num:
            li = soup.find("li", class_="next_page")
            n = li.previous_sibling.previous_sibling.findChild().text
            last_page_num = int(n)

        #Iterate through all marathon results on this page
        activities = soup.find("tbody").find_all("tr")
        try: activity_list
        except NameError: activity_list = []
        if page_num % 10 == 1: 
            activity_list = []

        for a in activities:
            print(race_id, "Page", page_num, "Activity", counter)
            counter += 1
            
            #Find the url of the activities page for this athlete's run 
            a_url = a.find("td", class_="athlete-activity").find(href=True)["href"]
            a_url = urlutil.convert_if_relative_url(BASE_URL, a_url)

            #Navigate to the activities page and check for privacy settings 
            driver.get(a_url)
            try:
                elem = driver.find_element_by_class_name("activity-stats")
            except:
                continue
            #Then check if they have shoe information
            stats = bs4.BeautifulSoup(elem.get_attribute("innerHTML"), 'lxml')
            shoes = stats.find("span", class_="gear-name")
            if shoes is None:
                continue

            #If the shoes are listed, then get all the information for this run
            attr_dict = {}
            attr_dict['RaceID'] = race_id

            #Information on the running_races page
            attr_dict['Name'] = a.find("a", class_="minimal").text
            attr_dict['Gender'] = a.find("td", class_="athlete-gender").text.strip()
            attr_dict['Age'] = a.find("td", class_="athlete-age").text
            attr_dict['Time1'] = a.find("td", class_="finish-time").text
            #Information on the activities page
            shoe_name = re.findall(r"(.+)\s\(", shoes.text.strip())
            if shoe_name:
                attr_dict['Shoes'] = shoe_name[0]
            else:
                attr_dict['Shoes'] = None
            attr_dict['Time2'] = stats.find_all("li")[1].find("strong").text

            activity_list.append(attr_dict)

        #Write this information to the specified CSV file, every 10 pages
        if page_num % 10 == 0 or page_num == last_page_num:
            with open(filename, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES, delimiter='|')
                writer.writerows(activity_list)

        #Switch to a different Strava account, every 3 pages
        if page_num % 3 == 0 or page_num == last_page_num:
            driver.close()

        #Move to the next page of marathon results
        page_num += 1


if __name__=="__main__":
    filename = sys.argv[1]
    race_id = sys.argv[2]
    start_page_num = int(sys.argv[3])
    scraper = sys.argv[4]
    if scraper == "Kevin":
        LOGIN_EMAILS = LOGIN_EMAILS[:7]
    elif scraper == "Peter":
        LOGIN_EMAILS = LOGIN_EMAILS[7:15]
    elif scraper == "Xingyu":
        LOGIN_EMAILS = LOGIN_EMAILS[15:23]
    else:
        LOGIN_EMAILS = LOGIN_EMAILS[24:]
    print(LOGIN_EMAILS)
    strava_scrape(filename, race_id, start_page_num)
