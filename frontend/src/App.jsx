import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import RegistrationForm from './pages/RegistrationForm';
import LifestyleForm from './pages/LifestyleForm';
import FamilyHistoryForm from './pages/FamilyHistoryForm';
import UploadReport from './pages/UploadReport';
import ResultsDashboard from './pages/ResultsDashboard';
import DiseaseDetail from './pages/DiseaseDetail';
import Assessment from './pages/Assessment';

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
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            
            {/* Combined Assessment Flow */}
            <Route 
              path="/assessment" 
              element={<Assessment />} 
            />
            
            {/* Individual Form Routes (legacy support) */}
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
            
            {/* Results */}
            <Route 
              path="/results" 
              element={<ResultsDashboard formData={formData} />} 
            />
            
            {/* Disease Details */}
            <Route 
              path="/disease/:diseaseName" 
              element={<DiseaseDetail />} 
            />
            
            {/* Catch all */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
