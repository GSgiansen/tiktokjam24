# Create DAG that runs the following tasks
# Use the file from data folder to train a model

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Helper functions

def remove_whitespace(df):
    """Remove leading and trailing whitespace from all string columns."""
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.strip()
    return df

def remove_duplicates(df):
    """Remove duplicate rows from data."""
    return df.drop_duplicates()

def separate_nan_target(df):
    """Separate rows with NaN values in the target column."""
    target_col = df.columns[-1]
    
    data_with_target = df.dropna(subset=[target_col])
    data_without_target = df[df[target_col].isna()]
    
    data_with_target.to_csv('data/data_with_target.csv', index=False)
    data_without_target.to_csv('data/data_without_target.csv', index=False)
    
    print(f"Rows with target: {len(data_with_target)}")
    print(f"Rows without target: {len(data_without_target)}")

    return data_with_target

def process_data(data):
    """Preprocess features and target columns separately for training"""
    import pandas as pd

    # remove whitespace
    data = remove_whitespace(data)

    # remove duplicates
    data = remove_duplicates(data)

    # separate nan rows in target
    data = separate_nan_target(data)

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

    process_data = pd.concat([categorical, numerical, y], axis=1)
    process_data = process_data.dropna()

    return process_data

def process_categorical_df(df):
    """Fill Nan values with mode for categorical features"""
    import pandas as pd

    for col in df.columns:
        # Check if the column has a mode
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            # If no mode exists, fill with a placeholder value
            df[col] = df[col].fillna('Unknown')

    return df

def process_numerical_df(df):
    """Fill Nan values with mean and scale numerical features"""
    import pandas as pd
    import sklearn.preprocessing as preprocessing

    for col in df.columns:
            # Convert column to numeric, coercing errors to NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Replace infinite values with NaN
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
            
            # Calculate mean, ignoring NaN values
            col_mean = df[col].mean()
            
            if pd.isna(col_mean):
                # If mean is NaN (all values are NaN), fill with 0
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna(col_mean)

    # Scale
    scaler = preprocessing.StandardScaler()
    scaled_df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    return scaled_df

def train_model(df):
    """Train model on preprocessed data"""
    # split into features and target (target is last column)
    X = df.drop(df.columns[-1], axis=1)
    y = df[df.columns[-1]]

    # choose model and data
    x, model = choose_model(X, y)

    # fit model
    model = fit_model(model, x, y)

    return model

def choose_model(X, y):
    """Choose model based on target type"""
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
    """Fit model to data"""

    # can implement CV here in future

    model.fit(X, y)

    return model

def test_model(model, test):
    """Test trained model on test data and return metric"""
    import pandas as pd
    import numpy as np

    # process data
    test = process_data(test)

    # split into features and target (target is last column)
    X_test = test.drop(test.columns[-1], axis=1)
    y_test = test[test.columns[-1]]

    # test model
    if y_test.dtype in [np.int64, np.float64]:
        y_pred = model.predict(X_test.select_dtypes(exclude=['object']))
        metric = get_metric(y_test, y_pred)
    else:
        y_pred = model.predict(X_test.select_dtypes(exclude=['object']))
        metric = get_metric(y_test, y_pred)

    return metric

def get_metric(y_true, y_pred):
    """Return metric based on target type"""

    from sklearn.metrics import mean_squared_error, accuracy_score

    if y_true.dtype in ['int64', 'float64']:
        return mean_squared_error(y_true, y_pred)
    else:
        return accuracy_score(y_true, y_pred)
    
    # can implement more metrics in future


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
    import joblib
    joblib.dump(model, 'data/model.pkl')

    print('Model saved')

    print(metric)

def predict():
    # Load model
    import joblib
    model = joblib.load('data/model.pkl')

    # Load predict data
    data = pd.read_csv('data/predict.csv')

    # Process data
    data = process_data(data)

    # Make predictions
    X = data.drop(data.columns[-1], axis=1)
    predictions = model.predict(X.select_dtypes(exclude=['object']))

    # Save predictions to the same file
    data['predictions'] = predictions
    data.to_csv('data/predict.csv', index=False)

    print('Predictions saved')

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
    start = DummyOperator(task_id='start')

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

    end = DummyOperator(task_id='end')

    start >> \
    prepare_data >> \
    [preprocess_train_data, preprocess_test_data] >> \
    train_and_test_model >> \
    end


    
