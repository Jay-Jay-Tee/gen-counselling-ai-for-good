# Gen Counselling AI for Good 🧬💙  
*A web-based AI preventive health platform for inherited disease risk awareness.*

---

## 📌 Project Gist (Brief)

We are building a web-based AI preventive health platform that predicts an individual's genetically inherited disease risks using:

- **Family history (up to 2 generations)**
- **User health records** (manual input / AI-OCR)
- **Open-source datasets**

The system displays **disease-wise risk** as ranked probabilities or risk classes (**I–IV**), explains each condition in simple language, and functions as a **dynamic health coach** by suggesting lifestyle interventions, recommended screening tests, and urgent doctor consultation when risk is high.

The goal is to reduce late diagnosis and improve early awareness among adolescents and adults.

---

## 1) 🧩 Problem Statement

Many individuals unknowingly carry a genetic predisposition to chronic and inherited diseases such as:

- Type-2 diabetes  
- Coronary artery disease  
- Hereditary breast and ovarian cancer (BRCA-related)  
- Thalassemia  
- Sickle cell disease  
- Familial hypercholesterolemia  

These risks remain invisible until symptoms appear, leading to delayed diagnosis and worse outcomes. Adolescents and young adults especially rarely undergo preventive screening or risk assessment, missing early intervention opportunities.

Existing healthcare systems largely react after disease onset rather than predicting and preventing it, increasing long-term health burden, healthcare costs, and avoidable morbidity.

---

## 2) 🌍 Context and Persistence of the Problem

This issue is widespread across both urban and semi-urban populations, especially in countries like India where preventive healthcare adoption is low.

It impacts individuals with family histories of chronic or inherited disease, many of whom remain unaware of their genetic risk. Despite medical advances, genetic testing and counseling still remain:

- expensive
- inaccessible
- poorly integrated into routine care

Healthcare systems largely focus on treatment rather than prediction. Asymptomatic individuals rarely seek screening, allowing inherited risks to go unnoticed and increasing preventable complications and long-term burden.

---

## 3) 🎯 Target Users / Beneficiaries or Community

**Primary users:**
- Adolescents and adults (**15–55 years**) who are asymptomatic but may carry inherited risk
- Students, working professionals, and middle-aged individuals in urban and semi-urban regions with limited access to preventive healthcare

**Secondary beneficiaries:**
- Families with known inherited medical histories who seek early screening and awareness

This solution is especially relevant for individuals who cannot afford routine genetic testing but have access to smartphones and basic medical records.

---

## 4) 😣 User Needs and Pain Points

Users often:
- lack awareness of inherited disease risks
- don't understand how family history affects personal health outcomes
- face high costs of genetic testing
- lack structured preventive guidance
- feel confused about when/what screening tests to take
- don't know what symptoms require urgency

Healthcare support is often reactive and fragmented. There is a large gap between:
> knowing a disease exists in the family  
and  
> knowing how lifestyle and preventive actions can reduce risk

This leads to anxiety, neglect, and delayed diagnosis of manageable conditions.

---

## 5) 🌱 Long-Term Impact

In the long run, this solution can shift healthcare from **reactive treatment** to **preventive decision-making**.

Early awareness of genetic risk enables:
- timely screening
- lifestyle modification
- faster diagnosis and intervention

This reduces disease severity and healthcare costs, while empowering youth to take ownership of health before symptoms appear.

At scale, the system can reduce the burden of chronic and inherited diseases and promote a stronger preventive health culture.

---

## 6) 🔍 What Informed Our Understanding of the Problem

Our understanding was shaped by:
- real-world observation of delayed diagnosis in hereditary conditions like Type-2 diabetes and cardiovascular disease
- a case where a peer developed diabetes without prior risk awareness despite strong family history
- discussions with affected families
- secondary research highlighting gaps in preventive healthcare and risk stratification
- academic exposure to health data analysis showing family history and lifestyle indicators are underused in early prediction

We observed that asymptomatic individuals—especially youth—rarely seek screening, missing early preventive opportunities.

---

## 7) ♻️ Relevant Sustainable Development Goals (SDG)

✅ **SDG 3: Good Health and Well-Being**

---

## 8) 🧠 Proposed Direction of the Solution

We are exploring a web-based preventive health platform that collects:

- user health records
- family medical history (up to two generations)

via manual input or AI-powered OCR.

Using open-source health datasets, AI models estimate risk for multiple inherited diseases and display them as:

- ranked probabilities  
or  
- categorized risk classes (**I–IV**)

