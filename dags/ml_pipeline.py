# Create DAG that runs the following tasks
# Use the file from data folder to train a model

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import io
import os
import tempfile
import joblib
from backend.db import get_supabase_client
import sklearn.preprocessing as preprocessing
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif, f_regression

supabase = get_supabase_client()

# Helper functions

def remove_whitespace(df):
    """Remove leading and trailing whitespace from all string columns."""
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.strip()
    return df

def remove_duplicates(df):
    """Remove duplicate rows from data."""
    return df.drop_duplicates()

def separate_nan_target(df, target_col):
    """Separate rows with NaN values in the target column."""
    
    data_with_target = df.dropna(subset=[target_col])
    data_without_target = df[df[target_col].isna()]
    
    print(f"Rows with target: {len(data_with_target)}")
    print(f"Rows without target: {len(data_without_target)}")

    return data_with_target

def process_data(data, target_col):
    """Preprocess features and target columns separately for training"""

    # remove whitespace
    data = remove_whitespace(data)

    # remove duplicates
    data = remove_duplicates(data)

    # separate nan rows in target
    data = separate_nan_target(data, target_col)

    # split into features and target (target is last column)
    X = data.drop(columns=[target_col])
    y = data[target_col]

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

    # Separate numerical and non-numerical columns
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
    non_numerical_cols = X.select_dtypes(exclude=['int64', 'float64']).columns

    # Handle non-numerical columns
    X_non_numerical = X[non_numerical_cols].copy()
    for col in non_numerical_cols:
        if X[col].dtype == 'object':
            le = preprocessing.LabelEncoder()
            X_non_numerical[col] = le.fit_transform(X[col].astype(str))

    X_numerical = X[numerical_cols]
    if y.dtype in [np.int64, np.float64]:
        selector = SelectKBest(score_func=f_regression, k=min(100, X_numerical.shape[1]))
    else:
        selector = SelectKBest(score_func=f_classif, k=min(100, X_numerical.shape[1]))

    X_numerical_selected = selector.fit_transform(X_numerical, y)
    selected_numerical_cols = X_numerical.columns[selector.get_support()].tolist()

    # Combine selected numerical features with non-numerical features
    X_selected = np.hstack((X_numerical_selected, X_non_numerical))
    selected_features = selected_numerical_cols + non_numerical_cols.tolist()

    # choose model and data
    X, model = choose_model(X_selected, y)

    # fit model
    model = fit_model(model, X, y)

    return model, selected_features

def choose_model(X, y):
    """Choose model based on target type"""

    # if y is numerical
    if y.dtype in [np.int64, np.float64]:
        model = RandomForestRegressor(n_estimators=50, max_depth=10, min_samples_split=5)
        print("Linear Regression")
    else:
        model = RandomForestClassifier(n_estimators=50, max_depth=10, min_samples_split=5)
        print("Logistic Regression")

    return X, model

def fit_model(model, X, y):
    """Fit model to data"""

    model.fit(X, y)

    return model

def test_model(model, test, selected_features, target_col):
    """Test trained model on test data and return metric"""

    # process data
    test = process_data(test, target_col)

    # split into features and target (target is last column)
    X_test = test.drop(test.columns[-1], axis=1)
    y_test = test[test.columns[-1]]

    # Handle non-numerical columns
    for col in X_test.columns:
        if X_test[col].dtype == 'object':
            le = preprocessing.LabelEncoder()
            X_test[col] = le.fit_transform(X_test[col].astype(str))

    # Select features
    X_test = X_test[selected_features]
    X_test = X_test.apply(pd.to_numeric, errors='coerce')
    X_test = X_test.fillna(X_test.mean())

    y_pred = model.predict(X_test)
    metric = get_metric(y_test, y_pred)

    return metric

def get_metric(y_true, y_pred):
    """Return metric based on target type"""

    if y_true.dtype in ['int64', 'float64']:
        return {"loss": mean_squared_error(y_true, y_pred)}
    else:
        return {"accuracy": accuracy_score(y_true, y_pred), "precision": precision_score(y_true, y_pred)}

def upload_file(file_path, storage_path, file_name, bucket):
    """Upload file to Supabase storage"""

    # If file does not exist, upload file
    # else, update file

    file_options = {
        "cache-control": "3600",
        "upsert": "true"
    }

    try:
        # Check if file exists
        files = supabase.storage.from_(bucket).list(storage_path)
        file_exists = any(file['name'] == file_name for file in files)

        with open(file_path, 'rb') as f:
            if file_exists:
                response = supabase.storage.from_(bucket).update(
                    file=f,
                    path=f'{storage_path}/{file_name}',
                    file_options=file_options
                )
                print('File updated')
            else:
                response = supabase.storage.from_(bucket).upload(
                    file=f,
                    path=f'{storage_path}/{file_name}',
                )
                print('File uploaded')
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise

## PIPELINE ##

# prepare data
def prepare_data(**context):
    bucket_name = 'projects'
    project_id = context['dag_run'].conf.get('project_id')
    folder_name = 'data'

    # Load data
    try:
        data_bytes = supabase.storage.from_(bucket_name).download(f'{project_id}/data.csv')
        data = pd.read_csv(io.BytesIO(data_bytes))
    except Exception as e:
        print(f"Error downloading project data: {e}")
        raise

    # Split into train and test
    train = data.sample(frac=0.8, random_state=200)
    test = data.drop(train.index)

    # Save train and test data
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as train_file, \
             tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as test_file:
            
            train.to_csv(train_file.name, index=False)
            test.to_csv(test_file.name, index=False)
            
            train_file_path = train_file.name
            test_file_path = test_file.name

            # Upload to Supabase storage
            upload_file(train_file_path, f'{project_id}/{folder_name}', 'train.csv', bucket_name)
            upload_file(test_file_path, f'{project_id}/{folder_name}', 'test.csv', bucket_name)
    except Exception as e:
        print(f"Error uploading project data: {e}")
        raise
    finally:
        # Cleanup temporary files
        try:
            os.remove(train_file_path)
            os.remove(test_file_path)
        except Exception as cleanup_error:
            print(f"Error cleaning up temporary files: {cleanup_error}")

    print('Data loaded and split into train and test data')

