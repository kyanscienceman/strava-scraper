'''
~~~3+1~~~
This file contains all relevant code for scraping data from Strava
'''
import queue
import urlutil

'''
We will have to manually input a list of Strava URLs to scrape
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
For the time being, let's hard code the JSON file as a Python dictionary.
'''
marathon_homepages = {'https://www.strava.com/running_races/2782/results?page={}': ('2019-13-10', 'Chicago')}
limiting_domain = "strava.com"


#Eventually, we will have a big dictionary of starting URLs, and we want
#to scrape the data for the marathon corresponding to each of them.

for url, (year, city) in marathon_homepages.items():
    page_num = 1
    next_page = url.format(page_num)
    

