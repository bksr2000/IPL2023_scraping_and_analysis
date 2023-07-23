from ipl_scrape import detail_link, match_number, result_df
from ipl_initial_data import team_id, player_id
from bs4 import BeautifulSoup
from requests import get
from pandas import DataFrame

print('Scraping...')
player_of_match = []

batter_name, batter_runs, batter_balls, batter_fours, batter_sixes, batter_sr, batter_out, batter_match_number, \
    batter_team_id = [], [], [], [], [], [], [], [], []
bowler_name, bowler_overs, bowler_maidens, bowler_runs, bowler_wickets, bowler_economy, bowler_extras, \
    bowler_match_number, bowler_team_id = [], [], [], [], [], [], [], [], []

fow_match_number, fow_team_id, fow_batter, fow_score, fow_over = [], [], [], [], []

stats_match, stats_team, stats_runs, stats_wickets, stats_overs, stats_rr, stats_sixes, stats_fours = \
    [], [], [], [], [], [], [], []
extras_match, extras_team, extras_total, extras_byes, extras_leg_byes, extras_no_ball, extras_wides = \
    [], [], [], [], [], [], []

for i in range(len(detail_link)):
    url = detail_link[-i-1]

    t1_batter_count = 0

    t1_extras, t1_extras_info = 0, 0

    flag = 0
    webpage = get(url)
    soup = BeautifulSoup(webpage.content, 'lxml')

    numb = match_number[-i-1]

    content = soup.find('div', attrs={'class': 'right-section'})
    try:
        player_of_match.append(player_id[content.find('span', attrs={'id': 'player-of-match'}).text.strip()])
    except KeyError:
        player_of_match.append('')

    teams = soup.find_all('span', attrs={'class': 'country bind'})

    team1_id = team_id[teams[0].text.strip()]
    team2_id = team_id[teams[1].text.strip()]

    t1 = soup.find('div', attrs={'class': 'one-innings-div innings-content-0'})
    t2 = soup.find('div', attrs={'class': 'one-innings-div innings-content-1'})

    for t in [t1, t2]:
        if t is None:
            extras_match.append(numb)
            extras_team.append(team2_id)
            extras_total.append('')
            extras_byes.append('')
            extras_leg_byes.append('')
            extras_no_ball.append('')
            extras_wides.append('')

            stats_match.append(numb)
            stats_team.append(team1_id)
            stats_runs.append('')
            stats_wickets.append('')
            stats_overs.append('')
            stats_rr.append('')
            stats_fours.append('')
            stats_sixes.append('')
            continue

        bat = t.find('div', attrs={'class': 'innings-table-body'})
        batters = bat.find_all('div', attrs={'class': 'parent-row-holder'})
        ball = t.find('div', attrs={'class': 'innings-table-bowling'})
        bowlers = ball.find_all('div', attrs={'class': 'innings-table-row-holder'})

        for b in batters:
            batter_match_number.append(numb)
            batter_name.append(player_id[b.find('span', attrs={'class': 'batsman-name'}).text.strip()])
            batter_runs.append(b.find('div', attrs={'class': 'innings-runs'}).text)
            batter_balls.append(b.find('div', attrs={'class': 'innings-balls'}).text)
            batter_fours.append(b.find('div', attrs={'class': 'innings-fours'}).text)
            batter_sixes.append(b.find('div', attrs={'class': 'innings-sixes'}).text)
            batter_sr.append(b.find('div', attrs={'class': 'innings-strike-rate'}).text.strip())
            batter_out.append(b.find('div', attrs={'class': 'innings-bowler-row'}).text.strip())
            batter_team_id.append(team1_id)

        extras_match.append(numb)
        extras_team.append(team2_id)
        extras_total.append(bat.find('div', attrs={'class': 'innings-extras-runs'}).text)
        details = bat.find('div', attrs={'class': 'innings-extras-info'}).text.strip(' ')
        temp = [i.split(':') for i in details.split(',')]
        extras_byes.append(temp[0][1].strip())
        extras_leg_byes.append(temp[1][1].strip())
        extras_no_ball.append(temp[2][1].strip())
        extras_wides.append(temp[3][1][:-1].strip())

        stats_match.append(numb)
        stats_team.append(team1_id)
        total_score = bat.find('div', attrs={'class': 'innings-total-runs'}).text
        stats_runs.append(int(total_score.split('/')[0]))
        stats_wickets.append(int(total_score.split('/')[1]))
        desc = bat.find('p', attrs={'class': 'innings-total-description'}).text
        stats_overs.append(float(desc.split(',')[0][1:-3]))
        stats_rr.append(float(desc.split(',')[1][4:-1]))
        stats_fours.append(bat.find('div', attrs={'class': 'innings-total-fours'}).text)
        stats_sixes.append(bat.find('div', attrs={'class': 'innings-total-sixes'}).text)

        for b in bowlers:
            bowler_match_number.append(numb)
            bowler_team_id.append(team2_id)
            bowler_name.append(player_id[b.find('span', attrs={'class': 'bowler-name'}).text.strip()])
            bowler_overs.append(b.find('div', attrs={'class': 'innings-overs'}).text)
            bowler_maidens.append(b.find('div', attrs={'class': 'innings-maiden-overs'}).text)
            bowler_runs.append(b.find('div', attrs={'class': 'innings-runs'}).text)
            bowler_wickets.append(b.find('div', attrs={'class': 'innings-wickets'}).text)
            bowler_economy.append(b.find('div', attrs={'class': 'innings-economy'}).text)
            bowler_extras.append(b.find('div', attrs={'class': 'innings-extras'}).text)

        fow = t.find('div', attrs={'class': 'innings-table-fow-body'})
        fow_batter.extend(player_id[i.text] for i in (fow.find_all('span', attrs={'class': 'fow-batsman'})))
        fow_score.extend(i.text for i in fow.find_all('div', attrs={'class': 'innings-score'}))
        fow_over.extend(i.text for i in fow.find_all('div', attrs={'class': 'innings-over'}))
        fow_match_number.extend([numb] * stats_wickets[-1])
        fow_team_id.extend([team1_id] * stats_wickets[-1])

        if flag == 0:
            team1_id, team2_id = team2_id, team1_id
            flag = 1

