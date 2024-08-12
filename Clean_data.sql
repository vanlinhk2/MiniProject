select TOP (1000) *
  from [test].[dbo].[Crawed]

select COUNT(DISTINCT [Link])
from [test].[dbo].[Crawed]

select 
    COLUMN_NAME, 
    DATA_TYPE, 
    CHARACTER_MAXIMUM_LENGTH, 
    IS_NULLABLE
from 
    INFORMATION_SCHEMA.COLUMNS
where 
    TABLE_NAME = 'Crawed';


--Change type of some columns
declare @sql NVARCHAR(MAX) = '';
select @sql = @sql + 'ALTER TABLE [test].[dbo].[Crawed] ALTER COLUMN ' 
    + COLUMN_NAME + ' FLOAT; ' + CHAR(13)
from INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME = 'Crawed'
  AND DATA_TYPE = 'tinyint';
exec sp_executesql @sql;



--Delete duplicate
with CTE AS (
	select *,
			ROW_NUMBER() OVER(PARTITION BY Link ORDER BY (select 0)) AS rn
	from [test].[dbo].[Crawed]
)
delete from CTE where rn>1;

--Clean Age, Height_cm, Weight_kg column 
--PATINDEX : Find first character is not number 
update [test].[dbo].[Crawed]
	set 
		Age = SUBSTRING(Age, 1, PATINDEX('%[^0-9]%', Age)-1)
	where 
		PATINDEX('%[^0-9]%', Age)>0;
update [test].[dbo].[Crawed]
	set 
		Height_cm = SUBSTRING(Height_cm, 1, PATINDEX('%[^0-9]%', Height_cm)-1)
	where 
		PATINDEX('%[^0-9]%', Height_cm)>0;
update [test].[dbo].[Crawed]
	set 
		Weight_kg = SUBSTRING(Weight_kg, 1, PATINDEX('%[^0-9]%', Weight_kg)-1)
	where 
		PATINDEX('%[^0-9]%', Weight_kg)>0;
--Clean Value and Wage column, change to Float
update [test].[dbo].[Crawed]
	set Value =
			CASE
				WHEN Value LIKE '%M' THEN CAST(REPLACE(REPLACE(Value, '€', ''), 'M', '') AS FLOAT) * 1000000
				ELSE CAST(REPLACE(Value, '€', '') AS FLOAT)
			END;
update [test].[dbo].[Crawed]
	set Wage =
			CASE
				WHEN Wage LIKE '%K' THEN CAST(REPLACE(REPLACE(Wage, '€', ''), 'K', '') AS FLOAT) * 1000
				ELSE CAST(REPLACE(Wage, '€', '') AS FLOAT)
			END;

ALTER TABLE [test].[dbo].[Crawed]
DROP COLUMN Crossing_1, Finishing_1, Heading_accuracy_1, Short_passing_1, Volleys_1, Height_ft_in, Weight_lbs

--Create new feature and caculator
ALTER TABLE [test].[dbo].[Crawed]
ADD 
	Avg_PAC FLOAT,
	Avg_SHO Float,
	Avg_PAS FLOAT,
	Avg_DRI FLOAT,
	Avg_DEF FLOAT,
	Avg_PHY FLOAT,
	Avg_Goalkeeping FLOAT;
update [test].[dbo].[Crawed]
	set 
		Avg_PAC = (ISNULL(Sprint_speed,0) + ISNULL(Acceleration, 0)) / 2.0, 
		Avg_SHO = (ISNULL(Finishing,0) + ISNULL(Att_Position, 0) + ISNULL(Shot_power, 0) + ISNULL(Long_shots, 0) + ISNULL(Penalties, 0) + ISNULL(Volleys, 0)) / 6.0 ,
		Avg_PAS = (ISNULL(Vision,0) + ISNULL(Crossing,0) + ISNULL(FK_Accuracy,0) + ISNULL(Long_passing,0) + ISNULL(Short_passing,0) + ISNULL(Curve,0)) /6.0,
		Avg_DRI = (ISNULL(Agility,0) + ISNULL(Balance,0) + ISNULL(Reactions,0) + ISNULL(Composure,0) + ISNULL(Ball_control,0) + ISNULL(Dribbling,0)) /6.0,
		Avg_DEF = (ISNULL(Interceptions,0) + ISNULL(Heading_accuracy,0) + ISNULL(Defensive_awareness,0) + ISNULL(Standing_tackle,0) + ISNULL(Sliding_tackle,0)) /5.0,
		Avg_PHY = (ISNULL(Jumping,0) + ISNULL(Stamina,0) + ISNULL(Strength,0) + ISNULL(Aggression,0)) /4.0,
		Avg_Goalkeeping = (ISNULL(GK_Diving,0) + ISNULL(GK_Handling,0) + ISNULL(GK_Kicking,0) + ISNULL(GK_Positioning,0) + ISNULL(GK_Reflexes,0)) /5.0;
-- Round to INT
update [test].[dbo].[Crawed]
set 
    Avg_PAC = ROUND(Avg_PAC, 0),
    Avg_SHO = ROUND(Avg_SHO, 0),
    Avg_PAS = ROUND(Avg_PAS, 0),
    Avg_DRI = ROUND(Avg_DRI, 0),
    Avg_DEF = ROUND(Avg_DEF, 0),
    Avg_PHY = ROUND(Avg_PHY, 0),
    Avg_Goalkeeping = ROUND(Avg_Goalkeeping, 0);

ALTER TABLE [test].[dbo].[Crawed]
ADD 
    Avg_Attacking FLOAT,
    Avg_Skill FLOAT,
    Avg_Movement FLOAT,
    Avg_Power FLOAT,
    Avg_Mentality FLOAT,
    Avg_Defending FLOAT;

update [test].[dbo].[Crawed]
	set 
		Avg_Attacking = (ISNULL(Crossing, 0) + ISNULL(Finishing, 0) + ISNULL(Heading_accuracy, 0) + ISNULL(Short_passing, 0) + ISNULL(Volleys, 0)) / 5.0,
		Avg_Skill = (ISNULL(Dribbling, 0) + ISNULL(Curve, 0) + ISNULL(FK_Accuracy, 0) + ISNULL(Long_passing, 0) + ISNULL(Ball_control, 0)) / 5.0,
		Avg_Movement = (ISNULL(Acceleration, 0) + ISNULL(Sprint_speed, 0) + ISNULL(Agility, 0) + ISNULL(Reactions, 0) + ISNULL(Balance, 0)) / 5.0,
		Avg_Power = (ISNULL(Shot_power, 0) + ISNULL(Jumping, 0) + ISNULL(Stamina, 0) + ISNULL(Strength, 0) + ISNULL(Long_shots, 0)) / 5.0,
		Avg_Mentality = (ISNULL(Aggression, 0) + ISNULL(Interceptions, 0) + ISNULL(Att_Position, 0) + ISNULL(Vision, 0) + ISNULL(Penalties, 0) + ISNULL(Composure, 0)) / 6.0,
		Avg_Defending = (ISNULL(Defensive_awareness, 0) + ISNULL(Standing_tackle, 0) + ISNULL(Sliding_tackle, 0)) / 3.0;
update [test].[dbo].[Crawed]
	set 
		Avg_Attacking = ROUND(Avg_Attacking, 0),
		Avg_Skill = ROUND(Avg_Skill, 0),
		Avg_Movement = ROUND(Avg_Movement, 0),
		Avg_Power = ROUND(Avg_Power, 0),
		Avg_Mentality = ROUND(Avg_Mentality, 0),
		Avg_Defending = ROUND(Avg_Defending, 0);
