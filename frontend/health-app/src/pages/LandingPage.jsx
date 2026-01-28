import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity } from 'lucide-react';

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-2xl mx-auto px-6 py-12 text-center">
        <div className="flex justify-center mb-6">
          <Activity className="w-16 h-16 text-indigo-600" />
        </div>
        
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Health Risk Assessment
        </h1>
        
        <p className="text-lg text-gray-600 mb-8">
          Get personalized insights into your health risks based on your lifestyle, 
          family history, and lab results. Take control of your health today.
        </p>
        
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            What You'll Get:
          </h2>
          <ul className="text-left space-y-3 text-gray-700">
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              Comprehensive disease risk assessment
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              Personalized prevention strategies
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              Recommended screening tests
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              Doctor consultation guidance
            </li>
          </ul>
        </div>
        
        <button
          onClick={() => navigate('/registration')}
          className="bg-indigo-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition-colors shadow-lg"
        >
          Get Started
        </button>
        
        <p className="text-sm text-gray-500 mt-6">
          Takes about 5-10 minutes to complete
        </p>
      </div>
    </div>
  );
}

export default LandingPage;
