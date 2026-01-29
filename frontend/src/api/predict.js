/**
 * Risk Prediction API
 * Handles calls to /predict-risk endpoint
 */

import { apiClient } from './client';

/**
 * Submit user data for risk prediction
 * @param {Object} userData - User assessment data
 * @param {Object} userData.patient - Patient info (age, gender, height, weight)
 * @param {Object} userData.lifestyle - Lifestyle data
 * @param {Array} userData.family - Family history
 * @param {Object} userData.lab_values - Lab test results
 * @returns {Promise} Risk prediction results
 */
export const predictRisk = async (userData) => {
  try {
    const response = await apiClient.post('/predict-risk/', userData);
    return response.data;
  } catch (error) {
    console.error('Error predicting risk:', error);
    throw error;
  }
};

/**
 * Example usage:
 * 
 * const userData = {
 *   patient: {
 *     age: 32,
 *     gender: "female",
 *     height: 165,
 *     weight: 70
 *   },
 *   lifestyle: {
 *     smoking: false,
 *     alcohol: "occasional",
 *     exercise: "moderate",
 *     diet: "balanced"
 *   },
 *   family: [
 *     { role: "mother", generation: 1, known_issues: ["type2_diabetes"] }
 *   ],
 *   lab_values: {
 *     hba1c: 5.8,
 *     fasting_glucose: 95
 *   }
 * };
 * 
 * const results = await predictRisk(userData);
 * // results.results = array of 10 diseases with risk scores
 */
