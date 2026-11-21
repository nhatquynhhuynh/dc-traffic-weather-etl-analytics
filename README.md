# DC Traffic Violations & Weather Analytics

**Python | Pandas | MySQL | SQLAlchemy | ETL | SQL**

## Project Overview

The objective was to build an automated ETL (Extract, Transform, Load) pipeline integrating Washington, DC traffic violation records with historical weather data to investigate traffic patterns, fine amounts, and the potential relationship between weather conditions and traffic violations.

The project combines Python-based data processing, relational database design, and SQL analytics.

## Project Highlights

- **2.47 Million Records:** Processed and loaded 2,475,473 unique traffic violation records into MySQL.
- **Automated ETL Pipeline:** Developed Python workflows to retrieve, clean, and consolidate data from multiple sources.
- **Database Development:** Designed relational tables and integrated datasets using MySQL and SQLAlchemy.
- **SQL Analytics:** Analyzed traffic violations by time, issuing agency, fine amounts, and weather conditions.
- **Incremental Data Collection:** Implemented automated data retrieval that skips previously downloaded files and supports continued data collection.

*Record count reflects the original academic project results.*

## Data Sources

| Source | Data | Description |
|---|---|---|
| DC Open Data | Moving Violations | Traffic citations, issuing agencies, violations, and fines |
| Visual Crossing API | Historical Weather | Daily temperature and precipitation data |

## ETL Workflow

The project follows five main stages:

1. **Extract:** Retrieve monthly traffic violation records from DC Open Data and daily weather information through the Visual Crossing API.
2. **Transform:** Clean missing values, standardize date and numeric fields, and remove duplicate records.
3. **Consolidate:** Combine monthly files into structured datasets for analysis.
4. **Load:** Transfer cleaned records into MySQL using Python, pandas, and SQLAlchemy.
5. **Analyze:** Execute SQL queries to investigate traffic patterns and relationships with weather conditions.

### Data Pipeline

`DC Open Data + Visual Crossing API → Python & Pandas → MySQL → SQL Analysis`

## Database Design

The database contains two main tables:

- **weather_daily:** Historical daily weather observations, including minimum temperature, maximum temperature, and precipitation.
- **violations:** Traffic violation records, including citation dates, issuing agencies, violation codes, fines, and geographic information.

The datasets are connected analytically through their corresponding dates.

### Entity Relationship Diagram

![Database ERD](assets/database-erd.png)

## SQL Analysis

The project includes SQL queries addressing questions such as:

- Which agencies issued traffic citations each month?
- How does ticket volume vary across weekdays and hours?
- How many citations were issued on rainy days?
- What were the monthly totals of speeding-related fines?
- How do accident-related citations differ between rainy and non-rainy days?

## Technologies Used

| Technology | Application |
|---|---|
| Python | Data extraction, transformation, and automation |
| Pandas | Data cleaning, consolidation, and processing |
| MySQL | Database design, storage, and querying |
| SQLAlchemy | Python-to-MySQL integration |
| SQL | Data analysis and reporting |
| Jupyter Notebook | ETL development and documentation |

## Repository Structure

| File | Description |
|---|---|
| `Project2_ETL.ipynb` | Python ETL notebook |
| `Project2_ETL.py` | Python ETL script |
| `01_Create_Tables_HuynhNhatQuynh.sql` | MySQL database schema |
| `02_Analysis_Queries_HuynhNhatQuynh.sql` | SQL analysis queries |
| `assets/database-erd.png` | Database relationship diagram |
| `requirements.txt` | Python dependencies |
| `.env.example` | Example configuration for local execution |

## How to Run

1. Install Python, MySQL, and the required dependencies using `pip install -r requirements.txt`.
2. Configure the environment variables described in `.env.example`.
3. Execute `01_Create_Tables_HuynhNhatQuynh.sql` to create the database tables.
4. Run the Python ETL notebook or script to collect, process, and load the data.
5. Execute `02_Analysis_Queries_HuynhNhatQuynh.sql` to explore the results.

**Note:** Run the project in a dedicated test database because the setup and loading scripts replace existing table contents. External data sources may change or impose API limits.

## Data Availability & Security

The project uses DC Open Data and historical weather information obtained through the Visual Crossing API.

Raw datasets are not included in this repository. The code has been adapted for public sharing by replacing embedded credentials with environment variables. The original analytical workflow and SQL queries are retained.
