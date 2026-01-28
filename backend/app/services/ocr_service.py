from app.schemas.lab_values import LabValues

def extract_lab_values_from_file(file) -> LabValues:
    # TEMP / dummy extracted values
    return LabValues(
        hba1c=6.2,
        fasting_glucose=112,
        ldl=145,
        hdl=42,
        hemoglobin=13.4,
        rbc=4.6
    )
