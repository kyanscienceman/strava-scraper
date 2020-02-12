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
    'Cookie': "ajs_anonymous_id=%226c7f28bf-7dc6-458d-ae6e-1a77d64bb699%22; sp=9b0c7ee1-35b7-4de1-b435-4591d5a6df24; _ga=GA1.2.78499818.1581111281; _fbp=fb.1.1581111281182.1991822037; _strava_cookie_banner=true; _sp_id.047d=7d1689d5-3c2a-4af1-bad4-9f67f5160169.1581118356.1.1581534481.1581118378.b964ce46-dd55-4f20-9b53-239c0d2a946b; ajs_user_id=null; ajs_group_id=null; _strava4_session=f4p9kcvcf0av2p4a1ao58ajt2p2q521k; _sp_ses.047d=*; _gid=GA1.2.1424905716.1581534482; _dc_gtm_UA-6309847-24=1",
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
