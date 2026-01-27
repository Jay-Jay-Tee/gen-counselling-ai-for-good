from app.schemas.prediction import RiskResponse, DiseaseRisk, RiskLevel, Recommendation

def predict_risk(payload):
    # TEMP / dummy logic
    return RiskResponse(
        patient_name=""
        results=[
            DiseaseRisk(
                disease="diabetes",
                risk_score=0.72,
                risk_level=RiskLevel.high,
                factors=["family history", "elevated sugar level"],
                recommendation=Recommendation.consult_soon
            )
        ]
    )