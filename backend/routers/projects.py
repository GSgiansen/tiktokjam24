from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile
from fastapi.responses import JSONResponse
from models import Project
from db.supabase import  get_supabase_client
from typing import Union
from uuid import UUID
import uuid
import bcrypt
from typing import Annotated
import json
from typing import List

router = APIRouter()
# Initialize supabase client
supabase = get_supabase_client()

def project_exists(name: str = None, owner: UUID = None):
    project = supabase.from_("projects").select("*").eq("name", name).eq("owner", owner).execute()
    return len(project.data) > 0

# Create a new project
@router.post("/project")
async def create_project(name: Annotated[str, Form()], owner: Annotated[str, Form()], file: Annotated[UploadFile, Form()], target: Annotated[str, Form()], columns: Annotated[List[str], Form()], ml_method: Annotated[str, Form()]):
    print(columns)
    json_array_str = columns[0]  # Assuming there's only one element in the list
    json_array = json.loads(json_array_str)

    # Convert the JSON array to PostgreSQL array literal format
    postgres_array = "{" + ",".join(f'"{col}"' for col in json_array) + "}"

    print(f"Received name: {name}")
    print(f"Received owner: {owner}")
    print(f"Received file: {file}")
    print(f"Received target: {target}")
    print(f"Received columns: {columns[0]}")
    print(f"Received ml_method {ml_method}")
    print(f"json columns {postgres_array}")
    try:
        contents = await file.read()
        response = (supabase.from_("projects")\
        .insert({"name": name, "owner": owner, "features": postgres_array, "target": target, "ml_method": ml_method})\
        .execute())
        data_json = json.loads(response.json())
        data_entries = data_json['data']
        print(data_entries)
        supabase.storage\
        .from_("projects/" + data_entries[0]["id"])\
        .upload(file=contents,path="data.csv")
        return JSONResponse(content={"id": data_entries[0]["id"]})

    except Exception as e:
        print(f"Error: {e}")
        return {"message": f"Project creation failed {e}"} 

#Retrieve a user's projects
@router.get("/queryProjects")
async def get_user_projects(owner: str):
    try:
        projects = supabase.from_("projects")\
            .select("id", "name", "owner")\
            .eq("owner", owner)\
            .execute()
        if projects:
            return projects
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Project not found"}


# Retrieve a project
@router.get("/project")
def get_project(project_id: Union[UUID, None] = None):
    try:
        if project_id:
            project = supabase.from_("projects")\
                .select("id", "name", "owner")\
                .eq("id", project_id)\
                .execute()

            if project:
                return project
        else:
            projects = supabase.from_("projects")\
                .select("id", "name", "owner")\
                .execute()
            if projects:
                return projects
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Project not found"}


# Update a project
@router.put("/project")
def update_project(project_id: UUID, name: str, owner: UUID):
    try:
        project_name = name.lower()

        # Check if project exists
        if project_exists("id", project_id):
            # Check if name already exists
            if project_exists(name=project_name, owner=owner):
                return {"message": "Project already exists"}

            # Update project
            project = supabase.from_("projects")\
                .update({"name": project_name, "owner": owner})\
                .eq("id", project_id).execute()
            if project:
                return {"message": "Project updated successfully"}
        else:
            return {"message": "Project update failed"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Project update failed"}

# Delete a project
@router.delete("/project")
def delete_project(project_id: UUID):
    try:        
        # Check if project exists
        if project_exists("id", project_id):
            # Delete project
            project = supabase.from_("projects")\
                .delete().eq("id", project_id).execute()
            if project:
                return {"message": "Project deleted successfully"}
        else:
            return {"message": "Project deletion failed"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Project deletion failed"}