# Python code to log into Strava

#https://www.strava.com/login

import requests
from lxml import html

session_requests = requests.session()

#email input
#<input type="email" name="email" id="email" value="" placeholder="Your Email" autofocus="autofocus" class="form-control">

#password input
#<input type="password" name="password" id="password" value="" placeholder="Password" class="form-control">

#csrf token
#<meta name="csrf-token" content="l3ge0TbJM9KhInAvxl0iCOI4uOLmzM+1ZiZs5j9y6OQvzuHtFX322osc4ipggMdHuoCuEEC4dpA6dHGcdNz83Q==">

payload = {
	"username": "<USER NAME>", 
	"password": "<PASSWORD>", 
	"csrfmiddlewaretoken": "l3ge0TbJM9KhInAvxl0iCOI4uOLmzM+1ZiZs5j9y6OQvzuHtFX322osc4ipggMdHuoCuEEC4dpA6dHGcdNz83Q"
}




