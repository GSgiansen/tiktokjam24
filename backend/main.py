from fastapi import FastAPI, Security,Depends
from routers import users, classification_models, regression_models
from db.supabase import get_supabase_client
from typing import Union

import airflow_client.client as client
from airflow_client.client.api import config_api
from airflow_client.client.api import dag_run_api
from airflow_client.client.model.dag_run import DAGRun
from airflow_client.client.model.config import Config
from airflow_client.client.model.error import Error
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated


app = FastAPI()
# Include the routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(classification_models.router,
                   prefix="/classification_models", tags=["classification_models"])
app.include_router(regression_models.router,
                   prefix="/regression_models", tags=["regression_models"])
# Initialize supabase client
supabase = get_supabase_client()
# Defining the host is optional and defaults to /api/v1


configuration = client.Configuration(
    host="http://localhost:8080/api/v1",
    username="airflow",
    password="airflow"
)

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    response = supabase.auth.get_user(token)
    
    if 'error' in response:
        raise HTTPException(status_code=401, detail="Invalid token or authentication credentials.")
    
    return response.user

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


@app.post("/login_supabase/")
# using supabase auth to login
async def login_supabase(email: str, password: str):
    
# data = supabase.auth.sign_in_with_password({"email": "j0@supabase.io", "password": "testsupabasenow"})
    response = supabase.auth.sign_in_with_password({"email":email, "password":password})
    # if response.error:
    #     return response.error
    return {"access_token": response.session.access_token, "token_type": "bearer"}


@app.post("/register_supabase/")
# using supabase auth to register
async def register_supabase(email: str, password: str):
    response = supabase.auth.sign_up(
        credentials={"email": email, "password": password}
    )
    print(response)
    # if response.error:
    #     return response.error
    return response.session.access_token


@app.get("/protected-route/")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route.", "user": user}