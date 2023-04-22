import requests
from bs4 import BeautifulSoup


def scraped_spot_list():
    # Extract the ids from the large json file
    return []


base_url = "https://thespot2be.com/spot/{}"

spot_list = scraped_spot_list()
# DEBUG
spot_list = [
    "e805b6a02cefe005",
    "st_lunaire___les_longchamps",
]  # list of unique ids or spot names

for spot in spot_list:
    url = base_url.format(spot)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    card_read_more_div = soup.find("div", {"class": "card-read-more m-b-40"})
    spot_info = card_read_more_div.text.strip()
    print(spot_info.split("----")[0])  # Get the french part of it
    # save spot_info to the database or do whatever you need with it
