import pandas as pd


def sql_query(frame, table) -> str:
    """creates the INSERT statement using the data from dataframe and returns it"""

    query = 'INSERT INTO ' + table + ' VALUES ('
    for x in range(len(df)):
        for y in frame.columns:
            if pd.isna(frame[y][x]):
                query += 'NULL,'
            else:
                try:
                    if float(frame[y][x]) % 1 == 0:
                        p = int(frame[y][x])
                        query += (str(p) + ',')
                    else:
                        p = float(frame[y][x])
                        query += (str(p) + ',')

                except ValueError:
                    query += ("'" + str(frame[y][x]) + "',")

        query = query[:-1] + '), ('
    query = query[:-3] + ';'
    return query


if __name__ == '__main__':
    df = pd.read_csv('files/_ipl_venues.csv')
    print(sql_query(df, 'venues'))

    df = pd.read_csv('files/_ipl_teams.csv')
    print(sql_query(df, 'teams'))

    df = pd.read_csv('files/_ipl_players.csv')
    print(sql_query(df, 'players'))

    df = pd.read_csv('files/ipl_results.csv')
    print(sql_query(df, 'match_result'))

    df = pd.read_csv('files/ipl_batting.csv')
    print(sql_query(df, 'batting_stats'))

    df = pd.read_csv('files/ipl_bowling.csv')
    print(sql_query(df, 'bowling_stats'))

    df = pd.read_csv('files/ipl_fall_of_wickets.csv')
    print(sql_query(df, 'fall_of_wickets'))

    df = pd.read_csv('files/ipl_stats.csv')
    print(sql_query(df, 'match_stats'))

    df = pd.read_csv('files/ipl_extras.csv')
    print(sql_query(df, 'extra_runs'))
