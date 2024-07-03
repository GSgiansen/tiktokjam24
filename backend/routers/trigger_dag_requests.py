from fastapi import APIRouter, Depends, HTTPException
from models import TriggerDagRequest
from db.supabase import get_supabase_client
from typing import Union
import random
import airflow_client.client as client
from airflow_client.client.api import config_api
from airflow_client.client.api import dag_run_api
from airflow_client.client.model.dag_run import DAGRun
from airflow_client.client.model.config import Config
from airflow_client.client.model.error import Error


router = APIRouter()


# Initialize supabase client
supabase = get_supabase_client()


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



@router.post("/trigger_dag/")
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


