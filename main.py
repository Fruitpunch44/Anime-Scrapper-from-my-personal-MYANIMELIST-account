import logging
import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from generate_random import *

# create a log file
file_name = 'scrapping.txt'
file_dir = 'MAl account'
FILEPATH = os.path.join(file_dir, file_name)

# create directory if it does not exist
if not os.path.exists(file_dir):
    os.mkdir(file_dir)

# logging settings
logging.basicConfig(filename=FILEPATH, level=logging.INFO, format="%(asctime)s:%(filename)s:%(message)s")

# had to use selenium cause beautiful soup can't handle JavaScript
driver = webdriver.Edge()

url = "https://myanimelist.net/animelist/CryingMinotaur?status=6"

anime_shows = []  # store anime data here


# test for website connection
def check(url_name):
    try:
        req = requests.get(url_name, timeout=5)
        if req.status_code == 200:
            print('success')
        else:
            print('sorry can not find shit')
        return req.status_code
    except (requests.ConnectionError, requests.Timeout) as e:
        print(f'error: {e} occurred ')
        logging.error(f'error: {e} occurred ')


# save locally for whatever reason I don't know lol
# future purposes
def save_html_locally(url_name):
    req = requests.get(url_name)
    filename = url_name.split('/')[-2]
    filename2 = f'{filename}.html'
    if not os.path.exists(filename2):
        with open(filename2, 'wb') as file:
            file.write(req.content)
    else:
        print('file exists already so yh kill yourself')
    logging.info(f'Successfully saved raw html file ')


def create_soup_object():
    driver.get(url)
    req = driver.page_source
    scroll_page_javascript()
    soup = BeautifulSoup(req, 'html.parser')
    print("soup created")
    logging.info(f'Successfully created soup object')
    return soup


def scroll_page_javascript():
    """there is a weird bug that where it doesn't scroll down during
     the scrapping process, but after it starts scrolling, I don't really get this
     fml will look into it later"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:

        driver.execute_script("scrollTo(0,document.body.scrollHeight)")
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height


def find():
    obj = create_soup_object()
    # find table object it's just one
    table = obj.find('table', class_="list-table")
    if not table:
        print('table not found')

    if table:
        elements = table.find_all('tbody', class_='list-item')

        if elements:
            for element in elements:
                # create a dict to store the values
                data = {"name": None,
                        "type": None,
                        "rating": None,
                        "Episode Count": None}

                # get name
                title = element.find('td', class_='data title clearfix')
                if title:
                    name = title.find('a', class_='link sort')
                    if name:
                        data['name'] = name.text.strip()
                # get type(i.e movie,tv ,ova etc)
                content_type = element.find('td', class_='data type')
                if content_type:
                    data['type'] = content_type.text.strip()

                # get tv rating(i.e pg13,R etc)
                rating = element.find('td', class_='data rated')
                if rating:
                    data['rating'] = rating.text.strip()

                # get episode count
                episode = element.find('td', class_="data progress")
                if episode:
                    episode_count = episode.find_all('span')
                    for episode_counts in episode_count:
                        data['Episode Count'] = episode_counts.text.strip()

                anime_shows.append(data)
    else:
        print(f'{table} not found')
        logging.info('sorry no table was found on this page')

        # print(element.prettify()) debugging purposes


def main():
    while True:
        # display options
        options = {"1": "Save Locally",
                   "2": "Start Scrapping",
                   "3": "Check Site Status",
                   "4": "Show All Shows",
                   "5": "Generate Random Number of Shows",
                   "6": "Save Random Shows",
                   "7": "Exit"}
        for key, value in options.items():
            print(f'{key}:{value}')

        selected_options: str = input("enter an option: ")
        if selected_options in options:
            opt = options[selected_options]

            if opt == 'Check Site Status':
                check(url)
            elif opt == 'Save Locally':
                save_html_locally(url)

            elif opt == 'Show All Shows':
                if not anime_shows:
                    print("nothing is here yet")
                else:
                    for number, name in enumerate(anime_shows):
                        print(f'{number + 1}\n'
                              f'Name:{name['name']}\n'
                              f'Type:{name['type']}\n'
                              f'Rating:{name['rating']}\n'
                              f'Episode Count:{name['Episode Count']}\n')

            elif opt == 'Start Scrapping':
                find()
            elif opt == 'Generate Random Number of Shows':
                generate(anime_shows)
            elif opt == 'Save Random Shows':
                save_list()
            elif opt == 'Exit':
                print("****Program Terminated****")
                driver.close()
                logging.info(f"program was terminate at {time.asctime()}")
                sys.exit(1)
            else:
                print('invalid option selected ')
                logging.error(f'An invalid option{opt} was used')


if __name__ == "__main__":
    main()