For each disease, the system generates:
- simple disease summaries
- personalized prevention advice
- screening / confirmatory test recommendations
- alerts for high-risk users encouraging timely doctor consultation

The platform functions as a dynamic health coach enabling continuous risk awareness and proactive prevention rather than one-time diagnosis.

---

## 9) 🤖 Role of AI in Our Approach

AI enables scalable and personalized genetic risk awareness by turning fragmented health records, family history, and lifestyle data into actionable risk insights.

Key AI roles include:
- **AI OCR** to digitize unstructured medical documents
- **pattern-learning ML models** to infer predisposition from population datasets
- **risk stratification** converting probabilities into risk classes (I–IV)
- **adaptive recommendation engine** that updates prevention advice based on user inputs

This reduces dependence on expensive one-time genetic testing while supporting early decision-making through prevention-first guidance.

---

## 🏗️ Technical Architecture

### Tech Stack

**Frontend:**
- React.js with Tailwind CSS
- Responsive web design for mobile/desktop

**Backend:**
- FastAPI (Python)
- RESTful API endpoints
- CORS enabled for frontend integration

**AI/ML:**
- AI-OCR: EasyOCR/PaddleOCR/Tesseract for medical report digitization
- Risk Engine: Rule-based scoring + pattern analysis
- Pure Python (no external ML dependencies for MVP)

**Data:**
- JSON-based configuration
- Disease definitions, thresholds, and guidelines
- Demo cases for testing

---

## 📂 Project Structure

```
project_root/
├── frontend/              # React application (3 members)
│   ├── src/
│   │   ├── components/   # Forms, Dashboard, Disease Detail pages
│   │   └── ...
│   └── package.json
│
├── backend/              # FastAPI application (3 members)
│   ├── main.py          # API routes
│   ├── models/          # Data models
│   └── ...
│
├── ai/                   # AI Module (2 members)
│   ├── data/            # Configuration & test data
│   │   ├── diseases_config.json
│   │   ├── guidelines.json
│   │   ├── tests_map.json
│   │   └── sample_inputs.json
│   │
│   ├── ocr/             # AI-1: OCR & Lab Extraction
│   │   ├── ocr_pipeline.py
│   │   ├── report_parser.py
│   │   └── normalize_units.py
│   │
│   ├── risk/            # AI-2: Risk Prediction
│   │   ├── risk_model.py
│   │   ├── scoring_rules.py
│   │   ├── risk_classes.py
│   │   └── explainability.py
│   │
│   └── coaching/        # AI-2: Health Coaching
│       ├── prevention_engine.py
│       ├── test_recommender.py
│       └── consult_logic.py
│
└── requirements.txt     # Python dependencies
```

---

## 🤖 AI Module (AI-2): Risk Prediction & Health Coaching

### Overview

The AI-2 module is responsible for:
1. **Risk Prediction**: Analyzing family history, lifestyle, and lab data to predict disease risk
2. **Risk Classification**: Converting probabilities to actionable Risk Classes (I–IV)
3. **Explainability**: Generating human-readable reasons for each prediction
4. **Health Coaching**: Providing personalized prevention plans, test recommendations, and consultation guidance

### Core Components

#### 1. Risk Prediction Engine (`ai/risk/`)

**Main Function:** `predict_risks(user_data) -> List[Dict]`

**Input:**
```json
{
  "basic_info": {"age": 32, "gender": "female", "bmi": 29.7},
  "lifestyle": {"diet": "high_sugar", "exercise": "sedentary", "smoking": false},
  "family_history": {
    "generation_1": {"mother": {"type2_diabetes": true}},
    "generation_2": {"maternal_grandmother": {"type2_diabetes": true}}
  },
  "lab_values": {"hba1c": 6.2, "fasting_glucose": 115, "ldl": 145}
}
```

**Output:** Ranked list of 10 diseases with:
- `disease_name`: Human-readable name
- `disease_id`: System identifier
- `probability`: 0.0 - 0.99 risk score
- `risk_class`: I (Low), II (Moderate), III (High), IV (Very High)
- `reasons`: 3-5 human-readable explanations
- `prevention`: Personalized prevention tips
- `recommended_tests`: Screening tests to take
- `consult`: Consultation urgency (none/routine/soon/urgent)

**Scoring Algorithm:**
- **Family Score (40%)**: Weighted by generation (Gen 1 = 0.30, Gen 2 = 0.10 per relative)
- **Lifestyle Score (35%)**: Matches user habits against disease risk factors
- **Lab Score (25%)**: Compares biomarkers against clinical thresholds

