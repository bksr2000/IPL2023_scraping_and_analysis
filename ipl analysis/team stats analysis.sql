-- types of players for each team(played atleast one match)
SELECT team_name, player_role, COUNT(*) FROM players AS p
JOIN teams AS t ON p.team_id = t.id
GROUP BY team_name, player_role;


-- total runs by each team
SELECT team_name, sum(score) AS runs_scored FROM match_stats AS ms
JOIN teams AS t ON ms.team_id = t.id
GROUP BY team_id 
ORDER BY runs_scored DESC;


-- centuries by each team players
SELECT team_name, count(*) AS centuries_made FROM batting_stats AS bs
JOIN teams AS t ON bs.team_id = t.id
WHERE runs >= 100
GROUP BY team_id 
ORDER BY centuries_made DESC;


-- fifties by each team players
SELECT team_name, count(*) AS fifties_made FROM batting_stats AS bs
JOIN teams AS t ON bs.team_id = t.id
WHERE runs >= 50 AND runs < 100
GROUP BY team_id 
ORDER BY fifties_made DESC;


-- boundaries by team
SELECT team_name, sum(sixes)+SUM(fours) AS boundaries_hit FROM match_stats AS ms
JOIN teams AS t ON ms.team_id = t.id
GROUP BY team_id 
ORDER BY boundaries_hit DESC;


-- total wickets lost by each teams
SELECT team_name, sum(wickets) AS wickets_lost FROM match_stats AS ms
JOIN teams AS t ON ms.team_id = t.id
GROUP BY team_id 
ORDER BY wickets_lost;


-- total wickets taken by teams
SELECT team_name, sum(wickets) AS wickets_lost FROM wickets_taken AS ms  -- using view
JOIN teams AS t ON ms.team_id = t.id
GROUP BY team_id 
ORDER BY wickets_lost DESC;


-- man of the matches per team
SELECT team_name, COUNT(*) FROM match_result AS mr
JOIN players AS p ON mr.player_of_match = p.id
JOIN teams AS t ON p.team_id=t.id
GROUP BY team_id
ORDER BY COUNT(*) DESC; 


-- home wins per team
SELECT team_name, COUNT(*) AS home_wins FROM match_result AS mr
JOIN teams AS t ON winner_team=t.id
WHERE winner_team = home_team
GROUP BY winner_team
ORDER BY COUNT(*) DESC;  


-- highest and lowest scores
SELECT 'highest' AS score_type,team_name, score FROM match_stats 
JOIN teams ON teams.id = team_id
WHERE score = (SELECT MAX(score) from match_stats)
UNION
SELECT 'lowest', team_name, score FROM match_stats 
JOIN teams ON teams.id = team_id
WHERE score = (SELECT MIN(score) from match_stats WHERE score>0);


-- teams and home ground
SELECT DISTINCT team_name, venue_name FROm match_result
JOIN teams on home_team=teams.id
JOIN venues ON venue_id=venues.id;
