-- -----------------------------------------
-- 01_Create_Tables.sql
-- -----------------------------------------

# 1.1 Create database
CREATE DATABASE IF NOT EXISTS dc_mv_weather;
USE dc_mv_weather;

# 1.2 Drop existing tables
DROP TABLE IF EXISTS weather_daily;
DROP TABLE IF EXISTS violations;

-- -----------------------------------------
-- weather_daily
CREATE TABLE weather_daily (
    weather_date DATE PRIMARY KEY,
    temp_min_c DECIMAL(5,2),
    temp_max_c DECIMAL(5,2),
    precipitation_mm DECIMAL(7,2)
);

-- -----------------------------------------
-- violations
CREATE TABLE violations (
    OBJECTID INT PRIMARY KEY,
    LOCATION VARCHAR(255),
    XCOORD DECIMAL(12,4),
    YCOORD DECIMAL(12,4),

    ISSUE_DATE DATETIME,
    ISSUE_TIME VARCHAR(10),

    ISSUING_AGENCY_CODE VARCHAR(10),
    ISSUING_AGENCY_NAME VARCHAR(255),
    ISSUING_AGENCY_SHORT VARCHAR(50),

    VIOLATION_CODE VARCHAR(50),
    VIOLATION_PROCESS_DESC VARCHAR(500),

    PLATE_STATE VARCHAR(10),
    ACCIDENT_INDICATOR VARCHAR(5),

    DISPOSITION_CODE INT,
    DISPOSITION_TYPE VARCHAR(100),
    DISPOSITION_DATE DATETIME,

    FINE_AMOUNT DECIMAL(10,2),
    TOTAL_PAID DECIMAL(10,2),

    PENALTY_1 DECIMAL(10,2),
    PENALTY_2 DECIMAL(10,2),
    PENALTY_3 DECIMAL(10,2),
    PENALTY_4 DECIMAL(10,2),
    PENALTY_5 DECIMAL(10,2),

    RP_MULT_OWNER_NO INT,
    BODY_STYLE VARCHAR(50),

    LATITUDE DECIMAL(10,6),
    LONGITUDE DECIMAL(10,6),

    MAR_ID INT,
    GIS_LAST_MOD_DTTM DATETIME
);
