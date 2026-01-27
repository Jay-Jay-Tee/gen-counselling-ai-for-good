from fastapi import APIRouter
from app.schemas.prediction import RiskRequest, RiskResponse
from app.services.prediction_service import predict_risk

router = APIRouter(prefix="/predict-risk", tags=["Prediction"])

@router.post("/", response_model=RiskResponse)
def predict_risk_api(payload: RiskRequest):
    return predict_risk(payload)
