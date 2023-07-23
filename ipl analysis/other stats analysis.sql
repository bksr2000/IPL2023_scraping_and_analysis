-- toal 4s an 6s
SELECT SUM(fours) AS total_fours, sum(sixes) AS total_sixes 
FROM match_stats;


-- man of the match more than once
SELECT player_name, COUNT(*) FROM match_result AS mr
JOIN players AS p ON mr.player_of_match = p.id
GROUP BY player_of_match 
HAVING COUNT(*)>1;


-- wins by innings
SELECT 'first' AS Innings, COUNT(*) AS wins FROM match_result AS mr
JOIN teams AS t ON winner_team=t.id
WHERE winner_team = team1_id
UNION
SELECT 'second', COUNT(*) FROM match_result AS mr
JOIN teams AS t ON winner_team=t.id
WHERE winner_team = team2_id;


-- extras -------------------------------------------------------------------------------------------
-- most extras given
SELECT team_name, sum(extras) AS extras_given FROM extra_runs AS er
JOIN teams AS t ON er.team_id = t.id
GROUP BY team_id 
ORDER BY extras_given DESC;

-- no balls bowled
SELECT team_name, sum(no_balls) AS no_balls FROM extra_runs AS er
JOIN teams AS t ON er.team_id = t.id
GROUP BY team_id 
ORDER BY no_balls DESC;

-- most extras given
SELECT team_name, sum(wides) AS wides_bowled FROM extra_runs AS er
JOIN teams AS t ON er.team_id = t.id
GROUP BY team_id 
ORDER BY wides_bowled DESC;


-- highest extras in a match by a team
SELECT team_name, extras FROM extra_runs
JOIN teams ON teams.id=team_id
ORDER BY extras DESC LIMIT 3;

-- fall of wickets ---------------------------------------------------------------------------------------------
-- wickets in each over 
SELECT CEIL(wicket_over), COUNT(*) 
FROM fall_of_wickets
GROUP BY CEIL(wicket_over), team_id
ORDER BY CEIL(wicket_over);


-- wickets lost in power play
SELECT team_name, COUNT(*) AS wickets_lost_in_powerplay
FROM fall_of_wickets AS fow
JOIN teams AS t ON fow.team_id = t.id
WHERE wicket_over<=6
GROUP BY team_id
ORDER BY COUNT(*);


-- wickets lost in death overs
SELECT team_name, COUNT(*) AS wickets_lost_in_powerplay
FROM fall_of_wickets AS fow
JOIN teams AS t ON fow.team_id = t.id
WHERE wicket_over>15
GROUP BY team_id
ORDER BY COUNT(*);
