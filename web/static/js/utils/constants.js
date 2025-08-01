// Application constants
export const FILE_CONFIG = {
  MAX_SIZE_BYTES: 10 * 1024 * 1024, // 10MB
  ALLOWED_TYPES: ['application/pdf'],
  ALLOWED_EXTENSIONS: ['.pdf']
};

export const ANIMATION_DELAYS = {
  STEP_TRANSITION: 1500,
  STEP_ANALYSIS: 2000,
  CARD_STAGGER: 100,
  SMOOTH_SCROLL_DURATION: 500
};

export const API_ENDPOINTS = {
  ANALYZE: '/api/analyze',
  UPLOAD_FALLBACK: '/upload',
  HEALTH: '/api/health'
};

export const UI_STATES = {
  UPLOAD: 'upload',
  LOADING: 'loading', 
  RESULTS: 'results',
  ERROR: 'error'
};

export const LOADING_STEPS = {
  EXTRACTING: { id: 'step1', text: 'Extracting text' },
  ANALYZING: { id: 'step2', text: 'Analyzing skills' },
  MATCHING: { id: 'step3', text: 'Finding matches' }
};

export const CSS_CLASSES = {
  DRAGOVER: 'dragover',
  ACTIVE: 'active',
  HIDDEN: 'hidden',
  FADE_IN: 'fadeInUp'
};

export const SELECTORS = {
  UPLOAD_SECTION: '#uploadSection',
  LOADING_SECTION: '#loadingSection', 
  RESULTS_SECTION: '#resultsSection',
  UPLOAD_AREA: '#uploadArea',
  FILE_INPUT: '#fileInput',
  SELECTED_FILE: '#selectedFile',
  ANALYZE_BTN: '#analyzeBtn',
  RESULTS_GRID: '#resultsGrid',
  NEW_SEARCH_BTN: '#newSearchBtn'
};