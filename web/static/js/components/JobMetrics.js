export class JobMetrics {
  constructor(job) {
    this.job = job;
  }

  render() {
    console.log('🎯 JobMetrics render - job:', this.job);
    
    // USA I DATI REALI DAL BACKEND SE DISPONIBILI!
    const realMetrics = this.job.metrics; // Dati veri dal tuo utils.py
    console.log('🔬 Real metrics from backend:', realMetrics);
    
    // Genera metriche usando i dati reali quando possibile
    const metrics = this.generateMetricsFromJob(this.job, realMetrics);
    console.log('📊 Final metrics:', metrics);
    
    return `
      <div class="job-metrics" id="metrics-${this.job.id || Math.random()}">
        <div class="metrics-header">
          <h4>📊 Why This Match?</h4>
          <button class="metrics-toggle">
            <span class="toggle-text">Show Details</span>
            <span class="toggle-icon">▼</span>
          </button>
        </div>
        
        <div class="metrics-content">
          ${this.renderOverallMatch(metrics)}
          ${this.renderSkillBreakdown(metrics)}
          ${this.renderKeywordAnalysis(metrics)}
          ${this.renderExperienceMatch(metrics)}
          ${this.renderJobInsights(metrics)}
        </div>
      </div>
    `;
  }

  renderOverallMatch(metrics) {
    const matchScore = Math.round(this.job.similarity * 100);
    return `
      <div class="overall-match">
        <div class="match-circle">
          <svg class="progress-ring" width="80" height="80">
            <circle class="progress-ring-circle" 
                    stroke="url(#gradient)" 
                    stroke-width="6"
                    fill="transparent"
                    r="35"
                    cx="40"
                    cy="40"
                    style="stroke-dasharray: ${2 * Math.PI * 35}; stroke-dashoffset: ${2 * Math.PI * 35 * (1 - this.job.similarity)}"/>
          </svg>
          <div class="match-percentage">${matchScore}%</div>
        </div>
        <div class="match-summary">
          <h5>Overall Match</h5>
          <p>${this.getMatchDescription(matchScore)}</p>
        </div>
      </div>
    `;
  }

  renderSkillBreakdown(metrics) {
    // Debug per capire cosa stiamo ricevendo
    console.log('🐛 renderSkillBreakdown called with metrics:', metrics);
    console.log('🐛 metrics.matchedSkills:', metrics?.matchedSkills);
    console.log('🐛 typeof metrics:', typeof metrics);
    
    // Difesa contro errori - verifica che metrics.matchedSkills esista e sia un array
    const skills = (metrics && Array.isArray(metrics.matchedSkills)) ? metrics.matchedSkills : [];
    
    if (skills.length === 0) {
      return `
        <div class="skill-breakdown">
          <h5>🎯 Skill Match Breakdown</h5>
          <p>No specific skills identified for this position.</p>
        </div>
      `;
    }
    
    return `
      <div class="skill-breakdown">
        <h5>🎯 Skill Match Breakdown</h5>
        <div class="skills-grid">
          ${skills.map(skill => `
            <div class="skill-item">
              <div class="skill-info">
                <span class="skill-name">${skill.name || 'Unknown Skill'}</span>
                <span class="skill-confidence">${skill.confidence || 0}%</span>
              </div>
              <div class="skill-bar">
                <div class="skill-progress" style="width: ${skill.confidence || 0}%"></div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  renderKeywordAnalysis(metrics) {
    const technicalKeywords = (metrics && Array.isArray(metrics.technicalKeywords)) ? metrics.technicalKeywords : [];
    const softSkills = (metrics && Array.isArray(metrics.softSkills)) ? metrics.softSkills : [];
    
    return `
      <div class="keyword-analysis">
        <h5>🔍 Keyword Analysis</h5>
        <div class="keyword-categories">
          <div class="keyword-category">
            <span class="category-label">Technical</span>
            <div class="keyword-tags">
              ${technicalKeywords.map(kw => 
                `<span class="keyword-tag technical">${kw}</span>`
              ).join('') || '<span class="no-keywords">No technical keywords found</span>'}
            </div>
          </div>
          <div class="keyword-category">
            <span class="category-label">Soft Skills</span>
            <div class="keyword-tags">
              ${softSkills.map(kw => 
                `<span class="keyword-tag soft">${kw}</span>`
              ).join('') || '<span class="no-keywords">No soft skills identified</span>'}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  renderExperienceMatch(metrics) {
    const requiredExp = (metrics && typeof metrics.requiredExperience === 'number') ? metrics.requiredExperience : 3;
    const yourExp = (metrics && typeof metrics.yourExperience === 'number') ? metrics.yourExperience : 2;
    const expMatch = (metrics && typeof metrics.experienceMatch === 'number') ? metrics.experienceMatch : 65;
    
    return `
      <div class="experience-match">
        <h5>📈 Experience Level</h5>
        <div class="experience-bars">
          <div class="experience-item">
            <span>Required Experience</span>
            <div class="exp-bar">
              <div class="exp-progress required" style="width: ${requiredExp * 20}%"></div>
            </div>
            <span>${requiredExp} years</span>
          </div>
          <div class="experience-item">
            <span>Your Experience</span>
            <div class="exp-bar">
              <div class="exp-progress yours" style="width: ${yourExp * 20}%"></div>
            </div>
            <span>${yourExp} years</span>
          </div>
        </div>
        <div class="experience-verdict ${expMatch >= 80 ? 'good' : 'fair'}">
          ${this.getExperienceVerdict(expMatch)}
        </div>
      </div>
    `;
  }

  renderJobInsights(metrics) {
    const insights = (metrics && Array.isArray(metrics.insights)) ? metrics.insights : [];
    
    return `
      <div class="job-insights">
        <h5>💡 AI Insights</h5>
        <div class="insights-list">
          ${insights.map(insight => `
            <div class="insight-item">
              <span class="insight-icon">${insight.icon || '💡'}</span>
              <span class="insight-text">${insight.text || 'No specific insights available'}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  generateMetricsFromJob(job, realMetrics = null) {
    console.log('🔧 Generating metrics for job:', job);
    console.log('🔬 Real backend metrics available:', realMetrics);
    
    // Valori di default sicuri
    const similarity = job.similarity || 0.5;
    const description = job.Description || '';
    
    try {
      const metrics = {
        matchedSkills: this.extractRealSkills(realMetrics, description, similarity),
        technicalKeywords: this.extractRealKeywords(realMetrics, description),
        softSkills: this.extractSoftSkills(description),
        requiredExperience: this.estimateRequiredExperience(description),
        yourExperience: this.estimateYourExperience(similarity),
        experienceMatch: Math.round(similarity * 100),
        insights: this.generateInsights(job, similarity)
      };
      
      console.log('✅ Generated metrics with real data:', metrics);
      return metrics;
      
    } catch (error) {
      console.error('❌ Error generating metrics:', error);
      
      // Fallback con valori minimi
      return {
        matchedSkills: [],
        technicalKeywords: [],
        softSkills: ['Communication', 'Teamwork'],
        requiredExperience: 3,
        yourExperience: 2,
        experienceMatch: Math.round(similarity * 100),
        insights: [{
          icon: '💡',
          text: 'Analysis in progress - basic match detected'
        }]
      };
    }
  }

  extractSkillsFromDescription(description, similarity) {
    // Espanso database di skills per settore
    const skillsDatabase = {
      frontend: ['React', 'Vue', 'Angular', 'JavaScript', 'TypeScript', 'CSS', 'HTML', 'Webpack'],
      backend: ['Node.js', 'Python', 'Java', 'C#', 'PHP', 'Ruby', 'Go', 'REST APIs', 'GraphQL'],
      database: ['SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch'],
      cloud: ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform'],
      mobile: ['React Native', 'Flutter', 'Swift', 'Kotlin', 'iOS', 'Android'],
      devops: ['Git', 'CI/CD', 'Jenkins', 'Docker', 'Linux', 'Bash'],
      data: ['Python', 'R', 'Pandas', 'NumPy', 'Machine Learning', 'TensorFlow'],
      soft: ['Leadership', 'Communication', 'Problem Solving', 'Team Collaboration', 'Agile', 'Scrum']
    };
    
    const allSkills = Object.values(skillsDatabase).flat();
    const matchedSkills = [];
    const safeDescription = (description || '').toLowerCase();
    const safeSimilarity = similarity || 0.5;
    
    allSkills.forEach(skill => {
      const skillLower = skill.toLowerCase();
      if (safeDescription.includes(skillLower) || 
          safeDescription.includes(skillLower.replace(/\s+/g, '')) ||
          safeDescription.includes(skillLower.replace('.', ''))) {
        
        
        //  Posizione nella descrizione (inizio = più importante)
        const occurrences = (safeDescription.match(new RegExp(skillLower, 'g')) || []).length;
        const positionBonus = safeDescription.indexOf(skillLower) < 100 ? 10 : 0;
        const baseConfidence = safeSimilarity * 100;
        const confidenceBoost = (occurrences * 5) + positionBonus;
        
        const confidence = Math.max(15, Math.min(98, 
          Math.round(baseConfidence + confidenceBoost + (Math.random() * 10 - 5))
        ));
        
        matchedSkills.push({
          name: skill,
          confidence: confidence,
          category: this.getSkillCategory(skill, skillsDatabase)
        });
      }
    });

    // se poche skill trovati, aggiunge skills contestuali
    if (matchedSkills.length < 3) {
      const contextualSkills = this.getContextualSkills(description, safeSimilarity);
      matchedSkills.push(...contextualSkills);
    }

    return matchedSkills
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, 6);
  }

  getSkillCategory(skill, skillsDatabase) {
    for (const [category, skills] of Object.entries(skillsDatabase)) {
      if (skills.includes(skill)) {
        return category;
      }
    }
    return 'general';
  }

  getContextualSkills(description, similarity) {
    const contextualSkills = [];
    const desc = description.toLowerCase();
    
    // analysis based on key words
    if (desc.includes('frontend') || desc.includes('ui') || desc.includes('user interface')) {
      contextualSkills.push(
        { name: 'JavaScript', confidence: Math.round(similarity * 85), category: 'frontend' },
        { name: 'React', confidence: Math.round(similarity * 80), category: 'frontend' }
      );
    }
    
    if (desc.includes('backend') || desc.includes('api') || desc.includes('server')) {
      contextualSkills.push(
        { name: 'Node.js', confidence: Math.round(similarity * 82), category: 'backend' },
        { name: 'REST APIs', confidence: Math.round(similarity * 78), category: 'backend' }
      );
    }
    
    if (desc.includes('data') || desc.includes('analytics') || desc.includes('machine learning')) {
      contextualSkills.push(
        { name: 'Python', confidence: Math.round(similarity * 88), category: 'data' },
        { name: 'SQL', confidence: Math.round(similarity * 75), category: 'database' }
      );
    }
    
    if (desc.includes('cloud') || desc.includes('aws') || desc.includes('azure')) {
      contextualSkills.push(
        { name: 'AWS', confidence: Math.round(similarity * 70), category: 'cloud' },
        { name: 'Docker', confidence: Math.round(similarity * 65), category: 'devops' }
      );
    }

    // always add some soft skills
    contextualSkills.push(
      { name: 'Problem Solving', confidence: Math.round(similarity * 75 + Math.random() * 15), category: 'soft' },
      { name: 'Team Collaboration', confidence: Math.round(similarity * 70 + Math.random() * 15), category: 'soft' }
    );
    
    return contextualSkills;
  }

  extractRealSkills(realMetrics, description, similarity) {
    console.log('🔬 Using real TF-IDF metrics for skills:', realMetrics);
    
    if (realMetrics && typeof realMetrics === 'object') {
      const realSkills = [];
      
      Object.entries(realMetrics).forEach(([keyword, scores]) => {
        if (Array.isArray(scores) && scores.length === 2) {
          const [cvScore, jobScore] = scores;
          
          const avgScore = (cvScore + jobScore) / 2;
          const confidence = Math.round(avgScore * 1000); // Convert to percentage
          
          if (confidence > 5) {
            realSkills.push({
              name: this.formatKeywordName(keyword),
              confidence: Math.min(98, Math.max(10, confidence)),
              category: this.guessSkillCategory(keyword),
              realData: true, 
              cvScore: cvScore,
              jobScore: jobScore
            });
          }
        }
      });
      
      // Ordina per confidence e prendi top 6
      const topSkills = realSkills
        .sort((a, b) => b.confidence - a.confidence)
        .slice(0, 6);
      
      console.log('✅ Real skills extracted:', topSkills);
      
      if (topSkills.length > 0) {
        return topSkills;
      }
    }
    
 
    console.log('📚 Falling back to simulated skills');
    return this.extractSkillsFromDescription(description, similarity);
  }

  extractRealKeywords(realMetrics, description) {
    console.log('🔬 Using real TF-IDF metrics for keywords:', realMetrics);
    
    if (realMetrics && typeof realMetrics === 'object') {
      const keywords = Object.keys(realMetrics)
        .map(kw => this.formatKeywordName(kw))
        .slice(0, 6);
      
      console.log('✅ Real keywords extracted:', keywords);
      
      if (keywords.length > 0) {
        return keywords;
      }
    }
    
    console.log('📚 Falling back to simulated keywords');
    return this.extractTechnicalKeywords(description);
  }

  formatKeywordName(keyword) {
    return keyword
      .split('_').join(' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  guessSkillCategory(keyword) {
    const kw = keyword.toLowerCase();
    
    if (kw.includes('javascript') || kw.includes('react') || kw.includes('vue') || 
        kw.includes('angular') || kw.includes('frontend') || kw.includes('css') || 
        kw.includes('html')) return 'frontend';
        
    if (kw.includes('python') || kw.includes('java') || kw.includes('node') || 
        kw.includes('backend') || kw.includes('api') || kw.includes('server')) return 'backend';
        
    if (kw.includes('sql') || kw.includes('database') || kw.includes('mongo') || 
        kw.includes('postgres')) return 'database';
        
    if (kw.includes('aws') || kw.includes('cloud') || kw.includes('docker') || 
        kw.includes('kubernetes')) return 'cloud';
        
    if (kw.includes('git') || kw.includes('devops') || kw.includes('ci') || 
        kw.includes('jenkins')) return 'devops';
        
    if (kw.includes('machine') || kw.includes('data') || kw.includes('analytics') || 
        kw.includes('ai')) return 'data';
        
    return 'general';
  }

  extractTechnicalKeywords(description) {
    const techKeywordMap = {
      // Frontend
      'javascript': 'JavaScript', 'react': 'React', 'vue': 'Vue.js', 'angular': 'Angular',
      'typescript': 'TypeScript', 'html': 'HTML', 'css': 'CSS',
      // Backend  
      'python': 'Python', 'java': 'Java', 'node.js': 'Node.js', 'nodejs': 'Node.js',
      'php': 'PHP', 'ruby': 'Ruby', 'go': 'Go', 'c#': 'C#',
      // Database
      'sql': 'SQL', 'mongodb': 'MongoDB', 'postgresql': 'PostgreSQL', 'mysql': 'MySQL',
      // Cloud/DevOps
      'aws': 'AWS', 'azure': 'Azure', 'docker': 'Docker', 'kubernetes': 'Kubernetes',
      'git': 'Git', 'jenkins': 'Jenkins',
      // Other
      'api': 'APIs', 'graphql': 'GraphQL', 'rest': 'REST'
    };
    
    const foundKeywords = [];
    const desc = description.toLowerCase();
    
    Object.entries(techKeywordMap).forEach(([keyword, displayName]) => {
      if (desc.includes(keyword)) {
        foundKeywords.push(displayName);
      }
    });
    
    return [...new Set(foundKeywords)].slice(0, 5); // Remove duplicates, max 5
  }

  extractSoftSkills(description) {
    const softSkillMap = {
      'leadership': 'Leadership',
      'lead': 'Leadership', 
      'manage': 'Management',
      'communication': 'Communication',
      'communicate': 'Communication',
      'team': 'Teamwork',
      'collaborate': 'Collaboration',
      'problem solving': 'Problem Solving',
      'analytical': 'Analytical Thinking',
      'creative': 'Creativity',
      'agile': 'Agile',
      'scrum': 'Scrum',
      'mentor': 'Mentoring'
    };
    
    const foundSkills = [];
    const desc = description.toLowerCase();
    
    Object.entries(softSkillMap).forEach(([keyword, displayName]) => {
      if (desc.includes(keyword)) {
        foundSkills.push(displayName);
      }
    });
    
   
    if (foundSkills.length === 0) {
      foundSkills.push('Communication', 'Problem Solving');
    }
    
    return [...new Set(foundSkills)].slice(0, 4); // Remove duplicates, max 4
  }

  estimateRequiredExperience(description) {
    const desc = description.toLowerCase();
    
    if (desc.includes('lead') || desc.includes('principal') || desc.includes('director')) return 8;
    if (desc.includes('senior') || desc.includes('sr.')) return 5;
    if (desc.includes('staff') || desc.includes('architect')) return 7;
    if (desc.includes('mid-level') || desc.includes('intermediate')) return 3;
    if (desc.includes('junior') || desc.includes('entry') || desc.includes('graduate')) return 1;
    if (desc.includes('internship') || desc.includes('intern')) return 0;
    
    let experienceScore = 2; // Base
    if (desc.includes('mentor') || desc.includes('guide')) experienceScore += 2;
    if (desc.includes('architecture') || desc.includes('design systems')) experienceScore += 2;
    if (desc.includes('team') && desc.includes('lead')) experienceScore += 3;
    if (desc.includes('stakeholder') || desc.includes('client facing')) experienceScore += 1;
    
    return Math.min(10, Math.max(0, experienceScore));
  }

  estimateYourExperience(similarity) {
    const baseSimilarity = similarity * 8; // 0-8 anni base
    const variance = (Math.random() - 0.5) * 2; // +/- 1 anno variance
    const experience = Math.round(baseSimilarity + variance);
    
    return Math.min(10, Math.max(0, experience));
  }

  generateInsights(job, similarity) {
    const insights = [];
    const desc = job.Description.toLowerCase();
    const company = job.Company.toLowerCase();
    const role = job.Role.toLowerCase();
    
    // Insight basato su similarity
    if (similarity > 0.9) {
      insights.push({
        icon: '🎯',
        text: 'Perfect match! Your profile aligns excellently with this position.'
      });
    } else if (similarity > 0.85) {
      insights.push({
        icon: '✅',
        text: 'Strong candidate - you meet most key requirements.'
      });
    } else if (similarity > 0.8) {
      insights.push({
        icon: '👍',
        text: 'Good fit - highlight your strongest matching skills in application.'
      });
    } else if (similarity > 0.75) {
      insights.push({
        icon: '📚',
        text: 'Potential match - emphasize transferable skills and growth mindset.'
      });
    } else {
      insights.push({
        icon: '💡',
        text: 'Learning opportunity - consider this for skill development.'
      });
    }

    // Insights basati su company type
    if (company.includes('tech') || company.includes('innovation') || company.includes('startup')) {
      insights.push({
        icon: '🚀',
        text: 'Fast-paced tech environment - emphasize adaptability and learning agility.'
      });
    } else if (company.includes('enterprise') || company.includes('solutions')) {
      insights.push({
        icon: '🏢',
        text: 'Enterprise environment - highlight scalability and process expertise.'
      });
    } else if (company.includes('data') || company.includes('analytics')) {
      insights.push({
        icon: '📊',
        text: 'Data-driven company - showcase analytical and problem-solving skills.'
      });
    }

    if (role.includes('senior') || role.includes('lead')) {
      insights.push({
        icon: '👨‍💼',
        text: 'Leadership role - emphasize mentoring, architecture, and team collaboration.'
      });
    } else if (role.includes('junior') || desc.includes('entry level')) {
      insights.push({
        icon: '🌱',
        text: 'Growth role - highlight eagerness to learn and foundational skills.'
      });
    } else if (role.includes('architect') || role.includes('principal')) {
      insights.push({
        icon: '🏗️',
        text: 'Technical leadership - focus on system design and strategic thinking.'
      });
    }

    // Insights basati su tech stack
    if (desc.includes('react') || desc.includes('frontend')) {
      insights.push({
        icon: '⚛️',
        text: 'Frontend-focused - showcase UI/UX skills and modern framework experience.'
      });
    } else if (desc.includes('backend') || desc.includes('api')) {
      insights.push({
        icon: '⚙️',
        text: 'Backend role - emphasize system architecture and API design skills.'
      });
    } else if (desc.includes('full stack') || desc.includes('fullstack')) {
      insights.push({
        icon: '🔄',
        text: 'Full-stack position - highlight versatility across frontend and backend.'
      });
    }

    // Insights basati su metodologie
    if (desc.includes('agile') || desc.includes('scrum')) {
      insights.push({
        icon: '🔄',
        text: 'Agile environment - mention experience with sprints and iterative development.'
      });
    }

    if (desc.includes('remote') || desc.includes('distributed')) {
      insights.push({
        icon: '🏠',
        text: 'Remote-friendly - highlight self-motivation and async communication skills.'
      });
    }

    // Shuffle per varietà e prendi max 3
    const shuffled = insights.sort(() => Math.random() - 0.5);
    return shuffled.slice(0, 3);
  }

  getMatchDescription(score) {
    if (score >= 90) return 'Outstanding match for your profile!';
    if (score >= 80) return 'Strong match with good potential';
    if (score >= 70) return 'Good fit with some gaps to bridge';
    return 'Potential match worth exploring';
  }

  getExperienceVerdict(match) {
    if (match >= 90) return '✅ Perfect experience level match';
    if (match >= 80) return '👍 Good experience alignment';
    if (match >= 60) return '⚡ Some experience gaps, but manageable';
    return '📚 Focus on highlighting relevant experience';
  }
}