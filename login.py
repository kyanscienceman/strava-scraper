# import bs4
# import requests

# VERSION = '0.1.0'

# # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
# USER_AGENT = "stravalib-scraper/%s" % VERSION
# HEADERS = {'User-Agent': USER_AGENT}

# BASE_URL = "https://www.strava.com"
# URL_LOGIN = "%s/login" % BASE_URL
# URL_SESSION = "%s/session" % BASE_URL
# URL_DASHBOARD = "%s/dashboard" % BASE_URL

# EMAIL = "stravascraper123@gmail.com"
# PASSWORD = "2hourmarathon"
# SESSION = requests.Session()

# is_authed = False
# dashboard_content = None

# def get_page(url):
#         response = SESSION.get(url, headers=HEADERS)
#         response.raise_for_status()
#         return response

# def login():
#     response = get_page(URL_LOGIN)
#     soup = bs4.BeautifulSoup(response.content, 'html.parser')
#     utf8 = soup.find_all('input',{'name': 'utf8'})[0].get('value').encode('utf-8')
#     token = soup.find_all('input',{'name': 'authenticity_token'})[0].get('value')
#     data = {'utf8': utf8,
#             'authenticity_token': token,
#             'plan': "",
#             'email': EMAIL,
#             'password': PASSWORD}
#     response = SESSION.post(URL_SESSION, data=data, headers=HEADERS)
#     response.raise_for_status()

#     # Simulate that redirect here:
#     response = get_page(URL_DASHBOARD)
#     #assert("<h2>Activity Feed</h2>" in response.content)
#     is_authed = True
#     dashboard_content = response.content
#     print(dashboard_content)

# login()

import requests
import bs4

get_url = "https://www.strava.com/login"
post_url = "https://www.strava.com"
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
}
login_data = {
    'name': "stravascraper123@mail.com",
    'pass': "2hourmarathon",
    'utf8': "",
    'token': "",
    'plan': ""
}

with requests.Session() as s:
    r = s.get(get_url, headers=headers)
    soup = bs4.BeautifulSoup(r.content, 'lxml')

    utf8 = soup.find("input", attrs={'name': "utf8"}).get('value').encode('utf-8')
    login_data['utf8'] = utf8

    token = soup.find("input", attrs={'name': "authenticity_token"}).get('value')
    login_data['token'] = token

    plan = soup.find("input", attrs={'name': "plan"}).get('value')
    login_data['plan'] = plan

    r = s.post(post_url, headers=headers, data=login_data)
    print(r.content)
