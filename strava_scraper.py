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
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

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
    'https://www.strava.com/running_races/2014-chicago-marathon/results?page={}': 'CH14',
    'https://www.strava.com/running_races/2015-chicago-marathon/results?page={}': 'CH15',
    'https://www.strava.com/running_races/2016-chicago-marathon/results?page={}': 'CH16',
    'https://www.strava.com/running_races/2017-chicago-marathon/results?page={}': 'CH17',
    'https://www.strava.com/running_races/2153/results?page={}': 'CH18',
    'https://www.strava.com/running_races/2782/results?page={}': 'CH19'
}
LOGIN_URL = BASE_URL + "/login"
LOGIN_EMAIL = "stravascraper123@mail.com"
LOGIN_PASSWORD = "2hourmarathon"
FIELDNAMES = ["RaceID", "Name", "Gender", "Age", "Time1", "Time2", "Shoes"]

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
        driver = webdriver.Firefox()
        try:
            driver.get(LOGIN_URL)
            working_proxy = True
        except:
            continue
    return driver

def strava_scrape(filename):
    '''
    Function that scrapes all marathons in MARATHON_PAGES
    and writes the information to a CSV file

    Inputs:
        filename (string): name of file

    Returns: None, but writes a new CSV file
    '''
    #Prepare csv file for results
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES, delimiter='|')
        writer.writeheader()
        
    #Get a list of proxy IP addresses to use
    proxy_pool = get_proxies()

    for page in MARATHON_PAGES: 
        page_num = 1
        last_page_num = sys.maxsize

        while page_num <= last_page_num:
            #Setup driver with a new proxy IP address
            driver = setup_driver(proxy_pool)

            #Log in to Strava with this driver
            elem = driver.find_element_by_id("email")
            elem.send_keys(LOGIN_EMAIL)
            elem = driver.find_element_by_id("password")
            elem.send_keys(LOGIN_PASSWORD)
            elem.submit()
            time.sleep(5) #To make sure server catches up

            #Navigate to the marathon results page
            driver.get(page.format(page_num))
            soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

            #If this is the first page, find what the last page number is
            if page_num == 1:
                li = soup.find("li", class_="next_page")
                n = li.previous_sibling.previous_sibling.findChild().text
                last_page_num = int(n)

            #Iterate through all marathon results on this page
            activities = soup.find("tbody").find_all("tr")
            for a in activities:
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
                attr_dict['RaceID'] = MARATHON_PAGES[page]

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

                #Write this information to the specified CSV file
                with open(filename, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES, delimiter='|')
                    writer.writerow(attr_dict)

                #In order to avoid "Too Many Requests", try adding a delay 
                time.sleep(5)

            #Move to the next page of marathon results
            page_num += 1

    #When we are done with all the marathons, close the selenium driver
    driver.close()

strava_scrape("chicago_20142019.csv")