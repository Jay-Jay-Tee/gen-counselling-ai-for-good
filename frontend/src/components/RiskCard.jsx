import React from 'react';
import { AlertCircle, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

function RiskCard({ disease, risk }) {
  const navigate = useNavigate();

  // Determine risk level styling and icon
  const getRiskStyle = (level) => {
    switch (level?.toLowerCase()) {
      case 'high':
        return {
          bg: 'bg-red-50',
          border: 'border-red-200',
          text: 'text-red-800',
          icon: <AlertCircle className="w-6 h-6 text-red-600" />,
          badge: 'bg-red-600',
        };
      case 'moderate':
      case 'medium':
        return {
          bg: 'bg-yellow-50',
          border: 'border-yellow-200',
          text: 'text-yellow-800',
          icon: <AlertTriangle className="w-6 h-6 text-yellow-600" />,
          badge: 'bg-yellow-600',
        };
      case 'low':
        return {
          bg: 'bg-green-50',
          border: 'border-green-200',
          text: 'text-green-800',
          icon: <CheckCircle className="w-6 h-6 text-green-600" />,
          badge: 'bg-green-600',
        };
      default:
        return {
          bg: 'bg-gray-50',
          border: 'border-gray-200',
          text: 'text-gray-800',
          icon: <Info className="w-6 h-6 text-gray-600" />,
          badge: 'bg-gray-600',
        };
    }
  };

  const style = getRiskStyle(risk?.risk_class);

  const handleLearnMore = () => {
    navigate(`/disease/${disease}`);
  };

  return (
    <div
      className={`${style.bg} ${style.border} border-2 rounded-lg p-6 transition-all hover:shadow-lg cursor-pointer`}
      onClick={handleLearnMore}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          {style.icon}
          <div>
            <h3 className="text-xl font-bold text-gray-900">
              {disease.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </h3>
            <span className={`inline-block ${style.badge} text-white text-xs font-semibold px-3 py-1 rounded-full mt-1`}>
              {risk?.risk_class?.toUpperCase() || 'UNKNOWN'} RISK
            </span>
          </div>
        </div>
      </div>

      {/* Risk Score */}
      {risk?.risk_score !== undefined && (
        <div className="mb-4">
          <div className="flex items-center justify-between mb-1">
            <span className="text-sm font-medium text-gray-700">Risk Score</span>
            <span className={`text-lg font-bold ${style.text}`}>
              {Math.round(risk.risk_score * 100)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`${style.badge} h-2 rounded-full transition-all duration-500`}
              style={{ width: `${risk.risk_score * 100}%` }}
            />
          </div>
        </div>
      )}

      {/* Key Factors */}
      {risk?.contributing_factors && risk.contributing_factors.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Key Factors:</h4>
          <ul className="space-y-1">
            {risk.contributing_factors.slice(0, 3).map((factor, index) => (
              <li key={index} className="text-sm text-gray-600 flex items-start">
                <span className="mr-2">•</span>
                <span>{factor}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Action Button */}
      <button
        onClick={handleLearnMore}
        className="w-full mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium"
      >
        View Details & Prevention
      </button>
    </div>
  );
}

export default RiskCard;
