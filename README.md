# 🧬 Gen Counselling AI for Good

**AI-Powered Genetic Risk Assessment & Health Coaching Platform**

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![Made for](https://img.shields.io/badge/made%20for-AI%20for%20Good-red.svg)]()

> **Empowering individuals to understand their genetic health risks and take preventive action before diseases develop.**

[Demo](#-live-demo) · [Features](#-key-features) · [Quick Start](#-quick-start) · [Documentation](#-documentation)

---

## 🎯 What is This?

Gen Counselling AI is a **web-based preventive health platform** that predicts inherited disease risks using family history, lifestyle data, and lab values. It provides:

- 🎲 **Risk predictions** for 10 major inherited diseases
- 📊 **Risk classification** (Class I-IV) with clear explanations
- 💡 **Personalized prevention plans** tailored to your profile
- 🩺 **Screening recommendations** for early detection
- ⚕️ **Consultation guidance** based on risk severity

**No genetic testing required.** Just answer questions about your family, lifestyle, and health.

---

## 🚨 The Problem We're Solving

### Silent Genetic Risks

Millions unknowingly carry genetic predispositions to diseases like:
- Type-2 Diabetes
- Heart Disease (CAD)
- BRCA-related Cancers
- Thalassemia & Sickle Cell
- Familial Hypercholesterolemia

**The Issue:**
- 🔴 Risks stay hidden until symptoms appear
- 🔴 Young adults rarely get preventive screening
- 🔴 Genetic testing is expensive & inaccessible
- 🔴 Healthcare reacts *after* disease onset

**Our Solution:** Early, accessible, explainable risk awareness.

---

## ✨ Key Features

### 🎯 Intelligent Risk Assessment
- **10 disease predictions** in one assessment
- **Evidence-based scoring** using medical guidelines
- **Explainable results** - know exactly why your risk is high
- **No black box** - transparent rule-based system

### 👨‍⚕️ Personalized Health Coaching
- **Custom prevention plans** based on your lifestyle
- **Recommended tests** with frequency and cost estimates
- **Urgency levels** (routine/soon/urgent consultation)
- **Action timelines** - what to do this week, month, year

### 📸 Smart Lab Report Processing *(Coming Soon)*
- **AI-powered OCR** to read medical reports
- **Automatic extraction** of lab values
- **Multi-format support** (images, PDFs)

### 🎨 User-Friendly Interface
- **Multi-step assessment** (profile, lifestyle, family history)
- **Visual risk dashboard** with clear risk classes
- **Detailed disease pages** with simple explanations
- **Mobile-responsive** design

---

## 🏗️ How It Works

### Our Approach: Rule-Based Expert System

We use a **transparent, explainable AI model** based on clinical guidelines:

```
Risk Score = (Family History × 40%) + (Lifestyle × 35%) + (Lab Values × 25%)

Then classify:
• Class I (Low):       0-29% risk
• Class II (Moderate): 30-54% risk
• Class III (High):    55-74% risk
• Class IV (Very High): 75-99% risk
```

**Why rule-based?**
- ✅ **Explainable** - can explain every prediction
- ✅ **Trustworthy** - based on medical research
- ✅ **No training data needed** - privacy-friendly
- ✅ **Transparent** - not a black box
- ✅ **Regulatory-friendly** - auditable logic

### Disease Coverage

| Disease | Family Weight | Key Risk Factors |
|---------|---------------|------------------|
| Type-2 Diabetes | 35% | High sugar, sedentary, obesity, family history |
| Coronary Artery Disease | 30% | Smoking, high-fat diet, high cholesterol |
| Hypertension | 28% | High salt, alcohol, stress, obesity |
| Familial Hypercholesterolemia | 50% | Strong genetic component, high LDL |
| BRCA (Breast/Ovarian Cancer) | 45% | Family history, hormones, lifestyle |
| Thalassemia | 50% | Pure genetic (carrier risk) |
| Sickle Cell Disease | 50% | Pure genetic (carrier risk) |
| Asthma | 25% | Allergens, pollution, family history |
| Hypothyroidism | 30% | Family history, iodine deficiency |
| PCOS | 35% | Obesity, sedentary lifestyle |

---

## 🚀 Quick Start

### Prerequisites

**Backend:**
- Python 3.8+
- pip

**Frontend:**
- Node.js 16+
- npm or yarn

### Installation (5 minutes)

#### 1. Clone Repository
```bash
git clone https://github.com/Jay-Jay-Tee/gen-counselling-ai-for-good.git
cd gen-counselling-ai-for-good
```

#### 2. Setup Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

#### 3. Setup Frontend (New Terminal)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:5173`

#### 4. Test It Works
```bash
# Health check
curl http://localhost:8000/health

# Expected: {"status":"healthy","service":"Genetic Risk Coach API"}
```

### Using the App

1. **Open browser:** `http://localhost:5173`
2. **Fill assessment:**
   - Personal info (age, gender, height, weight)
   - Lifestyle (diet, exercise, smoking, stress)
   - Family history (parents, siblings with diseases)
   - Lab values (HbA1c, cholesterol, etc.)
3. **Get results:** See risk predictions for 10 diseases
4. **Explore details:** Click any disease for prevention plans

---

## 📁 Project Structure

```
gen-counselling-ai-for-good/
│
├── frontend/                   # React + Vite + Tailwind
│   ├── src/
│   │   ├── api/               # API integration layer
│   │   │   ├── client.js      # Axios configuration
│   │   │   ├── predict.js     # Risk prediction endpoint
│   │   │   ├── ocr.js         # OCR endpoint
│   │   │   └── diseases.js    # Disease info endpoint
│   │   ├── pages/             # Main screens
│   │   │   ├── LandingPage.jsx
│   │   │   ├── RegistrationForm.jsx
│   │   │   ├── LifestyleForm.jsx
│   │   │   ├── FamilyHistoryForm.jsx
│   │   │   ├── UploadReport.jsx
│   │   │   ├── ResultsDashboard.jsx
│   │   │   └── DiseaseDetail.jsx
│   │   ├── App.jsx            # Routing
│   │   └── main.jsx           # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app & CORS
│   │   ├── config.py          # Environment config
│   │   ├── routers/           # API endpoints
│   │   │   ├── predict.py     # /predict-risk
│   │   │   ├── ocr.py         # /ocr
│   │   │   └── diseases.py    # /disease-info
│   │   ├── schemas/           # Pydantic models
│   │   │   ├── prediction.py
│   │   │   ├── profile.py
│   │   │   ├── lifestyle.py
│   │   │   ├── family.py
│   │   │   └── lab_values.py
│   │   └── services/          # Business logic
│   │       ├── prediction_service.py
│   │       ├── ocr_service.py
│   │       └── disease_service.py
│   └── requirements.txt
│
├── ai/                         # AI Module (Rule-based Engine)
│   ├── risk/                  # Risk prediction
│   │   ├── risk_model.py      # Main prediction function
│   │   ├── scoring_rules.py   # Scoring logic
│   │   ├── risk_classes.py    # Classification (I-IV)
│   │   └── explainability.py  # Reason generation
│   ├── coaching/              # Health coaching
│   │   ├── prevention_engine.py
│   │   ├── test_recommender.py
│   │   └── consult_logic.py
│   ├── ocr/                   # OCR pipeline (in progress)
│   │   └── ocr_pipeline.py
│   ├── data/                  # Configuration
│   │   ├── diseases_config.json
│   │   ├── guidelines.json
│   │   ├── tests_map.json
│   │   └── sample_inputs.json
│   └── requirements.txt
│
├── docs/                       # Documentation
│   └── api_contract.json
│
└── requirements.txt           # Root dependencies
```

---

## 🔬 Technology Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **Lucide React** - Icons

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Python 3.8+** - Language

### AI Module
- **Pure Python** - No ML frameworks needed
- **Rule-based system** - Transparent logic
- **EasyOCR** - Optical character recognition
- **OpenCV** - Image processing
- **NumPy** - Numerical operations

---

## 📖 API Documentation

### Endpoints

#### 1. Health Check
```bash
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "Genetic Risk Coach API",
  "version": "1.0.0"
}
```

#### 2. Predict Risk
```bash
POST /api/predict-risk/
```

**Request:**
```json
{
  "patient": {
    "age": 32,
    "gender": "female",
    "height": 165,
    "weight": 75,
    "race": "asian",
    "known_issues": []
  },
  "lifestyle": {
    "smoking": false,
    "alcohol": "occasional",
    "exercise": "sedentary",
    "diet": "high_sugar",
    "sleep_hours": 6,
    "stress_level": "high"
  },
  "family": [
    {
      "role": "mother",
      "generation": 1,
      "age": 58,
      "gender": "female",
      "known_issues": ["type2_diabetes"]
    }
  ],
  "lab_values": {
    "hba1c": 6.2,
    "fasting_glucose": 115,
    "ldl": 145,
    "hdl": 42
  }
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "disease_name": "Type-2 Diabetes",
      "disease_id": "type2_diabetes",
      "probability": 0.71,
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
        "specialist": {
          "recommended": "Endocrinologist or Diabetologist"
        }
      }
    }
    // ... 9 more diseases
  ]
}
```

#### 3. OCR Upload *(In Progress)*
```bash
POST /api/ocr/
```
Upload medical report image/PDF for automatic lab value extraction.

#### 4. Disease Info
```bash
GET /api/disease-info/{disease_id}
```
Get detailed information about a specific disease.

**Interactive API Docs:** `http://localhost:8000/docs`

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Run AI Module Tests
```bash
cd ai
python3 -c "
from risk.risk_model import predict_risks
import json

with open('data/sample_inputs.json', 'r') as f:
    data = json.load(f)

result = predict_risks(data['demo_cases']['case_b_high_diabetes_risk'])
print(f'Top Risk: {result[0][\"disease_name\"]} - {result[0][\"probability\"]}')
"
```

### Test API Endpoint
```bash
curl -X POST http://localhost:8000/api/predict-risk/ \
  -H "Content-Type: application/json" \
  -d @ai/data/sample_inputs.json
```

---

## 🎯 Demo Scenarios

### Scenario 1: High Diabetes Risk (Sarah, 32)
- **Profile:** Female, 32, BMI 30.1 (obese)
- **Lifestyle:** Sedentary, high sugar diet, poor sleep
- **Family:** Mother and sister have diabetes
- **Labs:** HbA1c 6.2%, glucose 115 mg/dL
- **Result:** **Class III (High Risk)** - 71% probability

### Scenario 2: Low Risk (John, 25)
- **Profile:** Male, 25, BMI 22 (normal)
- **Lifestyle:** Active, balanced diet, no smoking
- **Family:** No known diseases
- **Labs:** All normal
- **Result:** **Class I (Low Risk)** for all diseases

### Scenario 3: BRCA High Risk (Emma, 38)
- **Profile:** Female, 38
- **Family:** Mother had breast cancer at 42, grandmother ovarian cancer
- **Result:** **Class IV (Very High)** - urgent genetic counseling recommended

---

## 🔐 Privacy & Ethics

### Data Handling
- ✅ **No data storage** - All processing in-memory
- ✅ **No user accounts** required (MVP)
- ✅ **No PHI retention** - Data never logged
- ✅ **Client-side option** - Can run locally

### Medical Disclaimer
⚠️ **This platform is for educational and preventive awareness only.**
- Not a diagnostic tool
- Not a replacement for professional medical advice
- Always consult healthcare providers for medical decisions
- High-risk results require professional evaluation

### Ethical Considerations
- ✅ **Transparent** - Explainable predictions
- ✅ **Non-diagnostic** language used
- ✅ **Empowering** - Focus on prevention
- ✅ **Accessible** - Free to use
- ✅ **Privacy-first** - No genetic data collected

---

## 🎓 Scientific Basis

### Our Risk Model Uses:

**Family History Weighting:**
- Based on Mendelian inheritance patterns
- Generation proximity (parents > grandparents)
- Disease-specific heritability (BRCA: 50%, CAD: 30%)

**Lifestyle Factors:**
- Evidence from epidemiological studies
- Framingham Heart Study guidelines
- ADA diabetes prevention research

**Lab Value Thresholds:**
- **HbA1c ≥6.5%:** ADA diabetic threshold
- **LDL ≥190 mg/dL:** ACC/AHA very high risk
- **BP ≥140/90:** JNC-8 hypertension Stage 2

**References:**
- American Diabetes Association (ADA) Standards of Care
- American College of Cardiology (ACC/AHA) Guidelines
- National Comprehensive Cancer Network (NCCN) Guidelines
- Published peer-reviewed research on genetic risk

---

## 🗺️ Roadmap

### ✅ Completed (MVP)
- [x] Rule-based risk prediction for 10 diseases
- [x] Web-based assessment interface
- [x] Explainable results with reasons
- [x] Personalized prevention plans
- [x] Test recommendations
- [x] Consultation urgency levels
- [x] REST API with documentation

### 🔄 In Progress
- [ ] OCR for medical reports
- [ ] Enhanced UI/UX
- [ ] Error handling & validation

### 🔮 Future Enhancements
- [ ] User accounts & history tracking
- [ ] Downloadable PDF reports
- [ ] Multi-language support
- [ ] Mobile app (iOS/Android)
- [ ] Integration with wearables
- [ ] Machine learning enhancements
- [ ] Genetic test integration
- [ ] Telemedicine partnerships

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas to Contribute
- 🎨 UI/UX improvements
- 🧪 Testing & validation
- 📚 Documentation
- 🔬 Additional disease models
- 🌍 Internationalization
- ♿ Accessibility features

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**AI for Good Hackathon 2026**

- **AI Team (2):** Risk prediction engine & OCR
- **Backend Team (3):** FastAPI development
- **Frontend Team (3):** React UI/UX
- **Integration Lead (1):** API coordination

---

## 🙏 Acknowledgments

- Medical guidelines from ADA, ACC/AHA, NCCN
- Open-source community
- Families sharing health journeys
- Healthcare professionals providing guidance

---

## 📞 Support & Contact

**Issues?** [Open an issue](https://github.com/Jay-Jay-Tee/gen-counselling-ai-for-good/issues)

**Questions?** Check our [Documentation](#-api-documentation) or [Quick Start](#-quick-start)

---

## 🌟 Star Us!

If you find this project useful, please ⭐ star the repository to show support!

---

<div align="center">

**Built with ❤️ for preventive healthcare**

[⬆ Back to top](#-gen-counselling-ai-for-good)

</div>