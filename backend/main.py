import bcrypt
from fastapi import FastAPI
from routers import users, classification_models
from db.supabase import get_supabase_client
from typing import Union


app = FastAPI()
# Include the routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(classification_models.router, prefix="/classification_models", tags=["classification_models"])
# Initialize supabase client
supabase = get_supabase_client()
