import re
import easyocr
from pathlib import Path

# -------------------- RULES --------------------

INTERPRETATION_RULES = {
    "hba1c": [
        (0, 5.6, "normal"),
        (5.7, 6.4, "prediabetes"),
        (6.5, 20, "diabetes")
    ],
    "fasting_glucose": [
        (0, 99, "normal"),
        (100, 125, "impaired"),
        (126, 500, "diabetes")
    ],
    "ldl_cholesterol": [
        (0, 99, "optimal"),
        (100, 129, "near_optimal"),
        (130, 159, "borderline_high"),
        (160, 1000, "high")
    ],
    "hdl_cholesterol": [
        (0, 39, "low"),
        (40, 1000, "normal")
    ],
    "triglycerides": [
        (0, 149, "normal"),
        (150, 199, "borderline_high"),
        (200, 1000, "high")
    ]
}

LAB_DEFINITIONS = {
    "hba1c": {
        "labels": [r'hb[a-z]*c'],
        "min_digits": 2
    },
    "fasting_glucose": {
        "labels": [r'fasting.*glucose'],
        "min_digits": 3
    },
    "ldl_cholesterol": {
        "labels": [r'ldl'],
        "min_digits": 2
    },
    "hdl_cholesterol": {
        "labels": [r'hdl'],
        "min_digits": 2
    },
    "triglycerides": {
        "labels": [r'triglycerides'],
        "min_digits": 2
    }
}

NORMALIZATION_RULES = {
    "fasting_glucose": {
        "from": "mg/dL",
        "to": "mmol/L",
        "factor": 0.0555
    },
    "ldl_cholesterol": {
        "from": "mg/dL",
        "to": "mmol/L",
        "factor": 0.0259
    },
    "hdl_cholesterol": {
        "from": "mg/dL",
        "to": "mmol/L",
        "factor": 0.0259
    },
    "triglycerides": {
        "from": "mg/dL",
        "to": "mmol/L",
        "factor": 0.0113
    }
}

# -------------------- EXTRACTION --------------------

def preprocess(text: str) -> str:
    return text.lower()

def extract_single_value(text: str, label_patterns: list[str], *, min_digits=1):
    for label in label_patterns:
        pattern = rf'{label}[^0-9]{{0,30}}([\d]+\.?\d*)'
        match = re.search(pattern, text)
        if match:
            value = match.group(1)
            if len(value.replace('.', '')) >= min_digits:
                return float(value)
    return None

def extract_blood_pressure(text: str):
    match = re.search(
        r'(blood pressure|bp)[^0-9]*([1-9]\d{1,2})\s*/\s*([1-9]\d{1,2})',
        text
    )
    if match:
        return {
            "systolic": int(match.group(2)),
            "diastolic": int(match.group(3))
        }
    return None

def parse_lab_values(text: str) -> dict:
    results = {}

    for lab, config in LAB_DEFINITIONS.items():
        value = extract_single_value(
            text,
            config["labels"],
            min_digits=config["min_digits"]
        )
        if value is not None:
            results[lab] = value

    bp = extract_blood_pressure(text)
    if bp:
        results["blood_pressure"] = bp

    return results

# -------------------- INTERPRETATION --------------------

def interpret_value(lab_name: str, value):
    rules = INTERPRETATION_RULES.get(lab_name)
    if not rules:
        return "unknown"

    for low, high, label in rules:
        if low <= value <= high:
            return label

    return "unknown"

def interpret_blood_pressure(bp: dict):
    s = bp.get("systolic")
    d = bp.get("diastolic")

    if s is None or d is None:
        return "unknown"

    if s < 120 and d < 80:
        return "normal"
    if 120 <= s <= 129 and d < 80:
        return "elevated"
    if s >= 130 or d >= 80:
        return "hypertension"

    return "unknown"

def enrich_with_interpretation(parsed: dict) -> dict:
    enriched = {}

    for lab, value in parsed.items():
        if lab == "blood_pressure":
            enriched[lab] = {
                "value": value,
                "status": interpret_blood_pressure(value),
                "confidence": "high"
            }
        else:
            enriched[lab] = {
                "raw_value": value,
                "status": interpret_value(lab, value),
                "confidence": "high"
            }

    return enriched

# -------------------- NORMALIZATION --------------------

def normalize_values(parsed: dict) -> dict:
    normalized = {}

    for lab, value in parsed.items():
        if lab in NORMALIZATION_RULES:
            rule = NORMALIZATION_RULES[lab]
            normalized_value = round(value * rule["factor"], 2)

            normalized[lab] = {
                "raw_value": value,
                "raw_unit": rule["from"],
                "value": normalized_value,
                "unit": rule["to"],
                "normalized": True
            }
        else:
            normalized[lab] = {
                "value": value,
                "normalized": False
            }

    return normalized

# -------------------- MERGE --------------------

def merge_results(enriched: dict, normalized: dict) -> dict:
    final = {}

    for lab in enriched:
        if lab == "blood_pressure":
            final[lab] = enriched[lab]
        else:
            final[lab] = {
                **normalized.get(lab, {}),
                "status": enriched[lab]["status"],
                "confidence": enriched[lab]["confidence"]
            }

    return final

# -------------------- RUN --------------------

reader = easyocr.Reader(['en'])

def extract_raw_text(image_path: str) -> str:
    result = reader.readtext(image_path)
    text = " ".join([item[1] for item in result])
    return text

RAW_TEXT = extract_raw_text("IMAGE HERE")

RAW_TEXT = preprocess(RAW_TEXT)

parsed = parse_lab_values(RAW_TEXT)
enriched = enrich_with_interpretation(parsed)
normalized = normalize_values(parsed)
final_result = merge_results(enriched, normalized)

print(final_result)
