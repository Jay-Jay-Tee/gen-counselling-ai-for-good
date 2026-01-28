# Health Risk Assessment - Frontend Application

Complete React application for the Gen Counselling AI for Good Hackathon project.

## 📋 Project Overview

This is a multi-step health risk assessment application that collects user data (basic info, lifestyle, family history) and displays personalized disease risk predictions with prevention strategies.

### Forms & Validation
**Completed Components:**
- ✅ Landing Page (`LandingPage.jsx`)
- ✅ Registration/Basic Info Form (`RegistrationForm.jsx`)
  - Age, Gender, Height, Weight inputs
  - Auto-calculated BMI
  - Full validation with React Hook Form
- ✅ Lifestyle Form (`LifestyleForm.jsx`)
  - Smoking, Alcohol, Diet, Exercise, Stress, Sleep Hours
  - Dropdown and radio button inputs
- ✅ Family History Form (`FamilyHistoryForm.jsx`)
  - Dynamic family members across 3 generations
  - Parents (Gen 1) - Fixed
  - Siblings (Gen 0) - Dynamic add/remove
  - Children (Gen -1) - Dynamic add/remove
  - Grandparents & Extended (Gen 2) - Fixed grandparents, dynamic aunts/uncles
  - 10 disease checkboxes per family member
  - Converts to API-ready JSON format

### Results Dashboard 
**Completed Components:**
- ✅ Results Dashboard (`ResultsDashboard.jsx`)
  - Risk Class Legend (I-IV with colors)
  - Top 5 Risk Factors Bar Chart (using Recharts)
  - Sortable results table
  - Color-coded risk classes and urgency badges
  - Loading states and error handling
  - Click rows to navigate to disease details

### Disease Detail & OCR
**Completed Components:**
- ✅ Upload Report Component (`UploadReport.jsx`)
  - Drag & drop file upload
  - Support for PDF, PNG, JPG
  - OCR extraction of lab values
  - Display extracted values
  - Skip option available
- ✅ Disease Detail Page (`DiseaseDetail.jsx`)
  - Disease header with risk class badge
  - Risk progress bar
  - What This Means section
  - Why You're At Risk (reasons)
  - Prevention Plan
  - Recommended Screening Tests
  - Doctor Consultation guidance
  - Back navigation

## 🛠️ Tech Stack

- **React 18** - UI Framework
- **React Router DOM** - Navigation
- **React Hook Form** - Form validation
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Recharts** - Data visualization
- **Vite** - Build tool

## 📦 Installation

```bash
# Navigate to project directory
cd health-app

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will open at `http://localhost:3000`

## 🏗️ Project Structure

