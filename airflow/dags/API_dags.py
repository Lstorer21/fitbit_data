#Import the DAG Object
from airflow.models import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

# Define the default_args dictionary
default_args = {
    'owner' : 'Lance',
    'start_date' : datetime(2023,4,16),
    'retries' : 2,
    'schedule_interval' : '@daily'
}

#Instantiate DAGS
fitbit_dag = DAG('Fitbit_Dag', default_args=default_args)


#Define the BashOperator
t1 = BashOperator(
    task_id= 'heart_rate_api',
    #Define the bash command
    bash_command='python /home/data/Data_Science/fitbit_data/Heart_Rate_API.py',
    #Add the task to the dag
    dag=fitbit_dag
)
#Define the BashOperator
t2 = BashOperator(
    task_id= 'sleep_api',
    #Define the bash command
    bash_command='python /home/data/Data_Science/fitbit_data/Sleep_API_Call.py',
    #Add the task to the dag
    dag=fitbit_dag
)

# #Set  heart_rate_api_dag to run before sleep_api
t1 >> t2