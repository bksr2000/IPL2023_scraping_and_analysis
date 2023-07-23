import pandas as pd

# this file will get the data of team names, venue names and player names which we will use in other files

home_teams = {
    'Narendra Modi Stadium, Ahmedabad': 'Gujarat Titans',
    'Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh': 'Punjab Kings',
    'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow': 'Lucknow Super Giants',
    'Rajiv Gandhi International Stadium, Uppal, Hyderabad': 'Sunrisers Hyderabad',
    'M.Chinnaswamy Stadium, Bengaluru': 'Royal Challengers Bangalore',
    'MA Chidambaram Stadium, Chennai': 'Chennai Super Kings',
    'Arun Jaitley Stadium, Delhi': 'Delhi Capitals',
    'Eden Gardens, Kolkata': 'Kolkata Knight Riders',
    'Wankhede Stadium, Mumbai': 'Mumbai Indians',
    'Sawai Mansingh Stadium, Jaipur': 'Rajasthan Royals'
}

team_full_names = {
    'GT': 'Gujarat Titans',
    'PBKS': 'Punjab Kings',
    'LSG': 'Lucknow Super Giants',
    'SRH': 'Sunrisers Hyderabad',
    'RCB': 'Royal Challengers Bangalore',
    'CSK': 'Chennai Super Kings',
    'DC': 'Delhi Capitals',
    'KKR': 'Kolkata Knight Riders',
    'MI': 'Mumbai Indians',
    'RR': 'Rajasthan Royals',
}
team_id, venue_id, player_id = {}, {}, {}

df = pd.read_csv('files/_ipl_teams.csv')
t_id = df['id'].tolist()
t_name = df['name'].tolist()
for i in range(len(df)):
    team_id[t_name[i]] = t_id[i]

df = pd.read_csv('files/_ipl_venues.csv')
v_id = df['id'].tolist()
v_name = df['venue'].tolist()
for i in range(len(df)):
    venue_id[v_name[i]] = v_id[i]

df = pd.read_csv('files/_ipl_players.csv')
p_id = df['id'].tolist()
p_name = df['Name'].tolist()
for i in range(len(df)):
    player_id[p_name[i]] = p_id[i]
