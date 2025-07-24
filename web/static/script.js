class CVJobMatcher {
  constructor() {
    this.initializeElements()
    this.attachEventListeners()
    this.selectedFile = null
  }

  initializeElements() {
    // Sections
    this.uploadSection = document.getElementById("uploadSection")
    this.loadingSection = document.getElementById("loadingSection")
    this.resultsSection = document.getElementById("resultsSection")

    // Upload elements
    this.uploadArea = document.getElementById("uploadArea")
    this.fileInput = document.getElementById("fileInput")
    this.selectedFileDiv = document.getElementById("selectedFile")
    this.fileName = document.getElementById("fileName")
    this.fileSize = document.getElementById("fileSize")
    this.removeFileBtn = document.getElementById("removeFile")
    this.analyzeBtn = document.getElementById("analyzeBtn")

    // Other elements
    this.newSearchBtn = document.getElementById("newSearchBtn")
    this.resultsGrid = document.getElementById("resultsGrid")
  }

  attachEventListeners() {
    // File upload events
    this.uploadArea.addEventListener("click", () => this.fileInput.click())
    this.fileInput.addEventListener("change", (e) => this.handleFileSelect(e))
    this.removeFileBtn.addEventListener("click", () => this.removeFile())
    this.analyzeBtn.addEventListener("click", () => this.analyzeCV())
    this.newSearchBtn.addEventListener("click", () => this.resetToUpload())

    // Drag and drop events
    this.uploadArea.addEventListener("dragover", (e) => this.handleDragOver(e))
    this.uploadArea.addEventListener("dragleave", (e) => this.handleDragLeave(e))
    this.uploadArea.addEventListener("drop", (e) => this.handleDrop(e))

    // Browse text click
    document.querySelector(".browse-text").addEventListener("click", (e) => {
      e.stopPropagation()
      this.fileInput.click()
    })
  }

  handleDragOver(e) {
    e.preventDefault()
    this.uploadArea.classList.add("dragover")
  }

  handleDragLeave(e) {
    e.preventDefault()
    this.uploadArea.classList.remove("dragover")
  }

  handleDrop(e) {
    e.preventDefault()
    this.uploadArea.classList.remove("dragover")

    const files = e.dataTransfer.files
    if (files.length > 0) {
      this.processFile(files[0])
    }
  }

  handleFileSelect(e) {
    const file = e.target.files[0]
    if (file) {
      this.processFile(file)
    }
  }

  processFile(file) {
    // Validate file type
    const allowedTypes = ["application/pdf"]
    if (!allowedTypes.includes(file.type)) {
      alert("Please upload a PDF file.")
      return
    }

    // Validate file size (10MB limit)
    const maxSize = 10 * 1024 * 1024 // 10MB in bytes
    if (file.size > maxSize) {
      alert("File size must be less than 10MB.")
      return
    }

    this.selectedFile = file
    this.displaySelectedFile(file)
  }

  displaySelectedFile(file) {
    this.fileName.textContent = file.name
    this.fileSize.textContent = this.formatFileSize(file.size)

    this.uploadArea.style.display = "none"
    this.selectedFileDiv.style.display = "block"
    this.analyzeBtn.disabled = false
  }

  removeFile() {
    this.selectedFile = null
    this.fileInput.value = ""

    this.uploadArea.style.display = "block"
    this.selectedFileDiv.style.display = "none"
    this.analyzeBtn.disabled = true
  }

  formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes"

    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  async analyzeCV() {
    if (!this.selectedFile) return

    // Show loading section
    this.uploadSection.style.display = "none"
    this.loadingSection.style.display = "block"

    try {
      // Simulate analysis process with progress steps
      await this.simulateAnalysis()

      // Create FormData for file upload
      const formData = new FormData()
      formData.append("cvFile", this.selectedFile)

      // Call the api
      let response
      try {
        response = await fetch("/api/analyze", {
          method: "POST",
          body: formData,
        })

      } catch (error) {
        console.log("New API not available, using fallback...")
        response = await fetch("/upload", {
          method: "POST",
          body: formData,
        })

        if (response.redirected) {
          window.location.href = response.url
          return
        }
      }

      // Handle  API response
      if (response.headers.get("content-type")?.includes("application/json")) {
        const data = await response.json()
        if (!response.ok) {
          throw new Error(data.detail || "Analysis failed")
        }

        // Show results
        this.loadingSection.style.display = "none"
        this.resultsSection.style.display = "block"

        // Display real results from API
        this.displayResults(data.results)
      } else {
        // Handle old API response (HTML redirect)
        if (response.redirected) {
          window.location.href = response.url
        } else {
          throw new Error("Unexpected response format")
        }
      }
    } catch (error) {
      console.error("Error analyzing CV:", error)
      alert("Error analyzing CV: " + error.message + "\n\nUsing mock data for demonstration...")

      // Fallback to mock data for demonstration
      this.loadingSection.style.display = "none"
      this.resultsSection.style.display = "block"
      this.displayResults(this.generateMockResults())
    }
  }

  async simulateAnalysis() {
    const steps = ["step2", "step3"]

    // Step 1 is already active
    await this.delay(1500)

    // Activate step 2
    document.getElementById("step2").classList.add("active")
    await this.delay(2000)

    // Activate step 3
    document.getElementById("step3").classList.add("active")
    await this.delay(1500)
  }

  delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms))
  }

  generateMockResults() {
    // Mock job data - in a real application, this would come from your backend
    const mockJobs = [
      {
        Company: "TechCorp Solutions",
        Role: "Senior Software Engineer",
        Description:
          "We are looking for a passionate Senior Software Engineer to join our dynamic team. You will be responsible for developing scalable web applications, mentoring junior developers, and contributing to architectural decisions. Experience with React, Node.js, and cloud technologies is highly valued.",
        "Job Link": "https://example.com/job1",
        similarity: 0.92,
      },
      {
        Company: "DataFlow Analytics",
        Role: "Full Stack Developer",
        Description:
          "Join our innovative team as a Full Stack Developer where you'll work on cutting-edge data visualization tools. We need someone proficient in modern JavaScript frameworks, Python, and database design. Great opportunity for career growth in a fast-paced environment.",
        "Job Link": "https://example.com/job2",
        similarity: 0.88,
      },
      {
        Company: "CloudTech Innovations",
        Role: "DevOps Engineer",
        Description:
          "We're seeking a skilled DevOps Engineer to help us scale our cloud infrastructure. You'll work with Docker, Kubernetes, AWS, and CI/CD pipelines. Perfect role for someone who loves automation and wants to work with the latest cloud technologies.",
        "Job Link": "https://example.com/job3",
        similarity: 0.85,
      },
      {
        Company: "StartupHub Inc",
        Role: "Frontend Developer",
        Description:
          "Exciting opportunity for a Frontend Developer to shape the user experience of our next-generation platform. We use React, TypeScript, and modern CSS frameworks. You'll collaborate closely with designers and backend developers in an agile environment.",
        "Job Link": "https://example.com/job4",
        similarity: 0.82,
      },
      {
        Company: "Enterprise Solutions Ltd",
        Role: "Software Architect",
        Description:
          "Lead the technical direction as a Software Architect in our enterprise solutions team. You'll design system architectures, evaluate technologies, and guide development teams. Strong background in microservices, distributed systems, and team leadership required.",
        "Job Link": "https://example.com/job5",
        similarity: 0.79,
      },
    ]

    return mockJobs
  }

  displayResults(jobs) {
    this.resultsGrid.innerHTML = ""

    jobs.forEach((job, index) => {
      const jobCard = this.createJobCard(job, index)
      this.resultsGrid.appendChild(jobCard)
    })
  }

  createJobCard(job, index) {
    const card = document.createElement("div")
    card.className = "job-card"
    card.style.animationDelay = `${index * 0.1}s`

    const matchPercentage = Math.round(job.similarity * 100)

    card.innerHTML = `
            <div class="job-header">
                <div class="company-name">${job.Company}</div>
                <h3 class="job-title">${job.Role}</h3>
            </div>
            <p class="job-description">${job.Description}</p>
            <div class="job-footer">
                <div class="match-score">${matchPercentage}% Match</div>
                <a href="${job["Job Link"]}" class="apply-btn" target="_blank" rel="noopener noreferrer">
                    Apply Now
                </a>
            </div>
        `

    return card
  }

  resetToUpload() {
    // Reset all sections
    this.resultsSection.style.display = "none"
    this.loadingSection.style.display = "none"
    this.uploadSection.style.display = "block"

    // Reset file selection
    this.removeFile()

    // Reset progress steps
    document.querySelectorAll(".step").forEach((step) => {
      step.classList.remove("active")
    })
    document.querySelector(".step").classList.add("active")

    // Scroll to top
    window.scrollTo({ top: 0, behavior: "smooth" })
  }
}

// Initialize the application when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new CVJobMatcher()
})

// Add some additional interactive features
document.addEventListener("DOMContentLoaded", () => {
  // Add smooth scrolling for any anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Add keyboard navigation support
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      // Close any modals or reset to upload if in results
      const resultsSection = document.getElementById("resultsSection")
      if (resultsSection.style.display !== "none") {
        document.getElementById("newSearchBtn").click()
      }
    }
  })
})
