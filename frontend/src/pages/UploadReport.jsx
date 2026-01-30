import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, Check, AlertCircle } from 'lucide-react';
import { uploadReport } from '../api/ocr';

function UploadReport({ formData, updateFormData, onNext, onBack }) {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [extractedValues, setExtractedValues] = useState({});
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  };

  const handleFileSelect = (selectedFile) => {
    const validTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg'];
    
    if (!validTypes.includes(selectedFile.type)) {
      setUploadError('Please upload a PDF, PNG, or JPG file');
      return;
    }
    
    if (selectedFile.size > 10 * 1024 * 1024) { // 10MB limit
      setUploadError('File size must be less than 10MB');
      return;
    }
    
    setFile(selectedFile);
    setUploadError(null);
  };

  const handleFileInputChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      handleFileSelect(selectedFile);
    }
  };

  const extractLabValues = async () => {
    if (!file) return;

    setIsUploading(true);
    setUploadError(null);

    try {
      const data = await uploadReport(file);
      
      // Extract lab_values from the response
      const labValues = data.lab_values || {};
      setExtractedValues(labValues);
      
      // Update form data with extracted values
      updateFormData('lab_values', labValues);
      
    } catch (error) {
      setUploadError('Failed to extract lab values. Please try again or skip this step.');
      console.error('OCR Error:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSkip = () => {
    if (onNext) {
      onNext();
    } else {
      navigate('/results');
    }
  };

  const handleContinue = () => {
    if (onNext) {
      onNext();
    } else {
      navigate('/results');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium text-indigo-600">Step 4 of 4</span>
            <span className="text-sm text-gray-500">Upload Lab Report (Optional)</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-indigo-600 h-2 rounded-full" style={{ width: '100%' }}></div>
          </div>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center mb-6">
            <Upload className="w-8 h-8 text-indigo-600 mr-3" />
            <h2 className="text-2xl font-bold text-gray-900">Upload Lab Report</h2>
          </div>

          <p className="text-gray-600 mb-6">
            Upload your recent lab report to include lab values in your risk assessment. This step is optional but recommended for more accurate results.
          </p>

          {/* Upload Area */}
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
              isDragging 
                ? 'border-indigo-500 bg-indigo-50' 
                : 'border-gray-300 bg-gray-50'
            }`}
          >
            {!file ? (
              <>
                <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-700 mb-2">
                  Drag & drop your lab report here
                </p>
                <p className="text-gray-500 text-sm mb-4">or</p>
                <label className="inline-block px-6 py-2 bg-indigo-600 text-white rounded-lg cursor-pointer hover:bg-indigo-700 transition-colors">
                  Browse Files
                  <input
                    type="file"
                    accept=".pdf,.png,.jpg,.jpeg"
                    onChange={handleFileInputChange}
                    className="hidden"
                  />
                </label>
                <p className="text-gray-500 text-sm mt-4">
                  Supports: PDF, PNG, JPG (Max 10MB)
                </p>
              </>
            ) : (
              <div className="flex items-center justify-center space-x-3">
                <FileText className="w-8 h-8 text-indigo-600" />
                <div className="text-left">
                  <p className="font-medium text-gray-800">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <button
                  onClick={() => {
                    setFile(null);
                    setExtractedValues({});
                  }}
                  className="text-red-600 hover:text-red-700 ml-4"
                >
                  Remove
                </button>
              </div>
            )}
          </div>

          {/* Error Message */}
          {uploadError && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start">
              <AlertCircle className="w-5 h-5 text-red-600 mr-2 mt-0.5" />
              <p className="text-red-700 text-sm">{uploadError}</p>
            </div>
          )}

          {/* Extract Button */}
          {file && Object.keys(extractedValues).length === 0 && (
            <button
              onClick={extractLabValues}
              disabled={isUploading}
              className="w-full mt-6 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isUploading ? 'Extracting Lab Values...' : 'Extract Lab Values'}
            </button>
          )}

          {/* Extracted Values Display */}
          {Object.keys(extractedValues).length > 0 && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center mb-3">
                <Check className="w-5 h-5 text-green-600 mr-2" />
                <h3 className="font-semibold text-green-800">Extracted Lab Values:</h3>
              </div>
              <ul className="space-y-2">
                {Object.entries(extractedValues).map(([key, value]) => (
                  <li key={key} className="flex justify-between text-sm">
                    <span className="text-gray-700 font-medium">
                      {key.replace(/_/g, ' ').toUpperCase()}:
                    </span>
                    <span className="text-gray-900">{value}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8 pt-6 border-t">
            <button
              onClick={() => onBack ? onBack() : navigate('/family-history')}
              className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Back
            </button>
            <div className="flex space-x-3">
              <button
                onClick={handleSkip}
                className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Skip
              </button>
              <button
                onClick={handleContinue}
                disabled={file && Object.keys(extractedValues).length === 0 && !isUploading}
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                Continue to Results
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UploadReport;
