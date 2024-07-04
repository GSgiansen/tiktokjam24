from pydantic import BaseModel

class Classification_Model(BaseModel):
    name: str
    accuracy: float
    precision: float
    project_id: str
    project_id_run: int