```
health-app/
├── src/
│   ├── pages/
│   │   ├── LandingPage.jsx          # Landing page with "Get Started"
│   │   ├── RegistrationForm.jsx     # Step 1: Basic info + BMI
│   │   ├── LifestyleForm.jsx        # Step 2: Lifestyle factors
│   │   ├── FamilyHistoryForm.jsx    # Step 3: Family medical history
│   │   ├── UploadReport.jsx         # Step 4: OCR lab report upload
│   │   ├── ResultsDashboard.jsx     # Results page with charts
│   │   └── DiseaseDetail.jsx        # Individual disease details
│   ├── App.jsx                      # Main app with routing
│   ├── main.jsx                     # Entry point
│   └── index.css                    # Tailwind imports
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## 🔄 Data Flow

### 1. Form Data Collection
```javascript
{
  patient: {                    
    age: 32,
    gender: "F",                
    height: 162,
    weight: 78.5,
    race: "asian",              
    known_issues: []            
    // Note: BMI removed - calculated on backend
  },
  lifestyle: {
    smoking: false,
    alcohol: "occasional",
    exercise: "sedentary",
    diet: "high_sugar",
    sleep_hours: 6.5,
    stress_level: "high"
  },
  family: [                     
    {
      role: "mother",
      generation: 1,
      known_issues: ["type2_diabetes", "hypertension"] 
    },
    {
      role: "maternal_aunt",
      generation: 2,
      known_issues: ["breast_ovarian_cancer"]
    }
  ],
  lab_values: {
    hba1c: 6.2,                
    fasting_glucose: 115,
    ldl: 145,
    hdl: 38,
    triglycerides: 180,
    systolic_bp: 135,
    diastolic_bp: 88
  }
}
```

### 2. API Integration
All forms feed data into the main `formData` state in `App.jsx`, which is then sent to:

**POST** `/predict-risk`
- Sends complete formData with new structure
- Returns disease predictions with:
  - `disease_id` (e.g., "type2_diabetes")
  - `probability` (decimal 0-1, e.g., 0.82)
  - `risk_class` (I-IV)
  - `consult` level (none/routine/soon/urgent)
  - Detailed `consult_detail` object

**POST** `/ocr`
- Uploads lab report file
- Extracts lab values from PDF/image
- Returns numeric lab_values object

**GET** `/disease/:diseaseId`
- Fetches detailed information using disease_id (not disease_name)
- Returns comprehensive disease information

## 🎨 Design Features

### Risk Classes
- **Class I (Green)**: Low Risk - #22c55e
- **Class II (Yellow)**: Moderate Risk - #eab308
- **Class III (Orange)**: High Risk - #f97316
- **Class IV (Red)**: Very High Risk - #ef4444

### Urgency Levels
- None (Gray)
- Routine (Blue)
- Soon (Orange)
- Urgent (Red)

### Responsive Design
- Mobile-first approach
- Tailwind CSS utilities
- Smooth transitions and hover states

## ✅ Validation Rules

### Registration Form
- Age: 15-100
- Height: 100-250 cm
- Weight: 30-300 kg
- All fields required

### Lifestyle Form
- All dropdowns required
- Sleep hours: 0-12
- Radio buttons for smoking

### Family History
- Minimum: Parents + Grandparents (fixed)
- Can add unlimited siblings, children, aunts, uncles
- Each member has 10 disease checkboxes

## 🚀 Key Features

1. **Multi-step Form Flow**
   - Progress bar shows completion
   - Back/Next navigation
   - Form state persists across steps

2. **Dynamic Family Members**
   - Add/remove siblings, children, extended family
   - Fixed core family (parents, grandparents)
   - Disease checkboxes for each member

3. **Auto-calculations**
   - BMI calculated from height/weight
   - Real-time updates

4. **OCR Upload**
   - Drag & drop interface
   - File type validation
   - Extract lab values from reports

5. **Interactive Results**
   - Sortable table
   - Click rows for details
   - Visual charts
   - Risk class color coding

6. **Disease Details**
   - Comprehensive information
   - Prevention strategies
   - Recommended tests
   - Doctor consultation guidance

## 🔌 API Endpoints Expected

```javascript
// Risk Prediction
POST http://localhost:8000/predict-risk
Body: formData object
Response: { results: [...] }

// OCR Extraction
POST http://localhost:8000/ocr
Body: FormData with file
Response: { lab_values: {...} }

// Disease Details
GET http://localhost:8000/disease/:diseaseName
Response: { disease_name, description, reasons, prevention, ... }
```

## 📱 User Journey

1. **Landing Page** → Click "Get Started"
2. **Registration** → Enter basic info → BMI auto-calculates
3. **Lifestyle** → Select lifestyle factors
4. **Family History** → Add family members & diseases
5. **Upload Report** → Optional OCR upload
6. **Results Dashboard** → View all risk predictions
7. **Disease Detail** → Click any disease for detailed guidance


## 🐛 Error Handling

- Form validation errors (inline messages)
- API connection failures (retry button)
- Loading states for all async operations
- File upload validation (type, size)

## 🎉 Demo Ready Features

- Fully functional forms with validation
- Smooth multi-step navigation
- Professional UI with Tailwind
- Interactive charts
- Responsive design
- Error states and loading indicators

## 📝 Notes

- Backend API must be running on `http://localhost:8000`
- Mock data fallback in DiseaseDetail component for testing
- All 10 diseases supported in family history
- File size limit: 10MB for uploads

## 🚀 Deployment

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```
