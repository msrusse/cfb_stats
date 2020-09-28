#! python

import grequests, json, progressbar, datetime
from bs4 import BeautifulSoup as BS

def get_rosters_by_team_and_year(teams):
    urls = []
    for team in teams:
        for year in range(2004, int(datetime.datetime.now().year)+1):
            urls.append('https://www.espn.com/college-football/team/roster/_/id/%s/season/%s' % (teams[team]['ESPN_ID'], year))
            # teams[team]['PlayerStats_%s' % year] = get_player_stats_by_team(teams[team]['ESPN_ID'], year)
    return grequests.map((grequests.get(url) for url in urls))

def get_school_id_and_year_from_url(team_responses):
    responses = []
    for response in team_responses:
        try:
            responses.append({
                'Year' : response.url.split('/id/')[1].split('/season/')[1],
                'Team_ID' : response.url.split('/id/')[1].split('/season/')[0],
                'Status' : response.status_code,
                'URL' : response.url,
                'Response_Text' : response.text
            })
        except:
            print(response)
    return responses

def get_players_on_roster(team_responses_split):
    pb = progressbar.ProgressBar()
    for response in pb(team_responses_split):
        if response['Status'] == 200:
            roster_soup = BS(response['Response_Text'], features='lxml')
            tables = roster_soup.findAll('table')
            print(len(tables))

teams = json.load(open('teams.json'))
team_responses = get_rosters_by_team_and_year(teams)
team_responses_split = get_school_id_and_year_from_url(team_responses)
get_players_on_roster(team_responses_split)