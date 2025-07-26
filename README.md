# CV Job Matcher API

[![Python Version](https.img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https.img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is a powerful CV-Job Matching application designed to bridge the gap between job seekers and employers. It leverages Natural Language Processing (NLP) to analyze resumes, compare them against a database of job listings, and rank them based on relevance. Additionally, it includes a web scraping module to dynamically gather fresh job postings from popular platforms.

## 🚀 Live Demo

[LINK OF THE APP.](https://cvjobmatching-a7049acad1b5.herokuapp.com/)

_Note: The live demo runs on a Heroku ECO plan, so it might take a few moments to load._

## ✨ Features

- **📄 CV Analysis & Ranking**: Upload a CV in PDF or DOCX format, and the system will extract its content, analyze it, and match it against a pre-existing dataset of job advertisements. It then returns a list of the most suitable job openings, ranked by relevance.
- **🌐 Dynamic Job Scraping**: Fetch the latest job listings directly from multiple sources, including Indeed, LinkedIn, and InfoJobs.
- **🤖 NLP-Powered Matching**: Utilizes a TF-IDF (Term Frequency-Inverse Document Frequency) vectorizer from `scikit-learn` to intelligently compare the semantic content of a CV with job descriptions, ensuring accurate and meaningful matches.
- **🚀 Fast & Modern API**: Built with FastAPI, providing a high-performance, asynchronous API that is easy to use and well-documented.
- **📦 Deployment**: Includes a `Procfile` for seamless deployment to Heroku.

## ⚖️ Important Note on Data Scraping

The web scraping functionality in this project is provided for demonstration and educational purposes only. The scrapers for Indeed, LinkedIn, and InfoJobs are fully implemented. However, due to potential legal and ethical issues related to scraping proprietary data from these platforms, the live version of this project uses a static, pre-compiled dataset of fictitious job listings (`job_ads.csv`).

**This project does not actively scrape live data from the aforementioned websites.** The scraping code is included to showcase the technical capabilities and for educational purposes. Users interested in using the scraping functionality should be aware of the terms of service of the respective websites and use the scraper responsibly and at their own risk.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **NLP/Machine Learning**: Scikit-learn, Pandas
- **Web Scraping**: BeautifulSoup, Requests
- **Server**: Gunicorn, Uvicorn
- **Data Handling**: PDFMiner, python-multipart

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

Make sure you have Python 3.9 or higher installed on your system.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/cv-job-matching.git
   cd cv-job-matching
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Once the dependencies are installed, you can start the development server using Uvicorn:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## 📖 API Endpoints

The application provides the following API endpoints:

### 1. Health Check

- **Endpoint**: `GET /api/health`
- **Description**: Checks if the API is running and healthy.
- **Success Response (200)**:
  ```json
  {
    "status": "healthy",
    "message": "CV Job Matcher API is running"
  }
  ```

### 2. Analyze CV

- **Endpoint**: `POST /api/analyze`
- **Description**: Uploads a CV file (PDF or DOCX), extracts the text, and returns a list of the top job matches from the database.
- **Request**: `multipart/form-data` with a key `cvFile` holding the CV file.
- **Success Response (200)**:
  ```json
  {
    "success": true,
    "message": "CV analyzed successfully",
    "results": [
      {
        "Title": "Senior Python Developer",
        "Company": "Tech Solutions Inc.",
        "Description": "Seeking a senior Python developer with experience in Django and REST APIs...",
        "Similarity": 0.85
      },
      {
        "Title": "Backend Engineer (Python/Flask)",
        "Company": "Innovatech Ltd.",
        "Description": "We are looking for a backend engineer proficient in Python and Flask...",
        "Similarity": 0.78
      }
    ],
    "total_matches": 2
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: If the file type is invalid or the file is empty.
  - `500 Internal Server Error`: If an unexpected error occurs during processing.

### 3. Scrape Job Postings

- **Endpoint**: `POST /api/scrape`
- **Description**: Triggers a web scraping task to fetch new job listings from specified sources.
- **Request Body**:
  ```json
  {
    "keyword": "python developer",
    "location": "Milan, Italy",
    "sites": ["indeed", "linkedin"],
    "max_pages": 1
  }
  ```
- **Success Response (200)**:
  ```json
  {
    "success": true,
    "message": "Scraping completed for 'python developer'.",
    "total_found": 42,
    "results": [
      {
        "title": "Python Developer",
        "link": "https://it.indeed.com/viewjob?jk=...",
        "description": "We are looking for a Python Developer to join our team...",
        "company": "Example Corp",
        "source": "Indeed"
      }
    ]
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: If the keyword is missing or the request body is not valid JSON.
  - `500 Internal Server Error`: If an internal error occurs during scraping.

## 📂 Project Structure

Here is an overview of the key files and directories in this project:

```
.cv-job-matching/
├── .gitignore
├── main.py             # Main FastAPI application entry point
├── Procfile            # Heroku deployment configuration
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── scraper.py          # Module for scraping job data from various sites
|
├── model/              # Directory for ML model, datasets, and related scripts
│   ├── job_ads.csv         # Dataset of job ads used for matching
│   ├── tfidf_vectorizer.pkl  # Pickled TF-IDF vectorizer model
│   └── train_model.py      # Script to train and save the TF-IDF model
|
└── web/                # Web-related files (API, frontend, etc.)
    ├── api.py          # Defines the main API routes and logic
    ├── utils.py        # Utility functions for text extraction and matching
    ├── index.html      # Simple HTML frontend for file upload
    └── static/         # Static assets (CSS, JS)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
