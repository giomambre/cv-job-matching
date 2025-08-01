import { FILE_CONFIG } from './constants.js';

export class FileValidator {
  static validate(file) {
    const errors = [];
    
    if (!FILE_CONFIG.ALLOWED_TYPES.includes(file.type)) {
      errors.push('Please upload a PDF file.');
    }
    
    if (file.size > FILE_CONFIG.MAX_SIZE_BYTES) {
      errors.push('File size must be less than 10MB.');
    }
    
    if (errors.length > 0) {
      throw new ValidationError(errors.join(' '));
    }
    
    return true;
  }
}

export class FileFormatter {
  static formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}

export class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ValidationError';
  }
}