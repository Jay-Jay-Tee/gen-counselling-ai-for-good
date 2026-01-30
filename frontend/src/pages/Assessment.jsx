import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ProgressStepper from '../components/ProgressStepper';
import RegistrationForm from './RegistrationForm';
import LifestyleForm from './LifestyleForm';
import FamilyHistoryForm from './FamilyHistoryForm';
import UploadReport from './UploadReport';

function Assessment() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    patient: {},
    lifestyle: {},
    family: [],
    lab_values: {}
  });

  const steps = [
    { id: 1, label: 'Profile', description: 'Basic information' },
    { id: 2, label: 'Lifestyle', description: 'Health habits' },
    { id: 3, label: 'Family History', description: 'Genetic factors' },
    { id: 4, label: 'Lab Report', description: 'Optional upload' },
  ];

  const updateFormData = (section, data) => {
    setFormData(prev => ({
      ...prev,
      [section]: data
    }));
  };

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    } else {
      // Navigate to results
      navigate('/results', { state: { formData } });
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <RegistrationForm
            formData={formData}
            updateFormData={updateFormData}
            onNext={handleNext}
          />
        );
      case 2:
        return (
          <LifestyleForm
            formData={formData}
            updateFormData={updateFormData}
            onNext={handleNext}
            onBack={handleBack}
          />
        );
      case 3:
        return (
          <FamilyHistoryForm
            formData={formData}
            updateFormData={updateFormData}
            onNext={handleNext}
            onBack={handleBack}
          />
        );
      case 4:
        return (
          <UploadReport
            formData={formData}
            updateFormData={updateFormData}
            onNext={handleNext}
            onBack={handleBack}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Progress Stepper */}
        <ProgressStepper currentStep={currentStep} steps={steps} />

        {/* Current Step Content */}
        <div className="mt-8">
          {renderCurrentStep()}
        </div>
      </div>
    </div>
  );
}

export default Assessment;
