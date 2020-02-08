'''
This program scrapes the Chicago marathon page
'''

# Example pages
# https://results.chicagomarathon.com/2019/?page=1&event=MAR&lang=EN_CAP&pid=list&search%5Bsex%5D=M&search%5Bage_class%5D=%25
# https://chicago-history.r.mikatiming.com/2018/?page=2&event=MAR_999999107FA30900000000B5&lang=EN_CAP&pid=list&search%5Bsex%5D=M&search%5Bage_class%5D=%25


import urlutil
import bs4
import re
import csv




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
    

 
def go():
    '''
    Given a year, this function creates a csv file of the race results
    of Chicago that year. 
    '''
    with open("chicagomarathon2018.csv", mode='w') as csvfile:
        result_writer = csv.writer(csvfile)
        for i in range(1,958):
            print(i)
            url = "https://chicago-history.r.mikatiming.com/2018/?page=" + str(i) + "&event=MAR_999999107FA30900000000B5&lang=EN_CAP&pid=list&search%5Bsex%5D=M&search%5Bage_class%5D=%25"
            names, age_class_lst, time_lst = scrape_a_page(url)
            n = len(names)
            for k in range(0,n):
                result_writer.writerow([names[k], age_class_lst[k], time_lst[k]])
    


if __name__ == "__main__":
    go()