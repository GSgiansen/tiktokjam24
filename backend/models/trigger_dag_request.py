from pydantic import BaseModel

class TriggerDagRequest(BaseModel):
    dag_id: str
    conf: dict = {
    }


