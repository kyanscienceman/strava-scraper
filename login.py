# Python code to log into Strava

import requests
from lxml import html
import sys
import bs4
import re
import urlutil
import csv

# session_requests = requests.session()

#email input
#<input type="email" name="email" id="email" value="" placeholder="Your Email" autofocus="autofocus" class="form-control">

#password input
#<input type="password" name="password" id="password" value="" placeholder="Password" class="form-control">

#csrf token
#<meta name="csrf-token" content="l3ge0TbJM9KhInAvxl0iCOI4uOLmzM+1ZiZs5j9y6OQvzuHtFX322osc4ipggMdHuoCuEEC4dpA6dHGcdNz83Q==">
login_url = "https://www.strava.com/login"

login_page = urlutil.get_request(login_url)
login = urlutil.read_request(login_page)
soup = bs4.BeautifulSoup(login, 'html.parser')
utf8 = soup.find_all('input',
                     {'name': 'utf8'})[0].get('value').encode('utf-8')
token = soup.find_all('input',
                      {'name': 'authenticity_token'})[0].get('value')

payload = {
    'utf8': utf8,
    'authenticity_token': token,
    'plan': "",
    'email': "stravascraper123@gmail.com",
    'password': "2hourmarathon",
}

REQUEST_URL = "https://www.strava.com/login/session"
POST_LOGIN_URL = "https://www.strava.com/"
with requests.Session() as session:
    post = session.post(POST_LOGIN_URL, data=payload)
    r = session.get(REQUEST_URL)
    print(r.text)
# activity = urlutil.get_request(POST_LOGIN_URL)
# activity_html = urlutil.read_request(activity)
# soup = bs4.BeautifulSoup(activity_html, "lxml")
# print(soup)




