# #Code is from https://github.com/loisaidasam/stravalib-scraper
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

import urlutil
import requests
import bs4

GET_URL = "https://www.strava.com/login"
POST_URL = "https://www.strava.com/session"

HEADERS = {
    'Host': "www.strava.com",
    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Language': "en-US,en;q=0.5",
    'Accept-Encoding': "gzip, deflate, br",
    'Referer': "https://www.strava.com/login",
    'Content-Type': "application/x-www-form-urlencoded",
    'Content-Length': "191",
    'Origin': "https://www.strava.com",
    'Connection': "keep-alive",
	'Cookie': 'ajs_anonymous_id=%226360426c-11a4-4df6-8203-2cfeac907d31%22; sp=9b0c7ee1-35b7-4de1-b435-4591d5a6df24; _ga=GA1.2.78499818.1581111281; _fbp=fb.1.1581111281182.1991822037; _strava_cookie_banner=true; _gid=GA1.2.1424905716.1581534482; _strava4_session=75crj4v84fn2ccefpiu6sdfkfpobr8es; _sp_ses.047d=*; _dc_gtm_UA-6309847-24=1; _sp_id.047d=c5b35e03-9a67-4a48-9eef-985744f06b81.1581538078.0.1581538081..7f396e00-a16d-446a-aec1-caeb8aefd3f1; ajs_user_id=null; ajs_group_id=null',
	'Upgrade-Insecure-Requests': "1",
    'TE': "Trailers"
}
LOGIN_DATA = {
    'name': "stravascraper123@mail.com",
    'pass': "2hourmarathon",
    'utf8': "",
    'token': "",
    'plan': ""
}

html = urlutil.read_request(urlutil.get_request(GET_URL))
soup = bs4.BeautifulSoup(html, 'lxml')
utf8 = soup.find("input", attrs={'name': "utf8"}).get('value').encode('utf-8')
LOGIN_DATA['utf8'] = utf8
token = soup.find("input", attrs={'name': "authenticity_token"}).get('value')
LOGIN_DATA['token'] = token
#plan = soup.find("input", attrs={'name': "plan"}).get('value')
#LOGIN_DATA['plan'] = plan

with requests.Session() as s:
    r = s.post(POST_URL, data=LOGIN_DATA, headers=HEADERS)
    print(r.content)
