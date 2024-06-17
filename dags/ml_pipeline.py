# Create DAG that runs the following tasks
# Use the file from data folder to train a model
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Python function to clean, train the model
def prep_data():
    print('Data Preprocessing')
    # I want to read the csv file and do data cleaning only in this funciton
    # Read csv file
<<<<<<< HEAD
    df = pd.read_csv('data/data.csv')
    # Drop missing values
    df = df.dropna()
    # save the cleaned data to a new csv file
    df.to_csv('data/cleaned_data.csv', index=False)
=======
    # df = pd.read_csv('data/data.csv')
    # # Drop missing values
    # df = df.dropna()
>>>>>>> 210d77b (Fix dockerfile for apache airflow)
    # Split the data into features and target


def train_test_split():
    print('Train Test Split')
    # I want to split the data into train and test data only in this function


def train_model():
    print('Train Model')
    # I want to train the model only in this function


def predict_on_test_data():
    print('Predict on Test Data')
    # I want to predict on test data only in this function


def get_metrics():
    print('Get Metrics')
    # I want to get metrics only in this function


with DAG('ml_pipeline',
         description='Machine Learning Pipeline',
         schedule_interval='@daily',
         start_date=datetime(2024, 7, 17),
         catchup=False) as dag:
    
    prep_and_clean = PythonOperator(task_id="preparedata", python_callable=prep_data)
    split_data = PythonOperator(task_id="splitdata", python_callable=train_test_split)
    train_model = PythonOperator(task_id="trainmodel", python_callable=train_model)
    predict = PythonOperator(task_id="predict", python_callable=predict_on_test_data)
    get_metrics = PythonOperator(task_id="getmetrics", python_callable=get_metrics)

    prep_and_clean >> split_data >> train_model >> predict >> get_metrics