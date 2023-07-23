-- most runs by a player
SELECT p.player_name, sum(runs) AS runs_made FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
GROUP BY batter_id 
ORDER BY sum(runs) DESC 
LIMIT 10;

-- most runs in an innings
SELECT p.player_name, runs, balls, strike_rate AS runs_made FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
ORDER BY runs DESC, strike_rate DESC 
LIMIT 10;


-- highest strike rate all matches
SELECT p.player_name, ROUND((sum(runs) * 100)/sum(balls), 2) AS strike_rate FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
GROUP BY batter_id 
HAVING COUNT(*)>=7 AND SUM(balls)>=100  -- condition: minimum 7 matches and 100 balls faced(comment it to see for no conditions)
ORDER BY strike_rate DESC
LIMIT 10;


-- highest strike rate in one innings(no conditions)
SELECT p.player_name, strike_rate FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
ORDER BY strike_rate DESC, sixes DESC, fours DESC
LIMIT 10;


-- player faces most balls totally
SELECT p.player_name, sum(balls) AS balls_faced FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
GROUP BY batter_id 
ORDER BY balls_faced DESC 
LIMIT 5;



-- centurians(made atleast one century)
SELECT DISTINCT p.player_name AS centurians FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
WHERE runs>=100;


-- most 50s
SELECT p.player_name, COUNT(*) AS 50s_made FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
WHERE bs.runs >= 50 AND bs.runs < 100
GROUP BY batter_id 
ORDER BY COUNT(*) DESC, sum(runs) DESC 
LIMIT 10;


-- most 6s
SELECT p.player_name, sum(sixes) AS sixes_hit FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
GROUP BY batter_id 
ORDER BY sum(sixes) DESC 
LIMIT 10;


-- most 6s in one innings
SELECT p.player_name, sixes AS sixes_hit FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
ORDER BY sixes DESC, runs DESC
LIMIT 10;


-- most 4s
SELECT p.player_name, sum(fours) AS fours_hit FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
GROUP BY batter_id 
ORDER BY sum(fours) DESC 
LIMIT 10;


-- most 4s in one innings
SELECT p.player_name, fours AS fours_hit FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
ORDER BY fours DESC, runs DESC
LIMIT 10;


-- most boundaries
SELECT batter_id, p.player_name, sum(sixes)+SUM(fours) AS boundaries_hit FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
GROUP BY batter_id 
ORDER BY boundaries_hit DESC 
LIMIT 10;


-- highest average(no conditions) 
SELECT p.player_name,ROUND(SUM(runs)/innings(batter_id), 2) AS average FROM batting_stats AS bs
JOIN players AS p ON bs.batter_id = p.id
GROUP BY batter_id
ORDER BY average 
DESC LIMIT 10;
