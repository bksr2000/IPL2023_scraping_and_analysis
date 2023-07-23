from bs4 import BeautifulSoup
from requests import get
from pandas import DataFrame, to_datetime
from ipl_initial_data import home_teams, venue_id, team_id, team_full_names

url = 'https://www.sportskeeda.com/go/ipl/results'

date, number_venue, team1, team2, team1_score, team2_score, result, detail_link, match_number, match_venue, winner = \
    [], [], [], [], [], [], [], [], [], [], []

t1_runs, t1_wickets, t1_overs, t2_runs, t2_wickets, t2_overs, home_team = [], [], [], [], [], [], []

webpage = get(url)
soup = BeautifulSoup(webpage.content, 'lxml')
matches = soup.find_all('div', attrs={'class': 'keeda_cricket_event_card'})

for match in matches:
    d = match.find('div', attrs={'class': 'keeda_cricket_event_date'}).text.strip()
    date.append(to_datetime(d, format='%b %d').strftime('2023-%m-%d'))
    number_venue.append(match.find('div', attrs={'class': 'keeda_cricket_venue'}).text.strip())
    content = match.find('div', attrs={'class': 'keeda_cricket_team_group'}).text.strip()
    content = content.split('\n\n\n')
    content.remove('')
    team1.append(team_id[team_full_names[content[0].strip()]])
    team1_score.append(content[1].strip())
    team2.append(team_id[team_full_names[content[2].strip()]])
    team2_score.append(content[3].strip())
    result.append(content[4].strip())
    detail_link.append(
        'https://www.sportskeeda.com/' + match.find('a', attrs={'class': 'keeda_cricket_event_match post'}).get('href'))

for each in number_venue:
    t = each.split('\n')
    match_number.append(t[0][6:])
    match_venue.append(t[1][2:])

for t1, t2 in zip(team1_score, team2_score):
    try:
        t = t1.split(' (')
        if t[0][0] == '*':
            t[0] = t[0][1:]
        t1_runs.append(int(t[0].split('/')[0]))
        t1_wickets.append(int(t[0].split('/')[1]))
        t1_overs.append(float(t[1][:-4]))
    except ValueError:
        t1_runs.append('')
        t1_wickets.append('')
        t1_overs.append('')
    try:
        t = t2.split('(')
        t2_runs.append(int(t[0].split('/')[0]))
        t2_wickets.append(int(t[0].split('/')[1]))
        t2_overs.append(float(t[1][:-4]))
    except ValueError:
        t2_runs.append('')
        t2_wickets.append('')
        t2_overs.append('')

for i in range(len(match_number)):
    if 'abandoned' in result[i].lower():
        winner.append('')
    else:
        win = result[i].split(' won ')[0].strip()
        winner.append(team_id[win])
        result[i] = (((result[i]).split(' won '))[1]).rstrip('.')

    try:
        home_team.append(team_id[home_teams[match_venue[i]]])
    except KeyError:
        home_team.append('')

    match_venue[i] = venue_id[match_venue[i]]


# these are the playoff matches, so we give the numbers to those matches
match_number[0] = 74
match_number[1] = 73
match_number[2] = 72
match_number[3] = 71

result_df = DataFrame({
    'Match Number': match_number[::-1],
    'Match Date': date[::-1],
    'Match Venue': match_venue[::-1],
    'Team 1': team1[::-1],
    'Team 1 Runs': t1_runs[::-1],
    'Team 1 Wickets': t1_wickets[::-1],
    'Team 1 Overs': t1_overs[::-1],
    'Team 2': team2[::-1],
    'Team 2 Runs': t2_runs[::-1],
    'Team 2 Wickets': t2_wickets[::-1],
    'Team 2 Overs': t2_overs[::-1],
    'Winner': winner[::-1],
    'Home Team': home_team[::-1],
    'Result': result[::-1]
})

if __name__ == '__main__':
    print('Scraping...')
