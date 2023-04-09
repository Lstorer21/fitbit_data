#Import the DAG Object
from airflow.models import DAG
from datetime import datetime


# Define the default_args dictionary
default_args = {
    'owner' : 'Lance',
    'start_date' : datetime(2023,4,8),
    'retries' : 2,
    'schedule_interval' : '@weekly'
}

#Instantiate DAGS
sleep_api_dag = DAG('Sleep_API_DAG', default_args=default_args)
heart_rate_api_dag = DAG('Heart_Rate_API_DAG', default_args=default_args)

#Set  heart_rate_api_dag to run before sleep_api
heart_rate_api_dag >> sleep_api_dag
