# https://stackoverflow.com/questions/23303120/requests-interacting-strangely-with-redirect?rq=1
# Inspired by https://github.com/trchan/boston-marathon/blob/master/marathon/marathonguide.py
# Results of all marathon races come from marathonguide.com
import requests
import bs4
import urlutil
import re
import csv
import sys

# format of the dictionary:
# "Race Name": (Race ID, Format of Page)
# Format of Page == 0 for Old Format, == 1 for New Format)
# London also has a different format, but we may not get to it since we also have to scrape strava

dict_of_race = {
    "Chicago2019": 67191013,
    "Chicago2018": 67181007,
    "Chicago2017": 67171008,
    "Chicago2016": 67161009,
    "Chicago2015": 67151011,
    "Chicago2014": 67141012,
    "NewYork2019": 472191103,
    "NewYork2018": 472181104,
    "NewYork2017": 472171105,
    "NewYork2016": 472161106,
    "NewYork2015": 472151101,
    "NewYork2014": 472141102,
    "Boston2019": 15190415,
    "Boston2018": 15180416,
    "Boston2017": 15170417,
    "Boston2016": 15160418,
    "Boston2015": 15150420,
    "Boston2014": 15140421,
    "London2019": 16190428,
    "London2018": 16180422,
    "London2017": 16170423,
    "London2016": 16160424,
    "London2015": 16150426,
    "London2014": 16140413
}

def get_num_participants(race):
    '''
    Get the number of participants of a race

    Input: 
        race (str): race name

    Output: 
        (int) number of parcipants in this race
    '''
    search_page = 'http://www.marathonguide.com/results/browse.cfm?MIDD=' + str(dict_of_race[race])
    request = urlutil.get_request(search_page)
    text = urlutil.read_request(request)
    soup = bs4.BeautifulSoup(text, features='lxml')
    option_tag = soup.find("select", attrs={'name':"RaceRange", 'onchange':'clearoptions(0);'})
    last_range = option_tag.find_all("option")[-1].text
    part_number = re.findall(".+\ (\d+)", last_range)[0]
    return int(part_number)

def get_race_ranges(num_participants):
    '''
    Given a number of participants, this function returns a list of ranges of pages.

    Input:
        num_participants (int): number of participants in race

    Output:
        list of tuples, such as [(1,100), (101,176)]
    '''
    
    num_ranges = num_participants // 100
    race_range_lst = []
    for i in range(num_ranges + 1):
        if i == num_ranges:
            race_range_lst.append((i * 100 + 1, num_participants))
        else: 
            race_range_lst.append((i * 100 + 1, (i + 1) * 100))
    return race_range_lst

def get_soup_of_range(race, race_range):
    '''
    For a given race, given a range of the form (1,100), this function outputs the 
    soup of the result page with this range.

    Input: 
        race (str): race name
        race_range (tuple): a tuple of range, such as (101, 199)

    Output: 
        (soup) of the result page of this range
    '''

    num_participants = get_num_participants(race)
    race_id = str(dict_of_race[race])
    lower, upper = race_range
    s = requests.session()
    race_range_in_text = ','.join(['B', str(lower), str(upper), str(num_participants)])
    rp = 'http://www.marathonguide.com/results/makelinks.cfm'
    data = {
    'RaceRange':race_range_in_text, 
    'RaceRange_Required':'You must make a selection before viewing results.', 
    'MIDD':race_id, 
    'SubmitButton':'View'}
    
    headers = {
    "Referer":"http://www.marathonguide.com/results/browse.cfm?MIDD=" + race_id,
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"
    }
    results = s.post(rp, data=data, headers=headers)
    soup = bs4.BeautifulSoup(results.content, features='html5lib', from_encoding="utf-8")

    return soup

def next_tag(tag):
    return tag.next.next.next

def get_result_in_one_page(soup):
    '''
    Given the soup object of a page, this function returns list of participants
    and their corresponding information in this webpage. 

    Input: 
        soup: (soup) webpage of result

    Output: 
        info_lst: (list) list of participants' result in this page
    '''

    entries = soup.find_all("tr", {"bgcolor":"#CCCCCC"}) # first entry is always purple
    current_entry = entries[0]
    
    info_lst = []

    while current_entry != None:
        tag = current_entry.find("td")
        name = tag.get_text()
        name = re.findall('(.+)\ \(', name)[0]
        tag_lst = []
        while "\n" not in next_tag(tag) : # or tag != None or tag != '\n\n':
            tag = next_tag(tag)
            tag_lst.append(tag)
        for tag in tag_lst: 
            tag_text = tag.get_text()
            if ":" in tag_text: 
                time = tag_text
            elif tag_text[0] == "F" or tag_text[0] == "M":
                if tag_text[1].isnumeric() or tag_text[1] == "E":
                    div = tag_text
        current_entry = current_entry.next_sibling.next_sibling
        info_lst.append((name, div, time))

    return info_lst


def go(race):
    '''
    Given a race id, this function generates a csv file of the result of this race

    Intput: 
        race (str): race name
    '''
    
    num_participants = get_num_participants(race)
    range_lst = get_race_ranges(num_participants)

    with open("./race_result/" + race + "official.csv", mode='w') as csvfile:
        result_writer = csv.writer(csvfile)
        for race_range in range_lst: 
            print(race_range)
            soup = get_soup_of_range(race, race_range)
            info_lst = get_result_in_one_page(soup)
            for info in info_lst:
                result_writer.writerow(info)

        
if __name__ == "__main__":
    # usage example: python3 marathonguide.py Chicago2019
    race = sys.argv[1]
    go(race)
