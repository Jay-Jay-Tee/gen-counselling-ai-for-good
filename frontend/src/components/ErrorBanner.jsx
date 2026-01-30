import React from 'react';
import { AlertCircle, X, AlertTriangle, Info, CheckCircle } from 'lucide-react';

function ErrorBanner({ 
  type = 'error', 
  message, 
  onClose, 
  dismissible = true,
  className = '' 
}) {
  const variants = {
    error: {
      bg: 'bg-red-50',
      border: 'border-red-200',
      text: 'text-red-800',
      icon: <AlertCircle className="w-5 h-5 text-red-600" />,
    },
    warning: {
      bg: 'bg-yellow-50',
      border: 'border-yellow-200',
      text: 'text-yellow-800',
      icon: <AlertTriangle className="w-5 h-5 text-yellow-600" />,
    },
    info: {
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      text: 'text-blue-800',
      icon: <Info className="w-5 h-5 text-blue-600" />,
    },
    success: {
      bg: 'bg-green-50',
      border: 'border-green-200',
      text: 'text-green-800',
      icon: <CheckCircle className="w-5 h-5 text-green-600" />,
    },
  };

  const variant = variants[type] || variants.error;

  if (!message) return null;

  return (
    <div
      className={`${variant.bg} ${variant.border} border rounded-lg p-4 ${className}`}
      role="alert"
    >
      <div className="flex items-start">
        <div className="flex-shrink-0">{variant.icon}</div>
        
        <div className="ml-3 flex-1">
          <p className={`text-sm ${variant.text}`}>{message}</p>
        </div>

        {dismissible && onClose && (
          <button
            onClick={onClose}
            className={`ml-3 flex-shrink-0 ${variant.text} hover:opacity-75 transition-opacity`}
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
}

export default ErrorBanner;
