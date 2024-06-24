from pydantic import BaseModel

class Regression_Model(BaseModel):
    name: str
    epoch: int
    loss: int