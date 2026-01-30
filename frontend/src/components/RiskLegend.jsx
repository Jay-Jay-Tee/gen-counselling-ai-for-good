import React from 'react';
import { AlertCircle, AlertTriangle, CheckCircle } from 'lucide-react';

function RiskLegend() {
  const riskLevels = [
    {
      level: 'Low Risk',
      icon: <CheckCircle className="w-5 h-5 text-green-600" />,
      color: 'bg-green-100 border-green-300',
      description: 'Continue healthy habits and regular check-ups',
    },
    {
      level: 'Moderate Risk',
      icon: <AlertTriangle className="w-5 h-5 text-yellow-600" />,
      color: 'bg-yellow-100 border-yellow-300',
      description: 'Consider lifestyle modifications and closer monitoring',
    },
    {
      level: 'High Risk',
      icon: <AlertCircle className="w-5 h-5 text-red-600" />,
      color: 'bg-red-100 border-red-300',
      description: 'Consult healthcare provider and follow prevention plan',
    },
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold text-gray-900 mb-4">
        Understanding Your Risk Levels
      </h3>
      
      <div className="space-y-3">
        {riskLevels.map((item, index) => (
          <div
            key={index}
            className={`${item.color} border-2 rounded-lg p-4 transition-all`}
          >
            <div className="flex items-start space-x-3">
              {item.icon}
              <div className="flex-1">
                <h4 className="font-semibold text-gray-900 mb-1">
                  {item.level}
                </h4>
                <p className="text-sm text-gray-700">
                  {item.description}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-600">
          <strong>Important:</strong> These risk assessments are estimates based on 
          provided information. Always consult with a healthcare professional for 
          personalized medical advice.
        </p>
      </div>
    </div>
  );
}

export default RiskLegend;
