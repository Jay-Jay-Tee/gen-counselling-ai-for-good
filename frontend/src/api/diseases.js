/**
 * Disease Information API
 * Handles fetching detailed disease information
 */

import { apiClient } from './client';

/**
 * Get detailed information about a specific disease
 * @param {string} diseaseId - Disease identifier (e.g., "type2_diabetes")
 * @returns {Promise} Disease details
 */
export const getDiseaseInfo = async (diseaseId) => {
  try {
    const response = await apiClient.get(`/disease-info/${diseaseId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching disease info for ${diseaseId}:`, error);
    throw error;
  }
};

/**
 * Get list of all diseases
 * @returns {Promise} Array of all diseases
 */
export const getAllDiseases = async () => {
  try {
    const response = await apiClient.get('/disease-info/');
    return response.data;
  } catch (error) {
    console.error('Error fetching all diseases:', error);
    throw error;
  }
};

/**
 * Example usage:
 * 
 * // Get specific disease info
 * const diabetesInfo = await getDiseaseInfo('type2_diabetes');
 * console.log(diabetesInfo.name);
 * console.log(diabetesInfo.description);
 * console.log(diabetesInfo.symptoms);
 * 
 * // Get all diseases
 * const allDiseases = await getAllDiseases();
 * console.log('Total diseases:', allDiseases.length);
 */
