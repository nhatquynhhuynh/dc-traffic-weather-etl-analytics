#!/usr/bin/env python3
# Public portfolio copy; see README before executing.


# ## Project_2_ETL_HuynhNhatQuynh
# ### Section 1: Weather ETL
# ####   - Import libraries and set up
# ####  - Function to Fetch Weather
# ####  - Auto-Resume Downloader
# ### Section 2: Moving Violations ETL
# ####  - Setup
# ####  - Download Monthly CSVs
# ####  - Loop Automatically
# ####  - Combine All Monthly Files
# ### Section 3: Load into MySQL
# ####  - Connect to MySQL
# ####  - Load WEATHER Data into MySQL
# ####  - Load VIOLATIONS Data into MySQL

# # Section 1: Weather ETL

# ## 1.1 Import libraries and set up

import os, time, calendar, glob, requests
import pandas as pd
from datetime import date, timedelta

# ---- Visual Crossing setup ----
VC_API_KEY = os.environ["VISUAL_CROSSING_API_KEY"]
BASE_WEATHER = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Washington,DC"
os.makedirs("raw/weather", exist_ok=True)
MASTER_WEATHER = "raw/weather/DC_weather_since_Sep2024.csv"

# ## 1.2 Function to Fetch Weather

def fetch_weather_day(d):
    url = f"{BASE_WEATHER}/{d}?unitGroup=metric&key={VC_API_KEY}&contentType=json"
    r = requests.get(url, timeout=60)
    if r.ok:
        js = r.json()["days"][0]
        return {
            "weather_date": js["datetime"],
            "temp_min_c": js.get("tempmin"),
            "temp_max_c": js.get("tempmax"),
            "precipitation_mm": js.get("precip", 0)
        }
    else:
        print(f"{d} failed ({r.status_code})")
        return None

# ## 1.3 Auto-Resume Downloader

from datetime import date, timedelta

PROJECT_START = date(2024, 9, 1)
MAX_DAYS_PER_RUN = 30   # run in chunks

# Check if old file exists
if os.path.exists(MASTER_WEATHER):
    df_old = pd.read_csv(MASTER_WEATHER)
    df_old["weather_date"] = pd.to_datetime(df_old["weather_date"])
    last = df_old["weather_date"].max().date()
    start_date = last + timedelta(days=1)
    print(f"Existing file found. Last saved date: {last}")
else:
    df_old = None
    start_date = PROJECT_START
    print("No weather file found. Starting fresh.")

# Determine how far to download today
end_date = date.today() - timedelta(days=1)
hard_end = min(end_date, start_date + timedelta(days=MAX_DAYS_PER_RUN - 1))

print(f"\n Downloading weather {start_date} → {hard_end}")

rows = []
cur = start_date

while cur <= hard_end:
    try:
        rec = fetch_weather_day(cur)
        if rec:
            rows.append(rec)
            print(f"   ✔ {cur} added")
        else:
            print(f"   ⚠ {cur} returned no data")

        time.sleep(1.5)  # slow down to avoid burst limit

    except Exception as e:
        if "429" in str(e):
            print(f"\n Hit today's API limit at {cur} (429 Too Many Requests)")
            print(f" Progress saved up to: {cur - timedelta(days=1)}")
            break
        else:
            print(f"\n Error on {cur}: {e}")
            break

    cur += timedelta(days=1)

# Save new rows
if rows:
    df_new = pd.DataFrame(rows)

    # Append or write new file
    mode = "a" if os.path.exists(MASTER_WEATHER) else "w"
    header = not os.path.exists(MASTER_WEATHER)

    df_new.to_csv(MASTER_WEATHER, index=False, mode=mode, header=header)

    print(f"\n Added {len(df_new)} new rows to {MASTER_WEATHER}")

    # Show final range
    if df_old is not None:
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    
        # Convert entire column to datetime
        df_final["weather_date"] = pd.to_datetime(df_final["weather_date"], errors="coerce")
    
        print(f" Weather now covers: {df_final['weather_date'].min().date()} → {df_final['weather_date'].max().date()}")
    
    else:
        print(f" Weather now covers: {df_new['weather_date'].min().date()} → {df_new['weather_date'].max().date()}")

else:
    print("\nℹ No new weather downloaded.")



# # Section 2: Moving Violations ETL

# ## 2.1 Setup

import calendar
os.makedirs("raw/violations", exist_ok=True)
MASTER_VIOL = "raw/violations/DC_moving_violations_since_Sep2024.csv"


# ## 2.2 Download Monthly CSVs

def get_violation_url(y, m):
    monthname = calendar.month_name[m].lower()
    return f"https://opendata.dc.gov/datasets/DCGIS::moving-violations-issued-in-{monthname}-{y}.csv"

def fetch_violation_month(y, m):
    url = get_violation_url(y, m)
    fname = f"raw/violations/DC_moving_violations_{y}_{m:02d}.csv"
    if os.path.exists(fname):
        print(f"{fname} exists")
        return
    print(f"{calendar.month_name[m]} {y}")
    r = requests.get(url, timeout=180)
    if r.status_code == 200:
        with open(fname, "wb") as f:
            f.write(r.content)
        print(f"Saved {fname}")
    else:
        print(f" Missing {url}")


# ## 2.3 Loop Automatically

today = date.today()
for y in range(2024, today.year + 1):
    m_start = 9 if y == 2024 else 1
    m_end = today.month if y == today.year else 12
    for m in range(m_start, m_end + 1):
        fetch_violation_month(y, m)

# ## 2.4 Combine All Monthly Files

# -------------------------------------------------------
# 2.4 Combine ALL Monthly CSV Files
# -------------------------------------------------------

import pandas as pd
import glob

