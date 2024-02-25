# Fitbit Data Analytics Project

## Overview

This project involves extracting heart rate and sleep data from Fitbit's API using Python, transforming the data, and loading it into a PostgreSQL database. The data is then visualized using Power BI to create a dashboard showcasing the results.

## Project Structure

- Heart_Rate_API.py: Python script for extracting heart rate and sleep data from Fitbit's API.

-	Sleep_API_Call.py: Python script for transforming the extracted data.

-	API_dags.py: Python script utilizing Apache Airflow to create DAG’s to execute Heart_Rate_API.py and Sleep_API_Call.py daily.

-	Fitbit_Dashboard.pbix: Power BI file containing the dashboard visualizations.
  
## Dependencies

- Python 3.11.2

  - Requests 
 
  - Pandas 

  -	Datetime

  -	Time

  -	sqlalchemy

  -	Airflow

  -	re

- PostgreSQL

- Power BI Desktop

  -	Tabular Editor 2

