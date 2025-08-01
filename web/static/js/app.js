import { FileUpload } from './components/FileUpload.js';
import { LoadingManager } from './components/LoadingManager.js';
import { ResultsDisplay } from './components/ResultsDisplay.js';
import { ApiService, ApiError } from './services/ApiService.js';

class CVJobMatcher {
  constructor() {
    this.currentFile = null;
    this.init();
  }

  init() {
    try {
      console.log('🔧 Initializing CV Job Matcher...');
      this.initializeComponents();
      this.attachGlobalEventListeners();
      console.log('✅ CV Job Matcher initialized successfully with ES6 modules!');
    } catch (error) {
      console.error('❌ Error during initialization:', error);
      alert('Initialization failed. Please refresh the page. Error: ' + error.message);
    }
  }

  initializeComponents() {
    try {
      console.log('📤 Initializing FileUpload component...');
      this.fileUpload = new FileUpload(
        (file) => this.handleFileSelected(file),
        (error) => this.showError(error)
      );
      console.log('✅ FileUpload initialized');

      console.log('⏳ Initializing LoadingManager component...');
      this.loadingManager = new LoadingManager();
      console.log('✅ LoadingManager initialized');

      console.log('🎯 Initializing ResultsDisplay component...');
      this.resultsDisplay = new ResultsDisplay(
        () => this.handleNewSearch()
      );
      console.log('✅ ResultsDisplay initialized');

      console.log('🔘 Initializing analyze button...');
      this.initializeAnalyzeButton();
      console.log('✅ Analyze button initialized');
      
    } catch (error) {
      console.error('❌ Error in initializeComponents:', error);
      throw error;
    }
  }

  initializeAnalyzeButton() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
      analyzeBtn.addEventListener('click', () => this.analyzeCV());
    }
  }

  handleFileSelected(file) {
    this.currentFile = file;
    console.log('📄 File selected:', file.name);
  }

  async analyzeCV() {
    if (!this.currentFile) {
      this.showError('Please select a file first.');
      return;
    }

    try {
      // Show loading state
      await this.loadingManager.showLoading();

      // Call API
      const result = await ApiService.analyzeCV(this.currentFile);
      
      // If result is null, it means we got redirected
      if (result === null) {
        return;
      }

      // Show results
      this.loadingManager.showResults();
      this.resultsDisplay.displayResults(result.results || result);

    } catch (error) {
      console.error('❌ Error analyzing CV:', error);
      
      if (error instanceof ApiError) {
        this.showError(`Analysis failed: ${error.message}`);
      } else {
        this.showError('An unexpected error occurred. Please try again.');
      }

      // Show mock results for demonstration
      this.showMockResults();
    }
  }

  showMockResults() {
    console.log('🎭 Showing mock results for demonstration');
    
    setTimeout(() => {
      this.loadingManager.showResults();
      this.resultsDisplay.displayResults(this.resultsDisplay.generateMockResults());
    }, 1000);
  }

  handleNewSearch() {
    this.currentFile = null;
    this.fileUpload.reset();
    this.loadingManager.reset();
    this.resultsDisplay.clear();
    console.log('🔄 New search initiated');
  }

  showError(message) {
    // Simple error display - can be enhanced with a modal or toast
    alert(message);
    console.error('🚨 Application Error:', message);
  }

  attachGlobalEventListeners() {
    // Smooth scrolling for anchor links
    document.addEventListener('click', (e) => {
      if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
          });
        }
      }
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const resultsSection = document.getElementById('resultsSection');
        if (resultsSection && resultsSection.style.display !== 'none') {
          this.handleNewSearch();
        }
      }
    });

    // Add some accessibility improvements
    this.enhanceAccessibility();
  }

  enhanceAccessibility() {
    // Add focus indicators for keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
      }
    });

    document.addEventListener('mousedown', () => {
      document.body.classList.remove('keyboard-navigation');
    });
  }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new CVJobMatcher();
});

// Export for potential external access
export default CVJobMatcher;