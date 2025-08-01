# CV Job Matcher API

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![BERT](https://img.shields.io/badge/NLP-SentenceTransformers-orange.svg)](https://www.sbert.net/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced CV-Job Matching application that leverages state-of-the-art Natural Language Processing to intelligently match job seekers with relevant opportunities. The system uses BERT-based sentence transformers for semantic understanding and provides detailed matching analytics with interactive visualizations.

## 🚀 Live Demo

[**Try the Application**](https://cvjobmatching-a7049acad1b5.herokuapp.com/)

_Note: The live demo runs on a Heroku ECO plan, so it might take a few moments to load._

## Features

### AI Matching

- **BERT-Powered Semantic Analysis**: Uses `all-MiniLM-L6-v2` SentenceTransformer model for deep semantic understanding
- **Dual-Algorithm Approach**: Combines BERT embeddings with TF-IDF vectorization for comprehensive analysis
- **Contextual Understanding**: Goes beyond keyword matching to understand job requirements and candidate skills

### Intelligent Metrics & Analytics

- **Detailed Skill Breakdown**: Real-time analysis of technical and soft skills alignment
- **Keyword Analysis**: TF-IDF-based extraction of common keywords between CV and job descriptions
- **AI-Generated Insights**: Contextual recommendations and application strategies

## Technical Architecture

### Machine Learning Pipeline

```
CV Upload → Text Extraction → Preprocessing → BERT Encoding → Similarity Calculation → Results Ranking
                                          ↓
                            TF-IDF Analysis → Keyword Extraction → Metrics Generation
```

### Core Technologies

- **Backend**: Python, FastAPI, Uvicorn
- **ML/NLP**:
  - SentenceTransformers (`all-MiniLM-L6-v2`)
  - Scikit-learn (TF-IDF, Cosine Similarity)
  - Pandas, NumPy
- **Frontend**: Vanilla JavaScript (ES6+), CSS
- **Text Processing**: PDFMiner, python-multipart
- **Web Scraping**: BeautifulSoup, Requests
- **Deployment**: Gunicorn, Heroku

## Caching & Performance

Pre-computed job embeddings for faster matching
Pickle-based model persistence
Efficient vector operations with NumPy
Lazy loading for large datasets

## ⚖️ Important Note on Data Scraping

The web scraping functionality in this project is provided for demonstration and educational purposes only. The scrapers for Indeed, LinkedIn, and InfoJobs are fully implemented. However, due to potential legal and ethical issues related to scraping proprietary data from these platforms, the live version of this project uses a static, pre-compiled dataset of fictitious job listings (`job_ads.csv`).

**This project does not actively scrape live data from the aforementioned websites.** The scraping code is included to showcase the technical capabilities and for educational purposes. Users interested in using the scraping functionality should be aware of the terms of service of the respective websites and use the scraper responsibly and at their own risk.

## Tech Stack

- **Backend**: Python, FastAPI
- **NLP/Machine Learning**: Scikit-learn, Pandas
- **Web Scraping**: BeautifulSoup, Requests
- **Server**: Gunicorn, Uvicorn
- **Data Handling**: PDFMiner, python-multipart

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

### Prerequisites

- Python 3.9 or higher
- 4GB+ RAM (for BERT model loading)

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

## API Endpoints

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
cv-job-matching/
├── 📁 model/                    # ML models and training scripts
│   ├── job_ads.csv             # Curated job dataset
│   ├── tfidf_vectorizer.pkl    # Trained TF-IDF model
│   ├── sentence_embedding_model.pkl  # BERT model cache
│   ├── job_ads_embedding_vectors.pkl # Pre-computed embeddings
│   └── train_model.py          # Model training pipeline
├── 📁 web/                     # Web application components
│   ├── api.py                  # FastAPI routes and logic
│   ├── utils.py                # ML utilities and text processing
│   ├── index.html              # Main application interface
│   └── 📁 static/              # Frontend assets
│       ├── 📁 css/             # Stylesheets
│       ├── 📁 js/              # JavaScript modules
│       │   ├── 📁 components/  # UI components
│       │   ├── 📁 services/    # API services
│       │   └── 📁 utils/       # Utility functions
│       └── style.css           # Main stylesheet
├── main.py                     # FastAPI application entry point
├── scraper.py                  # Web scraping modules
├── requirements.txt            # Python dependencies
└── Procfile                    # Heroku deployment config
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Acknowledgments

- Hugging Face for the excellent SentenceTransformers library
- FastAPI team for the high-performance web framework
- scikit-learn contributors for robust ML tools
- Open Source Community for inspiration and support
