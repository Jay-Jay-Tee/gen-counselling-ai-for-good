/**
 * Validation utilities for form inputs
 */

/**
 * Validate email address
 * @param {string} email
 * @returns {boolean}
 */
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate phone number (basic format)
 * @param {string} phone
 * @returns {boolean}
 */
export const isValidPhone = (phone) => {
  const phoneRegex = /^[\d\s\-\+\(\)]{10,}$/;
  return phoneRegex.test(phone);
};

/**
 * Validate age
 * @param {number} age
 * @returns {boolean}
 */
export const isValidAge = (age) => {
  return age >= 1 && age <= 120;
};

/**
 * Validate height in cm
 * @param {number} height
 * @returns {boolean}
 */
export const isValidHeight = (height) => {
  return height >= 50 && height <= 250;
};

/**
 * Validate weight in kg
 * @param {number} weight
 * @returns {boolean}
 */
export const isValidWeight = (weight) => {
  return weight >= 20 && weight <= 300;
};

/**
 * Validate BMI
 * @param {number} bmi
 * @returns {boolean}
 */
export const isValidBMI = (bmi) => {
  return bmi >= 10 && bmi <= 60;
};

/**
 * Validate blood pressure
 * @param {number} systolic
 * @param {number} diastolic
 * @returns {boolean}
 */
export const isValidBloodPressure = (systolic, diastolic) => {
  return (
    systolic >= 70 &&
    systolic <= 250 &&
    diastolic >= 40 &&
    diastolic <= 150 &&
    systolic > diastolic
  );
};

/**
 * Validate glucose level
 * @param {number} glucose
 * @returns {boolean}
 */
export const isValidGlucose = (glucose) => {
  return glucose >= 50 && glucose <= 500;
};

/**
 * Validate cholesterol level
 * @param {number} cholesterol
 * @returns {boolean}
 */
export const isValidCholesterol = (cholesterol) => {
  return cholesterol >= 100 && cholesterol <= 400;
};

/**
 * Validate HbA1c
 * @param {number} hba1c
 * @returns {boolean}
 */
export const isValidHbA1c = (hba1c) => {
  return hba1c >= 4 && hba1c <= 15;
};

/**
 * Validate required field
 * @param {*} value
 * @returns {boolean}
 */
export const isRequired = (value) => {
  if (typeof value === 'string') {
    return value.trim().length > 0;
  }
  return value !== null && value !== undefined;
};

/**
 * Validate name (letters, spaces, hyphens only)
 * @param {string} name
 * @returns {boolean}
 */
export const isValidName = (name) => {
  const nameRegex = /^[a-zA-Z\s\-']+$/;
  return nameRegex.test(name) && name.trim().length >= 2;
};

/**
 * Validate date (not in future)
 * @param {string} date - Date string in YYYY-MM-DD format
 * @returns {boolean}
 */
export const isValidPastDate = (date) => {
  const selectedDate = new Date(date);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return selectedDate <= today;
};

/**
 * Validate file size
 * @param {File} file
 * @param {number} maxSizeMB - Maximum size in MB
 * @returns {boolean}
 */
export const isValidFileSize = (file, maxSizeMB = 10) => {
  return file.size <= maxSizeMB * 1024 * 1024;
};

/**
 * Validate file type
 * @param {File} file
 * @param {string[]} allowedTypes - Array of allowed MIME types
 * @returns {boolean}
 */
export const isValidFileType = (file, allowedTypes) => {
  return allowedTypes.includes(file.type);
};

/**
 * Get validation error message
 * @param {string} field - Field name
 * @param {*} value - Field value
 * @param {string} type - Validation type
 * @returns {string|null}
 */
export const getValidationError = (field, value, type) => {
  switch (type) {
    case 'required':
      return !isRequired(value) ? `${field} is required` : null;
    case 'email':
      return !isValidEmail(value) ? 'Please enter a valid email address' : null;
    case 'phone':
      return !isValidPhone(value) ? 'Please enter a valid phone number' : null;
    case 'name':
      return !isValidName(value) ? 'Please enter a valid name (letters only)' : null;
    case 'age':
      return !isValidAge(value) ? 'Please enter a valid age (1-120)' : null;
    case 'height':
      return !isValidHeight(value) ? 'Please enter a valid height (50-250 cm)' : null;
    case 'weight':
      return !isValidWeight(value) ? 'Please enter a valid weight (20-300 kg)' : null;
    case 'bmi':
      return !isValidBMI(value) ? 'Please enter a valid BMI (10-60)' : null;
    default:
      return null;
  }
};
