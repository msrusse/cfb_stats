#! python

import grequests, json, progressbar, datetime
from bs4 import BeautifulSoup as BS

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

def get_player_stats_by_team_pages(teams):
    urls = []
    for team in teams:
        for year in range(2004, int(datetime.datetime.now().year)+1):
            urls.append('https://www.espn.com/college-football/team/stats/_/id/%s/season/%s' % (teams[team]['ESPN_ID'], year))
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
    
def get_player_stats(team_responses):
    pb = progressbar.ProgressBar()
    player_stats = {}
    for response in pb(team_responses):
        if response['Status'] == 200:
            team_soup = BS(response['Response_Text'], features='lxml')
            tables = team_soup.findAll('table')
            temp_stats = {
                'Passing' : {},
                'Rushing' : {},
                'Receiving' : {},
                'Kicking' : {},
                'Defense' : {}
            }
            for i in range(0,len(tables)):
                stat_type = get_stat_type(i)
                if i%2 == 0:
                    for row in tables[i].find('tbody').findAll('tr'):
                        if row.find('a'):
                            player_uid = row.find('a').get('data-player-uid')
                            player_id = player_uid[player_uid.rfind(':')+1:]
                            temp_stats[stat_type][row.get('data-idx')] = {
                                'Player_ID' : player_id
                            }
                            player_stats[player_id] = {
                                'Name' : row.find('a').getText()
                            }
                else:
                    headers = []
                    for row in tables[i].find('thead').findAll('th'):
                        if row.find('a'):
                            headers.append(row.find('a').getText())
                    for player in tables[i].find('tbody').findAll('tr'):
                        stats = player.findAll('td')
                        for stat in range(0, len(stats)):
                            data_id = player.get('data-idx')
                            if int(data_id) in range(0, len(tables[i].find('tbody').findAll('tr'))-1):
                                # temp_stats[get_stat_type(i)][player.get('data-idx')][headers[stat]] = stats[stat].getText()
                                player_stats[temp_stats[stat_type][data_id]][stat_type][headers[stat]] = stats[stat].getText()                               
            # player_stats[response['URL']] = temp_stats
        else:
            player_stats[response.url] = {    
                'No Data' : response['Status'],
                'URL' : response['URL']
            }
    return player_stats

teams = json.load(open('teams.json'))
pb = progressbar.ProgressBar()
team_responses = get_player_stats_by_team_pages(teams)
team_responses = get_school_id_and_year_from_url(team_responses)
player_stats = get_player_stats(team_responses)
with open('team_player_stats.json', 'w') as outfile:
    outfile.write(json.dumps(player_stats, indent=4, sort_keys=True))