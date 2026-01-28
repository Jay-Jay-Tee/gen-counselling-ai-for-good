from pydantic import BaseModel
from typing import Optional

class LabValues(BaseModel):
    hba1c: Optional[float] = None
    fasting_glucose: Optional[float] = None
    random_glucose: Optional[float] = None
    ldl: Optional[float] = None
    hdl: Optional[float] = None
    triglycerides: Optional[float] = None
    total_cholesterol: Optional[float] = None
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    tsh: Optional[float] = None
    t4: Optional[float] = None
    t3: Optional[float] = None
    hemoglobin: Optional[float] = None
    rbc: Optional[float] = None
    mcv: Optional[float] = None
    mch: Optional[float] = None