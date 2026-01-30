import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { User } from 'lucide-react';

function RegistrationForm({ formData, updateFormData, onNext }) {
  const navigate = useNavigate();
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm({
    defaultValues: formData.patient
  });

  const height = watch('height');
  const weight = watch('weight');

  // Auto-calculate BMI for display only
  useEffect(() => {
    if (height && weight && height > 0) {
      const heightInMeters = height / 100;
      const bmi = (weight / (heightInMeters * heightInMeters)).toFixed(1);
      setValue('bmi', parseFloat(bmi));
    }
  }, [height, weight, setValue]);

  const onSubmit = (data) => {
    // Convert gender to API format (M/F/Other)
    if (data.gender === 'male') data.gender = 'M';
    else if (data.gender === 'female') data.gender = 'F';
    else if (data.gender === 'other') data.gender = 'Other';
    
    // Remove BMI as it's calculated on backend
    const { bmi, ...patientData } = data;
    
    // Initialize known_issues as empty array (can be added later if needed)
    patientData.known_issues = [];
    
    updateFormData('patient', patientData);
    if (onNext) {
      onNext();
    } else {
      navigate('/lifestyle');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium text-indigo-600">Step 1 of 4</span>
            <span className="text-sm text-gray-500">Basic Information</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-indigo-600 h-2 rounded-full" style={{ width: '25%' }}></div>
          </div>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center mb-6">
            <User className="w-8 h-8 text-indigo-600 mr-3" />
            <h2 className="text-2xl font-bold text-gray-900">Basic Information</h2>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Age */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Age *
              </label>
              <input
                type="number"
                {...register('age', {
                  required: 'Age is required',
                  min: { value: 10, message: 'Age must be at least 10' },
                  max: { value: 150, message: 'Age must be 150 or less' }
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Enter your age"
              />
              {errors.age && (
                <p className="mt-1 text-sm text-red-600">{errors.age.message}</p>
              )}
            </div>

            {/* Gender */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Gender *
              </label>
              <select
                {...register('gender', { required: 'Gender is required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="">Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
              {errors.gender && (
                <p className="mt-1 text-sm text-red-600">{errors.gender.message}</p>
              )}
            </div>

            {/* Race (Optional) */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Race/Ethnicity (Optional)
              </label>
              <select
                {...register('race')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="">Select race/ethnicity</option>
                <option value="asian">Asian</option>
                <option value="caucasian">Caucasian</option>
                <option value="african">African</option>
                <option value="hispanic">Hispanic</option>
                <option value="other">Other</option>
              </select>
              <p className="mt-1 text-xs text-gray-500">
                Helps with population-specific risk adjustment
              </p>
            </div>

            {/* Height */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Height (cm) *
              </label>
              <input
                type="number"
                {...register('height', {
                  required: 'Height is required',
                  min: { value: 70, message: 'Height must be at least 70 cm' },
                  max: { value: 250, message: 'Height must be 250 cm or less' }
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Enter your height in cm"
              />
              {errors.height && (
                <p className="mt-1 text-sm text-red-600">{errors.height.message}</p>
              )}
            </div>

            {/* Weight */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Weight (kg) *
              </label>
              <input
                type="number"
                step="0.1"
                {...register('weight', {
                  required: 'Weight is required',
                  min: { value: 20, message: 'Weight must be at least 20 kg' },
                  max: { value: 700, message: 'Weight must be 700 kg or less' }
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Enter your weight in kg"
              />
              {errors.weight && (
                <p className="mt-1 text-sm text-red-600">{errors.weight.message}</p>
              )}
            </div>

            {/* BMI (Auto-calculated) */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                BMI (Auto-calculated)
              </label>
              <input
                type="number"
                step="0.1"
                {...register('bmi')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100 cursor-not-allowed"
                readOnly
                placeholder="Will be calculated automatically"
              />
            </div>

            {/* Submit Button */}
            <div className="flex justify-between pt-6">
              <button
                type="button"
                onClick={() => navigate('/')}
                className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Back
              </button>
              <button
                type="submit"
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Next
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default RegistrationForm;
