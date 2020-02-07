'''
~~~3+1~~~
This file contains all relevant code for scraping data from Strava
'''
import sys
import bs4
import re
import urlutil
import csv

def go():
    '''
    Function that scrapes all 
    '''
    '''We will have to manually input a list of Strava URLs to scrape
    (I don't think there is a way around this).
    This should probably come from a JSON file that we upload to the repository.
    In that file we could store information something like this:
    {
        URL1: (2019, 'Chicago'),
        URL2: (2019, 'New York'),
        URL3: (2017, 'Chicago'),
        URL4: (2016, 'Boston')
    }
    where each key is a url, and each value is a tuple of (year, marathon city).
    For the time being, let's hard code the JSON file as a Python dictionary.'''
    marathon_homepages = {'https://www.strava.com/running_races/2782/results?page={}': ('2019-13-10', 'Chicago')}

    #Set up the CSV file with the header so we can append to it later
    with open("strava.csv", 'a') as csvfile:
        fieldnames = ["Name", "Gender", "Age", "Time1", "Time2", "Shoes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()

    '''Eventually, we will have a big dictionary of starting URLs, and we
    want to scrape the data for the marathon corresponding to each of them.
    Luckily Strava URLs are formatted super neatly, so we can just use 
    string formatting instead of searching the page for links.'''
    for url, (year, city) in marathon_homepages.items():
        page_num = 1
        last_page_num = sys.maxsize

        while page_num <= last_page_num:
            page_url = url.format(page_num)
            page = urlutil.get_request(page_url)
            page_html = urlutil.read_request(page)
            soup = bs4.BeautifulSoup(page_html, "lxml")

            '''On the first page we have an additional task:
            find the last page number that we need to scrape for this marathon.
            For example, Chicagp 2019 has 693 pages of information,
            so in this step we set last_page_num = 693.'''
            if page_num == 1:
                li = soup.find("li", class_="next_page")
                n = li.previous_sibling.previous_sibling.findChild().text
                last_page_num = int(n)

            #Now, scrape all the running data from this page.
            activities = soup.find("tbody").find_all("tr")
            for a in activities:
                attr_dict = {}
                attr_dict['Name'] = a.find("a", class_="minimal").text
                attr_dict['Gender'] = a.find("td", class_="athlete-gender").text.strip()
                attr_dict['Age'] = a.find("td", class_="athlete-age").text
                attr_dict['Time1'] = a.find("td", class_="finish-time").text
                activity_url = a.find("td", class_="athlete-activity").find(href=True)["href"]
                activity_url = urlutil.convert_if_relative_url(page_url, activity_url)
                print(attr_dict, activity_url)
                #Write all of this information to the output CSV file
                scrape_activity(activity_url, attr_dict)

            page_num += 1


def scrape_activity(activity_url, attr_dict):
    '''
    Scrapes a Strava activity page for running data
    
    Inputs:
        activity_url (string): URL of the Strava page to scrape
        attribute_dict (dict): other relevant data from the home page

    Returns:
        None, but appends to the strava.csv file
    '''
    activity = urlutil.get_request(activity_url)
    activity_html = urlutil.read_request(activity)
    soup = bs4.BeautifulSoup(activity_html, "lxml")

    #Get running time from activity page
    stats = soup.find("ul", class_="inline-stats section")
    time2 = stats.find("strong").text
    attr_dict['Time2'] = time2

    #Get shoes from activity page
    shoes = soup.find("span", class_="gear-name").text
    attr_dict['Shoes'] = shoes

    with open("strava.csv", 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
        writer.writerow(attr_dict)
        
go()