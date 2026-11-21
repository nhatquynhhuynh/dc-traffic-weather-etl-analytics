-- -----------------------------------------
-- 02_Analysis_Queries.sql
-- -----------------------------------------

USE dc_mv_weather;

# Verify Data in MySQL
SELECT * FROM weather_daily;
SELECT MIN(weather_date), MAX(weather_date) FROM weather_daily;

SELECT * FROM violations;
SELECT MIN(ISSUE_DATE), MAX(ISSUE_DATE) FROM violations;


# a. List every agency that issued moving violations for each month
SELECT 
    YEAR(ISSUE_DATE) AS violation_year,
    MONTH(ISSUE_DATE) AS violation_month,
    ISSUING_AGENCY_NAME
FROM violations
WHERE ISSUE_DATE IS NOT NULL
GROUP BY 
    YEAR(ISSUE_DATE),
    MONTH(ISSUE_DATE),
    ISSUING_AGENCY_NAME
ORDER BY 
    violation_year,
    violation_month,
    ISSUING_AGENCY_NAME;


# b. How many tickets have been issued since October 1, 2024?
SELECT COUNT(*) AS total_tickets
FROM violations
WHERE ISSUE_DATE >= '2024-10-01';


# c. Average number of tickets issued by day of the week
SELECT 
    DAYNAME(ISSUE_DATE) AS weekday,
    COUNT(*) / COUNT(DISTINCT DATE(ISSUE_DATE)) AS avg_tickets_per_day
FROM violations
GROUP BY weekday
ORDER BY FIELD(weekday,
    'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');


# d. How many tickets were issued during periods of rain?
SELECT COUNT(*)
FROM violations v, weather_daily w
WHERE DATE(v.ISSUE_DATE) = w.weather_date
  AND w.precipitation_mm > 0;


# e. Total precipitation for each month
SELECT 
    DATE_FORMAT(weather_date, '%Y-%m') AS month,
    SUM(precipitation_mm) AS total_precipitation_mm
FROM weather_daily
GROUP BY DATE_FORMAT(weather_date, '%Y-%m')
ORDER BY month;


# f. Total fines per month for >10 mph speeding violations
SELECT
    DATE_FORMAT(ISSUE_DATE, '%Y-%m') AS month,
    SUM(FINE_AMOUNT) AS total_fines
FROM violations
WHERE VIOLATION_CODE IN ('T119','T120','T121','T122','T123','T124','T125')
GROUP BY DATE_FORMAT(ISSUE_DATE, '%Y-%m')
ORDER BY month;


# g. Average tickets per hour of the day
SELECT 
    FLOOR(ISSUE_TIME / 100) AS hour_of_day,
    COUNT(*) / COUNT(DISTINCT DATE(ISSUE_DATE)) AS avg_tickets_per_hour
FROM violations
GROUP BY hour_of_day
ORDER BY hour_of_day;


# h. Compare accident tickets on rainy vs non-rainy days
SELECT 
    CASE 
        WHEN w.precipitation_mm > 0 THEN 'Rainy Day'
        ELSE 'Non-Rainy Day'
    END AS day_type,
    COUNT(*) AS accident_tickets
FROM violations v
JOIN weather_daily w
    ON DATE(v.ISSUE_DATE) = w.weather_date
WHERE v.ACCIDENT_INDICATOR = 'Y'
GROUP BY day_type;
