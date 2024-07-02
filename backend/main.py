from http.client import HTTPException
from io import BytesIO
from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from routers import users, classification_models, regression_models
from db.supabase import get_supabase_client
from typing import Union
from io import BytesIO

import airflow_client.client as client
from airflow_client.client.api import config_api
from airflow_client.client.api import dag_run_api
from airflow_client.client.model.dag_run import DAGRun
from airflow_client.client.model.config import Config
from airflow_client.client.model.error import Error
from pydantic import BaseModel
import pandas as pd

app = FastAPI()
# Include the routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(classification_models.router, prefix="/classification_models", tags=["classification_models"])
app.include_router(regression_models.router, prefix="/regression_models", tags=["regression_models"])
# Initialize supabase client
supabase = get_supabase_client()
# Defining the host is optional and defaults to /api/v1



configuration = client.Configuration(
    host="http://localhost:8080/api/v1",
    username="airflow",
    password="airflow"
)

# Enter a context with an instance of the API client
with client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = config_api.ConfigApi(api_client)

    try:
        # Get current configuration
        api_response = api_instance.get_config()
        print(api_response)
    except client.ApiException as e:
        print("Exception when calling ConfigApi->get_config: %s\n" % e)


class TriggerDagRequest(BaseModel):
    dag_id: str
    conf: dict = {}




@app.post("/trigger_dag/")
async def trigger_dag(request: TriggerDagRequest):
    dag_id = request.dag_id
    conf = request.conf
    api_instance = dag_run_api.DAGRunApi(api_client)

    # Prepare the DAG run payload
    dag_run = DAGRun(
        conf=conf,
        dag_run_id="dag_id",
    )

    try:
        with client.ApiClient(configuration) as api_2_client:
            # Create an instance of the DAGRun API class
            # Trigger the DAG
            api_response = api_instance.post_dag_run(dag_id, dag_run)
            return {"message": "DAG triggered successfully", "dag_run_id": api_response.dag_run_id}
    except client.ApiException as e:
        print("Exception when calling DAGRunApi->post_dag_run: %s\n" % e)

def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    try: 
        # Step 3: Select the specified columns
        selected_columns = df[columns]
        # Save the processed DataFrame to a new CSV file
        processed_csv_file = BytesIO()
        selected_columns.to_csv(processed_csv_file, index=False)
        processed_csv_file.seek(0)  # Reset the file pointer to the beginning
        upload_response = supabase.storage.from_('datamall').upload('processed_file.csv', processed_csv_file.getvalue())
        if not upload_response:
                raise HTTPException(status_code=500, detail="Failed to upload processed file")
        return {"message": "File processed and uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create function to select columns, then upload the processed file into Supabase
@app.post("/process_csv_supabase/")
async def process_csv_supabase(file_path: str, columns: list[str] = Query(...)):
    try:
        # Step 2: Download the CSV file
        with open("datatest", 'wb+') as f:
            # This will download the file from Supabase storage
            res = supabase.storage.from_('datamall').download(file_path)
            # This will write the downloaded file to the local file system
            f.write(res)
        if not res:
            raise HTTPException(status_code=404, detail="File not found")
        # This will read the CSV file into a pandas DataFrame
        df = pd.read_csv('datatest')
        return select_columns(df, columns)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_csv_local/")
async def process_csv_local(file_path: str, columns: list[str] = Query(...)):
    try:
        # Open CSV from local data folder
        df = pd.read_csv(file_path)
        return select_columns(df, columns)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))