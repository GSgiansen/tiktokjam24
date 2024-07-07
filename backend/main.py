from datetime import datetime
from io import BytesIO
import uuid
from fastapi import FastAPI, HTTPException, Query,Security,Depends, UploadFile, Form, Header
import pandas as pd
from routers import users, classification_models, regression_models, projects
from db.supabase import get_supabase_client
from typing import Union
from io import BytesIO
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import Response, FileResponse
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import time
import os 
import jwt
from typing import Annotated

import airflow_client.client as client
from airflow_client.client.api import config_api
from airflow_client.client.api import dag_run_api
from airflow_client.client.model.dag_run import DAGRun
from airflow_client.client.model.config import Config
from airflow_client.client.model.error import Error
from pydantic import BaseModel

app = FastAPI()
# Include the routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(classification_models.router, prefix="/classification_models", tags=["classification_models"])
app.include_router(regression_models.router, prefix="/regression_models", tags=["regression_models"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
# Initialize supabase client
supabase = get_supabase_client()
# Defining the host is optional and defaults to /api/v1
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain e.g., ["http://localhost", "https://example.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allowed HTTP methods
    allow_headers=["*"],  # Allowed headers
)

# Dependency to get the Authorization header
async def get_authorization_header(authorization: str = Header(...)):
    jwt.decode(authorization.replace('Bearer', '').strip(), os.getenv("SUPABASE_SECRET_KEY")
, audience="authenticated", algorithms=['HS256'])
    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header missing")
    return authorization


configuration = client.Configuration(
    host="http://airflow-webserver:8080/api/v1",
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


class SynthesizeDataRequest(BaseModel):
    dag_id: str
    conf: dict = {
        "filepath": "default",
        "input": "default",
        "iter_count": 10,
        "dirpath": "default"
    }


@app.post("/trigger_dag/")
async def trigger_dag(request: TriggerDagRequest, authorization: str = Depends(get_authorization_header)):
    dag_id = request.dag_id
    conf = request.conf
    api_instance = dag_run_api.DAGRunApi(api_client)
    dag_run_id = dag_id + datetime.now().strftime("%Y%m%d%H%M%S")

    # Prepare the DAG run payload
    dag_run = DAGRun(
        conf=conf,
        dag_run_id=dag_run_id,
    )

    try:
        with client.ApiClient(configuration) as api_2_client:
            # Create an instance of the DAGRun API class
            # Trigger the DAG
            api_response = api_instance.post_dag_run(dag_id, dag_run)
            return {"message": "DAG triggered successfully", "dag_run_id": api_response.dag_run_id}
    except client.ApiException as e:
        print("Exception when calling DAGRunApi->post_dag_run: %s\n" % e)



@app.post("/trigger_dag_synthesize")
async def trigger_dag_synthesize(request: SynthesizeDataRequest):
    dag_id = request.dag_id
    conf = request.conf
    api_instance = dag_run_api.DAGRunApi(api_client)
    dag_run_id = dag_id + datetime.now().strftime("%Y%m%d%H%M%S")

    # Prepare the DAG run payload
    dag_run = DAGRun(
        conf=conf,
        dag_run_id=dag_run_id,
    )

    try:
        with client.ApiClient(configuration) as api_2_client:
            # Create an instance of the DAGRun API class
            # Trigger the DAG
            api_response = api_instance.post_dag_run(dag_id, dag_run)
            return {"message": "Synthesize DAG triggered successfully", "dag_run_id": api_response.dag_run_id}
    except client.ApiException as e:
        print("Exception when calling Synthesize DAGRunApi->post_dag_run: %s\n" % e)





### Gety csv from frontend and generate uuid for the file
@app.post("/synthesize_data")
async def synthesize_data(file: Annotated[UploadFile, Form()],  input: Annotated[str, Form()], iter_count: Annotated[int, Form()]):
    bucket_name = "synthesize_data"
    ### Upload the file path to the bucket
    filename = str(uuid.uuid4())
    print(filename)
    filepath = f"{filename}/{filename}.csv"

    response =  supabase.storage\
        .from_("synthesize_data/" + filename)\
        .upload(file=file.file.read(), path=f"{filename}.csv")

    
    classreq = SynthesizeDataRequest(dag_id="synthesize_data", conf={"filepath": filepath, "input": input, "iter_count": iter_count, "dirpath": "data"})
    await trigger_dag_synthesize(classreq)
    
    time.sleep(30)
    
    with open(f"{filename}.csv", "wb+") as f:
        response = supabase.storage\
            .from_("synthesize_data")\
            .download(filename + "/generated.csv")       
        f.write(response)


    res = FileResponse(path=f"{filename}.csv", media_type="text/csv")
    print(res)
    return res 



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

def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    try: 
        # Step 3: Select the specified columns
        selected_columns = df[columns]
        # Save the processed DataFrame to a new CSV file
        processed_csv_file = BytesIO()
        selected_columns.to_csv(processed_csv_file, index=False)
        processed_csv_file.seek(0)  # Reset the file pointer to the beginning
        upload_response = supabase.storage.from_('projects').upload('processed_file_test.csv', processed_csv_file.getvalue())
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
            res = supabase.storage.from_('projects').download(file_path)
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