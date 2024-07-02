from fastapi import APIRouter, Depends, HTTPException
from models import Regression_Model
from db.supabase import get_supabase_client
from typing import Union
import bcrypt
import random

router = APIRouter()


# Initialize supabase client
supabase = get_supabase_client()
print("supabase", supabase)
### TODO
### Need to change model name to be unqieu
def regression_model_exists(key: str = "name", value: str = None):
    regression_model = supabase.from_("regression_models").select("*").eq(key, value).execute()
    return len(regression_model.data) > 0

# Create a new regression_model
@router.post("/regression_model")
def create_regression_model(regression_model: Regression_Model):
    try:
        # Convert name to lowercase
        regression_model_name = regression_model.name.lower()
        regression_model_epoch= regression_model.epoch
        ## TODO
        ## Handle unique model names
        if regression_model_exists(value=regression_model_name):
            return {"message": "regression_model already exists"}
        # Add regression_model to regression_models table
        regression_model = supabase.from_("regression_models")\
            .insert({"name": regression_model.name, "epoch": regression_model_epoch, "loss": random.random()})\
            .execute()

        # Check if regression_model was added
        if regression_model:
            return {"message": "regression_model created successfully"}
        else:
            return {"message": "regression_model creation failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "regression_model creation failed"}

# Retrieve a regression_model
@router.get("/regression_model")
def get_regression_model(regression_model_id: Union[str, None] = None):
    try:
        if regression_model_id:
            regression_model = supabase.from_("regression_models")\
                .select("id", "name")\
                .eq("id", regression_model_id)\
                .execute()

            if regression_model:
                return regression_model
        else:
            regression_models = supabase.from_("regression_models")\
                .select("id", "name")\
                .execute()
            if regression_models:
                return regression_models
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "regression_modelnot found"}


# Update a regression_model
@router.put("/regression_model")
def update_regression_model(regression_model_id: str, name: str):
    try:
        regression_model_name= name.lower()

        # Check if regression_model exists
        if regression_model_exists("id", regression_model_id):
            # Check if email already exists
            email_exists = supabase.from_("regression_models")\
                .select("*").eq("name", regression_model_name)\
                .execute()
            if len(email_exists.data) > 0:
                return {"message": "Name already exists"}

            # Update regression_model
            regression_model = supabase.from_("regression_models")\
                .update({"name": name})\
                .eq("id", regression_model_id).execute()
            if regression_model:
                return {"message": "regression_model updated successfully"}
        else:
            return {"message": "regression_model update failed"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "regression_model update failed"}

# Delete a regression_model
@router.delete("/regression_model")
def delete_regression_model(regression_model_id: str):
    try:        
        # Check if regression_model exists
        if regression_model_exists("id", regression_model_id):
            # Delete regression_model
            supabase.from_("regression_models")\
                .delete().eq("id", regression_model_id)\
                .execute()
            return {"message": "regression_model deleted successfully"}

        else:
            return {"message": "regression_model deletion failed"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "regression_model deletion failed"}