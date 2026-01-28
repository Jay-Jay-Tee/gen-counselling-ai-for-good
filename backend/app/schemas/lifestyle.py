from pydantic import BaseModel

class Lifestyle(BaseModel):
    smoking: bool
    alcohol: str
    exercise: str
    diet: str
    sleep_hours: float
    stress_level: str