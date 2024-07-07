from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import numpy as np
import pandas as pd
import io
import os
import tempfile
import joblib
from datetime import datetime, timedelta
from backend.db import get_supabase_client
import sklearn.preprocessing as preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer

supabase = get_supabase_client()

# Helper functions
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

def update_table(project_id):
    """Update table status"""

    try:
        response = supabase.table('projects').update({"additional_predict": True}).eq('id', project_id).execute()
    except Exception as e:
        print(f"Error updating table: {e}")
        raise

def remove_whitespace(df):
    """Remove leading and trailing whitespace from all string columns."""

    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.strip()
    return df

def remove_duplicates(df):
    """Remove duplicate rows from data."""

    return df.drop_duplicates()

def process_data(data):
    """Preprocess features and target columns separately for training"""

    # remove whitespace
    data = remove_whitespace(data)

    # remove duplicates
    data = remove_duplicates(data)

    X = data

    # split into categorical and numerical features
    categorical = X.select_dtypes(include=['object'])
    numerical = X.select_dtypes(exclude=['object'])

    # process categorical features
    categorical = process_categorical_df(categorical)

    # process numerical features
    numerical = process_numerical_df(numerical)

    process_data = pd.concat([categorical, numerical], axis=1)
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

# Pipeline
def predict(**context):
    bucket_name = 'projects'
    folder_name = 'data'
    project_id = context['dag_run'].conf.get('project_id')

    # Load data
    try:
        data_bytes = supabase.storage.from_(bucket_name).download(f'{project_id}/add_predict.csv')
        data = pd.read_csv(io.BytesIO(data_bytes))
    except Exception as e:
        print(f"Error downloading project data: {e}")
        raise

    # Load model
    try:
        model_bytes = supabase.storage.from_(bucket_name).download(f'{project_id}/{folder_name}/model.pkl')
        model = joblib.load(io.BytesIO(model_bytes))
    except Exception as e:
        print(f"Error downloading model: {e}")
        raise

    # Load selected features
    try:
        features_bytes = supabase.storage.from_(bucket_name).download(f'{project_id}/{folder_name}/selected_features.pkl')
        selected_features = joblib.load(io.BytesIO(features_bytes))
    except Exception as e:
        print(f"Error downloading selected features: {e}")
        raise

    # Get target column
    try:
        response = supabase.table('projects').select('target').eq('id', project_id).execute()
        target_col = response.data[0]['target']
    except Exception as e:
        print(f"Error getting target column: {e}")
        raise

    # Predict
    X = process_data(data)

    # Handle non-numerical columns
    for col in X.columns:
        if X[col].dtype == 'object':
            le = preprocessing.LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))

    X = X[selected_features]  # Use only selected features
    y_pred = model.predict(X)
    print(y_pred)

    # Save prediction
    try:
        data[target_col] = y_pred
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as add_predict_file:
            data.to_csv(add_predict_file.name, index=False)

            add_predict_file_path = add_predict_file.name

            # Upload file
            upload_file(add_predict_file_path, f'{project_id}/{folder_name}', 'add_predict_res.csv', bucket_name)

            # Update table
            update_table(project_id)
    except Exception as e:
        print(f"Error saving prediction: {e}")
        raise
    finally:
        # Cleanup temporary files
        try:
            os.remove(add_predict_file_path)
        except Exception as cleanup_error:
            print(f"Error cleaning up temporary files: {cleanup_error}")
        
with DAG(
    default_args = {
        'owner': 'RCH4CKERS',
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    description='Additional adhoc predict pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 6, 20),
    dag_id='add_predict_pipeline',
) as dag:
    start = DummyOperator(task_id='start')

    predict = PythonOperator(
        task_id='prepare_data',
        python_callable=predict
    )

    end = DummyOperator(task_id='end')

    start >> \
    predict >> \
    end