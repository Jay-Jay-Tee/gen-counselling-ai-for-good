from pydantic import BaseModel

class DiseaseOption(BaseModel):
    id: str
    name: str
