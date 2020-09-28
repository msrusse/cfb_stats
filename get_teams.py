#!/usr/bin/python3

import requests, json, progressbar
from bs4 import BeautifulSoup as BS
from pprint import pprint

def get_stat_type(x):
    return {
        0 : 'Passing',
        1 : 'Passing',
        2 : 'Rushing',
        4 : 'Receiving',
        6 : 'Kicking',
        8 : 'Defense',
        3 : 'Rushing',
        5 : 'Receiving',
        7 : 'Kicking',
        9 : 'Defense'
    }.get(x)

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
        teams[str(id_with_name[0])] = {
            'SanitizedName' : id_with_name[1],
            'Name' : team.find('h2').getText()
        }
    return teams

def get_player_stats_by_team(team_id):
    team_url = 'https://www.espn.com/college-football/team/stats/_/id/%s' % team_id
    team_request_response = requests.get(team_url)
    if team_request_response.status_code == 200:
        team_soup = BS(team_request_response.text, features='lxml')
        tables = team_soup.findAll('table')
        player_stats = {
            'Passing' : {},
            'Rushing' : {},
            'Receiving' : {},
            'Kicking' : {},
            'Defense' : {}
        }
        for i in range(0,len(tables)):
            if i%2 == 0:
                for row in tables[i].find('tbody').findAll('tr'):
                    if row.find('a'):
                        player_uid = row.find('a').get('data-player-uid')
                        player_id = player_uid[player_uid.rfind(':')+1:]
                        player_stats[get_stat_type(i)][row.get('data-idx')] = {
                            'Player_ID' : player_id,
                            'Name' : row.find('a').getText()
                        }
                player_stats[get_stat_type(i)][str(len(tables[i].find('tbody').findAll('tr'))-1)] = {
                    'Name' : 'Total'
                }
            else:
                headers = []
                for row in tables[i].find('thead').findAll('th'):
                    if row.find('a'):
                        headers.append(row.find('a').getText())
                for player in tables[i].find('tbody').findAll('tr'):
                    stats = player.findAll('td')
                    for stat in range(0, len(stats)):
                        player_stats[get_stat_type(i)][player.get('data-idx')][headers[stat]] = stats[stat].getText()
        return player_stats
    else:
        return {
            'No Data' : team_request_response.status_code
        }

teams = get_team_ids(get_division_i_teams())
pb = progressbar.ProgressBar()
for team in pb(teams):
    teams[team]['PlayerStats'] = get_player_stats_by_team(team)
with open('team_player_stats.json', 'w') as outfile:
    outfile.write(json.dumps(teams, indent=4, sort_keys=True))