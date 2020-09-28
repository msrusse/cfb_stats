#!/usr/bin/python3

import requests, json
from bs4 import BeautifulSoup as BS

def get_division_i_teams():
    espn_teams_url = 'https://www.espn.com/college-football/teams'
    teams_request_response = requests.get(espn_teams_url)
    if teams_request_response.status_code == 200:
        return BS(teams_request_response.text, features='lxml')
    else:
        print('Unable to retreieve Teams. Exiting with code %s...' %teams_request_response.status_code)

def get_team_ids(teams_soup):
    teams = {}
    teams_section = teams_soup.findAll('section', {'class':'TeamLinks'})
    for team in teams_section:
        href = team.find('a', href=True).get('href')
        id_with_name = href[href.find('/id/')+4:].split('/')
        teams[str(id_with_name[1])] = {
            'ESPN_ID' : str(id_with_name[0]),
            'Name' : team.find('h2').getText()
        }
    return teams

teams = get_team_ids(get_division_i_teams())
with open('teams.json', 'w') as outfile:
    outfile.write(json.dumps(teams, indent=4, sort_keys=True))