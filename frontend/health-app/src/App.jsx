import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import RegistrationForm from './pages/RegistrationForm';
import LifestyleForm from './pages/LifestyleForm';
import FamilyHistoryForm from './pages/FamilyHistoryForm';
import UploadReport from './pages/UploadReport';
import ResultsDashboard from './pages/ResultsDashboard';
import DiseaseDetail from './pages/DiseaseDetail';

function App() {
  const [formData, setFormData] = useState({
    patient: {},
    lifestyle: {},
    family: [],
    lab_values: {}
  });

  const updateFormData = (section, data) => {
    setFormData(prev => ({
      ...prev,
      [section]: data
    }));
  };

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route 
            path="/registration" 
            element={<RegistrationForm formData={formData} updateFormData={updateFormData} />} 
          />
          <Route 
            path="/lifestyle" 
            element={<LifestyleForm formData={formData} updateFormData={updateFormData} />} 
          />
          <Route 
            path="/family-history" 
            element={<FamilyHistoryForm formData={formData} updateFormData={updateFormData} />} 
          />
          <Route 
            path="/upload-report" 
            element={<UploadReport formData={formData} updateFormData={updateFormData} />} 
          />
          <Route 
            path="/results" 
            element={<ResultsDashboard formData={formData} />} 
          />
          <Route 
            path="/disease/:diseaseName" 
            element={<DiseaseDetail />} 
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
