import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, AlertTriangle, Dumbbell, Stethoscope, Users, Loader } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : "/api";


const RISK_CLASSES = {
  I: { label: 'Low Risk', color: 'bg-green-100 text-green-800' },
  II: { label: 'Moderate Risk', color: 'bg-yellow-100 text-yellow-800' },
  III: { label: 'High Risk', color: 'bg-orange-100 text-orange-800' },
  IV: { label: 'Very High Risk', color: 'bg-red-100 text-red-800' }
};

function DiseaseDetail() {
  const { diseaseName } = useParams(); // This is now disease_id from URL
  const navigate = useNavigate();
  const [diseaseData, setDiseaseData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDiseaseDetails = async () => {
      setLoading(true);
      
      try {
        // Note: Backend should provide an endpoint like /disease/:disease_id
        // For now, we'll use the disease_id from the URL
        const response = await fetch(`${API_BASE}/disease-info/${diseaseName}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch disease details');
        }
        
        const data = await response.json();
        setDiseaseData(data);
      } catch (error) {
        console.error('Error fetching disease details:', error);
        // Use mock data for demo purposes if API fails
        setDiseaseData(getMockDiseaseData(diseaseName));
      } finally {
        setLoading(false);
      }
    };

    fetchDiseaseDetails();
  }, [diseaseName]);

  // Mock data generator for demo
  const getMockDiseaseData = (diseaseId) => ({
    disease_name: diseaseId.replace(/_/g, ' '),
    disease_id: diseaseId,
    risk_class: 'III',
    probability: 0.68,
    description: 'A chronic condition that affects how your body processes blood sugar (glucose).',
    reasons: [
      'Mother has this condition',
      'HbA1c elevated at 6.2%, suggesting higher diabetes risk',
      'High sugar intake and poor dietary habits',
      'Sedentary lifestyle with minimal exercise'
    ],
    prevention: [
      'Eliminate sugary drinks and desserts immediately',
      'Reduce sugar and refined carbohydrates',
      '30 minutes of moderate activity daily',
      'Control portion sizes',
      'Get 7-8 hours quality sleep'
    ],
    recommended_tests: [
      'HbA1c (Glycated Hemoglobin)',
      'Fasting Blood Glucose',
      'Oral Glucose Tolerance Test (OGTT)',
      'Lipid Profile'
    ],
    consult: 'urgent',
    consult_detail: {
      level: 'urgent',
      timeframe: 'Schedule within 1-2 weeks',
      message: 'Urgent consultation recommended - significant risk factors detected',
      specialist: {
        recommended: 'Endocrinologist or Diabetologist',
        also_consider: 'Primary Care Physician'
      },
      what_to_discuss: [
        'Urgency of intervention given your risk level',
        'Your family medical history',
        'Blood sugar levels and HbA1c results',
        'Diet plan and carbohydrate management'
      ],
      preparation: [
        'Gather all recent medical records and test results',
        'Create detailed family medical history (2 generations)',
        'Log blood sugar readings if you have them',
        'Keep food diary for 3-5 days before visit'
      ]
    }
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-indigo-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-700">Loading disease details...</p>
        </div>
      </div>
    );
  }

  if (!diseaseData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-700 mb-4">Disease information not found</p>
          <button
            onClick={() => navigate('/results')}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Back to Results
          </button>
        </div>
      </div>
    );
  }

  const riskInfo = RISK_CLASSES[diseaseData.risk_class] || RISK_CLASSES.I;
  const probabilityPercent = (diseaseData.probability * 100).toFixed(1);

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Back Button */}
        <button
          onClick={() => navigate('/results')}
          className="flex items-center text-indigo-600 hover:text-indigo-700 mb-6"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Dashboard
        </button>

        {/* Disease Header */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-3">
            {diseaseData.disease_name}
          </h1>
          <div className="flex items-center space-x-3 mb-4">
            <span className={`inline-flex px-4 py-2 text-sm font-semibold rounded-full ${riskInfo.color}`}>
              Risk Class {diseaseData.risk_class} - {riskInfo.label}
            </span>
            <span className="text-gray-600">
              Probability: <span className="font-bold text-gray-900">{probabilityPercent}%</span>
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className={`h-3 rounded-full ${
                diseaseData.risk_class === 'IV' ? 'bg-red-500' :
                diseaseData.risk_class === 'III' ? 'bg-orange-500' :
                diseaseData.risk_class === 'II' ? 'bg-yellow-500' :
                'bg-green-500'
              }`}
              style={{ width: `${probabilityPercent}%` }}
            ></div>
          </div>
        </div>

        {/* Description */}
        {diseaseData.description && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-3 flex items-center">
              📋 What This Means
            </h2>
            <p className="text-gray-700 leading-relaxed">
              {diseaseData.description}
            </p>
          </div>
        )}

        {/* Risk Reasons */}
        {diseaseData.reasons && diseaseData.reasons.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <AlertTriangle className="w-6 h-6 text-orange-500 mr-2" />
              Why You're At Risk
            </h2>
            <ul className="space-y-3">
              {diseaseData.reasons.map((reason, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-orange-500 mr-3 mt-1">•</span>
                  <span className="text-gray-700">{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Prevention Plan */}
        {diseaseData.prevention && diseaseData.prevention.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <Dumbbell className="w-6 h-6 text-indigo-600 mr-2" />
              Your Prevention Plan
            </h2>
            <ul className="space-y-3">
              {diseaseData.prevention.map((step, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-indigo-600 mr-3 mt-1">✓</span>
                  <span className="text-gray-700">{step}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommended Tests */}
        {diseaseData.recommended_tests && diseaseData.recommended_tests.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <Stethoscope className="w-6 h-6 text-blue-600 mr-2" />
              Recommended Screening Tests
            </h2>
            <ul className="space-y-3">
              {diseaseData.recommended_tests.map((test, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-blue-600 mr-3 mt-1">🩺</span>
                  <span className="text-gray-700">{test}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Doctor Consultation */}
        {diseaseData.consult_detail && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <Users className="w-6 h-6 text-purple-600 mr-2" />
              Doctor Consultation
            </h2>
            
            <div className="space-y-4">
              {/* Urgency Level */}
              <div>
                <span className="text-sm font-medium text-gray-600">Urgency Level:</span>
                <span className={`ml-2 inline-flex px-3 py-1 text-sm font-semibold rounded-full ${
                  diseaseData.consult_detail.level === 'urgent' ? 'bg-red-100 text-red-800' :
                  diseaseData.consult_detail.level === 'soon' ? 'bg-orange-100 text-orange-800' :
                  diseaseData.consult_detail.level === 'routine' ? 'bg-blue-100 text-blue-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {diseaseData.consult_detail.level.charAt(0).toUpperCase() + diseaseData.consult_detail.level.slice(1)}
                </span>
              </div>

              {/* Timeframe */}
              {diseaseData.consult_detail.timeframe && (
                <div>
                  <span className="text-sm font-medium text-gray-600">Timeframe:</span>
                  <span className="ml-2 text-gray-900 font-semibold">
                    {diseaseData.consult_detail.timeframe}
                  </span>
                </div>
              )}

              {/* Message */}
              {diseaseData.consult_detail.message && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-yellow-800">{diseaseData.consult_detail.message}</p>
                </div>
              )}

              {/* Specialist */}
              {diseaseData.consult_detail.specialist && (
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-2">Recommended Specialist:</p>
                  <div className="space-y-1">
                    <p className="text-gray-900 font-semibold">
                      {diseaseData.consult_detail.specialist.recommended}
                    </p>
                    {diseaseData.consult_detail.specialist.also_consider && (
                      <p className="text-gray-600 text-sm">
                        Also consider: {diseaseData.consult_detail.specialist.also_consider}
                      </p>
                    )}
                  </div>
                </div>
              )}
              
              {/* What to Discuss */}
              {diseaseData.consult_detail.what_to_discuss && diseaseData.consult_detail.what_to_discuss.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-2">What to Discuss:</p>
                  <ul className="space-y-2">
                    {diseaseData.consult_detail.what_to_discuss.map((point, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-purple-600 mr-2">→</span>
                        <span className="text-gray-700">{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Preparation */}
              {diseaseData.consult_detail.preparation && diseaseData.consult_detail.preparation.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-2">How to Prepare:</p>
                  <ul className="space-y-2">
                    {diseaseData.consult_detail.preparation.map((point, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-purple-600 mr-2">✓</span>
                        <span className="text-gray-700">{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="flex justify-center">
          <button
            onClick={() => navigate('/results')}
            className="px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            View All Results
          </button>
        </div>
      </div>
    </div>
  );
}

export default DiseaseDetail;
