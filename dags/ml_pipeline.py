# Create DAG that runs the following tasks
# Use the file from data folder to train a model

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import pandas as pd
import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression

# Python function to clean, train the model

# greet example task
def greet():
    print('Hello World')

def process_data(data):
    import pandas as pd

    # split into features and target (target is last column)
    X = data.drop(data.columns[-1], axis=1)
    y = data[data.columns[-1]]

    # split into categorical and numerical features
    categorical = X.select_dtypes(include=['object'])
    numerical = X.select_dtypes(exclude=['object'])

    # process categorical features
    categorical = process_categorical_df(categorical)

    # process numerical features
    numerical = process_numerical_df(numerical)

    # Assume no Nan rows in target

    return pd.concat([categorical, numerical, y], axis=1)

def process_categorical_df(df):
    import pandas as pd

    # Assume binary catergorical features
    # Fill Nan with Mode
    for col in df.columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df

def process_numerical_df(df):
    import pandas as pd
    import sklearn.preprocessing as preprocessing

    # Fill Nan with Mean
    for col in df.columns:
        df[col] = df[col].fillna(df[col].mean())

    # Scale
    scaler = preprocessing.StandardScaler()
    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    return df

def train_model(df):

    # split into features and target (target is last column)
    X = df.drop(df.columns[-1], axis=1)
    y = df[df.columns[-1]]

    # choose model and data
    x, model = choose_model(X, y)

    # count nan values
    print(y.isna().sum())

    # fit model
    model = fit_model(model, x, y)

    return model

def choose_model(X, y):
    import sklearn.linear_model as linear_model

    # if y is numerical
    if y.dtype in [np.int64, np.float64]:
        model = linear_model.LinearRegression()
        x = X.select_dtypes(exclude=['object'])
        print("Linear Regression")
    else:
        model = linear_model.LogisticRegression()
        x = X.select_dtypes(exclude=['object'])
        print("Logistic Regression")

    # can return set of models in future

    return x, model

def fit_model(model, X, y):
    # can implement CV here in future

    model.fit(X, y)

    return model

def test_model(model, test):
    import pandas as pd
    import numpy as np

    # process data
    test = process_data(test)

    # split into features and target (target is last column)
    X_test = test.drop(test.columns[-1], axis=1)
    y_test = test[test.columns[-1]]

    # test model
    if y_test.dtype in ['int64', 'float64']:
        y_pred = model.predict(X_test.select_dtypes(exclude=['object']))
        metric = get_metric(y_test, y_pred)
    else:
        y_pred = model.predict(X_test)
        metric = get_metric(y_test, y_pred)

    return metric

def get_metric(y_true, y_pred):
    from sklearn.metrics import mean_squared_error, accuracy_score

    if y_true.dtype in ['int64', 'float64']:
        return mean_squared_error(y_true, y_pred)
    else:
        return accuracy_score(y_true, y_pred)


## PIPELINE ##

# prepare data
def prepare_data():
    import pandas as pd

    # Load dataset
    data = pd.read_csv('data/data.csv')

    # Split into train and test
    train = data.sample(frac=0.8, random_state=200)
    test = data.drop(train.index)

    # Save train and test data
    train.to_csv('data/train.csv', index=False)
    test.to_csv('data/test.csv', index=False)

    print('Data loaded and split into train and test data')

def preprocess_train_data():
    data = pd.read_csv('data/train.csv')
    data = process_data(data)

    print("Data processed")

    # Save data
    data.to_csv('data/processed_train_data.csv', index=False)

def preprocess_test_data():
    data = pd.read_csv('data/test.csv')
    data = process_data(data)

    print("Data processed")

    # Save data
    data.to_csv('data/processed_test_data.csv', index=False)

def train_and_test_model():
    train_data = pd.read_csv('data/processed_train_data.csv')
    test_data = pd.read_csv('data/processed_test_data.csv')

    model = train_model(train_data)
    metric = test_model(model, test_data)

    print(f'Model tested with metric: {metric}')

    # Save model to /data
    # import joblib
    # joblib.dump(model, 'data/model.pkl')

    # print('Model saved')

    print(metric)

with DAG(
    default_args = {
        'owner': 'RCH4CKERS',
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    description='ML Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 6, 20),
    dag_id='ml_pipeline',
) as dag:
    # task1 = PythonOperator(
    #     task_id='greet',
    #     python_callable=greet
    # )

    prepare_data = PythonOperator(
        task_id='prepare_data',
        python_callable=prepare_data
    )

    preprocess_train_data = PythonOperator(
        task_id='preprocess_train_data',
        python_callable=preprocess_train_data
    )

    preprocess_test_data = PythonOperator(
        task_id='preprocess_test_data',
        python_callable=preprocess_test_data
    )

    train_and_test_model = PythonOperator(
        task_id='train_and_test_model',
        python_callable=train_and_test_model
    )

    prepare_data >> [preprocess_train_data, preprocess_test_data] >> train_and_test_model


    
