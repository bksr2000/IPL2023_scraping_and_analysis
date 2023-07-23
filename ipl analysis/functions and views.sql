-- FUNCTIONS -------------------------------------------------------------------------------------
DELIMITER $$
CREATE FUNCTION innings(id INT)  -- returns innings played to calculate average(number of times out or else 1)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE innings INT;
 
	IF (SELECT count(*) as outs FROM batting_stats WHERE batter_id = id AND out_or_notout!='Not out') >= 1 THEN
		SET innings = (SELECT count(*) FROM batting_stats WHERE batter_id = id) 
			- (SELECT count(*) as outs FROM batting_stats WHERE batter_id = id AND out_or_notout='Not out');
	ELSE 
		SET innings = 1;
	END IF;
		RETURN innings;
END $$
DELIMITER ;



-- VIEWS ------------------------------------------------------------------------------------------------------------
CREATE VIEW wickets_taken AS   -- wickets taken by teams
SELECT match_date, team1_id AS team_id, team2_wickets AS wickets FROM match_result
UNION
SELECT match_date, team2_id, team1_wickets FROM match_result
order by match_date;