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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.strava.com"
MARATHON_PAGES = {'https://www.strava.com/running_races/2782/results?page={}': ('2019-13-10', 'Chicago')}
LOGIN_URL = BASE_URL + "/login"
LOGIN_EMAIL = "stravascraper123@mail.com"
LOGIN_PASSWORD = "2hourmarathon"

def strava_scrape(filename):
    '''
    Function that scrapes all marathons in MARATHON_PAGES
    and writes the information to a CSV file

    Inputs:
        filename (string): name of file

    Returns: None, but writes a new CSV file
    '''
    #Prepare 
    with open(filename, 'w') as csvfile:
        fieldnames = ["Name", "Gender", "Age", "Time1", "Time2", "Shoes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()

    #Log into Strava using our dummy account
    driver = webdriver.Firefox()
    driver.get(LOGIN_URL)
    elem = driver.find_element_by_id("email")
    elem.send_keys(LOGIN_EMAIL)
    elem = driver.find_element_by_id("password")
    elem.send_keys(LOGIN_PASSWORD)
    elem.submit()
    time.sleep(1) #To make sure server catches up 
    
    #Using this driver, start scraping the relevant data
    for page in MARATHON_PAGES:
        page_num = 1
        last_page_num = sys.maxsize

        #Navigate to the first page of the marathon results
        driver.get(page.format(page_num))
        # try: #Add this wait to ensure page loads before we continue
        #     element = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "results-table"))
        #     )
        # finally:
        #     driver.quit()
        soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

        while page_num <= last_page_num:
            #If this is the first page, find what the last page number is
            if page_num == 1:
                li = soup.find("li", class_="next_page")
                n = li.previous_sibling.previous_sibling.findChild().text
                last_page_num = int(n)

            #Iterate through all marathon results on this page
            activities = soup.find("tbody").find_all("tr")
            attr_dict = {}
            for a in activities:
                #Find the url of the activities page for this athlete's run 
                a_url = a.find("td", class_="athlete-activity").find(href=True)["href"]
                a_url = urlutil.convert_if_relative_url(BASE_URL, a_url)

                #Navigate to the activities page and check for shoe information
                driver.get(a_url)
                elem = driver.find_element_by_class_name("activity-stats")
                stats = bs4.BeautifulSoup(elem.get_attribute("innerHTML"), 'lxml')
                shoes = stats.find("span", class_="gear-name")

                #If so, then get all the information for this athelete's run
                if shoes is not None:
                    #Information on the running_races page
                    attr_dict['Name'] = a.find("a", class_="minimal").text
                    attr_dict['Gender'] = a.find("td", class_="athlete-gender").text.strip()
                    attr_dict['Age'] = a.find("td", class_="athlete-age").text
                    attr_dict['Time1'] = a.find("td", class_="finish-time").text

                    #Information on the activities page
                    attr_dict['Shoes'] = shoes.text.strip()
                    attr_dict['Time2'] = stats.find_all("li")[1].find("strong").text

                    #Write this information to the specified CSV file
                    with open(filename, 'a') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
                        writer.writerow(attr_dict)

            #Move to the next page of marathon results
            page_num += 1
            break

    #When we are done with all the marathons, close the selenium driver
    driver.close()

strava_scrape("strava.csv")

# def go():
#     '''
#     Function that scrapes all 
#     '''
#     '''We will have to manually input a list of Strava URLs to scrape
#     (I don't think there is a way around this).
#     This should probably come from a JSON file that we upload to the repository.
#     In that file we could store information something like this:
#     {
#         URL1: (2019, 'Chicago'),
#         URL2: (2019, 'New York'),
#         URL3: (2017, 'Chicago'),
#         URL4: (2016, 'Boston')
#     }
#     where each key is a url, and each value is a tuple of (year, marathon city).
#     For the time being, let's hard code the JSON file as a Python dictionary.'''
#     marathon_homepages = {'https://www.strava.com/running_races/2782/results?page={}': ('2019-13-10', 'Chicago')}

#     #Set up the CSV file with the header so we can append to it later
#     with open("strava.csv") as csvfile:
#         fieldnames = ["Name", "Gender", "Age", "Time1", "Time2", "Shoes"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
#         writer.writeheader()

#     '''Eventually, we will have a big dictionary of starting URLs, and we
#     want to scrape the data for the marathon corresponding to each of them.
#     Luckily Strava URLs are formatted super neatly, so we can just use 
#     string formatting instead of searching the page for links.'''
#     for url, (year, city) in marathon_homepages.items():
#         page_num = 1
#         last_page_num = sys.maxsize

#         while page_num <= last_page_num:
#             page_url = url.format(page_num)
#             page = urlutil.get_request(page_url)
#             page_html = urlutil.read_request(page)
#             soup = bs4.BeautifulSoup(page_html, "lxml")

#             '''On the first page we have an additional task:
#             find the last page number that we need to scrape for this marathon.
#             For example, Chicagp 2019 has 693 pages of information,
#             so in this step we set last_page_num = 693.'''
#             if page_num == 1:
#                 li = soup.find("li", class_="next_page")
#                 n = li.previous_sibling.previous_sibling.findChild().text
#                 last_page_num = int(n)

#             #Now, scrape all the running data from this page.
#             activities = soup.find("tbody").find_all("tr")
#             for a in activities:
#                 attr_dict = {}
#                 attr_dict['Name'] = a.find("a", class_="minimal").text
#                 attr_dict['Gender'] = a.find("td", class_="athlete-gender").text.strip()
#                 attr_dict['Age'] = a.find("td", class_="athlete-age").text
#                 attr_dict['Time1'] = a.find("td", class_="finish-time").text
#                 activity_url = a.find("td", class_="athlete-activity").find(href=True)["href"]
#                 activity_url = urlutil.convert_if_relative_url(page_url, activity_url)
#                 print(attr_dict, activity_url)
#                 #Write all of this information to the output CSV file
#                 scrape_activity(activity_url, attr_dict)

#             page_num += 1


# def scrape_activity(activity_url, attr_dict):
#     '''
#     Scrapes a Strava activity page for running data
    
#     Inputs:
#         activity_url (string): URL of the Strava page to scrape
#         attribute_dict (dict): other relevant data from the home page

#     Returns:
#         None, but appends to the strava.csv file
#     '''
#     activity = urlutil.get_request(activity_url)
#     activity_html = urlutil.read_request(activity)
#     soup = bs4.BeautifulSoup(activity_html, "lxml")

#     #Get running time from activity page
#     stats = soup.find("ul", class_="inline-stats section")
#     time2 = stats.find("strong").text
#     attr_dict['Time2'] = time2

#     #Get shoes from activity page
#     shoes = soup.find("span", class_="gear-name").text
#     attr_dict['Shoes'] = shoes

#     with open("strava.csv", 'a') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
#         writer.writerow(attr_dict)
        
# go()