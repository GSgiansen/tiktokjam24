from fastapi import APIRouter, Depends, HTTPException
from models import Classification_Model
from db.supabase import get_supabase_client
from typing import Union
import bcrypt
import random

router = APIRouter()


# Initialize supabase client
supabase = get_supabase_client()
### TODO
### Need to change model name to be unqieu
def classification_model_exists(key1: str = "project_id", value1: str = None, key2: str = "project_id_run", value2: int = None):

    classification_model = supabase.from_("classification_models").select("*").eq(key1, value1).eq(key2, value2).execute()
    return len(classification_model.data) > 0

# Create a new classification_model
@router.post("/classification_model")
def create_classification_model(classification_model: Classification_Model):
    try:
        # Convert name to lowercase
        classification_model_accuracy = classification_model.accuracy
        classification_model_precision = classification_model.precision
        classification_model_name = classification_model.name.lower()
        classification_model_project_id = classification_model.project_id
        classification_model_project_id_run = classification_model.project_id_run



        if classification_model_exists(value1=classification_model_project_id, value2=classification_model_project_id_run):
            return {"message": "Classification_model already exists"}
        # Add classification_model to classification_models table
        classification_model = supabase.from_("classification_models")\
            .insert({"name": classification_model.name, 
                     "accuracy": classification_model_accuracy, 
                     "precision": classification_model_precision,
                     "project_id": classification_model_project_id,
                     "project_id_run": classification_model_project_id_run
                     })\
            .execute()

        # Check if classification_model was added
        if classification_model:
            return {"message": "Classification_model created successfully"}
        else:
            return {"message": "Classification_model creation failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "Classification_model creation failed"}

# Retrieve a classification_model
@router.get("/classification_model")
def get_classification_model(classification_model_id: Union[str, None] = None):
    try:
        if classification_model_id:
            classification_model = supabase.from_("classification_models")\
                .select("id", "name", "accuracy", "precision", "project_id", "project_id_run")\
                .eq("id", classification_model_id)\
                .execute()

            if classification_model:
                return classification_model
        else:
            classification_models = supabase.from_("classification_models")\
                .select("id", "name")\
                .execute()
            if classification_models:
                return classification_models
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Classification_model not found"}


# Update a classification_model
@router.put("/classification_model")
def update_classification_model(classification_model_id: str, name: str):
    try:
        classification_model_name= name.lower()

        # Check if classification_model exists
        if classification_model_exists("id", classification_model_id):
            # Check if email already exists
            email_exists = supabase.from_("classification_models")\
                .select("*").eq("name", classification_model_name)\
                .execute()
            if len(email_exists.data) > 0:
                return {"message": "Name already exists"}

            # Update classification_model
            classification_model = supabase.from_("classification_models")\
                .update({"name": name})\
                .eq("id", classification_model_id).execute()
            if classification_model:
                return {"message": "Classification_model updated successfully"}
        else:
            return {"message": "Classification_model update failed"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Classification_model update failed"}

# Delete a classification_model
@router.delete("/classification_model")
def delete_classification_model(classification_model_id: str):
    try:        
        # Check if classification_model exists
        if classification_model_exists("id", classification_model_id):
            # Delete classification_model
            supabase.from_("classification_models")\
                .delete().eq("id", classification_model_id)\
                .execute()
            return {"message": "Classification_model deleted successfully"}

        else:
            return {"message": "Classification_model deletion failed"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Classification_model deletion failed"}
    


### Returns all model metrics given a project_id, returns a list of all runs and their metrics
@router.get("/query_classification_models")
def query_classification_models(project_id: str):
    try:
        classification_models = supabase.from_("classification_models")\
            .select("name", "epoch", "loss", "project_id_run")\
            .eq("project_id", project_id)\
            .execute()
        if classification_models:
            return classification_models
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "classification_model not found"}