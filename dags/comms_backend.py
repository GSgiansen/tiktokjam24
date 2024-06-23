# Description: Communication with local fastapi backend to print data


from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import numpy as np
import pandas as pd


def fetch_data():
    response = requests.get("http://host.docker.internal:8000/classification_models/classification_model")
    data = response.json()
    print("data is", data)
    return data

args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 23),
}


with DAG(dag_id='comms_backend', default_args=args, schedule_interval='@daily') as dag:
    start = DummyOperator(task_id='start')

    fetch_data = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data
    )

    end = DummyOperator(task_id='end')

    start >> fetch_data >> end