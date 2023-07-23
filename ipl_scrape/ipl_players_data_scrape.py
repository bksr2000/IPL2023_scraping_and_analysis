from ipl_scrape import detail_link
from ipl_initial_data import team_full_names, team_id
from bs4 import BeautifulSoup
from requests import get
from pandas import DataFrame


def players_details(sec) -> list:
    """finds all the player names from the website and stores the names into a list"""
    ls = []
    players = sec[0].find_all('div', attrs={'class': 'player-role-info'})
    if len(players) == 2 or len(players) == 11:
        ls.extend([j.text.strip() for j in players])
    players = sec[1].find_all('div', attrs={'class': 'player-role-info'})
    if len(players) == 11:
        ls.extend([j.text.strip() for j in players])
    return ls


def splitting_players(data) -> list:
    """Stripping out the extra details from player names"""
    ls = []
    for each in data:
        t = each.split('\n')
        while '' in t:
            t.remove('')
        if 'Impact Player' in t:
            t.remove('Impact Player')
        if 'Substitute' in t:
            t.remove('Substitute')
        if '(C)' in t:
            t.remove('(C)')
        ls.append((t[0].strip(), t[1]))
    return ls


def add_players(info, team):
    """adds new players to the list where we store the players data"""
    global player_id, player_name, player_team, player_role
    for each in info:
        if each[0] not in player_name:
            player_id.append(len(player_id)+1)
            player_name.append(each[0].strip())
            player_role.append(each[1])
            player_team.append(team)


player_id, player_name, player_team, player_role = [], [], [], []
lt_players, rt_players = [], []

for i in range(len(detail_link)):
    url = detail_link[-i-1] + '/squad'
    webpage = get(url)
    soup = BeautifulSoup(webpage.content, 'lxml')

    teams = soup.find_all('a', attrs={'class': 'team-flag-anchor'})
    lt = team_id[team_full_names[teams[0].text.strip()]]
    rt = team_id[team_full_names[teams[1].text.strip()]]

    section = soup.find_all('div', attrs={'class': 'team-squad-left'})
    lt_players = splitting_players(players_details(section))
    section = soup.find_all('div', attrs={'class': 'team-squad-right'})
    rt_players = splitting_players(players_details(section))

    add_players(lt_players, lt)
    add_players(rt_players, rt)


result = DataFrame({
    'id': player_id,
    'Name': player_name,
    'Team': player_team,
    'Role': player_role
})
# print(result)
result.to_csv('files/_ipl_players.csv', index=False)