if __name__ == '__main__':
    result = DataFrame({
        'Match Number': batter_match_number,
        'Team id': batter_team_id,
        'Batter id': batter_name,
        'Runs': batter_runs,
        'Balls': batter_balls,
        'Fours': batter_fours,
        'Sixes': batter_sixes,
        'Strike Rate': batter_sr,
        'Out/Not': batter_out
    })
    # print(result)
    # print('-' * 60)
    result.to_csv('files/ipl_batting.csv', index=False)

    result = DataFrame({
        'Match Number': bowler_match_number,
        'Team id': bowler_team_id,
        'Bowler id': bowler_name,
        'Overs': bowler_overs,
        'Maidens': bowler_maidens,
        'Runs': bowler_runs,
        'Wickets': bowler_wickets,
        'Economy': bowler_economy,
        'Extras': bowler_extras
    })
    # print(result)
    # print('-' * 60)
    result.to_csv('files/ipl_bowling.csv', index=False)

    result = DataFrame({
        'Match Number': fow_match_number,
        'Team id': fow_team_id,
        'Batter id': fow_batter,
        'Wicket Number': list(i.split('-')[0] for i in fow_score),
        'Score': list(i.split('-')[1] for i in fow_score),
        'Over': fow_over
    })
    # print(result)
    # print('-' * 60)
    result.to_csv('files/ipl_fall_of_wickets.csv', index=False)

    result = DataFrame({
        'Match Number': stats_match,
        'Team id': stats_team,
        'Score': stats_runs,
        'Wickets': stats_wickets,
        'Overs': stats_overs,
        'Run Rate': stats_rr,
        'Fours': stats_fours,
        'Sixes': stats_sixes,
        'Extras': extras_total
    })
    # print(result)
    # print('-' * 60)
    result.to_csv('files/ipl_stats.csv', index=False)

    result = DataFrame({
        'Match Number': extras_match,
        'Team id': extras_team,
        'Extras': extras_total,
        'Byes': extras_byes,
        'Leg Byes': extras_leg_byes,
        'No Balls': extras_no_ball,
        'Wides': extras_wides
    })
    # print(result)
    # print('-' * 60)
    result.to_csv('files/ipl_extras.csv', index=False)

    result_df['Man of the Match'] = player_of_match
    # print(result_df)
    result_df.to_csv('files/ipl_results.csv', index=False)
