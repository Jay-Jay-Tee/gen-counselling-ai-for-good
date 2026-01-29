/**
 * OCR API
 * Handles medical report upload and text extraction
 */

import { apiClient } from './client';

/**
 * Upload medical report for OCR processing
 * @param {File} file - Image or PDF file containing lab report
 * @returns {Promise} Extracted lab values
 */
export const uploadReport = async (file) => {
  try {
    // Create FormData for file upload
    const formData = new FormData();
    formData.append('file', file);
    
    // Send with multipart/form-data header
    const response = await apiClient.post('/ocr/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error uploading report:', error);
    throw error;
  }
};

/**
 * Example usage:
 * 
 * const handleFileUpload = async (event) => {
 *   const file = event.target.files[0];
 *   
 *   try {
 *     const result = await uploadReport(file);
 *     console.log('Extracted lab values:', result.lab_values);
 *     
 *     // Use extracted values to pre-fill form
 *     setFormData(prev => ({
 *       ...prev,
 *       lab_values: result.lab_values
 *     }));
 *   } catch (error) {
 *     console.error('Upload failed:', error);
 *   }
 * };
 */
