#! /usr/bim/local/python3

import requests
from bs4 import BeautifulSoup as BS
from pprint import pprint

espn_teams_url = 'https://www.espn.com/college-football/teams'
teams_request_response = requests.get(espn_teams_url)
if teams_request_response.status_code == 200:
    teams_soup = BS(teams_request_response.text, features='lxml')

with open('epsn_teams.html', 'w') as outfile:
    outfile.write(str(teams_soup))