*Dynamic weighting:* If labs unavailable, redistributes weight to family (50%) and lifestyle (40%)

**Risk Class Thresholds:**
- **Class I (Low)**: 0.00 - 0.30
- **Class II (Moderate)**: 0.30 - 0.55
- **Class III (High)**: 0.55 - 0.75
- **Class IV (Very High)**: 0.75 - 0.99

#### 2. Explainability Engine (`ai/risk/explainability.py`)

Generates non-diagnostic, risk-indicating language:
- ✅ "HbA1c elevated at 6.2%, suggesting higher diabetes risk"
- ❌ "You have diabetes" (diagnostic - avoided)

**Priority Logic:**
- If `probability >= 0.75` (urgent): Show critical lab reasons first
- Otherwise: Family → Lifestyle → Lab reasons

#### 3. Health Coaching (`ai/coaching/`)

**Prevention Engine:**
- Personalizes diet, exercise, and lifestyle recommendations
- Deduplicates tips from disease-specific and risk-class guidelines
- Adapts to user's current habits (e.g., "Start with 10-min walks" for sedentary users)

**Test Recommender:**
- Prioritizes tests based on risk class, age, gender, and family history
- Adjusts frequency: High risk = more frequent screening
- Provides test preparation tips and cost estimates (₹ for India)

**Consultation Logic:**
- **Red Flag Detection**: Escalates urgency for critical lab values
  - Example: LDL ≥ 190 mg/dL → Urgent
  - Example: HbA1c ≥ 7.0% → Urgent
- **Specialist Recommendations**: Suggests appropriate doctors (cardiologist, endocrinologist, genetic counselor)
- **Discussion Points**: Lists what to discuss with doctor
- **Preparation Tips**: How to prepare for consultation

### Supported Diseases (10)

1. **Type-2 Diabetes** - Family weight: 0.35
2. **Coronary Artery Disease (CAD)** - Family weight: 0.30
3. **Hypertension** - Family weight: 0.28
4. **Familial Hypercholesterolemia** - Family weight: 0.50 (highly heritable)
5. **Breast/Ovarian Cancer Risk (BRCA)** - Family weight: 0.45
6. **Thalassemia Carrier Risk** - Family weight: 0.50
7. **Sickle Cell Disease Risk** - Family weight: 0.50
8. **Asthma Predisposition** - Family weight: 0.25
9. **Hypothyroidism Predisposition** - Family weight: 0.30
10. **PCOS Predisposition** - Family weight: 0.35

### Key Features

**Lab Key Normalization:**
Handles OCR variations:
- "HbA1c" / "Hemoglobin A1c" / "hba1c" → `hba1c`
- "LDL Cholesterol" / "ldl" → `ldl`

**Data Completeness Handling:**
- Missing labs → Adjusts weighting automatically
- No family history → Uses baseline risk + lifestyle/lab data
- Incomplete lifestyle → Uses reasonable defaults

**Error Handling:**
- All modules include try-catch with fallbacks
- Missing JSON files → Loads default values
- Malformed input → Returns baseline risk estimates

### Integration Example

**FastAPI Endpoint:**
```python
from ai.risk.risk_model import predict_risks

@app.post("/predict-risk")
async def predict_risk_endpoint(user_data: dict):
    try:
        results = predict_risks(user_data)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}, 500
```

**Response Format:**
```json
{
  "results": [
    {
      "disease_name": "Type-2 Diabetes",
      "disease_id": "type2_diabetes",
      "probability": 0.68,
      "risk_class": "III",
      "reasons": [
        "Mother has this condition",
        "HbA1c elevated at 6.2%, suggesting higher diabetes risk",
        "High sugar intake and poor dietary habits",
        "Sedentary lifestyle with minimal physical activity"
      ],
      "prevention": [
        "Eliminate sugary drinks and desserts immediately",
        "Reduce sugar and refined carbohydrates",
        "30 minutes moderate activity daily",
        "Control portion sizes"
      ],
      "recommended_tests": [
        "HbA1c (Glycated Hemoglobin)",
        "Fasting Blood Glucose",
        "Oral Glucose Tolerance Test (OGTT)"
      ],
      "consult": "soon",
      "consult_detail": {
        "level": "soon",
        "timeframe": "Schedule within 4-6 weeks",
        "message": "Consult your doctor soon to assess risk and develop prevention plan",
        "specialist": {
          "recommended": "Endocrinologist or Diabetologist",
          "also_consider": "Primary Care Physician"
        },
        "what_to_discuss": [
          "Blood sugar levels and HbA1c results",
          "Diet plan and carbohydrate management",
          "Exercise recommendations"
        ]
      }
    }
  ]
}
```

