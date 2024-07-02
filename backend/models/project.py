from pydantic import BaseModel
from uuid import UUID

class Project(BaseModel):
    name: str
    owner: UUID
