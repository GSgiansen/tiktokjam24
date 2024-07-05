from pydantic import BaseModel
from uuid import UUID
from fastapi import UploadFile
import json
from fastapi import Form
from typing import Annotated

class Project(BaseModel):
    name: Annotated[str, Form()]
    file: Annotated[str, Form()]


