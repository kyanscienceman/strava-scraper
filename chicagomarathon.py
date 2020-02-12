'''
This program scrapes the Chicago marathon page
'''

# Example pages

'''
2019 results Men
https://results.chicagomarathon.com/2019/?page=1&event=MAR&lang=EN_CAP&pid=list&search%5Bsex%5D=M&search%5Bage_class%5D=%25

2018 results Women
https://chicago-history.r.mikatiming.com/2018/?page=2&event=MAR_999999107FA30900000000B5&lang=EN_CAP&pid=list&search%5Bsex%5D=W&search%5Bage_class%5D=%25

2018 results Men
https://chicago-history.r.mikatiming.com/2018/?page=2&event=MAR_999999107FA30900000000B5&lang=EN_CAP&pid=list&search%5Bsex%5D=M&search%5Bage_class%5D=%25

2017 results Men
https://chicago-history.r.mikatiming.com/2018/?page=2&event=MAR_999999107FA30900000000A1&lang=EN_CAP&pid=list&search%5Bsex%5D=M&search%5Bage_class%5D=%25

'''

import urlutil
import bs4
import re
import csv
import sys


year_url_dict = {
    2019: ["https://results.chicagomarathon.com/2019/?page=",
        "&event=MAR&lang=EN_CAP&pid=list&search%5Bsex%5D=",
        "&search%5Bage_class%5D=%25"], 
    2018: ["https://chicago-history.r.mikatiming.com/2018/?page=",
        "&event=MAR_999999107FA30900000000B5&lang=EN_CAP&pid=list&search%5Bsex%5D=",
        "&search%5Bage_class%5D=%25"] ,
    2017: ["https://chicago-history.r.mikatiming.com/2018/?page=",
        "&event=MAR_999999107FA30900000000A1&lang=EN_CAP&pid=list&search%5Bsex%5D=",
        "&search%5Bage_class%5D=%25"] 
}


def find_page_num(url):
    '''
    Given an url link, this function returns the number of pages of this marathon result
    '''
    request = urlutil.get_request(url)
    text = urlutil.read_request(request)
    soup = bs4.BeautifulSoup(text, features='lxml')

    button = soup.find("li", class_="pages-nav-button")

    return int(button.previous_sibling.text)

def scrape_a_page(url):
    request = urlutil.get_request(url)
    text = urlutil.read_request(request)
    soup = bs4.BeautifulSoup(text, features='lxml')
    name_tags = soup.find_all('h4', class_="list-field type-fullname")
    names = []
    for name_tag in name_tags:
        nametag = name_tag.text
        last_name = re.findall('\w*', nametag)[0]
        first_name = re.findall(', (.*)\s', nametag)[0]
        name = first_name + ' ' + last_name
        names.append(name)

    # here the names is in the format "Lastname, Firstname (NATIONALITY)"
    
    age_class_tags = soup.find_all('div', class_="list-field type-age_class")
    age_class_tags = age_class_tags[1:] # We eliminate the first element since it's column name on the website
    age_class_lst = []
    for age_class_tag in age_class_tags:
        age_class_text = age_class_tag.text
        age_class = re.search('\d(.*)', age_class_text).group()
        age_class_lst.append(age_class)
    # age_class_lst is a list of age class, where each age class is of the form '35-39'

    "visible-xs-block visible-sm-block list-label"
    time_tags = soup.find_all('div', class_="list-field type-time")
    time_tags = time_tags[1:]
    time_lst =[]
    for time_tag in time_tags:
        time_text = time_tag.text
        time = re.search('\d(.*)', time_text).group()
        time_lst.append(time)

    return (names, age_class_lst, time_lst)
    

 
def go(year):
    '''
    Given a year, this function creates a csv file of the race results
    of Chicago that year. 
    '''
    url_info = year_url_dict[year]
    year_1 = url_info[0]
    year_2 = url_info[1]
    year_3 = url_info[2]
    with open("chicagomarathon2017.csv", mode='w') as csvfile:
        result_writer = csv.writer(csvfile)
        initial_women_url = year_1 + '1' + year_2 + "W" + year_3
        page_num = find_page_num(initial_women_url)
        # write women results:
        for i in range(1,page_num + 1):
            print("W", i)
            women_url = year_1 + str(i) + year_2 + "W" + year_3
            names, age_class_lst, time_lst = scrape_a_page(women_url)
            n = len(names)
            for k in range(0,n):
                result_writer.writerow([names[k], age_class_lst[k], time_lst[k]])

        # write men results:
        initial_men_url = year_1 + '1' + year_2 + "M" + year_3
        page_num = find_page_num(initial_men_url)
        for i in range(1,page_num + 1):
            print("M", i)
            men_url = year_1 + str(i) + year_2 + "M" + year_3
            names, age_class_lst, time_lst = scrape_a_page(men_url)
            n = len(names)
            for k in range(0,n):
                result_writer.writerow([names[k], age_class_lst[k], time_lst[k]])
    


if __name__ == "__main__":
    # usage example: python3 chicagomarathon.py 2019
    year = int(sys.argv[1])
    go(year)