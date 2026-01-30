import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { Heart } from 'lucide-react';

function LifestyleForm({ formData, updateFormData, onNext, onBack }) {
  const navigate = useNavigate();
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: formData.lifestyle
  });

  const onSubmit = (data) => {
    // Convert smoking to boolean
    data.smoking = data.smoking === 'true';
    updateFormData('lifestyle', data);
    if (onNext) {
      onNext();
    } else {
      navigate('/family-history');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium text-indigo-600">Step 2 of 4</span>
            <span className="text-sm text-gray-500">Lifestyle Factors</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-indigo-600 h-2 rounded-full" style={{ width: '50%' }}></div>
          </div>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center mb-6">
            <Heart className="w-8 h-8 text-indigo-600 mr-3" />
            <h2 className="text-2xl font-bold text-gray-900">Lifestyle Information</h2>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Smoking */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Do you smoke? *
              </label>
              <div className="flex space-x-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="false"
                    {...register('smoking', { required: 'This field is required' })}
                    className="w-4 h-4 text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className="ml-2 text-gray-700">No</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="true"
                    {...register('smoking', { required: 'This field is required' })}
                    className="w-4 h-4 text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className="ml-2 text-gray-700">Yes</span>
                </label>
              </div>
              {errors.smoking && (
                <p className="mt-1 text-sm text-red-600">{errors.smoking.message}</p>
              )}
            </div>

            {/* Alcohol */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Alcohol Consumption *
              </label>
              <select
                {...register('alcohol', { required: 'This field is required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="">Select frequency</option>
                <option value="none">None</option>
                <option value="occasional">Occasional</option>
                <option value="moderate">Moderate</option>
                <option value="heavy">Heavy</option>
              </select>
              {errors.alcohol && (
                <p className="mt-1 text-sm text-red-600">{errors.alcohol.message}</p>
              )}
            </div>

            {/* Diet */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Diet Type *
              </label>
              <select
                {...register('diet', { required: 'This field is required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="">Select diet type</option>
                <option value="balanced">Balanced</option>
                <option value="high_sugar">High Sugar</option>
                <option value="high_fat_diet">High Fat</option>
                <option value="high_salt">High Salt</option>
              </select>
              {errors.diet && (
                <p className="mt-1 text-sm text-red-600">{errors.diet.message}</p>
              )}
            </div>

            {/* Exercise */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Exercise Frequency *
              </label>
              <select
                {...register('exercise', { required: 'This field is required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="">Select frequency</option>
                <option value="sedentary">Sedentary (Little to no exercise)</option>
                <option value="occasional">Occasional (1-2 times per week)</option>
                <option value="regular">Regular (3+ times per week)</option>
              </select>
              {errors.exercise && (
                <p className="mt-1 text-sm text-red-600">{errors.exercise.message}</p>
              )}
            </div>

            {/* Stress Level */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Stress Level *
              </label>
              <select
                {...register('stress_level', { required: 'This field is required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="">Select stress level</option>
                <option value="low">Low</option>
                <option value="moderate">Moderate</option>
                <option value="high">High</option>
              </select>
              {errors.stress_level && (
                <p className="mt-1 text-sm text-red-600">{errors.stress_level.message}</p>
              )}
            </div>

            {/* Sleep Hours */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Average Sleep Hours per Night *
              </label>
              <input
                type="number"
                step="0.5"
                {...register('sleep_hours', {
                  required: 'This field is required',
                  min: { value: 0, message: 'Sleep hours must be at least 0' },
                  max: { value: 12, message: 'Sleep hours must be 12 or less' }
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="e.g., 7"
              />
              {errors.sleep_hours && (
                <p className="mt-1 text-sm text-red-600">{errors.sleep_hours.message}</p>
              )}
            </div>

            {/* Submit Buttons */}
            <div className="flex justify-between pt-6">
              <button
                type="button"
                onClick={() => onBack ? onBack() : navigate('/registration')}
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

export default LifestyleForm;