files = sorted(glob.glob("raw/violations/*.csv"))

print(f"Found {len(files)} monthly files. Combining...")

df_list = []
for f in files:
    print(" -", f)
    df_list.append(pd.read_csv(f, low_memory=False))

df_viol = pd.concat(df_list, ignore_index=True)

print(f"\nTotal rows BEFORE removing duplicates: {len(df_viol):,}")

# Remove duplicates based on OBJECTID
df_viol = df_viol.drop_duplicates(subset=["OBJECTID"])

print(f"Total rows AFTER removing duplicates: {len(df_viol):,}")
print(f"Combined {len(files)} months into final violations dataset.")

# Save combined file
output_path = "raw/violations/DC_moving_violations_since_Sep2024.csv"
df_viol.to_csv(output_path, index=False)

print(f"Saved final combined file: {output_path}")

import os

weather_path   = "raw/weather/DC_weather_since_Sep2024.csv"
violations_path = "raw/violations/DC_moving_violations_since_Sep2024.csv"

print("Weather CSV exists:", os.path.exists(weather_path), weather_path)
print("Violations CSV exists:", os.path.exists(violations_path), violations_path)


# # Note: Run SQL (01_Create_Tables_HuynhNhatQuynh.sql ) to recreate database structure before run the Section 3 below

# # Section 3: Load into MySQL

# ## 3.1 – Connect to MySQL

# ----------------------------------------
# SECTION 3.1 – Connect to MySQL Database
# ----------------------------------------

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import pandas as pd

MYSQL_USER = os.getenv("MYSQL_USER", "root")              
MYSQL_PWD = os.environ["MYSQL_PASSWORD"]      
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1:3306")
MYSQL_DB   = "dc_mv_weather"

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{quote_plus(MYSQL_PWD)}@{MYSQL_HOST}/{MYSQL_DB}"
)

# Test connection
with engine.connect() as conn:
    db_name = conn.execute(text("SELECT DATABASE();")).scalar()
    print("Connected to:", db_name)


# ## 3.2 – Load WEATHER Data into MySQL

# -----------------------------------------------------
# SECTION 3.2 – Load WEATHER CSV into weather_daily
# -----------------------------------------------------

weather_path = "raw/weather/DC_weather_since_Sep2024.csv"

# Read CSV
df_weather = pd.read_csv(weather_path)

# Convert date column
df_weather["weather_date"] = pd.to_datetime(df_weather["weather_date"], errors="coerce")

print("Weather rows:", len(df_weather))
df_weather.head()

# -----------------------------------------------------
# TRUNCATE the table (CLEAR OLD DATA)
# -----------------------------------------------------

# Clear existing data before reloading
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE weather_daily;"))
    print("Cleared weather_daily table.")

# -----------------------------------------------------
# Load new weather rows
# -----------------------------------------------------

# Load data into MySQL
df_weather.to_sql(
    "weather_daily",
    con=engine,
    if_exists="append",
    index=False
)

print("Loaded", len(df_weather), "rows into weather_daily.")


# ## 3.3 – Load VIOLATIONS Data into MySQL

# -------------------------------------------------------
# SECTION 3.3 – Load VIOLATIONS CSV into violations table
# -------------------------------------------------------

violations_path = "raw/violations/DC_moving_violations_since_Sep2024.csv"

df_viol = pd.read_csv(violations_path, low_memory=False)

print("Initial violation rows loaded from CSV:", len(df_viol))
print("Columns detected:", df_viol.columns.tolist())

# -------------------------------------------------------
# Convert date & datetime fields
# -------------------------------------------------------

# Remove timezone and fix formatting
dt_cols = ["ISSUE_DATE", "DISPOSITION_DATE", "GIS_LAST_MOD_DTTM"]

for col in dt_cols:
    if col in df_viol.columns:
        df_viol[col] = (
            df_viol[col]
            .astype(str)
            .str.replace(r"\+.*$", "", regex=True)      # remove +00 timezone
            .str.replace("/", "-", regex=False)         # replace slashes with dashes
        )
        df_viol[col] = pd.to_datetime(df_viol[col], errors="coerce")

# -------------------------------------------------------
# Convert numeric fields safely
# -------------------------------------------------------

num_cols = [
    "OBJECTID", "XCOORD", "YCOORD", "FINE_AMOUNT", "FINE_REDUCTION_AMT",
    "PENALTY_1_REDUCED_AMT", "PENALTY_2_REDUCED_AMT", "PENALTY_3_REDUCED_AMT",
    "PENALTY_1_AMT", "PENALTY_2_AMT", "PENALTY_3_AMT",
    "TOTAL_AMT_PAID", "AMT_DUE", "LATITUDE", "LONGITUDE", "MAR_ID"
]

for col in num_cols:
    if col in df_viol.columns:
        df_viol[col] = pd.to_numeric(df_viol[col], errors="coerce")

# -------------------------------------------------------
# Drop duplicate OBJECTID rows
# -------------------------------------------------------

before = len(df_viol)
df_viol = df_viol.drop_duplicates(subset=["OBJECTID"], keep="last")
after = len(df_viol)

print(f"Rows BEFORE dropping duplicates: {before:,}")
print(f"Rows AFTER dropping duplicates:  {after:,}")
print(f"Duplicate rows removed: {before - after:,}")

# -------------------------------------------------------
# TRUNCATE violations table
# -------------------------------------------------------

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE violations;"))
    print("Cleared violations table.")

# -------------------------------------------------------
# Load Violations into MySQL
# -------------------------------------------------------

df_viol.to_sql(
    "violations",
    con=engine,
    if_exists="append",
    index=False
)

print(f"Loaded {after:,} rows into violations.")



