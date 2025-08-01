import { SELECTORS, ANIMATION_DELAYS } from '../utils/constants.js';
import { JobMetrics } from './JobMetrics.js';

export class ResultsDisplay {
  constructor(onNewSearch) {
    this.onNewSearch = onNewSearch;
    this.initializeElements();
    this.attachEventListeners();
  }

  initializeElements() {
    this.resultsGrid = document.querySelector(SELECTORS.RESULTS_GRID);
    this.newSearchBtn = document.querySelector(SELECTORS.NEW_SEARCH_BTN);
  }

  attachEventListeners() {
    if (this.newSearchBtn) {
      this.newSearchBtn.addEventListener('click', () => this.onNewSearch());
    }
  }

  displayResults(jobs) {
    console.log(`DEBUG: displayResults called with ${jobs ? jobs.length : 0} jobs`, jobs);
    if (!jobs || jobs.length === 0) {
      this.displayNoResults();
      return;
    }

    this.resultsGrid.innerHTML = '';

    jobs.forEach((job, index) => {
      const jobCard = this.createJobCard(job, index);
      this.resultsGrid.appendChild(jobCard);
    });
  }

  createJobCard(job, index) {
    const card = document.createElement('div');
    card.className = 'job-card';
    card.style.animationDelay = `${index * ANIMATION_DELAYS.CARD_STAGGER}ms`;

    // Aggiungi ID univoco per le metriche
    job.id = `job-${index}-${Date.now()}`;
    const matchPercentage = Math.round(job.similarity * 100);
    
    // Crea l'istanza delle metriche
    const jobMetrics = new JobMetrics(job);
    
    card.innerHTML = `
      <div class="job-header">
        <div class="company-name">${this.escapeHtml(job.Company)}</div>
        <h3 class="job-title">${this.escapeHtml(job.Role)}</h3>
      </div>
      <p class="job-description">${this.escapeHtml(job.Description)}</p>
      
      ${jobMetrics.render()}
      
      <div class="job-footer">
        <div class="match-score">${matchPercentage}% Match</div>
        <a href="${this.escapeHtml(job['Job Link'])}" 
           class="apply-btn" 
           target="_blank" 
           rel="noopener noreferrer">
          Apply Now
        </a>
      </div>
    `;

    // Aggiungi event listeners per le metriche
    this.attachMetricsEventListeners(card);

    return card;
  }

  displayNoResults() {
    this.resultsGrid.innerHTML = `
      <div class="no-results">
        <div class="no-results-icon">😔</div>
        <h3>No matching jobs found</h3>
        <p>Try uploading a different CV or check back later for new opportunities.</p>
      </div>
    `;
  }

  generateMockResults() {
    return [
      {
        Company: "TechCorp Solutions",
        Role: "Senior Software Engineer",
        Description: "We are looking for a passionate Senior Software Engineer to join our dynamic team. You will be responsible for developing scalable web applications, mentoring junior developers, and contributing to architectural decisions. Experience with React, Node.js, and cloud technologies is highly valued.",
        "Job Link": "https://example.com/job1",
        similarity: 0.92,
      },
      {
        Company: "DataFlow Analytics",
        Role: "Full Stack Developer",
        Description: "Join our innovative team as a Full Stack Developer where you'll work on cutting-edge data visualization tools. We need someone proficient in modern JavaScript frameworks, Python, and database design. Great opportunity for career growth in a fast-paced environment.",
        "Job Link": "https://example.com/job2",
        similarity: 0.88,
      },
      {
        Company: "CloudTech Innovations",
        Role: "DevOps Engineer",
        Description: "We're seeking a skilled DevOps Engineer to help us scale our cloud infrastructure. You'll work with Docker, Kubernetes, AWS, and CI/CD pipelines. Perfect role for someone who loves automation and wants to work with the latest cloud technologies.",
        "Job Link": "https://example.com/job3",
        similarity: 0.85,
      },
      {
        Company: "StartupHub Inc",
        Role: "Frontend Developer", 
        Description: "Exciting opportunity for a Frontend Developer to shape the user experience of our next-generation platform. We use React, TypeScript, and modern CSS frameworks. You'll collaborate closely with designers and backend developers in an agile environment.",
        "Job Link": "https://example.com/job4",
        similarity: 0.82,
      },
      {
        Company: "Enterprise Solutions Ltd",
        Role: "Software Architect",
        Description: "Lead the technical direction as a Software Architect in our enterprise solutions team. You'll design system architectures, evaluate technologies, and guide development teams. Strong background in microservices, distributed systems, and team leadership required.",
        "Job Link": "https://example.com/job5",
        similarity: 0.79,
      },
    ];
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  attachMetricsEventListeners(card) {
    const metricsToggle = card.querySelector('.metrics-toggle');
    const metrics = card.querySelector('.job-metrics');
    
    console.log('🔧 Attaching metrics event listeners:', { metricsToggle, metrics });
    
    if (metricsToggle && metrics) {
      metricsToggle.addEventListener('click', (e) => {
        e.preventDefault();
        console.log('🖱️ Metrics toggle clicked!');
        
        const isExpanded = metrics.classList.contains('expanded');
        console.log('📊 Current expanded state:', isExpanded);
        
        // Chiudi tutte le altre metriche aperte
        document.querySelectorAll('.job-metrics.expanded').forEach(openMetrics => {
          if (openMetrics !== metrics) {
            console.log('🔒 Closing other metrics');
            openMetrics.classList.remove('expanded');
            const otherCard = openMetrics.closest('.job-card');
            if (otherCard) otherCard.classList.remove('description-expanded');
            const otherToggle = openMetrics.querySelector('.toggle-text');
            const otherIcon = openMetrics.querySelector('.toggle-icon');
            if (otherToggle) otherToggle.textContent = 'Show Details';
            if (otherIcon) otherIcon.textContent = '▼';
          }
        });
        
        // Toggle corrente
        metrics.classList.toggle('expanded');
        const toggleText = metricsToggle.querySelector('.toggle-text');
        const toggleIcon = metricsToggle.querySelector('.toggle-icon');
        
        const newExpandedState = metrics.classList.contains('expanded');
        console.log('📊 New expanded state:', newExpandedState);
        
        // Aggiungi/rimuovi classe per espandere la descrizione
        if (newExpandedState) {
          card.classList.add('description-expanded');
          if (toggleText) toggleText.textContent = 'Hide Details';
          if (toggleIcon) toggleIcon.textContent = '▲';
          console.log('✅ Metrics expanded');
        } else {
          card.classList.remove('description-expanded');
          if (toggleText) toggleText.textContent = 'Show Details';
          if (toggleIcon) toggleIcon.textContent = '▼';
          console.log('❌ Metrics collapsed');
        }
      });
    } else {
      console.error('❌ Could not find metrics toggle or metrics container');
    }
  }

  clear() {
    if (this.resultsGrid) {
      this.resultsGrid.innerHTML = '';
    }
  }
}