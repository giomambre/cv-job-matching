import { API_ENDPOINTS } from '../utils/constants.js';

export class ApiService {
  static async analyzeCV(file) {
    const formData = new FormData();
    formData.append('cvFile', file);

    try {
      // Try new API first
      const response = await fetch(API_ENDPOINTS.ANALYZE, {
        method: 'POST',
        body: formData,
      });

      return await this.handleResponse(response);
    } catch (error) {
      console.log('New API not available, trying fallback...', error);
      
      try {
        // Fallback to old API
        const fallbackResponse = await fetch(API_ENDPOINTS.UPLOAD_FALLBACK, {
          method: 'POST',
          body: formData,
        });

        return await this.handleFallbackResponse(fallbackResponse);
      } catch (fallbackError) {
        console.error('Both APIs failed:', fallbackError);
        throw new ApiError('Service temporarily unavailable. Please try again later.');
      }
    }
  }

  static async handleResponse(response) {
    if (response.headers.get('content-type')?.includes('application/json')) {
      const data = await response.json();
      
      if (!response.ok) {
        throw new ApiError(data.detail || `HTTP error! status: ${response.status}`);
      }
      
      return data;
    } else {
      // Handle HTML redirect response
      if (response.redirected) {
        window.location.href = response.url;
        return null;
      } else {
        throw new ApiError('Unexpected response format');
      }
    }
  }

  static async handleFallbackResponse(response) {
    if (response.redirected) {
      window.location.href = response.url;
      return null;
    } else {
      throw new ApiError('Fallback API failed');
    }
  }

  static async checkHealth() {
    try {
      const response = await fetch(API_ENDPOINTS.HEALTH);
      return response.ok;
    } catch (error) {
      console.warn('Health check failed:', error);
      return false;
    }
  }
}

export class ApiError extends Error {
  constructor(message, status = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}