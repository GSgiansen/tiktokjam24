from fastapi import APIRouter, Depends, HTTPException
from models import Project
from db.supabase import  get_supabase_client
from typing import Union
from uuid import UUID
import bcrypt

router = APIRouter()
# Initialize supabase client
supabase = get_supabase_client()

def project_exists(name: str = None, owner: UUID = None):
    project = supabase.from_("projects").select("*").eq("name", name).eq("owner", owner).execute()
    return len(project.data) > 0

# Create a new project
@router.post("/project")
def create_project(project: Project):
    try:
        # Convert name to lowercase
        project_name = project.name.lower()

        # Check if project already exists
        if project_exists(name=project_name, owner=project.owner):
            return {"message": "Project already exists"}

        # Add project to projects table
        project = supabase.from_("projects")\
            .insert({"name": project_name, "owner": project.owner})\
            .execute()

        # Check if project was added
        if project:
            return {"message": "Project created successfully"}
        else:
            return {"message": "Project creation failed"}
        
    except Exception as e:
        print("Error: ", e)
        return {"message": "Project creation failed"}

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