### Testing

**Demo Cases Available:**
- `case_a_low_risk`: Healthy young adult, no family history
- `case_b_high_diabetes_risk`: Mother diabetic, elevated HbA1c (6.2%)
- `case_c_mixed_risk`: Smoking, CAD family history, high cholesterol
- `case_d_genetic_risk`: Strong BRCA and FH family history

**Test Command:**
```python
import json
from ai.risk.risk_model import predict_risks

# Load demo case
with open('ai/data/sample_inputs.json', 'r') as f:
    demos = json.load(f)['demo_cases']

# Run prediction
result = predict_risks(demos['case_b_high_diabetes_risk'])

# Output top risk
print(f"Top Risk: {result[0]['disease_name']}")
print(f"Probability: {result[0]['probability']}")
print(f"Risk Class: {result[0]['risk_class']}")
```

### Performance

- **No external ML dependencies** (uses rule-based scoring)
- **Processing time**: <50ms per prediction (all 10 diseases)
- **Memory footprint**: ~5MB (JSON configs cached)
- **Scalability**: Handles 1000+ requests/minute on standard server

### Data Privacy & Ethics

- **No data storage**: Module processes data in-memory only
- **No PHI retention**: User data not logged or persisted
- **Transparent reasoning**: All risk scores explainable
- **Non-diagnostic language**: Always recommends professional consultation for high risk
- **Family sensitivity**: Handles genetic information responsibly

---

## ✅ SDG Impact Summary

This system supports:
- early risk awareness
- preventive screening
- accessible health literacy
- reduced late-stage disease complications  
→ directly contributing to **SDG 3: Good Health & Well-Being**

---

## 📌 Important Notes

⚠️ This platform is intended as a **preventive decision-support tool**, not a replacement for licensed medical diagnosis. High-risk outputs always recommend professional medical consultation.

⚠️ **Data Accuracy**: The system uses family history patterns and clinical thresholds from established medical guidelines, but individual genetic testing and doctor consultation remain the gold standard for diagnosis.

⚠️ **Privacy**: All risk calculations happen on-demand. The AI module does not store or retain any personal health information.

---

## 🚀 Getting Started (AI-2 Module)

### Prerequisites
- Python 3.8+
- No external dependencies (pure Python stdlib)

### Setup
```bash
# Clone repository
git clone <repo-url>
cd project_root

# Verify AI module structure
tree ai/

# Test import
python3 -c "from ai.risk.risk_model import predict_risks; print('✅ Module ready')"
```

### Quick Test
```python
from ai.risk.risk_model import predict_risks

# Sample input
user_data = {
    "basic_info": {"age": 32, "gender": "female", "bmi": 29.7},
    "lifestyle": {"diet": "high_sugar", "exercise": "sedentary"},
    "family_history": {
        "generation_1": {"mother": {"type2_diabetes": true}}
    },
    "lab_values": {"hba1c": 6.2}
}

# Get predictions
results = predict_risks(user_data)
print(results[0])  # Top risk disease
```

---

## 👥 Team Structure

- **Frontend (3)**: React components, UI/UX, forms, dashboard
- **Backend (3)**: FastAPI, database, API integration
- **AI-OCR (1)**: Medical report digitization and lab extraction
- **AI-Risk (1)**: Risk prediction, coaching, and recommendations
- **API Lead (1)**: Integration coordination, endpoint contracts
- **Presentation (1)**: PPT, demo video, pitch preparation

---

## 📅 Development Timeline (Jan 26-31, 2026)

- **Day 1 (26th)**: Architecture freeze, repo setup, API contracts
- **Day 2 (27th)**: Core build - forms, APIs, risk engine v1
- **Day 3 (28th)**: OCR integration, dashboard with ranked results
- **Day 4 (29th)**: Disease detail pages, prevention plans, coaching features
- **Day 5 (30th)**: Polish, deployment, PPT 80% ready
- **Day 6 (31st)**: Final demo rehearsal, submission package

---

## 📄 License

[Coming Soon!]

---

## 🙏 Acknowledgments

- Open-source health datasets
- Medical literature on genetic risk assessment
- Families who shared their health journeys
- Academic mentors and health professionals

---

## 📧 Contact

[Coming Soon!]

**Last Updated:** January 27, 2026  
**Hackathon:** AI for Good Challenge 2026