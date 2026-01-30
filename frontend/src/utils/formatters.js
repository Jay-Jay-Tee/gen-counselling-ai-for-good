/**
 * Formatting utilities for display
 */

/**
 * Format a number as percentage
 * @param {number} value - Value between 0 and 1
 * @param {number} decimals - Number of decimal places
 * @returns {string}
 */
export const formatPercentage = (value, decimals = 0) => {
  return `${(value * 100).toFixed(decimals)}%`;
};

/**
 * Format a date string
 * @param {string|Date} date
 * @param {string} format - 'short', 'long', 'full'
 * @returns {string}
 */
export const formatDate = (date, format = 'short') => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  
  const options = {
    short: { year: 'numeric', month: 'numeric', day: 'numeric' },
    long: { year: 'numeric', month: 'long', day: 'numeric' },
    full: { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
  };

  return dateObj.toLocaleDateString('en-US', options[format] || options.short);
};

/**
 * Format phone number
 * @param {string} phone
 * @returns {string}
 */
export const formatPhone = (phone) => {
  const cleaned = phone.replace(/\D/g, '');
  
  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  }
  
  return phone;
};

/**
 * Format name (capitalize first letter of each word)
 * @param {string} name
 * @returns {string}
 */
export const formatName = (name) => {
  return name
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

/**
 * Format disease name (replace underscores, capitalize)
 * @param {string} disease
 * @returns {string}
 */
export const formatDiseaseName = (disease) => {
  return disease
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

/**
 * Format lab value name
 * @param {string} labName
 * @returns {string}
 */
export const formatLabName = (labName) => {
  const nameMap = {
    hba1c: 'HbA1c',
    ldl: 'LDL Cholesterol',
    hdl: 'HDL Cholesterol',
    tsh: 'TSH',
    t3: 'T3',
    t4: 'T4',
    rbc: 'RBC Count',
    fasting_glucose: 'Fasting Glucose',
    random_glucose: 'Random Glucose',
    total_cholesterol: 'Total Cholesterol',
    systolic_bp: 'Systolic BP',
    diastolic_bp: 'Diastolic BP',
  };

  return nameMap[labName] || formatName(labName.replace(/_/g, ' '));
};

/**
 * Format BMI category
 * @param {number} bmi
 * @returns {string}
 */
export const formatBMICategory = (bmi) => {
  if (bmi < 18.5) return 'Underweight';
  if (bmi < 25) return 'Normal';
  if (bmi < 30) return 'Overweight';
  return 'Obese';
};

/**
 * Format blood pressure
 * @param {number} systolic
 * @param {number} diastolic
 * @returns {string}
 */
export const formatBloodPressure = (systolic, diastolic) => {
  return `${systolic}/${diastolic} mmHg`;
};

/**
 * Format file size
 * @param {number} bytes
 * @returns {string}
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
};

/**
 * Truncate text
 * @param {string} text
 * @param {number} maxLength
 * @returns {string}
 */
export const truncateText = (text, maxLength = 100) => {
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Format risk level badge color
 * @param {string} riskLevel
 * @returns {object}
 */
export const getRiskLevelColors = (riskLevel) => {
  const level = riskLevel?.toLowerCase();
  
  switch (level) {
    case 'high':
      return {
        bg: 'bg-red-100',
        text: 'text-red-800',
        border: 'border-red-300',
      };
    case 'moderate':
    case 'medium':
      return {
        bg: 'bg-yellow-100',
        text: 'text-yellow-800',
        border: 'border-yellow-300',
      };
    case 'low':
      return {
        bg: 'bg-green-100',
        text: 'text-green-800',
        border: 'border-green-300',
      };
    default:
      return {
        bg: 'bg-gray-100',
        text: 'text-gray-800',
        border: 'border-gray-300',
      };
  }
};

/**
 * Calculate age from date of birth
 * @param {string|Date} dob
 * @returns {number}
 */
export const calculateAge = (dob) => {
  const birthDate = new Date(dob);
  const today = new Date();
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  
  return age;
};

/**
 * Calculate BMI
 * @param {number} weight - in kg
 * @param {number} height - in cm
 * @returns {number}
 */
export const calculateBMI = (weight, height) => {
  const heightInMeters = height / 100;
  return weight / (heightInMeters * heightInMeters);
};

/**
 * Format number with commas
 * @param {number} num
 * @returns {string}
 */
export const formatNumberWithCommas = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

/**
 * Format duration (minutes to hours and minutes)
 * @param {number} minutes
 * @returns {string}
 */
export const formatDuration = (minutes) => {
  if (minutes < 60) {
    return `${minutes} min`;
  }
  
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  
  return mins > 0 ? `${hours}h ${mins}min` : `${hours}h`;
};

/**
 * Format enum value to readable text
 * @param {string} value
 * @returns {string}
 */
export const formatEnumValue = (value) => {
  return value
    .toLowerCase()
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};
