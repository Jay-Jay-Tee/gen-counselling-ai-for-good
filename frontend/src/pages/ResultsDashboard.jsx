import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Activity, AlertCircle, Loader } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : "/api";


const RISK_CLASSES = {
  I: { label: 'Low', color: '#22c55e', bgColor: 'bg-green-100', textColor: 'text-green-800' },
  II: { label: 'Moderate', color: '#eab308', bgColor: 'bg-yellow-100', textColor: 'text-yellow-800' },
  III: { label: 'High', color: '#f97316', bgColor: 'bg-orange-100', textColor: 'text-orange-800' },
  IV: { label: 'Very High', color: '#ef4444', bgColor: 'bg-red-100', textColor: 'text-red-800' }
};

const URGENCY_STYLES = {
  none: 'bg-gray-100 text-gray-800',
  routine: 'bg-blue-100 text-blue-800',
  soon: 'bg-orange-100 text-orange-800',
  urgent: 'bg-red-100 text-red-800'
};

function ResultsDashboard({ formData: propFormData }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Use formData from location state (Assessment flow) or props (legacy routes)
  const formData = location.state?.formData || propFormData;

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`${API_BASE}/predict-risk/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        });

        if (!response.ok) {
          throw new Error('Failed to fetch risk assessment');
        }

        const data = await response.json();
        
        // Sort by probability (highest first)
        // Probability is now a decimal (0-1), so convert to percentage for display
        const sortedResults = (data.results || []).sort((a, b) => 
          b.probability - a.probability
        );
        
        setResults(sortedResults);
      } catch (err) {
        setError(err.message);
        console.error('API Error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [formData]);

  const handleRetry = () => {
    window.location.reload();
  };

  const handleDiseaseClick = (diseaseId) => {
    navigate(`/disease/${diseaseId}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-indigo-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-700 text-lg">Analyzing your health data...</p>
          <p className="text-gray-500 text-sm mt-2">This may take a moment</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-900 mb-2">Unable to Load Results</h2>
          <p className="text-gray-600 mb-6">{error}. Please try again.</p>
          <button
            onClick={handleRetry}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  // Prepare chart data (top 5 risks) - convert probability to percentage
  const chartData = results.slice(0, 5).map(result => ({
    name: result.disease_name.replace(/_/g, ' '),
    probability: result.probability * 100, // Convert to percentage
    color: RISK_CLASSES[result.risk_class]?.color || '#9ca3af'
  }));

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <div className="flex items-center mb-4">
            <Activity className="w-10 h-10 text-indigo-600 mr-3" />
            <h1 className="text-3xl font-bold text-gray-900">
              Your Health Risk Assessment Results
            </h1>
          </div>
          <p className="text-gray-600">
            Based on your lifestyle, family history, and lab values, here are your personalized disease risk predictions.
          </p>
        </div>

        {/* Risk Class Legend */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Risk Class Legend</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(RISK_CLASSES).map(([classNum, info]) => (
              <div key={classNum} className="flex items-center">
                <div
                  className="w-6 h-6 rounded mr-3"
                  style={{ backgroundColor: info.color }}
                ></div>
                <div>
                  <div className="font-semibold text-gray-800">Class {classNum}</div>
                  <div className="text-sm text-gray-600">{info.label}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chart Visualization */}
        {chartData.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Top 5 Risk Factors</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="name" 
                  angle={-45} 
                  textAnchor="end" 
                  height={100}
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  label={{ value: 'Probability (%)', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  formatter={(value) => `${value.toFixed(1)}%`}
                  labelStyle={{ color: '#000' }}
                />
                <Bar dataKey="probability" radius={[8, 8, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Results Table */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-800">All Disease Risk Assessments</h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Disease Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Probability
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Risk Class
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Urgency
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {results.map((result, index) => {
                  const riskInfo = RISK_CLASSES[result.risk_class] || RISK_CLASSES.I;
                  const probabilityPercent = (result.probability * 100).toFixed(1);
                  
                  return (
                    <tr
                      key={index}
                      onClick={() => handleDiseaseClick(result.disease_id)}
                      className="hover:bg-gray-50 cursor-pointer transition-colors"
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="font-medium text-gray-900">
                          {result.disease_name}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-gray-900 font-semibold">
                          {probabilityPercent}%
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-3 py-1 text-xs font-semibold rounded-full ${riskInfo.bgColor} ${riskInfo.textColor}`}>
                          {result.risk_class} - {riskInfo.label}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-3 py-1 text-xs font-semibold rounded-full ${URGENCY_STYLES[result.consult] || URGENCY_STYLES.none}`}>
                          {result.consult ? result.consult.charAt(0).toUpperCase() + result.consult.slice(1) : 'None'}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex justify-center space-x-4">
          <button
            onClick={() => navigate('/')}
            className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Start New Assessment
          </button>
        </div>
      </div>
    </div>
  );
}

export default ResultsDashboard;
