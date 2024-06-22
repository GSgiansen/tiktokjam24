from pydantic import BaseModel

class Classification_Model(BaseModel):
    name: str
    accuracy: float
    precision: float
