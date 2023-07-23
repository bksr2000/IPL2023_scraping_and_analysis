-- most wickets
SELECT bowler_id, p.player_name,sum(wickets) 
FROM bowling_stats AS bs
JOIN players AS p ON bs.bowler_id = p.id
GROUP BY bowler_id
ORDER BY sum(wickets) DESC, (6 * sum(runs))/sum((floor(overs)*6) + (MOD(overs, 1)*10))  -- checking economy if wickets are equal
LIMIT 10;


-- most overs bowled
SELECT p.player_name,round(((sum((floor(overs)*6)))/6) + floor(sum((mod(overs, 1)*10))/6) + (round(mod((sum((mod(overs, 1)*10))), 6))/10), 1) as overs_bowled-- -----------------------------------------------------
FROM bowling_stats AS bs
JOIN players AS p ON bs.bowler_id = p.id
GROUP BY bowler_id 
ORDER BY overs_bowled DESC
LIMIT 10;


-- average of bowler
SELECT p.player_name,
	CASE WHEN sum(wickets)>0 
        THEN round(sum(runs)/sum(wickets), 2)
	ELSE 0
	END as average
FROM bowling_stats AS bs
JOIN players AS p ON bs.bowler_id = p.id
GROUP BY bowler_id HAVING sum(wickets)>0
ORDER BY average
LIMIT 10;


-- strike rate of bowler
SELECT p.player_name,
	CASE WHEN sum(wickets)>0 
		THEN round(round((sum(floor(overs)*6)) + (sum((mod(overs, 1)*10))))/sum(wickets), 2)
	ELSE 0
	END as strike_rate
FROM bowling_stats AS bs
JOIN players AS p ON bs.bowler_id = p.id
GROUP BY bowler_id HAVING sum(wickets)>0
ORDER BY strike_rate, SUM(runs) DESC
LIMIT 10;


-- best economy(bowled atleast one full over)
SELECT p.player_name, round((6 * sum(runs))/(sum((floor(overs)*6) + (mod(overs, 1)*10))), 2) AS economy
FROM bowling_stats AS bs
JOIN players AS p ON bs.bowler_id = p.id
GROUP BY bowler_id HAVING sum(overs) >= 1
ORDER BY economy, sum(overs) DESC
LIMIT 10;


-- best economy in an innings (atleast bowled 2 full over)
SELECT p.player_name, economy FROM bowling_stats AS bs
JOIN players AS p ON bs.bowler_id = p.id
WHERE overs >= 2
ORDER BY economy, wickets DESC
LIMIT 5;


-- best economy in an innings (complete 4 overs bowled)
SELECT p.player_name, economy FROM bowling_stats AS bs
JOIN players AS p ON bs.bowler_id = p.id
WHERE overs = 4
ORDER BY economy
LIMIT 5;


-- best bowling figures
SELECT p.player_name, CONCAT(wickets, '/', runs) AS bowling_figures
from bowling_stats as bs
JOIN players AS p ON bs.bowler_id = p.id
ORDER BY wickets DESC, runs
LIMIT 10; 


-- players with 5 wicket hauls
SELECT DISTINCT p.player_name AS 5_wicket_hauls
FROM bowling_stats AS bs
JOIN players AS p ON bs.bowler_id = p.id
WHERE wickets>=5;


-- most runs conceded 
SELECT p.player_name, sum(runs) AS runs_conceded
from bowling_stats as bs
JOIN players AS p ON bs.bowler_id = p.id
GROUP BY bowler_id
ORDER BY runs_conceded DESC
LIMIT 10;


-- most runs conceded in an innings
SELECT p.player_name, runs AS runs_conceded
from bowling_stats as bs
JOIN players AS p ON bs.bowler_id = p.id
ORDER BY runs_conceded DESC, overs DESC
LIMIT 10;


-- maiden overs bowled
SELECT p.player_name, sum(maidens) AS maidens_overs, sum(overs) AS total_overs
from bowling_stats as bs
JOIN players AS p ON bs.bowler_id = p.id
GROUP BY bowler_id
ORDER BY maidens_overs DESC, sum(overs), sum(runs)
LIMIT 10;