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
    "Chicago2019": (67191013, 1),
    "Chicago2018": (67181007, 1),
    "Chicago2017": (67171008, 0),
    "Chicago2016": (67161009, 0),
    "Chicago2015": (67151011, 0),
    "Chicago2014": (67141012, 0),
    "NewYork2019": (472191103, 1),
    "NewYork2018": (472181104, 1),
    "NewYork2017": (472171105, 1),
    "NewYork2016": (472161106, 0),
    "NewYork2015": (472151101, 0),
    "NewYork2014": (472141102, 0),
    "Boston2019": (15190415, 1),
    "Boston2018": (15180416, 1),
    "Boston2017": (15170417, 0),
    "Boston2016": (15160418, 0),
    "Boston2015": (15150420, 0),
    "Boston2014": (15140421, 0)
}

dict_of_race_extra = {
    "London2019": (16190428, 1),
    "London2018": (16180422, 1),
    "London2017": (16170423, 0),
    "London2016": (16160424, 0),
    "London2015": (16150426, 0),
    "London2014": (16140413, 0)
}

def get_num_participants(race):
    '''
    Get the number of participants of a race

    Input: 
        race (str): race name

    Output: 
        (int) number of parcipants in this race
    '''
    search_page = 'http://www.marathonguide.com/results/browse.cfm?MIDD=' + str(dict_of_race[race][0])
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
    race_id = str(dict_of_race[race][0])
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

def get_result_in_one_page(soup, race):
    '''
    Given the soup object of a page, this function returns list of participants
    and their corresponding information in this webpage. 

    Input: 
        soup: (soup) webpage of result
        race (str): race name

    Output: 
        info_lst: (list) list of participants' result in this page
    '''

    entries = soup.find_all("tr", {"bgcolor":"#CCCCCC"}) # first entry is always purple
    current_entry = entries[0]
    
    info_lst = []

    while current_entry != None:
        print(current_entry)
        tag = current_entry.find("td")
        name = tag.get_text()
        name = re.findall('(.+)\ \(', name)[0]
        tag_lst = []
        tag = next_tag(tag)
        while tag != '\n' or tag != None or tag != '\n\n':
            print("THIS IS TAGGGGGG", tag)
            tag_lst.append(tag)
            tag = next_tag(tag)
        for tag in tag_lst: 
            tag_text = tag.get_text()
            if ":" in tag_text: 
                time = tag_text
            elif tag_text[0] == "F" or tag_text[0] == "M":
                if tag_text[1].isnumeric():
                    div = tag_text
                '''
        name = re.findall('(.+)\ \(', name)[0]
        time = current_entry.find("td").next.next.next
        time_text = time.get_text()
        overall_place = time.next.next.next
        overall_place_text = overall_place.get_text()
        div_place = overall_place.next.next.next
        if dict_of_race[race][1] == 1:
            age_div = div_place.get_text()
            div = div_place.next.next.next
            net_time_text = div.get_text()
            origin = div.next.next.next
            origin_text = origin.get_text()
        elif dict_of_race[race][1] == 0:
            div_place_text = div_place.get_text()
            div = div_place.next.next.next
            age_div = div.get_text()
            origin = div.next.next.next
            origin_text = origin.get_text()
            ag_time = origin.next.next.next
            net_time_text = ag_time.get_text()

        # we only need name, age_div, and time
        '''
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
            info_lst = get_result_in_one_page(soup, race)
            for info in info_lst:
                result_writer.writerow(info)

        
if __name__ == "__main__":
    # usage example: python3 marathonguide.py Chicago2019
    race = sys.argv[1]
    go(race)
