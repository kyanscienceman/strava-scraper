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
#from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://www.strava.com"
MARATHON_IDS = {
    'CH14': ('2014-12-10', 'Chicago'),
    'CH15': ('2015-11-10', 'Chicago'),
    'CH16': ('2016-09-10', 'Chicago'),
    'CH17': ('2017-08-10', 'Chicago'),
    'CH18': ('2018-07-10', 'Chicago'),
    'CH19': ('2019-13-10', 'Chicago')
}
MARATHON_PAGES = {
    'CH14': 'https://www.strava.com/running_races/2014-chicago-marathon/results?page={}',
    'CH15': 'https://www.strava.com/running_races/2015-chicago-marathon/results?page={}',
    'CH16': 'https://www.strava.com/running_races/2016-chicago-marathon/results?page={}',
    'CH17': 'https://www.strava.com/running_races/2017-chicago-marathon/results?page={}',
    'CH18': 'https://www.strava.com/running_races/2153/results?page={}',
    'CH19': 'https://www.strava.com/running_races/2782/results?page={}'
}
LOGIN_URL = BASE_URL + "/login"
#LOGIN_EMAIL = "stravascraper123@mail.com"
LOGIN_PASSWORD = "2hourmarathon"
L_STR = 'uchistrava{}@gmail.com'
LOGIN_EMAILS = [L_STR.format('+'+str(i)) for i in range(1, 21)]
FIELDNAMES = ["RaceID", "Name", "Gender", "Age", "Time1", "Time2", "Shoes"]
with open('CSIL_IPS.csv', newline='') as f:
    reader = csv.reader(f)
    CSIL_IPS = [r[0] for r in reader]

CHROME_PATH = '/usr/bin/google-chrome'
# CHROMEDRIVER_PATH = '~/three-plus-one/chromedriver'
WINDOW_SIZE = "1920,1080"
CHROME_OPTIONS = Options()  
CHROME_OPTIONS.add_argument("--headless")  
CHROME_OPTIONS.add_argument("--window-size=%s" % WINDOW_SIZE)
CHROME_OPTIONS.binary_location = CHROME_PATH


def get_proxies():
    '''
    Gets a list of proxy IP addresses to use,
    filtering for those based in the US

    Returns: cycle object containing all proxies found
    '''
    req_proxy = RequestProxy() 
    proxies = req_proxy.get_proxy_list()
    US_proxies = []
    for p in proxies:
        if p.country == 'United States':
            US_proxies.append(p)
    proxy_pool = cycle(US_proxies)
    return proxy_pool


def setup_driver(proxy_pool):
    '''
    Opens a Selenium webdriver object using a new proxy IP address

    Inputs:
        proxy_pool: cycle object containing IP addresses

    Returns: webdriver object with the https://www.strava.com/login page open
    '''
    working_proxy = False
    while not working_proxy:
        proxy = next(proxy_pool)
        PROXY = proxy.get_address()
        webdriver.DesiredCapabilities.FIREFOX['proxy']={
            "httpProxy":PROXY,
            "ftpProxy":PROXY,
            "sslProxy":PROXY,
            "proxyType":"MANUAL",
        }
        driver = webdriver.Chrome(options=CHROME_OPTIONS)  
        try:
            driver.get(LOGIN_URL)
            working_proxy = True
        except:
            continue
    return driver


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
        
    #Get a list of proxy IP addresses to use
    #proxy_pool = cycle(CSIL_IPS)
    email_pool = cycle(LOGIN_EMAILS)

    
    page_num = start_page_num
    last_page_num = sys.maxsize

    counter = 1

    while page_num <= last_page_num:
        #Setup driver with a new proxy IP address
        # working_proxy = False
        # while not working_proxy:
        #     proxy = next(proxy_pool)
        #     webdriver.DesiredCapabilities.FIREFOX['proxy']={
        #         "httpProxy":proxy,
        #         "ftpProxy":proxy,
        #         "sslProxy":proxy,
        #         "proxyType":"MANUAL",
        #     }
        #     driver = webdriver.Firefox()
        #     try:
        #         driver.get(LOGIN_URL)
        #         working_proxy = True
        #     except:
        #         time.sleep(4)
        #         driver.close()
        #         continue

        #Log in to Strava with this driver
        try: driver
        except NameError: driver = None 
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

        #If this is the first page, find what the last page number is
        if page_num == 1:
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
            #Find the url of the activities page for this athlete's run 
            a_url = a.find("td", class_="athlete-activity").find(href=True)["href"]
            a_url = urlutil.convert_if_relative_url(BASE_URL, a_url)

            print(marathon_page, "activity", counter)
            counter += 1

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

        #Write this information to the specified CSV file
        if page_num % 10 == 0:
            with open(filename, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES, delimiter='|')
                writer.writerows(activity_list)

            #In order to avoid "Too Many Requests", try adding a delay 
            #time.sleep(5)

        #Move to the next page of marathon results
        if page_num % 3 == 0:
            driver.close()
        page_num += 1
            

    #When we are done with all the marathons, close the selenium driver
    driver.close()

# strava_scrape("race_result/strava_chicago.csv")
# got to activity 1904. Start from page number 90


if __name__=="__main__":
    filename = sys.argv[1]
    race_id = sys.argv[2]
    start_page_num = int(sys.argv[3])
    strava_scrape(filename, race_id, start_page_num)