def preprocess_train_data(**context):
    bucket_name = 'projects'
    project_id = context['dag_run'].conf.get('project_id')
    folder_name = 'data'

    # Load data
    try:
        data_bytes = supabase.storage.from_(bucket_name).download(f'{project_id}/{folder_name}/train.csv')
        data = pd.read_csv(io.BytesIO(data_bytes))
    except Exception as e:
        print(f"Error downloading project data: {e}")
        raise

    # Get target column
    try:
        response = supabase.table('projects').select('target').eq('id', project_id).execute()
        target_col = response.data[0]['target']
    except Exception as e:
        print(f"Error getting target column: {e}")
        raise

    # Process data
    processed_data = process_data(data, target_col)
    print("Data processed")

    # Save data
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as processed_train_file:
            processed_data.to_csv(processed_train_file.name, index=False)
            
            processed_train_file_path = processed_train_file.name

            # Upload to Supabase storage
            upload_file(processed_train_file_path, f'{project_id}/{folder_name}', 'processed_train_data.csv', bucket_name)
    except Exception as e:
        print(f"Error uploading project data: {e}")
        raise
    finally:
        # Cleanup temporary files
        try:
            os.remove(processed_train_file_path)
        except Exception as cleanup_error:
            print(f"Error cleaning up temporary files: {cleanup_error}")

    print('Processed train data saved')

def preprocess_test_data(**context):
    bucket_name = 'projects'
    project_id = context['dag_run'].conf.get('project_id')
    folder_name = 'data'

    # Load data
    try:
        data_bytes = supabase.storage.from_(bucket_name).download(f'{project_id}/{folder_name}/test.csv')
        data = pd.read_csv(io.BytesIO(data_bytes))
    except Exception as e:
        print(f"Error downloading project data: {e}")
        raise

    # Get target column
    try:
        response = supabase.table('projects').select('target').eq('id', project_id).execute()
        target_col = response.data[0]['target']
    except Exception as e:
        print(f"Error getting target column: {e}")
        raise

    processed_data = process_data(data, target_col)
    print("Data processed")

     # Save data
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as processed_test_file:
            processed_data.to_csv(processed_test_file.name, index=False)
            
            processed_test_file_path = processed_test_file.name

            # Upload to Supabase storage
            upload_file(processed_test_file_path, f'{project_id}/{folder_name}' ,'processed_test_data.csv', bucket_name)
    except Exception as e:
        print(f"Error uploading project data: {e}")
        raise
    finally:
        # Cleanup temporary files
        try:
            os.remove(processed_test_file_path)
        except Exception as cleanup_error:
            print(f"Error cleaning up temporary files: {cleanup_error}")

    print('Processed train data saved')

def train_and_test_model(**context):
    bucket_name = 'projects'
    project_id = context['dag_run'].conf.get('project_id')
    folder_name = 'data'

    # Load data
    try:
        train_bytes = supabase.storage.from_(bucket_name).download(f'{project_id}/{folder_name}/processed_train_data.csv')
        train_data = pd.read_csv(io.BytesIO(train_bytes))
        test_bytes = supabase.storage.from_(bucket_name).download(f'{project_id}/{folder_name}/processed_test_data.csv')
        test_data = pd.read_csv(io.BytesIO(test_bytes))
        target_col = supabase.table('projects').select('target').eq('id', project_id).execute().data[0]['target']
    except Exception as e:
        print(f"Error downloading project data: {e}")
        raise

    model, selected_features = train_model(train_data)
    metric = test_model(model, test_data, selected_features, target_col)

    name = f"Run {datetime.now()}"

    if len(metric) == 1:  # Regression model
        _ = (
            supabase.table("regression_models")
            .insert(
                {
                    "epoch": 50,
                    "loss": metric.get("loss"),
                    "name": name,
                    "project_id": project_id,
                }
            )
            .execute()
        )
    elif len(metric) == 2:  # Classification model
        _ = (
            supabase.table("classification_models")
            .insert(
                {
                    "accuracy": metric.get("accuracy"),
                    "precision": metric.get("precision"),
                    "name": name,
                    "project_id": project_id,
                }
            )
            .execute()
        )

    print(f"Model tested with metric: {metric}")

    # Save model
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as model_file, \
             tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as features_file:
            joblib.dump(model, model_file.name)
            joblib.dump(selected_features, features_file.name)
            
            model_file_path = model_file.name
            features_file_path = features_file.name

            # Upload to Supabase storage
            upload_file(model_file_path, f'{project_id}/{folder_name}', 'model.pkl', bucket_name)
            upload_file(features_file_path, f'{project_id}/{folder_name}', 'selected_features.pkl', bucket_name)
    except Exception as e:
        print(f"Error uploading model or features: {e}")
        raise
    finally:
        # Cleanup temporary files
        try:
            os.remove(model_file_path)
            os.remove(features_file_path)
        except Exception as cleanup_error:
            print(f"Error cleaning up temporary files: {cleanup_error}")

    print('Model and selected features saved')

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


    
