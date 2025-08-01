import { SELECTORS, ANIMATION_DELAYS, LOADING_STEPS, CSS_CLASSES } from '../utils/constants.js';

export class LoadingManager {
  constructor() {
    this.initializeElements();
  }

  initializeElements() {
    this.uploadSection = document.querySelector(SELECTORS.UPLOAD_SECTION);
    this.loadingSection = document.querySelector(SELECTORS.LOADING_SECTION);
    this.resultsSection = document.querySelector(SELECTORS.RESULTS_SECTION);
  }

  async showLoading() {
    this.uploadSection.style.display = 'none';
    this.loadingSection.style.display = 'block';
    this.resultsSection.style.display = 'none';

    // Reset all steps
    this.resetSteps();
    
    // Activate first step
    document.querySelector('.step').classList.add(CSS_CLASSES.ACTIVE);
    
    // Simulate analysis progress
    await this.simulateAnalysisSteps();
  }

  async simulateAnalysisSteps() {
    // Step 1 is already active
    await this.delay(ANIMATION_DELAYS.STEP_TRANSITION);

    // Activate step 2 (Analyzing)
    const step2 = document.getElementById(LOADING_STEPS.ANALYZING.id);
    if (step2) {
      step2.classList.add(CSS_CLASSES.ACTIVE);
    }
    await this.delay(ANIMATION_DELAYS.STEP_ANALYSIS);

    // Activate step 3 (Matching)
    const step3 = document.getElementById(LOADING_STEPS.MATCHING.id);
    if (step3) {
      step3.classList.add(CSS_CLASSES.ACTIVE);
    }
    await this.delay(ANIMATION_DELAYS.STEP_TRANSITION);
  }

  showResults() {
    this.loadingSection.style.display = 'none';
    this.resultsSection.style.display = 'block';
  }

  showUpload() {
    this.loadingSection.style.display = 'none';
    this.resultsSection.style.display = 'none';
    this.uploadSection.style.display = 'block';
  }

  resetSteps() {
    document.querySelectorAll('.step').forEach(step => {
      step.classList.remove(CSS_CLASSES.ACTIVE);
    });
  }

  reset() {
    this.resetSteps();
    this.showUpload();
    
    // Scroll to top
    window.scrollTo({ 
      top: 0, 
      behavior: 'smooth' 
    });
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}